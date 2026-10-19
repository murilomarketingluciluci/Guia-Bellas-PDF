"""Empacota arquivos controlados, sem Git/credenciais; não sobrescreve inventários históricos."""
from __future__ import annotations
import hashlib
import json
import zipfile
import argparse
import os
import re
import stat
import subprocess
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXCLUDED_SUFFIXES = {".otf", ".ttf", ".ttc", ".woff", ".woff2"}
EXCLUDED_DIRS = {".git", ".hg", ".svn", "__pycache__", ".venv", "venv", "node_modules", ".pytest_cache", "dist"}
SECRET_NAMES = {"credentials.json", "secrets.json", "id_rsa", "id_ed25519", ".npmrc", ".pypirc", ".netrc"}
SECRET_SUFFIXES = {".pem", ".p12", ".pfx", ".key"}
SECRET_PATTERN = re.compile(rb"\bgh[pousr]_[A-Za-z0-9]{30,255}\b|\bgithub_pat_[A-Za-z0-9_]{40,255}\b|\bsk-(?:proj-|svcacct-)?[A-Za-z0-9_-]{32,255}\b|\bAIza[A-Za-z0-9_-]{35}\b|\b(?:AKIA|ASIA)[A-Z0-9]{16}\b|-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----|(?i:bearer)[ \t]+[A-Za-z0-9_.+/=-]{24,}|https?://[^\s/\"']+:[^\s/\"']+@")
TEXT_SUFFIXES = {".py", ".js", ".cjs", ".jsx", ".ps1", ".md", ".txt", ".json", ".jsonl", ".html", ".csv", ".toml", ".ini", ".yml", ".yaml", ".cfg", ".env"}


def io_path(path: Path) -> str:
    name = str(path.resolve())
    if os.name == "nt" and not name.startswith("\\\\?\\"):
        return "\\\\?\\UNC\\" + name[2:] if name.startswith("\\\\") else "\\\\?\\" + name
    return name


def digest(path: Path) -> str:
    with open(io_path(path), "rb") as file:
        return hashlib.file_digest(file, "sha256").hexdigest()


def allowed_name(relative: Path) -> bool:
    name = relative.name.lower()
    return not (any(p.lower() in EXCLUDED_DIRS for p in relative.parts) or name in SECRET_NAMES
                or (name.startswith(".env") and name != ".env.example")
                or relative.suffix.lower() in EXCLUDED_SUFFIXES | SECRET_SUFFIXES
                or name in {"thumbs.db", ".ds_store", "desktop.ini"}
                or name.startswith("~$") or relative.suffix.lower() in {".tmp", ".temp", ".pyc", ".pyo"})


def select_files(root: Path, filesystem: bool = False) -> list[Path]:
    if filesystem:
        names = []
        for directory, dirs, files in os.walk(io_path(root), followlinks=False):
            dirs[:] = [d for d in dirs if d.lower() not in EXCLUDED_DIRS and not os.path.islink(os.path.join(directory,d))]
            for name in files:
                # O caminho relativo é calculado no mesmo namespace estendido no Windows.
                names.append(Path(os.path.relpath(os.path.join(directory,name), io_path(root))).as_posix())
    else:
        top = subprocess.run(["git", "-C", str(root), "rev-parse", "--show-toplevel"], capture_output=True, text=True, encoding="utf-8")
        if top.returncode or Path(top.stdout.strip()).resolve() != root.resolve():
            raise ValueError("Sem Git próprio nesta raiz. Use --filesystem explicitamente para um pacote extraído.")
        result = subprocess.run(["git", "-C", str(root), "ls-files", "--cached", "-z"], capture_output=True, check=True)
        names = result.stdout.decode("utf-8").rstrip("\0").split("\0") if result.stdout else []
        ignored = subprocess.run(["git", "-C", str(root), "check-ignore", "--no-index", "--stdin", "-z"], input="\0".join(names).encode("utf-8") + b"\0", capture_output=True)
        if ignored.returncode not in (0,1):
            raise ValueError("Não foi possível conferir .gitignore")
        ignored_names = set(ignored.stdout.decode("utf-8").rstrip("\0").split("\0"))
        names = [n for n in names if n not in ignored_names]
    selected = []
    for name in sorted(set(names)):
        rel = Path(name)
        if not allowed_name(rel):
            continue
        path = root / rel
        if not path.resolve().is_relative_to(root.resolve()):
            raise ValueError("Arquivo fora da raiz: " + name)
        if path.is_symlink() or any(parent.is_symlink() for parent in path.parents if parent != root.parent):
            raise ValueError("Link simbólico não pode entrar no pacote: " + name)
        if not stat.S_ISREG(os.stat(io_path(path)).st_mode):
            raise ValueError("Arquivo não regular: " + name)
        selected.append(path)
    return selected


