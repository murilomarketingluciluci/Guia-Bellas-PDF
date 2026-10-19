# Decisões verificáveis da montagem Photopea

Esta é uma versão nova de Crescimento, refeita com a fonte original de nove artes e outras composições do catálogo. A versão anterior de Crescimento não foi usada como arte doadora. O molde Bellas e Optima aprovado são referências de identidade.

## Autorização e mapa

O usuário dispensou a aprovação intermediária: “nao prepare mapa visual pra aprovação quero testar seu conhecimento e capacidade de modelo e estrutura agentes.. faça do zero até o fim do entregável use validadores dos proprios agentes seus use sub agentes pra fazer isto”. O pedido posterior de começar outra versão não revogou essa autorização. A direção foi documentada para rastreabilidade, sem tratá-la como aprovação explícita de um mapa. A escolha de Photopea substituiu, para este experimento, o backend Photoshop/COM previsto no pacote.

## Backend efetivamente usado

Toda montagem, texto novo, posicionamento, crop, exposição, agrupamento, exportação PNG e gravação/reabertura do PSD foram executados pela API Live Messaging do Photopea. Python/psd-tools preparou inputs técnicos das camadas originais, copiou fontes/assets e fez validação; não compôs páginas finais. A montagem do PDF incorporou os PNGs exportados, sem reamostragem.

O PSD completo do molde não abriu corretamente neste ensaio. Foram preservados separadamente canais, máscaras, transforms e payloads originais. Três cópias técnicas de entrada trocaram Smart Object por PixelLayer mantendo pixels/máscaras/bbox/blend/opacidades; essa perda de editabilidade de SO está declarada. Os payloads originais permanecem em assets/base_molde/. Nenhuma página final é um placeholder.

## Ensaios e correções

- Um documento pequeno provou texto Gotham, PNG, PSD e reabertura antes da montagem.
- A ponte passou a usar um marcador de término por script e contagem de binários. Mensagens “done” intermediárias não são prova de conclusão.
- Os grupos de página passaram a ser criados com o fundo de raiz selecionado para evitar aninhamento na página anterior.
- Camadas duplicadas recebem o sufixo “ copy”; a seleção passou a usar identificador da camada importada, em vez de presumir a seleção ativa.
- O setter totalTextStyle não aplicou a mudança observada; os estilos internos foram escritos com Action Manager e conferidos na imagem e no PSD.
- O primeiro método DOM de brilho era indefinido e não modificou pixels. O ajuste efetivo da foto 06 foi feito por brightnessEvent, -35, contraste 0, no próprio Photopea.
- A primeira foto 09 não reservava 15% abaixo dos sapatos. Uma nova geração ampliou a cena continuamente; a revisão mediu aproximadamente 30% livres acima e 24% abaixo. O original rejeitado foi preservado.
- A impressão de uma barra contínua na página 08 foi rejeitada após medir pixels: existem três marcos de 24×24px. A hipótese visual não é registrada como defeito confirmado.
- Na aproximação do fecho 11, o filete passou a cruzar letras; foi movido para y715, com o fecho em y750.
- Ao organizar faixas da página 06, o fundo do bloco ficou à frente do texto. A ordem foi corrigida e a exportação/reabertura repetida. A hipótese inicial de subgrupo oculto foi rejeitada: a leitura do PSD mostrava grupos e textos visíveis.

## Limites de fidelidade e aprovação

Os fundos de conteúdo foram restaurados aos RGB medidos nos PNGs aprovados (#FBA9C3 e #BC718C); os destaques seguem #B3718E onde prescrito. A renderização de capa e agradecimento no Photopea não é pixel idêntica à exportação Photoshop histórica. O validador estrito original permanece reprovado nesses dois testes, com diferenças medidas no relatório técnico. Não foi criada uma falsa baseline aprovada a partir do próprio resultado novo.

A comparação do PSD salvo/reaberto confirmou as 12 páginas com os mesmos pixels dos PNGs finais. O PDF contém exatamente os RGB desses PNGs. Isso prova consistência da entrega, não equivalência binária ao Photoshop nem aprovação humana da projeção.

## Cobertura da auditoria

Os scripts JSX realmente enviados estão em auditoria/scripts_executados/, e as requisições/resultados em execucao/photopea_api.jsonl. O diário principal registra comandos, parâmetros, patches e justificativas operacionais. Scripts Python tiveram alterações registradas em patches; nem toda execução recebeu um snapshot Python separado. Delegações recentes foram pré-gravadas em prompts/. Há recuperação posterior explicitamente rotulada e mensagens cifradas que não puderam ser recuperadas. Não há promessa de cobertura literal de 100% da sessão.

Não são incluídos raciocínio privado, mensagens protegidas de sistema/desenvolvedor ou credenciais. “Modelo configurado” não é prova da identidade interna de serviços de geração. O resumo histórico SESSAO.md conserva seu corte intermediário; os pareceres finais e QA_FINAL.md registram o estado entregue.
