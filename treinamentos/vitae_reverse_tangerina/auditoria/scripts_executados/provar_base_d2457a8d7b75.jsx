#target photoshop
(function(){
var root="C:/Users/Murilo/Documents/Projetos/Bellas/Lives/Guia_Bellas_IA/Criador de PDF Agente/treinamentos/vitae_reverse_tangerina";
var oldDialogs=app.displayDialogs;var oldUnits=app.preferences.rulerUnits;
app.displayDialogs=DialogModes.NO;app.preferences.rulerUnits=Units.PIXELS;
function esc(s){return '"'+String(s).replace(/\\/g,'\\\\').replace(/"/g,'\\"').replace(/\r/g,'\\r').replace(/\n/g,'\\n')+'"';}
function write(path,s){var f=new File(path);f.encoding="UTF8";f.open("w");f.write(s);f.close();}
try{
var doc=app.open(new File(root+"/planejamento/molde_inicial.psd"));
var inv=[];
function walk(g,p){for(var i=0;i<g.layers.length;i++){var l=g.layers[i];var x='{'+ '"path":'+esc(p+l.name)+',"typename":'+esc(l.typename)+',"visible":'+l.visible;if(l.typename==="ArtLayer"&&l.kind===LayerKind.TEXT){x+=',"text":'+esc(l.textItem.contents)+',"font":'+esc(l.textItem.font)+',"size":'+l.textItem.size.as("pt");}inv.push(x+'}');if(l.typename==="LayerSet")walk(l,p+l.name+"/");}}
walk(doc,"");write(root+"/auditoria/molde_aberto_photoshop.json",'{"width":'+doc.width.as("px")+',"height":'+doc.height.as("px")+',"resolution":'+doc.resolution+',"layers":['+inv.join(',')+']}');
var folder=new Folder(root+"/planejamento/provas_base");if(!folder.exists)folder.create();
var opt=new ExportOptionsSaveForWeb();opt.format=SaveDocumentType.PNG;opt.PNG8=false;opt.transparency=true;opt.interlaced=false;opt.convertToSRGB=true;opt.includeProfile=true;
var names=["CAPA APROVADA - ALTERAR SOMENTE TITULO","TEMA CLARO VAZIO - DUPLICAR","TEMA ESCURO VAZIO - DUPLICAR","AGRADECIMENTO APROVADO - ULTIMA PAGINA"];
for(var j=0;j<names.length;j++){for(var i=0;i<doc.layerSets.length;i++)doc.layerSets[i].visible=doc.layerSets[i].name===names[j];doc.exportDocument(new File(folder.fsName+"/base_"+(j+1)+".png"),ExportType.SAVEFORWEB,opt);}
doc.close(SaveOptions.DONOTSAVECHANGES);
return "Molde aberto e quatro bases exportadas; fonte preservada.";
}finally{app.displayDialogs=oldDialogs;app.preferences.rulerUnits=oldUnits;}
})();
