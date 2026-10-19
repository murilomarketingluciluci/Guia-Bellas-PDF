"""Build a labeled 4-column contact sheet from exported Photoshop page PNGs.

Usage: python scripts/criar_contato_provas.py PROVAS_DIR SAIDA.jpg [EXPECTED_COUNT]
"""
from __future__ import annotations
import math
import sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont


def main() -> int:
    if len(sys.argv) not in (3, 4):
        print("Uso: python scripts/criar_contato_provas.py PROVAS_DIR SAIDA.jpg [EXPECTED_COUNT]")
        return 2
    folder = Path(sys.argv[1]).resolve()
    output = Path(sys.argv[2]).resolve()
    files = sorted(folder.glob("*.png"))
    if not files:
        print("Nenhum PNG encontrado em", folder)
        return 1
    if len(sys.argv) == 4 and len(files) != int(sys.argv[3]):
        print(f"Contagem incorreta: {len(files)} PNGs, esperado {sys.argv[3]}")
        return 1
    cols, cell_w, cell_h, label_h = 4, 400, 225, 26
    rows = math.ceil(len(files) / cols)
    sheet = Image.new("RGB", (cols * cell_w, rows * (cell_h + label_h)), "#f5eef2")
    draw = ImageDraw.Draw(sheet)
    try:
        font = ImageFont.truetype(r"C:\Windows\Fonts\arial.ttf", 17)
    except OSError:
        font = ImageFont.load_default()
    errors = []
    for i, file in enumerate(files):
        with Image.open(file) as raw:
            if abs(raw.width / raw.height - 16 / 9) > 0.003:
                errors.append(f"{file.name}: {raw.width}×{raw.height} não é 16:9")
            img = raw.convert("RGB").resize((cell_w, cell_h), Image.Resampling.LANCZOS)
        x, y = (i % cols) * cell_w, (i // cols) * (cell_h + label_h)
        sheet.paste(img, (x, y))
        draw.text((x + 5, y + cell_h + 3), file.stem, fill="#713b53", font=font)
    output.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(output, quality=92)
    print(f"Contato: {output}; {len(files)} telas")
    for error in errors:
        print("AVISO", error)
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
