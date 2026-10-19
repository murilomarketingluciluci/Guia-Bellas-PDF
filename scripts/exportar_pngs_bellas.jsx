#target photoshop
// Execute no Photoshop com o PSD de trabalho ativo. Adapte apenas OUTPUT_FOLDER se desejar.
// A exportacao Save for Web PNG24 foi conferida pixel a pixel contra os PNGs
// aprovados do caso Optima. Nao atribua perfil ao PSD ou a sua duplicata.
app.displayDialogs = DialogModes.NO;
var OUTPUT_FOLDER = null; // null = pasta "provas_png_srgb" ao lado do PSD salvo
var source = app.activeDocument;
if (!source.saved || !source.fullName) throw Error("Salve uma copia do PSD antes da exportacao.");
var target = OUTPUT_FOLDER ? new Folder(OUTPUT_FOLDER) : new Folder(source.fullName.parent.fsName + "/provas_png_srgb");
if (!target.exists && !target.create()) throw Error("Nao foi possivel criar " + target.fsName);
var copy = source.duplicate("Bellas - exportacao temporaria", false);
try {
    app.activeDocument = copy;
    var pages = [];
    for (var i = 0; i < copy.layerSets.length; i++) {
        var group = copy.layerSets[i];
        var match = /^(\d+)\s*[—–-]?\s*/.exec(group.name);
        if (match) {
            var number = parseInt(match[1], 10);
            if (pages[number]) throw Error("Numero de pagina repetido: " + number);
            pages[number] = group;
        }
    }
    var total = pages.length - 1;
    if (total < 1) throw Error("Nenhuma pasta de pagina numerada encontrada.");
    for (var n = 1; n <= total; n++) if (!pages[n]) throw Error("Falta a pasta da pagina " + n);
    var options = new ExportOptionsSaveForWeb();
    options.format = SaveDocumentType.PNG;
    options.PNG8 = false;
    options.transparency = true;
    options.interlaced = false;
    options.convertToSRGB = true;
    options.includeProfile = true;
    for (var pageNumber = 1; pageNumber <= total; pageNumber++) {
        for (var layerNumber = 0; layerNumber < copy.layers.length; layerNumber++) {
            var layer = copy.layers[layerNumber];
            layer.visible = layer === pages[pageNumber] || layer.name === "Plano de Fundo";
        }
        var id = ("0" + pageNumber).slice(-2);
        copy.exportDocument(new File(target.fsName + "/pagina_" + id + ".png"), ExportType.SAVEFORWEB, options);
    }
    "Exportadas " + total + " paginas para " + target.fsName;
} finally {
    copy.close(SaveOptions.DONOTSAVECHANGES);
    app.activeDocument = source;
}
