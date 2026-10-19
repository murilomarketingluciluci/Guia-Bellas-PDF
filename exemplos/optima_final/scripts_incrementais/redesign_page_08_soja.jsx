#target photoshop
app.displayDialogs=DialogModes.NO;
var target='C:/Users/Murilo/Documents/Codex/2026-10-14/tes/outputs/optima_apn_bellas_final.psd';
var source='C:/Users/Murilo/Documents/Codex/2026-10-14/tes/outputs/optima_assets/foto_08_soja_editorial.png';
var backup='C:/Users/Murilo/Documents/Codex/2026-10-14/tes/work/optima_antes_redesign_pagina_08.psd';
var proof='C:/Users/Murilo/Documents/Codex/2026-10-14/tes/outputs/optima_provas/pagina_08.jpg';
var d=null;
for(var i=0;i<app.documents.length;i++)if(app.documents[i].fullName.fsName.replace(/\\/g,'/').toLowerCase()==target.toLowerCase())d=app.documents[i];
if(!d)d=app.open(new File(target));app.activeDocument=d;
var g=null;for(var i=0;i<d.layerSets.length;i++)if(d.layerSets[i].name.indexOf('08')==0)g=d.layerSets[i];
if(!g)throw Error('Pagina 08 ausente');
var old=g.layerSets.getByName('CONTENT'),title=old.artLayers.getByName('Óleo de soja');
var bg=g.artLayers.getByName('BG copiar 3');
if(!old||!title||!bg||title.kind!=LayerKind.TEXT)throw Error('Estrutura pagina 08 mudou');
var opts=new PhotoshopSaveOptions();opts.layers=true;d.saveAs(new File(backup),opts,true,Extension.LOWERCASE);
for(var i=0;i<old.artLayers.length;i++)if(old.artLayers[i]!=title)old.artLayers[i].visible=false;
old.name='TITULO E CONTEUDO ANTERIOR | oculto';old.visible=true;
var src=app.open(new File(source)),x=1240,y=0,w=680,h=1080;
var sw=src.width.as('px'),sh=src.height.as('px'),scale=Math.max(w/sw,h/sh);
src.resizeImage(UnitValue(Math.ceil(sw*scale),'px'),UnitValue(Math.ceil(sh*scale),'px'),null,ResampleMethod.BICUBIC);
var rw=src.width.as('px'),rh=src.height.as('px'),cx=Math.max(0,(rw-w)/2),cy=Math.max(0,(rh-h)/2);
src.crop([UnitValue(cx,'px'),UnitValue(cy,'px'),UnitValue(cx+w,'px'),UnitValue(cy+h,'px')]);
src.selection.selectAll();src.selection.copy();
app.activeDocument=d;d.activeLayer=bg;
var photo=d.paste();photo.name='FOTO 08 | soja e oleo editorial';photo.move(bg,ElementPlacement.PLACEBEFORE);
photo.translate(UnitValue(x-photo.bounds[0].as('px'),'px'),UnitValue(y-photo.bounds[1].as('px'),'px'));photo.visible=true;
app.activeDocument=src;src.close(SaveOptions.DONOTSAVECHANGES);app.activeDocument=d;
var content=g.layerSets.add();content.name='BENEFICIOS | layout editorial';
function ink(hex){var c=new SolidColor();c.rgb.hexValue=hex;return c;}
function rect(name,x,y,w,h,hex){var l=content.artLayers.add();l.name=name;d.activeLayer=l;d.selection.select([[x,y],[x+w,y],[x+w,y+h],[x,y+h]]);d.selection.fill(ink(hex));d.selection.deselect();return l;}
function point(name,value,x,y,size,hex,font,track){var l=content.artLayers.add();l.kind=LayerKind.TEXT;l.name=name;var t=l.textItem;t.kind=TextType.POINTTEXT;t.contents=value;t.font=font;t.size=UnitValue(size,'pt');t.color=ink(hex);t.tracking=track;t.position=[UnitValue(x,'px'),UnitValue(y,'px')];return l;}
function para(name,value,x,y,w,h,size,hex,font,track,lead){var l=content.artLayers.add();l.kind=LayerKind.TEXT;l.name=name;var t=l.textItem;t.kind=TextType.PARAGRAPHTEXT;t.contents=value;t.font=font;t.size=UnitValue(size,'pt');t.color=ink(hex);t.tracking=track;t.leading=UnitValue(lead,'pt');t.position=[UnitValue(x,'px'),UnitValue(y,'px')];t.width=UnitValue(w,'px');t.height=UnitValue(h,'px');return l;}
function card(n,y,h,head,body){
 rect('Cartao '+n+' | fundo',145,y,1120,h,'86566F');
 rect('Cartao '+n+' | filete',145,y,7,h,'FFFFFF');
 point('Cartao '+n+' | numero','0'+n,178,y+58,38,'F5B3CB','Gotham-Book',-50);
 rect('Cartao '+n+' | divisor',232,y+23,2,40,'F5B3CB');
 point('Cartao '+n+' | titulo',head,262,y+58,30,'F5B3CB','Gotham-Bold',-55);
 if(body)para('Cartao '+n+' | texto',body,262,y+75,950,h-78,27,'FFFFFF','Gotham-Book',-55,35);
}
card(1,320,205,'HIDRATAÇÃO PROFUNDA DA PELE','O óleo de soja é rico em vitamina E, ômega 6 e 9 e fosfolipídeos. Esses nutrientes ajudam a hidratar, amaciar e restaurar a barreira da pele.');
card(2,565,130,'AÇÃO ANTI-INFLAMATÓRIA E CALMANTE','');
card(3,735,195,'AJUDA A CONTROLAR ODORES','Hidrata a pele, mantém o pH equilibrado e reduz a inflamação, a irritação e a vermelhidão.');
var vis=[];for(var i=0;i<d.layers.length;i++)vis.push(d.layers[i].visible);
for(var i=0;i<d.layers.length;i++)d.layers[i].visible=(d.layers[i]==g||d.layers[i].name=='Plano de Fundo');
var jo=new JPEGSaveOptions();jo.quality=12;d.saveAs(new File(proof),jo,true,Extension.LOWERCASE);
for(var i=0;i<d.layers.length;i++)d.layers[i].visible=vis[i];
d.save();
'OK pagina 08: foto editorial e tres cards, titulo original em um objeto preservado';