def check_payload(path: Path) -> None:
    with open(io_path(path), "rb") as handle:
        head = handle.read(256)
        if head.startswith(b"version https://git-lfs.github.com/spec/v1"):
            raise ValueError("Asset LFS não baixado; execute git lfs pull: " + path.name)
        if path.suffix.lower() in TEXT_SUFFIXES or path.name == ".env.example":
            handle.seek(0)
            if SECRET_PATTERN.search(handle.read()):
                raise ValueError("Padrão de credencial detectado; valor omitido: " + path.name)
    if path.suffix.lower() == ".zip":
        with zipfile.ZipFile(io_path(path)) as archive:
            for member in archive.infolist():
                if member.is_dir():
                    continue
                member_path = Path(member.filename.replace("\\", "/"))
                if member_path.is_absolute() or ".." in member_path.parts or not allowed_name(member_path):
                    raise ValueError("Entrada interna insegura em ZIP: " + path.name)
                if member_path.suffix.lower() in TEXT_SUFFIXES:
                    with archive.open(member) as handle:
                        if SECRET_PATTERN.search(handle.read()):
                            raise ValueError("Padrão de credencial dentro de ZIP; valor omitido: " + path.name)


def inventory_for(root, files):
    inventory = []
    for path in files:
        check_payload(path)
        inventory.append({"path":path.relative_to(root).as_posix(), "bytes":os.stat(io_path(path)).st_size, "sha256":digest(path)})
    return inventory


def package(root, files, output, inventory):
    # Somente artefatos novos. O inventário histórico da raiz não é regravado.
    sidecar = output.with_suffix(".inventario.json")
    if output.exists() or sidecar.exists():
        raise FileExistsError("Saída já existe; escolha outro nome de versão")
    output.parent.mkdir(parents=True, exist_ok=True)
    embedded = root.name + "/inventario_publicacao.json"
    if any(root.name+"/"+item["path"] == embedded for item in inventory):
        raise ValueError("Nome reservado inventario_publicacao.json já existe na raiz")
    payload = json.dumps({"created_utc":datetime.now(timezone.utc).isoformat(), "files":inventory}, ensure_ascii=False, indent=2) + "\n"
    created = False
    sidecar_created = False
    try:
        with open(io_path(output), "xb") as stream:
            created = True
            with zipfile.ZipFile(stream, "w", zipfile.ZIP_DEFLATED, compresslevel=6) as archive:
                for path in files:
                    archive.write(io_path(path), root.name+"/"+path.relative_to(root).as_posix())
                archive.writestr(embedded, payload)
        with zipfile.ZipFile(io_path(output)) as archive:
            if archive.testzip() is not None:
                raise RuntimeError("Falha de integridade ZIP")
            expected = {root.name+"/"+item["path"] for item in inventory} | {embedded}
            if set(archive.namelist()) != expected:
                raise RuntimeError("Inventário e ZIP divergem")
            for item in inventory:
                with archive.open(root.name+"/"+item["path"]) as handle:
                    if hashlib.file_digest(handle, "sha256").hexdigest() != item["sha256"]:
                        raise RuntimeError("Arquivo mudou durante o empacotamento: " + item["path"])
        with open(io_path(sidecar), "x", encoding="utf-8") as handle:
            sidecar_created = True
            handle.write(payload)
    except Exception:
        # Remove apenas saídas novas desta chamada, nunca arquivos anteriores.
        if created:
            os.unlink(io_path(output))
        if sidecar_created:
            os.unlink(io_path(sidecar))
        raise
    return sidecar


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--filesystem", action="store_true", help="Raiz extraída sem Git; aplica as mesmas exclusões obrigatórias")
    parser.add_argument("--dry-run", action="store_true", help="Confere seleção, credenciais, LFS e hashes sem criar ZIP")
    parser.add_argument("--output", type=Path)
    parser.add_argument("--report", type=Path)
    args = parser.parse_args()
    try:
        files = select_files(ROOT, args.filesystem)
        if not files:
            raise ValueError("Nenhum arquivo selecionado")
        if args.report and (args.report.exists() or args.report.resolve() in files):
            raise ValueError("Relatório deve ser arquivo novo e não pode sobrescrever entrada")
        output = args.output.resolve() if args.output else ROOT / "dist" / ("Guia_Bellas_IA_" + datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ") + ".zip")
        if output in files or output.with_suffix(".inventario.json") in files:
            raise ValueError("A saída não pode ser arquivo de entrada")
        inventory = inventory_for(ROOT,files)
        if not args.dry_run:
            package(ROOT,files,output,inventory)
        result = {"status":"passed", "dry_run":args.dry_run, "selection":"filesystem" if args.filesystem else "git_tracked", "file_count":len(files), "bytes":sum(i["bytes"] for i in inventory), "files":inventory}
        if args.report:
            args.report.parent.mkdir(parents=True,exist_ok=True)
            with args.report.open("x", encoding="utf-8") as handle:
                handle.write(json.dumps(result,ensure_ascii=False,indent=2)+"\n")
        print(f"Seleção conferida: {len(files)} arquivos; {result['bytes']} bytes; " + ("sem criar ZIP" if args.dry_run else f"ZIP verificado: {output}"))
        return 0
    except (ValueError, OSError, RuntimeError, zipfile.BadZipFile, subprocess.SubprocessError) as exc:
        print(f"Empacotamento recusado: {exc}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
