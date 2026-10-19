"""Monta um PDF de páginas raster sem reamostrar os PNGs.

Uso: python scripts/montar_pdf_dos_pngs.py PASTA_PNG PDF_SAIDA
Aceita pagina_01.png... ou nomes iniciados por 01, 02... .
"""
from __future__ import annotations

import argparse
import re
from pathlib import Path

import pymupdf
from PIL import Image, ImageChops


def numbered_pngs(folder: Path) -> list[Path]:
    images = list(folder.glob("*.png"))
    if not images:
        raise ValueError(f"Nenhum PNG em {folder}")
    numbered = []
    for image in images:
        match = re.match(r"(?:pagina[_ -]*)?(\d+)(?:\D|$)", image.stem, re.I)
        if not match:
            raise ValueError(f"Nome sem numero inicial: {image.name}")
        numbered.append((int(match.group(1)), image))
    numbered.sort()
    expected = list(range(1, len(numbered) + 1))
    if [n for n, _ in numbered] != expected:
        raise ValueError("Numeracao repetida ou nao sequencial nos PNGs")
    return [image for _, image in numbered]


def assemble(images: list[Path], output: Path) -> None:
    document = pymupdf.open()
    try:
        for image in images:
            with Image.open(image) as original:
                width, height = original.size
                if original.convert("RGBA").getchannel("A").getextrema() != (255, 255):
                    raise ValueError(f"PNG com transparencia: {image.name}")
            page = document.new_page(width=width, height=height)
            page.insert_image(page.rect, filename=str(image))
        output.parent.mkdir(parents=True, exist_ok=True)
        document.save(output, garbage=4, deflate=True)
    finally:
        document.close()
    # Valide os pixels efetivamente incorporados, nao so o numero de paginas.
    with pymupdf.open(output) as result:
        if len(result) != len(images):
            raise AssertionError("Numero de paginas divergente")
        for number, (page, path) in enumerate(zip(result, images), 1):
            embedded = page.get_images(full=True)
            if len(embedded) != 1:
                raise AssertionError(f"Pagina {number}: esperada uma imagem incorporada")
            pix = pymupdf.Pixmap(result, embedded[0][0])
            if pix.colorspace.n != 3 or pix.n not in (3, 4):
                raise AssertionError(f"Pagina {number}: espaco de cor inesperado")
            actual = Image.frombytes("RGB" if pix.n == 3 else "RGBA", (pix.width, pix.height), pix.samples).convert("RGB")
            with Image.open(path) as original:
                wanted = original.convert("RGB")
                if wanted.size != actual.size or ImageChops.difference(wanted, actual).getbbox():
                    raise AssertionError(f"Pagina {number}: RGB do PDF diverge de {path.name}")
    print(f"PDF verificado: {len(images)} paginas, RGB identico aos PNGs — {output}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("png_folder", type=Path)
    parser.add_argument("pdf_output", type=Path)
    args = parser.parse_args()
    assemble(numbered_pngs(args.png_folder), args.pdf_output)
