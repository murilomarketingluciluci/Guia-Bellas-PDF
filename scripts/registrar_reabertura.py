"""Registra hashes após a reabertura/exportação real no editor; não executa o editor."""
import argparse
from datetime import datetime, timezone
import json
from pathlib import Path

from validar_artefatos_bellas import numbered_pngs
from verificar_textos_psd import digest


def record(psd, folder, editor):
    problems = []
    pngs = numbered_pngs(folder,problems)
    if problems:
        raise ValueError("; ".join(problems))
    before = digest(psd)
    pages = [{"number":i,"sha256":digest(path)} for i,path in enumerate(pngs,1)]
    if before != digest(psd) or any(entry["sha256"] != digest(path) for entry,path in zip(pages,pngs)):
        raise ValueError("PSD/PNGs mudaram durante o registro")
    return {"created_utc":datetime.now(timezone.utc).isoformat(),"editor":editor,"psd_sha256":before,"pages":pages,"scope":"Vínculo de arquivos após abertura/exportação documentada no diário; este script não executa o editor."}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--psd",type=Path,required=True)
    parser.add_argument("--png-dir",type=Path,required=True)
    parser.add_argument("--editor",required=True)
    parser.add_argument("--output",type=Path,required=True)
    args = parser.parse_args()
    try:
        result = record(args.psd,args.png_dir,args.editor)
        args.output.parent.mkdir(parents=True,exist_ok=True)
        with args.output.open("x",encoding="utf-8") as handle:
            handle.write(json.dumps(result,ensure_ascii=False,indent=2)+"\n")
        print(f"Vínculo registrado: {len(result['pages'])} páginas; não substitui a ação real no editor.")
        return 0
    except (ValueError,OSError) as exc:
        print(f"Registro recusado: {exc}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
