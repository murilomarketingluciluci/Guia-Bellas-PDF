import json
from montar_photopea import P,js,q
m=json.loads((P/'manifest_photopea.json').read_text(encoding='utf-8-sig'))
p=m['pages'][7];name=f"08 - {p['name']}"
print(js('var g=app.activeDocument.layerSets.getByName('+q(name)+');g.artLayers.getByName("marco-01").remove();g.artLayers.getByName("marco-02").remove();g.artLayers.getByName("marco-03").remove();'))
for s in p['shapes']:
    if not s['name'].startswith('marco'):continue
    print(js('var g=app.activeDocument.layerSets.getByName('+q(name)+');rect(g,'+','.join(q(s[k]) for k in ['name','x','y','w','h','color'])+',100);'))
# A global photographic exposure adjustment keeps the actual sky continuous.
name6=f"06 - {m['pages'][5]['name']}"
print(js('var g=app.activeDocument.layerSets.getByName('+q(name6)+');var l=g.artLayers.getByName("FOTO - foto_permanencia_rochas");app.activeDocument.activeLayer=l;l.adjustBrightnessContrast(-30,0);app.echoToOE("PHOTO_EXPOSURE");'))
# Tighten related quote/reference clusters, moving free space to outer edges.
for page,changes in [(7,{'p05-citacao':(265,490),'p05-citacao-referencia':(270,590)}),(11,{'p09-convite':(250,390),'p09-testemunho':(255,520),'p09-testemunho-referencia':(255,655),'p09-fecho':(250,750)})]:
    p=m['pages'][page-1];name=f"{page:02d} - {p['name']}";code='var g=app.activeDocument.layerSets.getByName('+q(name)+');'
    for s in p['texts']:
        if s['name'] not in changes:continue
        s['x'],s['y']=changes[s['name']];code+='place(g.artLayers.getByName('+q(s['name'])+'),'+str(s['x'])+','+str(s['y'])+');'
    print(js(code))
(P/'manifest_photopea.json').write_text(json.dumps(m,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(js('app.activeDocument.saveToOE("psd");',['trabalho/crescimento_photopea_v2.psd']))
