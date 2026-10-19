#target photoshop
app.displayDialogs=DialogModes.NO;
var target='C:/Users/Murilo/Documents/Codex/2026-10-14/tes/outputs/optima_apn_bellas_final.psd';
var source='C:/Users/Murilo/Documents/Codex/2026-10-14/tes/outputs/optima_assets/foto_09_hidratacao_cena_continua.png';
var backup='C:/Users/Murilo/Documents/Codex/2026-10-14/tes/work/optima_antes_redesign_pagina_09.psd';
var proof='C:/Users/Murilo/Documents/Codex/2026-10-14/tes/outputs/optima_provas/pagina_09.jpg';
var d=null;
for(var i=0;i<app.documents.length;i++)if(app.documents[i].fullName.fsName.replace(/\\/g,'/').toLowerCase()==target.toLowerCase())d=app.documents[i];
if(!d)d=app.open(new File(target));app.activeDocument=d;
var g=null,oldContent=null,base=null,header=null;
for(var i=0;i<d.layerSets.length;i++)if(d.layerSets[i].name.indexOf('09')==0)g=d.layerSets[i];
if(!g)throw Error('Pagina 09 ausente');
for(var i=0;i<g.layerSets.length;i++)if(g.layerSets[i].name=='CONTENT')oldContent=g.layerSets[i];
for(var i=0;i<g.artLayers.length;i++){
 var l=g.artLayers[i];
 if(l.name.indexOf('FUNDO')==0)base=l;
 if(l.name.indexOf('Camada 1')==0)header=l;
 if(l.name.indexOf('FOTO 09 |')==0)throw Error('Foto 09 ja existe; revisar antes de editar');
}
if(!oldContent||!base||!header)throw Error('Estrutura base da pagina 09 mudou; nenhuma mudanca feita');
var psdOptions=new PhotoshopSaveOptions();psdOptions.layers=true;
d.saveAs(new File(backup),psdOptions,true,Extension.LOWERCASE);

// A arte anterior fica no PSD, oculta e integralmente editavel.
oldContent.name='CONTENT | versao anterior';oldContent.visible=false;
base.visible=true;header.visible=true;

// Fotografia unica, sem moldura ou faixa escura artificial, abaixo dos elementos fixos.
var x=0,y=0,w=670,h=1080;
var src=app.open(new File(source)),sw=src.width.as('px'),sh=src.height.as('px'),scale=Math.max(w/sw,h/sh);
src.resizeImage(UnitValue(Math.ceil(sw*scale),'px'),UnitValue(Math.ceil(sh*scale),'px'),null,ResampleMethod.BICUBIC);
var rw=src.width.as('px'),rh=src.height.as('px'),cx=Math.max(0,(rw-w)/2),cy=Math.max(0,(rh-h)/2);
src.crop([UnitValue(cx,'px'),UnitValue(cy,'px'),UnitValue(cx+w,'px'),UnitValue(cy+h,'px')]);
src.selection.selectAll();src.selection.copy();
app.activeDocument=d;d.activeLayer=base;
var photo=d.paste();photo.name='FOTO 09 | hidratacao natural cena continua';
photo.move(base,ElementPlacement.PLACEBEFORE);
photo.translate(UnitValue(x-photo.bounds[0].as('px'),'px'),UnitValue(y-photo.bounds[1].as('px'),'px'));
photo.visible=true;
app.activeDocument=src;src.close(SaveOptions.DONOTSAVECHANGES);app.activeDocument=d;

