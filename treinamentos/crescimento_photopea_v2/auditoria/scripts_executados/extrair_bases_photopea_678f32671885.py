"""Read-only extraction of the approved template into individual source assets.

No composite(), PSD save(), rasterization, reconstruction or Photopea call.
Cached pixels are decoded without ICC conversion; opacity/blending/masks/effects
remain separate metadata. Embedded smart object bytes are written unchanged.
"""
from __future__ import annotations
import argparse
import base64
from collections import Counter
from collections.abc import Mapping
from datetime import datetime, timezone
from enum import Enum
import hashlib
import json
from pathlib import Path
import re
import struct
import unicodedata

import psd_tools
from psd_tools import PSDImage


def sha(path):
    h = hashlib.sha256()
    with Path(path).open('rb') as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b''):
            h.update(chunk)
    return h.hexdigest()


def plain(value):
    """Lossless scalar/container representation; unknown types remain explicit."""
    if value is None or isinstance(value, (str, int, float, bool)):
        return value
    if isinstance(value, bytes):
        return {'bytes_base64': base64.b64encode(value).decode('ascii'), 'length': len(value)}
    if isinstance(value, Enum):
        return {'enum': type(value).__name__, 'name': value.name, 'value': plain(value.value)}
    if isinstance(value, Mapping) or hasattr(value, 'items'):
        result = {}
        for key, item in value.items():
            if isinstance(key, bytes):
                key = 'bytes:' + key.hex()
            else:
                key = str(getattr(key, 'value', key))
            result[key] = plain(item)
        return result
    if isinstance(value, (list, tuple)) or type(value).__name__ in ('List', 'ListElement'):
        return [plain(item) for item in value]
    if hasattr(value, 'value'):
        return plain(value.value)
    if hasattr(value, '__attrs_attrs__'):
        return {item.name: plain(getattr(value, item.name)) for item in value.__attrs_attrs__}
    return {'unconverted_class': type(value).__name__, 'repr': repr(value)}


def slug(name):
    clean = unicodedata.normalize('NFKD', name).encode('ascii', 'ignore').decode()
    return re.sub(r'[^A-Za-z0-9_-]+', '_', clean).strip('_')[:65] or 'layer'


