# Correções autorizadas — 19/10/2026

Escopo: validadores, consolidação das instruções e empacotamento, com publicação no GitHub após conferir preservação das artes. Sem subagentes. Modelo/esforço não informado por fonte verificável. Pedido literal em `pedido.json`.

## Resultado técnico

- Manifesto final 2.0 exige origem/destino de texto, cobertura dos trechos cadastrados, capas/agradecimento fixos, fontes/cores e estilos internos. Rótulos temporários ampliados; frases reais como “Item essencial” continuam aceitas. `--legacy` é diagnóstico histórico explícito.
- QA direto compara pastas e camadas reais, texto, visibilidade ancestral, fontes/cores por caracteres, texto extra não declarado, hash do molde aprovado e evidência de reexportação vinculada ao PSD atual. sRGB é exigido por padrão em finais novos. A saída não concede aprovação visual.
- `registrar_reabertura.py` registra os arquivos de uma ação de reabertura/exportação feita no editor; não executa nem certifica essa ação sozinho. A evidência operacional continua no diário.
- Empacotador seleciona arquivos rastreados e respeita `.gitignore`, com exclusões obrigatórias para Git, caches, fontes e credenciais; recusa padrões conhecidos de segredo, ZIP inseguro e LFS não baixado. Confere hashes do ZIP contra o inventário e recusa sobrescrita. O inventário histórico da raiz permanece intacto.
- `CONTRATO_ATUAL.md` centraliza as regras; AGENTS, skills, prompt e fluxo são pontos de entrada curtos. Redação anterior preservada em `instrucoes_antes/`. Corrigida referência ao molde v1 como atual; removidas duplicações do fluxo. Entradas anteriores tinham 6.151 palavras; novas entradas mais contrato têm 2.311. A redução não comprova melhora criativa por si só.

## Verificações

1. **24 testes de regressão passaram**, incluindo cinco manifestos antes aceitos, conteúdo/camadas, estilos Unicode/UTF-16, fontes, corpo branco, ancestrais ocultos, texto rasterizado, contagem, reabertura/hash/pixels, seleção Git, segredos/ZIP/LFS e não sobrescrita.
2. Leitor de estilos exercitado nos dois PSDs reais de Crescimento: 88 e 91 camadas de texto, sem erro de leitura. Não se declara nova homologação das artes históricas.
3. Sonda integrada em PSD/PNGs/PDF reais rejeitou manifesto artificial sem páginas e com estágio incorreto. As diferenças históricas de capa/agradecimento/ICC continuaram reportadas. Evidências: `sonda_integrada.json` e `qa_integrado_negativo.json`.
4. Catálogo validado: 227 referências únicas, 15 fontes, 26 arquétipos e links locais presentes. Molde conferido por estrutura e SHA-256 aprovado.
5. Duas skills passaram em `quick_validate.py`; nove documentos de entrada sem links locais quebrados. Manifesto de planejamento histórico segue legível; final antigo somente em `--legacy`.
6. **966 arquivos de arte rastreados comparados por SHA-256: nenhuma alteração**. Baseline `artes_antes.json`, resultado `preservacao_artes.json`. Fontes, PSDs, PDFs, PNGs/JPEGs, PSBs, BINs e ZIPs históricos não foram regravados. Manifestos históricos também não foram editados.
7. Seleção real do pacote conferida em `--dry-run`, sem Git interno nem trabalho não rastreado. ZIP real criado, conferido e descartado apenas em diretório temporário nos testes. Não foi gerada uma distribuição completa de 1,7 GB nesta manutenção. `selecao_pacote.json` é snapshot da seleção naquela ação; registros posteriores têm seu próprio corte.

## Falhas e correções preservadas

- Primeira captura de hashes falhou por limite de caminho do Windows; repetida com namespace estendido, sem renomear assets.
- Uma tentativa de substituir arquivo por delete/add no mesmo patch foi recusada; o arquivo original permaneceu e a edição foi aplicada incrementalmente.
- Primeira rodada de testes teve uma falha no próprio helper do teste de JSON nulo; corrigida a distinção entre valor ausente e `null`, e os 24 casos passaram.
- O executor de auditoria inicialmente não aceitou a origem externa de `quick_validate.py`; corrigido para preservar proveniência externa, e as duas skills passaram na repetição.
- A primeira inspeção de whitespace reportou CRLF no JSONL literal. O registro não foi normalizado/regravado; a conferência de código usa `cr-at-eol` e separa o arquivo de auditoria em crescimento.

## Cobertura e ponto de corte

`principal.jsonl` preserva os comandos executados pelo wrapper, saídas e falhas; `scripts_executados/` preserva versões identificadas por hash. Leituras iniciais, patches e algumas inspeções de ferramenta estão no transcript e resumidas neste registro; saídas extensas tiveram truncamento na interface, mantendo o conteúdo recebido pelo wrapper no diário. Não se afirma cobertura literal integral de todas as ferramentas neste diretório.

Ponto de corte versionado: após revisão/testes e antes do commit/push final. Para evitar que o diário se altere circularmente a cada commit, a publicação e a confirmação do hash remoto usam uma cópia do executor em `.git/auditoria/correcoes_2026-10-19/`, com diário local não publicado. O push é uma etapa autorizada prevista neste corte; seu resultado será confirmado pela ferramenta antes da resposta final.

Trabalhos não rastreados de empreendedorismo e a auditoria da análise anterior ficam preservados fora deste commit. Qualidade criativa, anatomia, margens, contraste percebido e fidelidade semântica continuam exigindo os pareceres visuais/editoriais; esta manutenção não produziu uma APN nova nem executou a avaliação criativa em três casos inéditos.
