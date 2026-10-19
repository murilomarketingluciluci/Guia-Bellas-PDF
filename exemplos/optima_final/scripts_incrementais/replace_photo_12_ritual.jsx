#target photoshop
app.displayDialogs = DialogModes.NO;
var target = 'C:/Users/Murilo/Documents/Codex/2026-10-14/tes/outputs/optima_apn_bellas_final.psd';
var source = 'C:/Users/Murilo/Documents/Codex/2026-10-14/tes/outputs/optima_assets/foto_12_ritual_optima_sem_tatuagem.png';
var proof = 'C:/Users/Murilo/Documents/Codex/2026-10-14/tes/outputs/optima_provas/pagina_12.jpg';
var d = null;
for (var i=0; i<app.documents.length; i++) {
  if (app.documents[i].fullName.fsName.replace(/\\/g,'/').toLowerCase() == target.toLowerCase()) d=app.documents[i];
}
if (!d) d=app.open(new File(target));
app.activeDocument=d;
var page=null, base=null, oldPhoto=null;
for (var i=0; i<d.layerSets.length; i++) if (d.layerSets[i].name.indexOf('12')==0) page=d.layerSets[i];
if (!page) throw Error('Pagina 12 ausente');
for (var i=0; i<page.artLayers.length; i++) {
  var l=page.artLayers[i];
  if (l.name.indexOf('Ret')==0 && l.name.indexOf(' 2')>0) base=l;
  if (l.name.indexOf('FOTO 12 |')==0) oldPhoto=l;
}
if (!base || !oldPhoto) throw Error('Foto antiga ou base da faixa nao encontrada; nenhuma mudanca feita');
var b=base.bounds;
var x=1129,y=0,w=791,h=1080;
if (Math.abs(b[0].as('px')-x)>10 || Math.abs(b[2].as('px')-1920)>50) throw Error('Geometria da faixa mudou; revisar antes');
var src=app.open(new File(source));
var sw=src.width.as('px'),sh=src.height.as('px'),scale=Math.max(w/sw,h/sh);
src.resizeImage(UnitValue(Math.ceil(sw*scale),'px'),UnitValue(Math.ceil(sh*scale),'px'),null,ResampleMethod.BICUBIC);
var rw=src.width.as('px'),rh=src.height.as('px');
var cx=(rw-w)/2,cy=(rh-h)/2;
src.crop([UnitValue(cx,'px'),UnitValue(cy,'px'),UnitValue(cx+w,'px'),UnitValue(cy+h,'px')]);
src.selection.selectAll();src.selection.copy();
app.activeDocument=d;d.activeLayer=base;
var fresh=d.paste();
fresh.name='FOTO 12 | ritual Optima sem tatuagem';
fresh.move(base,ElementPlacement.PLACEBEFORE);
fresh.translate(UnitValue(x-fresh.bounds[0].as('px'),'px'),UnitValue(y-fresh.bounds[1].as('px'),'px'));
oldPhoto.remove();
app.activeDocument=src;src.close(SaveOptions.DONOTSAVECHANGES);app.activeDocument=d;
var old=[];for (var i=0;i<d.layers.length;i++) old.push(d.layers[i].visible);
for (var i=0;i<d.layers.length;i++) d.layers[i].visible=(d.layers[i]==page || d.layers[i].name=='Plano de Fundo');
var f=new File(proof),o=new JPEGSaveOptions();o.quality=12;d.saveAs(f,o,true,Extension.LOWERCASE);
for (var i=0;i<d.layers.length;i++) d.layers[i].visible=old[i];
d.save();
'OK foto 12: '+fresh.name;
