import json
from montar_photopea import P,js,import_asset,q
manifest=json.loads((P/'manifest_photopea.json').read_text(encoding='utf-8-sig'))
p=next(x for x in manifest['pages'] if x['number']==9);name=f"09 - {p['name']}"
p['photo']['asset']='assets/foto_pessoas_encontro_v2.png'
print(import_asset(p['photo']['asset'],name,'FOTO NOVA REENQUADRADA',0,0,photo=[700,1080]))
print(js('var g=app.activeDocument.layerSets.getByName('+q(name)+');var novo=g.artLayers.getByName("FOTO NOVA REENQUADRADA");var old=g.artLayers.getByName("FOTO - foto_pessoas_encontro");novo.move(old,ElementPlacement.PLACEBEFORE);old.remove();novo.name="FOTO - foto_pessoas_encontro_v2";app.echoToOE("PHOTO_REPLACED");'))
# Restore approved RGB values for the fixed palette squares from approved PNG.
for p in manifest['pages']:
    if p['number']==12:continue # Closing is a fixed original composition.
    name=f"{p['number']:02d} - {p['name']}"
    colors=['#C6859B','#E79FB7','#EEEEED'] if p['theme']=='escuro' else ['#C27A94','#F4B1C7','#EEEEED']
    code='var g=app.activeDocument.layerSets.getByName('+q(name)+');'
    for i,(x,w) in enumerate([(1756,30),(1796,29),(1834,29)]):code+='rect(g,"COR APROVADA '+str(i+1)+'",'+str(x)+',53,'+str(w)+',30,'+q(colors[i])+',100);'
    print(js(code))
(P/'manifest_photopea.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(js('app.activeDocument.saveToOE("psd");',['trabalho/crescimento_photopea_v2.psd']))
