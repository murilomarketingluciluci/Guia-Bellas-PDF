"""Confere os links locais dos pontos de entrada consolidados."""
from pathlib import Path
import json
import re

ROOT = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parent
names = ["AGENTS.md","CONTRATO_ATUAL.md","CONTRATO_MANIFESTO.md","README.md","PROMPT_DE_USO.md","FLUXO_NOVO_TREINAMENTO.md","QA_FINAL.md","skills/bellas-apn/SKILL.md","skills/bellas-fotos/SKILL.md"]
errors = []
for name in names:
    path = ROOT/name
    text = path.read_text(encoding="utf-8-sig")
    for target in re.findall(r"\]\(([^)]+)\)",text):
        if target.startswith(("https:","http:","#")):
            continue
        if not (path.parent/target.split("#")[0]).exists():
            errors.append(name+": "+target)
before_names = ["AGENTS.md","PROMPT_DE_USO.md","FLUXO_NOVO_TREINAMENTO.md","skills/bellas-apn/SKILL.md","skills/bellas-fotos/SKILL.md"]
before = sum(len((HERE/"instrucoes_antes"/n).read_text(encoding="utf-8-sig").split()) for n in before_names)
after = sum(len((ROOT/n).read_text(encoding="utf-8-sig").split()) for n in before_names+["CONTRATO_ATUAL.md"])
report = {"status":"failed" if errors else "passed","documents_checked":len(names),"broken_links":errors,"entrypoint_words_before":before,"entrypoint_words_after_including_contract":after,"interpretation":"Contagem de palavras mede redução de duplicação, não prova mudança de comportamento criativo."}
(HERE/"documentacao_conferida.json").write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
print(json.dumps(report,ensure_ascii=True,indent=2))
raise SystemExit(bool(errors))
