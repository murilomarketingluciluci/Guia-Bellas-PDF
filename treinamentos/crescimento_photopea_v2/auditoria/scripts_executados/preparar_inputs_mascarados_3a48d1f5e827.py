"""Package three source cached layers/masks into single-layer PSD input files.

Deep-copies existing compressed pixel/mask channels. Never composites, applies
masks, resizes, recolors or sharpens. Writes PSD records directly, bypassing
PSDImage.save() because that public method auto-renders a merged preview.
"""
from __future__ import annotations
import argparse
from copy import deepcopy
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path

import psd_tools
from psd_tools import PSDImage
from psd_tools.api.layers import PixelLayer
from psd_tools.constants import Compression, Resource, Tag
from psd_tools.psd.image_resources import ImageResource, VersionInfo


def digest_bytes(data):
    return hashlib.sha256(data).hexdigest()


def digest(path):
    h = hashlib.sha256()
    with Path(path).open('rb') as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b''):
            h.update(chunk)
    return h.hexdigest()


def channels(layer):
    return [{'id': int(info.id), 'compression': int(data.compression), 'compressed_bytes': len(data.data),
             'compressed_sha256': digest_bytes(data.data)} for info, data in zip(layer._record.channel_info, layer._channels)]


def flags(mask):
    value = mask._data.flags
    return {key: bool(getattr(value, key)) for key in ('pos_relative_to_layer', 'mask_disabled', 'invert_mask',
            'user_mask_from_render', 'parameters_applied', 'undocumented_1', 'undocumented_2', 'undocumented_3')}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--project', type=Path, required=True)
    parser.add_argument('--source', type=Path, required=True)
    args = parser.parse_args()
    project, source_path = args.project.resolve(), args.source.resolve()
    folder = project / 'assets/base_molde_compativel'
    folder.mkdir(parents=True, exist_ok=True)
    metadata_path = project / 'leitura/inputs_mascarados.json'
    original_hash = digest(source_path)
    source = PSDImage.open(source_path)
    assert (source.width, source.height, source.depth) == (1920, 1080, 8)
    source_rows = list(source.descendants())
    extracted = json.loads((project / 'leitura/base_molde_extraida.json').read_text(encoding='utf-8'))
    extracted_rows = {}
    def read_rows(nodes):
        for row in nodes:
            extracted_rows[row['id']] = row
            read_rows(row.get('children', []))
    read_rows(extracted['tree'])
    retain = {Tag.UNICODE_LAYER_NAME, Tag.LAYER_ID, Tag.BLEND_FILL_OPACITY,
              Tag.BLEND_CLIPPING_ELEMENTS, Tag.BLEND_INTERIOR_ELEMENTS,
              Tag.KNOCKOUT_SETTING, Tag.PROTECTED_SETTING, Tag.SHEET_COLOR_SETTING}
    products, all_checks = [], []
    for source_id in (5, 6, 28):
        original = source_rows[source_id - 1]
        row = extracted_rows[source_id]
        assert original.name == row['name'] and original.kind == 'smartobject'
        assert original.has_mask() and not original.mask.has_real()
        assert not original.has_vector_mask()
        assert [int(c.id) for c in original._record.channel_info] == [-1, 0, 1, 2, -2]
        # A transparent empty merged-data placeholder is metadata, never a render
        # of the layer. has_composite=False tells readers not to treat it as art.
        document = PSDImage.new('RGBA', (1920, 1080), color=(0, 0, 0, 0), depth=8, compression=Compression.RLE)
        for resource in (Resource.RESOLUTION_INFO, Resource.ICC_PROFILE):
            if resource in source.image_resources:
                document.image_resources[resource] = deepcopy(source.image_resources[resource])
        document.image_resources[Resource.VERSION_INFO] = ImageResource(
            key=Resource.VERSION_INFO,
            data=VersionInfo(has_composite=False, writer='psd-tools input layer packaging',
                             reader='Photopea intended; pending real import test'))
        copied_record = deepcopy(original._record)
        removed = []
        for key in list(copied_record.tagged_blocks):
            if key not in retain:
                removed.append({'tag': getattr(key, 'value', key).decode('ascii', 'replace'), 'name': getattr(key, 'name', None)})
                del copied_record.tagged_blocks[key]
        copied_record.flags.pixel_data_irrelevant = False
        # No conversion through PIL: compressed RGB, alpha and mask data stay exact.
        pixel_layer = PixelLayer(document, copied_record, deepcopy(original._channels))
        document.append(pixel_layer)
        document._update_record()
        layer_info = document._record._get_layer_info()
        layer_info.layer_count = -1  # Merged image's fourth channel is transparency.
        document._merged_alpha = True
        output = folder / f'camada_{source_id:03d}.psd'
        with output.open('wb') as stream:
            document._record.write(stream)
        # Reopen bytes from disk and verify unbaked caches/masks, not a render.
        reopened = PSDImage.open(output)
        actual = reopened[0]
        before_pixels, after_pixels = original.topil(apply_icc=False), actual.topil(apply_icc=False)
        before_mask = original.mask.topil(real=False, layer_sized=False, apply_icc=False)
        after_mask = actual.mask.topil(real=False, layer_sized=False, apply_icc=False)
        check_values = {
            'canvas_1920_1080': (reopened.width, reopened.height) == (1920, 1080),
            'one_pixel_layer': len(reopened) == 1 and actual.kind == 'pixel' and not actual.is_group(),
            'source_name_preserved': actual.name == original.name,
            'bbox_exact': actual.bbox == original.bbox,
            'opacity_exact': actual.opacity == original.opacity,
            'fill_opacity_exact': actual.fill_opacity == original.fill_opacity,
            'blend_exact': actual.blend_mode == original.blend_mode,
            'visible_local_exact': actual.visible == original.visible,
            'source_compressed_channels_exact': channels(actual) == channels(original),
            'pixel_cache_mode_size_exact': before_pixels.mode == after_pixels.mode and before_pixels.size == after_pixels.size,
            'pixel_cache_bytes_exact': before_pixels.tobytes() == after_pixels.tobytes(),
            'mask_present': actual.has_mask(),
            'mask_bbox_exact': actual.mask.bbox == original.mask.bbox,
            'mask_background_exact': actual.mask.background_color == original.mask.background_color,
            'mask_flags_exact': flags(actual.mask) == flags(original.mask),
            'mask_data_record_exact': actual.mask._data.tobytes() == original.mask._data.tobytes(),
            'mask_cache_mode_size_exact': before_mask.mode == after_mask.mode and before_mask.size == after_mask.size,
            'mask_cache_bytes_exact': before_mask.tobytes() == after_mask.tobytes(),
            'no_composite_claim': reopened.image_resources.get_data(Resource.VERSION_INFO).has_composite is False,
            'icc_exact_no_profile_assignment': reopened.image_resources.get_data(Resource.ICC_PROFILE) == source.image_resources.get_data(Resource.ICC_PROFILE),
        }
        preview_channels = reopened._record.image_data.get_data(reopened._record.header)
        check_values['merged_placeholder_alpha_zero'] = len(preview_channels) == 4 and set(preview_channels[3]) == {0}
        for name, passed in check_values.items():
            all_checks.append({'layer_id': source_id, 'test': name, 'passed': bool(passed)})
        source_channels = channels(original)
        products.append({'source_layer_id': source_id, 'source_path': row['path'], 'name': original.name,
                         'asset': str(output.relative_to(project)).replace('\\', '/'), 'bytes': output.stat().st_size,
                         'sha256': digest(output), 'canvas': [1920, 1080], 'kind': actual.kind,
                         'empty_preview_compression': reopened._record.image_data.compression.name,
                         'bbox': list(actual.bbox), 'opacity255': actual.opacity, 'opacity_percent': actual.opacity * 100 / 255,
                         'fillOpacity255': actual.fill_opacity, 'blend': actual.blend_mode.value.decode('ascii'),
                         'channels': source_channels, 'source_cache_reference': row['pixel_cache']['path'],
                         'source_embedded_payload_preserved_separately': row['smart_object']['payload']['path'],
                         'mask': {'bbox': list(actual.mask.bbox), 'background': actual.mask.background_color,
                                  'disabled': actual.mask.disabled, 'flags': flags(actual.mask),
                                  'size': list(after_mask.size), 'cache_raw_sha256': digest_bytes(after_mask.tobytes()),
                                  'offset_from_layer_top_left': [actual.mask.left - actual.left, actual.mask.top - actual.top],
                                  'source_mask_reference': row['mask']['user_cache']['path']},
                         'pixel_cache': {'mode': after_pixels.mode, 'size': list(after_pixels.size),
                                         'raw_bytes_sha256': digest_bytes(after_pixels.tobytes())},
                         'removed_source_tags': removed, 'checks_passed': sum(check_values.values()),
                         'checks_failed': sum(not passed for passed in check_values.values())})
    after_hash = digest(source_path)
    all_checks.append({'test': 'original_psd_unchanged', 'passed': after_hash == original_hash})
    result = {'schema_version': '1.0', 'timestamp': datetime.now(timezone.utc).isoformat(),
              'stage': 'technical_input_conversion_only', 'psd_tools_version': psd_tools.__version__,
              'script_sha256': digest(__file__), 'source_reference': 'referencias/' + source_path.name,
              'source_sha256_before': original_hash, 'source_sha256_after': after_hash,
              'source_unchanged': original_hash == after_hash, 'products': products, 'checks': all_checks,
              'passed': sum(check['passed'] for check in all_checks), 'failed': sum(not check['passed'] for check in all_checks),
              'method': 'Deep-copy original compressed channel data and mask record into one PixelLayer; strip SO-specific/nonessential metadata; write PSD record directly without PSDImage.save or composite.',
              'limitations': ['These are single-layer technical input documents, not final pages or an APN created outside Photopea.',
                              'Smart Object editability, embedded-original link, original transform/warp history and nonessential metadata are removed from these input copies; originals/payloads remain preserved in source assets.',
                              'RGB/alpha/mask compressed channels, layer bbox, mask bbox/background/flags, opacity/fillOpacity/blend are preserved exactly and checked after disk re-open.',
                              'Merged preview is an intentionally transparent placeholder, has_composite=false. Rendering/import compatibility in Photopea must be tested by the principal.',
                              'No color conversion, resampling, sharpening, crop, mask application or masked-pixel multiplication was performed.',
                              'No Photopea bridge/browser or final art was accessed by this script.']}
    metadata_path.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({'metadata': str(metadata_path.relative_to(project)).replace('\\', '/'),
                      'products': [{'id': item['source_layer_id'], 'bytes': item['bytes'], 'sha256': item['sha256']} for item in products],
                      'passed': result['passed'], 'failed': result['failed'], 'source_unchanged': result['source_unchanged']}, ensure_ascii=True))
    return 0 if result['failed'] == 0 else 1


if __name__ == '__main__':
    raise SystemExit(main())
