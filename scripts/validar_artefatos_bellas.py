"""QA direto de PSD, PNGs e PDF Bellas; não altera os arquivos.

Exemplo:
python scripts/validar_artefatos_bellas.py --manifest PROJETO/manifesto_final.json
  --psd PROJETO/entrega/final.psd --png-dir PROJETO/entrega/provas_png
  --pdf PROJETO/entrega/final.pdf --require-srgb-icc
"""
from __future__ import annotations

import argparse
import json
import re
from io import BytesIO
from pathlib import Path

import pymupdf
from PIL import Image, ImageChops, ImageCms
from psd_tools import PSDImage
from validar_manifest import validate as validate_manifest
from contrato_bellas import normalized
from verificar_textos_psd import compare_pages, descendants as visible_descendants, verify_reopen
from verificar_molde import validate as validate_template


ROOT = Path(__file__).resolve().parents[1]
APPROVED = (ROOT / "referencias" / "molde_bellas_aprovado_capa_temas_agradecimento.psd").resolve()
THANKS = ROOT / "exemplos" / "optima_final" / "pngs_aprovados" / "pagina_13.png"
COVER = ROOT / "exemplos" / "optima_final" / "pngs_aprovados" / "pagina_01.png"
TITLE_REGION = (920, 415, 1870, 735)


def descendants(group, names=()):
    for layer in group:
        path = names + (layer.name,)
        yield layer, path
        if layer.is_group():
            yield from descendants(layer, path)


def numbered_pngs(folder: Path, problems: list[str]) -> list[Path]:
    numbered: list[tuple[int, Path]] = []
    for path in folder.glob("*.png"):
        match = re.fullmatch(r"pagina_(\d+)", path.stem, re.I)
        if not match:
            problems.append(f"PNG com nome fora do padrão pagina_NN: {path.name}")
            continue
        numbered.append((int(match.group(1)), path))
    numbered.sort()
    if [number for number, _ in numbered] != list(range(1, len(numbered) + 1)):
        problems.append("PNGs ausentes, duplicados ou fora da sequência 1..N")
    if not numbered:
        problems.append(f"nenhum PNG em {folder}")
    return [path for _, path in numbered]


def same_rgb(left: Image.Image, right: Image.Image) -> bool:
    a, b = left.convert("RGB"), right.convert("RGB")
    return a.size == b.size and ImageChops.difference(a, b).getbbox() is None


