"""Contrato compartilhado de manifestos finais 2.0; não renderiza nem aprova arte."""
from pathlib import Path, PureWindowsPath
import re

ROOT = Path(__file__).resolve().parents[1]
APPROVED = ROOT / "referencias/molde_bellas_aprovado_capa_temas_agradecimento.psd"
FONTS = {"Gotham-Book", "Gotham-Bold", "Gotham-Medium", "Gotham-Light"}
TEXT_ROLES = {"h1", "body", "bullet", "card", "callout", "quote"}
TEMP_LABEL = re.compile(
    r"(?im)^\s*(?:H1|BLOCO(?:\s*\d+)?|ITEM(?:\s*\d+)?|BULLET(?:\s*\d+)?|"
    r"T[ÍI]TULO|TEXTO|FOTO(?:\s*\d+|\s+AQUI)?|PLACEHOLDER|"
    r"(?:\d+\s*[-–—]\s*)?\d+\s*LINHAS)\s*[:/]?\s*$|"
    r"^\s*H1\s*/\s*T[ÍI]TULO\s*$|\bLOREM\s+IPSUM\b|\bINSERIR\s+(?:FOTO|TEXTO)\b"
)


def normalized(text):
    return " ".join(str(text).replace("\r", "\n").split())


def color_hex(value):
    return value.lstrip("#").upper() if isinstance(value, str) and re.fullmatch(r"#?[a-fA-F0-9]{6}", value) else None


def package_path(base, value):
    if not isinstance(value, str) or not value.strip() or Path(value).is_absolute() or PureWindowsPath(value).is_absolute() or re.match(r"^[a-zA-Z]:", value):
        return None
    path = (base / value).resolve()
    return path if path.is_relative_to(ROOT.resolve()) else None


