var d=app.activeDocument;
var l=d.artLayers.add();l.kind=LayerKind.TEXT;l.name='METRICA_GOTHAM';
var t=l.textItem;t.contents='Gotham Crescimento';t.font='Gotham-Book';t.size=60;t.position=[150,300];
app.echoToOE('STYLE:'+t.totalTextStyle);
app.echoToOE('BOUNDS:'+l.bounds);
