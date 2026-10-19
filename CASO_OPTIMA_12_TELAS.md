# Caso aplicado: treinamento Optima — planejamento e execução final

O PDF de conteúdo da palestrante tinha 12 páginas em 1920×1080. A grade v2 preservou **12 telas**, mas simplificou cada uma em blocos de capacidade textual. A tabela abaixo descreve essa **fase de planejamento**, não a arte final. O usuário acrescentou depois uma **13ª página de agradecimento**. A produção aprovada está em `exemplos/optima_final/` (PSD de 13 pastas, PDF, registro de saída, 13 PNGs aprovados, fotos usadas e contato). O texto médico/comercial do PDF original não passou por revisão factual, conforme o escopo pedido pelo usuário.

| Tela | Tema de origem | Fundo do estudo | Composição | Foto |
|---:|---|---|---|---|
| 1 | Desodorante Optima e três pontos | rosa claro | capa tipográfica, H1 + três pontos curtos | nenhuma |
| 2 | Alumínio: contexto | rosa claro | H1 + quatro faixas de texto | nenhuma |
| 3 | O que a ciência sabe, início | malva escuro | H1 + duas colunas longas | nenhuma |
| 4 | O que a ciência sabe, continuação | rosa claro | foto à esquerda + H1 + dois blocos | faixa esquerda `365×540` no estudo |
| 5 | O que a ciência sabe, ressalva | malva escuro | bloco longo + chamada lateral | nenhuma |
| 6 | Magnésio, introdução | rosa claro | produto à esquerda + H1 + dois blocos | faixa esquerda `350×540` |
| 7 | Magnésio, benefícios | rosa claro | H1 + três bullets + produto à direita | faixa direita `340×540` |
| 8 | Óleo de soja | malva escuro | H1 + três cards de propriedades | nenhuma |
| 9 | Pele hidratada e efeito do produto | rosa claro | H1 + três blocos empilhados | nenhuma |
| 10 | Tempo de adaptação | malva escuro | H1 + explicação + dado de duração | nenhuma |
| 11 | Motivos do processo | rosa claro | H1 + três cards | nenhuma |
| 12 | Dicas | rosa claro | H1 + seis itens em duas colunas | nenhuma |

As dimensões de foto são em coordenadas de **960×540** do mockup; no PSD 1920×1080, dobre os valores antes de ajustar à arte final. O campo `photo` sempre atravessa `y=0..540`. As fotos geradas foram três: pele adulta em rosa suave, frasco com minerais, e frasco em cenário rosa. A prévia está em `referencias/exemplos/optima_v2_visao_geral.jpg`; o PDF de placeholders está em `referencias/optima_v2_placeholders.pdf`.

## O que mudou após as correções do usuário

1. A primeira grade tinha todas as telas em rosa. A v2 alterna quatro páginas em malva escuro.
2. A primeira versão tinha foto na capa; a v2 usa só tipografia.
3. A primeira versão tinha fotos menores e recortadas. A v2 usa apenas faixas fotográficas na altura inteira.

Essas três decisões são **regras atuais do usuário** para futuras APNs, não inferências ocasionais deste exemplo.

4. A correção posterior exige **conteúdo real na entrega final**. Rótulos `H1`, `BLOCO`, `ITEM` e capacidades em linhas ficam restritos ao planejamento.

## O que a produção final acrescentou ao método

| Página | Resultado verificável na prova final | Decisão transferível |
|---:|---|---|
| 1 | capa tipográfica rosa, apenas o nome do treinamento como conteúdo | nenhuma foto principal nova nem benefícios; H1 em um objeto editável, com peso/cor variáveis e amplo respiro. O resultado aprovado conserva imagem de marca muito esmaecida |
| 2 | quatro blocos de contexto sobre rosa, com H1 de palavra destacada | corpo branco, largura e espaçamento ajustados ao texto real |
| 3 | fundo malva, H1 `O que a ciência sabe`, dois assuntos em colunas | variar tema e usar duas colunas só quando a leitura de ambos comporta |
| 4 | modelo de coque alto, joias e top sem alças aplicando Optima sobre ambiente doméstico neutro à esquerda; dois assuntos científicos à direita | gerar modelo com transparência real e cena completa separada, compor sem borda reta ou aspecto de estúdio, preservar marcas e área segura |
| 5 | retrato da modelo madura em cena neutra clara à esquerda; malva com H1, subtítulo em faixa e texto à direita | retrato fiel à pessoa, idade natural, margens e respiro para texto |
| 6 | cena integral creme do frasco à esquerda; explicação do magnésio à direita | usar foto real do produto como autoridade física; não alongar a tampa |
| 7 | três retângulos malva com título/corpo e filete branco cruzam a junção rosa/foto espresso do produto | card retangular pensado para o texto; foto contrastante e produto fiel |
| 8 | três cartões numerados e agrupados no PSD à esquerda; foto editorial da soja à direita | centralizar número, título e corpo em cada cartão e entregar o grupo completo para edição humana |
| 9 | foto integral de mulher bem arrumada com Optima em banheiro neutro à esquerda; H1 em um objeto, mini subtítulo e benefícios à direita | equilibrar cor e iluminação, usar cenário neutro e manter o frasco compacto fiel à referência; o teste com recorte transparente foi preservado à parte |
| 10 | explicação longa à esquerda, dado `4 a 8 semanas` e mulher adulta com Optima recortada sobre malva à direita | produto e gesto devem conectar com o assunto; recorte transparente e fundo do slide dispensam cenário escuro artificial |
| 11 | H1 grande à esquerda; três motivos empilhados à direita com filetes finos e corpo branco | substituir colunas mecânicas por sequência alinhada quando o conteúdo pede |
| 12 | seis faixas malva com checks brancos; título `Dicas` à esquerda e a atriz da referência aplicando Optima à direita, sem tatuagem | ajustar uma faixa manualmente como padrão; alinhar texto/ícone; reservar 15% livres no topo e rodapé da foto aplicada |

