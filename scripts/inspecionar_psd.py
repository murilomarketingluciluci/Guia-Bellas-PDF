"""Read editable PSD evidence offline; requires psd-tools. Does not mutate PSD."""
from __future__ import annotations
import argparse
import json
from pathlib import Path
from psd_tools import PSDImage


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("psd", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    psd = PSDImage.open(args.psd)
    layers = []
    def walk(items, parents=()):
        for layer in items:
            path = parents + (layer.name,)
            item = {"path": "/".join(path), "kind": layer.kind, "visible": layer.is_visible(), "bounds_px": list(layer.bbox)}
            if layer.kind == "type":
                item["text"] = getattr(layer, "text", "")
                try:
                    fonts = layer.resource_dict.get("FontSet", [])
                    styles = []
                    style_runs = layer.engine_dict.get("StyleRun", {})
                    lengths = style_runs.get("RunLengthArray", [])
                    for run_index, run in enumerate(style_runs.get("RunArray", [])):
                        data = run.get("StyleSheet", {}).get("StyleSheetData", {})
                        index = data.get("Font")
                        font = fonts[index].get("Name") if index is not None and index < len(fonts) else None
                        font = getattr(font, "value", font)
                        styles.append({"font": font.decode("utf-8") if isinstance(font, bytes) else font,
                                       "run_length": int(lengths[run_index]) if run_index < len(lengths) else None,
                                       "font_size_layer": float(data.get("FontSize", 0)),
                                       "leading": str(data.get("Leading")), "tracking": str(data.get("Tracking")),
                                       "color": str(data.get("FillColor"))})
                    item["styles"] = styles
                    item["transform"] = [float(v) for v in getattr(layer, "transform", ())]
                except Exception as exc:
                    item["style_read_error"] = str(exc)
            layers.append(item)
            if layer.is_group():
                walk(layer, path)
    walk(psd)
    resolution = psd.image_resources.get_data(1005)
    resolution = {key: getattr(resolution, key) for key in ("horizontal", "vertical", "horizontal_unit", "vertical_unit", "width_unit", "height_unit")} if resolution else None
    if resolution:
        resolution["horizontal_ppi"] = resolution["horizontal"] / 65536
        resolution["vertical_ppi"] = resolution["vertical"] / 65536
    result = {"canvas": [psd.width, psd.height], "resolution": resolution,
              "note": "Tamanhos são valores de camada; interprete junto a transform/resolução, não apenas como pt visuais.", "layers": layers}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"{len(layers)} camadas registradas em {args.output}")


if __name__ == "__main__":
    main()
