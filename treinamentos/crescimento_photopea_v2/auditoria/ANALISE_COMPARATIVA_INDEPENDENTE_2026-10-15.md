# Análise independente — Crescimento Photopea V2

**Data:** 15/10/2026 (São Paulo). **Escopo:** revisão dos artefatos finais e da auditoria da V2; comparação visual com Crescimento/Luciane anterior e com as instruções do repositório. Esta análise não altera a APN nem substitui uma aprovação do usuário.

## Resposta à dúvida sobre o fluxo

A V2 começou **antes** da revisão do fluxo. O diário do agente de catálogo (`execucao/catalogo.jsonl`, evento `catalogo-002`) registra a leitura de `AGENTS.md`, `FLUXO_NOVO_TREINAMENTO.md`, `MODELO_REUTILIZAVEL.md` e outros documentos às **11h01**. `DIRECAO_DE_ARTE.md` foi criado às **11h15**; `AGENTS.md` foi alterado nesse mesmo minuto. Não encontrei no diário do catálogo uma releitura posterior desses arquivos nem leitura de `DIRECAO_DE_ARTE.md`. O principal consultou verificadores novos mais tarde, inclusive `scripts/validar_artefatos_bellas.py` após 12h. Portanto, a V2 incorporou **parte** dos controles técnicos novos durante a execução, mas seu mapa de páginas não é um teste limpo da nova direção de arte.

A escolha da **API do Photopea** foi pedida expressamente pelo usuário (`pedido.txt`). Não cabe registrar a mudança de backend como descumprimento da regra padrão de Photoshop/COM. O fluxo tentou abrir o **molde aprovado** `referencias/molde_bellas_aprovado_capa_temas_agradecimento.psd`; a abertura integral falhou e a montagem reconstruiu as bases a partir de elementos extraídos desse molde. Não há evidência de que a V2 tenha usado o PSD final antigo do Optima como doador de páginas, problema identificado na outra versão.

## Evidência examinada

- `../entrega/visao_geral.jpg` e as 12 imagens de `../entrega/pngs/`, abertas em página inteira; comparação com `../../crescimento_luciane/entrega/visao_geral.jpg` e páginas correspondentes de `../../crescimento_luciane/entrega/provas_png/`.
- `../entrega/Crescimento_Photopea_V2.pdf` e o PDF da versão anterior: ambos têm **12 páginas**, acompanhadas de 12 PNGs 1920×1080.
- `../manifest_photopea.json`, `../leitura/direcao_catalogo_v2.md`, `../leitura/QA_VISUAL_V2_SUPLEMENTO_FINAL.md`, `../QA_FINAL.md`, `DECISOES_FINAIS.md` e os diários da execução.
- Amostragem técnica própria: as cores de fundo exportadas em ambas as versões coincidem nos pontos examinados (`#FBA9C3` claro e `#BC718C` escuro); 0/12 PNGs V2 contêm perfil ICC, ante 12/12 PNGs da versão anterior. Os PDFs têm imagens `/ICCBased` em 12/12 páginas; o perfil embutido na V2 identifica-se como **Artifex Software sRGB ICC Profile**. Assim, a ausência de ICC nos PNGs não autoriza dizer que o PDF esteja sem sRGB.

## Julgamento visual comparativo

**Conclusão:** a impressão de uma V2 menos forte é sustentada pela comparação, mas não de forma uniforme. As telas 07 e 11 da V2 têm boa hierarquia e cumprem a pausa/fecho. A V2 também substitui grades repetidas por registros horizontais e uma sequência aberta, preserva o conteúdo e apresenta cenários mais variados. A versão anterior, por sua vez, cria mais conexão humana e mantém pontos focais mais nítidos em páginas decisivas. O problema principal observado é **direção editorial da imagem e distribuição de ênfase**, não uma falha geral de renderização da Gotham ou de cor.

| Trecho | O que a V2 melhora | O que enfraquece em relação à anterior |
|---|---|---|
| 02 — preparação | Sequência de quatro atitudes clara e sem cartões decorativos. | Sai a mulher escrevendo, que tornava preparação uma ação reconhecível. Título, premissa e lista viram dois polos distantes; cada item tem peso muito parecido e menor destaque em contato reduzido. A versão anterior tinha foto + título maior + quatro faixas de leitura imediata. |
| 03 — propósito/direção | A arcada oferece um eixo visual coerente com “direção”. | A cena vazia é elegante, mas impessoal; a combinação título de duas linhas + foto lateral reaparece em outras páginas. |
| 04–05 — episódios 01–08 | O formato aberto diferencia a série da grade 2×2 anterior; todos os nomes, ações e referências ficam legíveis em tamanho cheio. | Na 04, nome e ação estão separados por uma distância horizontal grande, apesar de pertencerem à mesma unidade. Filetes/números leves segmentam menos que os cartões anteriores. Na 05, muito campo vazio à esquerda reduz o peso da lista. Os oito episódios passam a ter hierarquia quase uniforme. |
| 06 — episódios 09–12 | Foto, quatro faixas e fecho dão direção de leitura; o problema de contraste do cabeçalho foi corrigido. | As quatro faixas são sensivelmente mais densas que o restante do conjunto, e a foto de caminho rochoso repete a linguagem simbólica de espaço vazio. |
| 07 — “Está consumado” | **Boa solução da V2:** pausa clara, título/citação/referência associados, peso tipográfico adequado. | Nenhum problema relevante observado na composição. |
| 08 — multiplicação | Processo em três marcos representa a cadeia sem inventar conteúdo. | A linha e os quadrados de 24 px são corretos tecnicamente, mas discretos demais no contato. O slide perde a cena de duas mulheres interagindo da versão anterior; a mensagem humana vira diagrama leve e a parte superior fica sem título/foco dominante. |
| 09 — pessoas | **Boa imagem humana da V2:** três mulheres de idades diferentes, aparência real e margens fotográficas amplas. | A cena só chega após sete telas com pessoas ausentes; sua força emocional chega tarde. |
| 10 — samaritana | O poço/jarro ilustra a referência sem colagem e mantém o texto legível. | A protagonista da história não aparece. Mais um objeto/cenário sem pessoa reforça a distância criada pela sequência de fotos. A textura de pedra histórica se afasta do universo contemporâneo Bellas. |
| 11 — convite/fecho | **Boa solução da V2:** citação grande, explicação, referência e chamada com ritmo e proximidade. | Nenhum problema relevante observado após a correção do filete. |
| Capa e agradecimento | Composição fixa reconhecível; somente o título da capa varia. | A reconstrução Photopea não é pixel idêntica aos PNGs Photoshop aprovados; a própria QA mede as diferenças. Elas são pequenas visualmente e não explicam a fraqueza do conjunto. |

