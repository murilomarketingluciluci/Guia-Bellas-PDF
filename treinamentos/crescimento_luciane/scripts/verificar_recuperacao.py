"""Confere extratos contra as linhas originais e gera evidência do fechamento."""
from pathlib import Path
import collections
import hashlib
import json
import recuperar_auditoria as extract

P, R = extract.PROJECT, extract.OUTPUT


def rows(name):
    return [json.loads(x) for x in (R / name).read_text(encoding='utf-8').splitlines()]


def main():
    sources = {filename: (extract.SESSION_ROOT / filename).read_bytes().splitlines() for filename in extract.SOURCES.values()}
    counts = collections.Counter()
    coverage = json.loads((R / 'cobertura_final.json').read_text(encoding='utf-8'))
    for origin in coverage['origins']:
        info = origin['provenance']
        raw = Path(info['source_path']).read_bytes()[:info['snapshot_bytes']]
        assert hashlib.sha256(raw).hexdigest() == info['snapshot_sha256']
        counts['source_snapshots_verified'] += 1
    for name in ('acoes_operacionais.jsonl', 'chamadas_ferramentas.jsonl', 'retornos_ferramentas.jsonl',
                 'acoes_posteriores_ao_corte.jsonl', 'chamadas_posteriores_ao_corte.jsonl',
                 'retornos_posteriores_ao_corte.jsonl'):
        for row in rows(name):
            origin = row['provenance']
            raw = sources[origin['source_file']][origin['line'] - 1]
            assert hashlib.sha256(raw).hexdigest() == origin['line_sha256'], (name, origin)
            event = json.loads(raw)
            payload = event['payload']
            assert event['timestamp'] == row['timestamp_utc']
            if 'kind' in row:
                item = payload['item']
                assert row['kind'] in extract.OPERATIONAL
                assert row['kind'] == item['type']
                expected = {k: extract.filter_content(item[k]) for k in extract.ALLOWED_FIELDS[item['type']] if k in item}
                assert expected == row['data']
                counts['operational_rows_verified'] += 1
            elif 'tool' in row:
                text = payload.get('arguments', payload.get('input', ''))
                assert hashlib.sha256(text.encode()).hexdigest() == row['arguments_sha256']
                if row['arguments_exact_readable']:
                    assert row['arguments_raw'] == text
                    counts['readable_tool_arguments_verified'] += 1
                counts['tool_call_rows_verified'] += 1
            else:
                assert row['output'] == extract.filter_content(payload.get('output'))
                counts['tool_return_rows_verified'] += 1
    consolidated = json.loads((R / 'delegacoes_consolidadas.json').read_text(encoding='utf-8'))
    for row in consolidated:
        where = row['context_provenance']
        context = json.loads((R / where['file']).read_text(encoding='utf-8'))
        literal = context['mensagens'][where['message_index']]['texto']
        assert literal == row['message_literal']
        assert hashlib.sha256(literal.encode()).hexdigest() == row['message_sha256_utf8']
    counts['context_literals_copied_without_normalization'] = len(consolidated)
    assert coverage['context_recovery']['matches_with_main_conversation_literals'] == 7
    counts['literal_anchors_match_main_and_agent_context'] = 7
    assert all(x['sha256_matches_production_snapshot'] for x in json.loads((R / 'arte_preservada.json').read_text(encoding='utf-8'))['checks'])
    counts['production_files_unchanged'] = len(json.loads((R / 'arte_preservada.json').read_text(encoding='utf-8'))['checks'])
    settings = json.loads((R / 'modelos_registrados.json').read_text(encoding='utf-8'))
    assert {x['agent'] for x in settings} == set(extract.SOURCES)
    assert all(x['configuration_recorded']['model'] == 'gpt-6.1-sol' and x['configuration_recorded']['effort'] == 'high' for x in settings)
    # Compara literalmente os prompts retornados como revisados e as fotos selecionadas.
    generated = json.loads((R / 'prompts_revisados_imagens.json').read_text(encoding='utf-8'))
    prompts = json.loads((P / 'auditoria/prompts_imagens.json').read_text(encoding='utf-8'))
    image_links = []
    for item in generated:
        data = item['data']
        match = [x for x in prompts if x['prompt'] == data['revisedPrompt']]
        if len(match) != 1:
            image_links.append({'event_id': data['id'], 'prompt_matches_sent_prompt_literally': False})
            continue
        asset = P / 'assets' / match[0]['asset']
        source = Path(data['savedPath'])
        same = source.is_file() and hashlib.sha256(source.read_bytes()).digest() == hashlib.sha256(asset.read_bytes()).digest()
        image_links.append({'event_id': data['id'], 'asset': 'assets/' + match[0]['asset'],
            'prompt_matches_sent_prompt_literally': True, 'generated_file_matches_selected_asset': same})
    (R / 'correspondencia_imagens.json').write_text(json.dumps(image_links, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    counts['image_prompts_literally_match_sent_prompts'] = sum(x['prompt_matches_sent_prompt_literally'] for x in image_links)
    counts['generated_images_match_selected_assets'] = sum(x.get('generated_file_matches_selected_asset', False) for x in image_links)
    (R / 'verificacao_recuperacao.json').write_text(json.dumps({'status': 'passed', 'checks': counts,
       'not_certified': ['Equivalência de texto claro a payload cifrado.', 'Mensagens fora do contexto disponível.',
                         'Execução física de ações externas não registradas.', 'Identidade efetiva do backend a partir de configuração.']}, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

    # Exporta três prompts iniciais para leitura direta, sem mudar nem acrescentar uma linha.
    for row in consolidated:
        if row['tool'] == 'spawn_agent':
            (R / f'prompt_inicial_{row["target"]}.txt').write_text(row['message_literal'], encoding='utf-8')

    # Complemento atual tem seu próprio snapshot; não sobrescreve diretrizes/hashes de 14/10.
    repo = P.parents[1]
    changed_rules = ['AGENTS.md', 'DECISOES_APN_BELLAS.md', 'FLUXO_NOVO_TREINAMENTO.md', 'QA_FINAL.md',
                     'DOCUMENTACAO_DA_EXECUCAO.md', 'templates/registro_execucao.json']
    snapshot = R / 'diretrizes_apos_recuperacao'
    for relative in changed_rules:
        dest = snapshot / relative
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes((repo / relative).read_bytes())
    files = []
    selected = list(R.rglob('*')) + [P / 'LEIA_ME.md', P / 'auditoria/DELEGACOES.md', P / 'auditoria/SESSAO.md']
    selected += [P / 'scripts' / name for name in ('recuperar_auditoria.py', 'consolidar_recuperacao.py', 'verificar_recuperacao.py')]
    for path in sorted(set(selected)):
        if not path.is_file() or path.name == 'hashes_recuperacao.json':
            continue
        with path.open('rb') as data:
            sha = hashlib.file_digest(data, 'sha256').hexdigest()
        files.append({'path': path.relative_to(P).as_posix(), 'bytes': path.stat().st_size, 'sha256': sha})
    (R / 'hashes_recuperacao.json').write_text(json.dumps({'date': '2026-10-15', 'files': files,
        'note': 'Complemento; hashes_artefatos.json de 14/10 preservado. Arquivos de sessão vivos têm ponto de corte e hashes de captura no relatório.'}, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({'status': 'passed', 'checks': counts, 'hashed_files': len(files)}, ensure_ascii=False))


if __name__ == '__main__':
    main()
