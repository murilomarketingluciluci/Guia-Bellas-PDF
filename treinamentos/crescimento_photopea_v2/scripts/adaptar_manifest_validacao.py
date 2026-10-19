"""Explicit read-only schema adapter for the package's older manifest gate."""
import json,hashlib
from pathlib import Path
from psd_tools import PSDImage
p=Path(__file__).resolve().parents[1]
m=json.loads((p/'manifest_photopea.json').read_text(encoding='utf-8-sig'))
psd=PSDImage.open(p/'entrega/Crescimento_Photopea_V2.psd')
def walk(g):
    for l in g:
        yield l
        if l.is_group():yield from walk(l)
slides=[]
for page in m['pages']:
    g=next(g for g in psd if g.is_group() and g.name.startswith(f'{page["number"]:02d} - '))
    title=page['texts'][0]['name'];els=[]
    for l in walk(g):
        if l.kind!='type':continue
        x,y,r,b=l.bbox
        els.append({'name':l.name,'role':'h1' if l.name==title else 'body','text':l.text,'rect':[x/1920,y/1080,(r-x)/1920,(b-y)/1080]})
    if page.get('photo'):
        x,y,w,h=page['photo']['box'];els.append({'role':'photo','asset':page['photo']['asset'],'fit':'cover','rect':[x/1920,y/1080,w/1920,h/1080]})
    slides.append({'number':page['number'],'theme':page['theme'],'elements':els})
d={'purpose':'Schema-only validation adapter, not the Photopea authoring input. Bounds/text come from actual final PSD; variable photos come from final manifest. Fixed brand imagery remains part of template and is not a new cover photo.','source_authoring_manifest':'manifest_photopea.json','source_psd':'entrega/Crescimento_Photopea_V2.psd','source_psd_sha256':hashlib.sha256((p/'entrega/Crescimento_Photopea_V2.psd').read_bytes()).hexdigest(),'stage':'final','canvas':[1920,1080],'template':m['template'],'slides':slides}
(p/'manifesto_validacao_bellas.json').write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
