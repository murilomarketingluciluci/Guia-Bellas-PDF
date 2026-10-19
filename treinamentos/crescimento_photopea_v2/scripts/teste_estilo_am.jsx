try{
var l=app.activeDocument.layerSets[0].artLayers.getByName('p02-titulo');app.activeDocument.activeLayer=l;
var s=stringIDToTypeID,c=charIDToTypeID,ref=new ActionReference();ref.putEnumerated(c('Lyr '),c('Ordn'),c('Trgt'));
var tx=executeActionGet(ref).getObjectValue(s('textKey'));var value=tx.getString(s('textKey'));app.echoToOE('VALUE_LENGTH:'+value.length);
var list=new ActionList();for(var i=0;i<2;i++){
var range=new ActionDescriptor();range.putInteger(c('From'),i===0?0:11);range.putInteger(c('T   '),i===0?11:value.length);
var sty=tx.getList(s('textStyleRange')).getObjectValue(0).getObjectValue(s('textStyle'));
if(i===1){sty.putString(s('fontPostScriptName'),'Gotham-Bold');sty.putString(s('fontName'),'Gotham');sty.putString(s('fontStyleName'),'Bold');var col=new ActionDescriptor();col.putDouble(c('Rd  '),251);col.putDouble(c('Grn '),169);col.putDouble(c('Bl  '),195);sty.putObject(c('Clr '),c('RGBC'),col);}
range.putObject(s('textStyle'),s('textStyle'),sty);list.putObject(c('Txtt'),range);
}
var out=new ActionDescriptor(),target=new ActionReference();target.putEnumerated(c('TxLr'),c('Ordn'),c('Trgt'));out.putReference(c('null'),target);var content=new ActionDescriptor();content.putString(c('Txt '),value);content.putList(c('Txtt'),list);out.putObject(c('T   '),c('TxLr'),content);executeAction(c('setd'),out,DialogModes.NO);app.echoToOE('SET_STYLE_OK');
}catch(e){app.echoToOE('ERROR:'+e.message+' '+e);}
