"""Independent artifact checks; never edits PSD. A pass is not visual approval.

All paths are relative to --project unless absolute CLI arguments are supplied.
Requires psd-tools, Pillow, PyMuPDF. Reopen JSON and PNGs must be generated from
the saved PSD reopened in Photopea, not from the still-open build document.
"""
from __future__ import annotations
import argparse
from collections import Counter
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re
import sys
import unicodedata

from PIL import Image, ImageChops
import pymupdf as fitz
from psd_tools import PSDImage


def digest(path):
    h = hashlib.sha256()
    with Path(path).open('rb') as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b''):
            h.update(chunk)
    return h.hexdigest()


def norm(value):
    return re.sub(r'\s+', ' ', unicodedata.normalize('NFC', str(value))).strip()


def scalar(value):
    value = getattr(value, 'value', value)
    return value.decode('utf-8', 'replace') if isinstance(value, bytes) else value


def numbered(name):
    match = re.match(r'^(?:pagina[_ -]*)?(\d+)(?:\D|$)', name, re.I)
    return int(match.group(1)) if match else None


def walk(group, path=(), visible=True):
    for layer in group:
        current = path + (layer.name,)
        shown = visible and bool(layer.visible)
        yield layer, current, shown
        if layer.is_group():
            yield from walk(layer, current, shown)


def font_styles(layer):
    fonts = layer.resource_dict.get('FontSet', [])
    result = []
    runs = layer.engine_dict.get('StyleRun', {})
    lengths = runs.get('RunLengthArray', [])
    for index, run in enumerate(runs.get('RunArray', [])):
        data = run.get('StyleSheet', {}).get('StyleSheetData', {})
        fi = data.get('Font')
        font = scalar(fonts[int(fi)].get('Name')) if fi is not None and 0 <= int(fi) < len(fonts) else None
        color = data.get('FillColor', {}).get('Values', [])
        result.append({'font': font, 'length': int(lengths[index]) if index < len(lengths) else None,
                       'size': float(data.get('FontSize', 0)),
                       'tracking': float(data.get('Tracking', 0)),
                       'color': [float(x) for x in color]})
    return result


def image_equal(a, b):
    with Image.open(a) as ai, Image.open(b) as bi:
        ai, bi = ai.convert('RGB'), bi.convert('RGB')
        return ai.size == bi.size and ImageChops.difference(ai, bi).getbbox() is None


