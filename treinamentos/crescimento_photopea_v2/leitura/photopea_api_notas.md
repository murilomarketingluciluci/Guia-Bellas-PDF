# Photopea API — contrato e validação V2

Revisão independente em 15/10/2026 por `api_validacao_v2`. Fontes externas abaixo são exclusivamente documentação oficial. O agente não abriu navegador, não editou Photoshop/Photopea e não usou COM. Microtestes da integração ficam a cargo do principal; itens descritos como necessários ainda não são resultados executados.

## Transporte e ordem

[API Spec](https://www.photopea.com/api/) aceita configuração JSON no fragmento da URL, incluindo `files`, `resources` e `script`. Fontes podem entrar como recursos. Para URLs de arquivos, o servidor deve permitir CORS. O protocolo de salvamento HTTP tem cabeçalho JSON de 2.000 bytes; isso é diferente de `saveToOE`.

[Live Messaging](https://www.photopea.com/api/live) distingue `String` (script JavaScript) de `ArrayBuffer` (arquivo binário, inclusive fontes). O iframe envia `done` ao inicializar e ao terminar uma mensagem. O receptor deve separar Strings dos buffers e aguardar a conclusão entre comandos. `app.echoToOE(string)` devolve uma String; `app.activeDocument.saveToOE('psd')` ou `saveToOE('png')` devolve bytes via mensagem, seguidos por `done`.

Decisão de integração: verificar `event.origin` e `event.source`; correlacionar eventos com identificador próprio. Esses controles são desenho local, não uma garantia extra da documentação. Uma fila com um comando ativo evita associar o PNG/PSD ao pedido errado. Receber `done` comprova processamento, não sucesso visual nem existência de todas as camadas esperadas. Erros precisam ser enviados pelo próprio script em `try/catch`, com identificador.

## DOM e ActionManager

[Scripts](https://www.photopea.com/learn/scripts) descreve um DOM semelhante ao do Photoshop, não uma implementação integral. O global `app` e propriedades/métodos de documento/camada dão o ponto de entrada. Algumas propriedades são somente leitura; largura do documento, por exemplo, exige método de redimensionamento. `app.open(url, as, asSmart)` é extensão documentada, com segundo parâmetro ignorado. `saveToOE('psd:true')` gera PSD minificado; para esta entrega prefira `psd` comum até prova de preservação.

`textItem.totalTextStyle` é uma **String JSON** com os estilos; `textItem.transform` também é uma String JSON, de matriz afim. A página não especifica o esquema interno de runs. Não presumir que um descriptor Photoshop/ActionManager seja aceito igual, que a classe `TextItem` corresponda ao JSON interno, ou que um valor lido em uma sessão possa ser convertido sem inspeção. Primeiro ler o objeto real de uma camada Gotham do molde. A cobertura exata de ActionManager, objetos File/Folder, COM, alertas e operações de arquivo do sistema não está contratada nessas páginas. O principal deve testar cada operação usada; COM não faz parte desta API.

## Gotham real e carregamento

[Text Style](https://www.photopea.com/learn/text-style) permite abrir TTF/OTF como arquivos e usá-los nas camadas. Com o transporte binário documentado, o fluxo mínimo é ler cada OTF autorizado localmente, produzir ArrayBuffer, enviar ao iframe e esperar `done`, antes de abrir/editar o molde. O nome local do arquivo não é autoridade para `textItem.font`: usar o nome PostScript interno.

Fonte local encontrada por inspeção de `name` table com fontTools, **sem extração nesta inspeção**: `C:/Users/Murilo/Downloads/Gotham.zip` (proveniência histórica; não é caminho de asset operacional). Inventário completo: [gotham_inventario.json](gotham_inventario.json), com SHA-256 do ZIP e de cada membro.

| Membro do ZIP | PostScript verificado |
|---|---|
| `Gotham/Gotham Book/Gotham Book.otf` | `Gotham-Book` |
| `Gotham/Gotham Bold/Gotham Bold.otf` | `Gotham-Bold` |
| `Gotham/Gotham Light/Gotham Light.otf` | `Gotham-Light` |
| `Gotham/Gotham Medium/Gotham Medium.otf` | `Gotham-Medium` |

Há arquivos com nome enganoso no ZIP: `Gotham Regular.otf` declara `Gotham-Black`; `Gotham Italic.otf` declara `Gotham-BoldItalic`. Não os escolher por nome de pasta. As buscas anteriores nos diretórios padrão Windows e de usuário (1.160 arquivos) e no cache Adobe CoreSync (381 binários reconhecidos) não localizaram Gotham. Isso não invalida o ZIP real encontrado depois. Um arquivo padrão `dfmw5.ttf` não teve nome decodificado por erro de encoding; esse erro não foi corrigido ou ocultado.

## Cor, PSD e limites

[Color Spaces](https://www.photopea.com/learn/color-spaces) explica a função dos perfis ICC; valores RGB isolados não especificam a mesma aparência em qualquer espaço. [Open and Save](https://www.photopea.com/learn/opening-saving) usa PSD para preservar estrutura e distingue exportação raster de arquivo editável. Nenhuma dessas páginas garante que `saveToOE('png')` replique a receita Photoshop Save for Web aprovada no Optima ou descreve parâmetros para `convertToSRGB` e `includeProfile` nessa chamada. Não copiar tais nomes para a API como se fossem documentados.

Para V2: registrar ICC do molde e do PSD salvo, chunks ICC/sRGB dos PNGs, e comparar RGB das exportações do molde aberto em Photopea com os PNGs aprovados. Não atribuir perfil por suposição. Se houver diferença, identificar a rota e avaliar a prova antes de generalizar. A integridade PDF é outra verificação: a imagem extraída deve reproduzir cada PNG sem reamostragem.

## Ensaios mínimos antes da entrega

1. Mensageria: registrar `done` inicial, String de eco com ID, conclusão e tipo/tamanho dos buffers. Guardar payload exato do script e bytes SHA-256; não usar apenas retorno de execução.
2. Fontes: carregar os quatro binários identificados, fazer uma camada com caracteres portugueses e pesos Book/Bold, exportar PNG e salvar PSD. Abrir com psd-tools e conferir runs/fontes reais; inspecionar os glifos na prova. Nome de fonte no PSD não prova ausência de fallback na sessão.
3. Estilos: ler `totalTextStyle` antes, aplicar palavra em peso/cor diferente em **uma camada H1**, ler de novo e salvar/reabrir. Confirmar contagem de runs, comprimentos, fonte/cor e número de camadas. Não confiar apenas em `textItem.font`, que pode representar somente um trecho.
4. Bases aprovadas: exportar capa e agradecimento do molde pela mesma API. Comparar agradecimento inteiro e a capa fora da união das caixas do título. Conferir individualmente marcas/cabeçalho e paleta. A comparação com exportação do mesmo Photopea também detecta mudanças da composição; a comparação com PNG aprovado detecta diferença do renderizador.
5. PSD final: salvar, preservar bytes e hash, fechar o documento de construção, reabrir esses bytes em sessão Photopea com as fontes carregadas e reinventariar grupos/textos/styles/bounds. Exportar novamente todas as páginas e comparar RGB aos PNGs da entrega. Reabrir é uma ação real, não um campo `reopened: true` em manifesto.
6. Arquivos: rodar `scripts/validar_entrega_photopea.py`; a validação abre PSD com psd-tools, inventaria texto editável e runs, procura rótulos, compara sequência dos grupos/provas/manifesto/PDF e pixels incorporados. Valida capa/agradecimento contra o molde oficial, não contra qualquer Crescimento anterior. Reabertura exige inventário mais PNGs de reexportação.

O JSON de reabertura esperado pelo validador contém `psd_sha256` e `pages: [{name, layers: [...]}]`. O nome deve ser o do grupo real. Use `--baseline-dir` com `capa.png` e `agradecimento.png` exportados do molde no Photopea se for necessário distinguir variação do renderizador; mantenha a comparação visual com os PNGs aprovados registrada separadamente.

O validador retorna falha se algum artefato, fonte usada, texto previsto ou evidência mínima não satisfizer a checagem. Não aprova automaticamente anatomia, margens fotográficas, conteúdo rasterizado, overflow dentro da própria caixa de texto, contraste ou hierarquia. Isso exige revisão de cada PNG em resolução útil. Nenhum resultado real de V2 é declarado neste documento antes da existência da arte.