def cover_same_outside_title(final: Image.Image, reference: Image.Image) -> bool:
    if final.size != reference.size:
        return False
    diff = ImageChops.difference(final.convert("RGB"), reference.convert("RGB"))
    from PIL import ImageDraw
    ImageDraw.Draw(diff).rectangle(TITLE_REGION, fill=(0, 0, 0))
    return diff.getbbox() is None


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--psd", type=Path, required=True)
    parser.add_argument("--png-dir", type=Path, required=True)
    parser.add_argument("--pdf", type=Path, required=True)
    parser.add_argument("--require-srgb-icc", action="store_true",
                        help="Exigir ICC sRGB nos PNGs novos e no PDF; provas Optima históricas não têm ICC")
    parser.add_argument("--report", type=Path)
    parser.add_argument("--legacy", action="store_true", help="Diagnóstico de arte histórica, sem homologar contrato novo")
    parser.add_argument("--reopen-report", type=Path)
    parser.add_argument("--reopen-png-dir", type=Path)
    args = parser.parse_args()
    args.require_srgb_icc = args.require_srgb_icc or not args.legacy
    problems: list[str] = []
    details: dict[str, object] = {}
    try:
        manifest_path = args.manifest.resolve()
        manifest = json.loads(manifest_path.read_text(encoding="utf-8-sig"))
        manifest_problems = validate_manifest(manifest_path, "final", True, args.legacy)
        problems.extend("manifesto: " + p for p in manifest_problems)
        if not isinstance(manifest, dict):
            raise ValueError("manifesto deve ser objeto")
        template = manifest.get("template", {})
        value = template.get("psd")
        actual_template = (manifest_path.parent / value).resolve() if isinstance(value, str) else None
        if actual_template != APPROVED:
            problems.append(f"manifesto: template.psd deve apontar só para {APPROVED}")
        if template.get("approved_psd"):
            problems.append("manifesto: template.approved_psd aponta para outro PSD; use PNGs de referência visual, não um PSD doador")
        psd = PSDImage.open(args.psd)
        if (psd.width, psd.height) != (1920, 1080):
            problems.append(f"PSD: canvas {psd.width}x{psd.height}; esperado 1920x1080")
        groups = sorted([layer for layer in psd if layer.is_group() and re.match(r"^\d+\b", layer.name)], key=lambda layer: int(re.match(r"^(\d+)", layer.name).group(1)))
        nums = sorted(int(re.match(r"^(\d+)", group.name).group(1)) for group in groups)
        if nums != list(range(1, len(nums) + 1)):
            problems.append(f"PSD: grupos de página fora da sequência 1..N: {nums}")
        if not groups:
            problems.append("PSD: nenhuma pasta de página numerada")
        hidden = []
        for group in groups:
            for layer, path, visible in visible_descendants(group):
                # Visibilidade local, não a do grupo da página atualmente oculto.
                if layer.kind == "type" and not visible:
                    hidden.append(group.name + "/" + path)
        if hidden:
            problems.append("PSD: camadas de texto ocultas dentro de páginas finais: " + "; ".join(hidden))
        details["psd_page_groups"] = len(groups)
        details["hidden_text_layers"] = hidden
        if not args.legacy:
            problems.extend("molde: " + p for p in validate_template(APPROVED))
        fixed_texts = {}
        if not args.legacy:
            template_psd = PSDImage.open(APPROVED)
            for original in template_psd:
                if not original.is_group():
                    continue
                key = "cover" if original.name.startswith("CAPA APROVADA") else "thanks" if original.name.startswith("AGRADECIMENTO") else None
                if key:
                    fixed_texts[key] = [normalized(l.text) for l,p,v in visible_descendants(original) if l.kind == "type" and (key != "cover" or "Desodorante" not in str(l.text))]
        # Não executar comparações de estilos com dados malformados.
        if not manifest_problems:
            problems.extend(compare_pages(manifest, groups, fixed_texts, args.legacy))
        details["manifest_page_count"] = len(manifest.get("slides", [])) if isinstance(manifest.get("slides"), list) else None

        pngs = numbered_pngs(args.png_dir, problems)
        details["png_count"] = len(pngs)
        if len(pngs) != len(groups):
            problems.append(f"contagem: {len(groups)} páginas no PSD, {len(pngs)} PNGs")
        for path in pngs:
            with Image.open(path) as png:
                if png.size != (1920, 1080):
                    problems.append(f"{path.name}: canvas {png.size}")
                if png.convert("RGBA").getchannel("A").getextrema() != (255, 255):
                    problems.append(f"{path.name}: transparência inesperada")
                if args.require_srgb_icc:
                    icc = png.info.get("icc_profile")
                    if not icc:
                        problems.append(f"{path.name}: perfil ICC ausente")
                    else:
                        name = ImageCms.getProfileName(ImageCms.ImageCmsProfile(BytesIO(icc)))
                        if "srgb" not in name.casefold():
                            problems.append(f"{path.name}: perfil ICC não identificado como sRGB: {name}")
        if not args.legacy or args.reopen_report or args.reopen_png_dir:
            problems.extend(verify_reopen(args.psd, args.reopen_report, pngs, args.reopen_png_dir, same_rgb, Image.open))

        if pngs:
            with Image.open(pngs[0]) as final, Image.open(COVER) as ref:
                if not cover_same_outside_title(final, ref):
                    problems.append("capa diverge da referência fora da área do título")
            with Image.open(pngs[-1]) as final, Image.open(THANKS) as ref:
                if not same_rgb(final, ref):
                    problems.append("agradecimento diverge da referência aprovada")

        with pymupdf.open(args.pdf) as pdf:
            details["pdf_pages"] = len(pdf)
            if len(pdf) != len(pngs):
                problems.append(f"contagem: {len(pdf)} páginas no PDF, {len(pngs)} PNGs")
            for number, (page, path) in enumerate(zip(pdf, pngs), 1):
                images = page.get_images(full=True)
                if len(images) != 1:
                    problems.append(f"PDF p{number:02}: esperada exatamente uma imagem de página")
                elif args.require_srgb_icc:
                    kind, value = pdf.xref_get_key(images[0][0], "ColorSpace")
                    color_object = pdf.xref_object(int(value.split()[0])) if kind == "xref" else value
                    match = re.search(r"/ICCBased\s+(\d+)\s+0\s+R", color_object)
                    if not match:
                        problems.append(f"PDF p{number:02}: imagem sem espaço de cor ICCBased")
                    else:
                        with Image.open(path) as png:
                            if pdf.xref_stream(int(match.group(1))) != png.info.get("icc_profile"):
                                problems.append(f"PDF p{number:02}: ICC incorporado difere do PNG")
                pixels = page.get_pixmap(matrix=pymupdf.Matrix(1, 1), colorspace=pymupdf.csRGB, alpha=False)
                rendered = Image.frombytes("RGB", (pixels.width, pixels.height), pixels.samples)
                with Image.open(path) as png:
                    if not same_rgb(rendered, png):
                        problems.append(f"PDF p{number:02}: renderização diverge do PNG")
    except Exception as exc:
        problems.append(f"erro de leitura/validação: {type(exc).__name__}: {exc}")

    report = {"status": "passed" if not problems else "failed",
              "validation_mode": "legacy" if args.legacy else "final_2.0",
              "visual_approval": False,
              "problems": problems, "details": details}
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if problems:
        print("Artefatos inválidos:\n" + "\n".join("- " + p for p in problems))
        return 1
    print(f"Integridade técnica conferida: {details['psd_page_groups']} páginas; modo {report['validation_mode']}. Parecer visual/editorial separado obrigatório.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
