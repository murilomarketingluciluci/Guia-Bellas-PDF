import json
from montar_photopea import P,js,q
m=json.loads((P/'manifest_photopea.json').read_text(encoding='utf-8-sig'))
p=m['pages'][10];p['shapes'][0]['y']=715
print(js('var g=app.activeDocument.layerSets.getByName("11 - Venham ver");place(g.artLayers.getByName("filete-fecho"),250,715);app.echoToOE("FILETE_FIXED");'))
# A real Action Manager adjustment, since ArtLayer.adjustBrightnessContrast is
# undefined in this Photopea build (the earlier call had no pixel effect).
print(js('var g=app.activeDocument.layerSets.getByName("06 - Oposições 09 a 12 e permanência");app.activeDocument.activeLayer=g.artLayers.getByName("FOTO - foto_permanencia_rochas");var d=new ActionDescriptor();d.putInteger(charIDToTypeID("Brgh"),-35);d.putInteger(charIDToTypeID("Cntr"),0);d.putBoolean(stringIDToTypeID("useLegacy"),false);executeAction(stringIDToTypeID("brightnessEvent"),d,DialogModes.NO);app.echoToOE("EXPOSURE_ACTION");'))
(P/'manifest_photopea.json').write_text(json.dumps(m,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(js('var d=app.activeDocument;for(var i=0;i<d.layerSets.length;i++)d.layerSets[i].visible=d.layerSets[i].name.indexOf("01 -")===0;d.saveToOE("psd");',['trabalho/crescimento_photopea_v2.psd']))
