#target photoshop
/* Entrada: pagina_atual.json. Somente uma página é criada/alterada por execução. */
(function(){
    app.displayDialogs=DialogModes.NO;
    var project=new File($.fileName).parent.parent;
    var repo=project.parent.parent;
    function read(f){f.encoding='UTF8';f.open('r');var v=eval('('+f.read()+')');f.close();return v;}
    function encode(v){
        if(v===null)return 'null';
        if(typeof v==='string')return '"'+v.replace(/\\/g,'\\\\').replace(/"/g,'\\"').replace(/[\x00-\x1f]/g,function(c){return '\\u'+('0000'+c.charCodeAt(0).toString(16)).slice(-4);})+'"';
        if(typeof v==='number'||typeof v==='boolean')return String(v);
        var a=[],k;if(v instanceof Array){for(k=0;k<v.length;k++)a.push(encode(v[k]));return '['+a.join(',')+']';}
        for(k in v)if(v.hasOwnProperty(k))a.push(encode(k)+':'+encode(v[k]));return '{'+a.join(',')+'}';
    }
    function write(path,v){var f=new File(project.fsName+'/'+path);f.encoding='UTF8';f.open('w');f.write(encode(v));f.close();}
    function log(s){var f=new File(project.fsName+'/auditoria/photoshop_execucao.log');f.encoding='UTF8';f.open('a');f.writeln(new Date().toString()+' | '+s);f.close();}
    function openDoc(path){var f=new File(path);for(var i=0;i<app.documents.length;i++)try{if(app.documents[i].fullName.fsName===f.fsName)return app.documents[i];}catch(e){}return app.open(f);}
    function groupNumber(d,n){for(var i=0;i<d.layerSets.length;i++)if(parseInt(d.layerSets[i].name,10)===n)return d.layerSets[i];return null;}
    function findText(group,match){for(var i=0;i<group.layers.length;i++){var l=group.layers[i];if(l.typename==='LayerSet'){var r=findText(l,match);if(r)return r;}else if(l.kind===LayerKind.TEXT&&match.test(l.textItem.contents))return l;}return null;}
    function color(h){var c=new SolidColor();c.rgb.hexValue=h;return c;}
    function px(v){return UnitValue(v,'px');}
    function sid(v){return stringIDToTypeID(v);}function cid(v){return charIDToTypeID(v);}
    function textDesc(l){var r=new ActionReference();r.putIdentifier(cid('Lyr '),l.id);return executeActionGet(r).getObjectValue(sid('textKey'));}
    function clone(d){var x=new ActionDescriptor();x.fromStream(d.toStream());return x;}
    function styleRuns(l,emphasis){
        if(!emphasis)return;
        var A=textDesc(l),txt=l.textItem.contents,needle=emphasis.text.replace(/\n/g,'\r'),start=txt.indexOf(needle);
        if(start<0)throw Error('Destaque não localizado: '+needle);
        var base=A.getList(sid('textStyleRange')).getObjectValue(0).getObjectValue(sid('textStyle'));
        var bold=clone(base);bold.putString(sid('fontPostScriptName'),emphasis.font||'Gotham-Bold');
        bold.putString(sid('fontName'),'Gotham');bold.putString(sid('fontStyleName'),(emphasis.font||'Gotham-Bold').replace('Gotham-',''));
        if(emphasis.color){var c=color(emphasis.color),cd=new ActionDescriptor();cd.putDouble(cid('Rd  '),c.rgb.red);cd.putDouble(cid('Grn '),c.rgb.green);cd.putDouble(cid('Bl  '),c.rgb.blue);bold.putObject(sid('color'),sid('RGBColor'),cd);}
        var list=new ActionList();
        function run(a,b,st){if(b<=a)return;var d=new ActionDescriptor();d.putInteger(sid('from'),a);d.putInteger(sid('to'),b);d.putObject(sid('textStyle'),sid('textStyle'),st);list.putObject(sid('textStyleRange'),d);}
        run(0,start,base);run(start,start+needle.length,bold);run(start+needle.length,txt.length+1,base);
        A.putList(sid('textStyleRange'),list);
        var set=new ActionDescriptor(),r=new ActionReference();r.putIdentifier(cid('Lyr '),l.id);set.putReference(cid('null'),r);set.putObject(cid('T   '),cid('TxLr'),A);executeAction(cid('setd'),set,DialogModes.NO);
    }
    var job=read(new File(project.fsName+'/scripts/pagina_atual.json'));
    var manifest=read(new File(project.fsName+'/manifesto_final.json'));
    var approved=openDoc(repo.fsName+'/exemplos/optima_final/optima_apn_bellas_final.psd');
    var mold=openDoc(repo.fsName+'/referencias/molde_bellas_aprovado_capa_temas_agradecimento.psd');
    var dest=new File(project.fsName+'/entrega/crescimento_luciane_bellas.psd');
    var d;
    if(job.init){
        if(dest.exists)throw Error('Inicialização recusada: PSD de trabalho já existe.');
        for(var td=app.documents.length-1;td>=0;td--)if(app.documents[td].name==='Bellas | Crescimento | Luciane')app.documents[td].close(SaveOptions.DONOTSAVECHANGES);
        app.activeDocument=mold;
        d=mold.duplicate('Bellas | Crescimento | Luciane',false);app.activeDocument=d;
        for(var z=d.layerSets.length-1;z>=0;z--)d.layerSets[z].remove();
        app.activeDocument=approved;
        var first=groupNumber(approved,1).duplicate(d,ElementPlacement.PLACEATBEGINNING);app.activeDocument=d;first.name='01 Capa';
        app.activeDocument=approved;
        var last=groupNumber(approved,13).duplicate(d,ElementPlacement.PLACEATBEGINNING);app.activeDocument=d;last.name='12 Agradecimento';
        // Inventário anterior à primeira alteração de conteúdo.
        write('auditoria/estado_inicial.json',{source_template:'../../referencias/molde_v1_0_base.psd',approved:'../../exemplos/optima_final/optima_apn_bellas_final.psd',canvas:[d.width.as('px'),d.height.as('px')],resolution:d.resolution,profile:String(d.colorProfileType),cover_group:first.name,thanks_group:last.name});
        app.activeDocument=d;
        var title=findText(first,/Desodorante/);if(!title)throw Error('Título aprovado da capa não encontrado.');
        title.textItem.contents='Crescimento';title.name='H1 | Crescimento';styleRuns(title,{text:'Crescimento',font:'Gotham-Book',color:'FFFFFF'});
        var th=findText(last,/obrigada/i);if(!th)throw Error('H1 agradecimento ausente.');th.name='H1 | Agradecimento aprovado';
    } else {if(!dest.exists)throw Error('Inicialize antes.');d=openDoc(dest.fsName);app.activeDocument=d;}
    if(job.migrate){
        var previous=d,previousOptions=new PhotoshopSaveOptions();previousOptions.layers=true;
        previous.saveAs(new File(project.fsName+'/auditoria/antes_molde_consolidado.psd'),previousOptions,true,Extension.LOWERCASE);
        app.activeDocument=mold;d=mold.duplicate('Bellas Crescimento | molde consolidado',false);app.activeDocument=d;
        for(var rm=d.layerSets.length-1;rm>=0;rm--)d.layerSets[rm].remove();
        for(var cp=previous.layerSets.length-1;cp>=0;cp--){app.activeDocument=previous;previous.layerSets[cp].duplicate(d,ElementPlacement.PLACEATBEGINNING);}
        app.activeDocument=previous;previous.close(SaveOptions.DONOTSAVECHANGES);app.activeDocument=d;
        d.saveAs(dest,previousOptions,false,Extension.LOWERCASE);log('Migração para cópia do molde reutilizável consolidado; páginas 01/02/12 preservadas.');
    }
    var n=job.page,s=manifest.slides[n-1],g=groupNumber(d,n);
    if(n!==1&&n!==12){
        if(g&&!job.replace)throw Error('Página já existe; altere incrementalmente com replace autorizado no job.');
        if(g){
            var snap=new File(project.fsName+'/auditoria/antes_pagina_'+('0'+n).slice(-2)+'.psd');
            var saveopts=new PhotoshopSaveOptions();saveopts.layers=true;d.saveAs(snap,saveopts,true,Extension.LOWERCASE);
            g.remove();
        }
        var theme=mold.layerSets.getByName(s.theme==='claro'?'TEMA CLARO VAZIO - DUPLICAR':'TEMA ESCURO VAZIO - DUPLICAR');
        app.activeDocument=mold;
        g=theme.duplicate(d,ElementPlacement.PLACEATBEGINNING);app.activeDocument=d;g.name=('0'+n).slice(-2)+' '+s.name;g.visible=true;
        var base=null,chrome=null;
        for(var a=0;a<g.artLayers.length;a++){var lay=g.artLayers[a];if(/^FUNDO|^BG/.test(lay.name))base=lay;if(/^Camada [12]/.test(lay.name))chrome=lay;}
        if(!base||!chrome)throw Error('Molde sem fundo ou acabamento');
        var content=g.layerSets.add();content.name='CONTENT';var cards={};
        function rect(parent,name,x,y,w,h,hex){
            d.activeLayer=parent;
            var desc=new ActionDescriptor(),r=new ActionReference();r.putClass(sid('contentLayer'));desc.putReference(cid('null'),r);
            var use=new ActionDescriptor(),fill=new ActionDescriptor(),rgb=new ActionDescriptor(),c=color(hex);
            rgb.putDouble(cid('Rd  '),c.rgb.red);rgb.putDouble(cid('Grn '),c.rgb.green);rgb.putDouble(cid('Bl  '),c.rgb.blue);fill.putObject(sid('color'),sid('RGBColor'),rgb);
            use.putObject(sid('type'),sid('solidColorLayer'),fill);
            var box=new ActionDescriptor();box.putUnitDouble(sid('top'),sid('pixelsUnit'),y);box.putUnitDouble(sid('left'),sid('pixelsUnit'),x);box.putUnitDouble(sid('bottom'),sid('pixelsUnit'),y+h);box.putUnitDouble(sid('right'),sid('pixelsUnit'),x+w);
            use.putObject(sid('shape'),sid('rectangle'),box);desc.putObject(sid('using'),sid('contentLayer'),use);executeAction(sid('make'),desc,DialogModes.NO);
            var layer=d.activeLayer;layer.name=name;if(layer.parent!==parent)layer.move(parent,ElementPlacement.INSIDE);return layer;
        }
        function point(parent,el,box){
            var l=parent.artLayers.add();l.kind=LayerKind.TEXT;l.name=el.role.toUpperCase()+' | '+el.text.replace(/\n/g,' ').substr(0,80);
            var t=l.textItem;t.kind=TextType.POINTTEXT;t.font=el.font;t.size=UnitValue(el.size_pt,'pt');t.color=color(el.color);t.tracking=el.tracking;t.justification=Justification.LEFT;
            t.useAutoLeading=false;t.leading=UnitValue(el.leading_pt,'pt');t.position=[px(0),px(el.size_pt)];
            // Meça cada linha com a fonte real no Photoshop. Não reduza o corpo para encaixar.
            var paragraphs=el.text.replace(/\r/g,'\n').split('\n'),lines=[];
            for(var p=0;p<paragraphs.length;p++){
                var words=paragraphs[p].split(' '),line='';
                for(var w=0;w<words.length;w++){
                    var test=line?line+' '+words[w]:words[w];t.contents=test;
                    var width=l.bounds[2].as('px')-l.bounds[0].as('px');
                    if(width>box[2]&&line){lines.push(line);line=words[w];}else line=test;
                }
                lines.push(line);
            }
            t.contents=lines.join('\r');styleRuns(l,el.emphasis);
            var b=l.bounds,L=b[0].as('px'),T=b[1].as('px'),W=b[2].as('px')-L,H=b[3].as('px')-T;
            if(W>box[2]+3||H>box[3]+3)throw Error('Texto não cabe; página '+n+' '+el.text+' | '+W+'x'+H+' > '+box[2]+'x'+box[3]);
            var xpos=box[0]+(el.align==='center'?(box[2]-W)/2:0);l.translate(px(xpos-L),px(box[1]-T));return l;
        }
        function photo(el){
            d.activeLayer=base;var desc=new ActionDescriptor();desc.putPath(cid('null'),new File(project.fsName+'/'+el.asset));desc.putEnumerated(cid('FTcs'),cid('QCSt'),cid('Qcsa'));executeAction(cid('Plc '),desc,DialogModes.NO);
            var l=d.activeLayer;l.name='PHOTO | '+el.asset;var q=el.box_px,b=l.bounds,iw=b[2].as('px')-b[0].as('px'),ih=b[3].as('px')-b[1].as('px'),scale=Math.max(q[2]/iw,q[3]/ih)*100;
            l.resize(scale,scale,AnchorPosition.MIDDLECENTER);b=l.bounds;var nw=b[2].as('px')-b[0].as('px'),nh=b[3].as('px')-b[1].as('px');l.translate(px(q[0]+(q[2]-nw)/2-b[0].as('px')),px(q[1]+(q[3]-nh)/2-b[1].as('px')));l.move(base,ElementPlacement.PLACEBEFORE);d.activeLayer=l;
            d.selection.select([[q[0],q[1]],[q[0]+q[2],q[1]],[q[0]+q[2],q[1]+q[3]],[q[0],q[1]+q[3]]]);
            var mk=new ActionDescriptor(),r=new ActionReference();mk.putClass(cid('Nw  '),cid('Chnl'));r.putEnumerated(cid('Chnl'),cid('Chnl'),cid('Msk '));mk.putReference(cid('At  '),r);mk.putEnumerated(cid('Usng'),cid('UsrM'),cid('RvlS'));executeAction(cid('Mk  '),mk,DialogModes.NO);d.selection.deselect();
            return l;
        }
        for(var k=0;k<s.elements.length;k++){
            var el=s.elements[k],b=el.box_px.slice(0),parent=content;
            if(el.role==='photo'){photo(el);continue;}
            if(el.role==='card'){
                parent=content.layerSets.add();parent.name='CARD | '+el.card_id;cards[el.card_id]=parent;
                rect(parent,'Fundo',b[0],b[1],b[2],b[3],el.background);
                if(el.card_title){
                    rect(parent,'Filete',b[0],b[1],5,b[3],'FFFFFF');
                    var num={role:'number',text:el.number,font:'Gotham-Book',size_pt:34,leading_pt:40,tracking:-70,color:'FFFFFF'};
                    point(parent,num,[b[0]+29,b[1]+26,62,55]);
                    b=[b[0]+el.padding[0],b[1]+24,b[2]-el.padding[0]-32,53];
                }else{
                    // Faixas de preparação: número e texto centralizados no eixo óptico.
                    var num={role:'number',text:el.number,font:'Gotham-Book',size_pt:30,leading_pt:36,tracking:-70,color:'FFFFFF'};
                    point(parent,num,[b[0]+28,b[1]+25,60,45]);
                    b=[b[0]+el.padding[0],b[1]+24,b[2]-el.padding[0]-28,b[3]-35];
                }
            }else if(el.card_id){parent=cards[el.card_id];if(!parent)throw Error('Pasta de cartão ausente');}
            if(el.background&&el.role!=='card'){rect(parent,'Faixa de destaque',b[0],b[1],b[2],b[3],el.background);var pd=el.padding||[20,16];b=[b[0]+pd[0],b[1]+pd[1],b[2]-2*pd[0],b[3]-2*pd[1]];}
            point(parent,el,b);
        }
        if(n===10){rect(content,'Divisão entre ideia e relato',1158,470,3,415,'B3718E');}
        if(n===7){rect(content,'Filete de citação',840,449,240,4,'FBA9C3');}
    }
    // Uma página visível por vez; a ordem de camadas é normalizada no encerramento.
    app.activeDocument=d;for(var i=0;i<d.layers.length;i++)d.layers[i].visible=(d.layers[i]===g||d.layers[i].name==='Plano de Fundo');
    var opts=new PhotoshopSaveOptions();opts.layers=true;opts.embedColorProfile=true;
    if(!dest.exists)d.saveAs(dest,opts,false,Extension.LOWERCASE);else d.save();
    var temp=d.duplicate('Bellas exportação '+n,false);app.activeDocument=temp;
    try{var png=new ExportOptionsSaveForWeb();png.format=SaveDocumentType.PNG;png.PNG8=false;png.transparency=false;png.interlaced=false;png.convertToSRGB=true;png.includeProfile=true;temp.exportDocument(new File(project.fsName+'/entrega/provas_png/pagina_'+('0'+n).slice(-2)+'.png'),ExportType.SAVEFORWEB,png);}finally{temp.close(SaveOptions.DONOTSAVECHANGES);app.activeDocument=d;}
    log('Página '+n+' criada, salva e exportada; fonte real medida; perfil não alterado.');
    return 'Página '+n+' pronta para inspeção visual.';
})();
