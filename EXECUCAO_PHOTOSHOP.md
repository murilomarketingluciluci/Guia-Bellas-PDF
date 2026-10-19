# Execução por script no Photoshop

Este pacote produz **APNs finais com conteúdo real por script no Photoshop**, usando um manifesto JSON por apresentação. Para um treinamento novo, peça somente o PDF original sem edição, releia o repertório Bellas e apresente **primeiro um mapa visual com placeholders para aprovação** (`FLUXO_NOVO_TREINAMENTO.md`). Embora temporários, esses placeholders devem ocupar áreas calculadas com o texto real em Gotham/escala do PSD. Depois do mapa aprovado, faça a direção das imagens e a produção final a partir de uma cópia de `referencias/molde_bellas_aprovado_capa_temas_agradecimento.psd` (`MODELO_REUTILIZAVEL.md`). O manifesto final declara `stage: "final"`, usa `text` com o conteúdo real e não contém campos `placeholder`. Edite Photoshop exclusivamente por JSX/COM, nunca por computer-use.

Este é o procedimento do **backend padrão**. Se o usuário pedir a API do Photopea ou outro editor, mantenha o contrato de `AGENTS.md`, `FLUXO_NOVO_TREINAMENTO.md` e `QA_FINAL.md`. Antes do lote, teste importação/reabertura do molde e uma página com Gotham e texto real; compare capa/agradecimento, editabilidade das camadas, cor e ICC de PNG/PDF. O manifesto específico de outro backend deve ser validado antes da produção em seu próprio esquema; convertê-lo depois para satisfazer um validador não comprova que o planejamento foi dimensionado corretamente. Registre perdas concretas, sem chamar de versão homologada uma reconstrução aproximada.

## 1. Fonte editável confirmada

O **molde operacional aprovado** é `referencias/molde_bellas_aprovado_capa_temas_agradecimento.psd` (1920×1080, quatro grupos: capa, tema claro vazio, tema escuro vazio e agradecimento). `referencias/molde_v1_0_base.psd` é uma cópia histórica de `C:\Users\Murilo\Documents\Projetos\Bellas\Moldes Apn Fundo e Padrão\molde v1.0.psd`; seus grupos originais são `CAPA`, `molde escuro`, `molde claro` e `Plano de Fundo`. Use os nomes/IDs atuais da sessão, pois o usuário pode editar o arquivo entre execuções.

O documento editável Rosângela é referência para estilo de texto e espaçamento. Não substitua o arquivo principal: salve uma cópia de trabalho com nome novo e exporte provas dela. **Para novos treinamentos, preserve a capa e o agradecimento que já estão no molde operacional; mude somente o título da capa.** O grupo `CAPA` do molde bruto e o antigo procedimento de começar de `molde claro` são registros históricos anteriores à capa aprovada.

O pacote inclui provas do molde em `referencias/exemplos/molde_capa.jpg`, `molde_claro.jpg` e `molde_escuro.jpg`. Elas ajudam a localizar microcabeçalho, três quadrados e logos, mas a referência visual aprovada é `exemplos/optima_final/pngs_aprovados/`. A capa aprovada mantém título editável, identidade fixa e imagem de marca muito esmaecida na base. Não acrescente nova fotografia principal, subtítulo ou benefícios.

## 2. Contrato do manifesto

**Final novo: versão 2.0 em `CONTRATO_MANIFESTO.md`.** O exemplo abaixo é um fragmento geométrico, não um manifesto final completo. Acrescente proveniência, IDs, nomes reais das pastas/camadas, fontes, cores e estilos conforme aquele contrato. O esquema lógico é comum aos editores; a adaptação retrospectiva de uma entrega histórica continua sendo apenas diagnóstico.

O JSON tem `stage`, `canvas`, `template` e `slides`. Cada slide declara `number`, `name`, `theme` (`claro`/`escuro`) e `elements`. Cada elemento traz `role` (`h1`, `body`, `bullet`, `card`, `callout`, `photo` etc.) e `rect` **normalizado** `[x,y,w,h]`, com origem no canto superior esquerdo. No planejamento, textos podem ter `placeholder`. Na produção final, todos têm `text` real; fotos têm `asset` e `fit: "cover"`. `template.psd` e assets são relativos à pasta do manifesto; calcule o caminho relativo até `referencias/molde_bellas_aprovado_capa_temas_agradecimento.psd` a partir da pasta real do novo manifesto e valide sua resolução.

Exemplo:

