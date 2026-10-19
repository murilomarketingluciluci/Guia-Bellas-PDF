"""Cliente da ponte local. A ponte registra script literal e resultado antes/depois."""
import argparse,json,urllib.request,urllib.error
p=argparse.ArgumentParser();p.add_argument('--load');p.add_argument('--script');p.add_argument('--file');p.add_argument('--outputs',nargs='*',default=[]);p.add_argument('--result');a=p.parse_args()
job={'load':a.load} if a.load else ({'script_file':a.file,'outputs':a.outputs} if a.file else {'script':a.script,'outputs':a.outputs})
req=urllib.request.Request('http://127.0.0.1:8876/run',data=json.dumps(job).encode(),headers={'Content-Type':'application/json'})
try:
 with urllib.request.urlopen(req,timeout=240) as r:data=json.load(r)
except urllib.error.HTTPError as e:
 print(e.read().decode('utf-8'));raise SystemExit(1)
if a.result:
 from pathlib import Path
 Path(a.result).write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(data,ensure_ascii=False))
