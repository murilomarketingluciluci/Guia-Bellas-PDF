"""Preserva as diretrizes correntes e hashes dos artefatos, sem modificar a arte."""
from pathlib import Path
import hashlib
import json
import shutil

project = Path(__file__).resolve().parents[1]
repo = project.parents[1]
snapshot = project / 'auditoria/diretrizes_no_fechamento'
rules = ['AGENTS.md', 'DECISOES_APN_BELLAS.md', 'FLUXO_NOVO_TREINAMENTO.md',
         'MODELO_REUTILIZAVEL.md', 'PROMPT_DE_USO.md', 'QA_FINAL.md',
         'skills/bellas-apn/SKILL.md', 'skills/bellas-fotos/SKILL.md']
for relative in rules:
    target = snapshot / relative
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(repo / relative, target)

hashes = []
for path in sorted(project.rglob('*')):
    if not path.is_file() or '__pycache__' in path.parts or path.name == 'hashes_artefatos.json':
        continue
    with path.open('rb') as binary:
        digest = hashlib.file_digest(binary, 'sha256').hexdigest()
    hashes.append({'path': path.relative_to(project).as_posix(), 'bytes': path.stat().st_size,
                   'sha256': digest})
(project / 'auditoria/hashes_artefatos.json').write_text(
    json.dumps({'date': '2026-10-14', 'files': hashes}, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(f'{len(hashes)} arquivos registrados; {len(rules)} diretrizes preservadas.')
