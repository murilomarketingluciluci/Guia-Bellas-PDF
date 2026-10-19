#target photoshop
(function(){
 app.displayDialogs=DialogModes.NO;
 var project=new File($.fileName).parent.parent;
 function read(p){var f=new File(project.fsName+'/'+p);f.encoding='UTF8';f.open('r');var v=eval('('+f.read()+')');f.close();return v;}
 function sid(x){return stringIDToTypeID(x)}function cid(x){return charIDToTypeID(x)}
 function ink(hex){var c=new SolidColor();c.rgb.hexValue=hex;return c;}
 function rgb(c){var a=new ActionDescriptor();a.putDouble(cid('Rd  '),c.rgb.red);a.putDouble(cid('Grn '),c.rgb.green);a.putDouble(cid('Bl  '),c.rgb.blue);return a;}
 var job=read('scripts/pagina_atual.json'),manifest=read('manifesto_final.json'),s=manifest.slides[job.page-1],d=null;
 var path=new File(project.fsName+'/entrega/crescimento_luciane_bellas.psd');
 for(var i=0;i<app.documents.length;i++)try{if(app.documents[i].fullName.fsName===path.fsName)d=app.documents[i];}catch(e){}
 if(!d)d=app.open(path);app.activeDocument=d;
 var g=null;for(var i=0;i<d.layerSets.length;i++)if(parseInt(d.layerSets[i].name,10)===job.page)g=d.layerSets[i];if(!g)throw Error('Página ausente');
 var backup=new File(project.fsName+'/auditoria/antes_ajustes_paleta.psd');if(!backup.exists){var o=new PhotoshopSaveOptions();o.layers=true;d.saveAs(backup,o,true,Extension.LOWERCASE);}
 function fill(l,hex){d.activeLayer=l;var set=new ActionDescriptor(),r=new ActionReference();r.putEnumerated(sid('contentLayer'),sid('ordinal'),sid('targetEnum'));set.putReference(sid('null'),r);var v=new ActionDescriptor();v.putObject(sid('color'),sid('RGBColor'),rgb(ink(hex)));set.putObject(sid('to'),sid('solidColorLayer'),v);executeAction(sid('set'),set,DialogModes.NO);}
 function walk(group){for(var k=0;k<group.layers.length;k++){
  var l=group.layers[k];if(l.typename==='LayerSet'){walk(l);continue;}
  if(l.name==='Fundo'||l.name==='Faixa de destaque')fill(l,s.theme==='claro'?'A9708A':'86566F');
  if(s.theme==='escuro'&&l.kind===LayerKind.TEXT&&l.name.indexOf('H1 |')===0){
   var ref=new ActionReference();ref.putIdentifier(cid('Lyr '),l.id);var A=executeActionGet(ref).getObjectValue(sid('textKey')),list=A.getList(sid('textStyleRange')),out=new ActionList();
   for(var a=0;a<list.count;a++){var r=list.getObjectValue(a),st=r.getObjectValue(sid('textStyle'));if(st.hasKey(sid('fontPostScriptName'))&&st.getString(sid('fontPostScriptName'))==='Gotham-Bold')st.putObject(sid('color'),sid('RGBColor'),rgb(ink('E7A7C1')));r.putObject(sid('textStyle'),sid('textStyle'),st);out.putObject(sid('textStyleRange'),r);}
   A.putList(sid('textStyleRange'),out);var set=new ActionDescriptor();set.putReference(cid('null'),ref);set.putObject(cid('T   '),cid('TxLr'),A);executeAction(cid('setd'),set,DialogModes.NO);
  }
 }}
 walk(g);
 for(var i=0;i<d.layers.length;i++)d.layers[i].visible=(d.layers[i]===g||d.layers[i].name==='Plano de Fundo');
 d.save();var copy=d.duplicate('Bellas prova paleta '+job.page,false);app.activeDocument=copy;
 try{var o=new ExportOptionsSaveForWeb();o.format=SaveDocumentType.PNG;o.PNG8=false;o.transparency=false;o.convertToSRGB=true;o.includeProfile=true;copy.exportDocument(new File(project.fsName+'/entrega/provas_png/pagina_'+('0'+job.page).slice(-2)+'.png'),ExportType.SAVEFORWEB,o);}finally{copy.close(SaveOptions.DONOTSAVECHANGES);app.activeDocument=d;}
 var log=new File(project.fsName+'/auditoria/photoshop_execucao.log');log.open('a');log.writeln(new Date().toString()+' | Ajuste pontual de paleta na página '+job.page+' usando RGB armazenado medido na referência aprovada.');log.close();
 return 'Paleta da página '+job.page+' ajustada; conferir RGB exportado.';
})();
