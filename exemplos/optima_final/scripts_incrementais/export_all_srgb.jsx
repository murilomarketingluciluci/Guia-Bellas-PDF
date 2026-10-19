#target photoshop
app.displayDialogs=DialogModes.NO;
var root='C:/Users/Murilo/Documents/Codex/2026-10-14/tes/';
var outFolder=new Folder(root+'work/srgb_provas');if(!outFolder.exists)outFolder.create();
for(var j=app.documents.length-1;j>=0;j--)if(app.documents[j].name=='Exportacao final sRGB')app.documents[j].close(SaveOptions.DONOTSAVECHANGES);
var d=null;for(var i=0;i<app.documents.length;i++)if(app.documents[i].name=='optima_apn_bellas_final.psd')d=app.documents[i];
if(!d)throw Error('PSD principal nao esta aberto');
var t=d.duplicate('Exportacao final sRGB',false);app.activeDocument=t;
t.colorProfileName='sRGB IEC61966-2.1';
if(t.colorProfileName!='sRGB IEC61966-2.1')throw Error('Perfil sRGB nao aplicado');
var pages=[];for(var i=0;i<t.layerSets.length;i++){var g=t.layerSets[i];var m=/^(\d\d)\b/.exec(g.name);if(m)pages[parseInt(m[1],10)]=g;}
for(var n=1;n<=12;n++)if(!pages[n])throw Error('Pagina '+n+' ausente');
var jo=new JPEGSaveOptions();jo.quality=12;jo.embedColorProfile=true;
for(var n=1;n<=12;n++){
 for(var i=0;i<t.layers.length;i++){var l=t.layers[i];l.visible=(l==pages[n]||l.name=='Plano de Fundo');}
 var id=n<10?'0'+n:''+n;
 t.saveAs(new File(root+'work/srgb_provas/pagina_'+id+'.jpg'),jo,true,Extension.LOWERCASE);
}
t.close(SaveOptions.DONOTSAVECHANGES);app.activeDocument=d;
'OK: 12 paginas exportadas do PSD corrente com ICC sRGB incorporado';
