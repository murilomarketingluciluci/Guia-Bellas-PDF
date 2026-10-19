"""Validate planning/final Bellas manifests without opening Photoshop."""
from __future__ import annotations
import argparse
import json
import math
import re
from pathlib import Path

ROLES = {"h1", "body", "bullet", "card", "callout", "photo", "line", "quote", "chart"}
TEXT_ROLES = ROLES - {"photo", "line", "chart"}
TEMP_LABEL = re.compile(r"(?:^|\n)\s*(?:H1\b|BLOCO\s*\d*\b|ITEM\s*\d*\b|BULLET\s*\d*\b|PLACEHOLDER\b)", re.I)
APPROVED_TEMPLATE = (Path(__file__).resolve().parents[1] / "referencias" / "molde_bellas_aprovado_capa_temas_agradecimento.psd").resolve()


def relative_asset(base: Path, value: object, label: str, problems: list[str]) -> None:
    if not isinstance(value, str) or not value.strip():
        problems.append(label + ": caminho ausente")
        return
    if Path(value).is_absolute() or re.match(r"^[A-Za-z]:", value):
        problems.append(label + ": use caminho relativo ao manifesto")
    if not (base / value).is_file():
        problems.append(label + ": arquivo ausente: " + value)


def validate(path: Path, requested_stage: str | None = None, require_approved_template: bool = False) -> list[str]:
    data = json.loads(path.read_text(encoding="utf-8-sig"))
    problems: list[str] = []
    stage = requested_stage or data.get("stage", "planejamento")
    if stage not in {"planejamento", "final"}:
        problems.append("stage deve ser planejamento ou final")
    if requested_stage == "final" and data.get("stage") != "final":
        problems.append("manifesto final deve declarar stage: final")
    canvas = data.get("canvas")
    valid_canvas = isinstance(canvas, list) and len(canvas) == 2 and all(isinstance(v, (int, float)) and not isinstance(v, bool) and math.isfinite(v) and v > 0 for v in canvas)
    if not valid_canvas or abs(canvas[0] / canvas[1] - 16 / 9) > 0.001:
        problems.append("canvas deve ser [largura, altura] 16:9")
    template = data.get("template", {})
    if template.get("psd"):
        relative_asset(path.parent, template["psd"], "template.psd", problems)
    else:
        problems.append("template.psd ausente")
    if require_approved_template:
        selected = (path.parent / template["psd"]).resolve() if isinstance(template.get("psd"), str) else None
        if selected != APPROVED_TEMPLATE:
            problems.append("template.psd deve ser exclusivamente o molde aprovado de capa, dois temas vazios e agradecimento")
        if template.get("approved_psd"):
            problems.append("template.approved_psd sugere outro PSD doador; use somente os PNGs Optima como referência visual")
    slides = data.get("slides")
    if not isinstance(slides, list) or not slides:
        return problems + ["slides deve ser lista não vazia"]
    themes = set()
    for index, slide in enumerate(slides, 1):
        prefix = f"slide {index}"
        if not isinstance(slide, dict):
            problems.append(prefix + ": objeto esperado")
            continue
        if slide.get("number") != index:
            problems.append(prefix + ": number deve seguir sequência 1..N")
        theme = slide.get("theme")
        if theme not in {"claro", "escuro"}:
            problems.append(prefix + ": theme deve ser claro ou escuro")
        else:
            themes.add(theme)
        elements = slide.get("elements")
        if not isinstance(elements, list) or not elements:
            problems.append(prefix + ": elements deve ser lista não vazia")
            continue
        h1_count = 0
        for j, el in enumerate(elements, 1):
            label = prefix + f", elemento {j}"
            if not isinstance(el, dict):
                problems.append(label + ": objeto esperado")
                continue
            role = el.get("role")
            if role not in ROLES:
                problems.append(label + ": role desconhecido")
            h1_count += role == "h1"
            rect = el.get("rect")
            if not isinstance(rect, list) or len(rect) != 4 or not all(isinstance(v, (float, int)) and not isinstance(v, bool) and math.isfinite(v) for v in rect):
                problems.append(label + ": rect deve ser [x,y,w,h] finito")
                continue
            x, y, w, h = rect
            if min(x, y) < 0 or w <= 0 or h <= 0 or x + w > 1.000001 or y + h > 1.000001:
                problems.append(label + ": retângulo fora da tela")
            if role == "photo":
                if not (abs(y) < 1e-6 and abs(h - 1) < 1e-6 and (abs(x) < 1e-6 or abs(x + w - 1) < 1e-6)):
                    problems.append(label + ": foto deve preencher altura tocando uma lateral")
                relative_asset(path.parent, el.get("asset"), label + ".asset", problems)
                if el.get("fit") != "cover":
                    problems.append(label + ": foto exige fit: cover")
                if index == 1:
                    problems.append("slide 1: capa não pode conter foto")
            elif role in TEXT_ROLES:
                value = el.get("text") if stage == "final" else el.get("placeholder", el.get("text"))
                if not isinstance(value, str) or not value.strip():
                    problems.append(label + (": text real ausente" if stage == "final" else ": texto/placeholder ausente"))
                elif stage == "final" and TEMP_LABEL.search(value):
                    problems.append(label + ": rótulo de planejamento em texto final")
            if stage == "final" and "placeholder" in el:
                problems.append(label + ": campo placeholder proibido no final")
        if h1_count != 1:
            problems.append(prefix + ": deve ter exatamente um H1")
    if len(slides) > 1 and themes != {"claro", "escuro"}:
        problems.append("apresentação deve alternar temas claro e escuro")
    return problems


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("manifest", type=Path)
    parser.add_argument("--stage", choices=["planejamento", "final"])
    parser.add_argument("--require-approved-template", action="store_true",
                        help="Para novos treinamentos: recusar PSD de partida/doador diferente do molde consolidado")
    args = parser.parse_args()
    try:
        problems = validate(args.manifest.resolve(), args.stage, args.require_approved_template)
    except (ValueError, OSError, TypeError) as exc:
        print("Manifest inválido:", exc)
        return 1
    if problems:
        print("Manifest inválido:\n" + "\n".join("- " + p for p in problems))
        return 1
    print("Manifest válido. A prova visual e a revisão editorial ainda são necessárias.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
