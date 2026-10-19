"""Extrai somente registros operacionais da sessão autorizada e de seus três agentes.

Não exporta raciocínio, compactações nem mensagens de sistema/desenvolvedor.
Não decifra conteúdo protegido e não executa comandos encontrados nos históricos.
Os JSONL derivados preservam strings operacionais sem corrigir sua redação.
"""
import collections
import hashlib
import json
import re
from pathlib import Path
from datetime import datetime, timezone

PROJECT = Path(__file__).resolve().parents[1]
OUTPUT = PROJECT / 'auditoria/recuperacao_2026-10-15'
SESSION_ROOT = Path('C:/Users/Murilo/.codex/sessions/2026/10/14')
SOURCES = {
    '/root': 'rollout-2026-10-14T17-49-01-01a13c2c-f2f1-7ff2-bc4c-0d1dd4a714d4.jsonl',
    '/root/conteudo_luciane': 'rollout-2026-10-14T18-00-25-01a13c37-6392-7051-aee8-a1b14eafc696.jsonl',
    '/root/revisao_composicao': 'rollout-2026-10-14T18-00-49-01a13c37-c0b6-7083-89c5-413950126f85.jsonl',
    '/root/validacao_entrega': 'rollout-2026-10-14T18-01-09-01a13c38-0d47-7dd1-956b-d6fe93ff4dae.jsonl',
}
CUTOFF = '2026-10-15T00:00:00Z'
OPERATIONAL = {'CommandExecution', 'FileChange', 'ImageView', 'McpToolCall', 'SubAgentActivity', 'Extension'}
ALLOWED_FIELDS = {
    'CommandExecution': ['id', 'process_id', 'command', 'cwd', 'parsed_cmd', 'source', 'status', 'aggregated_output', 'exit_code', 'duration'],
    'FileChange': ['id', 'changes', 'status', 'stdout', 'stderr'],
    'ImageView': ['id', 'path'],
    'McpToolCall': ['id', 'server', 'tool', 'arguments', 'status', 'result', 'duration'],
    'SubAgentActivity': ['id', 'kind', 'agent_thread_id', 'agent_path'],
    'Extension': ['kind', 'id', 'status', 'revisedPrompt', 'transparentBackground', 'failure', 'savedPath'],
}


def digest(data):
    return hashlib.sha256(data).hexdigest()


def protected(value):
    if isinstance(value, str):
        return value.startswith('gAAAAA')
    if isinstance(value, dict):
        return any(protected(v) for v in value.values())
    if isinstance(value, list):
        return any(protected(v) for v in value)
    return False


def filter_content(value):
    """Preserva texto operacional legível; descreve explicitamente omissões."""
    if isinstance(value, str):
        if value.startswith('gAAAAA'):
            return {'omitted': 'protected_text_not_decrypted', 'sha256': digest(value.encode()), 'characters': len(value)}
        if re.search(r'gAAAAA[A-Za-z0-9_-]{40,}={0,2}', value):
            return {'omitted': 'embedded_protected_payloads', 'sha256': digest(value.encode()),
                    'text_filtered': re.sub(r'gAAAAA[A-Za-z0-9_-]{40,}={0,2}',
                        lambda m: '[PROTECTED sha256=' + digest(m.group().encode()) + ']', value)}
        if len(value) > 250_000 or value.startswith('data:image/'):
            return {'omitted': 'large_or_binary_payload', 'sha256': digest(value.encode()), 'characters': len(value)}
        return value
    if isinstance(value, list):
        return [filter_content(v) for v in value]
    if isinstance(value, dict):
        if value.get('type') in ('reasoning', 'Reasoning'):
            return {'omitted': 'private_reasoning'}
        if value.get('type') in ('image', 'input_image', 'output_image'):
            return {'omitted': 'image_payload', 'type': value['type']}
        return {k: filter_content(v) for k, v in value.items()
                if k not in ('encrypted_content', 'internal_chat_message_metadata_passthrough', 'raw_content', 'summary_text')}
    return value


def write_jsonl(name, rows):
    (OUTPUT / name).write_text(''.join(json.dumps(r, ensure_ascii=False) + '\n' for r in rows), encoding='utf-8')