def extension(data, filename):
    if data[:4] == b'8BPS' and len(data) >= 6:
        return '.psb' if struct.unpack('>H', data[4:6])[0] == 2 else '.psd'
    if data.startswith(b'\x89PNG\r\n\x1a\n'):
        return '.png'
    if data.startswith(b'\xff\xd8'):
        return '.jpg'
    if data.startswith(b'%PDF'):
        return '.pdf'
    suffix = Path(filename).suffix.lower()
    return suffix if suffix in ('.ai', '.svg', '.tif', '.tiff', '.eps', '.ps', '.gif', '.webp') else '.bin'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--project', type=Path, required=True)
    parser.add_argument('--source', type=Path, required=True)
    args = parser.parse_args()
    project, source = args.project.resolve(), args.source.resolve()
    assets = project / 'assets/base_molde'
    output = project / 'leitura/base_molde_extraida.json'
    assets.mkdir(parents=True, exist_ok=True)
    before = sha(source)
    psd = PSDImage.open(source)
    errors, warnings, records, files = [], [], [], []
    def relative(path):
        return str(path.relative_to(project)).replace('\\', '/')
    def save_bytes(path, data, origin):
        path.write_bytes(data)
        info = {'path': relative(path), 'bytes': len(data), 'sha256': sha(path), 'origin': origin}
        files.append(info)
        return info
    icc = psd.image_resources.get_data(1039)
    profile = save_bytes(assets / 'document_profile.icc', icc, 'source.image_resources[1039] exact bytes') if isinstance(icc, bytes) else None
    resolution = psd.image_resources.get_data(1005)
    def cache(layer, folder, stem):
        result = {'method': 'layer.topil(apply_icc=False)', 'applies_layer_opacity_blend_effects_or_user_mask': False,
                  'icc_conversion': False, 'source_depth': psd.depth}
        try:
            image = layer.topil(apply_icc=False)
            if image is None:
                result.update(status='absent', reason='No stored PIL-compatible pixels returned by topil; no synthetic render attempted.')
                return result
            result.update(source_mode=image.mode, size=list(image.size))
            if image.mode not in ('RGB', 'RGBA', 'L', 'LA', 'P', '1', 'I', 'I;16'):
                result.update(status='unsupported_mode', reason='Conversion to RGB would alter source values; not performed.')
                return result
            path = folder / (stem + '.cache.png')
            image.save(path, format='PNG')
            info = {'path': relative(path), 'bytes': path.stat().st_size, 'sha256': sha(path),
                    'origin': 'Stored per-layer channels decoded to PNG, not a page composite'}
            files.append(info)
            result.update(status='extracted', **info)
            if psd.depth != 8:
                result['precision_limitation'] = 'Pillow may reduce 16/32-bit RGB cache to 8-bit; source depth is recorded.'
            return result
        except Exception as exc:
            result.update(status='error', error=type(exc).__name__ + ': ' + str(exc))
            errors.append({'layer': layer.name, 'operation': 'cached_pixels', 'error': result['error']})
            return result
    def walk(container, parent_path=(), ancestor_visible=True, group_name=None):
        nodes = []
        siblings = list(container)
        for order, layer in enumerate(siblings):
            index = len(records) + 1
            stem = f'{index:03d}_{slug(layer.name)}'
            top_group = group_name or layer.name
            folder = assets / slug(top_group)
            folder.mkdir(parents=True, exist_ok=True)
            path = parent_path + (layer.name,)
            local_visible = bool(layer.visible)
            record = {'id': index, 'path': '/'.join(path), 'parent_path': '/'.join(parent_path),
                      'name': layer.name, 'top_group': top_group, 'kind': layer.kind,
                      'is_group': layer.is_group(), 'sibling_index_bottom_to_top': order,
                      'sibling_index_top_to_bottom': len(siblings) - order - 1,
                      'layer_id_source': layer.layer_id, 'visible_local': local_visible,
                      'visible_with_source_ancestors': ancestor_visible and local_visible,
                      'opacity_0_255': layer.opacity, 'opacity_percent': 100 * layer.opacity / 255,
                      'blend_mode': plain(layer.blend_mode), 'bbox_px': list(layer.bbox),
                      'raw_record_bbox_px': [layer._record.left, layer._record.top, layer._record.right, layer._record.bottom],
                      'clipping': bool(layer.clipping), 'fill_opacity_0_255': getattr(layer, 'fill_opacity', None),
                      'source_channel_ids': [int(x.id) for x in layer._record.channel_info],
                      'tagged_block_keys': [getattr(x, 'name', str(x)) for x in layer.tagged_blocks.keys()]}
            records.append(record)
            nodes.append(record)
            # Preserve layer-specific descriptors as serialized source semantics.
            # These are NOT claimed to be original raw byte offsets from the PSD.
            block_entries = []
            for key, block in layer.tagged_blocks.items():
                keybytes = getattr(key, 'value', key)
                tag = keybytes.decode('ascii', 'replace') if isinstance(keybytes, bytes) else str(keybytes)
                entry = {'key': tag, 'parsed': plain(block.data)}
                if hasattr(block.data, 'tobytes'):
                    try:
                        raw = block.data.tobytes()
                        entry['serialized_semantics'] = save_bytes(folder / (stem + '.tag_' + slug(tag) + '.bin'), raw,
                            'psd-tools serialization of parsed layer descriptor; not claimed original raw bytes')
                    except Exception as exc:
                        entry['serialization_error'] = type(exc).__name__ + ': ' + str(exc)
                block_entries.append(entry)
            metadata_path = folder / (stem + '.tagged_blocks.json')
            save_bytes(metadata_path, (json.dumps(block_entries, ensure_ascii=False, indent=2) + '\n').encode('utf-8'), 'Parsed per-layer source tagged blocks')
            record['tagged_blocks_file'] = relative(metadata_path)
            if not layer.is_group():
                record['pixel_cache'] = cache(layer, folder, stem)
            if layer.has_mask():
                mask = layer.mask
                record['mask'] = {'bbox_px': list(mask.bbox), 'background_color': mask.background_color,
                                  'disabled': mask.disabled, 'has_real': mask.has_real(), 'stored_parameters': plain(mask._data)}
                for real in (False, True):
                    if real and not mask.has_real():
                        continue
                    label = 'real' if real else 'user'
                    try:
                        image = mask.topil(real=real, layer_sized=False, apply_icc=False)
                        if image is None:
                            record['mask'][label + '_cache'] = {'status': 'absent'}
                        else:
                            image_path = folder / (stem + '.mask_' + label + '.png')
                            image.save(image_path, format='PNG')
                            info = {'status': 'extracted', 'path': relative(image_path), 'size': list(image.size),
                                    'sha256': sha(image_path), 'origin': 'Stored mask channel without resizing or applying it'}
                            files.append(info)
                            record['mask'][label + '_cache'] = info
                    except Exception as exc:
                        record['mask'][label + '_cache'] = {'status': 'error', 'error': str(exc)}
                        errors.append({'layer': record['path'], 'operation': 'mask_' + label, 'error': str(exc)})
            if layer.kind == 'smartobject':
                try:
                    smart = layer.smart_object
                    so = {'kind': smart.kind, 'original_filename_metadata': smart.filename,
                          'filetype_source': smart.filetype, 'unique_id': smart.unique_id,
                          'transform_box': plain(smart.transform_box), 'warp': plain(smart.warp),
                          'resolution_source': smart.resolution}
                    if smart.kind == 'data':
                        payload = smart.data
                        so['payload'] = save_bytes(folder / (stem + '.embedded' + extension(payload, smart.filename)), payload,
                                                   'Exact embedded SmartObject.data bytes; no PSD save or conversion')
                    else:
                        so['payload'] = {'status': 'not_embedded', 'reason': 'No external file read; source link metadata only.'}
                        warnings.append({'layer': record['path'], 'reason': 'Smart object is not embedded; original payload unavailable inside source.'})
                    record['smart_object'] = so
                except Exception as exc:
                    record['smart_object'] = {'status': 'error', 'error': str(exc)}
                    errors.append({'layer': record['path'], 'operation': 'smartobject', 'error': str(exc)})
            if layer.kind == 'type':
                fonts = layer.resource_dict.get('FontSet', [])
                engine_text = str(getattr(layer.engine_dict.get('Editor', {}).get('Text', ''), 'value', ''))
                runs = layer.engine_dict.get('StyleRun', {})
                lengths = runs.get('RunLengthArray', [])
                styles, start = [], 0
                utf16 = engine_text.encode('utf-16-le', 'surrogatepass')
                for ri, run in enumerate(runs.get('RunArray', [])):
                    length = int(lengths[ri]) if ri < len(lengths) else 0
                    data = run.get('StyleSheet', {}).get('StyleSheetData', {})
                    font_index = int(data['Font']) if data.get('Font') is not None else None
                    font_record = fonts[font_index] if font_index is not None and 0 <= font_index < len(fonts) else None
                    styles.append({'run_index': ri, 'start_utf16': start, 'end_utf16_exclusive': start + length,
                                   'length_source': length, 'substring_from_engine_utf16': utf16[start * 2:(start + length) * 2].decode('utf-16-le', 'replace'),
                                   'font_index_source': font_index, 'font_record_source': plain(font_record),
                                   'style_sheet_data_source': plain(data)})
                    start += length
                record['text'] = {'contents': layer.text, 'engine_editor_text': engine_text,
                                  'engine_utf16_length': len(utf16) // 2, 'style_run_length_sum': start,
                                  'text_type': plain(layer.text_type), 'transform_affine_xx_xy_yx_yy_tx_ty': list(layer.transform),
                                  'styles': styles, 'engine_dict_source': plain(layer.engine_dict),
                                  'resource_dict_source': plain(layer.resource_dict),
                                  'document_resources_source': plain(layer.document_resources), 'warp_source': plain(layer.warp),
                                  'provenance': 'All values read from original TypeToolObjectSetting/EngineData; font sizes are stored PSD units, not inferred visual pixels.',
                                  'indices_note': 'RunLengthArray and font indices retained as stored; UTF-16 substrings are decoded for inspection. Terminal carriage-return sentinel may be present.'}
            if layer.is_group():
                record['children'] = walk(layer, path, ancestor_visible and local_visible, top_group)
        return nodes
    tree = walk(psd)
    after = sha(source)
    caches = Counter(record.get('pixel_cache', {}).get('status', 'group_no_cache_attempt') for record in records)
    result = {'schema_version': '1.0', 'timestamp': datetime.now(timezone.utc).isoformat(),
              'stage': 'source_asset_preparation_only', 'source_reference_repo_relative': 'referencias/' + source.name,
              'source_sha256_before': before, 'source_sha256_after': after, 'source_unchanged': before == after,
              'script_sha256': sha(__file__), 'psd_tools_version': psd_tools.__version__,
              'canvas': [psd.width, psd.height], 'color_mode_source': plain(psd.color_mode), 'depth': psd.depth,
              'resolution_source': plain(resolution), 'icc_profile': profile,
              'order_note': 'psd-tools iteration order is bottom-to-top, as verified in installed GroupMixin.append documentation; sibling indices are zero-based.',
              'tree': tree, 'layer_count_including_groups': len(records), 'pixel_cache_status_counts': dict(caches),
              'files': files, 'errors': errors, 'warnings': warnings,
              'limitations': ['No whole-page composite or flattened page was created.',
                              'PNG caches contain stored per-layer pixels only; layer opacity, group opacity, blend mode, clipping, masks, effects and vector geometry must be reconstructed separately.',
                              'Missing cache pixels are reported. Vector rasterization or replacement pixels were not invented.',
                              'Smart object embedded payload bytes are exact; per-layer tagged-block binary sidecars are psd-tools serializations of parsed semantics, not certified original byte ranges.',
                              'Editable text remains separate as contents, EngineDict, FontSet, style runs and transform; conversion into Photopea totalTextStyle is not performed.',
                              'No reconstruction/import test has been executed by this extraction; compatibility and visual fidelity remain to be tested in Photopea.']}
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({'manifest': relative(output), 'source_unchanged': before == after, 'layers': len(records),
                      'cache_status': dict(caches), 'files': len(files), 'errors': len(errors), 'warnings': len(warnings)}, ensure_ascii=False))
    return 0 if before == after and not errors else 1


if __name__ == '__main__':
    raise SystemExit(main())
