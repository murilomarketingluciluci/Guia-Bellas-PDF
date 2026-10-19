# Recuperação de prompts e ações — 15/10/2026

Pedido do usuário: recuperar o que faltou, completar com os prompts e ações exatos disponíveis, sem inventar, e exigir documentação durante a execução dos próximos agentes.

## Resultado

Foram encontrados quatro registros relacionados: a sessão principal e os três subagentes, vinculados pelo identificador da sessão de origem. A produção de 14/10 foi separada das ações posteriores pelo corte **15/10/2026 00:00 UTC** (14/10 às 21h em São Paulo), posterior ao encerramento da entrega original. O instante/quantidade de bytes realmente lidos de cada arquivo vivo está em `cobertura_final.json`; eventos futuros não estão incluídos nessa captura.

| Evidência recuperada da produção | Quantidade | Natureza |
|---|---:|---|
| Eventos operacionais | 406 | Campos registrados nos logs, com linha e SHA-256 |
| Execuções de comandos | 176 | String ou vetor de argumentos, saída/código/estado quando registrados |
| Inspeções de imagem | 153 | Caminho e evento de abertura; não é um novo parecer visual |
| Alterações de arquivos | 29 | Evento registrado; chamadas de ferramentas conservam código/patch disponível |
| Atividades de subagentes | 42 | Eventos de coordenação |
| Gerações de imagem | 4 | Prompt revisado, ID, resultado/arquivo e parâmetros disponíveis |
| Chamadas MCP | 2 | Ferramenta, argumentos e resultado registrado |
| Chamadas de ferramentas | 185 | Código/argumentos literais legíveis ou campo protegido explicitamente identificado |
| Retornos de ferramentas | 189 | Não supõe relação 1:1 com chamadas; payloads grandes/binários omitidos são indicados |
| Textos copiados dos contextos dos agentes | 42 | 33 mensagens de delegação/coordenação e nove finais; incluem três tarefas iniciais |

Os eventos e chamadas são perspectivas diferentes do mesmo trabalho: **não somar as linhas como se fossem execuções independentes**. Um comando pode aparecer tanto na chamada do orquestrador quanto no evento de execução. Ações herdadas em contexto também não comprovam uma segunda execução.

## Onde ler

- [Linha do tempo legível](LINHA_DO_TEMPO.md): comandos, imagens abertas, arquivos alterados e coordenação em ordem de registro. Comandos são históricos; este arquivo não deve ser executado.
- [Delegações consolidadas](delegacoes_consolidadas.json): 33 mensagens com texto, origem, hash, ID/horário candidato e limite da associação.
- Prompts iniciais em texto puro: [conteúdo](prompt_inicial_conteudo_luciane.txt), [composição](prompt_inicial_revisao_composicao.txt) e [validação](prompt_inicial_validacao_entrega.txt).
- Contextos literais declarados pelos próprios agentes: [conteúdo](contexto_conteudo_luciane.json), [composição](contexto_revisao_composicao.json), [validação](contexto_validacao_entrega.json).
- [Prompts revisados das imagens](prompts_revisados_imagens.json), separados dos [prompts enviados já registrados](../prompts_imagens.json).
- [Correspondência dos prompts e arquivos das fotos](correspondencia_imagens.json): comparação literal dos prompts e dos bytes da imagem gerada/asset selecionado.
- [Configuração de modelos nos logs](modelos_registrados.json): `gpt-6.1-sol`, esforço `high`, no principal e nos três subagentes. Trata-se de configuração registrada; não é uma verificação independente do backend. O modelo exato de imagem continua não identificado.
- [Cobertura final e fontes](cobertura_final.json), [verificação da recuperação](verificacao_recuperacao.json), [arte preservada](arte_preservada.json) e [hashes do complemento](hashes_recuperacao.json).