```json
{
  "number": 4,
  "name": "Continuação",
  "theme": "claro",
  "elements": [
    {"role": "photo", "rect": [0, 0, 0.38, 1], "asset": "assets/foto_pele.png", "fit": "cover"},
    {"role": "h1", "rect": [0.42, 0.12, 0.51, 0.16], "text": "Como a pele se protege"}
  ]
}
```

A regra `rect` é **geometria da área**, não tipografia. O script deve ler o estilo do documento Bellas editável e aplicar a família/peso/tamanho corretos ao papel do elemento. A largura/altura em pixels é `rect × canvas`; assim o exemplo `x=0.42` vira `806.4 px` em 1920.

## 3. Preparação e validação

**Pré-checagem obrigatória de treinamento novo:** execute `python scripts/verificar_molde.py` e crie a cópia de trabalho a partir do PSD aprovado de quatro grupos. Valide o manifesto corrente com `--require-approved-template`. O exemplo Optima é referência visual; nunca o abra como fonte de grupos. Em Crescimento/Luciane, o script inicial apagou os grupos do molde e copiou capa/agradecimento do PSD Optima, trazendo três textos antigos ocultos. Migrar depois para o molde correto não removeu essas camadas. Quando a tarefa for continuar um PSD já editado pelo usuário, preserve esse PSD e inspecione todas as camadas, inclusive ocultas, antes de tocar nele.

1. Faça inventário do PSD aberto por script: nome/caminho, largura/altura, grupos top-level, visibilidade, tipo de camada, bounds, fonte e tamanho das camadas de texto. Registre o mapa de camadas antes de mutar.
2. Reutilize a **capa aprovada** como primeira tela, trocando apenas o título, e a **tela de agradecimento aprovada** como última. Para as páginas intermediárias, duplique `TEMA CLARO VAZIO - DUPLICAR` ou `TEMA ESCURO VAZIO - DUPLICAR` conforme o mapa aprovado. Garanta que cada tela herde a versão correta de cabeçalho/rodapé/marca d'água.
3. Reaproveite estilos de texto verificados no documento Rosângela. Se alguma camada não puder ser lida ou a fonte estiver ausente, pare antes de produzir dezenas de telas divergentes.
4. Valide o planejamento com `python scripts/validar_manifest.py exemplos/optima_manifest_placeholders.json --stage planejamento`. **Aprovação do mapa visual pelo usuário vem antes da direção de imagens.** Para produzir, valide o manifesto real com `python scripts/validar_manifest.py CAMINHO_DO_MANIFEST_FINAL.json --stage final`. Esse passo rejeita campos/rótulos de placeholder, fotografia nova na capa, fotos ambientais sem altura completa e caminhos ausentes. Corrija antes de executar Photoshop.
5. Resolva os caminhos de `asset` relativos ao manifesto e confirme dimensões das fotos. Abra/corte por `cover` sem deixar faixa vazia e sem esticar a imagem.

## 4. Geração

Antes de repetir cores em todas as páginas, crie um cartão/fundo/apoio de prova na **cópia** do PSD e exporte pela rota final. Meça o RGB do PNG e compare com os PNGs aprovados. Não use o HEX alvo da exportação como valor armazenado no PSD sem testar: essa confusão criou a primeira paleta saturada de Crescimento/Luciane. Para composição, decida gesto narrativo e hierarquia antes de copiar uma geometria do catálogo; consulte `DIRECAO_DE_ARTE.md`.

Antes de produzir o conjunto, renderize também uma tela densa e uma de impacto com os textos reais em Gotham pela **mesma rota final**. Compare o tamanho aparente do H1, a relação com o corpo e o primeiro foco com páginas aprovadas em 1920×1080 e em contato reduzido. Corrija o mapa e os estilos antes de replicar a página. Uma geometria variada não compensa um H1 sem presença; a regra de H1 em uma camada trata de editabilidade, não determina a ênfase.

O executor deve trabalhar numa **cópia** do molde aprovado de quatro grupos e produzir **um único PSD**. Cada página fica em uma **pasta de camadas de topo separada**, numerada e nomeada de forma estável (`01 Capa`, `02 Contexto`, ...). Dentro de cada página intermediária, usar um subgrupo `CONTENT` para H1, painéis, textos e foto; os elementos fixos vêm da duplicação do grupo vazio claro/escuro correspondente. Não achatar todas as telas em uma camada nem criar um PSD por página. Para cada tela de conteúdo: duplicar `TEMA CLARO VAZIO - DUPLICAR` ou `TEMA ESCURO VAZIO - DUPLICAR`, renomear com o número sequencial, preservar cabeçalho/rodapé, criar camadas em `CONTENT` e aplicar a ordem de sobreposição correta. Renomear a capa como página 01 e o agradecimento com o último número; manter as duas bases vazias ocultas e sem número. Durante a exportação, tornar visível só a pasta da tela corrente (e elementos globais necessários) para evitar mistura entre páginas.

