# Manual visual resumido

## 1. Formato e linguagem

O molde aprovado é a **estrutura fixa de marca**, não uma fórmula para páginas internas. Comece um treinamento novo somente em `referencias/molde_bellas_aprovado_capa_temas_agradecimento.psd` (capa, dois temas vazios, agradecimento). Use os PSDs Optima/Rosângela para estudar estilo e os PNGs aprovados para comparar aparência; não copie grupos deles para o PSD novo. Antes de escolher entre os 26 arquétipos, defina a relação visual do conteúdo conforme `DIRECAO_DE_ARTE.md`. Esse passo evita repetir H1 e faixa de foto por inércia.

- Canvas 16:9. O PDF Rosângela anexado mede **1920×1080** por página; o mockup Optima v2 usa **960×540** e escala proporcionalmente.
- A composição usa campos cromáticos amplos, áreas de respiro, títulos sem serifa, barras rosadas para bullets e fotografias de leitura imediata.
- A primeira catalogação reuniu **227 telas de 15 PDFs** e condensou padrões em 26 arquétipos. Esses arquétipos são abstrações; não são cópias pixel a pixel dos originais.

## 2. Elementos recorrentes observados

Na APN Rosângela fornecida, observam-se o microtítulo superior espaçado (`EMPREENDEDORISMO FEMININO`), três pequenos quadrados no canto superior direito, a marca **BELLAS** no rodapé esquerdo, **LUCI|LUCI** no rodapé direito e um `B` grande com baixa opacidade no fundo. O acabamento muda conforme fundo e foto. Alguns materiais catalogados mostram variações; use as camadas do PSD como autoridade para o projeto atual. Na referência editável Rosângela de 1920×1080, o cabeçalho foi localizado em `x≈96–742, y≈58–70`; logos em `x≈55–212, y≈991–1020` e `x≈1704–1859, y≈981–1029`.

## 3. Paleta e autoridade de cor

Os **13 PNGs aprovados pelo usuário** em `exemplos/optima_final/pngs_aprovados/` determinam a aparência final do caso. As cores dominantes medidas neles são `#FBA9C3` nas páginas claras e `#BC718C` nas escuras; pequenas variações locais vêm de textura, transparência e fotografia. O PSD Optima estava sem perfil atribuído; outras rotas de exportação mostraram `#E7A7C1` e `#A9708A`, mas produziram um PDF percebido como opaco e foram rejeitadas. **O usuário fixou `#B3718E` para texto escuro de apoio sobre tema claro; parágrafos corridos ficam brancos.** Os valores históricos abaixo ajudam a interpretar referências, não substituem a comparação com os PNGs aprovados.

| Uso | HEX de estudo | Origem |
|---|---|---|
| Rosa claro de fundo | `#F8A5BF` | catálogo histórico / mockup Optima |
| Rosa claro aprovado no Optima | `#FBA9C3` | cor dominante dos PNGs finais aprovados; alvo visual |
| Rosa claro de exportação opaca | `#E7A7C1` | rota antiga; não usar como alvo final |
| Rosa luz | `#FCB1C8` | catálogo histórico |
| Barra rosa | `#FFADCD` | catálogo histórico |
| Malva aprovado no Optima | `#BC718C` | cor dominante dos PNGs finais aprovados |
| Malva escuro | `#A96281` | catálogo histórico |
| Malva da exportação rejeitada | `#A9708A` | rota antiga opaca; não usar como alvo final |
| Malva escuro Optima v2 | `#9E5D79` | decisão de mockup, não marca validada |
| Creme quase branco | `#FFF4F7` | catálogo histórico |
| Texto escuro histórico | `#713B53` | catálogo antigo; **não usar** como apoio no projeto atual |
| Texto escuro de apoio atual | `#B3718E` | decisão explícita do usuário para tema claro |
| Branco | `#FFFFFF` | catálogo histórico |
| Fotografia quente de referência | `#4A251F` | placeholder, não cor de pele ou filtro obrigatório |

No PDF Rosângela, a página 14 mostra um malva de fundo, barras rosa luminosas e texto branco. O PSD deve decidir os valores de produção.

## 4. Tipografia e tamanhos

A referência **editável** `referencias/rosangela_editavel.psd` foi inspecionada offline. Famílias encontradas: **Gotham-Book, Gotham-Bold, Gotham-Medium e Gotham-Light**. Valores de tamanho armazenados nas camadas: H1 interior recorrente **102.505**, H1 da capa **120.863**, subtítulo **56.947**, corpo **40–56.947**, bullets finais **67.156**, cabeçalho Gotham-Medium **25**. Esses valores não são tamanhos visuais em pontos que possam ser aplicados diretamente: a transformação de cada camada e a resolução influenciam o resultado. Por exemplo, o cabeçalho armazena tamanho 25, transformação vertical ≈0.6082 e bounds visíveis de cerca de 12 px de altura. Para arte nova, copiar os estilos das camadas equivalentes e verificar tamanho aparente na prova.

Antes da produção em lote, teste a tipografia no editor que produzirá o PSD final. Renderize texto real em Gotham, exporte pela rota final e compare o **tamanho aparente, peso e contraste** do título com páginas aprovadas de função semelhante em 1920×1080 e no contato. O H1 em uma camada permite estilos internos; não obriga a mesma palavra em Bold, a mesma quebra ou a mesma escala em todas as telas. Uma disposição nova de cards não compensa, por si só, uma hierarquia enfraquecida.

