from pathlib import Path
import fitz, json
from PIL import Image, ImageDraw
root=Path.cwd()
out=root/'treinamentos/crescimento_photopea_v2/leitura/catalogo_integral'
out.mkdir(parents=True,exist_ok=True)
candidates={'financas':[7,15,16],'namorados':[10],'colageno':[23,24],'oito_passos':[4,10,16,29,31],'mulheres':[5,8],'posicionamento':[2,7,11],'etiqueta':[3,4],'base':[10,16]}
records=[]
for alias,pages in candidates.items():
    doc=fitz.open(root/'referencias/pdfs_15'/f'{alias}.pdf')
    for n in pages:
        page=doc[n-1]; pix=page.get_pixmap(matrix=fitz.Matrix(1920/page.rect.width,1920/page.rect.width),alpha=False)
        path=out/f'{alias}_{n:02}.png';pix.save(path)
        records.append({'alias':alias,'page':n,'pdf':f'referencias/pdfs_15/{alias}.pdf','render':str(path.relative_to(root)).replace('\\','/'),'size':[pix.width,pix.height]})
doc=fitz.open(root/'referencias/rosangela_original.pdf')
page=doc[13]; pix=page.get_pixmap(matrix=fitz.Matrix(1920/page.rect.width,1920/page.rect.width),alpha=False); pix.save(out/'rosangela_14.png')
records.append({'alias':'rosangela','page':14,'pdf':'referencias/rosangela_original.pdf','render':str((out/'rosangela_14.png').relative_to(root)).replace('\\','/'),'size':[pix.width,pix.height]})
doc=fitz.open(root/'referencias/catalogo_historico_26_layouts.pdf')
thumbs=[]
for i,page in enumerate(doc):
    pix=page.get_pixmap(matrix=fitz.Matrix(.5,.5),alpha=False)
    im=Image.frombytes('RGB',[pix.width,pix.height],pix.samples); im.thumbnail((460,340))
    thumbs.append(im)
contact=Image.new('RGB',(460*4,370*((len(thumbs)+3)//4)),'white')
draw=ImageDraw.Draw(contact)
for i,im in enumerate(thumbs):
    x=i%4*460;y=i//4*370;contact.paste(im,(x,y));draw.text((x+8,y+342),f'Pagina catalogo historico {i+1}',fill='black')
contact.save(out/'catalogo_26_contato.png')
(out/'renders_index.json').write_text(json.dumps(records,ensure_ascii=False,indent=2),encoding='utf8')
print(json.dumps({'renders':len(records),'catalog_pdf_pages':len(doc),'out':str(out)},ensure_ascii=False))

