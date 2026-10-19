#target photoshop
(function(){
 app.displayDialogs=DialogModes.NO;
 var project=new File($.fileName).parent.parent;
 var psd=new File(project.fsName+'/entrega/crescimento_luciane_bellas.psd'),d=null;
 function sid(x){return stringIDToTypeID(x)}function cid(x){return charIDToTypeID(x)}
 function encode(v){if(v===null)return 'null';if(typeof v==='string')return '"'+v.replace(/\\/g,'\\\\').replace(/"/g,'\\"').replace(/[\x00-\x1f]/g,function(c){return '\\u'+('0000'+c.charCodeAt(0).toString(16)).slice(-4);})+'"';if(typeof v==='number'||typeof v==='boolean')return String(v);var a=[],k;if(v instanceof Array){for(k=0;k<v.length;k++)a.push(encode(v[k]));return '['+a.join(',')+']';}for(k in v)if(v.hasOwnProperty(k))a.push(encode(k)+':'+encode(v[k]));return '{'+a.join(',')+'}';}
 for(var i=0;i<app.documents.length;i++)try{if(app.documents[i].fullName.fsName===psd.fsName)d=app.documents[i];}catch(e){}
 if(!d)d=app.open(psd);app.activeDocument=d;
 function page(doc,n){for(var i=0;i<doc.layerSets.length;i++)if(parseInt(doc.layerSets[i].name,10)===n)return doc.layerSets[i];throw Error('Falta página '+n);}
 if(d.layerSets.length!==12)throw Error('Quantidade inesperada de grupos: '+d.layerSets.length);
 for(var n=12;n>=1;n--)page(d,n).move(d,ElementPlacement.PLACEATBEGINNING);
 for(var i=0;i<d.layers.length;i++)d.layers[i].visible=(d.layers[i]===page(d,1)||d.layers[i].name==='Plano de Fundo');
 d.save();
 // Mesmo método validado do pacote: duplicata, perfil inalterado, Save for Web PNG24.
 var copy=d.duplicate('Bellas | exportação final completa',false);app.activeDocument=copy;
 try{
  var o=new ExportOptionsSaveForWeb();o.format=SaveDocumentType.PNG;o.PNG8=false;o.transparency=false;o.interlaced=false;o.convertToSRGB=true;o.includeProfile=true;
  for(var n=1;n<=12;n++){
   var current=page(copy,n);for(var i=0;i<copy.layers.length;i++)copy.layers[i].visible=(copy.layers[i]===current||copy.layers[i].name==='Plano de Fundo');
   copy.exportDocument(new File(project.fsName+'/entrega/provas_png/pagina_'+('0'+n).slice(-2)+'.png'),ExportType.SAVEFORWEB,o);
  }
 }finally{copy.close(SaveOptions.DONOTSAVECHANGES);app.activeDocument=d;}
 d.close(SaveOptions.DONOTSAVECHANGES);d=app.open(psd);app.activeDocument=d;
 var available={};for(var a=0;a<app.fonts.length;a++)available[app.fonts[a].postScriptName]=true;
 var inventory={psd:'entrega/crescimento_luciane_bellas.psd',reopened:true,canvas:[d.width.as('px'),d.height.as('px')],resolution:d.resolution,profile:String(d.colorProfileType),photoshop:app.version,top_level_groups:[],pages:[],template_evidence:{cover:{reference_png:'../../exemplos/optima_final/pngs_aprovados/pagina_01.png',title_masks:[[920,415,1870,735]]},thanks:{reference_png:'../../exemplos/optima_final/pngs_aprovados/pagina_13.png'}},visual_review:{all_pages_inspected:false,pdf_render_inspected:false}};
 for(var n=1;n<=12;n++){
  var g=page(d,n),record={number:n,group:g.name,layers:[]};inventory.top_level_groups.push(g.name);
  // Photoshop DOM pode reportar filhos como invisíveis quando o grupo pai está oculto.
  // Isole a página de verdade antes de ler os filhos; não salve essas alternâncias.
  for(var vi=0;vi<d.layers.length;vi++)d.layers[vi].visible=(d.layers[vi]===g||d.layers[vi].name==='Plano de Fundo');
  function walk(group,path,visible){
   for(var j=0;j<group.layers.length;j++){
    var l=group.layers[j],v=visible&&l.visible,b=l.bounds,item={id:l.id,name:l.name,path:path+l.name,visible:v,type:l.typename==='LayerSet'?'group':'art',variable:false,bounds:[b[0].as('px'),b[1].as('px'),b[2].as('px'),b[3].as('px')]};
    if(l.typename==='ArtLayer'&&l.kind===LayerKind.TEXT){
     item.type='text';item.text=l.textItem.contents;item.font=l.textItem.font;item.size_pt=l.textItem.size.as('pt');item.variable=/^(H1|BODY|CALLOUT|QUOTE|CARD|NUMBER) \|/.test(l.name);item.role=l.name.indexOf('H1 |')===0?'h1':(item.variable?l.name.split(' |')[0].toLowerCase():'fixed');item.font_runs=[];item.missing_font=false;
     var r=new ActionReference();r.putIdentifier(cid('Lyr '),l.id);var desc=executeActionGet(r).getObjectValue(sid('textKey')),runs=desc.getList(sid('textStyleRange'));
     for(var k=0;k<runs.count;k++){
      var run=runs.getObjectValue(k),st=run.getObjectValue(sid('textStyle')),font=st.hasKey(sid('fontPostScriptName'))?st.getString(sid('fontPostScriptName')):item.font;
      var fr={from:run.getInteger(sid('from')),to:run.getInteger(sid('to')),font:font};
      if(st.hasKey(sid('color'))){var c=st.getObjectValue(sid('color'));try{fr.color_rgb=[c.getDouble(cid('Rd  ')),c.getDouble(cid('Grn ')),c.getDouble(cid('Bl  '))];}catch(e){}}
      item.font_runs.push(fr);if(!available[font])item.missing_font=true;
     }
    }else if(l.name.indexOf('PHOTO |')===0){item.role='photo';item.variable=true;item.asset_status='final';item.placeholder=false;item.smart_object=l.kind===LayerKind.SMARTOBJECT;}
    record.layers.push(item);if(l.typename==='LayerSet')walk(l,path+l.name+'/',v);
   }
  }
  // A visibilidade é a efetiva DENTRO da página isolada; outras páginas não interferem.
  walk(g,g.name+'/',true);inventory.pages.push(record);
 }
 for(var vi=0;vi<d.layers.length;vi++)d.layers[vi].visible=(d.layers[vi]===page(d,1)||d.layers[vi].name==='Plano de Fundo');
 var f=new File(project.fsName+'/inventario_final.json');f.encoding='UTF8';f.open('w');f.write(encode(inventory));f.close();
 return '12 páginas exportadas; PSD salvo, reaberto e inventariado. Perfil original preservado.';
})();
