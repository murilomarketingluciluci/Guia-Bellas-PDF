# Molde reutilizável aprovado

Para começar outro treinamento, use **somente uma cópia direta** de `referencias/molde_bellas_aprovado_capa_temas_agradecimento.psd`. Este é o arquivo que contém capa aprovada, **duas páginas vazias** (tema claro e escuro) e agradecimento aprovado. O contato das quatro partes está em `referencias/molde_bellas_aprovado_contato.jpg`. O arquivo original permanece intacto. O PDF enviado pelo usuário é fonte de **conteúdo**; o ponto de partida editável é este **PSD**.

O PSD 1920×1080 contém somente quatro grupos de trabalho, além do plano de fundo:

1. `CAPA APROVADA - ALTERAR SOMENTE TITULO`: conserva a arte aprovada, a etiqueta fixa `TREINAMENTO`, cabeçalho, marcas e imagem de marca esmaecida. O texto a alterar está na camada `Agrupar 12 > Desodorante Optima`. Edite **somente esse título**, mantendo seu objeto de texto e estilos internos; faça as quebras necessárias para o novo nome sem mudar a composição.
2. `TEMA CLARO VAZIO - DUPLICAR`: campo rosa claro com elementos fixos, sem conteúdo do Optima. Duplique para criar páginas claras.
3. `TEMA ESCURO VAZIO - DUPLICAR`: campo malva com elementos fixos e B de fundo, sem conteúdo do Optima. Duplique para criar páginas escuras.
4. `AGRADECIMENTO APROVADO - ULTIMA PAGINA`: copie como última página **sem mudar nada**.

**Não apague os quatro grupos para remontar a estrutura a partir de outro PSD.** Em Crescimento/Luciane, o script inicial abriu `exemplos/optima_final/optima_apn_bellas_final.psd`, apagou os grupos do molde e copiou capa/agradecimento daquele exemplo. Isso reintroduziu três textos Optima ocultos na capa; uma migração posterior preservou o resíduo. O exemplo Optima serve para comparar **provas visuais**, não para doar grupos ao arquivo novo. `referencias/molde_v1_0_base.psd`, `referencias/rosangela_editavel.psd`, PSDs de treinamentos e scripts históricos também não são base de produção.

Antes de criar páginas, execute `python scripts/verificar_molde.py` a partir da raiz. O script confere a estrutura do arquivo aprovado. Na cópia de produção, renomeie a capa para `01 - Capa`, duplique e numere as páginas intermediárias em sequência (`02 - ...`, `03 - ...`) e renomeie o agradecimento com o último número. Deixe as duas bases originais ocultas e sem número, ou retire-as da cópia de produção depois de gerar as páginas. Assim `scripts/exportar_pngs_bellas.jsx` encontra apenas as páginas numeradas. Cada página de conteúdo recebe seus textos/fotos em um grupo `CONTENT` próprio; H1 continua em um objeto de texto e cards são agrupados integralmente.

Se houver uma tarefa de **continuar um PSD que o usuário já editou**, esse PSD corrente deve ser preservado. Inventarie-o primeiro; não o substitua pelo molde nem copie páginas do exemplo Optima. Ao migrar excepcionalmente camadas de um documento antigo, liste e revise também camadas ocultas, remova conteúdo legado e confirme capa/agradecimento contra o molde.

As exportações de teste por Save for Web PNG24 da capa e do agradecimento desse molde foram comparadas **pixel a pixel** com `exemplos/optima_final/pngs_aprovados/pagina_01.png` e `pagina_13.png`: RGB idêntico. As duas páginas de tema vazio foram inspecionadas no contato. Esse PSD é a base operacional para novos treinamentos; `referencias/molde_v1_0_base.psd` é a fonte histórica do molde anterior.
