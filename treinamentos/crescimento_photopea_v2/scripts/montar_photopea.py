"""Author pages only through official Photopea Live Messaging bridge.
Source JSON and individual cached assets are read, not rendered, by this runner.
Every script is snapshotted by the bridge before execution.
"""
import json,time,urllib.request,sys,argparse
from pathlib import Path
P=Path(__file__).resolve().parents[1]
REPO=P.parents[1]
LIB=(P/'scripts/photopea_funcoes.jsx').read_text(encoding='utf-8')
def call(job):
    req=urllib.request.Request('http://127.0.0.1:8876/run',data=json.dumps(job,ensure_ascii=False).encode(),headers={'Content-Type':'application/json'})
    with urllib.request.urlopen(req,timeout=240) as r: out=json.load(r)
    for e in out.get('echoes',[]):
        if isinstance(e,str) and e.startswith('ERROR:'): raise RuntimeError(e)
    return out
def js(code,outputs=None):
    return call({'script':LIB+'\ntry{'+code+'\n}catch(e){app.echoToOE("ERROR:"+e.message+" "+e);}', 'outputs':outputs or []})
def load(asset):return call({'load':(P/asset).relative_to(REPO).as_posix()})
def q(x):return json.dumps(x,ensure_ascii=False)
def import_asset(asset,page,name,x,y,opacity=100,blend=None,photo=None):
    load(asset)
    if photo:
        w,h=photo
        # Assets are all 1024x1536; resize proportionately, crop centered in editor.
        rw=round(1024*max(w/1024,h/1536));rh=round(1536*max(w/1024,h/1536))
        dx=(rw-w)/2;dy=(rh-h)/2
        js(f'app.activeDocument.resizeImage({rw},{rh});app.echoToOE("RESIZED");')
        js(f'app.activeDocument.crop([{dx},{dy},{dx+w},{dy+h}]);app.echoToOE("CROPPED");')
    token='INPUT_'+Path(asset).stem
    js('app.activeDocument.layers[0].name='+q(token)+';app.activeDocument.layers[0].duplicate(app.documents[0],ElementPlacement.PLACEATBEGINNING);app.echoToOE("DUPLICATED");')
    js('app.activeDocument.close(SaveOptions.DONOTSAVECHANGES);app.echoToOE("SOURCE_CLOSED");')
    code='app.echoToOE("PLACE_START");var dst=app.activeDocument;var l=findLayer(dst,'+q(token+' copy')+');if(!l)l=findLayer(dst,'+q(token)+');app.echoToOE("FOUND:"+(l?1:0));'
    code+='l.name='+q(name)+';app.echoToOE("RENAMED");l.translate('+q(x)+','+q(y)+');app.echoToOE("TRANSLATED");'
    if opacity is not None:code+='l.opacity='+str(opacity)+';'
    if blend:code+='l.blendMode=BlendMode.'+blend+';'
    code+='var parent=dst.layerSets.getByName('+q(page)+');app.echoToOE("PARENT:"+(parent?1:0));for(var i=0;i<dst.layerSets.length;i++)app.echoToOE("GROUPNAME:"+dst.layerSets[i].name);l.move(parent,ElementPlacement.INSIDE);app.echoToOE("IMPORTED:"+l.name);'
    return js(code)