Na capa, nenhum novo elemento `photo` é aceito; use a imagem de marca já integrada à capa aprovada. Para foto ambiental de página interna, preencher toda a faixa com máscara/recorte e tocar `y=0` e `y=1080` mais a borda lateral correspondente. Modelo recortada com alpha verdadeiro pode ocupar outra composição aprovada.

Após o `cover`, conferir no slide **15% de altura livre no topo e 15% no rodapé** da fotografia, sem cabeça, braços, mãos, produto ou outros elementos importantes. Cabeçalho e assinatura devem permanecer sobre cenário simples. A foto de entrada precisa de margem adicional para sobreviver ao corte.

Para texto, centralizar ou alinhar conforme a camada de referência do papel (`h1`, corpo, bullet); manter entrelinhas e tracking da referência. Dimensionar a caixa de texto e verificar overflow. Se o conteúdo não couber, redistribuir em mais telas ou ajustar a composição sem mudar alegações/números fora do escopo editorial autorizado.

**Correção confirmada após Optima:** um H1 visual é um único objeto editável de texto, com Gotham Book/Bold e cores aplicadas a intervalos internos; não criar uma camada por palavra. Corpo corrido branco. No tema claro, usar `#B3718E` para título de apoio escuro. Os valores de tracking usados como ponto de partida em Optima foram -70 para H1 e -60 para corpo; verificar cada tela após a composição.

### Continuação de PSD já editado pelo usuário

Quando existe um PSD em andamento, esse arquivo é a fonte atual, inclusive mudanças manuais feitas após o último script. Antes de tocar uma tela, salve uma cópia e faça inventário de grupos/camadas, bounds, textos, visibilidade e prova dessa página. Execute JSX/COM **por página**, selecionando o grupo atual confirmado. Não rode o gerador inicial de 12 telas novamente nem recrie grupos inteiros sobre alterações manuais. Exporte a tela tocada, compare com o estado anterior e corrija o encaixe. No fim, reexporte PDF e contato das telas correntes do PSD. O exemplo da página 12 mostra por que importa: o usuário refez a disposição e o alinhamento dos cartões depois da primeira automação.

**Exportação de cor validada no Optima:** o PSD está em RGB/8 sem perfil atribuído. Os PNGs que o usuário salvou em `exemplos/optima_final/pngs_aprovados/` são a autoridade para a aparência final. Testes com atribuição de sRGB numa duplicata e `saveAs` JPEG/PNG geraram malva `#A9708A`, visivelmente opaco; esses scripts antigos em `scripts_incrementais/export_all_srgb.jsx` e `build_srgb_pdf.py` ficam somente como histórico de uma tentativa rejeitada. O método que reproduziu **todos os 13 PNGs pixel a pixel** foi: duplicar o PSD atual sem alterar perfil nem camadas originais; isolar cada pasta de página; `ExportOptionsSaveForWeb` com `format=PNG`, `PNG8=false`, `convertToSRGB=true`, `includeProfile=true`; fechar a duplicata sem salvar. Use `scripts/exportar_pngs_bellas.jsx` após conferir nomes e grupos do arquivo corrente. A exportação produz PNG24 com ICC sRGB e RGB aprovado. Monte o PDF com `scripts/montar_pdf_dos_pngs.py`, que confere o RGB extraído de cada página. Inspecione também o PDF renderizado. O resultado aprovado do Optima usa rosa claro próximo de `#FBA9C3` e malva `#BC718C`; os números `#E7A7C1` e `#A9708A` obtidos em outras rotas não são a cor final. Em novo PSD ou perfil, faça uma página de teste e compare com a referência aprovada antes de exportar o conjunto.

## 5. Provas e aprovação

O QA final novo também exige `--reopen-report` e `--reopen-png-dir`. Reabra o PSD no editor, reexporte suas páginas em uma pasta separada e registre o vínculo com `scripts/registrar_reabertura.py`, conforme `CONTRATO_MANIFESTO.md`. O verificador confronta os textos/camadas do manifesto com o PSD real. Para inspeção histórica 1.0, use `--legacy` explicitamente; isso não homologa um trabalho novo.