def validate_contract(data, path, requested_stage=None, legacy=False):
    errors = []
    if not isinstance(data, dict):
        return ["manifesto deve ser um objeto JSON"]
    if (requested_stage or data.get("stage", "planejamento")) != "final" or legacy:
        return errors
    if data.get("schema_version") != "2.0":
        errors.append("final novo exige schema_version: 2.0; --legacy é somente diagnóstico histórico")
    if data.get("canvas") != [1920, 1080]:
        errors.append("final novo exige canvas [1920,1080]")
    template = data.get("template")
    if not isinstance(template, dict) or package_path(path.parent, template.get("psd")) != APPROVED.resolve():
        errors.append("template.psd deve apontar para o molde aprovado dentro do pacote")
    sources = {}
    entries = data.get("sources")
    if not isinstance(entries, list) or not entries:
        errors.append("sources: registre id, file, page e text dos trechos de origem")
    else:
        for source in entries:
            if not isinstance(source, dict) or not isinstance(source.get("id"), str) or not source["id"].strip():
                errors.append("sources: objeto com id não vazio esperado")
                continue
            sid = source["id"]
            if sid in sources:
                errors.append(f"sources: id duplicado {sid}")
            sources[sid] = source
            selected = package_path(path.parent, source.get("file"))
            if selected is None or not selected.is_file():
                errors.append(f"sources[{sid}]: file deve existir em caminho relativo dentro do pacote")
            if type(source.get("page")) is not int or source["page"] < 1 or not isinstance(source.get("text"), str) or not source["text"].strip():
                errors.append(f"sources[{sid}]: page positiva e text original obrigatórios")
    slides = data.get("slides")
    if not isinstance(slides, list) or len(slides) < 2:
        return errors + ["final novo exige lista de slides com capa e agradecimento distintos"]
    used, ids, groups = set(), set(), set()
    for index, slide in enumerate(slides, 1):
        if not isinstance(slide, dict):
            continue  # A geometria relata o tipo inválido.
        label = f"slide {index}"
        if type(slide.get("number")) is not int:
            errors.append(label + ": number deve ser inteiro")
        group = slide.get("group")
        match = re.match(r"^(\d+)\b", group) if isinstance(group, str) else None
        if not match or int(match[1]) != index or group in groups:
            errors.append(label + ": group deve ser a pasta numerada única do PSD")
        if isinstance(group, str):
            groups.add(group)
        fixed = "cover" if index == 1 else "thanks" if index == len(slides) else None
        if slide.get("fixed") != fixed:
            errors.append(label + f": fixed deve ser {fixed!r}")
        if fixed and slide.get("theme") != "claro":
            errors.append(label + ": capa e agradecimento aprovados usam tema claro")
        elements = slide.get("elements")
        if not isinstance(elements, list):
            continue
        if fixed == "cover" and (len(elements) != 1 or not isinstance(elements[0], dict) or elements[0].get("role") != "h1"):
            errors.append("slide 1: capa admite somente o H1 do treinamento")
        if fixed == "thanks" and elements != []:
            errors.append(label + ": agradecimento usa elements: [] e mantém a arte fixa")
        layer_paths = set()
        for el in elements:
            if not isinstance(el, dict):
                continue
            if el.get("role") == "photo" and package_path(path.parent, el.get("asset")) is None:
                errors.append(label + ": asset deve permanecer dentro do pacote")
            if el.get("role") not in TEXT_ROLES:
                continue
            eid, layer = el.get("id"), el.get("layer")
            if not isinstance(eid, str) or not eid.strip() or eid in ids:
                errors.append(label + ": id textual não vazio e único obrigatório")
            else:
                ids.add(eid)
            if not isinstance(layer, str) or not layer or "\\" in layer or any(p in {"", ".", ".."} for p in layer.split("/")) or layer in layer_paths:
                errors.append(label + ": layer deve ser caminho único relativo à pasta da página")
            else:
                layer_paths.add(layer)
            refs = el.get("source_ids")
            if not isinstance(refs, list) or not refs or not all(isinstance(v, str) and v in sources for v in refs):
                errors.append(label + ": source_ids deve apontar para trechos de sources")
            else:
                used.update(refs)
            if el.get("font") not in FONTS:
                errors.append(label + ": font deve ser um estilo Gotham autorizado")
            color = color_hex(el.get("color"))
            if color is None or (el.get("role") == "body" and color != "FFFFFF"):
                errors.append(label + ": color HEX obrigatório; body sempre FFFFFF")
            runs = el.get("runs", [])
            if not isinstance(runs, list):
                errors.append(label + ": runs deve ser lista")
                continue
            last = 0
            for run in runs:
                if not isinstance(run, dict):
                    errors.append(label + ": run deve ser objeto")
                    continue
                start, end = run.get("start"), run.get("end")
                if type(start) is not int or type(end) is not int or not (last <= start < end <= len(el.get("text", ""))):
                    errors.append(label + ": intervalos de runs inválidos ou sobrepostos")
                else:
                    last = end
                if run.get("font", el.get("font")) not in FONTS:
                    errors.append(label + ": fonte não autorizada em run")
                rc = color_hex(run.get("color", el.get("color")))
                if rc is None or (el.get("role") == "body" and rc != "FFFFFF"):
                    errors.append(label + ": cor inválida em run")
    omitted = set()
    omissions = data.get("omitted_sources", [])
    if not isinstance(omissions, list):
        errors.append("omitted_sources deve ser lista")
        omissions = []
    for omission in omissions:
        if not isinstance(omission, dict) or not isinstance(omission.get("id"), str) or omission["id"] not in sources or not isinstance(omission.get("reason"), str) or not omission["reason"].strip():
            errors.append("omitted_sources exige id conhecido e reason editorial")
        else:
            omitted.add(omission["id"])
    for sid in sorted(set(sources)-used-omitted):
        errors.append(f"sources[{sid}]: trecho sem destino nem decisão editorial de omissão")
    if used & omitted:
        errors.append("trecho não pode estar usado e omitido simultaneamente")
    return errors
