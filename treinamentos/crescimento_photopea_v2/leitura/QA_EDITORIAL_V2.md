# QA editorial — Crescimento V2

**Concluído no escopo editorial. Nenhuma omissão, diferença de texto ou corte de conteúdo detectado.**

Corte desta revisão: **15/10/2026, 12:23:51 −03:00**. Revisor: conteudo_novo_v2. Esta conclusão se aplica somente às versões identificadas abaixo.

## Fontes e método

A fonte editorial é `leitura/conteudo_v2.json`, transcrição independente dos nove PNGs originais. Não foi consultado treinamento, PSD, prova ou manifesto da versão anterior de Crescimento.

Foram realizados três controles complementares:

1. Comparação dos **40 blocos da fonte** ao texto nativo efetivamente extraído do PSD final por psd-tools 1.25.0: **85 componentes**, incluindo números, títulos, ações e referências, sem diferenças após normalizar somente espaços/quebras.
2. Comparação das **88 entradas de texto do manifesto final** às camadas nativas correspondentes, inclusive dentro de pastas agrupadas: **88/88 iguais**. Nenhuma camada de texto esperada apresentou visibilidade local desligada ou opacidade zero. Os grupos de página podem estar ocultos para alternância de telas; a visibilidade final de conteúdo foi avaliada nas provas, não inferida desse inventário.
3. Leitura visual integral dos **12 PNGs finais em 1920×1080**, contra a transcrição. Todos os textos de conteúdo foram vistos; nenhum trecho cortado, omitido ou encoberto foi identificado.

O PSD contém **88 camadas nativas de texto**. Além dos componentes da fonte, há os três textos fixos “TREINAMENTO”, “OBRIGADA!” e “EMPREENDEDORISMO FEMININO”. Cabeçalhos/logos também podem conter partes rasterizadas; sua reconstrução e fidelidade de template não integram este parecer.

## Resultado por página

| Página | Conteúdo da fonte | Camadas nativas | Resultado editorial da prova final |
|---|---|---:|---|
| 01 | Crescimento | 2 | Título íntegro e legível; sem conteúdo variável adicional |
| 02 | Todo mundo quer crescer; preparação; itens 01–04 | 10 | Quatro itens, números e premissa presentes; nenhuma omissão |
| 03 | Jesus sabia para que veio; propósito; Sua direção | 3 | Três blocos íntegros; pronomes e sentido preservados |
| 04 | Episódios 01–04 | 17 | Números, nomes, ações e quatro referências completos e visíveis; agrupamento não suprimiu texto |
| 05 | Episódios 05–08 | 17 | Quatro episódios e referências completos; Ele, Suas e dEle preservados |
| 06 | Episódios 09–12 e fecho | 18 | Doze episódios completados na ordem; “Salva-te a ti mesmo”, referências e fecho visíveis |
| 07 | Ele foi até o fim; Está consumado; João 19:30 | 3 | Título, citação e referência íntegros |
| 08 | Jesus preparou pessoas; prepararam outras; até chegar a nós | 3 | Cadeia completa; correção de regência já documentada preservada |
| 09 | Crescimento; preparar pessoas; propósito; não parar em nós | 4 | Quatro blocos íntegros e conclusões preservadas |
| 10 | Nem todas precisaram de anos; samaritana; João 4 | 4 | Ressalva, exemplo e referência presentes sem corte |
| 11 | Encontrou Jesus; convite; testemunho; João 4:29, 39; fecho | 5 | Cinco blocos íntegros. Filete visto abaixo da referência, sem atravessar texto; fecho completo |
| 12 | Agradecimento fixo | 2 | “OBRIGADA!” e cabeçalho vistos; conteúdo textual íntegro |

**Cobertura final:** 40/40 blocos; 4/4 preparações; 12/12 episódios; 12/12 referências da série; 3/3 outras referências; todas as conclusões preservadas.

