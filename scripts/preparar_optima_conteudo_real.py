"""Replace layout placeholders with the complete supplied Optima content.

Creates a content-ready manifest; does not certify fit or execute Photoshop.
"""
from __future__ import annotations
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    source = (ROOT / "referencias/optima_conteudo_extraido.txt").read_text(encoding="utf-8-sig")
    manifest = json.loads((ROOT / "exemplos/optima_manifest_placeholders.json").read_text(encoding="utf-8-sig"))
    chunks = re.split(r"--- PAGE (\d+) ---", source)
    pages = {int(chunks[i]): chunks[i + 1].strip() for i in range(1, len(chunks), 2)}
    manifest.update(project="Optima - conteúdo real integral para produção Bellas", stage="final", production_status="conteudo_preparado_layout_a_validar_no_photoshop",
                    source="../referencias/optima_conteudo_original.pdf",
                    note="Textos preservados da fonte da palestrante. Alegações não comprovadas pelo repositório. Este manifesto não é prova de arte final executada.")
    for slide in manifest["slides"]:
        number = slide["number"]
        parts = pages[number].split("•")
        content = [re.sub(r"\s+", " ", part).strip() for part in parts]
        if number == 5:
            tail = "EVITAR DESODORANTES COM ALUMÍNIO EM AEROSOL"
            assert content[-1].endswith(tail)
            content[-1] = content[-1][:-len(tail)].strip()
            content.append(tail)
        # Preserve the hyphenated product term broken by PDF line wrap.
        content = [text.replace("TRANS- RESVERATROL", "TRANS-RESVERATROL") for text in content]
        texts = [element for element in slide["elements"] if element["role"] != "photo"]
        if len(texts) != len(content):
            raise ValueError(f"Página {number}: {len(content)} trechos para {len(texts)} caixas")
        for index, (element, text) in enumerate(zip(texts, content)):
            element.pop("placeholder", None)
            element["text"] = text
            element["source"] = {"file": "../referencias/optima_conteudo_original.pdf", "page": number, "block": index}
        for element in slide["elements"]:
            if element["role"] == "photo":
                element["asset"] = {4: "assets/foto_04_730x1080_v2.png", 6: "assets/foto_06_700x1080_v2.png", 7: "assets/foto_07_680x1080_v2.png"}[number]
    output = ROOT / "exemplos/optima_manifest_conteudo_real.json"
    output.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Conteúdo real de {len(pages)} páginas preparado; produção e prova visual ainda pendentes.")


if __name__ == "__main__":
    main()
