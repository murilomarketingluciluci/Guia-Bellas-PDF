from pathlib import Path
import json,collections,datetime,hashlib
src=Path('C:/Users/Murilo/.codex/sessions/2026/10/14/rollout-2026-10-14T17-49-01-01a13c2c-f2f1-7ff2-bc4c-0d1dd4a714d4.jsonl')
b=Path('treinamentos/crescimento_photopea_v2')
allowed={'spawn_agent','followup_task','send_message'}
calls=[];metas=[];parse_errors=[]
with src.open(encoding='utf-8')as f:
    for n,line in enumerate(f,1):
        try:o=json.loads(line)
        except Exception as e:parse_errors.append({'line':n,'error':str(e)});continue
        typ=o.get('type');p=o.get('payload',{})
        if not isinstance(p,dict):continue
        if typ in ['session_meta','turn_context']:
            meta={k:p[k]for k in ['model','reasoning_effort','effort','service_tier']if k in p and isinstance(p[k],(str,int,float,type(None)))}
            if meta:metas.append({'source_line':n,'timestamp':o.get('timestamp'),'record_type':typ,'metadata':meta})
            continue
        if typ in ['function_call','tool_call']:q=o
        elif typ=='response_item'and p.get('type')in ['function_call','tool_call']:q=p
        else:continue
        name=q.get('name','')
        if 'collaboration'not in name or name.split('.')[-1]not in allowed:continue
        args=q.get('arguments')
        if not isinstance(args,str):continue
        try:parsed=json.loads(args)
        except Exception:continue
        calls.append({'source_line':n,'timestamp':o.get('timestamp'),'tool_name':name,'call_id':q.get('call_id')or q.get('id'),'arguments_literal':args,'parsed':parsed})
hits=[c for c in calls if 'crescimento_photopea_v2'in c['arguments_literal']]
assert hits,'No reliable V2 cutoff found'
cutoff=min(c['source_line']for c in hits)
known={'catalogo_novo_v2','conteudo_novo_v2','api_validacao_v2'}
selected=[];ambiguous=[]
for c in calls:
    if c['source_line']<cutoff:continue
    a=c['parsed'];a_text=c['arguments_literal']
    explicit=('crescimento_photopea_v2'in a_text or 'V2'in a_text or any(k in a_text for k in known))
    if explicit:
        selected.append({k:v for k,v in c.items()if k!='parsed'})
    else:ambiguous.append({'source_line':c['source_line'],'timestamp':c['timestamp'],'tool_name':c['tool_name'],'call_id':c['call_id'],'reason':'Sem marcador V2 ou alvo reconhecido; arguments não extraídos.'})
out=b/'auditoria/prompts/delegacoes_recuperadas.jsonl'
assert not out.exists(),'Preserve previous recovery; choose append strategy'
with out.open('w',encoding='utf-8')as f:
    for c in selected:
        row={'recovery_status':'recuperacao_posterior_nao_pre_registro','recovered_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'source_file':str(src),'cutoff_rule':'Primeiro function_call de collaboration com arguments contendo crescimento_photopea_v2','cutoff_line':cutoff,**c}
        f.write(json.dumps(row,ensure_ascii=False)+'\\n')
summary={'source_file':str(src),'recovered_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'cutoff_line':cutoff,'selected_calls':len(selected),'tool_counts':dict(collections.Counter(x['tool_name']for x in selected)),'excluded_ambiguous_calls':ambiguous,'parse_errors':parse_errors,'metadata_after_cutoff':[m for m in metas if m['source_line']>=cutoff],'metadata_scope':'Somente campos escalares model/reasoning_effort/effort/service_tier de session_meta/turn_context; não foram extraídas mensagens ou conteúdo de análise.','recovery_sha256':hashlib.sha256(out.read_bytes()).hexdigest()}
(b/'auditoria/prompts/delegacoes_recuperadas_indice.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'cutoff_line':cutoff,'selected_calls':len(selected),'tool_counts':summary['tool_counts'],'ambiguous_count':len(ambiguous),'parse_errors':len(parse_errors),'metadata_after_cutoff':summary['metadata_after_cutoff']},ensure_ascii=False))

