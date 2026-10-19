#target photoshop
(function(){
var R='C:/Users/Murilo/Documents/Projetos/Bellas/Lives/Guia_Bellas_IA/Criador de PDF Agente/treinamentos/vitae_reverse_tangerina';
var old=app.displayDialogs;app.displayDialogs=DialogModes.NO;var d=null;
try{d=app.open(new File(R+'/producao/vitae_reverse_com_fotos.psd'));var folder=new Folder(R+'/auditoria/reabertura_fotos');if(!folder.exists)folder.create();var o=new ExportOptionsSaveForWeb();o.format=SaveDocumentType.PNG;o.PNG8=false;o.transparency=false;o.interlaced=false;o.convertToSRGB=true;o.includeProfile=true;
for(var n=1;n<=9;n++){var g=null;for(var i=0;i<d.layerSets.length;i++)if(parseInt(d.layerSets[i].name,10)===n)g=d.layerSets[i];if(!g)throw Error('Pagina ausente '+n);for(var k=0;k<d.layers.length;k++)d.layers[k].visible=d.layers[k]===g||d.layers[k].name==='Plano de Fundo';d.exportDocument(new File(folder.fsName+'/pagina_'+('0'+n).slice(-2)+'.png'),ExportType.SAVEFORWEB,o);}
d.close(SaveOptions.DONOTSAVECHANGES);return 'PSD reaberto; nove provas para comparacao exportadas.';
}finally{app.displayDialogs=old;}
})();
