function rgb(hex){var c=new SolidColor();c.rgb.hexValue=hex.replace('#','');return c;}
function bounds(l){var b=l.bounds;return [b[0].value,b[1].value,b[2].value,b[3].value];}
function place(l,x,y){var b=bounds(l);l.translate(x-b[0],y-b[1]);}
function rect(parent,name,x,y,w,h,hex,opacity){
 var d=app.activeDocument,l=d.artLayers.add();l.name=name;
 d.selection.select([[x,y],[x+w,y],[x+w,y+h],[x,y+h]]);d.selection.fill(rgb(hex));d.selection.deselect();
 l.opacity=opacity;if(parent)l.move(parent,ElementPlacement.INSIDE);return l;
}
function text(parent,spec){
 var d=app.activeDocument,l=d.artLayers.add();l.kind=LayerKind.TEXT;l.name=spec.name;var t=l.textItem;
 t.contents=spec.text.split('\\n').join(String.fromCharCode(13));t.font=spec.font||'Gotham-Book';t.size=spec.size;t.position=[0,spec.size];t.color=rgb(spec.color||'#FFFFFF');
 if(spec.leading){t.useAutoLeading=false;t.leading=spec.leading;}
 if(spec.tracking!==undefined)t.tracking=spec.tracking;
 if(spec.runs&&spec.runs.length){
  var a=JSON.parse(t.totalTextStyle),base=a.Style.styles[0],runs=[],styles=[],cursor=0;
  function segment(length,font,color){if(length<=0)return;var z=JSON.parse(JSON.stringify(base));var idx=-1;for(var k=0;k<a.fontSet.length;k++)if(a.fontSet[k].Name===font)idx=k;if(idx<0){idx=a.fontSet.length;a.fontSet.push({Name:font,Script:0,FontType:1,Synthetic:0});}z.Font=idx;var q=rgb(color);z.FillColor={Type:1,Values:[1,q.rgb.red/255,q.rgb.green/255,q.rgb.blue/255]};runs.push(length);styles.push(z);}
  for(var i=0;i<spec.runs.length;i++){var v=spec.runs[i];segment(v.start-cursor,spec.font||'Gotham-Book',spec.color||'#FFFFFF');segment(v.length,v.font||spec.font||'Gotham-Bold',v.color||spec.color||'#FFFFFF');cursor=v.start+v.length;}
  segment(t.contents.length+1-cursor,spec.font||'Gotham-Book',spec.color||'#FFFFFF');a.Style={runs:runs,styles:styles};t.totalTextStyle=JSON.stringify(a);
 }
 if(parent)l.move(parent,ElementPlacement.INSIDE);place(l,spec.x,spec.y);return l;
}
function group(parent,name){var g=app.activeDocument.layerSets.add();g.name=name;if(parent)g.move(parent,ElementPlacement.INSIDE);return g;}
function styleRanges(l,spec){
 if(!spec.runs||!spec.runs.length)return;
 app.activeDocument.activeLayer=l;var s=stringIDToTypeID,c=charIDToTypeID,ref=new ActionReference();ref.putEnumerated(c('Lyr '),c('Ordn'),c('Trgt'));
 var tx=executeActionGet(ref).getObjectValue(s('textKey')),value=tx.getString(s('textKey')),segments=[],pos=0;
 for(var i=0;i<spec.runs.length;i++){var run=spec.runs[i];if(run.start>pos)segments.push({start:pos,end:run.start,font:spec.font,color:spec.color});segments.push({start:run.start,end:run.start+run.length,font:run.font,color:run.color});pos=run.start+run.length;}
 if(pos<value.length)segments.push({start:pos,end:value.length,font:spec.font,color:spec.color});
 var list=new ActionList();for(var i=0;i<segments.length;i++){
  var v=segments[i],r=new ActionDescriptor();r.putInteger(c('From'),v.start);r.putInteger(c('T   '),v.end);
  var st=tx.getList(s('textStyleRange')).getObjectValue(0).getObjectValue(s('textStyle'));
  st.putString(s('fontPostScriptName'),v.font);st.putString(s('fontName'),'Gotham');st.putString(s('fontStyleName'),v.font.replace('Gotham-',''));
  var col=new ActionDescriptor(),co=rgb(v.color);col.putDouble(c('Rd  '),co.rgb.red);col.putDouble(c('Grn '),co.rgb.green);col.putDouble(c('Bl  '),co.rgb.blue);st.putObject(c('Clr '),c('RGBC'),col);r.putObject(s('textStyle'),s('textStyle'),st);list.putObject(c('Txtt'),r);
 }
 var d=new ActionDescriptor(),target=new ActionReference();target.putEnumerated(c('TxLr'),c('Ordn'),c('Trgt'));d.putReference(c('null'),target);var content=new ActionDescriptor();content.putString(c('Txt '),value);content.putList(c('Txtt'),list);d.putObject(c('T   '),c('TxLr'),content);executeAction(c('setd'),d,DialogModes.NO);
}

