from pathlib import Path
import json,datetime,hashlib,re
base=Path('treinamentos/crescimento_photopea_v2')
source=json.loads((base/'leitura/conteudo_v2.json').read_text(encoding='utf-8-sig'))
proposal=json.loads((base/'leitura/layouts_propostos_v2.json').read_text(encoding='utf-8-sig'))
blocks={b['id']:b for p in source['pages'] for b in p['blocks']}
pages=[]; mapping={}
WHITE='#FFFFFF'; PINK='#FBA9C3'; DARK='#B3718E'; MAUVE='#BC718C'
def page(n,name,theme,src):
    p={'number':n,'name':name,'theme':theme,'source':['fonte/'+x for x in src],'layout_reference':proposal['slides'][n-1]['references'],'texts':[],'shapes':[]}
    pages.append(p);return p
def txt(p,name,text,x,y,size,width,height,leading=None,font='Gotham-Book',color=WHITE,highlight=None,source_id=None):
    t={'name':name,'text':text,'x':x,'y':y,'size':size,'font':font,'color':color,'width':width,'height':height,'leading':leading if leading is not None else round(size*1.16,2)}
    if highlight:
        runs=[]
        for phrase in highlight:
            start=text.find(phrase)
            assert start>=0,(name,phrase)
            runs.append({'start':start,'length':len(phrase),'font':'Gotham-Bold','color':DARK if p['theme']=='claro' else PINK})
        t['runs']=runs
    p['texts'].append(t)
    if source_id:mapping.setdefault(source_id,[]).append({'page':p['number'],'text_layer':name})
    return t
def block(p,bid,text,x,y,size,width,height,**kw):
    assert re.sub(r'\\s+',' ',text).strip()==re.sub(r'\\s+',' ',blocks[bid]['text']).strip(),(bid,text,blocks[bid]['text'])
    return txt(p,bid,text,x,y,size,width,height,source_id=bid,**kw)
def shape(p,name,x,y,w,h,color,opacity=100):
    p['shapes'].append({'name':name,'x':x,'y':y,'w':w,'h':h,'color':color,'opacity':opacity})
def episode(p,bid,num_x,title_x,desc_x,y,name_w,desc_w,title_size=36,desc_size=34,ref_size=28,inline=True):
    b=blocks[bid]
    txt(p,bid+'-numero',b['number'],num_x,y,32,65,45,font='Gotham-Light',color=DARK if p['theme']=='claro' else PINK,source_id=bid)
    txt(p,bid+'-nome',b['title'],title_x,y,title_size,name_w,70,font='Gotham-Bold',source_id=bid)
    dy=y if inline else y+48
    txt(p,bid+'-acao',b['text'],desc_x,dy,desc_size,desc_w,45,source_id=bid)
    txt(p,bid+'-referencia',b['reference'],desc_x,dy+48 if inline else dy+43,ref_size,desc_w,40,source_id=bid)
p=page(1,'Capa','claro',['01.png'])
p['fixed_template_role']='cover_title_only'
block(p,'p01-titulo','Crescimento',936,430,120,900,160,font='Gotham-Light',leading=140)
p=page(2,'Preparação','escuro',['02.png'])
block(p,'p02-titulo','Todo mundo\\nquer crescer',140,290,72,620,190,leading=82,highlight=['quer crescer'])
block(p,'p02-premissa','Mas crescimento\\nexige preparação',145,505,40,590,115,leading=48)
for i,y in enumerate([255,395,535,675],1):
    bid=f'p02-{i:02}'; b=blocks[bid]
    txt(p,bid+'-numero',b['number'],920,y+10,36,70,55,font='Gotham-Light',color=PINK)
    shape(p,bid+'-filete',1015,y,3,100,PINK)
    lines={'01':'Estar alicerçado','02':'Estar preparado','03':'Estar disposto\\na aprender','04':'Estar disposto\\na ensinar'}[b['number']]
    block(p,bid,lines,1050,y+8,43,690,110,leading=51)