O usuário mostrou capturas do Photoshop enquanto ajustava o PSD e pediu que os demais cartões seguissem o primeiro cartão reduzido e alinhado por ele. A página 12 final preserva a sequência de seis faixas sobre a divisão rosa/foto. O usuário também pediu H1 em **um único objeto editável**, fotos com menor saturação, fundos creme/espresso e substituição de fotos repetidas. As alterações são observáveis nas provas; sem histórico completo de versões, este registro não atribui cada deslocamento de camada a uma ação manual específica.

Capturas preservadas em `exemplos/optima_final/revisoes_usuario/`: `h1_uma_camada.png` mostra a correção do H1 editável; `cartao_check_alinhado.png` mostra o cartão tomado como padrão; `dicas_espaco_foto.png` mostra a área reservada à nova fotografia; `modelo_margem.png` registra o pedido de enquadramento mais folgado. A foto real de proporção do frasco e o retrato original estão em `referencias/optima_frasco_proporcao_real.png` e `referencias/optima_modelo_referencia.png`.

Outras correções diretas: corpo corrido sempre branco; texto escuro de apoio `#B3718E` no tema claro; Gotham com tracking compacto (-70 H1, -60 corpo como ponto de partida); mini subtítulo e palavra em Bold/rosa claro quando a composição comporta; frasco compacto conforme a foto real enviada; produto gerado como cena nova integral, sem colagem visível; modelo da página 5 com testa e corpo afastados do corte. A página 12 teve uma versão intermediária relacionada a água/aloe, depois substituída pela aplicação espontânea do produto. `DECISOES_APN_BELLAS.md` contém a regra atual consolidada.

**Revisão posterior da página 12:** o usuário pediu voltar ao gesto espontâneo de aplicação, usando a mesma atriz da foto que enviou, o produto Optima, sem a tatuagem do braço. O enquadramento final tem balcão espresso na parte inferior e parede livre no alto. A exigência transferível é manter **15% livres em cada extremidade vertical após o recorte** para cabeçalho e rodapé. O resultado está em `exemplos/optima_final/optima_provas/pagina_12.jpg`; a foto de pose de referência está em `referencias/optima_dicas_pose_referencia.png`. `exemplos/optima_final/scripts_incrementais/replace_photo_12_ritual.jsx` registra a substituição pontual no PSD.

A mesma regra de margem levou ao reenquadramento **intermediário** da foto na página 4, antes cortada no topo. O script daquela fase está em `exemplos/optima_final/scripts_incrementais/replace_photo_04_margens.jsx`; a composição final posterior aparece na revisão abaixo. As fotos de produto das páginas 6 e 7 já mantinham o assunto centralizado com folga vertical; o retrato da página 5 conserva espaço para cabeçalho e rodapé sobre o cenário.

**Fase intermediária da página 10:** a área branca da direita recebeu uma foto integral de uma mulher adulta de aparência natural, num momento cotidiano, sobre fundo espresso. O rosto ficou afastado da área onde o cartão `4 a 8 semanas` avançava sobre a foto. Uma primeira versão tentou criar contraste para LUCI|LUCI com uma faixa horizontal escura; o usuário rejeitou esse recorte artificial e mostrou um exemplo de cena contínua. A versão seguinte estendeu piso e roupa escuros naturalmente até a base. O asset histórico é `optima_assets/foto_10_adaptacao_cena_continua.png`; a composição final foi alterada novamente, como descrito abaixo. A diretriz transferível é pedir pessoas individuais e críveis, preservando textura de pele, sinais da idade e pequenas assimetrias, e compor margens seguras dentro da própria fotografia.

**Fase intermediária da página 9:** os três argumentos antes ocupavam uma coluna extensa num fundo rosa uniforme. Após comparar as quatro fontes já catalogadas, a tela passou a usar foto de cuidado da pele em toda a altura à esquerda, H1 com dois pesos/cores num só objeto, mini subtítulo branco e três faixas de benefício alinhadas à direita. Corpo e dados originais foram preservados. `LEITURA_VISUAL_4_PDFS.md` documenta todas as 65 páginas reenviadas e indica as referências de composição usadas aqui. O script daquela fase é `exemplos/optima_final/scripts_incrementais/redesign_page_09_hidratacao.jsx`; a foto final foi substituída como descrito abaixo.