`referencias/rosangela_estilos_medidos.json` contém 518 camadas, incluindo 67 de texto, com caminho, bounds, fontes por run, tamanho armazenado, leading, tracking e transformação. `referencias/molde_camadas_medidas.json` registra as 12 camadas do molde. A inspeção não modificou Photoshop; foi realizada com `scripts/inspecionar_psd.py`. Dados de leading/tracking também são valores armazenados e exigem interpretar auto-leading e a escala. Não use a média das fontes como um token universal.

O PDF Bellas/Rosângela está essencialmente rasterizado e não expõe fontes pela API de extração. A inspeção do **PSD** é a base destes valores. O **mockup Optima** foi desenhado em 960×540 com Arial/Arial Bold apenas como marcador temporário: H1 de 25–33 unidades do PDF; corpo e bullets de 16–20 unidades. **Não copie Arial nem esses tamanhos para a arte Bellas**; use Gotham e as camadas do PSD.

Hierarquia observável: H1 grande e com amplo respiro, podendo ocupar até duas linhas; uma palavra pode ganhar peso extra **quando isso expressa uma ênfase real**. Duas linhas Book/Bold não são receita obrigatória. Faixas horizontais são uma solução histórica para itens comparáveis, não um padrão para qualquer lista ou benefício. Em telas densas, dividir o conteúdo mantém a leitura melhor que reduzir todo o texto.

Na APN Optima final, o H1 foi feito como **uma camada de texto com estilos internos** para palavra Book/Bold e eventuais cores diferentes. O usuário preferiu caixa mista, tracking compacto (aproximadamente -70 para H1 e -60 para corpo) e variação de uma palavra em Bold ou uma palavra maiúscula com mini subtítulo. Não separar palavras do mesmo H1 em camadas soltas. A aparência final depende do espaço de cada página. **Corpo/parágrafo: branco.** Cor de apoio escura no fundo claro: `#B3718E`; destaques no fundo escuro podem usar rosa claro. Consulte as 13 provas em `exemplos/optima_final/pngs_aprovados/` para a escala visual atual.

## 5. Medidas de composição do mockup Optima v2

Estas são **coordenadas do estudo**, não medidas finais do PSD. Origem no canto superior esquerdo, tela 960×540. Em telas sem foto, H1 começa tipicamente em `x≈65` e `y≈56–63`, com largura de 550–836 e altura de 76–89. As caixas de corpo ocupam com frequência `x≈65–67` até `x≈895`. A assinatura placeholder ficou no retângulo `x=837, y=493, w=80, h=31`; no PSD, use o rodapé pronto.

Faixas fotográficas efetivamente usadas: tela 4 `x=0, w=365, h=540`; tela 6 `x=0, w=350, h=540`; tela 7 `x=620, w=340, h=540`. Assim, a largura fotográfica varia cerca de **35–38%** da tela e sempre vai de `y=0` a `y=540`. A página 14 do PDF Rosângela usa uma faixa esquerda de cerca de **41%** da tela; esse valor é uma leitura visual do PDF.

## 6. Fundos e ritmo

O usuário corrigiu explicitamente o primeiro rascunho rosa uniforme. No Optima v2, as telas **3, 5, 8 e 10** foram desenhadas com malva escuro; 1, 2, 4, 6, 7, 9, 11 e 12 ficaram claras. Esta sequência é um exemplo específico de adaptação ao conteúdo, não regra fixa para todo treinamento.

No fundo escuro, títulos e painéis podem ganhar rosa claro; no fundo claro, `#B3718E` serve ao texto de apoio e o H1 principal costuma ser branco. Parágrafos corridos permanecem brancos nos dois temas. Ajuste hierarquia e respiro por tela; conserve cabeçalho e rodapé da variante correta do PSD.

## 7. Regra de fotos e capas

**Regra atual do usuário:** capa com **somente o título do treinamento** como conteúdo textual, em um único objeto editável; cabeçalho, três quadrados, B de fundo quando pertinente e marcas Bellas/Luci são identidade fixa. A capa aprovada do Optima conserva uma fotografia de marca muito esmaecida na base; não incluir nova foto principal, benefícios, mini subtítulo ou outras chamadas. Nas páginas internas, a foto ambiental pode preencher a altura inteira e tocar uma lateral ou ocupar a tela completa. Uma modelo recortada sobre o campo cromático também é uma variação válida quando a luz e o recorte se integram à composição.

Para não confundir imagem e fundo rosa, usar fotos de saturação contida com cenário creme, cinza/ardósia ou espresso, sem impor uma dominante marrom. Variar poses e assunto conforme o benefício. Reservar margem para testa, corpo, mãos e produto. A forma do frasco segue a foto real enviada pelo usuário, não a aproximação da IA. A página 8 combina ingrediente real com cartões; a 9 usa mulher bem arrumada e Optima em interior neutro, além de um teste recortado separado; a 12 mostra a atriz da referência aplicando o produto na checklist.

A partir da revisão da página 12, toda fotografia deve reservar **pelo menos 15% da altura no topo e 15% no rodapé após o recorte final** para cabeçalho e assinatura, sem cabeça, mãos, braços, produto ou outro elemento importante nessas faixas. A página 12 atual mostra aplicação espontânea do Optima pela atriz da referência, sem tatuagem, com cenário espresso livre nas extremidades. Audite fotos históricas antes de reusá-las nesta regra.

A correção da página 10 mostrou que **margem segura não é uma barra escura colada**. Na versão final com recorte transparente, o logo branco pousa sobre a roupa naturalmente escura da modelo e o fundo malva da própria tela continua sem emenda. Para estrutura de páginas, consulte `LEITURA_VISUAL_4_PDFS.md`, uma leitura dirigida das 65 telas de quatro PDFs Bellas já presentes no índice geral.