def collect_strings(obj, keys=('text', 'title', 'h1', 'body', 'quote', 'caption', 'reference', 'heading', 'content')):
    result = []
    if isinstance(obj, dict):
        for key, value in obj.items():
            if key in keys and isinstance(value, str):
                result.append(value)
            elif isinstance(value, (dict, list)):
                result.extend(collect_strings(value, keys))
    elif isinstance(obj, list):
        for value in obj:
            if isinstance(value, str):
                result.append(value)
            else:
                result.extend(collect_strings(value, keys))
    return result


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--project', type=Path, required=True)
    p.add_argument('--manifest', default='manifesto_final.json')
    p.add_argument('--content-source', default='leitura/conteudo_v2.json', help='Independent content transcription for coverage beyond manifest flags')
    p.add_argument('--psd', required=True)
    p.add_argument('--png-dir', required=True)
    p.add_argument('--pdf', required=True)
    p.add_argument('--reopen-report')
    p.add_argument('--reopen-png-dir')
    p.add_argument('--baseline-dir', help='Photopea exports of official template: capa.png, agradecimento.png')
    p.add_argument('--output', default='auditoria/validacao_independente.json')
    p.add_argument('--inspect-only', action='store_true', help='Diagnose unfinished artifacts; still fails missing checks')
    args = p.parse_args()
    project = args.project.resolve()
    repo = Path(__file__).resolve().parents[3]
    def resolve(value):
        candidate = Path(value)
        return candidate.resolve() if candidate.is_absolute() else (project / candidate).resolve()
    checks, errors, warnings, inventory = [], [], [], {}
    def check(name, ok, detail=None):
        checks.append({'check': name, 'passed': bool(ok), 'evidence': detail})
        if not ok:
            errors.append(name)
    def run():
        manifest_path, psd_path = resolve(args.manifest), resolve(args.psd)
        png_dir, pdf_path = resolve(args.png_dir), resolve(args.pdf)
        for label, path in [('manifest', manifest_path), ('psd', psd_path), ('png_dir', png_dir), ('pdf', pdf_path)]:
            check('exists_' + label, path.exists(), str(path))
        if errors:
            return
        manifest = json.loads(manifest_path.read_text(encoding='utf-8-sig'))
        pages = manifest.get('pages', manifest.get('paginas', []))
        check('manifest_pages', isinstance(pages, list) and len(pages) >= 3, len(pages))
        check('manifest_final', manifest.get('stage') == 'final', manifest.get('stage'))
        def manifest_scan(obj, path='$'):
            if isinstance(obj, dict):
                for key, value in obj.items():
                    at = path + '.' + key
                    if 'placeholder' in key.lower():
                        check('manifest_no_placeholder_' + at, False, value)
                    if key.lower() in ('src', 'path', 'file', 'asset', 'font_file', 'photo_path') and isinstance(value, str):
                        if '://' not in value:
                            target = (project / value).resolve()
                            check('relative_asset_' + at, not Path(value).is_absolute() and target.is_relative_to(project), value)
                            check('exists_asset_' + at, target.is_file(), value)
                    if isinstance(value, (dict, list)):
                        manifest_scan(value, at)
            elif isinstance(obj, list):
                for i, value in enumerate(obj):
                    manifest_scan(value, path + '[' + str(i) + ']')
        manifest_scan(manifest)
        with psd_path.open('rb') as stream:
            check('psd_signature', stream.read(4) == b'8BPS')
        psd = PSDImage.open(psd_path)
        check('canvas_1920_1080', (psd.width, psd.height) == (1920, 1080), [psd.width, psd.height])
        groups = sorted([(numbered(x.name), x) for x in psd if x.is_group() and numbered(x.name) is not None], key=lambda x: x[0])
        check('groups_sequential', [n for n, _ in groups] == list(range(1, len(pages) + 1)), [x.name for _, x in groups])
        check('only_one_page_visible', sum(bool(x.visible) for _, x in groups) == 1)
        pngs = sorted([(numbered(x.stem), x) for x in png_dir.glob('*.png') if numbered(x.stem) is not None], key=lambda x: x[0])
        check('pngs_sequential', [n for n, _ in pngs] == list(range(1, len(pages) + 1)), [x.name for _, x in pngs])
        check('all_pngs_numbered', len(pngs) == len(list(png_dir.glob('*.png'))))
        placeholder = re.compile(r'^(?:H1|T[IÍ]TULO|TEXTO|BLOCO(?:\s+\d+)?|ITEM(?:\s+\d+)?|BULLET(?:\s+\d+)?|FOTO|IMAGEM|\d+\s*[–-]\s*\d+\s+LINHAS)$', re.I)
        page_inventory = []
        for number, group in groups:
            records, texts = [], []
            for layer, path, shown in walk(group):
                record = {'path': '/'.join(path), 'kind': layer.kind, 'visible_in_page': shown, 'bounds': list(layer.bbox)}
                if layer.kind == 'type':
                    text = layer.text.rstrip('\x00\r\n')
                    record['text'] = text
                    try:
                        record['styles'] = font_styles(layer)
                    except Exception as exc:
                        record['style_error'] = str(exc)
                        check(f'text_styles_readable_{number}_{record["path"]}', False, str(exc))
                    if shown:
                        texts.append(text)
                        check(f'no_placeholder_{number}_{record["path"]}', not any(placeholder.fullmatch(norm(line)) for line in text.splitlines()), text)
                        used = [s['font'] for s in record.get('styles', []) if s['length'] != 0]
                        check(f'gotham_{number}_{record["path"]}', bool(used) and all(f and 'gotham' in f.lower() for f in used), used)
                        x0, y0, x1, y1 = layer.bbox
                        check(f'text_inside_canvas_{number}_{record["path"]}', x0 >= 0 and y0 >= 0 and x1 <= psd.width and y1 <= psd.height, list(layer.bbox))
                records.append(record)
            check(f'editable_text_page_{number}', bool(texts), len(texts))
            if number <= len(pages):
                expected = collect_strings(pages[number - 1])
                actual = norm(' '.join(texts))
                # Layout labels / layout type strings are deliberately not treated as content.
                for value in expected:
                    check(f'manifest_text_page_{number}_{norm(value)[:55]}', norm(value) in actual, value)
                if not expected:
                    check(f'manifest_content_defined_{number}', False)
                h1 = pages[number - 1].get('h1') if isinstance(pages[number - 1], dict) else None
                if isinstance(h1, str):
                    check(f'h1_single_editable_object_{number}', sum(norm(t) == norm(h1) for t in texts) == 1, h1)
            page_inventory.append({'number': number, 'group': group.name, 'layers': records})
        inventory['pages'] = page_inventory
        source_path = resolve(args.content_source)
        check('independent_content_source_exists', source_path.is_file(), str(source_path))
        if source_path.is_file():
            source = json.loads(source_path.read_text(encoding='utf-8-sig'))
            page_texts = [norm(' '.join(x.get('text', '') for x in page['layers'] if x.get('visible_in_page') and x['kind'] == 'type')).casefold() for page in page_inventory]
            source_numbers = Counter()
            actual_numbers = Counter(norm(x.get('text', '')) for page in page_inventory for x in page['layers'] if x.get('visible_in_page') and x['kind'] == 'type')
            for source_page in source.get('pages', []):
                for block in source_page.get('blocks', []):
                    values = [norm(block[key]).casefold() for key in ('title', 'text', 'reference') if isinstance(block.get(key), str)]
                    # A source episode's title, action and reference must remain together.
                    check('source_block_' + block.get('id', '?'), bool(values) and any(all(value in text for value in values) for text in page_texts), values)
                    if isinstance(block.get('number'), str):
                        source_numbers[block['number']] += 1
            for number, count in source_numbers.items():
                check('source_number_occurrences_' + number, actual_numbers[number] >= count, {'expected_minimum': count, 'actual_exact_text_layers': actual_numbers[number]})
            inventory['independent_source_sha256'] = digest(source_path)
        icc = psd.image_resources.get_data(1039)
        inventory['psd_icc'] = {'present': bool(icc), 'sha256': hashlib.sha256(icc).hexdigest() if isinstance(icc, bytes) else None}
        for number, path in pngs:
            with Image.open(path) as image:
                check(f'png_size_{number}', image.size == (1920, 1080), image.size)
                check(f'png_rgb_{number}', image.mode in ('RGB', 'RGBA'), image.mode)
                check(f'png_opaque_{number}', image.convert('RGBA').getchannel('A').getextrema() == (255, 255))
                inventory.setdefault('pngs', []).append({'number': number, 'file': path.name, 'sha256': digest(path), 'icc_present': bool(image.info.get('icc_profile')), 'srgb_chunk': image.info.get('srgb')})
        with fitz.open(pdf_path) as pdf:
            check('pdf_page_count', len(pdf) == len(pages), len(pdf))
            for i, ((number, png), page) in enumerate(zip(pngs, pdf)):
                images = page.get_images(full=True)
                check(f'pdf_single_embedded_image_{number}', len(images) == 1, len(images))
                if len(images) != 1:
                    continue
                pix = fitz.Pixmap(pdf, images[0][0])
                if pix.colorspace is None or pix.colorspace.n != 3:
                    check(f'pdf_rgb_{number}', False)
                    continue
                extracted = Image.frombytes('RGBA' if pix.alpha else 'RGB', (pix.width, pix.height), pix.samples).convert('RGB')
                with Image.open(png) as image:
                    image = image.convert('RGB')
                    same = image.size == extracted.size and ImageChops.difference(image, extracted).getbbox() is None
                check(f'pdf_pixels_identical_{number}', same)
                check(f'pdf_aspect_{number}', abs(page.rect.width / page.rect.height - 16 / 9) < 0.00001)
        # The approved template is independent of any earlier Crescimento implementation.
        template = PSDImage.open(repo / 'referencias/molde_bellas_aprovado_capa_temas_agradecimento.psd')
        cover_ref = next(x for x in template if x.is_group() and x.name.startswith('CAPA APROVADA'))
        thanks_ref = next(x for x in template if x.is_group() and x.name.startswith('AGRADECIMENTO APROVADO'))
        def visible_types(group):
            return [norm(x.text) for x, _, shown in walk(group) if shown and x.kind == 'type']
        if groups:
            cover_text = visible_types(groups[0][1])
            fixed = Counter(visible_types(cover_ref))
            fixed.pop(norm('Desodorante Optima'), None)
            remainder = Counter(cover_text) - fixed
            check('cover_fixed_text_preserved', not bool(fixed - Counter(cover_text)), list((fixed - Counter(cover_text)).elements()))
            check('cover_only_one_content_title', sum(remainder.values()) == 1, list(remainder.elements()))
            title = manifest.get('title', manifest.get('training_title'))
            if title:
                check('cover_title_matches_manifest', list(remainder.elements()) == [norm(title)], title)
            check('thanks_fixed_text', Counter(visible_types(groups[-1][1])) == Counter(visible_types(thanks_ref)))
            # New photographs or removed fixed layers change the multiset of visible kinds.
            def kind_counts(group):
                return Counter(x.kind for x, _, shown in walk(group) if shown and not x.is_group())
            check('cover_fixed_layer_kind_counts', kind_counts(groups[0][1]) == kind_counts(cover_ref), dict(kind_counts(groups[0][1])))
            check('thanks_fixed_layer_kind_counts', kind_counts(groups[-1][1]) == kind_counts(thanks_ref), dict(kind_counts(groups[-1][1])))
        if args.baseline_dir:
            baseline = resolve(args.baseline_dir)
            ref_thanks, ref_cover = baseline / 'agradecimento.png', baseline / 'capa.png'
        else:
            ref_thanks = repo / 'exemplos/optima_final/pngs_aprovados/pagina_13.png'
            ref_cover = repo / 'exemplos/optima_final/pngs_aprovados/pagina_01.png'
        if pngs:
            check('thanks_pixels_approved', ref_thanks.is_file() and image_equal(ref_thanks, pngs[-1][1]), str(ref_thanks))
            # Exclude union of the old and new title bounds only; inspect all fixed pixels.
            old = [x.bbox for x, _, shown in walk(cover_ref) if shown and x.kind == 'type' and 'optima' in norm(x.text).lower()]
            new = [x.bbox for x, _, shown in walk(groups[0][1]) if shown and x.kind == 'type' and norm(x.text) not in fixed]
            check('cover_title_bounds_identified', bool(old) and bool(new), {'old': old, 'new': new})
            if old and new and ref_cover.is_file():
                with Image.open(ref_cover) as a, Image.open(pngs[0][1]) as b:
                    diff = ImageChops.difference(a.convert('RGB'), b.convert('RGB'))
                    from PIL import ImageDraw
                    draw = ImageDraw.Draw(diff)
                    for box in old + new:
                        draw.rectangle((box[0] - 3, box[1] - 3, box[2] + 3, box[3] + 3), fill=(0, 0, 0))
                    check('cover_fixed_pixels_approved', diff.getbbox() is None)
        check('photopea_reopen_report_present', bool(args.reopen_report) and resolve(args.reopen_report).is_file())
        if args.reopen_report and resolve(args.reopen_report).is_file():
            reopened = json.loads(resolve(args.reopen_report).read_text(encoding='utf-8-sig'))
            check('reopen_psd_hash_matches', reopened.get('psd_sha256') == digest(psd_path), reopened.get('psd_sha256'))
            rp = reopened.get('pages', [])
            check('reopen_page_names', [x.get('name', x.get('group')) for x in rp] == [x.name for _, x in groups])
            for page in rp:
                check('reopen_actual_layer_inventory_' + str(page.get('name', page.get('group'))), isinstance(page.get('layers'), list) and bool(page['layers']))
            warnings.append('Reopen JSON is corroborative evidence. Independent PSD parsing and re-export PNG comparisons are also required.')
        check('reopen_png_folder_present', bool(args.reopen_png_dir) and resolve(args.reopen_png_dir).is_dir())
        if args.reopen_png_dir and resolve(args.reopen_png_dir).is_dir():
            reopened_pngs = sorted([(numbered(x.stem), x) for x in resolve(args.reopen_png_dir).glob('*.png') if numbered(x.stem) is not None], key=lambda x: x[0])
            check('reopen_png_count', len(reopened_pngs) == len(pngs))
            for (n, a), (m, b) in zip(pngs, reopened_pngs):
                check(f'reopen_png_pixels_{n}', n == m and image_equal(a, b))
        inventory['hashes'] = {str(x.relative_to(project)) if x.is_relative_to(project) else str(x): digest(x) for x in [manifest_path, psd_path, pdf_path]}
        warnings.extend(['No automated check certifies photo realism, whitespace, glyph clipping inside text boxes, visual hierarchy, editorial completeness, or visible rasterized placeholder text.', 'Gotham names in PSD are necessary but do not prove that font files were loaded in Photopea; require font-load event evidence and visual comparison.'])
    try:
        run()
    except Exception as exc:
        check('validator_exception', False, {'type': type(exc).__name__, 'message': str(exc)})
    output = resolve(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    result = {'timestamp': datetime.now(timezone.utc).isoformat(), 'validator_sha256': digest(__file__),
              'status': 'passed_artifact_checks' if not errors else 'failed', 'visual_approval': False,
              'checks': checks, 'errors': errors, 'warnings': warnings, 'inventory': inventory}
    output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({'status': result['status'], 'passed': sum(x['passed'] for x in checks), 'failed': len(errors), 'report': str(output)}, ensure_ascii=False))
    return 0 if not errors else 1


if __name__ == '__main__':
    sys.exit(main())
