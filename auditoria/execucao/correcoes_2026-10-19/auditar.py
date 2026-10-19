"""Registra comandos e preserva as versões Python efetivamente executadas."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import os
import subprocess
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
command = sys.argv[1:]
if not command:
    raise SystemExit("Informe um comando sem credenciais.")
action = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
versions = HERE / "scripts_executados"
versions.mkdir(exist_ok=True)
snapshots = []
for arg in command:
    candidate = ROOT / arg
    if candidate.is_file() and candidate.suffix in {".py", ".ps1"}:
        data = candidate.read_bytes()
        sha = hashlib.sha256(data).hexdigest()
        saved = versions / (candidate.stem + "_" + sha[:12] + candidate.suffix)
        if not saved.exists():
            saved.write_bytes(data)
        origin = candidate.relative_to(ROOT).as_posix() if candidate.is_relative_to(ROOT) else str(candidate)
        snapshots.append({"source":origin, "sha256":sha, "snapshot":saved.relative_to(ROOT).as_posix()})
base = {"action_id":action, "agent":"principal", "tool":"subprocess", "parameters_exact":{"argv":command}, "script_versions":snapshots}
def log(event, **fields):
    with (HERE / "principal.jsonl").open("a", encoding="utf-8") as handle:
        handle.write(json.dumps({**base, "event":event, "timestamp":datetime.now(timezone.utc).isoformat(), **fields}, ensure_ascii=False) + "\n")
log("started", status="running")
result = subprocess.run(command, cwd=ROOT, capture_output=True, text=True, encoding="utf-8", errors="replace", env={**os.environ, "PYTHONIOENCODING":"utf-8"})
log("result", status="succeeded" if result.returncode == 0 else "failed", exit_code=result.returncode, stdout=result.stdout, stderr=result.stderr)
sys.stdout.reconfigure(encoding="utf-8")
print(result.stdout, end="")
print(result.stderr, end="", file=sys.stderr)
raise SystemExit(result.returncode)
