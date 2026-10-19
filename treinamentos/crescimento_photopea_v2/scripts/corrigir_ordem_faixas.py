import json
from montar_photopea import P,js,q
m=json.loads((P/'manifest_photopea.json').read_text(encoding='utf-8-sig'))
p=m['pages'][5];name=f"06 - {p['name']}"
for number in range(9,13):
    prefix=f'p04-{number:02d}'
    code='var g=app.activeDocument.layerSets.getByName('+q(name)+');var row=g.layerSets.getByName('+q(f'{number:02d} - bloco editável')+');'
    for t in p['texts']:
        if t['name'].startswith(prefix):code+='row.artLayers.getByName('+q(t['name'])+').move(row,ElementPlacement.INSIDE);'
    print(js(code))
print(js('var d=app.activeDocument;for(var i=0;i<d.layerSets.length;i++)d.layerSets[i].visible=d.layerSets[i].name.indexOf("01 -")===0;d.saveToOE("psd");',['trabalho/crescimento_photopea_v2.psd']))
