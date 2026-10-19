"""Mantém bytes/terminadores históricos fora das pequenas correções de autoridade."""
from pathlib import Path
ROOT = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parent
for name in ["FONTES_E_EVIDENCIAS.md","DECISOES_APN_BELLAS.md","DIRECAO_DE_ARTE.md"]:
    original = (HERE/"instrucoes_antes"/name).read_bytes().decode("utf-8")
    nl = "\r\n" if "\r\n" in original else "\n"
    if name == "FONTES_E_EVIDENCIAS.md":
        result = original.replace("O projeto atual usa `molde v1.0.psd`", "**Proveniência histórica da inspeção inicial; não é a base operacional atual.** O estudo inicial usou `molde v1.0.psd`")
        result = result.replace("## PSDs e medidas disponíveis", "## PSDs e medidas disponíveis"+nl+nl+"A base operacional vigente é `referencias/molde_bellas_aprovado_capa_temas_agradecimento.psd`, conforme `CONTRATO_ATUAL.md` e `MODELO_REUTILIZAVEL.md`.")
    elif name == "DECISOES_APN_BELLAS.md":
        result = original.replace("Este é o contrato editorial e visual atual para novas APNs.", "Este é o registro de decisões editoriais/visuais e sua proveniência. As regras vigentes estão consolidadas em `CONTRATO_ATUAL.md`; os casos abaixo mantêm seu escopo original.")
    else:
        result = original.replace("# Direção de arte antes do layout", "# Direção de arte antes do layout"+nl+nl+"Aplicação do `CONTRATO_ATUAL.md`. As justificativas do mapa devem ser comprovadas nas provas: nomear um objetivo não demonstra que a composição o atingiu. Classifique procedimento, condição/restrição, benefício, evidência, atribuição e fecho antes de diagramar; preserve essas funções. Compare a alternativa escolhida à descartada por foco, clareza e leitura, sem exigir variedade por contagem.")
    (ROOT/name).write_bytes(result.encode("utf-8"))
print("Três referências com alterações focais e terminadores originais preservados.")
