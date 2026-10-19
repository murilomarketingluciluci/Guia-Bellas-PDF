"""Sonda negativa contra PSD/PNGs/PDF reais; não produz ou altera APN."""
from pathlib import Path
import json
import os
import subprocess
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
fixture = HERE/"fixture_manifesto_sem_paginas.json"
fixture.write_text(json.dumps({"purpose":"Fixture negativa; nunca usar em produção","schema_version":"2.0","stage":"planejamento","canvas":[1920,1080],"template":{"psd":os.path.relpath(ROOT/"referencias/molde_bellas_aprovado_capa_temas_agradecimento.psd",HERE).replace("\\","/")},"slides":[]}),encoding="utf-8")
report_path = HERE/"qa_integrado_negativo.json"
project = ROOT/"treinamentos/crescimento_photopea_v2/entrega"
cmd = [sys.executable,str(ROOT/"scripts/validar_artefatos_bellas.py"),"--manifest",str(fixture),"--psd",str(project/"Crescimento_Photopea_V2.psd"),"--png-dir",str(project/"pngs"),"--pdf",str(project/"Crescimento_Photopea_V2.pdf"),"--report",str(report_path)]
result = subprocess.run(cmd,capture_output=True,text=True,encoding="utf-8",errors="replace",env={**os.environ,"PYTHONIOENCODING":"utf-8"})
report = json.loads(report_path.read_text(encoding="utf-8"))
expected = result.returncode == 1 and any("stage: final" in p for p in report["problems"]) and any("slides" in p for p in report["problems"]) and report["visual_approval"] is False
summary = {"command_exact":cmd,"exit_code":result.returncode,"expected_rejection":expected,"technical_problem_count":len(report["problems"]),"stdout":result.stdout,"stderr":result.stderr,"scope":"Reprovação esperada de manifesto artificial; diferenças históricas de ICC/capa/agradecimento continuam reportadas. Não homologa a arte V2."}
(HERE/"sonda_integrada.json").write_text(json.dumps(summary,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
print(json.dumps({"expected_rejection":expected,"exit_code":result.returncode,"problem_count":len(report["problems"])}))
raise SystemExit(not expected)
