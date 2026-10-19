var s=stringIDToTypeID,c=charIDToTypeID;
var d=new ActionDescriptor(),r=new ActionReference();r.putClass(s('contentLayer'));d.putReference(c('null'),r);
var use=new ActionDescriptor(),fill=new ActionDescriptor(),rgb=new ActionDescriptor();
rgb.putDouble(c('Rd  '),179);rgb.putDouble(c('Grn '),113);rgb.putDouble(c('Bl  '),142);fill.putObject(s('color'),s('RGBColor'),rgb);use.putObject(s('type'),s('solidColorLayer'),fill);
var box=new ActionDescriptor();box.putUnitDouble(s('top'),s('pixelsUnit'),400);box.putUnitDouble(s('left'),s('pixelsUnit'),150);box.putUnitDouble(s('bottom'),s('pixelsUnit'),410);box.putUnitDouble(s('right'),s('pixelsUnit'),900);use.putObject(s('shape'),s('rectangle'),box);d.putObject(s('using'),s('contentLayer'),use);executeAction(s('make'),d,DialogModes.NO);
app.echoToOE('SHAPE_CREATED');
