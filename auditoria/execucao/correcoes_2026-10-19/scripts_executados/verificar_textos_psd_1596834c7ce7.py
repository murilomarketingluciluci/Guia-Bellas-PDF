"""Vínculo entre manifesto e camadas reais; nenhuma inferência de aprovação visual."""
from collections import Counter
import hashlib
import json

from contrato_bellas import FONTS, TEXT_ROLES, TEMP_LABEL, color_hex, normalized


def descendants(group, prefix=(), visible=True):
    for layer in group:
        path = prefix + (layer.name,)
        shown = visible and bool(layer.visible)
        yield layer, "/".join(path), shown
        if layer.is_group():
            yield from descendants(layer, path, shown)


def text_styles(layer):
    """Os offsets do engine PSD usam UTF-16, inclusive o retorno terminal."""
    fonts = layer.resource_dict.get("FontSet", [])
    runs = layer.engine_dict.get("StyleRun", {})
    lengths = runs.get("RunLengthArray", [])
    result, offset = [], 0
    for i, run in enumerate(runs.get("RunArray", [])):
        style = run.get("StyleSheet", {}).get("StyleSheetData", {})
        font_index = style.get("Font")
        font = fonts[int(font_index)].get("Name") if font_index is not None and 0 <= int(font_index) < len(fonts) else None
        font = getattr(font, "value", font)
        if isinstance(font, bytes):
            font = font.decode("utf-8")
        values = style.get("FillColor", {}).get("Values", [])
        color = "".join(f"{round(float(v)*255):02X}" for v in values[1:4]) if len(values) == 4 else None
        size = int(lengths[i]) if i < len(lengths) else 0
        result.append((offset, offset+size, font, color))
        offset += size
    return result


def compare_style(layer, element):
    actual = text_styles(layer)
    text = str(layer.text).replace("\r", "\n").rstrip("\n\x00")
    expected = str(element.get("text", "")).replace("\r", "\n").rstrip("\n\x00")
    if text != expected:
        return ["texto/quebras diferem da camada declarada"]
    offset = 0
    for index, char in enumerate(expected):
        wanted_font, wanted_color = element.get("font"), color_hex(element.get("color"))
        for run in element.get("runs", []):
            if run["start"] <= index < run["end"]:
                wanted_font = run.get("font", wanted_font)
                wanted_color = color_hex(run.get("color", wanted_color))
                break
        width = len(char.encode("utf-16-le")) // 2
        style = next((s for s in actual if s[0] <= offset and offset+width <= s[1]), None)
        if style is None or style[2] != wanted_font or style[3] != wanted_color:
            return [f"fonte/cor real difere do manifesto no caractere {index}"]
        offset += width
    return []


def compare_pages(manifest, groups, fixed_texts=None, legacy=False):
    errors = []
    slides = manifest.get("slides", [])
    if not isinstance(slides, list):
        return ["manifesto: slides inválido para conferência do PSD"]
    if len(slides) != len(groups):
        errors.append(f"contagem: {len(slides)} páginas no manifesto, {len(groups)} no PSD")
    for slide, group in zip(slides, groups):
        if not isinstance(slide, dict):
            continue
        label = f"PSD p{slide.get('number', '?')}"
        if not legacy and slide.get("group") != group.name:
            errors.append(f"{label}: pasta difere de group do manifesto")
        layers = list(descendants(group))
        types = [(l,p,v) for l,p,v in layers if l.kind == "type"]
        used = set()
        for element in slide.get("elements", []):
            if not isinstance(element, dict) or element.get("role") not in TEXT_ROLES:
                continue
            if legacy:
                candidates = [(l,p,v) for l,p,v in types if id(l) not in used and normalized(l.text) == normalized(element.get("text", ""))]
            else:
                candidates = [(l,p,v) for l,p,v in layers if p == element.get("layer")]
            if len(candidates) != 1 or candidates[0][0].kind != "type":
                errors.append(f"{label}: objeto de texto editável único não localizado: {element.get('id', element.get('layer', element.get('role')))}")
                continue
            layer, path, visible = candidates[0]
            used.add(id(layer))
            if not visible:
                errors.append(f"{label}/{path}: conteúdo oculto por camada ou grupo ancestral")
            if normalized(layer.text) != normalized(element.get("text", "")):
                errors.append(f"{label}/{path}: texto difere do manifesto")
            if TEMP_LABEL.search(str(layer.text)):
                errors.append(f"{label}/{path}: rótulo temporário no PSD")
            try:
                styles = text_styles(layer)
                if not styles or any(font not in FONTS for start,end,font,color in styles if end > start):
                    errors.append(f"{label}/{path}: fonte real ausente ou fora da Gotham autorizada")
                if element.get("role") == "body" and any(color != "FFFFFF" for start,end,font,color in styles if end > start):
                    errors.append(f"{label}/{path}: corpo real não está branco")
                if not legacy:
                    errors.extend(f"{label}/{path}: {p}" for p in compare_style(layer, element))
            except (ValueError, KeyError, TypeError, AttributeError, IndexError) as exc:
                errors.append(f"{label}/{path}: estilo não verificável ({type(exc).__name__})")
        if not legacy:
            allowed = Counter((fixed_texts or {}).get(slide.get("fixed"), []))
            for layer,path,visible in types:
                if id(layer) in used:
                    continue
                text = normalized(layer.text)
                if allowed[text] > 0:
                    allowed[text] -= 1
                else:
                    errors.append(f"{label}/{path}: texto não declarado no manifesto nem pertencente à arte fixa")
            if +allowed:
                errors.append(f"{label}: texto fixo do molde está ausente ou alterado")
    return errors


def digest(path):
    with path.open("rb") as handle:
        return hashlib.file_digest(handle, "sha256").hexdigest()


def verify_reopen(psd_path, report_path, pngs, reopened, same_rgb, image_open):
    if report_path is None or reopened is None:
        return ["reabertura: informe --reopen-report e --reopen-png-dir para vincular PSD atual às provas"]
    report = json.loads(report_path.read_text(encoding="utf-8-sig"))
    errors = []
    if not isinstance(report, dict):
        return ["reabertura: relatório deve ser objeto"]
    if report.get("psd_sha256") != digest(psd_path):
        errors.append("reabertura: hash não corresponde ao PSD atual")
    pages = report.get("pages", [])
    if not isinstance(pages, list) or [p.get("number") if isinstance(p, dict) else None for p in pages] != list(range(1,len(pngs)+1)):
        errors.append("reabertura: relatório de páginas deve seguir sequência 1..N")
        pages = []
    expected_names = {p.name for p in pngs}
    if {p.name for p in reopened.glob("*.png")} != expected_names:
        errors.append("reabertura: provas ausentes ou extras")
    for page, png in zip(pages, pngs):
        fresh = reopened / png.name
        if not fresh.is_file() or page.get("sha256") != digest(fresh):
            errors.append(f"reabertura: hash/arquivo inválido em {png.name}")
            continue
        with image_open(fresh) as left, image_open(png) as right:
            if not same_rgb(left,right):
                errors.append(f"reabertura: PSD reexportado diverge da prova {png.name}")
    return errors
