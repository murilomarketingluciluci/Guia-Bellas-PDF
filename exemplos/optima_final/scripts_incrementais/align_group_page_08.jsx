#target photoshop
app.displayDialogs=DialogModes.NO;
var target='C:/Users/Murilo/Documents/Codex/2026-10-14/tes/outputs/optima_apn_bellas_final.psd';
var backup='C:/Users/Murilo/Documents/Codex/2026-10-14/tes/work/optima_antes_alinhar_cards_08.psd';
var proof='C:/Users/Murilo/Documents/Codex/2026-10-14/tes/outputs/optima_provas/pagina_08.jpg';
var d=null;for(var i=0;i<app.documents.length;i++)if(app.documents[i].fullName.fsName.replace(/\\/g,'/').toLowerCase()==target.toLowerCase())d=app.documents[i];
if(!d)d=app.open(new File(target));app.activeDocument=d;
var page=null;for(var i=0;i<d.layerSets.length;i++)if(d.layerSets[i].name.indexOf('08')==0)page=d.layerSets[i];
var content=page.layerSets.getByName('BENEFICIOS | layout editorial');
if(!content)throw Error('Layout editorial da pagina 08 ausente');
var opts=new PhotoshopSaveOptions();opts.layers=true;d.saveAs(new File(backup),opts,true,Extension.LOWERCASE);
var titles=['HIDRATAÇÃO PROFUNDA DA PELE','AÇÃO ANTI-INFLAMATÓRIA E CALMANTE','AJUDA A CONTROLAR ODORES'];
for(var n=1;n<=3;n++){
 var layers=[];
 for(var i=0;i<content.artLayers.length;i++)if(content.artLayers[i].name.indexOf('Cartao '+n+' |')==0)layers.push(content.artLayers[i]);
 if(layers.length<5)throw Error('Cartao '+n+' incompleto');
 for(var j=0;j<layers.length;j++){
  var l=layers[j];
  if(l.name.indexOf('| numero')>0){l.textItem.size=UnitValue(30,'pt');l.textItem.tracking=-55;}
  if(l.name.indexOf('| fundo')<0&&l.name.indexOf('| filete')<0)l.translate(UnitValue(0,'px'),UnitValue(16,'px'));
 }
 var group=content.layerSets.add();group.name='BENEFÍCIO 0'+n+' | '+titles[n-1];
 for(var j=layers.length-1;j>=0;j--)layers[j].move(group,ElementPlacement.INSIDE);
}
var vis=[];for(var i=0;i<d.layers.length;i++)vis.push(d.layers[i].visible);
for(var i=0;i<d.layers.length;i++)d.layers[i].visible=(d.layers[i]==page||d.layers[i].name=='Plano de Fundo');
var jo=new JPEGSaveOptions();jo.quality=12;d.saveAs(new File(proof),jo,true,Extension.LOWERCASE);
for(var i=0;i<d.layers.length;i++)d.layers[i].visible=vis[i];
d.save();
'OK: cartoes agrupados e conteudo centralizado';
