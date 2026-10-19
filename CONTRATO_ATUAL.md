# Contrato Bellas vigente

Versão **2.0 — 19/10/2026**. Fonte única das regras operacionais para trabalhos novos. Os detalhes técnicos ficam nos documentos indicados; casos anteriores ficam como evidência. Esta revisão reorganiza as instruções e os controles, sem homologar novas artes ou outro editor.

## Autoridades e escopo

1. Pedido e correções atuais do usuário determinam o escopo. Não reconstruir automaticamente páginas já aceitas.
2. Os 13 PNGs em `exemplos/optima_final/pngs_aprovados/` determinam acabamento, cor e identidade aprovados. O PSD corrente determina as camadas e edições manuais que devem ser preservadas. Estilos Gotham são medidos no PSD Bellas/Rosângela.
3. Este contrato determina o processo. `MODELO_REUTILIZAVEL.md`, `DIRECAO_DE_ARTE.md` e os guias técnicos detalham sua aplicação. `DECISOES_APN_BELLAS.md` conserva decisões e proveniência; seus casos não viram regras universais por analogia.
4. As 227 telas e os 26 arquétipos fornecem repertório. Não fornecem uma grade obrigatória, uma nova capa ou autorização para usar tratamentos históricos rejeitados.

## Entrada e decisão criativa

- Peça inicialmente somente o PDF original sem edição. Leia todas as suas telas, os 13 PNGs aprovados e os contatos das 227 referências; abra as páginas integrais pertinentes. Não peça ao usuário que prepare roteiro, manifesto ou seleção de layouts.
- Extraia e identifique o conteúdo por origem, página e trecho. Preserve números, termos, atribuições e ressalvas. Diferencie procedimento, condição/restrição, benefício, evidência, citação e fecho. A composição precisa preservar essas funções, além das palavras. No Optima somente revisão de português foi autorizada; em outro trabalho vale o escopo editorial atual.
- Antes de selecionar arquétipo, defina gesto narrativo, primeiro foco, relação espacial e função da imagem. Para cada página interna não seriada, compare duas candidatas de composições diferentes nas 227 telas, preferencialmente de PDFs distintos. Abra-as integralmente e registre origem, aproveitamento e rejeição. Uma terceira solução original é possível; se faltarem referências úteis, registre a busca.
- Apresente primeiro mapa visual com placeholders dimensionados pelo texto real em Gotham e escala de PSD. Registre dominante, papel da foto, relação entre blocos e diferença para as vizinhas. Compare assinaturas de H1, foco, espaço e imagem no contato. Repetição que facilita séries é válida; variar lado/cor/foto sem melhorar comunicação não comprova criatividade.
- Antes do lote, prove no editor texto real e Gotham em uma tela densa e uma de impacto, quando existirem. Compare peso/tamanho aparente do H1 e leitura em 1920×1080 e no contato com referências aprovadas. Corrija o mapa. Aprovação do mapa precede direção e geração das fotos. Dispensa expressa pelo usuário é registrada e mantém as provas e crítica interna.
- Avalie as justificativas contra a imagem: uma restrição apresentada como passo numerado continua sendo passo visual, ainda que o manifesto diga o contrário. Registre evidência observável e correção quando houver divergência.

## Marca e editabilidade

- Comece somente em cópia de `referencias/molde_bellas_aprovado_capa_temas_agradecimento.psd`. Execute `python scripts/verificar_molde.py`: estrutura e hash devem corresponder à base aprovada. `MODELO_REUTILIZAVEL.md` descreve os quatro grupos.
- Reutilize a capa, alterando apenas o título do treinamento no objeto existente; conserve estilos internos, cabeçalho, quadrados, marcas e imagem de marca muito esmaecida. Não acrescente foto, subtítulo, benefícios ou chamadas. Agradecimento final permanece idêntico. O número de páginas intermediárias depende do conteúdo.
- Duplique bases vazias clara/escura do molde para criar as páginas internas. Preserve os elementos fixos do tema. Um PSD único contém pastas de topo numeradas por página, conteúdo variável em `CONTENT` e cards completos em pastas próprias. Os PSDs de Optima, Rosângela, molde v1 e outros treinamentos não doam grupos.
- Gotham Book/Light/Medium/Bold; H1 em um objeto editável com estilos internos. Corpo sempre branco; apoio escuro sobre claro usa `#B3718E`. Tamanhos armazenados, tracking e transformações são referências técnicas, não prova de tamanho aparente. Não substituir fontes silenciosamente.
- Ajuste uma unidade de card/checklist/número visualmente antes de replicar. Centralize opticamente; preserve hierarquia e legibilidade. Maior respiro fica nas extremidades do conjunto, com intervalos menores e consistentes entre blocos relacionados. Não espalhe blocos pela altura para preencher espaço. Veja a preferência do usuário em `DECISOES_APN_BELLAS.md`, seção 2.1.
- Claro/escuro seguem o roteiro. Cores exportadas de referência Optima são aproximadamente `#FBA9C3` e `#BC718C`. HEX armazenado em PSD sem perfil pode exportar outro RGB: faça prova de fundo/card/apoio pela rota final antes do lote. Não generalize a receita de perfil sem teste.

