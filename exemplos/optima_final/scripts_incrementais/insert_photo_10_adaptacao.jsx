#target photoshop
app.displayDialogs = DialogModes.NO;

var target = 'C:/Users/Murilo/Documents/Codex/2026-10-14/tes/outputs/optima_apn_bellas_final.psd';
var source = 'C:/Users/Murilo/Documents/Codex/2026-10-14/tes/outputs/optima_assets/foto_10_adaptacao_real.png';
var backup = 'C:/Users/Murilo/Documents/Codex/2026-10-14/tes/work/optima_antes_foto_10_adaptacao.psd';
var proof = 'C:/Users/Murilo/Documents/Codex/2026-10-14/tes/outputs/optima_provas/pagina_10.jpg';
var d = null;
for (var i=0; i<app.documents.length; i++) {
  if (app.documents[i].fullName.fsName.replace(/\\/g,'/').toLowerCase() == target.toLowerCase()) d=app.documents[i];
}
if (!d) d=app.open(new File(target));
app.activeDocument=d;
var page=null,base=null,existing=null;
for (var i=0;i<d.layerSets.length;i++) if (d.layerSets[i].name.indexOf('10')==0) page=d.layerSets[i];
if (!page) throw Error('Pagina 10 ausente');
for (var i=0;i<page.artLayers.length;i++) {
  var l=page.artLayers[i], b=l.bounds;
  if (Math.abs(b[0].as('px')-1336)<12 && Math.abs(b[2].as('px')-1920)<12 && Math.abs(b[1].as('px'))<12) base=l;
  if (l.name.indexOf('FOTO 10 |')==0) existing=l;
}
if (!base) throw Error('Faixa direita da pagina 10 mudou; nenhuma mudanca feita');
if (existing) throw Error('Pagina 10 ja tem foto; revisar antes de substituir');

// Salva o estado corrente, incluindo ajustes manuais ainda nao gravados.
var psdOptions=new PhotoshopSaveOptions();
psdOptions.layers=true;
d.saveAs(new File(backup),psdOptions,true,Extension.LOWERCASE);

var x=1336,y=0,w=584,h=1080;
var src=app.open(new File(source));
var sw=src.width.as('px'),sh=src.height.as('px'),scale=Math.max(w/sw,h/sh);
src.resizeImage(UnitValue(Math.ceil(sw*scale),'px'),UnitValue(Math.ceil(sh*scale),'px'),null,ResampleMethod.BICUBIC);
var rw=src.width.as('px'),rh=src.height.as('px');
var cx=Math.max(0,(rw-w)/2),cy=Math.max(0,(rh-h)/2);
src.crop([UnitValue(cx,'px'),UnitValue(cy,'px'),UnitValue(cx+w,'px'),UnitValue(cy+h,'px')]);
src.selection.selectAll();src.selection.copy();
app.activeDocument=d;d.activeLayer=base;
var fresh=d.paste();
fresh.name='FOTO 10 | adaptacao espontanea';
fresh.move(base,ElementPlacement.PLACEBEFORE);
fresh.translate(UnitValue(x-fresh.bounds[0].as('px'),'px'),UnitValue(y-fresh.bounds[1].as('px'),'px'));
fresh.visible=true;
app.activeDocument=src;src.close(SaveOptions.DONOTSAVECHANGES);app.activeDocument=d;

var old=[];
for(var i=0;i<d.layers.length;i++) old.push(d.layers[i].visible);
for(var i=0;i<d.layers.length;i++) d.layers[i].visible=(d.layers[i]==page || d.layers[i].name=='Plano de Fundo');
var f=new File(proof),o=new JPEGSaveOptions();o.quality=12;
d.saveAs(f,o,true,Extension.LOWERCASE);
for(var i=0;i<d.layers.length;i++) d.layers[i].visible=old[i];
d.save();
'OK foto 10: '+fresh.name;
