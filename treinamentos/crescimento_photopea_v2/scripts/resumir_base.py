import json
from pathlib import Path
p=Path(__file__).resolve().parents[1]
data=json.loads((p/'leitura/base_molde_extraida.json').read_text(encoding='utf-8-sig'))
def walk(ns):
    for n in ns:
        print(n['id'],n['path'],n['bbox_px'],round(n['opacity_percent'],2),n['kind'],n.get('text',{}).get('contents',''))
        walk(n.get('children',[]))
walk(data['tree'])
