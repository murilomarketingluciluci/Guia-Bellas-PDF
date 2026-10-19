"""Renderiza o PDF entregue e compara sua aparência com as provas, em 1920×1080."""
from pathlib import Path
import json
import pymupdf
from PIL import Image, ImageChops

project = Path(__file__).resolve().parents[1]
target = project / 'leitura/pdf_final_render'
target.mkdir(exist_ok=True)
results = []
with pymupdf.open(project / 'entrega/crescimento_luciane_bellas.pdf') as document:
    for number, page in enumerate(document, 1):
        pix = page.get_pixmap(matrix=pymupdf.Matrix(1, 1), colorspace=pymupdf.csRGB, alpha=False)
        output = target / f'pagina_{number:02}.png'
        pix.save(output)
        actual = Image.frombytes('RGB', (pix.width, pix.height), pix.samples)
        with Image.open(project / f'entrega/provas_png/pagina_{number:02}.png') as source:
            diff = ImageChops.difference(source.convert('RGB'), actual)
            results.append({'page': number, 'size': list(actual.size), 'render_equals_proof': diff.getbbox() is None})
report = {'renderer': 'PyMuPDF', 'version': pymupdf.VersionBind, 'pages': results}
(project / 'auditoria/renderizacao_pdf.json').write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
assert all(page['render_equals_proof'] for page in results), 'Há divergência entre renderização e prova'
print(f'{len(results)} páginas renderizadas, todas com RGB igual à prova.')
