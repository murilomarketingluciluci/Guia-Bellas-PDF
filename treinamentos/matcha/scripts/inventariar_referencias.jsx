#target photoshop
(function () {
    var root = new File($.fileName).parent.parent.parent.parent;
    var out = new File(root.fsName + '/treinamentos/matcha/leitura/inventario_photoshop.json');
    function encode(v) {
        if(v===null) return 'null';
        if(typeof v==='string') return '"'+v.replace(/\\/g,'\\\\').replace(/"/g,'\\"').replace(/\r/g,'\\r').replace(/\n/g,'\\n').replace(/\t/g,'\\t')+'"';
        if(typeof v==='number' || typeof v==='boolean') return String(v);
        var a=[], k;
        if(v instanceof Array) {for(k=0;k<v.length;k++) a.push(encode(v[k]));return '['+a.join(',')+']';}
        for(k in v) if(v.hasOwnProperty(k)) a.push(encode(k)+':'+encode(v[k]));
        return '{'+a.join(',')+'}';
    }
    var fonts=[];
    for(var f=0;f<app.fonts.length;f++) if(/Gotham/i.test(app.fonts[f].postScriptName)) fonts.push({name:app.fonts[f].name,ps:app.fonts[f].postScriptName});
    var result={photoshop:app.version,fonts:fonts,documents:[]};
    var paths=['exemplos/optima_final/optima_apn_bellas_final.psd','referencias/molde_v1_0_base.psd'];
    for(var p=0;p<paths.length;p++) {
        var target = new File(root.fsName+'/'+paths[p]), d=null;
        for(var n=0;n<app.documents.length;n++) try {if(app.documents[n].fullName.fsName===target.fsName) d=app.documents[n];}catch(e){}
        if(!d) d=app.open(target);
        var record={path:paths[p],width:d.width.as('px'),height:d.height.as('px'),resolution:d.resolution,layers:[]};
        try{record.profile=String(d.colorProfileType);record.profileName=d.colorProfileName;}catch(e){}
        function walk(group,prefix) {
            for(var j=0;j<group.layers.length;j++) {
                var l=group.layers[j], item={name:l.name,id:l.id,path:prefix+l.name,visible:l.visible,type:l.typename};
                try{item.bounds=[l.bounds[0].as('px'),l.bounds[1].as('px'),l.bounds[2].as('px'),l.bounds[3].as('px')];}catch(e){}
                if(l.typename==='ArtLayer' && l.kind===LayerKind.TEXT) {
                    var t=l.textItem;item.text=t.contents;
                    try{item.font=t.font;item.size=t.size.as('pt');item.tracking=t.tracking;item.leading=t.leading.as('pt');item.position=[t.position[0].as('px'),t.position[1].as('px')];item.textKind=String(t.kind);}catch(e){}
                }
                record.layers.push(item);
                if(l.typename==='LayerSet') walk(l,prefix+l.name+'/');
            }
        }
        walk(d,'');result.documents.push(record);
    }
    out.encoding='UTF8';out.open('w');out.write(encode(result));out.close();
    return 'Inventario somente leitura salvo; Gotham: '+fonts.length+' fontes.';
})();
