"""Roteiro de produção Bellas; conteúdo identificado por fonte e bloco."""
import json
from pathlib import Path

P = Path(__file__).resolve().parents[1]
source = json.loads((P/'leitura/conteudo_transcrito.json').read_text(encoding='utf-8'))
pages = source['paginas_fonte']
slides=[]

def src(page, block): return {'file':f'fonte/{page:02}.png','page':page,'block':block}
def element(role, text, box, size, *, font='Gotham-Book', lead=None, color='FFFFFF', bold=None, source_page=None, block='', **extra):
    e={'role':role,'text':text,'rect':[round(box[0]/1920,7),round(box[1]/1080,7),round(box[2]/1920,7),round(box[3]/1080,7)],'box_px':box,'size_pt':size,'font':font,'leading_pt':lead or round(size*1.13,2),'tracking':-70 if role in ('h1','callout') else -60,'color':color}
    if bold:e['emphasis']=bold
    if source_page:e['source']=src(source_page,block)
    e.update(extra);return e
def add(n,name,theme,source_page,photo=None,reason=''):
    s={'number':n,'name':name,'theme':theme,'elements':[],'source_file':f'fonte/{source_page:02}.png' if source_page else '../../exemplos/optima_final/optima_apn_bellas_final.psd','composition_reason':reason}
    if photo:
        asset,x,w=photo
        s['elements'].append({'role':'photo','rect':[x/1920,0,w/1920,1],'box_px':[x,0,w,1080],'asset':f'assets/{asset}','fit':'cover','asset_status':'final','safe_top_bottom':0.15})
    slides.append(s);return s['elements']

# Capa: grupo aprovado. O executor troca somente o título, preserva sua transformação.
e=add(1,'Capa','claro',1,reason='Composição aprovada da capa; somente o título muda.')
e.append(element('h1','Crescimento',[929,420,940,310],112,source_page=1,block='titulo'))

e=add(2,'Crescer exige preparação','claro',2,('foto_02_preparacao.png',0,700),'Quatro atitudes curtas em faixas; imagem de estudo dá contexto sem competir com a lista.')
e.append(element('h1','Todo mundo\nquer crescer',[800,158,990,205],95,lead=101,bold={'text':'quer crescer','font':'Gotham-Bold','color':'B3718E'},source_page=2,block='titulo'))
e.append(element('body',pages[1]['subtitulo_final'],[805,387,990,60],39,source_page=2,block='subtitulo'))
for i,b in enumerate(pages[1]['blocos']):
    e.append(element('card',b['texto_final'],[800,501+i*103,980,80],37,font='Gotham-Medium',source_page=2,block=str(i+1),card_id=f'atitude_{i+1}',number=b['numero'],padding=[112,25],background='BC718C'))

e=add(3,'Propósito e direção','escuro',3,('foto_03_caminho.png',1220,700),'Fotografia de caminho acompanha a afirmação de direção; frase principal com amplo respiro.')
e.append(element('h1','Jesus sabia\npara que veio',[135,205,1010,232],101,lead=112,bold={'text':'para que veio','font':'Gotham-Bold','color':'FBA9C3'},source_page=3,block='titulo'))
e.append(element('body',pages[2]['blocos'][0]['texto_final'],[145,516,975,88],48,source_page=3,block='1'))
e.append(element('callout','E nada mudou\na Sua direção.',[145,660,975,158],52,lead=62,font='Gotham-Bold',source_page=3,block='2'))

