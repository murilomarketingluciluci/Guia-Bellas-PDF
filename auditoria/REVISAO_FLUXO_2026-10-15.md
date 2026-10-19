# Revisão do fluxo após Crescimento/Luciane

Data: 15/10/2026. Escopo: instruções e verificações reutilizáveis do repositório. As fontes, PSD, PNGs, PDF e registros históricos de Crescimento/Luciane não foram alterados nesta revisão. Este é um registro de fechamento das mudanças; não se apresenta como diário incremental de todos os comandos desta sessão.

## Causa confirmada

O arquivo correto de partida já existia: `referencias/molde_bellas_aprovado_capa_temas_agradecimento.psd`, com capa, dois grupos vazios (claro/escuro) e agradecimento. O script histórico `treinamentos/crescimento_luciane/scripts/produzir_pagina.jsx` abriu também `exemplos/optima_final/optima_apn_bellas_final.psd`; na inicialização apagou os grupos da cópia do molde e copiou de lá a capa e o agradecimento. Uma migração posterior para o molde novo preservou os grupos já copiados. A capa final contém, dentro de `01 Capa/CONTENT`, três camadas Optima ocultas: `LIVRE DE ALUMÍNIO`, `TOQUE SECO` e `NANOTECNOLOGIA`. Elas não aparecem no PDF; o problema é a limpeza/editabilidade do PSD e a possibilidade de reativação.

O segundo problema era de ordem de decisão: o prompt mandava escolher um dos arquétipos antes de estabelecer a relação visual específica de cada página. A revisão de Crescimento encontrou marca consistente, mas H1s muito parecidos em assuntos distintos, três interiores de escritório semelhantes e pouca tradução espacial da ideia de multiplicação. A repetição da grade numerada 04–06, em contraste, foi útil. Por isso a solução não é impor uma quota de layouts/fotos diferentes.

Na cor, o primeiro lote escreveu no PSD sem perfil o HEX desejado para o PNG; a exportação gerou outro RGB. A paleta foi corrigida no trabalho histórico. A nova etapa de prova de cor exportada ocorre **antes** da produção em lote.

## Mudanças reutilizáveis

- `MODELO_REUTILIZAVEL.md`, `AGENTS.md`, `FLUXO_NOVO_TREINAMENTO.md`, `PROMPT_DE_USO.md`, `README.md`, `MANUAL_IDENTIDADE.md` e `skills/bellas-apn/SKILL.md`: identificam o único PSD inicial; distinguem PDF de conteúdo, molde de camadas e PNGs/PSDs de referência; proíbem reconstruir o molde com grupos do PSD Optima.
- `DIRECAO_DE_ARTE.md`, `skills/bellas-fotos/SKILL.md` e `GERACAO_DE_FOTOS.md`: a ideia narrativa precede o arquétipo; mapa e contato passam por crítica de repetição funcional versus automática; fotos são dirigidas como sequência.
- `EXECUCAO_PHOTOSHOP.md`, `QA_FINAL.md`, `DOCUMENTACAO_DA_EXECUCAO.md` e `DECISOES_APN_BELLAS.md`: prova de cor exportada antes do lote, inspeção direta de camadas ocultas, distinção entre ICC configurado e ICC presente e separação do QA mecânico do parecer visual.
- `scripts/verificar_molde.py`: valida a estrutura do PSD aprovado antes de iniciar. `scripts/validar_manifest.py --require-approved-template`: impede manifesto novo de apontar para outro PSD doador; mantém a leitura dos manifestos históricos sem essa opção. `scripts/validar_artefatos_bellas.py`: lê diretamente o PSD final, acusa texto oculto, confere sequência/contagem de páginas, capa/agradecimento, ICC sRGB em PNGs novos, ICC incorporado no PDF e igualdade dos pixels renderizados.

## Testes executados

- `python scripts/verificar_molde.py`: passou no molde atual (1920×1080; quatro grupos esperados).
- `python scripts/verificar_molde.py --path referencias/molde_v1_0_base.psd`: falhou como esperado, por nomes/estrutura do molde antigo.
- `python scripts/validar_manifest.py exemplos/optima_manifest_placeholders.json --stage planejamento`: continuou passando como exemplo histórico.
- Validação rígida do manifesto Crescimento/Luciane: falhou como esperado no campo `template.approved_psd`; uma cópia temporária sem esse campo passou, mantendo o molde aprovado no `template.psd`.
- `scripts/validar_artefatos_bellas.py` sobre a entrega histórica: detectou o PSD Optima indicado como doador e as três camadas ocultas. As checagens restantes (12 páginas, sRGB, PDF/PNG) passaram.
- `python -m py_compile` dos três scripts alterados/criados; `quick_validate.py` das duas skills; `scripts/validar_pacote.py`: passaram.

O validador novo não substitui a revisão visual nem autoriza automaticamente refazer uma página aceita pelo usuário. A prova real do novo fluxo será um treinamento iniciado **desde o primeiro passo** com o molde correto e com o mapa de direção de arte registrado durante a execução.