var content=g.layerSets.add();content.name='CONTENT';
function ink(hex){var c=new SolidColor();c.rgb.hexValue=hex;return c;}
function rect(name,x,y,w,h,hex){
 var l=content.artLayers.add();l.name=name;d.activeLayer=l;
 d.selection.select([[x,y],[x+w,y],[x+w,y+h],[x,y+h]]);
 d.selection.fill(ink(hex));d.selection.deselect();return l;
}
function point(value,x,y,size,hex,font,track,lead){
 var l=content.artLayers.add();l.kind=LayerKind.TEXT;l.name=value.replace(/\r/g,' ').substr(0,52);
 var t=l.textItem;t.kind=TextType.POINTTEXT;t.contents=value;t.font=font;t.size=UnitValue(size,'pt');
 t.color=ink(hex);t.tracking=track;t.justification=Justification.LEFT;
 if(lead)t.leading=UnitValue(lead,'pt');
 t.position=[UnitValue(x,'px'),UnitValue(y,'px')];return l;
}
function para(value,x,y,w,h,size,hex,font,track,lead){
 var l=content.artLayers.add();l.kind=LayerKind.TEXT;l.name=value.replace(/\r/g,' ').substr(0,52);
 var t=l.textItem;t.kind=TextType.PARAGRAPHTEXT;t.contents=value;t.font=font;t.size=UnitValue(size,'pt');
 t.color=ink(hex);t.tracking=track;t.justification=Justification.LEFT;t.leading=UnitValue(lead,'pt');
 t.position=[UnitValue(x,'px'),UnitValue(y,'px')];t.width=UnitValue(w,'px');t.height=UnitValue(h,'px');return l;
}
function sd(s){return stringIDToTypeID(s)}function cd(s){return charIDToTypeID(s)}
function textDesc(id){var r=new ActionReference();r.putIdentifier(cd('Lyr '),id);return executeActionGet(r).getObjectValue(sd('textKey'))}
function mergeTitle(a,b){
 var first=a.textItem.contents,second=b.textItem.contents,merged=first+'\r'+second,cut=first.length+1,A=textDesc(a.id),B=textDesc(b.id);
 var s1=A.getList(sd('textStyleRange')).getObjectValue(0).getObjectValue(sd('textStyle'));
 var s2=B.getList(sd('textStyleRange')).getObjectValue(0).getObjectValue(sd('textStyle'));
 var list=new ActionList(),r1=new ActionDescriptor(),r2=new ActionDescriptor();
 r1.putInteger(sd('from'),0);r1.putInteger(sd('to'),cut);r1.putObject(sd('textStyle'),sd('textStyle'),s1);list.putObject(sd('textStyleRange'),r1);
 r2.putInteger(sd('from'),cut);r2.putInteger(sd('to'),merged.length);r2.putObject(sd('textStyle'),sd('textStyle'),s2);list.putObject(sd('textStyleRange'),r2);
 A.putString(sd('textKey'),merged);A.putList(sd('textStyleRange'),list);
 var pr=A.getList(sd('paragraphStyleRange')).getObjectValue(0);pr.putInteger(sd('from'),0);pr.putInteger(sd('to'),merged.length);
 var pl=new ActionList();pl.putObject(sd('paragraphStyleRange'),pr);A.putList(sd('paragraphStyleRange'),pl);
 var set=new ActionDescriptor(),ref=new ActionReference();ref.putIdentifier(cd('Lyr '),a.id);set.putReference(cd('null'),ref);set.putObject(cd('T   '),cd('TxLr'),A);
 executeAction(cd('setd'),set,DialogModes.NO);a.name='H1 | Pele hidratada melhora o efeito';b.remove();
}

var title1=point('Pele hidratada',754,196,74,'FFFFFF','Gotham-Book',-70,79);
var title2=point('melhora o efeito',754,275,74,'B3718E','Gotham-Bold',-70,79);
mergeTitle(title1,title2);
rect('Subtitulo | faixa branca',752,296,1030,49,'FFFFFF');
point('DO DESODORANTE SEM ALUM\u00cdNIO',778,331,26,'B3718E','Gotham-Medium',145);

function block(n,head,body,barY,bodyY,bodyH){
 rect('Beneficio '+n+' | faixa malva',752,barY,1030,50,'B3718E');
 point(('0'+n),776,barY+35,25,'FFFFFF','Gotham-Medium',30);
 rect('Beneficio '+n+' | divisor',831,barY+11,2,28,'FFFFFF');
 point(head,856,barY+36,29,'FFFFFF','Gotham-Bold',-45);
 para(body,756,bodyY,1020,bodyH,29,'FFFFFF','Gotham-Book',-60,37);
}
block(1,'MENOS ATRITO E IRRITA\u00c7\u00c3O',
 'Sem o alum\u00ednio, a axila continua suando, o que \u00e9 natural. Se a pele est\u00e1 ressecada, ela se irrita mais facilmente e fica mais sens\u00edvel ao atrito com a roupa. Irrita\u00e7\u00e3o e suor s\u00e3o a combina\u00e7\u00e3o perfeita para o mau odor.',
 384,445,153);
block(2,'pH MAIS EQUILIBRADO',
 'A pele ressecada tende a desregular o pH, e com isso o mau odor aumenta. Com a hidrata\u00e7\u00e3o, o pH da pele fica mais est\u00e1vel, deixando o ambiente menos favor\u00e1vel \u00e0s bact\u00e9rias que causam mau odor.',
 610,671,137);
block(3,'MELHORA A A\u00c7\u00c3O DOS ATIVOS NATURAIS',
 'A pele hidratada permite que os ativos do desodorante sem alum\u00ednio funcionem melhor.',
 817,878,86);

for(var i=0;i<d.layers.length;i++)d.layers[i].visible=(d.layers[i]==g||d.layers[i].name=='Plano de Fundo');
var f=new File(proof),o=new JPEGSaveOptions();o.quality=12;d.saveAs(f,o,true,Extension.LOWERCASE);
d.save();
'OK pagina 09 redesenhada, '+content.layers.length+' camadas, foto inteira';
