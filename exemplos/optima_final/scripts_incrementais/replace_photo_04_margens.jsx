#target photoshop
app.displayDialogs=DialogModes.NO;
var target='C:/Users/Murilo/Documents/Codex/2026-10-14/tes/outputs/optima_apn_bellas_final.psd';
var source='C:/Users/Murilo/Documents/Codex/2026-10-14/tes/outputs/optima_assets/foto_04_espresso_margens_15.png';
var proof='C:/Users/Murilo/Documents/Codex/2026-10-14/tes/outputs/optima_provas/pagina_04.jpg';
var d=null;
for(var i=0;i<app.documents.length;i++)if(app.documents[i].fullName.fsName.replace(/\\/g,'/').toLowerCase()==target.toLowerCase())d=app.documents[i];
if(!d)d=app.open(new File(target));app.activeDocument=d;
var g=null,photo=null,placeholder=null;
for(var i=0;i<d.layerSets.length;i++)if(d.layerSets[i].name.indexOf('04')==0)g=d.layerSets[i];
if(!g)throw Error('Pagina 04 ausente');
for(var i=0;i<g.artLayers.length;i++){
 var l=g.artLayers[i];
 if(l.name.indexOf('FOTO 04 | fundo neutro')==0)photo=l;
 if(l.name.indexOf('FOTO 04 | substituir imagem')==0)placeholder=l;
}
if(!photo)throw Error('Foto 04 corrente nao encontrada');
var x=0,y=0,w=730,h=1080;
var src=app.open(new File(source)),sw=src.width.as('px'),sh=src.height.as('px'),scale=Math.max(w/sw,h/sh);
src.resizeImage(UnitValue(Math.ceil(sw*scale),'px'),UnitValue(Math.ceil(sh*scale),'px'),null,ResampleMethod.BICUBIC);
var rw=src.width.as('px'),rh=src.height.as('px'),cx=(rw-w)/2,cy=(rh-h)/2;
src.crop([UnitValue(cx,'px'),UnitValue(cy,'px'),UnitValue(cx+w,'px'),UnitValue(cy+h,'px')]);
src.selection.selectAll();src.selection.copy();
app.activeDocument=d;d.activeLayer=photo;
var fresh=d.paste();fresh.name='FOTO 04 | espresso margens 15pct';
fresh.move(photo,ElementPlacement.PLACEBEFORE);
fresh.translate(UnitValue(x-fresh.bounds[0].as('px'),'px'),UnitValue(y-fresh.bounds[1].as('px'),'px'));
photo.remove();if(placeholder)placeholder.visible=false;
for(var i=0;i<g.artLayers.length;i++){
 var keep=g.artLayers[i];
 if(keep.name.indexOf('Camada 1')==0||keep.name.indexOf('FUNDO')==0||keep==fresh)keep.visible=true;
}
fresh.visible=true;
app.activeDocument=src;src.close(SaveOptions.DONOTSAVECHANGES);app.activeDocument=d;
var old=[];for(var i=0;i<d.layers.length;i++)old.push(d.layers[i].visible);
for(var i=0;i<d.layers.length;i++)d.layers[i].visible=(d.layers[i]==g||d.layers[i].name=='Plano de Fundo');
var f=new File(proof),o=new JPEGSaveOptions();o.quality=12;d.saveAs(f,o,true,Extension.LOWERCASE);
for(var i=0;i<d.layers.length;i++)d.layers[i].visible=old[i];
d.save();
'OK foto 04: '+fresh.name;
