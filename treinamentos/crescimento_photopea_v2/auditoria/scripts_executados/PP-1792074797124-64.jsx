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

try{var src=app.activeDocument;var dst=app.documents.getByName("Crescimento Photopea V2");src.activeLayer.duplicate(dst,ElementPlacement.PLACEATBEGINNING);src.close(SaveOptions.DONOTSAVECHANGES);app.activeDocument=dst;var l=dst.activeLayer;l.name="B BELLAS - marca d’água";l.translate(1309,-236);l.opacity=5.098039215686274;l.move(dst.layerSets.getByName("02 - Preparação"),ElementPlacement.INSIDE);app.echoToOE("IMPORTED:"+l.name);
}catch(e){app.echoToOE("ERROR:"+e.message+" "+e);}