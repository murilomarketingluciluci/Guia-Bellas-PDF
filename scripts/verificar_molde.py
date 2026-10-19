"""Confere o único molde editável de partida Bellas, sem abrir Photoshop."""
from __future__ import annotations

import argparse
import hashlib
from pathlib import Path

from psd_tools import PSDImage


ROOT = Path(__file__).resolve().parents[1]
APPROVED = ROOT / "referencias" / "molde_bellas_aprovado_capa_temas_agradecimento.psd"
GROUPS = {
    "CAPA APROVADA - ALTERAR SOMENTE TITULO",
    "TEMA CLARO VAZIO - DUPLICAR",
    "TEMA ESCURO VAZIO - DUPLICAR",
    "AGRADECIMENTO APROVADO - ULTIMA PAGINA",
}


def descendants(group):
    for layer in group:
        yield layer
        if layer.is_group():
            yield from descendants(layer)


def validate(path: Path) -> list[str]:
    problems: list[str] = []
    if not path.is_file():
        return [f"molde ausente: {path}"]
    psd = PSDImage.open(path)
    if (psd.width, psd.height) != (1920, 1080):
        problems.append(f"canvas inesperado: {psd.width}x{psd.height}")
    groups = [layer for layer in psd if layer.is_group()]
    names = {layer.name for layer in groups}
    if len(groups) != 4 or names != GROUPS:
        problems.append(f"esperados exatamente os quatro grupos aprovados; encontrados: {sorted(names)}")
        return problems
    for group in groups:
        texts = [layer for layer in descendants(group) if layer.kind == "type"]
        if "VAZIO" in group.name and texts:
            problems.append(f"{group.name}: grupo vazio contém {len(texts)} camadas de texto")
    cover = next(group for group in groups if group.name.startswith("CAPA APROVADA"))
    if not any(layer.kind == "type" and "Desodorante" in str(layer.text)
               for layer in descendants(cover)):
        problems.append("capa aprovada: título editável original não localizado")
    thanks = next(group for group in groups if group.name.startswith("AGRADECIMENTO"))
    if not any(layer.kind == "type" and "obrigada" in str(layer.text).lower()
               for layer in descendants(thanks)):
        problems.append("agradecimento aprovado: texto não localizado")
    return problems


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--path", type=Path, default=APPROVED,
                        help="Cópia do molde a conferir; padrão: molde aprovado do repositório")
    args = parser.parse_args()
    path = args.path.resolve()
    try:
        problems = validate(path)
    except Exception as exc:
        print(f"Falha ao ler o PSD: {exc}")
        return 1
    if problems:
        print("Molde inválido:\n" + "\n".join("- " + p for p in problems))
        return 1
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    print(f"Molde aprovado: capa, dois temas vazios e agradecimento; 1920x1080. SHA-256 {digest}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
