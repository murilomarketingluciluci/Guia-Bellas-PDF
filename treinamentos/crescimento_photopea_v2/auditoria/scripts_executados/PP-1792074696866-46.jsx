function rgb(hex){var c=new SolidColor();c.rgb.hexValue=hex.replace('#','');return c;}
function bounds(l){var b=l.bounds;return [b[0].value,b[1].value,b[2].value,b[3].value];}
function place(l,x,y){var b=bounds(l);l.translate(x-b[0],y-b[1]);}
function rect(parent,name,x,y,w,h,hex,opacity){
 var s=stringIDToTypeID,c=charIDToTypeID,d=new ActionDescriptor(),r=new ActionReference();r.putClass(s('contentLayer'));d.putReference(c('null'),r);
 var u=new ActionDescriptor(),f=new ActionDescriptor(),v=new ActionDescriptor(),color=rgb(hex);
 v.putDouble(c('Rd  '),color.rgb.red);v.putDouble(c('Grn '),color.rgb.green);v.putDouble(c('Bl  '),color.rgb.blue);f.putObject(s('color'),s('RGBColor'),v);u.putObject(s('type'),s('solidColorLayer'),f);
 var b=new ActionDescriptor();b.putUnitDouble(s('top'),s('pixelsUnit'),y);b.putUnitDouble(s('left'),s('pixelsUnit'),x);b.putUnitDouble(s('bottom'),s('pixelsUnit'),y+h);b.putUnitDouble(s('right'),s('pixelsUnit'),x+w);u.putObject(s('shape'),s('rectangle'),b);d.putObject(s('using'),s('contentLayer'),u);executeAction(s('make'),d,DialogModes.NO);
 var l=app.activeDocument.activeLayer;l.name=name;if(opacity!==undefined)l.opacity=opacity;if(parent)l.move(parent,ElementPlacement.INSIDE);return l;
}
function text(parent,spec){
 var d=app.activeDocument,l=d.artLayers.add();l.kind=LayerKind.TEXT;l.name=spec.name;var t=l.textItem;
 t.contents=spec.text.replace(/\n/g,'\r');t.font=spec.font||'Gotham-Book';t.size=spec.size;t.position=[0,spec.size];t.color=rgb(spec.color||'#FFFFFF');
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

try{var src=app.activeDocument;var dst=app.documents.getByName("Crescimento Photopea V2");src.activeLayer.duplicate(dst,ElementPlacement.PLACEATBEGINNING);src.close(SaveOptions.DONOTSAVECHANGES);app.activeDocument=dst;var l=dst.activeLayer;l.name="MARCAS E CABECALHO APROVADOS";l.translate(0,0);l.opacity=100;l.move(dst.layerSets.getByName("02 - Preparação"),ElementPlacement.INSIDE);app.echoToOE("IMPORTED:"+l.name);
}catch(e){app.echoToOE("ERROR:"+e.message+" "+e);}