Depois de inspecionar páginas isoladas, compare o contato inteiro: títulos iguais em assuntos distintos, fotos de mesmo cenário/gesto e áreas vazias sem função podem sobreviver a um QA por página. Verifique se uma série mantém número, tema, ação e referência próximos e fáceis de comparar. Rode `python scripts/validar_artefatos_bellas.py --manifest CAMINHO --psd CAMINHO --png-dir PASTA --pdf CAMINHO --require-srgb-icc` para conferir diretamente grupos, textos ocultos, perfil ICC e renderização integral do PDF. Faça separadamente um parecer visual comparativo contra referências aprovadas, além da lista de bloqueadores; uma validação técnica aprovada não decide a força da composição.

**Nota de cor:** a rota Save for Web com `includeProfile=true` é a configuração de exportação; a presença real de ICC precisa ser lida no PNG. Os 13 PNGs Optima históricos aprovados preservam a cor em pixels mas não contêm ICC embutido. Os PNGs novos de Crescimento/Luciane contêm sRGB e o PDF incorpora ICCBased. Não infira perfil pela opção do script nem regrave as provas históricas.

Exportar PNG24 de **todas** as telas, em 1920×1080 ou resolução equivalente, e criar um contato de visão geral. Conferir individualmente:

- capa com somente título de conteúdo, sem fotografia nova ou benefícios;
- alternância de fundos prevista;
- todas as fotos encostadas nas bordas, sem moldura/recorte pequeno;
- cabeçalho e rodapé corretos na versão clara/escura;
- H1 legível, blocos sem clipping, bullets com alinhamento regular;
- H1 em uma camada de texto com destaques internos; corpo branco; cor de apoio correta; check e texto no mesmo eixo;
- fotos neutras e variadas, não repetição de poses ou produto fora de proporção;
- produto e anatomia revisados; rótulos gerados por IA substituídos por arte real, quando necessário;
- fidelidade de conteúdo ao PDF da palestrante, inclusive números e ressalvas.
- ausência de rótulos temporários H1/BLOCO/ITEM/BULLET e texto real em todas as camadas variáveis.

Revise as provas contra o manifesto e contra o documento Rosângela; quando disponível, use um revisor diferente da execução. A aprovação final requer prova visual de cada tela e inspeção do PSD único com contagem dinâmica de pastas. O Optima aprovado tem **13 pastas/páginas** (12 de conteúdo e uma de agradecimento), além do retorno de sucesso do JSX/COM. Use `QA_FINAL.md` para registrar os resultados.

## 6. Arquivos executáveis

- `scripts/validar_manifest.py`: valida o contrato de entrada antes do Photoshop.
- `scripts/executar_jsx.ps1`: controlador COM parametrizado; recebe o caminho de um JSX. Exemplo de comando: `powershell -ExecutionPolicy Bypass -File scripts/executar_jsx.ps1 -ScriptPath CAMINHO_DO_JSX_FINAL.jsx`. Execute apenas o JSX que corresponde ao manifesto final e à cópia de trabalho.
- `scripts/inspecionar_psd.py`: registra camadas/bounds/estilos offline, sem alterar Photoshop.
- `scripts/preparar_optima_conteudo_real.py`: troca os rótulos de planejamento pelos textos reais completos da fonte; não renderiza nem certifica encaixe.
- `scripts/exportar_pngs_bellas.jsx`: exporta cada pasta numerada do PSD ativo por Save for Web PNG24 sem atribuir perfil à duplicata.
- `scripts/montar_pdf_dos_pngs.py`: junta PNGs numerados sem reamostragem e verifica igualdade de RGB entre PNG e PDF.
- `scripts/planejamento/`: JSX/entrada da montagem histórica de placeholders com caminhos adaptados; somente planejamento, jamais saída final.
- O caso final Optima foi integrado em `exemplos/optima_final/` com PSD, registro de saída, assets, provas e PDF. O registro de saída não tem o esquema de manifesto de entrada exigido por `validar_manifest.py`. Scripts históricos em `scripts/planejamento/` continuam restritos ao planejamento; não os execute sobre o PSD final.
- `exemplos/optima_final/optima_codigo_historico.zip` guarda scripts incrementais usados na etapa final. Consulte como referência de JSX; adapte caminhos, nomes e IDs após inspecionar o PSD atual antes de executar.