### Causa visual mais provável

Das **quatro fotos novas da V2**, apenas a 09 mostra pessoas; as demais mostram arquitetura, costa/caminho e poço/jarro. A versão anterior tinha mulheres nas páginas 02, 08 e 09, embora repetisse um tipo de ambiente de trabalho. A V2 corrigiu repetição de cenários, mas trocou grande parte da **presença humana** por símbolos de lugar/objeto. Como a argumentação fala de preparação, influência, crescimento e pessoas, essa troca reduz a conexão emocional em pontos decisivos. Isso é uma inferência de direção de arte baseada no contato e nas páginas inteiras, não uma falha técnica demonstrável por validador.

O segundo fator é de **hierarquia/ritmo**: as páginas abertas 04–05 dependem de números e filetes finos; a 08 depende de um eixo igualmente fino; a 06 concentra muita informação em faixas. A alternância entre pouco peso visual e uma página densa enfraquece o conjunto no contato. Não identifiquei substituição evidente de fonte ou texto cortado como causa principal; o PSD e a QA relatam Gotham nativa e conferência editorial.

## O que os validadores provam — e o que não provam

O relatório final registra 1.045 controles técnicos aprovados e três diferenças de identidade RGB na capa/agradecimento; a reabertura do PSD reproduziu os 12 PNGs da V2, e o PDF usa os mesmos pixels. Isso dá boa confiança na **consistência da entrega**, não em sua qualidade comparativa ou aprovação de marca pelo usuário. O parecer visual anterior chamou todas as páginas de “aptas” porque buscou bloqueadores, como corte, baixo contraste e margens; não fez julgamento comparativo suficiente do vínculo entre fotografia, assunto e peso dos blocos. A palavra “apto” deve ser entendida nesse alcance limitado.

Os **PNGs V2 não têm ICC incorporado**. O PDF final tem perfil sRGB embutido e suas cores de fundo medidas estão corretas, mas a entrega PNG não satisfaz a orientação atual de perfil explícito. Isso merece correção no fluxo de exportação Photopea ou declaração separada na QA. Não há base para atribuir a percepção de fraqueza visual a esse detalhe de metadados.

## Decisões úteis para o próximo agente

1. No mapa, registrar **quem/que ação humana** a foto torna visível, além de tema, luz e variedade de cenários. Para uma história centrada em pessoas, evitar que três das quatro fotos sejam espaços/objetos vazios sem uma justificativa narrativa forte. A solução não é repetir a mesma foto de axila ou reunião.
2. Em série com personagem, ação e referência, testar a leitura em **contato reduzido**. Se nome e ação se separam demais, aproximá-los dentro de uma unidade editável; se quatro registros ficam com a mesma ênfase, destacar o que conduz à conclusão sem alterar o conteúdo.
3. Para slides de processo como a 08, testar se o **assunto principal aparece primeiro** em tamanho de apresentação. Uma linha tecnicamente correta pode ser insuficiente como foco. Considerar pessoa em ação ou um eixo com ponto de chegada mais forte, conforme a narrativa.
4. Fazer uma revisão **comparativa** contra páginas aprovadas e contra alternativas do próprio mapa, além da revisão de bloqueadores. Não copiar a versão anterior: usar a comparação para verificar calor humano, hierarquia e cadência.
5. No backend Photopea, manter o teste de abertura/reabertura do PSD, registrar as perdas de Smart Object e **incluir ICC sRGB nos PNGs finais** ou marcar explicitamente a limitação. Confirmar separadamente o perfil do PDF e a igualdade de pixels.
6. Quando documentos ativos mudarem durante um trabalho longo, registrar a versão/data lida e reler as instruções antes de fechar o mapa. Esta V2 começou antes da nova direção de arte; sua qualidade não deve ser usada como veredito sobre a eficácia do fluxo revisado.

## Limites desta revisão

Não alterei camadas nem gerei nova arte. A comparação de força visual é crítica editorial, não métrica objetiva ou autorização para substituir a entrega. Não atribuo diferenças de tipografia diretamente ao Photopea: as composições foram redesenhadas, e a V2 mostra Gotham sem substituição evidente. A reconstrução do molde no backend e o perfil ausente dos PNGs são limitações técnicas reais, mas distintas da causa visual provável.