def main():
    a=argparse.ArgumentParser();a.add_argument('--init',action='store_true');a.add_argument('--page',type=int);a.add_argument('--export',action='store_true');args=a.parse_args()
    manifest=json.loads((P/'manifest_photopea.json').read_text(encoding='utf-8-sig'))
    if args.init:
        print(js('while(app.documents.length)app.activeDocument.close(SaveOptions.DONOTSAVECHANGES);app.documents.add(1920,1080,72,"Crescimento Photopea V2");app.echoToOE("CREATED_MASTER");'))
    if args.page:
        p=next(v for v in manifest['pages'] if v['number']==args.page);name=f"{p['number']:02d} - {p['name']}";p['group_name']=name
        (P/'auditoria').mkdir(exist_ok=True)
        code='var d=app.activeDocument;for(var i=0;i<d.layerSets.length;i++)d.layerSets[i].visible=false;var g=group(null,'+q(name)+');'
        code+='rect(g,"FUNDO",0,0,1920,1080,'+q('#BC718C' if p['theme']=='escuro' else '#FBA9C3')+',100);app.echoToOE("PAGE_CREATED");'
        print(js(code))
        if p.get('photo'):
            a=p['photo'];x,y,w,h=a['box'];print(import_asset(a['asset'],name,'FOTO - '+Path(a['asset']).stem,x,y,photo=[w,h]))
        # Fixed theme chrome comes from separate approved source layer.
        base=json.loads((P/'leitura/base_molde_extraida.json').read_text(encoding='utf-8-sig'))
        def allnodes(ns):
            for n in ns:
                yield n
                yield from allnodes(n.get('children',[]))
        nodes={n['id']:n for n in allnodes(base['tree'])}
        chrome=nodes[22 if p['theme']=='escuro' else 25]
        print(import_asset(chrome['pixel_cache']['path'],name,'MARCAS E CABECALHO APROVADOS',0,0))
        if p['theme']=='escuro':
            n=nodes[21];print(import_asset(n['pixel_cache']['path'],name,'B BELLAS - marca d\u2019água',n['bbox_px'][0],n['bbox_px'][1],n['opacity_percent']))
        code='var g=app.activeDocument.layerSets.getByName('+q(name)+');'
        for s in p.get('shapes',[]):
            code+='rect(g,'+','.join(q(s[k]) for k in ['name','x','y','w','h','color'])+','+q(s.get('opacity',100))+');'
        code+='var measured=[];'
        for s in p.get('texts',[]):code+='var spec='+q(s)+';var l=text(g,spec);measured.push({name:l.name,text:l.textItem.contents,bounds:bounds(l),font:l.textItem.font});'
        code+='app.echoToOE("METRICS:"+JSON.stringify(measured));'
        out=js(code);(P/f'auditoria/metricas_p{args.page:02d}.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf-8');print(out)
        for spec in p.get('texts',[]):
            if not spec.get('runs'):continue
            # Run Action Manager at top-level: Photopea evaluator crashes for this
            # operation nested within our reusable function.
            c='var l=app.activeDocument.layerSets.getByName('+q(name)+').artLayers.getByName('+q(spec['name'])+');app.activeDocument.activeLayer=l;var s=stringIDToTypeID,c=charIDToTypeID,ref=new ActionReference();ref.putEnumerated(c("Lyr "),c("Ordn"),c("Trgt"));var tx=executeActionGet(ref).getObjectValue(s("textKey"));var value=tx.getString(s("textKey"));var list=new ActionList();'
            segments=[];pos=0
            for r in spec['runs']:
                if r['start']>pos:segments.append((pos,r['start'],spec['font'],spec['color']))
                segments.append((r['start'],r['start']+r['length'],r['font'],r['color']));pos=r['start']+r['length']
            # Preserve terminal sentinel through the actual native descriptor.
            segments.append((pos,None,spec['font'],spec['color']))
            for start,end,font,color in segments:
                c+='var range=new ActionDescriptor();range.putInteger(c("From"),'+str(start)+');range.putInteger(c("T   "),'+('value.length' if end is None else str(end))+');var sty=tx.getList(s("textStyleRange")).getObjectValue(0).getObjectValue(s("textStyle"));'
                c+='sty.putString(s("fontPostScriptName"),'+q(font)+');sty.putString(s("fontName"),"Gotham");sty.putString(s("fontStyleName"),'+q(font.replace('Gotham-',''))+');var col=new ActionDescriptor();'
                for channel,i in [('Rd  ',0),('Grn ',2),('Bl  ',4)]:c+='col.putDouble(c('+q(channel)+'),'+str(int(color.lstrip('#')[i:i+2],16))+');'
                c+='sty.putObject(c("Clr "),c("RGBC"),col);range.putObject(s("textStyle"),s("textStyle"),sty);list.putObject(c("Txtt"),range);'
            c+='var out=new ActionDescriptor(),target=new ActionReference();target.putEnumerated(c("TxLr"),c("Ordn"),c("Trgt"));out.putReference(c("null"),target);var content=new ActionDescriptor();content.putString(c("Txt "),value);content.putList(c("Txtt"),list);out.putObject(c("T   "),c("TxLr"),content);executeAction(c("setd"),out,DialogModes.NO);app.echoToOE("STYLE_OK");'
            print(js(c))
        print(js('app.activeDocument.saveToOE("png");',[f'provas/pagina_{args.page:02d}.png']))
        print(js('app.activeDocument.saveToOE("psd");',['trabalho/crescimento_photopea_v2.psd']))
    if args.export:
        for p in manifest['pages']:
            name=f"{p['number']:02d} - {p['name']}"
            print(js('var d=app.activeDocument;for(var i=0;i<d.layerSets.length;i++)d.layerSets[i].visible=d.layerSets[i].name==='+q(name)+';d.saveToOE("png");',[f'provas/pagina_{p["number"]:02d}.png']))
if __name__=='__main__':main()
