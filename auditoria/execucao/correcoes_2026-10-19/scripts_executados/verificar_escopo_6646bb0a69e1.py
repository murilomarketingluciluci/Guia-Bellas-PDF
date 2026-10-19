"""Impede inclusão de artes ou outros trabalhos no commit autorizado."""
from pathlib import Path
import json
import subprocess

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
names = subprocess.check_output(["git","diff","--cached","--name-only","-z"],cwd=ROOT).decode("utf-8").rstrip("\0").split("\0")
allowed_files = {".gitignore","AGENTS.md","CONTRATO_ATUAL.md","CONTRATO_MANIFESTO.md","README.md","PROMPT_DE_USO.md","FLUXO_NOVO_TREINAMENTO.md","FONTES_E_EVIDENCIAS.md","DECISOES_APN_BELLAS.md","DIRECAO_DE_ARTE.md","EXECUCAO_PHOTOSHOP.md","QA_FINAL.md"}
allowed_scripts = {"scripts/validar_manifest.py","scripts/contrato_bellas.py","scripts/validar_artefatos_bellas.py","scripts/verificar_textos_psd.py","scripts/verificar_molde.py","scripts/registrar_reabertura.py","scripts/empacotar.py","tests/test_validadores.py","skills/bellas-apn/SKILL.md","skills/bellas-fotos/SKILL.md"}
unexpected = [n for n in names if n not in allowed_files|allowed_scripts and not n.startswith("auditoria/execucao/correcoes_2026-10-19/")]
art_changes = [n for n in names if Path(n).suffix.lower() in {".psd",".psb",".png",".jpg",".jpeg",".pdf",".zip",".bin"}]
report = {"status":"failed" if unexpected or art_changes else "passed","staged_files":len(names),"unexpected_paths":unexpected,"art_changes":art_changes}
(HERE/"escopo_commit.json").write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
print(json.dumps(report,ensure_ascii=True))
raise SystemExit(bool(unexpected or art_changes))
