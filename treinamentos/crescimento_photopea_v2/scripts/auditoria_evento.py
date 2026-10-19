"""Diário incremental: argumentos literais recebidos em JSON/base64 ou stdin."""
from pathlib import Path
import argparse, base64, json, datetime

parser=argparse.ArgumentParser()
parser.add_argument('--project',required=True)
parser.add_argument('--agent',default='principal')
parser.add_argument('--base64')
args=parser.parse_args()
record=json.loads(base64.b64decode(args.base64).decode('utf-8')) if args.base64 else json.load(__import__('sys').stdin)
record.setdefault('timestamp',datetime.datetime.now(datetime.timezone.utc).isoformat())
record.setdefault('agent',args.agent)
folder=Path(args.project)/'auditoria/execucao';folder.mkdir(parents=True,exist_ok=True)
with (folder/(args.agent+'.jsonl')).open('a',encoding='utf-8') as output:
    output.write(json.dumps(record,ensure_ascii=False)+'\n')
