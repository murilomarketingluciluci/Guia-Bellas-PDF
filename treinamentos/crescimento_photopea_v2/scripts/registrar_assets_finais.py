import hashlib,json
from pathlib import Path
from datetime import datetime,timezone
p=Path(__file__).resolve().parents[1]
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
m=json.loads((p/'manifest_photopea.json').read_text(encoding='utf-8-sig'))
assets=[{'page':x['number'],'asset':x['photo']['asset'],'sha256':sha(p/x['photo']['asset']),'box':x['photo']['box']} for x in m['pages'] if x.get('photo')]
(p/'auditoria/assets_selecionados_finais.json').write_text(json.dumps({'timestamp':datetime.now(timezone.utc).isoformat(),'assets':assets,'photo09_refinement':{'prompt':'auditoria/prompts/foto09_refinamento.json','original_preserved':'assets/foto_pessoas_encontro.png','original_sha256':sha(p/'assets/foto_pessoas_encontro.png'),'generated_source_historical':'C:/Users/Murilo/.codex/generated_images/01a13c2c-f2f1-7ff2-bc4c-0d1dd4a714d4/exec-74160c42-2195-4a7b-bdb2-00495f359e20.png','selected':'assets/foto_pessoas_encontro_v2.png','sha256':sha(p/'assets/foto_pessoas_encontro_v2.png'),'reason':'Minimum15%top/bottom safe space after crop; independent visual measurement ~30.3%top/24.1%bottom'}},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
files=[p/'entrega/Crescimento_Photopea_V2.psd',p/'entrega/Crescimento_Photopea_V2.pdf',p/'manifest_photopea.json']+sorted((p/'entrega/pngs').glob('*.png'))
(p/'auditoria/hashes_entrega.json').write_text(json.dumps({'timestamp':datetime.now(timezone.utc).isoformat(),'files':[{'path':x.relative_to(p).as_posix(),'bytes':x.stat().st_size,'sha256':sha(x)} for x in files]},indent=2)+'\n',encoding='utf-8')
print('Assets4; finalfiles',len(files))