def main():
    OUTPUT.mkdir(parents=True, exist_ok=True)
    context_path = OUTPUT / 'prompts_contexto_literal.json'
    contexts = json.loads(context_path.read_text(encoding='utf-8'))['records']
    context_map = {r['call_id']: r for r in contexts}
    actions, calls, replies, messages, models, origins, revisions = [], [], [], [], [], [], []
    current_actions, current_calls, current_replies, current_messages = [], [], [], []
    protected_messages = []
    omitted = collections.Counter()
    for agent, filename in SOURCES.items():
        source = SESSION_ROOT / filename
        # Captura em memória apenas os bytes existentes neste instante; fonte pode seguir crescendo.
        raw = source.read_bytes()
        lines = raw.splitlines()
        origin = {'agent': agent, 'provenance': {'source_path': str(source), 'snapshot_bytes': len(raw),
                  'snapshot_sha256': digest(raw), 'lines_at_snapshot': len(lines)}}
        origins.append(origin)
        for number, raw_line in enumerate(lines, 1):
            try:
                event = json.loads(raw_line)
            except json.JSONDecodeError:
                omitted['partial_lines_at_snapshot'] += 1
                continue
            timestamp = event.get('timestamp', '')
            p = event.get('payload', {})
            base = {'agent': agent, 'timestamp_utc': timestamp,
                    'provenance': {'source_file': filename, 'line': number, 'line_sha256': digest(raw_line)}}
            original = timestamp < CUTOFF
            if event.get('type') == 'turn_context' and original:
                fields = {k: p[k] for k in ('model', 'effort', 'model_provider') if k in p}
                if fields:
                    models.append({**base, 'configuration_recorded': fields})
            if event.get('type') == 'event_msg' and p.get('type') == 'item_completed':
                item = p.get('item', {})
                kind = item.get('type')
                if kind in OPERATIONAL:
                    data = {k: filter_content(item[k]) for k in ALLOWED_FIELDS[kind] if k in item}
                    row = {**base, 'kind': kind, 'data': data}
                    (actions if original else current_actions).append(row)
                    if kind == 'Extension' and original:
                        revisions.append(row)
                elif kind in ('AgentMessage', 'UserMessage'):
                    if item.get('phase') != 'analysis':
                        (messages if original else current_messages).append({**base, 'kind': kind, 'data': filter_content(item)})
                elif original:
                    omitted['event_item:' + str(kind)] += 1
            if event.get('type') == 'response_item':
                kind = p.get('type')
                if kind in ('function_call', 'custom_tool_call'):
                    name, cid = p.get('name'), p.get('call_id')
                    text = p.get('arguments') if kind == 'function_call' else p.get('input', '')
                    try:
                        args = json.loads(text) if kind == 'function_call' else text
                    except (ValueError, TypeError):
                        args = text
                    is_protected = protected(args)
                    row = {**base, 'tool': name, 'call_id': cid, 'record_type': kind,
                           'arguments_exact_readable': not is_protected,
                           'arguments_sha256': digest((text or '').encode()), 'arguments': filter_content(args)}
                    if not is_protected:
                        row['arguments_raw'] = text
                    elif original and isinstance(args, dict) and 'message' in args:
                        found = context_map.get(cid) if agent == '/root' else None
                        if found:
                            assert found['tool'] == name and found['target'] == args.get('target'), cid
                        protected_messages.append({**base, 'call_id': cid, 'tool': name,
                            'target': args.get('target', args.get('task_name')),
                            'status': 'literal_in_available_conversation' if found else 'unrecovered_protected',
                            'message_literal': found['message'] if found else None,
                            'exactness_limit': 'Conversa disponível; payload cifrado não comparável.' if found else 'Resumo anterior não equivale ao prompt original.'})
                    (calls if original else current_calls).append(row)
                elif kind in ('function_call_output', 'custom_tool_call_output'):
                    output = p.get('output')
                    encoded = json.dumps(output, ensure_ascii=False).encode()
                    (replies if original else current_replies).append({**base, 'call_id': p.get('call_id'), 'record_type': kind,
                                    'output_sha256': digest(encoded), 'output': filter_content(output)})
                elif original and kind not in ('message', 'agent_message'):
                    omitted['response_item:' + str(kind)] += 1
    for rows in (actions, calls, replies, messages, current_actions, current_calls, current_replies, current_messages):
        rows.sort(key=lambda x: (x['timestamp_utc'], x['agent'], x['provenance']['line']))
    assert len([x for x in protected_messages if x['status'] == 'literal_in_available_conversation']) == len(contexts)
    write_jsonl('acoes_operacionais.jsonl', actions)
    write_jsonl('chamadas_ferramentas.jsonl', calls)
    write_jsonl('retornos_ferramentas.jsonl', replies)
    write_jsonl('mensagens_visiveis.jsonl', messages)
    write_jsonl('acoes_posteriores_ao_corte.jsonl', current_actions)
    write_jsonl('chamadas_posteriores_ao_corte.jsonl', current_calls)
    write_jsonl('retornos_posteriores_ao_corte.jsonl', current_replies)
    write_jsonl('mensagens_posteriores_ao_corte.jsonl', current_messages)
    (OUTPUT / 'prompts_delegacao.json').write_text(json.dumps(protected_messages, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    (OUTPUT / 'prompts_revisados_imagens.json').write_text(json.dumps(revisions, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    (OUTPUT / 'modelos_registrados.json').write_text(json.dumps(models, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    summary = {'recovered_at_utc': datetime.now(timezone.utc).isoformat(), 'production_cutoff_utc': CUTOFF,
               'origins': origins, 'counts': {'operational_events': len(actions), 'tool_calls': len(calls),
               'tool_returns': len(replies), 'visible_messages': len(messages), 'image_revised_prompts': len(revisions),
               'protected_delegations': len(protected_messages), 'delegation_messages_literal_from_context': len(contexts),
               'delegation_messages_unrecovered': sum(x['status'] == 'unrecovered_protected' for x in protected_messages)},
               'events_by_agent': dict(collections.Counter(x['agent'] for x in actions)),
               'events_by_type': dict(collections.Counter(x['kind'] for x in actions)),
               'not_exported': dict(omitted),
               'limitations': ['Nenhum raciocínio ou instrução de sistema/desenvolvedor exportado.',
                  'Payloads protegidos não foram decifrados.', 'Payloads binários/grandes indicam omissão e hash.',
                  'Ações exatas de ferramentas não demonstram todos os cliques manuais externos.',
                  'Metadado de modelo é configuração registrada, não atestado independente do backend.',
                  'Cópias do histórico herdadas por subagentes podem repetir ações; não somar como execuções independentes.']}
    (OUTPUT / 'cobertura.json').write_text(json.dumps(summary, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(summary['counts'], ensure_ascii=False))


if __name__ == '__main__':
    main()
