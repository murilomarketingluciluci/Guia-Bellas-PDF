"""Create a portable distributable ZIP and a SHA-256 file inventory."""
from __future__ import annotations
import hashlib
import json
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXCLUDED_SUFFIXES = {".otf", ".ttf", ".ttc", ".woff", ".woff2"}


def digest(path: Path) -> str:
    with path.open("rb") as file:
        return hashlib.file_digest(file, "sha256").hexdigest()


def main() -> None:
    files = [p for p in ROOT.rglob("*") if p.is_file()
             and "__pycache__" not in p.parts
             and p.name != "inventario_sha256.json"
             and p.suffix.lower() not in EXCLUDED_SUFFIXES]
    inventory = [{"path": p.relative_to(ROOT).as_posix(), "bytes": p.stat().st_size,
                  "sha256": digest(p)} for p in sorted(files)]
    inventory_file = ROOT / "inventario_sha256.json"
    inventory_file.write_text(json.dumps({"files": inventory}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    output = ROOT.parent / "Guia_Bellas_IA.zip"
    with zipfile.ZipFile(output, "w", zipfile.ZIP_DEFLATED, compresslevel=6) as archive:
        for path in sorted(files + [inventory_file]):
            archive.write(path, ROOT.name + "/" + path.relative_to(ROOT).as_posix())
    with zipfile.ZipFile(output) as archive:
        if archive.testzip() is not None:
            raise RuntimeError("Falha de integridade ZIP")
        expected = {ROOT.name + "/" + item["path"] for item in inventory}
        actual = set(archive.namelist()) - {ROOT.name + "/inventario_sha256.json"}
        if actual != expected:
            raise RuntimeError("Inventário e entradas do ZIP divergem")
    print(f"ZIP validado: {output} ({output.stat().st_size} bytes; {len(files)+1} arquivos)")


if __name__ == "__main__":
    main()
