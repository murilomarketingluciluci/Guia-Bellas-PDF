# QA visual V2 — suplemento do conjunto final

**APTO visualmente: páginas 01–12 de `entrega/pngs/`, nas versões identificadas abaixo. Nenhum bloqueador visual permanece.** Este suplemento substitui o estado pendente do parecer intermediário; o documento anterior e seus snapshots continuam como histórico.

Revisor: `catalogo_novo_v2`. Revisão de 15/10/2026, ponto de corte das métricas **2026-10-15T15:20:52.566813+00:00**. As 12 telas foram abertas individualmente em 1920×1080. Capa/agradecimento foram comparados visualmente aos PNGs aprovados 01/13 de Optima. O revisor não alterou arte, PSD ou API.

## Versão examinada e alcance

- PSD: [Crescimento_Photopea_V2.psd](../entrega/Crescimento_Photopea_V2.psd), SHA-256 `ced7857b6168c1a5f008f6775b433191a62bd5562b202f93267ef1ba74470bb7`.
- PDF inventariado: [Crescimento_Photopea_V2.pdf](../entrega/Crescimento_Photopea_V2.pdf), SHA-256 `8b091a380833f74827241a89a9b89726226c2ca67a37372e00fc99acea6050d1`. Esta revisão abriu os PNGs finais; não fez inspeção independente das páginas internas do PDF.
- Manifesto examinado: SHA-256 `98e986cc2b5c33c7c4862966f0a57ca2078e7b9a8d3a6d67b07f9604b326d457`. A [direção](direcao_catalogo_v2.md) e os [layouts propostos](layouts_propostos_v2.json) são referências de intenção; diferenças de posição destinadas a encaixe foram avaliadas na arte real.
- [Inventário de hashes e métricas](QA_VISUAL_V2_FINAL_metricas.json) vincula individualmente todos os 12 PNGs e as fontes documentais. [Script exato de medição](medir_qa_visual_final.py).
- [Inventário de reabertura](../auditoria/reabertura_psd.json) identifica o mesmo SHA do PSD. O [relatório de pixels pós-reabertura](../auditoria/pixels_reabertura.json) registra igualdade nas 12 páginas. São evidências técnicas do principal lidas por este revisor; a aprovação visual vem das imagens abertas.
- Corpo branco, alternância claro/escuro e destaques em Gotham permanecem visualmente consistentes. Este parecer não substitui a auditoria de famílias/runs das camadas nem a comparação editorial dos 40 blocos.

## Correções verificadas

**06 — resolvida.** A fotografia foi escurecida sem faixa pintada. O microcabeçalho branco agora é identificável sobre o céu e não se perde como na primeira prova. A sonda nos mesmos oito pontos de fundo resultou em **3,18–4,12** de razão contra branco, ante 1,64–2,07 na prova inicial. Não é teste de conformidade tipográfica; confirma o ganho observado. As quatro faixas mostram número, nome, descrição e referência completos por cima dos fundos. O fecho também está visível, sem contato com a marca. A cena preserva continuidade, caminho reconhecível e saturação contida.

**11 — resolvida.** O filete está em y715–717 e o fecho tem os primeiros pixels brancos em y751: **33 linhas livres** entre ambos. Não há mais linha atravessando letras. Título, citação, explicação, atribuição e fecho formam um conjunto compacto com margem externa ampla.

**09 — resolvida.** Assunto humano delimitado manualmente em aproximadamente y327–820, incerteza de 6 px, deixando **30,3% no topo e 24,1% no rodapé**. O mínimo é 162 px/15% em cada extremidade. Cabeças, mãos e calçados estão seguros. A folga é pavimento/teto contínuos da própria cena. A conversa entre três mulheres de idades distintas continua legível, com roupas contemporâneas e aparência natural. Não ampliar novamente as pessoas à custa dessas margens.

**08 — sem defeito confirmado.** Nova sonda do PNG final confirma três marcos de 24×24 px em x340–363, x1000–1023 e x1600–1623, y398–421, com eixo de 3 px em y410–412. A barra larga percebida em preview não existe nos pixels. Não há motivo para correção gráfica.

## Parecer por página

