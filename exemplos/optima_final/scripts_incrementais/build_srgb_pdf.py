from pathlib import Path
from PIL import Image, ImageCms, ImageDraw
from pypdf import PdfReader
import io
import pymupdf

root = Path(__file__).resolve().parent
proof_dir = root / 'srgb_provas'
proofs = [proof_dir / f'pagina_{i:02d}.jpg' for i in range(1, 13)]
profile = None
for proof in proofs:
    with Image.open(proof) as im:
        assert im.size == (1920, 1080), proof
        icc = im.info.get('icc_profile')
        assert icc, f'ICC ausente: {proof}'
        assert 'sRGB' in ImageCms.getProfileName(ImageCms.ImageCmsProfile(io.BytesIO(icc)))
        if profile is None:
            profile = icc
        else:
            assert icc == profile, f'ICC divergente: {proof}'

pdf_path = root / 'optima_apn_bellas_final_srgb_stage.pdf'
pdf = pymupdf.open()
for proof in proofs:
    page = pdf.new_page(width=1920, height=1080)
    page.insert_image(page.rect, filename=str(proof))
pdf.save(pdf_path, garbage=4, deflate=True)
pdf.close()

reader = PdfReader(str(pdf_path))
assert len(reader.pages) == 12
for number, page in enumerate(reader.pages, 1):
    xobjects = page['/Resources']['/XObject']
    assert len(xobjects) == 1, f'Imagem da página {number}: {len(xobjects)} objetos'
    image = next(iter(xobjects.values())).get_object()
    color_space = image['/ColorSpace']
    assert color_space[0] == '/ICCBased', f'Página {number} sem ICCBased'
    embedded_profile = color_space[1].get_object().get_data()
    assert embedded_profile == profile, f'ICC PDF divergente na página {number}'

sheet = Image.new('RGB', (1940, 1580), '#f5f2f2')
draw = ImageDraw.Draw(sheet)
for index, proof in enumerate(proofs):
    with Image.open(proof) as im:
        thumb = im.resize((620, 349), Image.Resampling.LANCZOS)
    x = 20 + (index % 3) * 640
    y = 20 + (index // 3) * 390
    sheet.paste(thumb, (x, y + 22))
    draw.text((x + 4, y + 2), f'PÁGINA {index+1:02d}', fill='#B3718E')
sheet.save(root / 'optima_visao_geral_srgb_stage.jpg', quality=92, subsampling=0, icc_profile=profile)
print(f'PDF sRGB validado: 12 páginas, ICCBased em todas, {pdf_path.stat().st_size} bytes')
