#target photoshop
app.displayDialogs=DialogModes.NO;
var p='C:/Users/Murilo/Documents/Codex/2026-10-14/tes/outputs/optima_teste_pagina_09_modelo_recortada.psd';
var jpg='C:/Users/Murilo/Documents/Codex/2026-10-14/tes/outputs/optima_teste_pagina_09_modelo_recortada.jpg';
var d=app.open(new File(p)),page=null,photo=null,cut=null;
for(var i=0;i<d.layerSets.length;i++)if(d.layerSets[i].name.indexOf('09')==0)page=d.layerSets[i];
for(var i=0;i<page.artLayers.length;i++){
 if(page.artLayers[i].name.indexOf('FOTO 09 |')==0)photo=page.artLayers[i];
 if(page.artLayers[i].name.indexOf('TESTE | modelo recortada')==0)cut=page.artLayers[i];
}
if(!photo||!cut)throw Error('Camadas ausentes');
photo.visible=false;cut.visible=true;
var b=cut.bounds,h=b[3].as('px')-b[1].as('px'),scale=116;
cut.resize(scale,scale,AnchorPosition.TOPLEFT);
cut.translate(UnitValue(0-cut.bounds[0].as('px'),'px'),UnitValue(135-cut.bounds[1].as('px'),'px'));
var vis=[];for(var i=0;i<d.layers.length;i++)vis.push(d.layers[i].visible);
for(var i=0;i<d.layers.length;i++)d.layers[i].visible=(d.layers[i]==page||d.layers[i].name=='Plano de Fundo');
var jo=new JPEGSaveOptions();jo.quality=12;d.saveAs(new File(jpg),jo,true,Extension.LOWERCASE);
for(var i=0;i<d.layers.length;i++)d.layers[i].visible=vis[i];
d.save();d.close(SaveOptions.DONOTSAVECHANGES);
'OK: modelo recortada estendida ate fora da base, sem linha de corte';
