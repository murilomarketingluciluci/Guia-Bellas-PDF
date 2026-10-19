# QA visual V2 — páginas 02 a 11

> **Parecer intermediário preservado.** O estado atual das 12 telas finais está no [suplemento final](QA_VISUAL_V2_SUPLEMENTO_FINAL.md): APTO visualmente nas versões e hashes ali identificados. O bloqueador 11 abaixo foi corrigido e revisto.

**Resultado: PENDENTE por sobreposição na página 11. As páginas 02–10 estão visualmente aptas nas versões examinadas, algumas com acabamento opcional. Este parecer não aprova capa, agradecimento, PSD reaberto ou PDF final.**

Revisor: `catalogo_novo_v2`. Data: 15/10/2026. Foram abertas individualmente as dez provas em 1920×1080. Após reexportações concorrentes do principal, todas foram revistas; as páginas 06/08/09 receberam uma segunda abertura explícita e a página 11 foi inspecionada também em cópia congelada. Não houve edição de PSD, chamada ao bridge/API ou alteração de montagem por este revisor.

## Versões e evidências

- [Snapshot das dez telas, com hashes](./qa_visual_snapshot_20261015T151353Z/indice.json), capturado em **2026-10-15T15:13:53.548022+00:00**. Os links por página abaixo apontam para essa cópia estável, não para um PNG que pode ser reexportado depois.
- [Métricas iniciais](QA_VISUAL_V2_metricas.json): preservam o estado anterior do contraste 06 e da foto 09; não usar para aprovar as versões substituídas.
- [Métricas atualizadas](QA_VISUAL_V2_metricas_atualizadas.json): contraste 06, estimativa da margem 09, marcos 08 e hashes das provas.
- Comparação de intenção: [direção](direcao_catalogo_v2.md), [layouts](layouts_propostos_v2.json), manifesto de produção e referências Bellas já lidas integralmente no repertório desta V2.
- Hash do manifesto no instante da captura: `a36e1fa89870094b9a6421d29898e95350236ae663d46f5a4e67ab5d6f57fd55`. O manifesto está sendo ajustado pelo principal; este hash não declara correspondência definitiva entre todo o documento de montagem e as provas já exportadas.

O parecer é baseado nas imagens e nas medições descritas, não em logs de sucesso de exportação.

## Variedade, simplicidade e personalização

A variedade é **real e suficiente**: título lateral/lista na 02; bloco compacto com foto na 03; registros largos na 04; título lateral com episódios empilhados na 05; foto/faixas na 06; citação na 07; processo aberto na 08; pessoas/texto na 09; exemplo e imagem de água na 10; conjunto tipográfico de conclusão na 11. Não há repetição de H1 de duas linhas + quatro cards 2×2.

As páginas 02/05 compartilham a tese na lateral;03/10 compartilham faixa direita. A repetição é espaçada e as funções/densidades são diferentes. A identidade fixa e o B de fundo repetidos pertencem à marca. Não recomendo acrescentar ornamentação ou cards para tornar as telas “mais personalizadas”: as escolhas de composição e assunto fotográfico já fazem essa personalização.

A simplicidade é apropriada ao conteúdo. A 08 tem só três blocos porque a fonte tem uma cadeia breve; a 07 funciona como pausa. As páginas de episódios concentram mais informação. As fotos variam arquitetura, paisagem, pessoas e objeto/cenário, com neutros e saturação contida. Não há repetição de um mesmo tipo de retrato.

O respiro maior fica nas extremidades na maioria das telas. Há oportunidade de aproximar referências de seus textos na 10 e de alinhar segmentos curtos na 02, mas não há necessidade de distribuir mais elementos para preencher as margens.

## Bloqueadores e estados alterados

| Achado | Estado |
|---|---|
| Página 11: filete em y780 atravessa o fecho em y750 | **Bloqueador ativo** no snapshot; exige nova prova |
| Página 09 anterior: calçados chegavam a aproximadamente y944, restando 12,6% livres | **Resolvido** pela nova fotografia observada; não reusar a prova antiga como atual |
| Página 06 anterior: microcabeçalho muito fraco sobre céu claro | **Melhorou** após escurecimento real da foto; apto com observação de projeção |
| Página 08: aparência preliminar de barra comprida | **Não confirmado/refutado por pixels.** Não é bloqueador nem motivo para editar os marcos |
| Capa/agradecimento | **Fora deste escopo**, continuam pendentes de revisão própria |
| Editabilidade, fontes/runs no PSD, reabertura e igualdade PDF/PNG | **Fora desta aprovação visual parcial**, dependem da validação técnica final |

