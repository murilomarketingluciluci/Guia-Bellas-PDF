#target photoshop
app.displayDialogs=DialogModes.NO;
var root='C:/Users/Murilo/Documents/Codex/2026-10-14/tes/';
var target=root+'outputs/optima_apn_bellas_final.psd';
var backup=root+'work/optima_antes_fotos_04_10.psd';
var d=null;
for(var i=0;i<app.documents.length;i++)if(app.documents[i].fullName.fsName.replace(/\\/g,'/').toLowerCase()==target.toLowerCase())d=app.documents[i];
if(!d)d=app.open(new File(target));
app.activeDocument=d;
function findPage(n){for(var i=0;i<d.layerSets.length;i++)if(d.layerSets[i].name.indexOf(n)==0)return d.layerSets[i];throw Error('Pagina '+n+' ausente');}
function findLayer(g,prefix){for(var i=0;i<g.artLayers.length;i++)if(g.artLayers[i].name.indexOf(prefix)==0)return g.artLayers[i];throw Error('Camada '+prefix+' ausente');}
var p4=findPage('04'),old4=findLayer(p4,'FOTO 04 | espresso');
var p10=findPage('10'),old10=findLayer(p10,'FOTO 10 |'),white=findLayer(p10,'Ret');
for(var k=0;k<p4.artLayers.length;k++)if(p4.artLayers[k].name.indexOf('FOTO 04 | modelo recortada e Optima')==0)throw Error('Foto 04 ja aplicada');
for(var k=0;k<p10.artLayers.length;k++)if(p10.artLayers[k].name.indexOf('FOTO 10 | modelo recortada e Optima')==0)throw Error('Foto 10 ja aplicada');
var opts=new PhotoshopSaveOptions();opts.layers=true;d.saveAs(new File(backup),opts,true,Extension.LOWERCASE);
function addRaster(path,anchor,name,x,y,w,h,crop){
 var src=app.open(new File(path)),sw=src.width.as('px'),sh=src.height.as('px');
 var scale=crop?Math.max(w/sw,h/sh):h/sh;
 src.resizeImage(UnitValue(Math.ceil(sw*scale),'px'),UnitValue(Math.ceil(sh*scale),'px'),null,ResampleMethod.BICUBIC);
 if(crop){var rw=src.width.as('px'),rh=src.height.as('px'),cx=Math.max(0,(rw-w)/2),cy=Math.max(0,(rh-h)/2);src.crop([UnitValue(cx,'px'),UnitValue(cy,'px'),UnitValue(cx+w,'px'),UnitValue(cy+h,'px')]);}
 src.selection.selectAll();src.selection.copy();app.activeDocument=d;d.activeLayer=anchor;
 var l=d.paste();l.name=name;l.move(anchor,ElementPlacement.PLACEBEFORE);l.translate(UnitValue(x-l.bounds[0].as('px'),'px'),UnitValue(y-l.bounds[1].as('px'),'px'));
 app.activeDocument=src;src.close(SaveOptions.DONOTSAVECHANGES);app.activeDocument=d;return l;
}
function proof(p,n){var vis=[];for(var i=0;i<d.layers.length;i++)vis.push(d.layers[i].visible);for(var i=0;i<d.layers.length;i++)d.layers[i].visible=(d.layers[i]==p||d.layers[i].name=='Plano de Fundo');var jo=new JPEGSaveOptions();jo.quality=12;d.saveAs(new File(root+'outputs/optima_provas/pagina_'+n+'.jpg'),jo,true,Extension.LOWERCASE);for(var i=0;i<d.layers.length;i++)d.layers[i].visible=vis[i];}
var env=addRaster(root+'outputs/optima_assets/foto_04_ambiente_real_neutro.png',old4,'FOTO 04 | ambiente real neutro',0,0,730,1080,true);
var cut4=addRaster(root+'outputs/optima_assets/foto_04_modelo_joias_optima_recorte_final.png',env,'FOTO 04 | modelo recortada e Optima',20,120,0,1000,false);
old4.visible=false;env.visible=true;cut4.visible=true;proof(p4,'04');
var cut10=addRaster(root+'outputs/optima_assets/foto_10_modelo_touca_optima_recorte_final.png',old10,'FOTO 10 | modelo recortada e Optima',1335,130,0,950,false);
old10.visible=false;white.visible=false;cut10.visible=true;proof(p10,'10');
d.save();
'OK: fotos 04 e 10 aplicadas e provas exportadas';
