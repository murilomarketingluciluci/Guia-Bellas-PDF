"""Verify portable catalog/media links without Photoshop."""
from __future__ import annotations
import csv
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    errors = []
    def asset(value: str, context: str) -> None:
        if not value or not (ROOT / value).is_file():
            errors.append(f"{context}: arquivo ausente {value}")
        if Path(value).is_absolute() or re.match(r"^[A-Za-z]:", value):
            errors.append(f"{context}: caminho absoluto {value}")
    data = json.loads((ROOT / "fontes_15_pdfs.json").read_text(encoding="utf-8-sig"))
    if data["count"] != 15 or data["pages"] != 227 or sum(s["pages"] for s in data["files"]) != 227:
        errors.append("fontes: esperado 15 PDFs e 227 páginas")
    for source in data["files"]:
        asset(source["contact_sheet"], source["alias"])
        asset(source["full_pdf_in_package"], source["alias"])
    rows = list(csv.DictReader((ROOT / "indice_227_telas.csv").open(encoding="utf-8-sig", newline="")))
    if len(rows) != 227 or len({(r["source_alias"], r["page"]) for r in rows}) != 227:
        errors.append("índice: esperado 227 referências únicas")
    for row in rows:
        asset(row.get("thumbnail", ""), row["source_alias"] + " " + row["page"])
    catalog = json.loads((ROOT / "catalogo_atual_26_layouts.json").read_text(encoding="utf-8-sig"))
    if len(catalog["layouts"]) != 26:
        errors.append("catálogo: esperado 26 arquétipos")
    for name in ["galeria_227_telas.html", "galeria_layouts.html"]:
        markup = (ROOT / name).read_text(encoding="utf-8")
        for value in re.findall(r'(?:href|src)="([^"]+)"', markup):
            if not value.startswith(("https:", "http:", "#", "data:", "javascript:")):
                asset(value.split("#", 1)[0], name)
    if errors:
        print("Pacote inválido:\n" + "\n".join("- " + e for e in errors))
        return 1
    print("Pacote válido: 227 referências únicas, 15 fontes, 26 arquétipos e links locais presentes.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
