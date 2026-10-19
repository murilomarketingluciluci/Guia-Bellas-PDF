"""Explicit, read-only compatibility rules for the Photopea input conversion."""
from pathlib import Path
import hashlib
import json
from PIL import Image
from psd_tools import PSDImage


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def channel_records(layer):
    return [{'id': int(info.id), 'compression': int(data.compression), 'compressed_bytes': len(data.data),
             'compressed_sha256': hashlib.sha256(data.data).hexdigest()} for info, data in zip(layer._record.channel_info, layer._channels)]


def equal_pixels(left, right):
    return left is not None and right is not None and left.mode == right.mode and left.size == right.size and left.tobytes() == right.tobytes()


def validate_compatible_inputs(project, template, groups, check, inventory):
    """The flag authorizes SO/shape/fill->pixel input conversion, not visual approval."""
    metadata_file = project / 'leitura/inputs_mascarados.json'
    extraction_file = project / 'leitura/base_molde_extraida.json'
    original_file = Path(__file__).resolve().parents[3] / 'referencias/molde_bellas_aprovado_capa_temas_agradecimento.psd'
    check('compatible_packaging_metadata_exists', metadata_file.is_file())
    check('compatible_extraction_metadata_exists', extraction_file.is_file())
    if not metadata_file.is_file() or not extraction_file.is_file():
        return
    metadata = json.loads(metadata_file.read_text(encoding='utf-8-sig'))
    extraction = json.loads(extraction_file.read_text(encoding='utf-8-sig'))
    check('compatible_original_hash_anchor', sha(original_file) == metadata['source_sha256_before'] == metadata['source_sha256_after'] == extraction['source_sha256_before'])
    script = project / 'scripts/preparar_inputs_mascarados.py'
    check('compatible_packaging_script_hash', script.is_file() and sha(script) == metadata.get('script_sha256'))
    source_rows = list(template.descendants())
    extracted_rows = {}
    def walk_rows(rows):
        for row in rows:
            extracted_rows[row['id']] = row
            walk_rows(row.get('children', []))
    walk_rows(extraction['tree'])
    # Corroborate all 23 original cache assets with actual PSD channels.
    for source_id, row in extracted_rows.items():
        cache = row.get('pixel_cache', {})
        if cache.get('status') == 'extracted':
            path = project / cache['path']
            check(f'compatible_cache_hash_{source_id}', path.is_file() and sha(path) == cache['sha256'])
            if path.is_file():
                with Image.open(path) as image:
                    check(f'compatible_cache_source_pixels_{source_id}', equal_pixels(source_rows[source_id - 1].topil(apply_icc=False), image))
    group_map = dict(groups)
    associations = []
    for product in metadata['products']:
        source_id = product['source_layer_id']
        if source_id not in (5, 6, 28):
            check('compatible_only_expected_packaged_ids', False, source_id)
            continue
        source = source_rows[source_id - 1]
        path = project / product['asset']
        check(f'compatible_input_hash_{source_id}', path.is_file() and sha(path) == product['sha256'], str(path))
        if not path.is_file():
            continue
        packed = PSDImage.open(path)
        check(f'compatible_input_one_pixel_layer_{source_id}', len(packed) == 1 and packed[0].kind == 'pixel')
        if len(packed) != 1:
            continue
        input_layer = packed[0]
        check(f'compatible_input_source_channels_{source_id}', channel_records(input_layer) == channel_records(source) == product['channels'])
        check(f'compatible_input_source_mask_record_{source_id}', input_layer.has_mask() and input_layer.mask._data.tobytes() == source.mask._data.tobytes())
        page = 1 if source_id == 28 else max(group_map)
        expected_name = f'FOTO FIXA ORIGINAL - {source_id}'
        candidates = [layer for layer in group_map[page].descendants() if layer.name == expected_name]
        check(f'compatible_native_input_unique_{source_id}', len(candidates) == 1, {'page': page, 'name': expected_name})
        if len(candidates) != 1:
            continue
        actual = candidates[0]
        check(f'compatible_native_kind_{source_id}', actual.kind == 'pixel', actual.kind)
        check(f'compatible_native_bbox_{source_id}', actual.bbox == source.bbox, {'expected': list(source.bbox), 'actual': list(actual.bbox)})
        check(f'compatible_native_opacity_{source_id}', actual.opacity == source.opacity, {'expected': source.opacity, 'actual': actual.opacity})
        check(f'compatible_native_fillopacity_{source_id}', actual.fill_opacity == source.fill_opacity, {'expected': source.fill_opacity, 'actual': actual.fill_opacity})
        check(f'compatible_native_blend_{source_id}', actual.blend_mode == source.blend_mode, {'expected': source.blend_mode.name, 'actual': actual.blend_mode.name})
        check(f'compatible_native_cache_pixels_{source_id}', equal_pixels(actual.topil(apply_icc=False), source.topil(apply_icc=False)))
        check(f'compatible_native_mask_present_{source_id}', actual.has_mask())
        if actual.has_mask():
            check(f'compatible_native_mask_bbox_{source_id}', actual.mask.bbox == source.mask.bbox, {'expected': list(source.mask.bbox), 'actual': list(actual.mask.bbox)})
            check(f'compatible_native_mask_background_{source_id}', actual.mask.background_color == source.mask.background_color)
            check(f'compatible_native_mask_disabled_{source_id}', actual.mask.disabled == source.mask.disabled)
            source_flags = source.mask._data.flags.tobytes()
            actual_flags = actual.mask._data.flags.tobytes()
            params = actual.mask._data.parameters
            param_values = {field: getattr(params, field) for field in ('user_mask_density', 'user_mask_feather', 'vector_mask_density', 'vector_mask_feather')} if params else None
            check(f'compatible_native_mask_flags_{source_id}', actual_flags == source_flags,
                  {'source_hex': source_flags.hex(), 'actual_hex': actual_flags.hex(), 'actual_parameters': param_values,
                   'policy': 'Binary diagnostic retained. Only 0x10 plus identity density255/feather0 is allowed by the separately required semantic check.'}, required=False)
            # Observed Photopea encoding: bit4 signals added MaskParameters.
            # Density255 is identity (share=255/255); feather0 adds no feather.
            neutral_added_params = source.mask._data.parameters is None and param_values == {
                'user_mask_density': 255, 'user_mask_feather': 0.0,
                'vector_mask_density': None, 'vector_mask_feather': None}
            effective_flags_same = (actual_flags == source_flags) or (
                len(source_flags) == len(actual_flags) == 1 and
                (actual_flags[0] ^ source_flags[0]) == 0x10 and neutral_added_params)
            check(f'compatible_native_mask_effective_flags_{source_id}', effective_flags_same,
                  {'exact_bytes': actual_flags == source_flags, 'only_neutral_0x10_extension': neutral_added_params,
                   'source_reference': 'Installed psd-tools1.25 composite.py _get_mask: share=density/255; shape=share*shape+(1-share). No compositor was called.'})
            check(f'compatible_native_mask_pixels_{source_id}', equal_pixels(actual.mask.topil(real=False, layer_sized=False, apply_icc=False), source.mask.topil(real=False, layer_sized=False, apply_icc=False)))
        associations.append({'source_id': source_id, 'page': page, 'native_layer': actual.name, 'input_sha256': product['sha256'], 'bbox': list(actual.bbox)})
    check('compatible_all_three_inputs_linked', {row['source_id'] for row in associations} == {5, 6, 28}, associations)
    inventory['compatible_inputs'] = {'metadata_sha256': sha(metadata_file), 'extraction_sha256': sha(extraction_file), 'associations': associations,
        'policy': 'Explicit --compatible-source-inputs authorizes pixel input caches instead of SO/shape/fill kinds. Exact approved PNG comparisons remain required and can fail independently.'}
