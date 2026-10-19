import json
from pathlib import Path
p=Path(__file__).resolve().parents[1]/'manifest_photopea.json'
m=json.loads(p.read_text(encoding='utf-8-sig'))
m['template']={'psd':'../../referencias/molde_bellas_aprovado_capa_temas_agradecimento.psd','usage':'Original source assets and masks extracted without changing source; final composition authored via Photopea API. Whole original PSD import failed.'}
p.write_text(json.dumps(m,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
