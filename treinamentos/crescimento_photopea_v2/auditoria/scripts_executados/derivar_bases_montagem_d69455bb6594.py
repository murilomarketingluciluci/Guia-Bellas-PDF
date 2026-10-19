"""Derive compact reconstruction metadata. Reads pixels only for measurements.

Never writes/edits an image, PSD, mask, canvas or browser. All output is JSON.
"""
from __future__ import annotations
import argparse
from datetime import datetime, timezone
import hashlib
import json
import math
from pathlib import Path

import numpy as np
from PIL import Image


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def pixel_measurements(path):
    with Image.open(path) as image:
        if image.mode not in ('RGB', 'RGBA'):
            return {'path': str(path), 'mode': image.mode, 'status': 'not_sampled_no_conversion'}
        colors = image.getcolors(maxcolors=image.width * image.height)
        opaque = [(count, value) for count, value in colors if len(value) == 3 or value[3] == 255]
        opaque.sort(reverse=True)
        points = [(10, 10), (960, 10), (1910, 10), (10, 540), (960, 540), (1910, 540), (10, 1070), (960, 1070), (1910, 1070)]
        return {'mode': image.mode, 'size': list(image.size), 'sha256': digest(path),
                'top_opaque_rgb': [{'rgb': list(value[:3]), 'hex': '#' + ''.join(f'{v:02X}' for v in value[:3]), 'count': count} for count, value in opaque[:8]],
                'samples': [{'xy': [x, y], 'pixel': list(image.getpixel((x, y)))} for x, y in points if x < image.width and y < image.height]}


def stats(values):
    return {'min': int(values.min()), 'max': int(values.max()), 'mean': round(float(values.mean()), 4),
            'zero_fraction': round(float(np.mean(values == 0)), 6), 'white_fraction': round(float(np.mean(values == 255)), 6)}


def mask_metrics(project, record):
    mask = record['mask']
    cached = mask.get('user_cache', {})
    if cached.get('status') != 'extracted':
        return {'status': 'no_stored_mask_cache'}
    path = project / cached['path']
    with Image.open(path) as image:
        data = np.asarray(image)
        if data.ndim != 2:
            return {'status': 'unexpected_mode_no_conversion', 'mode': image.mode}
        mean_x, mean_y = data.mean(axis=0), data.mean(axis=1)
        gray_values = np.unique(data)
        profiles = {}
        fractions = [0, .1, .25, .5, .75, .9, 1]
        for axis, length in [('column', image.width), ('row', image.height)]:
            rows = []
            for fraction in fractions:
                index = round((length - 1) * fraction)
                values = data[:, index] if axis == 'column' else data[index, :]
                rows.append({'fraction': fraction, 'index': index, **stats(values)})
            profiles[axis] = rows
        x0, y0, x1, y1 = mask['bbox_px']
        doc_samples = []
        for y in (0, 108, 270, 540, 810, 972, 1079):
            row = []
            for x in (0, 192, 480, 960, 1440, 1728, 1919):
                inside = x0 <= x < x1 and y0 <= y < y1
                row.append({'x': x, 'value': int(data[y - y0, x - x0]) if inside else mask['background_color'],
                            'stored': inside})
            doc_samples.append({'y': y, 'samples': row})
        fraction_gray = float(np.mean((data > 0) & (data < 255)))
        range_x, range_y = float(np.ptp(mean_x)), float(np.ptp(mean_y))
        sampled_y_deltas = np.diff([row['mean'] for row in profiles['row']])
        reversal_y = bool(np.any(sampled_y_deltas > 5) and np.any(sampled_y_deltas < -5))
        return {'status': 'measured_read_only', 'source_layer_id': record['id'], 'asset': cached['path'],
                'sha256': digest(path), 'mode': image.mode, 'size': list(image.size), 'bbox_document_px': mask['bbox_px'],
                'offset_from_layer_top_left': [x0 - record['bbox_px'][0], y0 - record['bbox_px'][1]],
                'background_outside_stored_bbox': mask['background_color'], 'disabled': mask['disabled'],
                **stats(data), 'unique_gray_levels': len(gray_values), 'intermediate_fraction': round(fraction_gray, 6),
                'edges': {'left': stats(data[:, 0]), 'right': stats(data[:, -1]), 'top': stats(data[0, :]), 'bottom': stats(data[-1, :])},
                'profiles': profiles, 'document_sample_grid': doc_samples,
                'mean_profile_range': {'x': round(range_x, 4), 'y': round(range_y, 4)},
                'mean_adjacent_abs_delta': {'x': round(float(np.abs(np.diff(data.astype(np.int16), axis=1)).mean()), 6),
                                            'y': round(float(np.abs(np.diff(data.astype(np.int16), axis=0)).mean()), 6)},
                'classification': 'soft_grayscale_mask_with_intermediate_values' if fraction_gray > 0 else 'binary_or_constant_mask',
                'dominant_mean_variation_axis': 'x' if range_x > range_y else 'y',
                'sampled_row_mean_reversal_larger_than_5_gray_levels': reversal_y,
                'interpretation_limit': 'Intermediate grayscale proves soft masking, not a unique linear gradient formula. Use stored mask at its own document bbox; default outside is recorded. No mask was applied or resized.'}