p=page(3,'Propósito e direção','claro',['03.png'])
p['photo']={'asset':'assets/foto_direcao_arcada.png','box':[1230,0,690,1080]}
block(p,'p03-titulo','Jesus sabia\\npara que veio',145,335,80,1000,200,leading=91,highlight=['para que veio'])
block(p,'p03-proposito','Ele tinha um propósito.',150,565,45,970,65,leading=54)
block(p,'p03-direcao','E nada mudou a Sua direção.',150,635,45,1000,70,leading=54,font='Gotham-Bold')
p=page(4,'Oposições 01 a04','claro',['04.png'])
block(p,'p04-titulo','Tentaram mudar Sua direção',140,200,76,1650,120,leading=88,highlight=['Sua direção'])
for i,y in enumerate([350,480,610,740],1):
    bid=f'p04-{i:02}';shape(p,bid+'-filete',155,y,4,96,DARK)
    episode(p,bid,180,270,760,y,420,1000,36,34,28,True)
p=page(5,'Oposições 05 a08','escuro',['04.png'])
block(p,'p04-titulo','Tentaram mudar\\nSua direção',140,350,69,590,200,leading=82,highlight=['Sua direção'])
for i,y in zip(range(5,9),[210,375,540,705]):
    bid=f'p04-{i:02}';shape(p,bid+'-filete',820,y,3,130,PINK)
    episode(p,bid,850,935,935,y,850,850,35,32,27,False)
p=page(6,'Oposições 09 a12 epermanência','claro',['04.png'])
p['photo']={'asset':'assets/foto_permanencia_rochas.png','box':[0,0,600,1080]}
block(p,'p04-titulo','Tentaram mudar\\nSua direção',710,180,62,1080,145,leading=73,highlight=['Sua direção'])
for i,y in zip(range(9,13),[350,480,610,740]):
    bid=f'p04-{i:02}';b=blocks[bid]
    shape(p,bid+'-faixa',555,y-8,1240,118,MAUVE)
    shape(p,bid+'-filete',555,y-8,5,118,WHITE)
    txt(p,bid+'-numero',b['number'],620,y+8,31,65,42,font='Gotham-Light',source_id=bid)
    txt(p,bid+'-nome',b['title'],710,y+5,32,1040,40,font='Gotham-Bold',source_id=bid)
    txt(p,bid+'-acao',b['text'],710,y+43,31,1040,40,source_id=bid)
    txt(p,bid+'-referencia',b['reference'],710,y+82,25,1040,32,source_id=bid)
