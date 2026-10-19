from pathlib import Path
from PIL import Image
import hashlib,json,datetime
import numpy as np
root=Path(__file__).resolve().parents[1]
package=root.parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def record(p):
 return {"path":p.relative_to(root).as_posix(),"sha256":sha(p),"bytes":p.stat().st_size}
paths=[root/"entrega"/"pngs"/f"pagina_{n:02}.png" for n in range(1,13)]
items=[]
for p in paths:
 r=record(p);r["dimensions"]=list(Image.open(p).size);items.append(r)
aux=["entrega/Crescimento_Photopea_V2.psd","entrega/Crescimento_Photopea_V2.pdf","manifest_photopea.json","leitura/direcao_catalogo_v2.md","leitura/layouts_propostos_v2.json","leitura/conteudo_v2.json","auditoria/reabertura_psd.json","auditoria/pixels_reabertura.json"]
out={"cutoff_utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),"reviewer":"catalogo_novo_v2","artifacts":[record(root/p) for p in aux],"pngs":items}
im=Image.open(paths[5]).convert("RGB")
def lum(rgb):
 a=[v/255 for v in rgb];b=[v/12.92 if v<=.04045 else ((v+.055)/1.055)**2.4 for v in a]
 return .2126*b[0]+.7152*b[1]+.0722*b[2]
out["photo06_header_background_samples"]=[{"x":x,"y":y,"rgb":list(im.getpixel((x,y))),"contrast_white":round(1.05/(lum(im.getpixel((x,y)))+.05),3)} for y in [50,80] for x in [100,250,400,550]]
im8=np.asarray(Image.open(paths[7]).convert("RGB"))
rows={}
for y in [398,409,410,412,413,421]:
 mask=np.max(np.abs(im8[y,:,:].astype(int)-np.array([179,113,142])),axis=1)<=1
 xs=np.where(mask[150:1750])[0]+150
 groups=[]
 for x in xs.tolist():
  if groups and x==groups[-1][1]+1:groups[-1][1]=x
  else:groups.append([x,x])
 rows[str(y)]=groups
out["page08_shape_runs_x_by_y"]=rows
im11=np.asarray(Image.open(paths[10]).convert("RGB"))
region=im11[718:790,240:1700,:]
mask=(region[:,:,0]>240)&(region[:,:,1]>240)&(region[:,:,2]>240)
ys=np.where(mask.any(axis=1))[0]+718
out["page11_closer_white_text_y_after_rule"]=[int(ys.min()),int(ys.max())]
out["page11_rule_manifest_y"]=715
out["page11_clear_rows_after_rule_estimate"]=int(ys.min()-718)
out["page09_manual_subject_bounds_y"]={"top":327,"bottom":820,"uncertainty_px":6,"top_percent":round(327/1080*100,2),"bottom_percent":round((1080-820)/1080*100,2),"required_blank_px":162,"method":"Leitura manual da imagem integral; valor herdado da inspeção anterior e reconfirmado visualmente no PNG final, não detecção automática."}
ref=package/"exemplos/optima_final/pngs_aprovados/pagina_13.png"
if ref.exists():
 a=np.asarray(Image.open(paths[11]).convert("RGB")).astype(int);b=np.asarray(Image.open(ref).convert("RGB")).astype(int)
 d=np.abs(a-b)
 out["thanks_reference_comparison"]={"reference_path":"exemplos/optima_final/pngs_aprovados/pagina_13.png","reference_sha256":sha(ref),"same_dimensions":a.shape==b.shape,"identical_pixel_fraction":float(np.mean(np.all(d==0,axis=2))),"mean_abs_channel_difference":float(d.mean()),"max_channel_difference":int(d.max()),"note":"Comparação quantitativa de reconstrução; não interpretar como identidade literal quando houver diferenças de rasterização."}
out["reopen_comparison_report"]=json.loads((root/"auditoria/pixels_reabertura.json").read_text(encoding="utf-8-sig"))
dest=root/"leitura/QA_VISUAL_V2_FINAL_metricas.json";dest.write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding="utf-8")
print(json.dumps(out,ensure_ascii=False,indent=2))