## Fotografia

- Fotos ambientais ocupam altura integral tocando uma lateral, ou todo o canvas, sem distorcer proporções. Recorte transparente é uma alternativa quando coerente com a composição. Preserve alpha verdadeiro, luz integrada e bordas sem halo, fundo residual ou corte horizontal do corpo.
- Gere pessoa e produto juntos numa geração original; refaça uma geração defeituosa em vez de acumular remendos. Compare ações, ambientes, escala de câmera, pessoas e luz na sequência. Prefira neutros creme, cinza/ardósia ou espresso com saturação contida e exposição equilibrada.
- Mulheres bem arrumadas com roupa contemporânea, traços individuais, textura de pele e idade naturais. Pessoa de referência mantém identidade reconhecível; produto mantém proporção, tampa/corpo e rótulo da referência real. Mostre-o quando o gesto comunica seu uso. Declare referência essencial ausente antes de afirmar fidelidade.
- Após o recorte definitivo, pelo menos 15% da altura no topo e 15% no rodapé ficam sem assunto importante sob cabeçalho e assinatura. Roupa/ambiente podem continuar naturalmente. Não fabricar área livre com faixa pintada, linha de emenda ou vinheta colada. Confira anatomia, embalagem e margens na foto aplicada, não apenas no prompt.

## Execução, continuidade e entrega

- Photoshop somente por JSX/COM. Se o usuário escolher Photopea ou outro editor, teste importação/reabertura do molde, texto Gotham, editabilidade, capa/agradecimento, cor e ICC antes do lote. Registre perdas; aproximação não é paridade homologada. Não interferir no editor ocupado por outro trabalho.
- Em PSD já editado, inventarie estado atual, camadas visíveis/ocultas e prova antes de mudar. Trabalhe em cópia e uma página por vez, preservando ajustes manuais. Não reaplique um gerador inicial sobre o trabalho corrente.
- Exportação Photoshop usa `scripts/exportar_pngs_bellas.jsx`: duplicata sem atribuir/mudar perfil, Save for Web PNG24, `convertToSRGB=true`, `includeProfile=true`. Verifique presença real de ICC sRGB nos PNGs novos e ICCBased no PDF, além da igualdade de pixels. PNGs históricos aprovados sem ICC permanecem intactos.
- Final novo usa manifesto 2.0: origem dos trechos, destino em camadas, fontes, cores e intervalos estilísticos. `CONTRATO_MANIFESTO.md` documenta o esquema e os comandos. Validação histórica com `--legacy` não homologa um final novo nem prova planejamento anterior.
- Execute os validadores, reabra o PSD no editor e reexporte todas as páginas. Vincule relatório de reabertura ao hash desse PSD e aos PNGs reexportados. Inspecione todas as telas em resolução útil e o contato. Gere PDF sem reamostrar. Um JSON de inventário isolado não prova o estado do PSD.
- Faça dois pareceres: integridade técnica e crítica visual comparativa. Esta última verifica candidatas consultadas, H1, proximidade, cadência, função das fotos e repetição funcional. Aprovação técnica não substitui aprovação visual ou revisão editorial. Fonte recebida e aparência aprovada não comprovam alegações científicas.
- Entregue PSD, manifesto, fotos usadas, PNGs, contato, PDF, evidências e QA. Não declarar final com placeholder, foto nova na capa, marca perdida, texto cortado ou fonte substituída. Registre limitações de editor/perfil separadamente.

## Auditoria e manutenção

Siga `DOCUMENTACAO_DA_EXECUCAO.md` desde a primeira ação: diário incremental, comandos/parâmetros e prompts operacionais literais, scripts executados preservados, resultados/falhas, decisões e evidências. Declare modelo apenas quando verificável, lacunas e ponto de corte. Não registrar credenciais, raciocínio privado ou instruções protegidas.

Assets e manifestos usam caminhos relativos dentro do pacote; caminhos antigos só como proveniência. Preserve históricos e artes aprovadas. Empacotamento seleciona arquivos controlados, exclui Git/caches/fontes/credenciais e cria inventário por versão; nunca regrava `inventario_sha256.json` histórico. Fontes Gotham precisam estar licenciadas no ambiente e não são redistribuídas.
