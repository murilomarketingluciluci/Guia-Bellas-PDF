"""Verifica artefatos APN; não substitui a inspeção visual/editorial independente.

Uso: python scripts/validar_entrega.py PASTA_PROJETO --manifest manifesto_final.json
     --inventory inventario_final.json --pngs provas --pdf treinamento_final.pdf
Saída JSON sempre preserva lacunas e hashes. Código 0: verificações mecânicas
passaram; 1: falha; 2: argumento/dependência indisponível. Veja VALIDACAO.md.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path, PureWindowsPath


TEMP = re.compile(r"(?:^|[\n\r])\s*(?:H1\b|BLOCO\s*\d*\b|ITEM\s*\d*\b|BULLET\s*\d*\b|PLACEHOLDER\b|FOTO\s*(?:\d+|AQUI)?\s*$|(?:\d+\s*[–-]\s*)?\d+\s*LINHAS\b)|LOREM IPSUM|INSERIR (?:FOTO|TEXTO)", re.I)
PATH_KEYS = {"asset", "psd", "path", "file", "png", "pdf", "reference_png", "source_file", "inventory"}


def sha256(path):
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def read_json(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def normalized(value):
    return " ".join(str(value).replace("\r", "\n").split())


def absolute_path(value):
    return Path(value).is_absolute() or PureWindowsPath(value).is_absolute() or bool(re.match(r"^[a-z]:|^\\\\", value, re.I))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("project", type=Path)
    parser.add_argument("--manifest", default="manifesto_final.json")
    parser.add_argument("--inventory", default="inventario_final.json")
    parser.add_argument("--pngs", default="provas")
    parser.add_argument("--pdf", default="treinamento_final.pdf")
    parser.add_argument("--report", default="validacao_entrega.json")
    args = parser.parse_args()
    try:
        from PIL import Image, ImageChops, ImageDraw
        import pymupdf
    except ImportError as exc:
        print("Dependência indisponível:", exc, file=sys.stderr)
        return 2
    project = args.project.resolve()
    repo = Path(__file__).resolve().parents[3]
    problems, checks, files = [], [], []
    limitations = [
        "Resultado mecânico não comprova aprovação visual: todas as páginas e a renderização do PDF devem ser inspecionadas.",
        "Anatomia, fotografia contínua, áreas seguras de 15%, proporções, contraste, alinhamento óptico e fidelidade editorial exigem revisão independente.",
        "Fonte reportada em inventário exige inventário produzido do PSD reaberto; o JSON isolado não prova a origem.",
    ]

    def check(ok, name, detail=None):
        checks.append({"check": name, "passed": bool(ok), "detail": detail})
        if not ok:
            problems.append(name + (": " + str(detail) if detail else ""))

    def artifact(value, base=project):
        if absolute_path(str(value)):
            raise ValueError("Caminho operacional absoluto proibido: " + str(value))
        result = (base / value).resolve()
        # ../referencias is legitimate within the repository package.
        if not result.is_relative_to(repo):
            raise ValueError("Caminho fora do pacote: " + str(value))
        return result

    def record(path):
        if path.is_file() and path not in files:
            files.append(path)

    try:
        manifest_path, inventory_path, png_folder, pdf_path = [artifact(value) for value in (args.manifest, args.inventory, args.pngs, args.pdf)]
        manifest, inventory = read_json(manifest_path), read_json(inventory_path)
        record(manifest_path)
        record(inventory_path)
        validator = load_module("bellas_manifest", repo / "scripts/validar_manifest.py")
        errors = validator.validate(manifest_path, "final")
        check(not errors, "manifesto final válido", errors or None)

        def walk_paths(node, cursor="manifest", provenance=False):
            if isinstance(node, list):
                for i, child in enumerate(node):
                    walk_paths(child, f"{cursor}[{i}]", provenance)
            elif isinstance(node, dict):
                for key, value in node.items():
                    historical = provenance or key.lower() in {"provenance", "proveniencia", "historical", "historico"}
                    if not historical and key in PATH_KEYS and isinstance(value, str):
                        path = artifact(value, manifest_path.parent)
                        check(path.is_file(), f"arquivo relativo {cursor}.{key}", value)
                        record(path)
                    if key == "placeholder":
                        check(False, "campo placeholder proibido", cursor)
                    walk_paths(value, f"{cursor}.{key}", historical)
        walk_paths(manifest)
        slides = manifest.get("slides", [])
        pages = inventory.get("pages", [])
        check(isinstance(pages, list) and len(pages) == len(slides) and len(pages) > 1, "contagem manifesto/inventário", [len(slides), len(pages)])
        check(inventory.get("canvas") == manifest.get("canvas") == [1920, 1080], "canvas do PSD e manifesto 1920×1080")
        check(inventory.get("reopened") is True, "inventário do PSD salvo e reaberto")
        psd = artifact(inventory.get("psd", "arquivo_ausente.psd"))
        check(psd.is_file(), "PSD final presente", inventory.get("psd"))
        record(psd)
        if psd.is_file():
            check(inventory.get("psd_sha256") == sha256(psd), "hash do PSD coincide com inventário reaberto")
        top_groups = inventory.get("top_level_groups")
        if top_groups is not None:
            check(top_groups == [page.get("group") for page in pages], "todos os grupos de topo correspondem às páginas")
        else:
            check(False, "inventário lista todos os grupos de topo")

        for index, (slide, page) in enumerate(zip(slides, pages), 1):
            prefix = f"página {index:02}"
            group = page.get("group", "")
            number = re.match(r"^(\d+)(?:\D|$)", group)
            check(page.get("number") == index and number and int(number.group(1)) == index, prefix + " grupo numerado", group)
            layers = page.get("layers", [])
            visible = [layer for layer in layers if layer.get("visible") is True]
            # Role and effective visibility must be explicit. Hidden source/template layers may retain old text.
            variable = [layer for layer in visible if layer.get("variable") is True]
            text_layers = [layer for layer in variable if layer.get("type") == "text"]
            h1 = [layer for layer in text_layers if layer.get("role") == "h1"]
            check(len(h1) == 1, prefix + " H1 único e editável", len(h1))
            check(bool(text_layers), prefix + " texto variável editável presente")
            for layer in visible:
                label = prefix + "/" + layer.get("name", "sem nome")
                check(not TEMP.search(str(layer.get("text", ""))), label + " sem texto placeholder")
                check(layer.get("placeholder") is not True, label + " sem foto/camada placeholder")
                if layer.get("role") == "photo":
                    check(layer.get("asset_status") == "final", label + " fotografia final")
                if layer not in text_layers:
                    continue
                runs = layer.get("font_runs") or [{"font": layer.get("font", "")}]
                fonts = [run.get("font", "") if isinstance(run, dict) else str(run) for run in runs]
                check(bool(fonts) and all("gotham" in font.casefold() for font in fonts), label + " Gotham em todos os intervalos", fonts)
                check(layer.get("missing_font") is not True, label + " fonte sem substituição")
                bounds = layer.get("bounds")
                check(isinstance(bounds, list) and len(bounds) == 4 and all(isinstance(v, (float, int)) for v in bounds) and bounds[0] >= 0 and bounds[1] >= 0 and bounds[2] <= 1920 and bounds[3] <= 1080 and bounds[2] > bounds[0] and bounds[3] > bounds[1], label + " bounds dentro do canvas", bounds)
            actual_text = [normalized(layer.get("text", "")) for layer in text_layers]
            for el in slide.get("elements", []):
                if el.get("role") in validator.TEXT_ROLES:
                    check(normalized(el.get("text", "")) in actual_text, prefix + " texto do manifesto em camada editável", el.get("text"))
            if index == 1:
                check(len(variable) == 1 and len(h1) == 1, "capa apenas título variável")
                check(not any(layer.get("role") == "photo" for layer in variable), "capa sem foto nova")

        assembler = load_module("bellas_assemble", repo / "scripts/montar_pdf_dos_pngs.py")
        pngs = assembler.numbered_pngs(png_folder)
        check(len(pngs) == len(slides), "contagem PNGs/manifesto", [len(pngs), len(slides)])
        for path in pngs:
            record(path)
            with Image.open(path) as image:
                check(image.size == (1920, 1080), path.name + " 1920×1080/16:9", list(image.size))
                check(image.convert("RGBA").getchannel("A").getextrema() == (255, 255), path.name + " opaco")
        record(pdf_path)
        with pymupdf.open(pdf_path) as pdf:
            check(len(pdf) == len(pngs) == len(slides), "contagem PDF/PNGs/manifesto", [len(pdf), len(pngs), len(slides)])
            for i, (page, png) in enumerate(zip(pdf, pngs), 1):
                check(abs(page.rect.width / page.rect.height - 16 / 9) < .0001, f"PDF página {i} 16:9")
                embedded = page.get_images(full=True)
                check(len(embedded) == 1, f"PDF página {i} imagem única sem reamostragem")
                if len(embedded) != 1:
                    continue
                pix = pymupdf.Pixmap(pdf, embedded[0][0])
                check(pix.colorspace is not None and pix.colorspace.n == 3 and pix.n in (3, 4), f"PDF página {i} espaço RGB")
                if pix.colorspace is None or pix.colorspace.n != 3 or pix.n not in (3, 4):
                    continue
                actual = Image.frombytes("RGB" if pix.n == 3 else "RGBA", (pix.width, pix.height), pix.samples).convert("RGB")
                with Image.open(png) as image:
                    wanted = image.convert("RGB")
                check(actual.size == wanted.size and ImageChops.difference(actual, wanted).getbbox() is None, f"PDF página {i} RGB exato ao PNG")
                image_rects = page.get_image_rects(embedded[0][0])
                check(len(image_rects) == 1 and all(abs(a-b) < .01 for a,b in zip(image_rects[0], page.rect)), f"PDF página {i} imagem ocupa a página")

        evidence = inventory.get("template_evidence", {})
        for name, image_path in (("cover", pngs[0]), ("thanks", pngs[-1])):
            item = evidence.get(name, {})
            reference = item.get("reference_png")
            check(bool(reference), name + " referência de comparação disponível")
            if not reference:
                continue
            reference_path = artifact(reference)
            record(reference_path)
            with Image.open(reference_path) as image:
                baseline = image.convert("RGB")
            with Image.open(image_path) as image:
                produced = image.convert("RGB")
            check(baseline.size == produced.size, name + " dimensões da referência")
            if baseline.size != produced.size:
                continue
            diff = ImageChops.difference(baseline, produced)
            if name == "cover":
                masks = item.get("title_masks", [])
                mask_image = Image.new("L", produced.size, 0)
                drawer = ImageDraw.Draw(mask_image)
                valid_masks = bool(masks)
                for box in masks:
                    valid = isinstance(box, list) and len(box) == 4 and all(isinstance(v, int) for v in box) and 0 <= box[0] < box[2] <= 1920 and 0 <= box[1] < box[3] <= 1080
                    valid_masks = valid_masks and valid
                    if valid:
                        drawer.rectangle(box, fill=255)
                area = sum(mask_image.histogram()[1:]) / (1920 * 1080)
                check(valid_masks and area <= .4, "capa máscara limitada aos títulos", {"masks": masks, "fraction": area})
                diff.paste((0, 0, 0), mask=mask_image)
            check(diff.getbbox() is None, name + " pixels fixos idênticos à referência")
        check(inventory.get("visual_review", {}).get("all_pages_inspected") is True, "revisão visual de todas as páginas registrada")
        check(inventory.get("visual_review", {}).get("pdf_render_inspected") is True, "renderização do PDF inspecionada")
    except (OSError, ValueError, TypeError, KeyError, AttributeError, IndexError) as exc:
        check(False, "verificação interrompida", f"{type(exc).__name__}: {exc}")
    report = {
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "status": "falhou" if problems else "verificacoes_mecanicas_passaram",
        "final_approval": False,
        "checks": checks, "problems": problems, "limitations": limitations,
        "files": [{"path": str(path.relative_to(repo)).replace("\\", "/"), "bytes": path.stat().st_size, "sha256": sha256(path)} for path in files],
    }
    try:
        report_path = artifact(args.report)
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    except (OSError, ValueError) as exc:
        print("Não foi possível gravar relatório:", exc, file=sys.stderr)
        return 2
    print(json.dumps({"status": report["status"], "checks": len(checks), "failures": len(problems), "report": args.report}, ensure_ascii=False))
    for problem in problems:
        print("- " + problem)
    return int(bool(problems))


if __name__ == "__main__":
    raise SystemExit(main())
