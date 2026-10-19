#target photoshop
(function(){
var R='C:/Users/Murilo/Documents/Projetos/Bellas/Lives/Guia_Bellas_IA/Criador de PDF Agente/treinamentos/vitae_reverse_tangerina';
var oldDialogs=app.displayDialogs,oldUnits=app.preferences.rulerUnits,d=null;
app.displayDialogs=DialogModes.NO;app.preferences.rulerUnits=Units.PIXELS;
function read(p){var f=new File(p);f.encoding='UTF8';f.open('r');var s=f.read();f.close();return eval('('+s+')');}
function px(x){return UnitValue(x,'px');}function sid(x){return stringIDToTypeID(x);}function cid(x){return charIDToTypeID(x);}
function page(n){for(var i=0;i<d.layerSets.length;i++)if(parseInt(d.layerSets[i].name,10)===n)return d.layerSets[i];throw Error('Pagina ausente: '+n);}
function isolate(g){for(var i=0;i<d.layers.length;i++)d.layers[i].visible=d.layers[i]===g||d.layers[i].name==='Plano de Fundo';}
function bounds(l){var b=l.bounds;return [b[0].as('px'),b[1].as('px'),b[2].as('px'),b[3].as('px')];}
try{
var m=read(R+'/manifesto_com_fotos.json');d=app.open(new File(R+'/producao/vitae_reverse_com_fotos.psd'));
for(var p=0;p<m.slides.length;p++){
var s=m.slides[p],e=null;for(var k=0;k<s.elements.length;k++)if(s.elements[k].role==='photo')e=s.elements[k];if(!e)continue;
var g=page(s.number);isolate(g);var placeholder=null,chrome=null,base=null;
for(var i=0;i<g.layerSets.length;i++)if(g.layerSets[i].name.indexOf('FOTO PLANEJADA')===0)placeholder=g.layerSets[i];
for(var i=0;i<g.artLayers.length;i++){if(/^Camada [12]/.test(g.artLayers[i].name))chrome=g.artLayers[i];if(/^FUNDO|^BG/.test(g.artLayers[i].name))base=g.artLayers[i];}
if(!placeholder||!chrome||!base)throw Error('Estrutura inesperada na pagina '+s.number);
d.activeLayer=base;var desc=new ActionDescriptor();desc.putPath(cid('null'),new File(R+'/'+e.asset));desc.putEnumerated(cid('FTcs'),cid('QCSt'),cid('Qcsa'));executeAction(cid('Plc '),desc,DialogModes.NO);
var photo=d.activeLayer;photo.name='FOTO | '+e.asset;var q=e.box_px,b=bounds(photo),w=b[2]-b[0],h=b[3]-b[1],scale=Math.max(q[2]/w,q[3]/h)*100;photo.resize(scale,scale,AnchorPosition.MIDDLECENTER);b=bounds(photo);w=b[2]-b[0];h=b[3]-b[1];photo.translate(px(q[0]+(q[2]-w)/2-b[0]),px(q[1]+(q[3]-h)/2-b[1]));photo.move(chrome,ElementPlacement.PLACEAFTER);d.activeLayer=photo;
d.selection.select([[q[0],q[1]],[q[0]+q[2],q[1]],[q[0]+q[2],q[1]+q[3]],[q[0],q[1]+q[3]]]);var mk=new ActionDescriptor(),r=new ActionReference();mk.putClass(cid('Nw  '),cid('Chnl'));r.putEnumerated(cid('Chnl'),cid('Chnl'),cid('Msk '));mk.putReference(cid('At  '),r);mk.putEnumerated(cid('Usng'),cid('UsrM'),cid('RvlS'));executeAction(cid('Mk  '),mk,DialogModes.NO);d.selection.deselect();placeholder.remove();d.save();
}
var opts=new ExportOptionsSaveForWeb();opts.format=SaveDocumentType.PNG;opts.PNG8=false;opts.transparency=false;opts.interlaced=false;opts.convertToSRGB=true;opts.includeProfile=true;
for(var n=1;n<=m.slides.length;n++){isolate(page(n));d.exportDocument(new File(R+'/producao/provas/pagina_'+('0'+n).slice(-2)+'.png'),ExportType.SAVEFORWEB,opts);}
isolate(page(1));d.save();d.close(SaveOptions.DONOTSAVECHANGES);return 'Quatro fotos aplicadas em copia; nove provas exportadas.';
}catch(e){if(d)try{d.close(SaveOptions.DONOTSAVECHANGES);}catch(_){}throw e;}finally{app.displayDialogs=oldDialogs;app.preferences.rulerUnits=oldUnits;}
})();
