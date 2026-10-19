import json,hashlib,datetime
from pathlib import Path
import fitz
from PIL import Image
root=Path("treinamentos/crescimento_photopea_v2")
pdf_path=root/"entrega/Crescimento_Photopea_V2.pdf"
doc=fitz.open(pdf_path)
pages=[]
for i,page in enumerate(doc):
    images=page.get_images(full=True)
    png_path=root/f"entrega/pngs/pagina_{i+1:02}.png"
    expected=Image.open(png_path).convert("RGB")
    exact=False
    if len(images)==1:
        pm=fitz.Pixmap(doc,images[0][0])
        if pm.n!=3: pm=fitz.Pixmap(fitz.csRGB,pm)
        actual=Image.frombytes("RGB",(pm.width,pm.height),pm.samples)
        exact=actual.size==expected.size and actual.tobytes()==expected.tobytes()
    pages.append({"page":i+1,"image_count":len(images),"pdf_image_matches_reviewed_png_rgb":exact,"png_sha256":hashlib.sha256(png_path.read_bytes()).hexdigest()})
result={"timestamp":datetime.datetime.now().astimezone().isoformat(),"pdf_sha256":hashlib.sha256(pdf_path.read_bytes()).hexdigest(),"pdf_pages":len(doc),"all_reviewed_pngs_embedded_exactly":len(doc)==12 and all(p["pdf_image_matches_reviewed_png_rgb"] for p in pages),"pages":pages,"scope":"Vínculo editorial do PDF às provas PNG lidas; não aprova cor/perfil/template do PSD."}
(root/"auditoria/editorial_pdf_provas_final.json").write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding="utf-8")
print(json.dumps(result,ensure_ascii=False,indent=2))

