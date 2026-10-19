"""Compara bytes das artes rastreadas; não escreve nas artes."""
from pathlib import Path
import hashlib
import json
import subprocess
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
BASELINE = HERE / "artes_antes.json"
extensions = {".psd", ".psb", ".png", ".jpg", ".jpeg", ".pdf", ".zip", ".bin"}
def digest(p):
    with p.open("rb") as f:
        return hashlib.file_digest(f, "sha256").hexdigest()
if sys.argv[1:] == ["--capture"]:
    if BASELINE.exists():
        raise SystemExit("Baseline já existe; não sobrescrever.")
    tracked = subprocess.check_output(["git", "ls-files", "-z"], cwd=ROOT).decode("utf-8").split("\0")
    data = {n:digest(ROOT / n) for n in tracked if Path(n).suffix.lower() in extensions}
    BASELINE.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Baseline: {len(data)} arquivos de arte rastreados.")
else:
    data = json.loads(BASELINE.read_text(encoding="utf-8"))
    changed = [n for n,sha in data.items() if not (ROOT/n).is_file() or digest(ROOT/n) != sha]
    result = {"files_checked":len(data), "changed":changed, "status":"failed" if changed else "passed"}
    (HERE / "preservacao_artes.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, ensure_ascii=True))
    raise SystemExit(bool(changed))