block(p,'p04-fecho','E, ainda assim, Ele não perdeu o propósito!',710,905,33,1090,50,font='Gotham-Bold',leading=40)
p=page(7,'Até ofim','escuro',['05.png'])
block(p,'p05-titulo','Ele foi até o fim!',260,345,92,1400,135,leading=106,highlight=['até o fim!'])
block(p,'p05-citacao','“Está consumado.”',265,525,78,1390,115,font='Gotham-Light',leading=90)
txt(p,'p05-citacao-referencia',blocks['p05-citacao']['reference'],270,670,31,650,50,font='Gotham-Medium',source_id='p05-citacao')
p=page(8,'Pessoas quepreparam pessoas','claro',['06.png'])
shape(p,'eixo-transmissao',190,410,1520,3,DARK)
for i,x in enumerate([340,1000,1600],1):shape(p,f'marco-{i:02}',x,398,24,24,DARK)
block(p,'p06-titulo','Jesus preparou\\npessoas',150,475,66,500,170,leading=79,highlight=['pessoas'])
block(p,'p06-cadeia','E essas pessoas\\nprepararam outras',760,485,45,560,135,leading=55)
block(p,'p06-fecho','Até chegar\\na nós',1430,475,62,360,170,leading=75,font='Gotham-Bold')
p=page(9,'Crescer parapreparar','escuro',['07.png'])
p['photo']={'asset':'assets/foto_pessoas_encontro.png','box':[0,0,700,1080]}
block(p,'p07-titulo','Estamos crescendo',835,255,70,960,115,leading=81,highlight=['crescendo'])
block(p,'p07-consequencia','E, quanto mais crescemos,\\nmais pessoas precisamos preparar.',840,410,40,945,125,leading=49)
block(p,'p07-proposito','Porque o nosso maior propósito\\nsão pessoas.',840,585,48,950,145,leading=57,font='Gotham-Book')
block(p,'p07-fecho','O propósito não pode parar em nós.',840,775,36,945,70,leading=45,font='Gotham-Bold')
p=page(10,'Começar amultiplicar','claro',['08.png'])
p['photo']={'asset':'assets/foto_agua_poco.png','box':[1230,0,690,1080]}
block(p,'p08-titulo','Jesus preparou\\npessoas',145,260,76,1010,170,leading=88,highlight=['pessoas'])
block(p,'p08-tempo','Mas nem todas precisaram de anos\\nao lado dEle para começar a multiplicar.',150,460,40,980,145,leading=50)
shape(p,'filete-exemplo',150,635,900,3,DARK)
block(p,'p08-exemplo','A mulher samaritana encontrou Jesus\\n— e levou outros até Ele.',150,675,40,980,130,leading=50)
txt(p,'p08-exemplo-referencia',blocks['p08-exemplo']['reference'],150,830,28,500,45,font='Gotham-Medium',source_id='p08-exemplo')
p=page(11,'Venham ver','escuro',['09.png'])
block(p,'p09-titulo','Ela encontrou Jesus\\ne levou outros até Ele',250,215,66,1420,160,leading=79,highlight=['levou outros até Ele'])
block(p,'p09-convite','“Venham ver...”',250,405,90,1420,125,font='Gotham-Light',leading=104)
block(p,'p09-testemunho','Muitos samaritanos creram em Jesus\\npor causa do testemunho daquela mulher.',255,565,42,1410,125,leading=52)
txt(p,'p09-testemunho-referencia',blocks['p09-testemunho']['reference'],255,710,28,700,45,font='Gotham-Medium',source_id='p09-testemunho')
shape(p,'filete-fecho',250,780,1420,3,PINK)
block(p,'p09-fecho','Quem recebe não guarda para si.',250,825,46,1420,80,font='Gotham-Bold',leading=56)
p=page(12,'Agradecimento','claro',[])
p['fixed_template_role']='thank_you_unchanged'
p['layout_reference']=[{'approved_png':'exemplos/optima_final/pngs_aprovados/pagina_13.png','instruction':'Reconstruir composição fixa conforme PNG; elementos fixos são montados pelo principal.'}]
txt(p,'agradecimento-fixo','OBRIGADA!',635,494,116,720,150,font='Gotham-Light',leading=135)
for p in pages:p['name']=p['name'].replace('a04','a 04').replace('a08','a 08').replace('a12','a 12').replace('epermanência','e permanência').replace('ofim','o fim').replace('quepreparam','que preparam').replace('parapreparar','para preparar').replace('amultiplicar','a multiplicar')
assert set(mapping)==set(blocks),(set(blocks)-set(mapping))
assert len(blocks)==40
episodes=[b for b in blocks.values() if b['role']=='episodio']
assert len(episodes)==12
for b in episodes:
    pp=[x for p in pages for x in p['texts'] if x['name'].startswith(b['id']+'-')]
    for key in ['number','title','text','reference']:
        assert b[key] in [x['text'] for x in pp],(b['id'],key)
for p in pages:
    assert len([t for t in p['texts'] if t['name'].endswith('-titulo')]) <= 1
    for t in p['texts']:
        assert t['font'].startswith('Gotham-')
        assert all(r['start']+r['length']<=len(t['text']) for r in t.get('runs',[]))
        assert t['x']>=0 and t['y']>=0 and t['x']+t['width']<=1920 and t['y']+t['height']<=1080,(p['number'],t['name'])
manifest={'title':'Crescimento','width':1920,'height':1080,'stage':'production','editorial_source':'leitura/conteudo_v2.json','layout_source':'leitura/layouts_propostos_v2.json','coordinate_semantics':'x/y são o topo visível da camada. width/height são limites de layout; o montador ajusta bounds e valida Gotham no backend.','typography_status':'Famílias Gotham reais especificadas; prova e ajustes de tamanho/bounds a cargo do montador Photopea. Capa e agradecimento devem seguir medição do molde/PNG aprovado.','photo_fit':'cover proporcional, sem distorção; foco seguro y162..918 após recorte.','source_block_count':40,'source_episode_count':12,'source_block_mapping':mapping,'pages':pages}
out=base/'manifest_photopea.json';out.write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
report={'timestamp':datetime.datetime.now(datetime.timezone.utc).isoformat(),'manifest':'manifest_photopea.json','sha256':hashlib.sha256(out.read_bytes()).hexdigest(),'pages':len(pages),'source_blocks':len(blocks),'source_blocks_mapped':len(mapping),'episodes':len(episodes),'photos':[p['number'] for p in pages if 'photo'in p],'text_layers':sum(len(p['texts'])for p in pages),'shapes':sum(len(p['shapes'])for p in pages),'all_boxes_within_canvas':True,'h1_single_layer':True,'status':'Validação editorial e estrutural local passou; prova visual/bounds reais ainda pendente.'}
(base/'leitura/manifest_photopea_validacao.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(report,ensure_ascii=False))

