import json
from pathlib import Path
from montar_photopea import P,js,import_asset,q
data=json.loads((P/'leitura/base_molde_extraida.json').read_text(encoding='utf-8-sig'))
def walk(ns):
    for n in ns:
        yield n
        yield from walk(n.get('children',[]))
nodes={n['id']:n for n in walk(data['tree'])}
manifest=json.loads((P/'manifest_photopea.json').read_text(encoding='utf-8-sig'))
for number in [1,12]:
    p=next(x for x in manifest['pages'] if x['number']==number);name=f"{number:02d} - {p['name']}"
    print(js('var d=app.activeDocument;for(var i=0;i<d.layerSets.length;i++)d.layerSets[i].visible=false;var g=group(null,'+q(name)+');rect(g,"FUNDO",0,0,1920,1080,"#FBA9C3",100);app.echoToOE("FIXED_PAGE_CREATED");'))
    for sourceid in ([28] if number==1 else [5,6]):
        print(import_asset(f'assets/base_molde_compativel/camada_{sourceid:03d}.psd',name,'FOTO FIXA ORIGINAL - '+str(sourceid),0,0,opacity=None))
    if number==1:
        for sourceid in [29,33]:
            n=nodes[sourceid];print(import_asset(n['pixel_cache']['path'],name,n['name'],n['bbox_px'][0],n['bbox_px'][1]))
        # The approved swatch/label color was measured from approved exported PNG.
        print(js('var g=app.activeDocument.layerSets.getByName('+q(name)+');rect(g,"ETIQUETA TREINAMENTO",936,336,649,51,"#C87290",100);'))
        # Bring its original lettering above the native color restoration.
        print(js('var g=app.activeDocument.layerSets.getByName('+q(name)+');g.artLayers.getByName("TREINAMENTO").move(g,ElementPlacement.INSIDE);'))
        title={'name':'p01-titulo','text':'Crescimento','x':936,'y':428,'size':130.70151814288087,'font':'Gotham-Book','color':'#FFFFFF','tracking':-70,'leading':156.84}
    else:
        for sourceid in [11,12,13,15,16,17,18]:
            n=nodes[sourceid];print(import_asset(n['pixel_cache']['path'],name,n['name'],n['bbox_px'][0],n['bbox_px'][1]))
        title={'name':'p12-agradecimento','text':'OBRIGADA!','x':638,'y':494,'size':123.30260638374024,'font':'Gotham-Light','color':'#FFFFFF','tracking':-70,'leading':123.30260638374024}
    p['texts']=[title]
    print(js('var g=app.activeDocument.layerSets.getByName('+q(name)+');var l=text(g,'+q(title)+');app.echoToOE("FIXED_TEXT:"+JSON.stringify(bounds(l)));'))
    print(js('app.activeDocument.saveToOE("png");',[f'provas/pagina_{number:02d}.png']))
    print(js('app.activeDocument.saveToOE("psd");',['trabalho/crescimento_photopea_v2.psd']))
(P/'manifest_photopea.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
