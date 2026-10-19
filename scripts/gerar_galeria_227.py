"""Render source PDFs and rebuild the offline gallery (requires pdftoppm)."""
from __future__ import annotations
import csv
import html
import json
import shutil
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    sources = json.loads((ROOT / "fontes_15_pdfs.json").read_text(encoding="utf-8"))
    renderer = shutil.which("pdftoppm")
    if not renderer:
        raise SystemExit("Instale Poppler e adicione pdftoppm ao PATH.")
    sections, rows = [], []
    for source in sources["files"]:
        alias = source["alias"]
        slug = "rosangela" if alias == "anexo Rosangela" else alias
        pdf = ROOT / source["full_pdf_in_package"]
        folder = ROOT / "referencias" / "telas_227" / slug
        folder.mkdir(parents=True, exist_ok=True)
        prefix = folder / "pagina"
        subprocess.run([renderer, "-jpeg", "-scale-to", "640", "-jpegopt", "quality=86", str(pdf), str(prefix)], check=True, capture_output=True)
        files = sorted(folder.glob("pagina-*.jpg"), key=lambda p: int(p.stem.rsplit("-", 1)[1]))
        if len(files) != source["pages"]:
            raise RuntimeError(f"{alias}: {len(files)} provas, esperado {source['pages']}")
        cards = []
        for page, image in enumerate(files, 1):
            relative = image.relative_to(ROOT).as_posix()
            link = source["full_pdf_in_package"] + f"#page={page}"
            title = f"{alias} - página {page:02d}"
            cards.append(f'<a class="card" href="{html.escape(link)}" target="_blank"><img loading="lazy" src="{html.escape(relative)}" alt="{html.escape(title)}"><span>{html.escape(title)}</span></a>')
            rows.append(dict(source_alias=alias, source_pdf=source["source_name"], page=page, contact_sheet=source["contact_sheet"], full_pdf_in_package=source["full_pdf_in_package"], thumbnail=relative))
        sections.append(f'<section><h2>{html.escape(source["source_name"])} <small>{source["pages"]} telas</small></h2><div class="grid">{"".join(cards)}</div></section>')
    if len(rows) != 227:
        raise RuntimeError(f"Contagem global incorreta: {len(rows)}")
    with (ROOT / "indice_227_telas.csv").open("w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    markup = '''<!doctype html><html lang="pt-BR"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Bellas - 227 telas de referência</title><style>body{margin:0;background:#f8eef2;color:#502a3e;font:16px Arial,sans-serif}header{padding:36px max(24px,5vw);background:#713b53;color:white}main{padding:20px 5vw}h1{margin:0 0 12px;font-size:32px}p{max-width:1000px;line-height:1.5}h2{font-size:19px;margin:36px 0 16px}small{font-weight:normal}a{color:inherit}.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(280px,1fr));gap:18px}.card{background:white;text-decoration:none;border-radius:6px;overflow:hidden;box-shadow:0 3px 10px #502a3e15}.card img{width:100%;display:block}.card span{display:block;padding:10px 12px}.card:hover{outline:3px solid #a9708a}header a{margin-right:20px}footer{padding:40px}</style><header><h1>227 telas Bellas</h1><p>15 PDFs históricos. Clique em uma tela para abrir sua página na fonte. Miniaturas são referências visuais; confira o PDF em resolução integral. Padrões históricos com foto pequena ou foto na capa exigem adaptação às regras atuais.</p><a href="galeria_layouts.html">26 arquétipos atuais</a><a href="indice_227_telas.csv">Índice CSV</a></header><main>''' + "".join(sections) + '</main><footer>Galeria local e independente de rede. Fontes de identidade: PSD Bellas/Rosângela e molde editável.</footer></html>'
    (ROOT / "galeria_227_telas.html").write_text(markup, encoding="utf-8")
    print(f"Galeria criada: {len(rows)} telas / {len(sections)} fontes")


if __name__ == "__main__":
    main()
