# Fontes, autoridade e confiança

## Evidência disponível

| Item | Evidência | Confiança / limite |
|---|---|---|
| Formato 16:9 | 15 PDFs catalogados; Rosângela 1920×1080 | alta |
| 227 telas / 26 arquétipos | `catalogo_historico_26_layouts.json` e mosaicos de 15 PDFs | alta para contagem; arquétipos são interpretação editorial |
| Cabeçalho, quadrados, marcas e B ao fundo | PDF Rosângela, sobretudo páginas 1, 14 e 15 | alta para presença; medidas finas dependem do PSD |
| Faixa fotográfica esquerda na página 14 | PDF Rosângela, foto cerca de 41% da largura | alta para padrão; proporção aproximada |
| Paleta HEX do catálogo | primeira catalogação visual | média; **aproximações**, não tokens oficiais |
| Tipografia da marca | PSD Rosângela editável inspecionado offline: Gotham, tamanhos de camada descritos no manual | alta para nome da família; tamanhos podem sofrer escala de transformação |
| Aparência final aprovada no Optima | 13 PNGs em `exemplos/optima_final/pngs_aprovados/`: claro dominante `#FBA9C3`, escuro `#BC718C` | alta para pixels exportados; a combinação depende de textura e transparência locais |
| Cores de uma exportação antiga | claro `#E7A7C1`, escuro `#A9708A` | rota rejeitada pelo usuário por ficar opaca; não é alvo de produção |
| Fotos ambientais em faixas/full bleed ou modelos recortadas; capa com somente título de conteúdo | correções explícitas e PNGs aprovados; imagem de marca esmaecida permanece na capa Optima | alta e prioritária |
| Corpo branco, apoio `#B3718E`, H1 numa camada, Gotham/tracking compacto | correções explícitas do usuário e PSD/provas Optima finais | alta para a decisão; conferir aparência por página |
| Cards/checks alinhados, fotos creme/espresso menos saturadas, produto fiel ao frasco real | capturas e correções explícitas do usuário; provas finais | alta para direção; composição depende do tema |
| 15% livres em cima e embaixo de cada foto após recorte; página 12 com mesma atriz, Optima e sem tatuagem | nova correção explícita do usuário e prova final da página 12 | alta; auditar fotos antigas antes de reuso |
| Geometria das 12 telas Optima | script que criou o mockup v2 | alta para o mockup; não garante equivalência ao PSD |

## PSDs e medidas disponíveis

A base operacional vigente é `referencias/molde_bellas_aprovado_capa_temas_agradecimento.psd`, conforme `CONTRATO_ATUAL.md` e `MODELO_REUTILIZAVEL.md`.

**Proveniência histórica da inspeção inicial; não é a base operacional atual.** O estudo inicial usou `molde v1.0.psd` em `C:\Users\Murilo\Documents\Projetos\Bellas\Moldes Apn Fundo e Padrão\`, canvas 1920×1080. A leitura inicial confirmou os grupos superiores `CAPA`, `molde escuro`, `molde claro` e `Plano de Fundo`. Em `CAPA` há `h1 capa`, `FUNDO`, `Camada 1` e `LUCI LUCI-443`; no escuro, `Camada 2` e `BG`; no claro, `Camada 1` e `FUNDO`. A referência `apresentação bellas  rosangela.psd` também tem 1920×1080 e **15 grupos de página no nível raiz** (`CAPA` + `PÁGINA 01` ...), confirmando a organização em um PSD único. Antes de automatizar, revalidar nomes/IDs, visibilidade e itens fixos na cópia de trabalho do molde.

O pacote inclui a referência editável em `referencias/rosangela_editavel.psd`, o dump original `referencias/rosangela_camadas_medidas.txt` e `referencias/rosangela_estilos_medidos.json` (518 camadas/67 de texto; zero erros de leitura de estilo). O JSON registra Gotham-Book/Bold/Medium/Light, tamanho armazenado, leading, tracking, bounds e transformação por camada. `referencias/molde_camadas_medidas.json` registra as 12 camadas da base. Ainda requerem conferência visual caso a caso: tamanho aparente após transformação, auto-leading, caixa e estilo de cada bloco e consistência com o molde. Os PDFs Bellas inspecionados não expõem fontes incorporadas pela API de extração; vários são páginas rasterizadas. **Não converter a tipografia temporária Arial do mockup em especificação Bellas.**

As 15 fontes de 227 páginas estão disponíveis integralmente: 14 em `referencias/pdfs_15/` e Rosângela em `referencias/rosangela_original.pdf`. `galeria_227_telas.html` e `indice_227_telas.csv` associam cada miniatura à sua página original; todas as referências locais passaram pela validação do pacote. As miniaturas de 640 px servem para reconhecimento; o PDF é a fonte para leitura fina.

Em 14/10/2026, o usuário reenviou quatro dessas fontes: `colageno`, `guiar`, `posicionamento` e `anexo Rosangela`. Comparação SHA-256 confirmou que os quatro arquivos correspondem exatamente às cópias já arquivadas. `LEITURA_VISUAL_4_PDFS.md` registra o padrão de composição **de cada uma das 65 páginas** e separa o que pode ser adaptado para o padrão atual das soluções históricas que não devem ser reproduzidas literalmente.

## Padrão histórico versus regra atual

O catálogo histórico registra layouts encontrados nos PDFs, inclusive foto menor, colagens e produtos isolados. O usuário depois determinou que, no novo framework, toda foto preencha uma lateral na altura inteira ou a tela toda e que a capa não tenha foto. O arquivo `catalogo_atual_26_layouts.json` aplica essa decisão em seis arquétipos (05, 09, 17, 18, 19, 24) e conserva os demais. A galeria HTML mostra o motivo de cada adaptação.

## Limite editorial do caso Optima

O PDF da palestrante contém alegações sobre alumínio, absorção, câncer, Alzheimer, microbioma e adaptação. Este repositório **não comprova nem endossa** tais afirmações: ele documenta a distribuição de conteúdo em slides. O usuário pediu manter o texto e revisar somente português nesta execução. Uma eventual revisão factual ou jurídica é um trabalho separado, quando solicitado.