try{var g=app.activeDocument.layerSets.getByName("02 - Preparação");rect(g,"p02-01-filete",1015,255,3,100,"#FBA9C3",100);rect(g,"p02-02-filete",1015,395,3,100,"#FBA9C3",100);rect(g,"p02-03-filete",1015,535,3,100,"#FBA9C3",100);rect(g,"p02-04-filete",1015,675,3,100,"#FBA9C3",100);var measured=[];var spec={"name": "p02-titulo", "text": "Todo mundo\nquer crescer", "x": 140, "y": 290, "size": 72, "font": "Gotham-Book", "color": "#FFFFFF", "width": 620, "height": 190, "leading": 82, "runs": [{"start": 11, "length": 12, "font": "Gotham-Bold", "color": "#FBA9C3"}]};var l=text(g,spec);measured.push({name:l.name,text:l.textItem.contents,bounds:bounds(l),font:l.textItem.font});var spec={"name": "p02-premissa", "text": "Mas crescimento\nexige preparação", "x": 145, "y": 505, "size": 40, "font": "Gotham-Book", "color": "#FFFFFF", "width": 590, "height": 115, "leading": 48};var l=text(g,spec);measured.push({name:l.name,text:l.textItem.contents,bounds:bounds(l),font:l.textItem.font});var spec={"name": "p02-01-numero", "text": "01", "x": 920, "y": 265, "size": 36, "font": "Gotham-Light", "color": "#FBA9C3", "width": 70, "height": 55, "leading": 41.76};var l=text(g,spec);measured.push({name:l.name,text:l.textItem.contents,bounds:bounds(l),font:l.textItem.font});var spec={"name": "p02-01", "text": "Estar alicerçado", "x": 1050, "y": 263, "size": 43, "font": "Gotham-Book", "color": "#FFFFFF", "width": 690, "height": 110, "leading": 51};var l=text(g,spec);measured.push({name:l.name,text:l.textItem.contents,bounds:bounds(l),font:l.textItem.font});var spec={"name": "p02-02-numero", "text": "02", "x": 920, "y": 405, "size": 36, "font": "Gotham-Light", "color": "#FBA9C3", "width": 70, "height": 55, "leading": 41.76};var l=text(g,spec);measured.push({name:l.name,text:l.textItem.contents,bounds:bounds(l),font:l.textItem.font});var spec={"name": "p02-02", "text": "Estar preparado", "x": 1050, "y": 403, "size": 43, "font": "Gotham-Book", "color": "#FFFFFF", "width": 690, "height": 110, "leading": 51};var l=text(g,spec);measured.push({name:l.name,text:l.textItem.contents,bounds:bounds(l),font:l.textItem.font});var spec={"name": "p02-03-numero", "text": "03", "x": 920, "y": 545, "size": 36, "font": "Gotham-Light", "color": "#FBA9C3", "width": 70, "height": 55, "leading": 41.76};var l=text(g,spec);measured.push({name:l.name,text:l.textItem.contents,bounds:bounds(l),font:l.textItem.font});var spec={"name": "p02-03", "text": "Estar disposto\na aprender", "x": 1050, "y": 543, "size": 43, "font": "Gotham-Book", "color": "#FFFFFF", "width": 690, "height": 110, "leading": 51};var l=text(g,spec);measured.push({name:l.name,text:l.textItem.contents,bounds:bounds(l),font:l.textItem.font});var spec={"name": "p02-04-numero", "text": "04", "x": 920, "y": 685, "size": 36, "font": "Gotham-Light", "color": "#FBA9C3", "width": 70, "height": 55, "leading": 41.76};var l=text(g,spec);measured.push({name:l.name,text:l.textItem.contents,bounds:bounds(l),font:l.textItem.font});var spec={"name": "p02-04", "text": "Estar disposto\na ensinar", "x": 1050, "y": 683, "size": 43, "font": "Gotham-Book", "color": "#FFFFFF", "width": 690, "height": 110, "leading": 51};var l=text(g,spec);measured.push({name:l.name,text:l.textItem.contents,bounds:bounds(l),font:l.textItem.font});app.echoToOE("METRICS:"+JSON.stringify(measured));
}catch(e){app.echoToOE("ERROR:"+e.message+" "+e);}