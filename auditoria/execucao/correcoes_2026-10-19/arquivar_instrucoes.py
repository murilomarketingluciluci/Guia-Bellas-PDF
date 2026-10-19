"""Preserva a redação anterior antes da consolidação autorizada."""
from pathlib import Path
import shutil

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
names = ["AGENTS.md", "README.md", "PROMPT_DE_USO.md", "FLUXO_NOVO_TREINAMENTO.md", "FONTES_E_EVIDENCIAS.md", "EXECUCAO_PHOTOSHOP.md", "QA_FINAL.md", "DECISOES_APN_BELLAS.md", "DIRECAO_DE_ARTE.md", "skills/bellas-apn/SKILL.md", "skills/bellas-fotos/SKILL.md"]
for name in names:
    target = HERE / "instrucoes_antes" / name
    if target.exists():
        raise SystemExit("Snapshot já existe; não sobrescrever: " + name)
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(ROOT/name, target)
print(f"{len(names)} documentos preservados antes da edição.")
