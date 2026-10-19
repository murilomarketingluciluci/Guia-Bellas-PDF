# Molde reutilizável aprovado

Para começar outro treinamento, use uma **cópia** de `referencias/molde_bellas_aprovado_capa_temas_agradecimento.psd`. O contato das quatro partes está em `referencias/molde_bellas_aprovado_contato.jpg`. O arquivo original permanece intacto.

O PSD 1920×1080 contém somente quatro grupos de trabalho, além do plano de fundo:

1. `CAPA APROVADA - ALTERAR SOMENTE TITULO`: conserva a arte aprovada, a etiqueta fixa `TREINAMENTO`, cabeçalho, marcas e imagem de marca esmaecida. O texto a alterar está na camada `Agrupar 12 > Desodorante Optima`. Edite **somente esse título**, mantendo seu objeto de texto e estilos internos; faça as quebras necessárias para o novo nome sem mudar a composição.
2. `TEMA CLARO VAZIO - DUPLICAR`: campo rosa claro com elementos fixos, sem conteúdo do Optima. Duplique para criar páginas claras.
3. `TEMA ESCURO VAZIO - DUPLICAR`: campo malva com elementos fixos e B de fundo, sem conteúdo do Optima. Duplique para criar páginas escuras.
4. `AGRADECIMENTO APROVADO - ULTIMA PAGINA`: copie como última página **sem mudar nada**.

No PSD de produção, renomeie a capa para `01 - Capa`, duplique e numere as páginas intermediárias em sequência (`02 - ...`, `03 - ...`) e renomeie o agradecimento com o último número. Deixe as duas bases originais ocultas e sem número, ou retire-as da cópia de produção depois de gerar as páginas. Assim `scripts/exportar_pngs_bellas.jsx` encontra apenas as páginas numeradas. Cada página de conteúdo recebe seus textos/fotos em um grupo `CONTENT` próprio; H1 continua em um objeto de texto e cards são agrupados integralmente.

As exportações de teste por Save for Web PNG24 da capa e do agradecimento desse molde foram comparadas **pixel a pixel** com `exemplos/optima_final/pngs_aprovados/pagina_01.png` e `pagina_13.png`: RGB idêntico. As duas páginas de tema vazio foram inspecionadas no contato. Esse PSD é a base operacional para novos treinamentos; `referencias/molde_v1_0_base.psd` é a fonte histórica do molde anterior.
