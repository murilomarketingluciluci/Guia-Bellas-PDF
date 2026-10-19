#target photoshop
app.displayDialogs=DialogModes.NO;
var target='C:/Users/Murilo/Documents/Codex/2026-10-14/tes/outputs/optima_apn_bellas_final.psd';
var source='C:/Users/Murilo/Documents/Codex/2026-10-14/tes/outputs/optima_assets/foto_10_adaptacao_cena_continua.png';
var backup='C:/Users/Murilo/Documents/Codex/2026-10-14/tes/work/optima_antes_correcao_foto_10.psd';
var proof='C:/Users/Murilo/Documents/Codex/2026-10-14/tes/outputs/optima_provas/pagina_10.jpg';
var d=null;
for(var i=0;i<app.documents.length;i++)if(app.documents[i].fullName.fsName.replace(/\\/g,'/').toLowerCase()==target.toLowerCase())d=app.documents[i];
if(!d)d=app.open(new File(target));app.activeDocument=d;
var g=null,oldPhoto=null,base=null;
for(var i=0;i<d.layerSets.length;i++)if(d.layerSets[i].name.indexOf('10')==0)g=d.layerSets[i];
if(!g)throw Error('Pagina 10 ausente');
for(var i=0;i<g.artLayers.length;i++){
 var l=g.artLayers[i],b=l.bounds;
 if(l.name.indexOf('FOTO 10 |')==0)oldPhoto=l;
 if(Math.abs(b[0].as('px')-1336)<12&&Math.abs(b[2].as('px')-1920)<12&&Math.abs(b[1].as('px'))<12)base=l;
}
if(!oldPhoto||!base)throw Error('Foto atual ou faixa base ausente; nenhuma mudanca feita');
var opts=new PhotoshopSaveOptions();opts.layers=true;
d.saveAs(new File(backup),opts,true,Extension.LOWERCASE);
var x=1336,y=0,w=584,h=1080;
var src=app.open(new File(source)),sw=src.width.as('px'),sh=src.height.as('px'),scale=Math.max(w/sw,h/sh);
src.resizeImage(UnitValue(Math.ceil(sw*scale),'px'),UnitValue(Math.ceil(sh*scale),'px'),null,ResampleMethod.BICUBIC);
var rw=src.width.as('px'),rh=src.height.as('px'),cx=Math.max(0,(rw-w)/2),cy=Math.max(0,(rh-h)/2);
src.crop([UnitValue(cx,'px'),UnitValue(cy,'px'),UnitValue(cx+w,'px'),UnitValue(cy+h,'px')]);
src.selection.selectAll();src.selection.copy();
app.activeDocument=d;d.activeLayer=oldPhoto;
var fresh=d.paste();fresh.name='FOTO 10 | cena continua sem faixa';
fresh.move(oldPhoto,ElementPlacement.PLACEBEFORE);
fresh.translate(UnitValue(x-fresh.bounds[0].as('px'),'px'),UnitValue(y-fresh.bounds[1].as('px'),'px'));
oldPhoto.remove();fresh.visible=true;
app.activeDocument=src;src.close(SaveOptions.DONOTSAVECHANGES);app.activeDocument=d;
var old=[];for(var i=0;i<d.layers.length;i++)old.push(d.layers[i].visible);
for(var i=0;i<d.layers.length;i++)d.layers[i].visible=(d.layers[i]==g||d.layers[i].name=='Plano de Fundo');
var f=new File(proof),o=new JPEGSaveOptions();o.quality=12;d.saveAs(f,o,true,Extension.LOWERCASE);
for(var i=0;i<d.layers.length;i++)d.layers[i].visible=old[i];
d.save();
'OK foto 10 continua: '+fresh.name;