As repetições de “Tentaram mudar Sua direção” nas páginas 04–06 são títulos de continuação. “A multidão” aparece nos episódios 03 e 10 com eventos diferentes, conforme a fonte. “Jesus preparou pessoas” nas páginas 08 e 10 já é repetido nos originais. Não há repetição indevida detectada.

As intervenções editoriais permanecem restritas às registradas na revisão inicial: caixa/quebras, pontuação e “Até chegar em nós” → “Até chegar a nós”. Não foram acrescentadas interpretações, versículos integrais ou novas conclusões. Números de capítulos/versículos e o sentido de “nem todas precisaram de anos” foram mantidos.

## PDF entregue

O PDF final possui **12 páginas**, cada uma com uma imagem. As 12 imagens extraídas do PDF correspondem exatamente, em dimensões e bytes RGB, aos 12 PNGs que foram lidos visualmente nesta revisão. Assim, a leitura editorial das provas cobre o conteúdo incorporado no PDF entregue.

Este vínculo não é aprovação de cor/perfil nem da reprodução do molde do Photoshop. Não foi feita renderização independente do PDF por outro visualizador; a evidência utilizada foi a extração das imagens incorporadas.

## Versões e evidências

| Arquivo | SHA-256 |
|---|---|
| `entrega/Crescimento_Photopea_V2.psd` | `ced7857b6168c1a5f008f6775b433191a62bd5562b202f93267ef1ba74470bb7` |
| `manifest_photopea.json` | `98e986cc2b5c33c7c4862966f0a57ca2078e7b9a8d3a6d67b07f9604b326d457` |
| `leitura/conteudo_v2.json` | `cd6c918de25147bc4dbada2e6bd6ae5b7dc109f072551e01a711f2a52491236f` |
| `entrega/Crescimento_Photopea_V2.pdf` | `8b091a380833f74827241a89a9b89726226c2ca67a37372e00fc99acea6050d1` |

Evidências locais:

- `auditoria/editorial_final_text_layers.json`: extração independente de cada camada nativa de texto final, com caminho/página, texto, visibilidade local, opacidade e limites.
- `auditoria/editorial_final_comparacao.json`: 85 controles da fonte e 88 do manifesto; zero diferenças.
- `auditoria/editorial_pdf_provas_final.json`: contagem PDF, igualdade das imagens e hashes dos 12 PNGs.
- `auditoria/execucao/conteudo.jsonl`: diário incremental; prompts, parâmetros de inspeção visual, scripts/patches literais, resultados e limites.
- `auditoria/execucao/revisar_editorial_psd_final.py`: versão executada do comparador.
- `auditoria/execucao/conferir_pdf_provas_editorial.py`: versão executada com pypdf. A primeira tentativa usando fitz falhou por dependência ausente e foi preservada em `conferir_pdf_provas_editorial_v1_fitz.py`; a falha e a reexecução estão registradas.

## Histórico e limite do aceite

A revisão intermediária conferiu o manifesto anterior SHA `3FD0D8722563E557E376B68E1305710A1DE02CE9DD78F34E8FED591FE6B88BF1`, com 86 textos previstos, e deixou PSD/PNGs pendentes. Ela foi superada pela conferência final acima; os eventos não foram apagados do diário.

Durante o fechamento, o manifesto mudou de `a36e1fa89870094b9a6421d29898e95350236ae663d46f5a4e67ab5d6f57fd55` para a versão da tabela. A comparação foi reexecutada integralmente às 12:23:51 −03:00: os 85 componentes da fonte e 88 textos do manifesto continuaram iguais ao mesmo PSD final, sem diferenças.

**Aceite restrito à fidelidade editorial e à integralidade visual dos textos nas provas identificadas.** Não aprova igualdade de pixels da capa/agradecimento ao molde, gerenciamento de cor/perfil, fidelidade de template, qualidade fotográfica ou fontes tipográficas. A validação factual/teológica das referências e afirmações permanece fora do escopo. Não foi realizada nenhuma edição no PSD, PDF ou PNGs finais por este revisor.