def compact_text(node):
    source = node['text']
    a, b, c, d, tx, ty = source['transform_affine_xx_xy_yx_yy_tx_ty']
    sx, sy = math.hypot(a, b), math.hypot(c, d)
    paragraphs = source['engine_dict_source'].get('ParagraphRun', {})
    runs = []
    for run in source['styles']:
        style = run['style_sheet_data_source']
        size = float(style.get('FontSize', 0))
        auto = bool(style.get('AutoLeading', False))
        stored_leading = float(style.get('Leading', 0))
        runs.append({'start': run['start_utf16'], 'end': run['end_utf16_exclusive'], 'length': run['length_source'],
                     'text': run['substring_from_engine_utf16'], 'fontIndex': run['font_index_source'],
                     'font': (run['font_record_source'] or {}).get('Name'), 'storedSize': size,
                     'size': size * sy, 'sizeX': size * sx, 'tracking': style.get('Tracking'),
                     'trackingPx': size * sy * float(style.get('Tracking', 0)) / 1000,
                     'leading': None if auto else stored_leading * sy, 'storedLeading': stored_leading,
                     'autoLeading': auto, 'color': style.get('FillColor'), 'sourceStyle': style})
    return {'contents': source['contents'], 'engineText': source['engine_editor_text'], 'font': runs[0]['font'] if runs else None,
            'fonts': sorted(set(run['font'] for run in runs if run['font'])), 'runs': runs,
            'size': runs[0]['size'] if runs else None, 'tracking': runs[0]['tracking'] if runs else None,
            'leading': runs[0]['leading'] if runs else None,
            'visiblebbox': node['bbox_px'], 'baselineOrigin': [tx, ty], 'transform': [a, b, c, d, tx, ty],
            'transformScaleX': sx, 'transformScaleY': sy,
            'FontSet': source['resource_dict_source'].get('FontSet', []),
            'styles': [run['sourceStyle'] for run in runs], 'paragraphRuns': paragraphs,
            'runLengthsSource': [run['length'] for run in runs],
            'sizeFormula': 'size = stored FontSize * hypot(transform[2], transform[3]); source stored transforms are uniform for these four text objects.',
            'leadingNote': 'leading null means AutoLeading=true; storedLeading is retained and must not be imposed as the manual line height. Paragraph auto-leading parameters remain in paragraphRuns.',
            'sourceLayerId': node['id'], 'sourcePath': node['path']}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--project', type=Path, required=True)
    parser.add_argument('--approved-dir', type=Path, required=True)
    args = parser.parse_args()
    project, approved = args.project.resolve(), args.approved_dir.resolve()
    source_path = project / 'leitura/base_molde_extraida.json'
    source_hash = digest(source_path)
    source = json.loads(source_path.read_text(encoding='utf-8'))
    approved_samples = []
    for path in sorted(approved.glob('pagina_*.png')):
        approved_samples.append({'reference': 'exemplos/optima_final/pngs_aprovados/' + path.name, **pixel_measurements(path)})
    templates, shared, all_nodes, text_by_id = {}, [], {}, {}
    names = {'CAPA APROVADA': 'capa', 'TEMA CLARO VAZIO': 'claro', 'TEMA ESCURO VAZIO': 'escuro', 'AGRADECIMENTO APROVADO': 'agradecimento'}
    groups = []
    def leaves(node, ancestors=(), within_visible=True):
        all_nodes[node['id']] = node
        if node['is_group']:
            group = {key: node[key] for key in ('id', 'name', 'parent_path', 'opacity_0_255', 'fill_opacity_0_255', 'blend_mode_code', 'visible_local')}
            groups.append(group)
            result = []
            for child in node['children']:
                result.extend(leaves(child, ancestors + (group,), within_visible and node['visible_local']))
            return result
        item = {'id': node['id'], 'nome': node['name'], 'kind': node['kind'], 'sourcePath': node['path'],
                'assetcache': node.get('pixel_cache', {}).get('path'), 'cacheStatus': node.get('pixel_cache', {}).get('status'),
                'bbox': node['bbox_px'], 'opacity': node['opacity_percent'], 'opacity255': node['opacity_0_255'],
                'fillOpacity': None if node['fill_opacity_0_255'] is None else node['fill_opacity_0_255'] * 100 / 255,
                'blend': node['blend_mode_code'], 'visible': node['visible_local'], 'visibleWithinTemplate': within_visible and node['visible_local'],
                'clipping': node['clipping'], 'ancestorGroups': list(ancestors), 'mask': None,
                'sourceDescriptors': node['tagged_blocks_file']}
        if 'mask' in node:
            mask = node['mask']
            item['mask'] = {'asset': mask.get('user_cache', {}).get('path'), 'realAsset': mask.get('real_cache', {}).get('path'),
                            'bbox': mask['bbox_px'], 'background': mask['background_color'], 'disabled': mask['disabled'],
                            'sourceParameters': mask['stored_parameters']}
        if 'smart_object' in node:
            so = node['smart_object']
            item['smartObject'] = {'payload': so.get('payload', {}).get('path'), 'transformBox': so.get('transform_box'), 'sourceFilenameMetadata': so.get('original_filename_metadata')}
        if 'text' in node:
            item['text'] = compact_text(node)
            text_by_id[node['id']] = item['text']
        return [item]
    for root in source['tree']:
        template_name = next((value for name, value in names.items() if root['name'].startswith(name)), None)
        if template_name:
            # Exclude root visibility from within-template visibility: three source roots are intentionally hidden.
            child_leaves = []
            root_meta = {'id': root['id'], 'name': root['name'], 'opacity': root['opacity_percent'],
                         'fillOpacity': root['fill_opacity_0_255'] * 100 / 255 if root['fill_opacity_0_255'] is not None else None,
                         'blend': root['blend_mode_code'], 'sourceVisible': root['visible_local']}
            all_nodes[root['id']] = root
            for child in root['children']:
                child_leaves.extend(leaves(child))
            templates[template_name] = {'root': root_meta, 'order': 'bottom_to_top', 'layers': child_leaves}
        else:
            shared.extend(leaves(root))
    mask_details = {str(i): mask_metrics(project, all_nodes[i]) for i in (5, 6, 28)}
    raw_bg = []
    for i in (4, 20, 24, 27):
        node = all_nodes[i]
        raw_bg.append({'layer_id': i, 'name': node['name'], 'template_source': node['top_group'],
                       'asset': node['pixel_cache']['path'], **pixel_measurements(project / node['pixel_cache']['path'])})
    approved_counts = {sample['reference']: {color['hex']: color['count'] for color in sample['top_opaque_rgb']} for sample in approved_samples}
    result = {'schema_version': '1.0', 'timestamp': datetime.now(timezone.utc).isoformat(),
              'stage': 'metadata_only_no_reconstruction', 'source': 'leitura/base_molde_extraida.json', 'source_sha256': source_hash,
              'script_sha256': digest(__file__), 'canvas': source['canvas'], 'templates': templates, 'sharedBackground': shared,
              'title_exact_source': text_by_id[31],
              'sourcefixedlook': {'approvedLight': '#FBA9C3', 'approvedDark': '#BC718C', 'supportTextOnLight': '#B3718E',
                                  'measuredRawLight': next(x['top_opaque_rgb'][0]['hex'] for x in raw_bg if x['layer_id'] == 24),
                                  'measuredRawDark': next(x['top_opaque_rgb'][0]['hex'] for x in raw_bg if x['layer_id'] == 20),
                                  'confirmation': {'light_in_page_02_top_colors': approved_counts.get('exemplos/optima_final/pngs_aprovados/pagina_02.png', {}).get('#FBA9C3', 0),
                                                   'dark_in_page_03_top_colors': approved_counts.get('exemplos/optima_final/pngs_aprovados/pagina_03.png', {}).get('#BC718C', 0)},
                                  'approved_samples': approved_samples, 'raw_background_samples': raw_bg,
                                  'instruction_scope': 'Raw RGB observations and approved appearance targets only. No recoloring, assignment/conversion of profile, raster operation or Photopea change was performed by this script.',
                                  'sourceProfilePresent': bool(source['icc_profile']),
                                  'colorLimit': 'A target HEX does not define a proven conversion for photos or all pixels. Compare a reconstruction/export visually and by fixed regions; do not globally replace colors based on this JSON alone.'},
              'mask_details': mask_details,
              'units': {'bbox': 'document pixels [left,top,right,bottom]', 'opacity': 'percent 0..100', 'blend': 'PSD four-character code',
                        'text_size': 'stored FontSize times vertical affine scale, as explicitly requested; verify Photopea runtime behavior',
                        'tracking': 'source Photoshop thousandths of em', 'runs': 'UTF-16 code-unit intervals including source terminal CR sentinel'},
              'limitations': ['No image, mask, PSD or browser was edited. Pixel arrays were read only to compute statistics.',
                              'No mask, opacity, blend, clipping or effect was applied. Layer assets are separate stored caches; text remains separate editable metadata.',
                              'Nested group opacity/blend/masks must be respected; source descriptors contain vector/effect definitions.',
                              'The compact manifest excludes source root invisibility from visibleWithinTemplate so hidden templates can be reconstructed as visible pages.',
                              'Approved HEX samples confirm targets, not a completed or approved visual reconstruction.']}
    output = project / 'leitura/bases_montagem.json'
    output.write_text(json.dumps(result, ensure_ascii=False, separators=(',', ':')) + '\n', encoding='utf-8')
    assert digest(source_path) == source_hash
    print(json.dumps({'output': 'leitura/bases_montagem.json', 'bytes': output.stat().st_size,
                      'templates': {name: len(template['layers']) for name, template in templates.items()},
                      'approvedPaletteConfirmation': result['sourcefixedlook']['confirmation'],
                      'masks': {key: {field: value[field] for field in ('min', 'max', 'unique_gray_levels', 'intermediate_fraction', 'dominant_mean_variation_axis')} for key, value in mask_details.items()}}, ensure_ascii=True))


if __name__ == '__main__':
    main()
