#target photoshop
/*
 * HISTÓRICO DE PLANEJAMENTO - contém placeholders; não produz APN final.
 * Execute via Photoshop.DoJavaScriptFile depois de revisar o manifesto ao lado.
 * A fonte permanece aberta/intacta; o script trabalha em uma duplicata e salva
 * um arquivo novo. As provas ficam em exemplos/planejamento/provas_regeradas.
 */
(function () {
    var script = new File($.fileName);
    var workDir = script.parent;
    var manifestFile = new File(workDir.fsName + "/optima_layout_historico.json");
    var logFile = new File(workDir.fsName + "/optima_planejamento.log");
    function log(s) {
        logFile.open("a");
        logFile.writeln((new Date()).toString() + " | " + s);
        logFile.close();
    }
    function fail(s) { throw new Error(s); }
    function hexColor(hex) {
        var c = new SolidColor();
        c.rgb.hexValue = hex;
        return c;
    }
    function px(n) { return UnitValue(n, "px"); }
    function fileOf(path) {
        path = path.replace(/\\/g, "/");
        return new File(/^(?:[A-Za-z]:|\/)/.test(path) ? path : workDir.fsName + "/" + path);
    }
    function rectLayer(group, name, x, y, w, h, color) {
        var layer = group.artLayers.add();
        layer.name = name;
        var doc = app.activeDocument;
        doc.activeLayer = layer;
        doc.selection.select([[x,y],[x+w,y],[x+w,y+h],[x,y+h]]);
        doc.selection.fill(hexColor(color), ColorBlendMode.NORMAL, 100, false);
        doc.selection.deselect();
        return layer;
    }
    function textLayer(group, name, text, x, y, w, h, size, color, bold) {
        var layer = group.artLayers.add();
        layer.kind = LayerKind.TEXT;
        layer.name = name;
        var t = layer.textItem;
        t.kind = TextType.PARAGRAPHTEXT;
        t.position = [px(x), px(y)];
        t.width = px(w);
        t.height = px(h);
        t.contents = text.replace(/\n/g, "\r");
        t.size = UnitValue(size, "pt");
        t.font = bold ? "Gotham-Bold" : "Gotham-Medium";
        t.color = hexColor(color);
        t.justification = Justification.CENTER;
        try { t.useAutoLeading = false; t.leading = UnitValue(size * 1.18, "pt"); } catch (_) {}
        return layer;
    }
    function getGroup(doc, name) {
        for (var i=0; i<doc.layerSets.length; i++) if (doc.layerSets[i].name === name) return doc.layerSets[i];
        fail("Grupo ausente no molde: " + name);
    }
    function getArt(group, name) {
        for (var i=0; i<group.artLayers.length; i++)
            if (group.artLayers[i].name.indexOf(name) === 0) return group.artLayers[i];
        fail("Camada de acabamento ausente: " + name);
    }
    function addPhoto(doc, group, path, id, x, y, w, h, chromeName) {
        var f = fileOf(path);
        if (!f.exists) fail("Foto ausente: " + path);
        var p = app.open(f);
        var iw = p.width.as("px"), ih = p.height.as("px");
        if (Math.round(iw) !== w || Math.round(ih) !== h)
            fail("Dimensão inesperada da foto " + id + ": " + iw + "x" + ih + " (esperado " + w + "x" + h + ")");
        p.selection.selectAll(); p.selection.copy();
        p.close(SaveOptions.DONOTSAVECHANGES);
        app.activeDocument = doc;
        doc.activeLayer = group;
        doc.paste();
        var layer = doc.activeLayer;
        layer.name = "FOTO " + id + " | substituir imagem";
        // A foto fica abaixo da camada de acabamento já presente no molde.
        var chrome=getArt(group,chromeName);
        layer.move(chrome,ElementPlacement.PLACEAFTER);
        var left = layer.bounds[0].as("px"), top = layer.bounds[1].as("px");
        layer.translate(px(x-left), px(y-top));
        return layer;
    }
    function hidePages(pages) {
        for (var i=0; i<pages.length; i++) pages[i].visible = false;
    }
    function savePng(doc, path) {
        var f=fileOf(path);
        if (f.exists) f.remove();
        var opts = new PNGSaveOptions();
        opts.interlaced = false;
        doc.saveAs(f, opts, true, Extension.LOWERCASE);
    }

    if (!manifestFile.exists) fail("Manifesto ausente: " + manifestFile.fsName);
    manifestFile.encoding = "UTF8";
    manifestFile.open("r");
    var manifest = eval("(" + manifestFile.read() + ")");
    manifestFile.close();
    var output = fileOf(manifest.output_psd), sourceFile=fileOf(manifest.template_path);
    var proofDir = new Folder(workDir.fsName + "/" + manifest.proof_dir);
    if (!sourceFile.exists) fail("Molde ausente: " + sourceFile.fsName);
    if (output.exists) fail("Saída já existe; não sobrescrever: " + output.fsName);
    if (!proofDir.exists && !proofDir.create()) fail("Não foi possível criar pasta de provas");
    if (manifest.pages.length !== 12) fail("O manifesto precisa conter exatamente 12 páginas");
    var oldRuler = app.preferences.rulerUnits, oldType=app.preferences.typeUnits;
    var oldDialogs=app.displayDialogs;
    app.preferences.rulerUnits=Units.PIXELS;
    app.preferences.typeUnits=TypeUnits.POINTS;
    app.displayDialogs=DialogModes.NO;
    var doc = null;
    try {
        log("INÍCIO " + output.fsName);
        // Limpa somente duplicatas sem arquivo geradas por uma tentativa anterior.
        for (var z=app.documents.length-1; z>=0; z--) {
            var stale=app.documents[z];
            if (stale.name.indexOf("treinamento_optima_molde_v1_editavel") === 0) {
                var hasPath=false;
                try { hasPath=stale.fullName.exists; } catch (_) {}
                if (!hasPath) stale.close(SaveOptions.DONOTSAVECHANGES);
            }
        }
        var src = app.open(sourceFile);
        doc = src.duplicate("treinamento_optima_molde_v1_editavel", false);
        app.activeDocument = doc;
        if (doc.width.as("px") !== 1920 || doc.height.as("px") !== 1080)
            fail("Molde deve ter 1920x1080 px");
        var light = getGroup(doc, "molde claro"), dark=getGroup(doc, "molde escuro");
        var cover=getGroup(doc, "CAPA");
        light.visible=false; dark.visible=false; cover.visible=false;
        var pages=[];
        var scale=manifest.scale, colors=manifest.palette;
        for (var i=0; i<manifest.pages.length; i++) {
            var p=manifest.pages[i], isDark=p.theme === "dark";
            var page=(isDark ? dark : light).duplicate();
            page.name = p.id + " — " + p.name;
            page.visible=true;
            if (p.photo) {
                var ph=p.photo, key=p.id;
                addPhoto(doc,page,manifest.photos[key],key,ph[0]*scale,ph[1]*scale,ph[2]*scale,ph[3]*scale,
                    isDark ? "Camada 2" : "Camada 1");
            }
            for (var j=0; j<p.blocks.length; j++) {
                var b=p.blocks[j], kind=b[0], x=b[1]*scale,y=b[2]*scale,w=b[3]*scale,h=b[4]*scale;
                var label=b[5], size=b[6]*scale;
                var fill, fg, bold=(kind==="h1");
                if (kind==="h1") { fill=colors[isDark?"h1_dark":"h1_light"]; fg=isDark?colors.text_dark:colors.white; }
                else if (kind==="body") { fill=colors[isDark?"body_dark":"body_light"]; fg=colors.text_dark; }
                else if (kind==="bullet") { fill=colors[isDark?"bullet_dark":"bullet_light"]; fg=colors.text_dark; }
                else if (kind==="callout") { fill=colors[isDark?"callout_dark":"callout_light"]; fg=isDark?colors.text_dark:colors.white; }
                else if (kind==="card") { fill=colors[isDark?"card_dark":"card_light"]; fg=colors.text_dark; }
                else fail("Tipo de bloco desconhecido: " + kind);
                // Cards têm duas a três linhas; o tamanho do manifesto é um teto.
                if (kind==="card") size=Math.min(size,50);
                rectLayer(page,""+(j+1)+" | " + kind.toUpperCase() + " | fundo",x,y,w,h,fill);
                // Margem interna preserva o texto como camada editável independente.
                var pad=Math.min(24,Math.max(12,Math.round(w*0.035)));
                var textH=(kind==="card") ? Math.min(h-20,260) :
                    Math.min(h-12, Math.max(size*2.65, size*1.3));
                var ty=y+(h-textH)/2;
                textLayer(page,""+(j+1)+" | " + label,label,x+pad,ty,w-2*pad,textH,size,fg,bold);
            }
            pages.push(page);
            page.visible=false;
            log("PÁGINA " + p.id + " criada");
        }
        // Os elementos originais do molde seguem no documento como referência oculta.
        hidePages(pages); pages[0].visible=true;
        var saveOpts=new PhotoshopSaveOptions();
        saveOpts.layers=true; saveOpts.embedColorProfile=true;
        doc.saveAs(output,saveOpts,false,Extension.LOWERCASE);
        log("PSD SALVO " + output.fsName);
        for (var k=0; k<pages.length; k++) {
            hidePages(pages); pages[k].visible=true;
            savePng(doc,proofDir.fsName+"/pagina_"+manifest.pages[k].id+".png");
            log("PROVA " + manifest.pages[k].id + " salva");
        }
        hidePages(pages); pages[0].visible=true;
        doc.save();
        log("CONCLUÍDO");
    } catch(e) {
        log("ERRO " + e.message + " @ linha " + e.line);
        throw e;
    } finally {
        app.preferences.rulerUnits=oldRuler;
        app.preferences.typeUnits=oldType;
        app.displayDialogs=oldDialogs;
    }
})();


