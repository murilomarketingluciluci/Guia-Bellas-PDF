import re,json
from pathlib import Path
from datetime import datetime,timezone
p=Path(__file__).resolve().parents[1]
docs=[p/'QA_FINAL.md',p/'entrega/LEIA-ME.md',p/'auditoria/DECISOES_FINAIS.md',p/'auditoria/SESSAO.md',p/'auditoria/INDICE_EVIDENCIAS.md']
bad=[];count=0
for f in docs:
    for target in re.findall(r'\]\(([^)]+)\)',f.read_text(encoding='utf-8-sig')):
        if target.startswith(('https:','http:','#')):continue
        count+=1
        if not (f.parent/target).resolve().exists():bad.append({'file':f.relative_to(p).as_posix(),'target':target})
d={'timestamp':datetime.now(timezone.utc).isoformat(),'checked_links':count,'broken_links':bad,'scope':'final delivery index, QA and principal audit documents'}
(p/'auditoria/links_fechamento.json').write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(d,ensure_ascii=False))
if bad:raise SystemExit(1)