| Página final | Estado e evidência visual | Relação com catálogo/decisão |
|---|---|---|
| [01](../entrega/pngs/pagina_01.png) | **APTO.** Só “Crescimento” como título variável; etiqueta, cabeçalho, quadrados, marcas e imagem de marca muito esmaecida preservados visualmente. Sem subtítulo ou chamada. | Composição aprovada de Optima 01/molde de capa. Título de uma linha mantém o eixo e não invade a margem. |
| [02](../entrega/pngs/pagina_02.png) | **APTO.** Tese lateral e quatro condições completas em lista, hierarquia clara. | Finanças p7; filetes apoiados também em Optima 11. O comprimento dos dois filetes de itens curtos é acabamento opcional. |
| [03](../entrega/pngs/pagina_03.png) | **APTO.** Conjunto tipográfico curto e fotografia arquitetônica direita; respiro amplo. | Oito Passos p4. Eixo da arcada comunica direção; foto fullheight, topo estrutural e piso livres de foco relevante. |
| [04](../entrega/pngs/pagina_04.png) | **APTO.** Quatro registros largos com nomes, ações e referências visíveis, sem grade de cards. | Colágeno p23. Aproximar horizontalmente nomes/ações seria refinamento opcional. |
| [05](../entrega/pngs/pagina_05.png) | **APTO.** Título lateral e episódios 05–08 em coluna, alinhamentos regulares e leitura integral. | Namorados p10 e Finanças p7. Recorrência com 02 é espaçada e atende a densidade diferente. |
| [06](../entrega/pngs/pagina_06.png) | **APTO.** Faixas, textos e fecho completos, header com ganho efetivo de contraste. | Rosângela p14. Foto costeira e passagem rochosa representam permanência/caminho, sem repetir o assunto de 03. |
| [07](../entrega/pngs/pagina_07.png) | **APTO.** Pausa de citação com referência próxima, margens generosas e impacto. | Finanças p16. Não pede foto ou decoração extra. |
| [08](../entrega/pngs/pagina_08.png) | **APTO.** Três estações abertas da cadeia de preparação; fonte completa e marcos corretos. | Oito Passos p31/p29. Elementos ligados pelo eixo sem transformar cada frase em cartão. |
| [09](../entrega/pngs/pagina_09.png) | **APTO.** Pessoas e texto em níveis distintos, margens fotográficas comprovadamente amplas. | Mulheres p8 e Etiqueta p3. Foto humana reforça o propósito em pessoas. |
| [10](../entrega/pngs/pagina_10.png) | **APTO.** Dois núcleos editoriais e poço/jarro à direita. Texto sem corte, relação com a samaritana clara. | Etiqueta p3/Oito Passos p4. João 4 poderia aproximar-se cerca de 30 px do exemplo; refinamento opcional. |
| [11](../entrega/pngs/pagina_11.png) | **APTO.** Filete separado do fecho, todos os níveis visíveis. | Posicionamento p7/Mulheres p5. Citação e consequência agrupadas sem ocupar artificialmente toda a altura. |
| [12](../entrega/pngs/pagina_12.png) | **APTO visualmente.** “OBRIGADA!”, fotos de marca esmaecidas, cabeçalho, quadrados e logos mantêm a composição aprovada. | Comparação direta com Optima 13; detalhes quantitativos abaixo. |

As páginas referidas nos PDFs correspondem aos números humanos das páginas integrais arquivadas em [catálogo integral](catalogo_integral/renders_index.json), não a uma escolha feita apenas por miniaturas.

## Fidelidade do agradecimento e da capa

A reconstrução conserva visualmente a composição fixa e não introduz conteúdo. A página 12 é equivalente visualmente à referência aprovada; **não é pixel a pixel idêntica ao PNG Optima**: a comparação RGB tem diferença média absoluta de **0,689 por canal em escala 0–255**, máximo 90 e 17,18% dos pixels exatamente iguais. A média pequena é consistente com diferenças sutis, mas este revisor não atribui causalidade única sem isolar cada camada. A igualdade 12/12 após reabrir o PSD é outra comparação: diz respeito à persistência da V2, não à identidade com Optima.

Na capa, a mudança do título é autorizada. A imagem de marca quase transparente corresponde à composição fixa; não há fotografia nova destacada na capa. Não vi perda de marca, corte no título ou chamada editorial acrescentada.

## Imagens, variedade e respiro

Os quatro assuntos variam **arquitetura, paisagem, pessoas e poço/objeto**. Correspondem às ideias específicas de direção, perseverança, preparação humana e samaritana; não são fotos genéricas repetidas de uma mesma mulher. Todas encostam em uma lateral e ocupam altura integral, com proporções naturais e sem emenda horizontal aparente. As áreas superiores e inferiores são continuidade natural das cenas. Na 03 o piso e o teto enquadram a arcada; na 06 o caminho entra no rodapé como ambiente contínuo, sem rosto ou produto ali; na 10 o foco do jarro/abertura fica na zona central e o piso inferior fica livre. A regra de 15% foi verificada quantitativamente para as pessoas da 09 e visualmente para os focos das demais.

Há variação real entre lista vertical, registros horizontais, faixas, processo aberto, citação, coluna lateral e bloco compacto. Não aparece uma fórmula repetida de H1 duas linhas com quatro cards 2×2. As repetições de 02/05 e 03/10 são espaçadas e têm densidade/função diferentes. Os intervalos internos permanecem menores que o respiro externo na leitura global; não se recomenda espalhar mais os blocos para preencher as telas.

**Pendências visuais bloqueadoras: nenhuma neste conjunto de hashes.** As sugestões opcionais de 02/04/08/10 não impedem a entrega. A validação técnica/editorial final, o PDF e a cobertura da auditoria devem ser consolidados pelo principal em seus próprios relatórios, sem transformar este parecer em prova de verificações que ele não executou.

## Pedido recebido, literal

Registro também preservado no diário do agente (`visual-final-001`), antes das ações finais. Não é transcrição de sistema/desenvolvedor nem raciocínio privado.

> Conjunto final para revisão é entrega/pngs/pagina_01.png...pagina_12.png (não provas/ antigo). PSD entrega/Crescimento_Photopea_V2.psd sha ced7857b6168c1a5f008f6775b433191a62bd5562b202f93267ef1ba74470bb7. Arquivo foi reaberto naAPI;auditoria/reabertura_psd.json inventariaactual;pixels_reabertura.json compara12PNGs. Alterações recentes: foto09reenquadrada com30%topo/24%rodapé; Photo06brightnessEvent real -35 (DOM adjustBrightnessContrast era indefinido, no-op), fecho11y750/filete715; textosda06foramrecolocadosacimafaixasdepoisdeagrupamento. Marcadores08têm24pxcada—sondapixelconfirma queabarraaparenteerapreview/ilusão, nãodefeito. Faça suplemento final do parecer atual comversões/SHAs eaptooupendências; confira06/11e12/capareconstruídas e imagemadequação/variação. Nãoalterearquivosarte;registreessepromptliteral.

Diário: [catalogo.jsonl](../auditoria/execucao/catalogo.jsonl), eventos `visual-final-001` em diante. A releitura do parecer/documentação em `visual-final-004` teve registro posterior explicitamente declarado; as aberturas individuais, script e medições finais têm pares antes/depois.