## Arquivos e fases

### Revisão final incorporada ao PSD principal

**Exportação após novas edições manuais — correção do método:** o Photoshop informou `ColorProfile.NONE`. A tentativa de atribuir `sRGB IEC61966-2.1` numa duplicata e exportar 12 JPEGs com ICC deixou o malva opaco; esses JPEGs em `optima_provas/` e os scripts `export_all_srgb.jsx`/`build_srgb_pdf.py` são históricos e **não representam o resultado aprovado**. Os 13 PNGs que o usuário salvou em `pngs_aprovados/` são a referência final. Um teste de Save for Web PNG24 (`convertToSRGB=true`, `includeProfile=true`) em duplicata **sem atribuir perfil** reproduziu os 13 PNGs pixel a pixel; o PDF final foi montado sem reamostragem e seus pixels extraídos conferidos contra esses PNGs. O método reproduzível está em `scripts/exportar_pngs_bellas.jsx` e `scripts/montar_pdf_dos_pngs.py`. A página 4 aprovada mostra a modelo recortada sobre rosa; o ambiente fotográfico anterior é histórico. A capa traz `TREINAMENTO` e `Desodorante OptimaPlus`, sem benefícios.

As descrições históricas acima registram tentativas e decisões intermediárias. A primeira composição com essa modelo substituiu a antiga foto marrom da página 4 por uma **modelo gerada do zero em PNG com transparência real**, de coque alto, joias e top sem alças, aplicando o frasco Optima. O ambiente neutro, com sinais de um banheiro usado de verdade, foi gerado separadamente e combinado no PSD. Na edição manual mais recente, o usuário retirou o ambiente e deixou a modelo diretamente sobre rosa. A figura conserva margem para cabeçalho e assinatura, sem corte reto artificial no ombro.

Na página 10, a mulher com toalha e frasco compacto Optima foi igualmente gerada do zero como recorte transparente. O fundo malva do próprio slide substitui a cena marrom; o cartão `4 a 8 semanas` e LUCI|LUCI permanecem legíveis. A roupa escura e a toalha clara dão contraste sem faixa pintada. O recorte permite reposicionar a modelo independentemente dos textos.

A página 8 passou a usar três cartões numerados, com cada cartão completo agrupado em uma pasta do PSD e foto editorial da soja à direita. A página 9 mostra uma mulher adulta bem arrumada, com traços reais e frasco fiel, num banheiro claro e neutro. A capa contém somente o título do treinamento como texto de conteúdo. Foi preservado um PSD/JPG **alternativo** da página 9 com modelo recortada para testar essa linguagem sem sobrescrever a composição aprovada.

Arquivos incrementais: `scripts_incrementais/apply_cutouts_04_10.jsx`, `redesign_page_08_soja.jsx`, `align_group_page_08.jsx`, `update_cover_and_photo_09.jsx`, `refine_test_photo_09_cutout.jsx`; os arquivos `export_all_srgb.jsx` e `build_srgb_pdf.py` registram a exportação rejeitada. As fotos usadas e os assets históricos estão em `optima_assets/`; as **provas atuais aprovadas** estão em `pngs_aprovados/`.

- Fonte integral: `referencias/optima_conteudo_original.pdf` e `referencias/optima_conteudo_extraido.txt`.
- Layout planejado: `exemplos/optima_manifest_placeholders.json` e PDF v2 de placeholders.
- Exemplo editável histórico: `exemplos/planejamento/optima_placeholders_editavel.psd`, provas e contato. Contém rótulos temporários e **não é uma APN final**.
- Conteúdo real preparado: `exemplos/optima_manifest_conteudo_real.json`. Contém os textos integrais, referências por página/bloco e fotos recortadas; passou na validação de contrato final. A geometria veio do planejamento e precisa de ajuste/prova no Photoshop antes de ser arte final.
- Produção final: `exemplos/optima_final/optima_apn_bellas_final.psd`, PDF, `optima_registro_final.json`, fotos, 13 PNGs aprovados, contato e `optima_codigo_historico.zip`. O registro final é um inventário de saída, **não** um manifesto compatível com `validar_manifest.py`. Os scripts do ZIP são exemplos de alterações incrementais, com caminhos antigos a adaptar; a exportação nele é histórica/rejeitada. Consulte `REGISTRO_DA_EXECUCAO.md` para distinguir esta fase da integração anterior. O manifesto do planejamento, sozinho, não comprova encaixe visual.

`scripts/preparar_optima_conteudo_real.py` reconstrói o manifesto a partir da extração e do layout planejado, conferindo o número de blocos por página. A única normalização textual feita, além de espaços/quebras de linha, une `TRANS-RESVERATROL` quebrado pela extração do PDF; a chamada sobre aerossol da página 5 é separada em sua própria caixa.