## Métrica específica — foto da página 09

O limite exigido é **162px livres** em cada extremidade de 1080 px; assuntos importantes devem permanecer entre **y162 e y918** após o crop.

Na foto anterior, a leitura manual do PNG integral estimou cabelo em y157 e calçados em y944, com incerteza de cerca de 5 px: topo 14,5%, rodapé 12,6%. O rodapé ficava pelo menos cerca de 20 px aquém do necessário, mesmo considerando a incerteza. Era um problema real de enquadramento, não algo a resolver com uma faixa pintada.

Na prova atualizada, as extremidades do assunto estão aproximadamente em **y327 (cabelo)** e **y820 (calçado inferior)**, com incerteza de cerca de 6 px. Isso deixa **30,3% no topo e 24,1% no rodapé**, amplamente acima dos 15%. A área livre pertence ao mesmo teto/pátio/pavimento contínuos. Não vi linha de emenda nem barra artificial.

Esses valores são **estimativas de foco delimitado manualmente sobre o PNG**, não detecção automática de pessoa. A conclusão de cumprimento dos 15% é robusta porque há mais de 90 px de folga além do mínimo no rodapé. O recuo das pessoas reduz a presença facial em relação à primeira foto, mas a conversa continua claramente reconhecível e a hierarquia textual domina corretamente.

## Métrica específica — cabeçalho da página 06

Foram sondados oito pontos de fundo nas proximidades do microcabeçalho, fora das letras, em x100/250/400/550 e y50/80. A razão de luminância contra branco aumentou de **1,64–2,07** para **2,19–2,84** na versão escurecida. O ganho é mensurável; a foto mantém continuidade e não ganhou uma faixa gráfica.

Visualmente, o header ficou identificável. Ele ainda é mais delicado sobre a nuvem clara que sobre os campos cromáticos e outras fotos. Recomendo uma última conferência no tamanho real de apresentação. Se a leitura cair na projeção, ajustar altas luzes/exposição da própria cena, sem inserir barra escura e sem mudar a posição fixa da marca. A métrica é suporte ao parecer, não aprovação automática.

## Correção explícita — processo da página 08

Na primeira visualização, interpretei o trecho entre o segundo e o terceiro marco como uma barra larga. A medição de várias linhas do PNG refutou essa interpretação:

- y398–409 e y413–421: três segmentos de 24 px, em x340–363,1000–1023 e1600–1623.
- y410–412: eixo contínuo de 3 px de altura, conforme o manifesto.
- Nos espaços entre marcos fora do eixo, os pixels são o fundo #FBA9C3; não há retângulo de 624 px.

Corrigi a observação no diário e comuniquei ao principal. Não considero a impressão inicial uma falha confirmada da arte.

## Página 02 — APTO com acabamento opcional

Evidência: [snapshot individual](qa_visual_snapshot_20261015T151353Z/pagina_02.png). Título lateral + quatro registros/filetes; a premissa e os itens estão íntegros. Boa hierarquia, respiro predominante fora do conjunto e leitura distinta dos episódios.

**Recomendação:** Nos dois itens de uma linha, o filete de 100 px prolonga-se bastante abaixo do texto; se houver ajuste fino, centrar número/texto no segmento ou encurtar esses dois filetes. Não é corte nem bloqueador.

## Página 03 — APTO

Evidência: [snapshot individual](qa_visual_snapshot_20261015T151353Z/pagina_03.png). Bloco curto e foto arquitetônica direita; título/afirmações formam um conjunto compacto. Eixo da arcada comunica direção sem acrescentar conteúdo. Marcas visíveis e fotografia contínua.

**Recomendação:** Manter a composição. Não preencher o grande respiro com novos elementos; ele é coerente com a frase breve.

## Página 04 — APTO com acabamento opcional

Evidência: [snapshot individual](qa_visual_snapshot_20261015T151353Z/pagina_04.png). Quatro registros largos substituem a grade2×2. Personagem, ação e referência são legíveis. A relação vertical ação/referência está clara e o título de uma linha muda o ritmo.

**Recomendação:** A distância horizontal nome→ação é maior do que precisa nos nomes curtos. Uma aproximação discreta da coluna de ação, de x760 para cerca x720–730, deixaria o registro mais unido sem reduzir fonte.

## Página 05 — APTO

Evidência: [snapshot individual](qa_visual_snapshot_20261015T151353Z/pagina_05.png). Título lateral e lista de quatro episódios geram outra leitura da mesma série. Conteúdos completos, filetes regulares, números e títulos em eixos consistentes. O malva diferencia a sequência.

