#target photoshop
// Correções pontuais em uma página por execução, após revisão humana dos agentes.
(function(){
 app.displayDialogs=DialogModes.NO;
 var project=new File($.fileName).parent.parent;
 var job=new File(project.fsName+'/scripts/pagina_atual.json');job.open('r');var n=eval('('+job.read()+')').page;job.close();
 var dest=new File(project.fsName+'/entrega/crescimento_luciane_bellas.psd'),d=null;
 for(var i=0;i<app.documents.length;i++)try{if(app.documents[i].fullName.fsName===dest.fsName)d=app.documents[i];}catch(e){}
 if(!d)d=app.open(dest);app.activeDocument=d;
 var snap=new File(project.fsName+'/auditoria/antes_revisao_critica.psd');
 if(!snap.exists){var save=new PhotoshopSaveOptions();save.layers=true;d.saveAs(snap,save,true,Extension.LOWERCASE);}
 var g=null;for(var i=0;i<d.layerSets.length;i++)if(parseInt(d.layerSets[i].name,10)===n)g=d.layerSets[i];if(!g)throw Error('Página ausente');
 function find(group,match){for(var i=0;i<group.layers.length;i++){var l=group.layers[i];if(l.typename==='LayerSet'){var x=find(l,match);if(x)return x;}else if(match.test(l.name))return l;}return null;}
 function unit(v){return UnitValue(v,'px');}
 function sid(x){return stringIDToTypeID(x)}function cid(x){return charIDToTypeID(x)}
 if(n===1){
  var l=find(g,/^H1 \|/),old=l.bounds,x=old[0].as('px'),y=old[1].as('px');
  var r=new ActionReference();r.putIdentifier(cid('Lyr '),l.id);var td=executeActionGet(r).getObjectValue(sid('textKey'));
  var style=td.getList(sid('textStyleRange')).getObjectValue(0).getObjectValue(sid('textStyle'));
  style.putString(sid('fontPostScriptName'),'Gotham-Book');style.putString(sid('fontName'),'Gotham');style.putString(sid('fontStyleName'),'Book');
  var run=new ActionDescriptor();run.putInteger(sid('from'),0);run.putInteger(sid('to'),l.textItem.contents.length+1);run.putObject(sid('textStyle'),sid('textStyle'),style);
  var list=new ActionList();list.putObject(sid('textStyleRange'),run);td.putList(sid('textStyleRange'),list);
  var set=new ActionDescriptor();set.putReference(cid('null'),r);set.putObject(cid('T   '),cid('TxLr'),td);executeAction(cid('setd'),set,DialogModes.NO);
  l.translate(unit(x-l.bounds[0].as('px')),unit(y-l.bounds[1].as('px')));
 }else if(n===6){find(g,/^CALLOUT \|/).translate(unit(0),unit(-10));
 }else if(n===10){find(g,/^BODY \| João 4$/).translate(unit(0),unit(-129));
 }else if(n===11){var l=find(g,/^CALLOUT \|/),x=l.bounds[0].as('px'),y=l.bounds[1].as('px');l.textItem.size=UnitValue(52,'pt');l.textItem.leading=UnitValue(58.76,'pt');l.translate(unit(x-l.bounds[0].as('px')),unit(y-l.bounds[1].as('px')));
 }else throw Error('Página não autorizada pelo ajuste');
 for(var i=0;i<d.layers.length;i++)d.layers[i].visible=(d.layers[i]===g||d.layers[i].name==='Plano de Fundo');
 d.save();
 var copy=d.duplicate('Prova revisão crítica '+n,false);app.activeDocument=copy;
 try{var o=new ExportOptionsSaveForWeb();o.format=SaveDocumentType.PNG;o.PNG8=false;o.transparency=false;o.interlaced=false;o.convertToSRGB=true;o.includeProfile=true;copy.exportDocument(new File(project.fsName+'/entrega/provas_png/pagina_'+('0'+n).slice(-2)+'.png'),ExportType.SAVEFORWEB,o);}finally{copy.close(SaveOptions.DONOTSAVECHANGES);app.activeDocument=d;}
 var log=new File(project.fsName+'/auditoria/photoshop_execucao.log');log.encoding='UTF8';log.open('a');log.writeln(new Date().toString()+' | Revisão crítica aplicada somente à página '+n);log.close();
 return 'Revisão crítica página '+n+' salva e exportada.';
})();
