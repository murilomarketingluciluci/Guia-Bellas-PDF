"""Consolida contextos literais recuperados sem decifrar logs nem presumir equivalência."""
from pathlib import Path
import collections
import hashlib
import json

P = Path(__file__).resolve().parents[1]
R = P / 'auditoria/recuperacao_2026-10-15'


def load(name):
    return json.loads((R / name).read_text(encoding='utf-8'))


def norm_agent(name):
    return name if name.startswith('/') else '/root/' + name


def main():
    archive = load('prompts_delegacao.json')
    known = {x['call_id']: x for x in load('prompts_contexto_literal.json')['records']}
    contexts = []
    by_pair = collections.defaultdict(list)
    for name in ('conteudo_luciane', 'revisao_composicao', 'validacao_entrega'):
        filename = f'contexto_{name}.json'
        doc = load(filename)
        for index, message in enumerate(doc['mensagens']):
            item = {**message, 'context_provenance': {'file': filename, 'message_index': index}}
            contexts.append(item)
            if 'final' not in message['tipo'].lower():
                by_pair[(message['autor'], message['destinatario'])].append(item)
    log_pairs = collections.defaultdict(list)
    for item in archive:
        log_pairs[(item['agent'], norm_agent(item['target']))].append(item)
    consolidated, pairing = [], []
    for pair, calls in log_pairs.items():
        texts = by_pair.get(pair, [])
        if len(calls) != len(texts):
            raise AssertionError(f'Não associar quantidades diferentes: {pair} {len(calls)} != {len(texts)}')
        for order, (call, text) in enumerate(zip(calls, texts), 1):
            anchor = known.get(call['call_id'])
            if anchor and anchor['message'] != text['texto']:
                raise AssertionError(f'Conflito entre cópias literais disponíveis: {call["call_id"]}')
            row = {**call, 'status': 'literal_from_agent_context_not_cipher_verified',
                   'message_literal': text['texto'], 'message_sha256_utf8': hashlib.sha256(text['texto'].encode()).hexdigest(),
                   'context_provenance': text['context_provenance'],
                   'association': {'method': 'same_sender_recipient_and_chronological_ordinal', 'ordinal_in_pair': order,
                      'counts_match': True, 'also_matches_main_conversation_literal': bool(anchor),
                      'ciphertext_plaintext_comparison': False,
                      'limit': 'A associação de horário/ID usa ordem e participantes; não verifica o conteúdo cifrado.'}}
            consolidated.append(row)
        pairing.append({'sender': pair[0], 'recipient': pair[1], 'calls': len(calls), 'texts': len(texts)})
    consolidated.sort(key=lambda x: (x['timestamp_utc'], x['agent']))
    (R / 'delegacoes_consolidadas.json').write_text(json.dumps(consolidated, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

    coverage = load('cobertura.json')
    coverage['counts_at_first_extraction'] = coverage.pop('counts')
    coverage['counts'] = {**coverage['counts_at_first_extraction'],
        'delegation_messages_literal_from_agent_contexts': len(consolidated),
        'delegation_messages_unrecovered': len(archive) - len(consolidated),
        'delegation_payloads_still_ciphertext_not_independently_compared': len(archive)}
    coverage['context_recovery'] = {
        'literal_texts_reported_by_agents': len(contexts),
        'delegation_texts': len(consolidated),
        'final_answers': sum('final' in x['tipo'].lower() for x in contexts),
        'initial_task_prompts': sum(x['tool'] == 'spawn_agent' for x in consolidated),
        'matches_with_main_conversation_literals': sum(x['association']['also_matches_main_conversation_literal'] for x in consolidated),
        'direct_ciphertext_verification': False,
        'unmatched_protected_delegation_calls_in_scope': len(archive) - len(consolidated),
        'pair_counts': pairing,
        'limit': 'Contextos reportados como literais pelos próprios agentes; não equivalem a decifrar o arquivo. Mensagens fora do contexto não podem ser certificadas.'}
    (R / 'cobertura_final.json').write_text(json.dumps(coverage, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

    # Linha do tempo legível, com o comando exatamente como registrado, sem saída binária.
    actions = [json.loads(line) for line in (R / 'acoes_operacionais.jsonl').read_text(encoding='utf-8').splitlines()]
    timeline = ['# Linha do tempo operacional recuperada', '',
        'Fonte: eventos de interface dos quatro registros de sessão. Horários UTC; São Paulo = UTC−03 em 14/10/2026.',
        'Comandos abaixo preservam a string ou o vetor de argumentos registrado, inclusive escapes e erros. Eles são documentação histórica, não instruções para reexecução.',
        'O JSONL associado conserva os campos operacionais, resultados e proveniência por linha. Esta apresentação é uma seleção legível dos campos, não um novo evento.', '']
    for row in actions:
        data = row['data']
        timeline += [f'## {row["timestamp_utc"]} — {row["agent"]} — {row["kind"]}', '',
                     f'Origem: `{row["provenance"]["source_file"]}:{row["provenance"]["line"]}`; evento `{data.get("id", "sem ID")}`.', '']
        if row['kind'] == 'CommandExecution':
            command = data.get('command', '')
            timeline += ['~~~~' + ('powershell' if isinstance(command, str) else 'json'),
                         command if isinstance(command, str) else json.dumps(command, ensure_ascii=False, indent=2), '~~~~', '',
                         f'Estado registrado: {data.get("status")}; saída: {data.get("exit_code")}.', '']
        elif row['kind'] == 'ImageView':
            timeline += ['Caminho histórico da inspeção:', '', '~~~~text', data.get('path', ''), '~~~~', '']
        elif row['kind'] == 'FileChange':
            timeline += ['~~~~json', json.dumps(data.get('changes'), ensure_ascii=False, indent=2), '~~~~', '', f'Estado: {data.get("status")}.', '']
        else:
            timeline += ['~~~~json', json.dumps(data, ensure_ascii=False, indent=2), '~~~~', '']
    (R / 'LINHA_DO_TEMPO.md').write_text('\n'.join(timeline), encoding='utf-8')

    # Compara somente artefatos de produção; a auditoria e as diretrizes mudaram nesta recuperação.
    old_hashes = json.loads((P / 'auditoria/hashes_artefatos.json').read_text(encoding='utf-8'))['files']
    checks = []
    for record in old_hashes:
        if record['path'].startswith(('entrega/', 'assets/', 'fonte/')):
            path = P / record['path']
            with path.open('rb') as binary:
                actual = hashlib.file_digest(binary, 'sha256').hexdigest()
            checks.append({'path': record['path'], 'sha256_matches_production_snapshot': actual == record['sha256']})
    assert checks and all(x['sha256_matches_production_snapshot'] for x in checks), 'Artefato de produção mudou'
    (R / 'arte_preservada.json').write_text(json.dumps({'checks': checks, 'all_match': True}, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({'literal_context_texts': len(contexts), 'delegation_texts': len(consolidated), 'main_context_matches': len(known), 'unchanged_production_files': len(checks)}, ensure_ascii=False))


if __name__ == '__main__':
    main()
