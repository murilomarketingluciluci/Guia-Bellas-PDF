"""Inventário e detecção de padrões de credenciais sem imprimir seus valores."""
from pathlib import Path
import hashlib
import json
import re
import sys
import zipfile

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent
PATTERNS = {
    "github_token": re.compile(rb"\bgh[pousr]_[A-Za-z0-9]{30,255}\b|\bgithub_pat_[A-Za-z0-9_]{40,255}\b"),
    "openai_key": re.compile(rb"\bsk-(?:proj-|svcacct-)?[A-Za-z0-9_-]{32,255}\b"),
    "google_key": re.compile(rb"\bAIza[A-Za-z0-9_-]{35}\b"),
    "aws_key": re.compile(rb"\b(?:AKIA|ASIA)[A-Z0-9]{16}\b"),
    "private_key": re.compile(rb"-----BEGIN (?:RSA |EC |OPENSSH |DSA )?PRIVATE KEY-----"),
    "bearer": re.compile(rb"(?i)\bbearer[ \t]+[A-Za-z0-9_.+/=-]{24,}"),
    "credential_url": re.compile(rb"https?://[^\s/\"']+:[^\s/\"']+@"),
}
TEXT_EXTS = {".md", ".json", ".jsonl", ".py", ".jsx", ".js", ".cjs", ".txt", ".html", ".csv", ".log", ".ps1", ".yaml", ".yml", ".toml", ".ini", ".cfg", ".env"}
files = []
findings = []
scanned = 0
archives_scanned = 0
for p in sorted(ROOT.rglob("*")):
    if not p.is_file() or ".git" in p.relative_to(ROOT).parts:
        continue
    rel = p.relative_to(ROOT).as_posix()
    data = p.read_bytes()
    files.append({"path": rel, "bytes": len(data), "sha256": hashlib.sha256(data).hexdigest()})
    if p.suffix.lower() in TEXT_EXTS or p.name.startswith(".env"):
        scanned += 1
        for kind, pattern in PATTERNS.items():
            for match in pattern.finditer(data):
                findings.append({"path": rel, "line": data[:match.start()].count(b"\n") + 1, "kind": kind})
    if p.suffix.lower() == ".zip":
        with zipfile.ZipFile(p) as z:
            for name in z.namelist():
                if Path(name).suffix.lower() not in TEXT_EXTS:
                    continue
                archives_scanned += 1
                member = z.read(name)
                for kind, pattern in PATTERNS.items():
                    for match in pattern.finditer(member):
                        findings.append({"path": rel + "!" + name, "line": member[:match.start()].count(b"\n") + 1, "kind": kind})
    if p.name in {".env", "credentials.json", "id_rsa", "id_ed25519"} or p.suffix.lower() in {".pem", ".p12", ".pfx", ".key"}:
        findings.append({"path": rel, "kind": "sensitive_filename"})
report = {"files": len(files), "bytes": sum(f["bytes"] for f in files), "text_files_scanned": scanned, "archive_text_members_scanned": archives_scanned, "findings": findings, "limits": "Padrões conhecidos; não substitui auditoria manual nem examina conteúdo visual."}
(OUT / "inventario_publicacao.json").write_text(json.dumps(files, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
(OUT / "verificacao_credenciais.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps(report, ensure_ascii=True, indent=2))
sys.exit(2 if findings else 0)
