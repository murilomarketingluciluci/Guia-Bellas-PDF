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
import numpy as np
import pymupdf as fitz
from psd_tools import PSDImage
from validacao_inputs_compativeis import validate_compatible_inputs


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


def pixel_metrics(reference, actual, exclusions=()):
    """Measures independent approved RGB; never substitutes the current output as baseline."""
    with Image.open(reference) as a, Image.open(actual) as b:
        left, right = np.asarray(a.convert('RGB')), np.asarray(b.convert('RGB'))
        if left.shape != right.shape:
            return {'same_size': False, 'reference_shape': list(left.shape), 'actual_shape': list(right.shape), 'identical': False}
        selected = np.ones(left.shape[:2], dtype=bool)
        for x0, y0, x1, y1 in exclusions:
            selected[max(0, int(y0) - 3):min(left.shape[0], int(y1) + 4), max(0, int(x0) - 3):min(left.shape[1], int(x1) + 4)] = False
        delta = np.abs(left.astype(np.int16) - right.astype(np.int16))[selected]
        changed = np.any(delta != 0, axis=1)
        return {'same_size': True, 'reference_sha256': digest(reference), 'actual_sha256': digest(actual),
                'pixels_compared': len(delta), 'pixels_changed': int(changed.sum()),
                'changed_percent': float(changed.mean() * 100), 'mae_rgb': float(delta.mean()),
                'max_channel_delta': int(delta.max()), 'identical': not bool(changed.any()), 'excluded_title_boxes': [list(x) for x in exclusions]}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--project', type=Path, required=True)
    p.add_argument('--manifest', default='manifesto_final.json')
    p.add_argument('--content-source', default='leitura/conteudo_v2.json', help='Independent content transcription for coverage beyond manifest flags')
    p.add_argument('--psd', required=True)
    p.add_argument('--png-dir', default='provas')
    p.add_argument('--pdf', default='entrega/crescimento_photopea_v2.pdf')
    p.add_argument('--compatible-source-inputs', action='store_true', help='Audit explicit SO/shape/fill->pixel input packaging; does not relax approved PNG equality')
    p.add_argument('--psd-audit-only', action='store_true', help='Audit PSD and available proofs; defer PDF/reopen checks explicitly, never final approval')
    p.add_argument('--reopen-report')
    p.add_argument('--reopen-png-dir')
    p.add_argument('--baseline-dir', help='Optional runtime comparison only; never replaces approved Photoshop PNG references')
    p.add_argument('--output', default='auditoria/validacao_independente.json')
    p.add_argument('--inspect-only', action='store_true', help='Diagnose unfinished artifacts; still fails missing checks')
    args = p.parse_args()
    project = args.project.resolve()
    repo = Path(__file__).resolve().parents[3]
    def resolve(value):
        candidate = Path(value)
        return candidate.resolve() if candidate.is_absolute() else (project / candidate).resolve()
    checks, errors, warnings, inventory, deferred = [], [], [], {}, []
    def check(name, ok, detail=None, category='artifact', required=True):
        checks.append({'check': name, 'passed': bool(ok), 'evidence': detail, 'category': category, 'required': required})
        if not ok and required:
            errors.append(name)
    def run():
        manifest_path, psd_path = resolve(args.manifest), resolve(args.psd)
        png_dir, pdf_path = resolve(args.png_dir), resolve(args.pdf)
        for label, path in [('manifest', manifest_path), ('psd', psd_path)]:
            check('exists_' + label, path.exists(), str(path))
        if errors:
            return
        check('exists_png_dir', png_dir.is_dir(), str(png_dir))
        if args.psd_audit_only:
            deferred.extend(['Final PDF and embedded pixel checks', 'Photopea reopen JSON/hash and re-export pixel checks'])
        else:
            check('exists_pdf', pdf_path.is_file(), str(pdf_path))
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
        inventory['psd_total_layer_count'] = len(list(walk(psd)))
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
            background = [layer for layer, _, shown in walk(group) if shown and layer.name == 'FUNDO' and layer.kind == 'pixel']
            if args.compatible_source_inputs:
                check(f'compatible_background_unique_{number}', len(background) == 1)
                if len(background) == 1:
                    target = (188, 113, 140) if pages[number - 1].get('theme') == 'escuro' else (251, 169, 195)
                    bg = background[0].topil(apply_icc=False)
                    extrema = bg.convert('RGB').getextrema() if bg is not None else None
                    check(f'compatible_approved_background_rgb_{number}', extrema == tuple((c, c) for c in target), {'target': target, 'channel_extrema': extrema})
            if number <= len(pages):
                page_spec = pages[number - 1]
                # Actual V2 schema: only texts[].text is editorial content.
                # Source image paths/layout reference labels are provenance, not rendered text.
                specs = page_spec.get('texts', [])
                expected = [spec['text'] for spec in specs] if specs else collect_strings(page_spec)
                actual = norm(' '.join(texts))
                # Layout labels / layout type strings are deliberately not treated as content.
                for value in expected:
                    check(f'manifest_text_page_{number}_{norm(value)[:55]}', norm(value) in actual, value)
                if not expected:
                    check(f'manifest_content_defined_{number}', False)
                for spec in specs:
                    matches = [row for row in records if row.get('kind') == 'type' and row['path'].split('/')[-1] == spec['name'] and row['visible_in_page']]
                    check(f'manifest_editable_object_{number}_{spec["name"]}', len(matches) == 1)
                    if len(matches) == 1:
                        check(f'manifest_object_contents_{number}_{spec["name"]}', norm(matches[0]['text']) == norm(spec['text']))
                        expected_fonts = {spec['font']} | {run.get('font', spec['font']) for run in spec.get('runs', [])}
                        actual_fonts = {style['font'] for style in matches[0].get('styles', []) if style['length'] != 0}
                        check(f'manifest_object_fonts_{number}_{spec["name"]}', expected_fonts <= actual_fonts, {'expected': sorted(expected_fonts), 'actual': sorted(actual_fonts)})
                        def hex_rgb(value):
                            return tuple(int(value.lstrip('#')[i:i + 2], 16) for i in (0, 2, 4))
                        expected_colors = {hex_rgb(spec['color'])} | {hex_rgb(run.get('color', spec['color'])) for run in spec.get('runs', [])}
                        actual_colors = {tuple(round(channel * 255) for channel in style['color'][-3:]) for style in matches[0].get('styles', []) if style['length'] != 0 and len(style['color']) >= 3}
                        check(f'manifest_object_colors_{number}_{spec["name"]}', expected_colors <= actual_colors, {'expected': sorted(expected_colors), 'actual': sorted(actual_colors)})
                        if spec['name'].endswith('-titulo'):
                            check(f'h1_single_editable_object_{number}', len(matches) == 1, spec['name'])
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
            actual_text_layers = [norm(x.get('text', '')) for page in page_inventory for x in page['layers'] if x.get('visible_in_page') and x['kind'] == 'type']
            for source_page in source.get('pages', []):
                for block in source_page.get('blocks', []):
                    values = [norm(block[key]).casefold() for key in ('title', 'text', 'reference') if isinstance(block.get(key), str)]
                    # A source episode's title, action and reference must remain together.
                    check('source_block_' + block.get('id', '?'), bool(values) and any(all(value in text for value in values) for text in page_texts), values)
                    if isinstance(block.get('number'), str):
                        source_numbers[block['number']] += 1
            for number, count in source_numbers.items():
                actual_count = sum(bool(re.match(r'^0?' + str(int(number)) + r'(?:\D|$)', text)) for text in actual_text_layers)
                check('source_number_occurrences_' + number, actual_count >= count, {'expected_minimum': count, 'actual_text_layers_starting_with_number': actual_count})
            inventory['independent_source_sha256'] = digest(source_path)
        icc = psd.image_resources.get_data(1039)
        inventory['psd_icc'] = {'present': bool(icc), 'sha256': hashlib.sha256(icc).hexdigest() if isinstance(icc, bytes) else None}
        for number, path in pngs:
            with Image.open(path) as image:
                check(f'png_size_{number}', image.size == (1920, 1080), image.size)
                check(f'png_rgb_{number}', image.mode in ('RGB', 'RGBA'), image.mode)
                check(f'png_opaque_{number}', image.convert('RGBA').getchannel('A').getextrema() == (255, 255))
                inventory.setdefault('pngs', []).append({'number': number, 'file': path.name, 'sha256': digest(path), 'icc_present': bool(image.info.get('icc_profile')), 'srgb_chunk': image.info.get('srgb')})
        if not args.psd_audit_only and pdf_path.is_file():
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
        if args.compatible_source_inputs:
            validate_compatible_inputs(project, template, groups, check, inventory)
        if groups:
            cover_text = visible_types(groups[0][1])
            fixed = Counter(visible_types(cover_ref))
            reference_title_layers = [x for x, _, shown in walk(cover_ref) if shown and x.kind == 'type' and x.name == 'Desodorante Optima']
            check('template_title_layer_identified', len(reference_title_layers) == 1)
            for layer in reference_title_layers:
                fixed.subtract([norm(layer.text)])
            fixed = +fixed
            remainder = Counter(cover_text) - fixed
            check('cover_fixed_text_preserved', not bool(fixed - Counter(cover_text)), list((fixed - Counter(cover_text)).elements()))
            check('cover_only_one_content_title', sum(remainder.values()) == 1, list(remainder.elements()))
            title = manifest.get('title', manifest.get('training_title'))
            if title:
                check('cover_title_matches_manifest', list(remainder.elements()) == [norm(title)], title)
            thanks_actual, thanks_expected = visible_types(groups[-1][1]), visible_types(thanks_ref)
            if args.compatible_source_inputs:
                source_thanks = [x for x, _, shown in walk(thanks_ref) if shown and x.kind == 'type' and norm(x.text) == 'obrigada!']
                source_caps = [int(style.get('StyleSheet', {}).get('StyleSheetData', {}).get('FontCaps', -1)) for x in source_thanks for style in x.engine_dict.get('StyleRun', {}).get('RunArray', [])]
                check('compatible_thanks_case_exception_source_fontcaps', source_caps == [2], source_caps)
                # The sole permitted case equivalence: source obrigada! + FontCaps2 -> native OBRIGADA!.
                thanks_expected = ['OBRIGADA!' if value == 'obrigada!' else value for value in thanks_expected]
                warnings.append('Explicit compatibility exception: source obrigada! with FontCaps2 is represented by native OBRIGADA!, because the API lacks TextCase.ALLCAPS. Other fixed strings remain case-sensitive.')
            check('thanks_fixed_text', Counter(thanks_actual) == Counter(thanks_expected), {'expected': thanks_expected, 'actual': thanks_actual})
            # New photographs or removed fixed layers change the multiset of visible kinds.
            def kind_counts(group):
                return Counter(x.kind for x, _, shown in walk(group) if shown and not x.is_group())
            check('cover_fixed_layer_kind_counts', kind_counts(groups[0][1]) == kind_counts(cover_ref), {'expected_original': dict(kind_counts(cover_ref)), 'actual': dict(kind_counts(groups[0][1])), 'policy': 'Original-kind diagnostic is nonrequired only with explicit compatible-source-inputs; linked-channel checks replace it.'}, required=not args.compatible_source_inputs)
            check('thanks_fixed_layer_kind_counts', kind_counts(groups[-1][1]) == kind_counts(thanks_ref), {'expected_original': dict(kind_counts(thanks_ref)), 'actual': dict(kind_counts(groups[-1][1]))}, required=not args.compatible_source_inputs)
            if args.compatible_source_inputs:
                def mapped_kinds(group):
                    return Counter('pixel' if x.kind in ('smartobject', 'shape', 'solidcolorfill') else x.kind for x, _, shown in walk(group) if shown and not x.is_group())
                expected_cover = mapped_kinds(cover_ref) + Counter({'pixel': 3})
                check('compatible_cover_mapped_kind_counts', kind_counts(groups[0][1]) == expected_cover, {'expected': dict(expected_cover), 'actual': dict(kind_counts(groups[0][1])), 'extra_three': 'Three explicit restored approved swatches, checked independently below.'})
                check('compatible_thanks_mapped_kind_counts', kind_counts(groups[-1][1]) == mapped_kinds(thanks_ref), {'expected': dict(mapped_kinds(thanks_ref)), 'actual': dict(kind_counts(groups[-1][1]))})
                source_swatches = ['Retângulo 572', 'Retângulo 572 copiar', 'Retângulo 572 copiar 2']
                approved_path = repo / 'exemplos/optima_final/pngs_aprovados/pagina_01.png'
                with Image.open(approved_path) as approved:
                    for index, source_name in enumerate(source_swatches, 1):
                        reference = [x for x, _, shown in walk(thanks_ref) if shown and x.name == source_name]
                        native = [x for x, _, shown in walk(groups[0][1]) if shown and x.name == f'COR APROVADA {index}']
                        check(f'compatible_cover_swatch_unique_{index}', len(reference) == len(native) == 1)
                        if len(reference) == len(native) == 1:
                            box = reference[0].bbox
                            check(f'compatible_cover_swatch_bbox_{index}', native[0].bbox == box)
                            target = approved.convert('RGB').getpixel(((box[0] + box[2]) // 2, (box[1] + box[3]) // 2))
                            cache = native[0].topil(apply_icc=False)
                            actual = cache.convert('RGB').getpixel((cache.width // 2, cache.height // 2)) if cache else None
                            check(f'compatible_cover_swatch_approved_rgb_{index}', actual == target, {'expected': target, 'actual': actual})
        # These references always remain the independent approved Photoshop PNGs.
        ref_thanks = repo / 'exemplos/optima_final/pngs_aprovados/pagina_13.png'
        ref_cover = repo / 'exemplos/optima_final/pngs_aprovados/pagina_01.png'
        if pngs:
            thanks_metrics = pixel_metrics(ref_thanks, pngs[-1][1]) if ref_thanks.is_file() else {'identical': False}
            check('thanks_pixels_approved', thanks_metrics['identical'], thanks_metrics, category='strict_approved_appearance')
            inventory.setdefault('approved_rgb_comparison', {})['thanks'] = thanks_metrics
            # Exclude union of the old and new title bounds only; inspect all fixed pixels.
            old = [x.bbox for x, _, shown in walk(cover_ref) if shown and x.kind == 'type' and 'optima' in norm(x.text).lower()]
            new = [x.bbox for x, _, shown in walk(groups[0][1]) if shown and x.kind == 'type' and norm(x.text) not in fixed]
            check('cover_title_bounds_identified', bool(old) and bool(new), {'old': old, 'new': new})
            if old and new and ref_cover.is_file():
                with Image.open(ref_cover) as a, Image.open(pngs[0][1]) as b:
                    cover_metrics = pixel_metrics(ref_cover, pngs[0][1], old + new)
                    check('cover_fixed_pixels_approved', cover_metrics['identical'], cover_metrics, category='strict_approved_appearance')
                    inventory['approved_rgb_comparison']['cover_outside_title'] = cover_metrics
        if args.baseline_dir:
            warnings.append('Runtime comparison baseline is supplementary only; strict approved equality is still evaluated against original approved PNGs.')
        if not args.psd_audit_only:
          check('photopea_reopen_report_present', bool(args.reopen_report) and resolve(args.reopen_report).is_file())
        if args.reopen_report and resolve(args.reopen_report).is_file():
            reopened = json.loads(resolve(args.reopen_report).read_text(encoding='utf-8-sig'))
            check('reopen_psd_hash_matches', reopened.get('psd_sha256') == digest(psd_path), reopened.get('psd_sha256'))
            rp = reopened.get('pages', [])
            check('reopen_page_names', [x.get('name', x.get('group')) for x in rp] == [x.name for _, x in groups])
            for page in rp:
                check('reopen_actual_layer_inventory_' + str(page.get('name', page.get('group'))), isinstance(page.get('layers'), list) and bool(page['layers']))
            warnings.append('Reopen JSON is corroborative evidence. Independent PSD parsing and re-export PNG comparisons are also required.')
        if not args.psd_audit_only:
          check('reopen_png_folder_present', bool(args.reopen_png_dir) and resolve(args.reopen_png_dir).is_dir())
        if args.reopen_png_dir and resolve(args.reopen_png_dir).is_dir():
            reopened_pngs = sorted([(numbered(x.stem), x) for x in resolve(args.reopen_png_dir).glob('*.png') if numbered(x.stem) is not None], key=lambda x: x[0])
            check('reopen_png_count', len(reopened_pngs) == len(pngs))
            for (n, a), (m, b) in zip(pngs, reopened_pngs):
                check(f'reopen_png_pixels_{n}', n == m and image_equal(a, b))
        inventory['hashes'] = {str(x.relative_to(project)) if x.is_relative_to(project) else str(x): digest(x) for x in [manifest_path, psd_path, pdf_path] if x.is_file()}
        warnings.extend(['No automated check certifies photo realism, whitespace, glyph clipping inside text boxes, visual hierarchy, editorial completeness, or visible rasterized placeholder text.', 'Gotham names in PSD are necessary but do not prove that font files were loaded in Photopea; require font-load event evidence and visual comparison.'])
    try:
        run()
    except Exception as exc:
        check('validator_exception', False, {'type': type(exc).__name__, 'message': str(exc)})
    output = resolve(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    structural_failures = [x['check'] for x in checks if x['required'] and not x['passed'] and x['category'] != 'strict_approved_appearance']
    appearance_failures = [x['check'] for x in checks if x['required'] and not x['passed'] and x['category'] == 'strict_approved_appearance']
    result = {'timestamp': datetime.now(timezone.utc).isoformat(), 'validator_sha256': digest(__file__),
              'status': 'passed_artifact_checks' if not errors else 'failed', 'visual_approval': False,
              'scope': 'psd_and_available_proofs_only' if args.psd_audit_only else 'full_delivery',
              'compatible_source_inputs': args.compatible_source_inputs, 'deferred_checks': deferred,
              'structural_conformance': 'passed' if not structural_failures else 'failed', 'structural_failures': structural_failures,
              'strict_approved_appearance': 'failed' if appearance_failures else 'no_failure_recorded', 'appearance_failures': appearance_failures,
              'checks': checks, 'errors': errors, 'warnings': warnings, 'inventory': inventory}
    output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({'status': result['status'], 'passed': sum(x['passed'] for x in checks), 'failed': len(errors), 'report': str(output)}, ensure_ascii=False))
    return 0 if not errors else 1


if __name__ == '__main__':
    sys.exit(main())
