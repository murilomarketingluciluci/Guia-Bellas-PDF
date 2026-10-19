import json,hashlib,shutil
from montar_photopea import P,REPO,js,load,q
from PIL import Image,ImageChops
m=json.loads((P/'manifest_photopea.json').read_text(encoding='utf-8-sig'))
out=P/'entrega';out.mkdir(exist_ok=True)
psd=out/'Crescimento_Photopea_V2.psd';shutil.copy2(P/'trabalho/crescimento_photopea_v2.psd',psd)
def export(folder):
    for p in m['pages']:
        name=f"{p['number']:02d} - {p['name']}"
        js('var d=app.activeDocument;for(var i=0;i<d.layerSets.length;i++)d.layerSets[i].visible=d.layerSets[i].name==='+q(name)+';d.saveToOE("png");',[f'{folder}/pagina_{p["number"]:02d}.png'])
        print(folder,p['number'],flush=True)
export('entrega/pngs')
js('app.activeDocument.close(SaveOptions.DONOTSAVECHANGES);app.echoToOE("CLOSED_NATIVE_MASTER");')
load('entrega/Crescimento_Photopea_V2.psd')
report=js('var pages=[];function collect(g,path,out){for(var i=0;i<g.artLayers.length;i++){var l=g.artLayers[i];out.push({name:l.name,path:path,visible:l.visible,opacity:l.opacity,bounds:bounds(l)});}for(var i=0;i<g.layerSets.length;i++)collect(g.layerSets[i],path+"/"+g.layerSets[i].name,out);}var d=app.activeDocument;for(var i=0;i<d.layerSets.length;i++){var g=d.layerSets[i],ls=[];collect(g,g.name,ls);pages.push({name:g.name,layers:ls});}app.echoToOE("INVENTORY:"+JSON.stringify(pages));')
pages=json.loads(next(x[len('INVENTORY:'):] for x in report['echoes'] if x.startswith('INVENTORY:')))
pages.sort(key=lambda p:int(p['name'].split(' - ')[0]))
data={'psd_sha256':hashlib.sha256(psd.read_bytes()).hexdigest(),'source':'actual saved PSD reopened via Photopea ArrayBuffer','pages':pages,'api_action_id':report['id']}
(P/'auditoria/reabertura_psd.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
export('auditoria/reabertura_pngs')
checks=[]
for p in m['pages']:
    name=f'pagina_{p["number"]:02d}.png'
    with Image.open(out/'pngs'/name) as a,Image.open(P/'auditoria/reabertura_pngs'/name) as b:
        equal=a.size==b.size and ImageChops.difference(a.convert('RGB'),b.convert('RGB')).getbbox() is None
    checks.append({'page':p['number'],'pixels_identical_after_reopen':equal})
(P/'auditoria/pixels_reabertura.json').write_text(json.dumps({'all_pass':all(x['pixels_identical_after_reopen'] for x in checks),'checks':checks},indent=2)+'\n',encoding='utf-8')
if not all(x['pixels_identical_after_reopen'] for x in checks):raise RuntimeError('Reopened PSD renders differently')
print('12/12 reopened page pixels identical',data['psd_sha256'])
