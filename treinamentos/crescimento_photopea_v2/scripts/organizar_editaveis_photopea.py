import json
from montar_photopea import P,js,q
m=json.loads((P/'manifest_photopea.json').read_text(encoding='utf-8-sig'))
b=json.loads((P/'leitura/bases_montagem.json').read_text(encoding='utf-8-sig'))
for page,template,layerid,oldname in [(1,'capa',33,'TREINAMENTO'),(12,'agradecimento',12,'EMPREENDEDORISMO FEMININO')]:
    n=next(x for x in b['templates'][template]['layers'] if x['id']==layerid);t=n['text'];x,y,_,_=n['bbox']
    spec={'name':oldname,'text':t['contents'],'x':x,'y':y,'size':t['size'],'font':t['font'],'color':'#FFFFFF','tracking':t['tracking']}
    name=f"{page:02d} - {m['pages'][page-1]['name']}"
    print(js('var g=app.activeDocument.layerSets.getByName('+q(name)+');g.artLayers.getByName('+q(oldname)+').remove();var l=text(g,'+q(spec)+');app.echoToOE("FIXED_TYPE:"+JSON.stringify(bounds(l)));'))
    m['pages'][page-1]['texts'].append(spec)
# Group each repeated editorial unit into a complete editable folder.
for page,ids,prefix in [(2,range(1,5),'p02-'),(4,range(1,5),'p04-'),(5,range(5,9),'p04-'),(6,range(9,13),'p04-')]:
    p=m['pages'][page-1];name=f"{page:02d} - {p['name']}"
    for number in ids:
        token=prefix+f'{number:02d}'
        names=[t['name'] for t in p['texts'] if t['name'].startswith(token)]
        names += [s['name'] for s in p['shapes'] if token in s['name'] or s['name'].endswith(f'-{number:02d}')]
        if not names:continue
        code='var g=app.activeDocument.layerSets.getByName('+q(name)+');var row=group(g,'+q(f'{number:02d} - bloco editável')+');'
        for n in names:code+='g.artLayers.getByName('+q(n)+').move(row,ElementPlacement.INSIDE);'
        print(js(code))
m['stage']='final'
m['backend']={'editor':'Photopea','api':'Live Messaging postMessage','source_import':'individual original channels/masks in compatible input PSDs; complete original template import failed','editable_content':'native Gotham type layers; rectangles on separate native pixel layers; fixed originals retained as layer assets','photo9_refinement':'assets/foto_pessoas_encontro_v2.png'}
(P/'manifest_photopea.json').write_text(json.dumps(m,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(js('var d=app.activeDocument;for(var i=0;i<d.layerSets.length;i++)d.layerSets[i].visible=d.layerSets[i].name.indexOf("01 -")===0;d.saveToOE("psd");',['trabalho/crescimento_photopea_v2.psd']))
