import json,re,hashlib,datetime
from pathlib import Path
from psd_tools import PSDImage
root=Path("treinamentos/crescimento_photopea_v2")
psd_path=root/"entrega/Crescimento_Photopea_V2.psd"
manifest_path=root/"manifest_photopea.json"
source_path=root/"leitura/conteudo_v2.json"
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
m=json.loads(manifest_path.read_text(encoding="utf-8-sig"))
c=json.loads(source_path.read_text(encoding="utf-8-sig"))
psd=PSDImage.open(psd_path)
layers=[]
def walk(container,path="",page=None):
    for layer in container:
        current=path+"/"+layer.name if path else layer.name
        match=re.match(r"^(\d+) - ",layer.name) if not path else None
        current_page=int(match.group(1)) if match else page
        if layer.kind=="type":
            layers.append({"page":current_page,"path":current,"name":layer.name,"text":layer.text,"own_visible":layer.visible,"opacity":layer.opacity,"bounds":list(layer.bbox)})
        if layer.is_group(): walk(layer,current,current_page)
walk(psd)
def norm(s): return re.sub(r"\s+"," ",str(s).replace("\x00","")).strip()
by_key={}
for layer in layers: by_key.setdefault((layer["page"],layer["name"]),[]).append(layer)
issues=[]; checks=[]
def check(page,name,expected,origin,scope):
    actual=by_key.get((page,name),[])
    ok=len(actual)==1 and norm(actual[0]["text"])==norm(expected)
    item={"page":page,"name":name,"origin":origin,"scope":scope,"expected":expected,"actual":[a["text"] for a in actual],"match":ok}
    checks.append(item)
    if not ok: issues.append(item)
    if len(actual)==1 and (not actual[0]["own_visible"] or actual[0]["opacity"]==0): issues.append({"visibility_issue":item,"layer":actual[0]})
for src_page in c["pages"]:
    for b in src_page["blocks"]:
        maps=m["source_block_mapping"].get(b["id"],[])
        if not maps: issues.append({"missing_source_mapping":b["id"]})
        for mp in maps:
            name=mp["text_layer"]
            if b["role"]=="episodio":
                field={"numero":"number","nome":"title","acao":"text","referencia":"reference"}[name.rsplit("-",1)[1]]
            else: field="reference" if name==b["id"]+"-referencia" else "text"
            check(mp["page"],name,b[field],b["id"],"source_to_native")
        if b.get("number") and b["role"]!="episodio":
            check(maps[0]["page"],b["id"]+"-numero",b["number"],b["id"],"source_to_native")
source_checks=len(checks)
for page in m["pages"]:
    for t in page["texts"]:
        check(page["number"],t["name"],t["text"],"manifest","manifest_to_native")
summary={"timestamp":datetime.datetime.now().astimezone().isoformat(),"psd":str(psd_path.relative_to(root)),"psd_sha256":sha(psd_path),"manifest_sha256":sha(manifest_path),"source_sha256":sha(source_path),"native_text_layers":len(layers),"source_components_checked":source_checks,"manifest_components_checked":len(checks)-source_checks,"issues":issues,"per_page_native_count":{str(p):sum(x["page"]==p for x in layers) for p in range(1,13)},"checks":checks}
(root/"auditoria/editorial_final_text_layers.json").write_text(json.dumps(layers,ensure_ascii=False,indent=2),encoding="utf-8")
(root/"auditoria/editorial_final_comparacao.json").write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding="utf-8")
print(json.dumps({k:v for k,v in summary.items() if k!="checks"},ensure_ascii=False,indent=2))