**Recomendação:** Manter. A repetição estrutural com a página 02 ocorre em outro contexto e não é excessiva no conjunto.

## Página 06 — APTO com observação de contraste

Evidência: [snapshot individual](qa_visual_snapshot_20261015T151353Z/pagina_06.png). Foto esquerda, quatro faixas e fecho; as unidades estão alinhadas e não encobrem o foco do caminho. Texto visível e hierarquia clara. Cenário contínuo, sem faixa artificial; topo/rodapé sem foco humano/produto.

**Recomendação:** O céu foi escurecido entre as versões. O microcabeçalho ficou mais legível; ainda é a área mais frágil da tela. Conferir na projeção real. Se precisar de mais ganho, comprimir altas luzes da própria fotografia, preservando céu contínuo, sem pintar uma faixa e sem mover o cabeçalho fixo.

## Página 07 — APTO

Evidência: [snapshot individual](qa_visual_snapshot_20261015T151353Z/pagina_07.png). Pausa tipográfica com uma frase, citação e referência. A versão reexportada aproximou João 19:30 da citação, melhorando a unidade. Respiro externo amplo e mensagem de impacto legível.

**Recomendação:** Manter a proximidade atual. Não acrescentar foto, ícone ou caixa apenas para ocupar o espaço.

## Página 08 — APTO; observação preliminar corrigida

Evidência: [snapshot individual](qa_visual_snapshot_20261015T151353Z/pagina_08.png). Processo horizontal aberto, três blocos integrais da fonte e três marcos de 24×24 px. Variedade real em relação às listas. Início/fim mais fortes e elo intermediário mais leve fazem sentido.

**Recomendação:** Não há um retângulo comprido nos bytes do PNG. A impressão preliminar de barra foi refutada pela sonda de pixels: ver nota de correção. Como acabamento, o primeiro marco poderia ficar mais próximo do centro óptico do primeiro bloco; é opcional.

## Página 09 — APTO na fotografia atualizada

Evidência: [snapshot individual](qa_visual_snapshot_20261015T151353Z/pagina_09.png). A nova imagem reduz as pessoas e cria margem natural real acima/abaixo. Conversa entre mulheres de idades distintas corresponde ao assunto; gestos e vestuário parecem contemporâneos. Corpo inteiro, cabeças e mãos seguros. Texto legível e fecho forte.

**Recomendação:** A foto anterior falhava no rodapé; a atual resolve. Não reduzir novamente a folga para ampliar as pessoas. O bloco textual tem intervalos generosos, mas as margens externas continuam maiores; aproximar corpo/fecho é acabamento opcional, sem obrigação.

## Página 10 — APTO com acabamento opcional

Evidência: [snapshot individual](qa_visual_snapshot_20261015T151353Z/pagina_10.png). Dois núcleos editoriais, filete e poço/jarro em faixa direita. A foto corresponde ao exemplo da samaritana como símbolo; topo e piso contínuos livres. Não há corte de texto.

**Recomendação:** João 4 pode ficar cerca de 30–40 px mais próximo do exemplo para reforçar atribuição. Preservar a distinção entre a premissa e o exemplo, sem criar novos cards.

## Página 11 — PENDENTE — bloqueador visual

Evidência: [snapshot individual](qa_visual_snapshot_20261015T151353Z/pagina_11.png). A compactação recente melhorou a relação título/citação/explicação/referência, mas o fecho foi movido para y750 e o filete permaneceu em y780. A linha atravessa a parte inferior de “Quem recebe não guarda para si.”.

**Recomendação:** Mover o filete para aproximadamente y720, deixando o fecho em y750–755; ou remover o filete. Reexportar e abrir a página novamente antes de marcar apta. O texto não está cortado, mas há sobreposição visual confirmada.

## Síntese operacional

**Apto:** páginas 02–10, nos snapshots identificados, com as observações não bloqueadoras descritas.

**Pendente:** página 11 por interseção entre filete e fecho. Ajuste concreto sugerido: filete y720, fecho y750–755; manter 20–30 px de separação visual livre entre a linha e as letras. Uma nova abertura do PNG corrigido deve confirmar a resolução.

Nenhum corte, placeholder ou perda evidente de palavras foi visto nas dez provas. Esse achado visual não substitui a comparação editorial/estrutural de todas as camadas. Cabeçalho, quadrados e marcas estão presentes; a fidelidade completa do molde, das cores e da editabilidade continua com a revisão final do principal.

Diário: `auditoria/execucao/catalogo.jsonl`, eventos `visual-001` em diante. O prompt operacional recebido está preservado literalmente no evento inicial. Todas as ações deste parecer foram de leitura, medição ou documentação.

