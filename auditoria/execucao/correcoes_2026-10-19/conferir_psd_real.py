"""Exercita o leitor em PSDs existentes, sem declarar homologação de suas artes."""
from pathlib import Path
import collections
import json
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[3]/"scripts"))
from psd_tools import PSDImage
from verificar_textos_psd import descendants,text_styles,compare_style
from contrato_bellas import FONTS

ROOT = Path(__file__).resolve().parents[3]
reports = []
for name in ["treinamentos/crescimento_photopea_v2/entrega/Crescimento_Photopea_V2.psd", "treinamentos/crescimento_luciane/entrega/crescimento_luciane_bellas.psd"]:
    psd = PSDImage.open(ROOT/name)
    fonts = collections.Counter()
    count = 0
    errors = []
    for layer,path,visible in descendants(psd):
        if layer.kind != "type":
            continue
        count += 1
        try:
            for start,end,font,color in text_styles(layer):
                if end>start:
                    fonts[font] += 1
                    if font not in FONTS or color is None:
                        errors.append(path+": fonte/cor não verificável")
        except Exception as exc:
            errors.append(path+": "+type(exc).__name__+": "+str(exc))
    reports.append({"psd":name,"text_layers":count,"fonts":dict(fonts),"reader_errors":errors})
out = Path(__file__).resolve().parent/"leitor_psd_real.json"
out.write_text(json.dumps(reports,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
print(json.dumps(reports,ensure_ascii=True,indent=2))
raise SystemExit(any(r["reader_errors"] for r in reports))
