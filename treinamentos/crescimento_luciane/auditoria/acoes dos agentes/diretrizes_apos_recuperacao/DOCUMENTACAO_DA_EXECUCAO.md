# Documentar durante a execução

Regra solicitada pelo usuário em 15/10/2026. Aplica-se ao agente principal e a cada subagente que trabalhar neste pacote. A documentação começa na primeira ação e é atualizada durante o trabalho, não reconstruída somente no fechamento.

## 1. Iniciar o registro

Antes da leitura/edição operacional, crie no projeto `auditoria/execucao/`. Registre o pedido vigente, o escopo, as fontes e versões disponíveis, os agentes envolvidos e a configuração de modelo/esforço que uma fonte verificável realmente informar. Identifique a origem desse dado. Se não estiver disponível, escreva **não informado**, sem inferir pela capacidade percebida.

Cada agente mantém seu arquivo JSONL, por exemplo `principal.jsonl`, `conteudo.jsonl` e `visual.jsonl`. Preserve os arquivos anteriores. Identifique ação, agente, horário com fuso/UTC e relação com a tarefa; ao reunir agentes, mantenha a autoria e não conte histórico herdado como nova execução.

## 2. Registrar antes e depois de cada ação

**Antes:** registre objetivo e justificativa operacional breve, ferramenta, parâmetros/comando/JSX exatos, arquivos de entrada e saídas previstas. Para scripts que serão alterados depois, arquive a versão efetivamente executada ou seu diff e hash. Não basta apontar para um script mutável no fim.

**Depois:** associe o resultado ao mesmo identificador; registre sucesso, falha ou estado desconhecido, código de retorno, saída relevante, arquivos realmente produzidos/alterados, revisão realizada e evidência. Planejado, executado e validado são estados distintos. Esperas, reexecuções, tentativas abortadas e erros também entram no registro. Não reclassifique falhas como sucesso para limpar o histórico.

Use JSONL sem reescrever entradas antigas; uma correção é uma nova entrada referenciando a anterior. O esquema mínimo está em `templates/registro_execucao.json`. Um resumo em `auditoria/SESSAO.md` explica etapas e decisões; ele complementa os eventos literais.

## 3. Prompts e delegações

- Preserve literalmente o texto enviado a cada agente, incluindo tarefa inicial, complementos, correções e pedidos de revisão. Grave **antes de enviar**. Registre destinatário, ferramenta, modelo/esforço pedidos ou herdados e identificador retornado, quando disponível.
- Preserve prompts completos de imagem e outros geradores, parâmetros, referências usadas, identificador de chamada e resultado selecionado. Se a ferramenta retornar prompt revisado, guarde-o separadamente do prompt enviado.
- Guarde a redação original; não normalize espaços, pontuação ou erros e depois a apresente como literal. Versão melhorada ou resumo deve ser rotulado como tal.
- Não chame de exato um texto reconstituído de memória, um resumo de agente ou uma paráfrase. Para recuperação posterior, informe fonte, horário/linha/ID, integridade e limite de comparação. Conteúdo protegido e não legível permanece uma lacuna declarada; não tente substituí-lo por um prompt plausível.

## 4. Evidência e limites

Inclua decisões aceitas/rejeitadas e por quê, leituras/inspeções feitas, inventários antes/depois, versões de arquivos, relatórios de validadores e pareceres visuais/editoriais. Identifique quem revisou cada etapa. Log de sucesso não é aprovação visual.

Arquivos e referências operacionais ficam em caminhos relativos ao pacote. Caminhos locais de logs originais podem aparecer apenas como proveniência histórica. Registre SHA-256 para vincular versões relevantes, sem sobrescrever um inventário histórico com hashes de arquivos já modificados.

Não copie credenciais, tokens, dados de autenticação, mensagens de sistema/desenvolvedor ou raciocínio privado. A auditoria contém ações, prompts operacionais e justificativas verificáveis. Caso algo não possa ser registrado integralmente, descreva o campo omitido, o motivo e a evidência restante; não declare cobertura total.

## 5. Fechamento

Confira o diário contra os registros disponíveis das ferramentas e dos agentes. Complete lacunas recuperáveis, mantenha as não recuperáveis explícitas e vincule tudo no índice da entrega. Registre um ponto de corte com data/hora: registros de sessão continuam crescendo, e uma captura não contém ações futuras.

Declare a cobertura concreta: quais ações/prompts estão literais, quais são resumos, quais outputs foram truncados/omitidos e quais modelos são apenas configuração registrada. Não entregue “tudo documentado” sem essa checagem. A ausência de um formato de log automático não dispensa o registro incremental pelo agente.
