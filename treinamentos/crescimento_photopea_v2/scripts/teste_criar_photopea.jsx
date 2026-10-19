try{
 var d=app.documents.add(640,360,72,'Teste API Bellas V2');
 var l=d.artLayers.add();l.kind=LayerKind.TEXT;l.name='TEXTO_EDITAVEL_GOTHAM';
 l.textItem.contents='Crescimento';l.textItem.font='Gotham-Book';l.textItem.size=40;
 var c=new SolidColor();c.rgb.hexValue='B3718E';l.textItem.color=c;l.textItem.position=[50,160];
 app.echoToOE(JSON.stringify({name:d.name,font:l.textItem.font,bounds:l.bounds,totalStyle:l.textItem.totalTextStyle}));
 d.saveToOE('png');d.saveToOE('psd');
}catch(e){app.echoToOE('ERROR:'+String(e));}