Arquivos literais extensos: `acoes_operacionais.jsonl`, `chamadas_ferramentas.jsonl`, `retornos_ferramentas.jsonl` e `mensagens_visiveis.jsonl`. Os correspondentes `*_posteriores_ao_corte.jsonl` registram a continuação/revisão da documentação, inclusive as ações desta recuperação disponíveis no instante da captura. [Tarefas desta rodada](tarefas_desta_recuperacao.json) preservam os três prompts atuais, registrados como complemento posterior ao envio.

## O que é exato e o que não foi certificado

1. **Literal do registro:** strings/vetores de comandos, código das chamadas, campos de eventos e mensagens visíveis foram extraídos sem corrigir grafia, escapes ou erros. A verificação confere conteúdo/proveniência contra as linhas de origem. Quando há truncamento ou omissão no original/derivado, isso não é preenchido artificialmente.
2. **Literal disponível no contexto:** os textos de delegação estão cifrados nos arquivos. Os agentes copiaram somente os textos que declararam ainda ter literalmente no contexto. Incluem os três prompts iniciais, antes apenas resumidos. Sete mensagens também coincidem byte a byte com cópias no contexto disponível do principal. Não foram corrigidos espaços ausentes ou português.
3. **Associação declarada:** participantes, contagem e ordem permitiram associar os 33 textos a chamadas registradas. A associação de horário/ID é por ordem e participantes, **não uma comparação do texto claro com o payload cifrado**. As fontes de contexto sozinhas não trazem esses horários/IDs. Esse limite consta em cada registro consolidado.
4. **Lacuna mantida:** não há certificação de mensagens fora do contexto disponível, saídas já truncadas, payloads binários omitidos, atos humanos externos não registrados nem a identidade efetiva de um backend a partir de seu nome configurado. Não foi tentada decifragem nem busca de chaves. Não é correto dizer que todo o histórico bruto ficou recuperado.
5. **Material excluído:** raciocínio privado, mensagens de sistema/desenvolvedor e conteúdo de autenticação não foram copiados. Metadados de origem e hashes não substituem conteúdo ausente.

Payloads protegidos encontrados dentro de uma saída de inspeção também são substituídos por marcadores/hash no complemento; a saída derivada fica identificada como filtrada. Não se apresenta esse retorno filtrado como saída textual integral.

`cobertura.json` e `prompts_delegacao.json` mostram a extração preliminar, quando só sete textos do principal estavam disponíveis e os demais eram lacunas. O estado complementado está em **`cobertura_final.json` e `delegacoes_consolidadas.json`**; o preliminar foi mantido para não apagar a sequência da recuperação.

## Conferência e preservação

Os scripts `../../scripts/recuperar_auditoria.py`, `../../scripts/consolidar_recuperacao.py` e `../../scripts/verificar_recuperacao.py` preservam o procedimento reexecutável. Eles não executam comandos encontrados no histórico e não exportam eventos de raciocínio. A primeira consolidação encontrou `command` como vetor em vez de texto e parou; a correção e a reexecução estão no registro de sessão e nos eventos posteriores.

Os **28 arquivos de produção, fontes e assets** coincidem com os hashes históricos de 14/10. Nenhum PSD, PDF, prova, foto ou fonte foi alterado nesta recuperação. Os hashes e o snapshot de diretrizes de 14/10 foram preservados; o complemento possui seus próprios hashes e `diretrizes_apos_recuperacao/`.

## Regra para os próximos agentes

Persistida em `../../../../AGENTS.md`, decisões, fluxo e QA. O guia [DOCUMENTACAO_DA_EXECUCAO.md](../../../../DOCUMENTACAO_DA_EXECUCAO.md) exige iniciar a auditoria na primeira ação, preservar prompts antes do envio, comandos/parâmetros e versões de scripts, registrar resultados/erros e manter evidências por agente durante a execução. Resumos finais complementam o diário. Textos ausentes nunca podem ser reconstruídos e apresentados como literais.