for j in range(3):
    n=4+j;theme='claro' if j!=1 else 'escuro';accent='B3718E' if theme=='claro' else 'FBA9C3'
    e=add(n,f'Direção - episódios {j*4+1:02} a {j*4+4:02}',theme,4,reason='Quatro episódios por página com descrição e referência completas; grid 2 por 2 para preservar corpo e entrelinha.')
    e.append(element('h1','Tentaram mudar\nSua direção',[140,145,1635,205],91,lead=99,bold={'text':'Sua direção','font':'Gotham-Bold','color':accent},source_page=4,block='titulo'))
    for k,b in enumerate(pages[3]['blocos'][j*4:j*4+4]):
        x=140+(k%2)*835;y=421+(k//2)*243
        # Cada cartão completo é uma pasta; título/descrição/referência permanecem objetos separados editáveis.
        e.append(element('card',b['sujeito'],[x,y,800,211],37,font='Gotham-Bold',source_page=4,block=b['numero']+'.sujeito',card_id='episodio_'+b['numero'],number=b['numero'],background='BC718C' if theme=='claro' else '9E5874',padding=[108,24],card_title=True))
        e.append(element('body',b['texto_final'],[x+108,y+83,650,72],33,lead=39,source_page=4,block=b['numero']+'.descricao',card_id='episodio_'+b['numero']))
        e.append(element('body',b['referencia'],[x+108,y+162,650,35],27,font='Gotham-Medium',source_page=4,block=b['numero']+'.referencia',card_id='episodio_'+b['numero']))
    if j==2:e.append(element('callout',pages[3]['fecho_final'],[145,915,1630,52],37,font='Gotham-Bold',source_page=4,block='fecho'))

e=add(7,'Até o fim','escuro',5,reason='Pausa tipográfica depois dos doze episódios. Citação e referência preservadas.')
e.append(element('h1','Ele foi até o fim!',[210,243,1500,166],126,bold={'text':'até o fim!','font':'Gotham-Bold','color':'FBA9C3'},source_page=5,block='titulo',align='center'))
e.append(element('quote','“Está consumado.”',[225,519,1470,122],79,font='Gotham-Light',source_page=5,block='citacao',align='center'))
e.append(element('body','João 19:30',[650,710,620,65],34,font='Gotham-Medium',source_page=5,block='referencia',align='center'))

e=add(8,'Preparar outras pessoas','claro',6,('foto_08_mentoria.png',0,710),'Mentoria contemporânea à esquerda; progressão textual à direita sem acrescentar etapas inexistentes na fonte.')
e.append(element('h1','Jesus preparou\npessoas',[815,183,970,218],97,lead=104,bold={'text':'pessoas','font':'Gotham-Bold','color':'B3718E'},source_page=6,block='titulo'))
e.append(element('body','E essas pessoas\nprepararam outras',[820,504,950,142],48,lead=61,source_page=6,block='1'))
e.append(element('callout','Até chegar em nós',[815,769,960,105],54,font='Gotham-Bold',source_page=6,block='2',background='BC718C',padding=[32,20]))

e=add(9,'Crescimento tem pessoas como propósito','escuro',7,('foto_09_equipe.png',1220,700),'Equipe à direita e três níveis de mensagem à esquerda; palavra pessoas se destaca sem substituir o argumento.')
e.append(element('h1','Estamos\ncrescendo',[140,164,1000,208],97,lead=105,bold={'text':'crescendo','font':'Gotham-Bold','color':'FBA9C3'},source_page=7,block='titulo'))
e.append(element('body','E quanto mais crescemos,\nmais pessoas precisamos preparar.',[145,438,1000,134],41,lead=53,source_page=7,block='1'))
e.append(element('callout','Porque o nosso maior\npropósito são pessoas.',[145,628,1000,142],51,lead=61,font='Gotham-Bold',source_page=7,block='2'))
e.append(element('body','O propósito não pode parar em nós.',[145,861,1000,76],38,source_page=7,block='3'))

e=add(10,'Começar a multiplicar','claro',8,reason='Duas partes da fonte 08, com a mensagem sobre tempo e a mulher samaritana separadas por um filete; preservar João 4.')
e.append(element('h1','Jesus preparou\npessoas',[140,167,960,210],97,lead=105,bold={'text':'pessoas','font':'Gotham-Bold','color':'B3718E'},source_page=8,block='titulo'))
e.append(element('body','Mas nem todas precisaram de anos\nao lado dEle para começar a multiplicar.',[145,481,1000,195],48,lead=60,source_page=8,block='1'))
e.append(element('callout','A mulher samaritana\nencontrou Jesus e levou\noutros até Ele.',[1210,475,570,265],43,lead=57,font='Gotham-Medium',source_page=8,block='2'))
e.append(element('body','João 4',[1210,670,570,55],32,font='Gotham-Medium',source_page=8,block='referencia'))

e=add(11,'Quem recebe compartilha','escuro',9,reason='Última tela de conteúdo em composição tipográfica; chamada e testemunho completos, sem foto desnecessária.')
e.append(element('h1','Ela encontrou Jesus\ne levou outros até Ele',[140,152,1620,220],87,lead=97,bold={'text':'levou outros até Ele','font':'Gotham-Bold','color':'FBA9C3'},source_page=9,block='titulo'))
e.append(element('quote','“Venham ver...”',[145,448,1620,125],86,font='Gotham-Light',source_page=9,block='citacao'))
e.append(element('body','Muitos samaritanos creram em Jesus por causa\ndo testemunho daquela mulher.',[150,638,1580,114],42,lead=53,source_page=9,block='1'))
e.append(element('body','João 4:29, 39',[150,791,1200,55],30,font='Gotham-Medium',source_page=9,block='referencia'))
e.append(element('callout','Quem recebe não guarda para si.',[145,904,1620,62],52,font='Gotham-Bold',source_page=9,block='2'))

e=add(12,'Agradecimento','claro',None,reason='Grupo aprovado preservado sem alterações; igualdade de pixels verificada ao final.')
e.append(element('h1','obrigada!',[630,490,660,110],85.63322,font='Gotham-Light',source={'file':'../../exemplos/optima_final/optima_apn_bellas_final.psd','group':'13 - Agradecimento'}))
# Valores armazenados no PSD medidos na referência, não alvos RGB de outra rota de exportação.
for slide in slides:
    for el in slide['elements']:
        if el.get('background')=='BC718C':
            el['background']='A9708A';el['background_export_target']='BC718C'
        elif el.get('background')=='9E5874':
            el['background']='86566F';el['background_export_target']='965570'
        if el.get('emphasis',{}).get('color')=='FBA9C3':
            el['emphasis']['color']='E7A7C1';el['emphasis']['export_target']='FBA9C3'
manifest={'schema_version':'1.0','stage':'final','project':'Crescimento | APN Luciane | Bellas','canvas':[1920,1080],'template':{'psd':'../../referencias/molde_bellas_aprovado_capa_temas_agradecimento.psd','approved_psd':'../../exemplos/optima_final/optima_apn_bellas_final.psd','groups':{'cover':'CAPA APROVADA - ALTERAR SOMENTE TITULO','thanks':'AGRADECIMENTO APROVADO - ULTIMA PAGINA','light':'TEMA CLARO VAZIO - DUPLICAR','dark':'TEMA ESCURO VAZIO - DUPLICAR'}},'workflow_override':{'map_approval':'Dispensada explicitamente pelo usuário nesta sessão; executar até o final com revisão independente.'},'slides':slides}
(P/'manifesto_final.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(f'Manifesto: {len(slides)} páginas, {sum(len(s["elements"]) for s in slides)} elementos')
