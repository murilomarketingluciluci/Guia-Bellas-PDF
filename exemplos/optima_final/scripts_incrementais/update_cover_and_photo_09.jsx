#target photoshop
app.displayDialogs=DialogModes.NO;
var target='C:/Users/Murilo/Documents/Codex/2026-10-14/tes/outputs/optima_apn_bellas_final.psd';
var source='C:/Users/Murilo/Documents/Codex/2026-10-14/tes/outputs/optima_assets/foto_09_neutra_optima.png';
var backup='C:/Users/Murilo/Documents/Codex/2026-10-14/tes/work/optima_antes_capa_e_foto09.psd';
var outDir='C:/Users/Murilo/Documents/Codex/2026-10-14/tes/outputs/optima_provas/';
var d=null;
for(var i=0;i<app.documents.length;i++) if(app.documents[i].fullName.fsName.replace(/\\/g,'/').toLowerCase()==target.toLowerCase()) d=app.documents[i];
if(!d)d=app.open(new File(target));app.activeDocument=d;
var cover=null,page=null;
for(var i=0;i<d.layerSets.length;i++){
 if(d.layerSets[i].name.indexOf('01')==0)cover=d.layerSets[i];
 if(d.layerSets[i].name.indexOf('09')==0)page=d.layerSets[i];
}
if(!cover||!page)throw Error('Capa ou pagina 09 ausente');
var c=cover.layerSets.getByName('CONTENT');
var names=['NANOTECNOLOGIA','TOQUE SECO','LIVRE DE ALUMÍNIO'];
for(var j=0;j<names.length;j++) if(!c.artLayers.getByName(names[j]))throw Error('Beneficio ausente: '+names[j]);
var title=c.artLayers.getByName('Desodorante Optima');
if(title.kind!=LayerKind.TEXT)throw Error('Titulo da capa deixou de ser texto editavel');
var oldPhoto=null;
for(var i=0;i<page.artLayers.length;i++) if(page.artLayers[i].name.indexOf('FOTO 09 |')==0)oldPhoto=page.artLayers[i];
if(!oldPhoto)throw Error('Foto 09 ausente');
var b=oldPhoto.bounds;
if(Math.abs(b[0].as('px'))>5||Math.abs(b[1].as('px'))>5||Math.abs(b[2].as('px')-670)>5||Math.abs(b[3].as('px')-1080)>5)throw Error('Foto 09 mudou de geometria');
var opts=new PhotoshopSaveOptions();opts.layers=true;
d.saveAs(new File(backup),opts,true,Extension.LOWERCASE);
for(var j=0;j<names.length;j++)c.artLayers.getByName(names[j]).visible=false;
var src=app.open(new File(source)),w=670,h=1080,sw=src.width.as('px'),sh=src.height.as('px'),scale=Math.max(w/sw,h/sh);
src.resizeImage(UnitValue(Math.ceil(sw*scale),'px'),UnitValue(Math.ceil(sh*scale),'px'),null,ResampleMethod.BICUBIC);
var rw=src.width.as('px'),rh=src.height.as('px'),cx=Math.max(0,(rw-w)/2),cy=Math.max(0,(rh-h)/2);
src.crop([UnitValue(cx,'px'),UnitValue(cy,'px'),UnitValue(cx+w,'px'),UnitValue(cy+h,'px')]);
src.selection.selectAll();src.selection.copy();
app.activeDocument=d;d.activeLayer=oldPhoto;
var fresh=d.paste();fresh.name='FOTO 09 | Optima neutra com produto';
fresh.move(oldPhoto,ElementPlacement.PLACEBEFORE);
fresh.translate(UnitValue(-fresh.bounds[0].as('px'),'px'),UnitValue(-fresh.bounds[1].as('px'),'px'));
oldPhoto.remove();fresh.visible=true;
app.activeDocument=src;src.close(SaveOptions.DONOTSAVECHANGES);app.activeDocument=d;
function proof(g,path){
 var vis=[];for(var i=0;i<d.layers.length;i++)vis.push(d.layers[i].visible);
 for(var i=0;i<d.layers.length;i++)d.layers[i].visible=(d.layers[i]==g||d.layers[i].name=='Plano de Fundo');
 var o=new JPEGSaveOptions();o.quality=12;d.saveAs(new File(path),o,true,Extension.LOWERCASE);
 for(var i=0;i<d.layers.length;i++)d.layers[i].visible=vis[i];
}
proof(cover,outDir+'pagina_01.jpg');
proof(page,outDir+'pagina_09.jpg');
d.save();
'OK: capa so titulo; foto 09 substituida; provas 01 e 09 exportadas';
