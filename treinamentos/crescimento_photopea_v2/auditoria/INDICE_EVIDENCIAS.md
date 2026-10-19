# Índice de evidências — Crescimento / Luciane V2

> O inventário abaixo é um snapshot histórico. Para a versão entregue, consulte [QA final](../QA_FINAL.md), [decisões finais](DECISOES_FINAIS.md), [hashes da entrega](hashes_entrega.json), [assets selecionados finais](assets_selecionados_finais.json), [reabertura do PSD](reabertura_psd.json), [comparação de pixels](pixels_reabertura.json) e [suplemento visual final](../leitura/QA_VISUAL_V2_SUPLEMENTO_FINAL.md).

**Índice intermediário. A montagem ainda está em andamento. Nenhum item abaixo constitui aprovação final de PSD, PNG ou PDF.**

Consolidação: `catalogo_novo_v2`. Snapshot de referência: **15/10/2026 às 14:49:54 UTC /11:49:54 em São Paulo**. Os arquivos de diário continuam crescendo. [SESSAO.md](SESSAO.md) explica decisões e limites; [inventario_evidencias_20261015T144954Z.json](inventario_evidencias_20261015T144954Z.json) fixa contagens, hashes e estado dos prompts/fotos naquele instante.

## 1. Pedido, origem e identidade visual

| Evidência | O que sustenta | Limite |
|---|---|---|
| [Pedido vigente](pedido.txt) | Solicitação de outra versão do zero, catálogo diferente e teste da API Photopea | Não é aprovação do resultado |
| [Fontes originais e hashes](fontes_originais.json) | Nove cópias em `fonte/01.png` a `09.png`, com proveniência externa histórica | Fidelidade editorial é conferida separadamente |
| [Contato das fontes](../leitura/fontes_contato.jpg) | Visão geral do material recebido | A leitura foi feita também em cada PNG integral |
| [Modelo reutilizável do pacote](../../../MODELO_REUTILIZAVEL.md) | Fonte operacional aprovada de capa/temas/agradecimento | O backend precisa demonstrar fidelidade na exportação |
| [PNG Optima capa](../../../exemplos/optima_final/pngs_aprovados/pagina_01.png) | Aparência aprovada da capa; trocar somente título | Não autoriza copiar outra APN Crescimento |
| [PNG Optima agradecimento](../../../exemplos/optima_final/pngs_aprovados/pagina_13.png) | Aparência fixa de encerramento | Equivalência da reconstrução V2 ainda pendente |

## 2. Leitura, catálogo e conteúdo

| Evidência | Resultado registrado | Estado |
|---|---|---|
| [Direção de catálogo](../leitura/direcao_catalogo_v2.md) | 9 fontes, 13 PNGs aprovados, 15 contatos/227 telas, 26 arquétipos e 21 páginas integrais candidatas inspecionados | Leitura executada |
| [Proposta estruturada](../leitura/layouts_propostos_v2.json) | 12 páginas, 10 de conteúdo; três sistemas para os 12 episódios; citações, filetes, processo e assimetria | Proposta, sem aceite final comprovado neste índice |
| [Índice de renders integrais](../leitura/catalogo_integral/renders_index.json) | PDF, página exata e render de cada candidata | Evidência de leitura visual |
| [Transcrição nova](../leitura/conteudo_v2.json) | 40 blocos, 4 preparações, 12 episódios e 3 outras referências | Fonte editorial vigente |
| [Revisão inicial](../leitura/revisao_editorial_inicial.md) | Alterações evidentes de português e decisões de caixa/pontuação | Não é revisão factual |
| [Manifesto de produção](../manifest_photopea.json) | Textos reais, fontes, runs, geometrias e origem por bloco | Previsto para montagem; pode receber novas versões |
| [Conferência estrutural do manifesto](../leitura/manifest_photopea_validacao.json) | 12 páginas, 40 blocos mapeados, 12 episódios, 86 textos, 26 formas; caixas previstas dentro do canvas | Validação de dados, não visual |
| [QA editorial V2](../leitura/QA_EDITORIAL_V2.md) | 85 componentes comparados, zero diferenças no hash do manifesto indicado | PSD e provas finais explicitamente pendentes |
| [Índice do catálogo](CATALOGO_SESSAO.md) | Ações, falhas e cobertura do subagente | Não substitui os eventos JSONL |
| [Hashes do catálogo](catalogo_inventario_sha256.json) e [hashes do manifesto](manifest_inventario_sha256.json) | Vínculo das versões no momento de cada inventário | Não sobrescrever com estado futuro |

O manifesto editorialmente conferido tem SHA-256 `3FD0D8722563E557E376B68E1305710A1DE02CE9DD78F34E8FED591FE6B88BF1`. Uma alteração posterior exige nova conferência, sem reaproveitar esse parecer como se fosse do arquivo modificado.

## 3. Quatro fotografias novas e seus prompts

| Página | Asset operacional | Evidência da geração |
|---:|---|---|
| 03 | [foto_direcao_arcada.png](../assets/foto_direcao_arcada.png) | Arquitetura/eixo de direção |
| 06 | [foto_permanencia_rochas.png](../assets/foto_permanencia_rochas.png) | Caminho/rochas e permanência |
| 09 | [foto_pessoas_encontro.png](../assets/foto_pessoas_encontro.png) | Pessoas em encontro/conversa |
| 10 | [foto_agua_poco.png](../assets/foto_agua_poco.png) | Cena simbólica de água/poço |

- [Prompts completos](prompts/fotos_v2.json): quatro textos legíveis, também encontrados literalmente em eventos do diário principal.
- [Gerações selecionadas](geracoes_selecionadas.json): origem histórica e SHA-256 de cada asset selecionado.
- [Snapshot dos assets](inventario_evidencias_20261015T144954Z.json): os quatro hashes atuais coincidem com os hashes das gerações selecionadas.

As caixas de foto e a proporção cover estão no manifesto. O pedido de 22% livres nos prompts não comprova os 15% depois do recorte real. A aprovação das margens, anatomia, luz, continuidade do fundo e relação com marcas depende da inspeção das páginas finais. O identificador do modelo de imagem não foi informado por evidência verificável nesta consolidação.

## 4. API, fontes e testes reais

| Evidência | O que foi observado | O que não prova |
|---|---|---|
| [Notas de API](../leitura/photopea_api_notas.md) | Contrato oficial de mensageria, fontes e saveToOE; ensaios e limites descritos | Paridade integral com Photoshop |
| [Índice independente API/validação](API_VALIDACAO_INDICE.md) | Pesquisa, extração, snapshots de scripts e limitações | Aprovação da arte final |
| [Inventário OpenType](../leitura/gotham_inventario.json) | Nomes PostScript reais dos quatro pesos, hashes dos membros do ZIP | Ausência de fallback por si só |
| [Fontes extraídas para uso](fontes_gotham_usadas.json) | Book, Bold, Light e Medium em `assets/fonts/`, com hashes | Render final ainda precisa de prova |
| [Eco da sessão](teste_echo.json) | Resposta real com versão 30 e documentos 0 | Documento final aberto |
| [DOM básico](teste_dom_basico.json) | Documento/camada reconhecidos em ensaio | Todos os métodos usados são compatíveis |
| [PNG de teste](teste_exportar_png.json) | Buffer real, 4.533 bytes e hash | Cor/visual aprovado da APN |
| [PSD de teste](teste_exportar_psd.json) | Buffer real, 63.241 bytes e hash | PSD final completo e editável |
| [Chamada de reabertura do teste](teste_reabrir_criado.json) | Registro da chamada pequena, sem echoes | Reabertura e reexportação do PSD final |
| [Ensaios de estilos](texto_estilos_resultado.json) | Respostas do teste de estilos na integração | Runs/fonte de todas as páginas finais |
| [Métricas página 02](metricas_p02.json) | Bounds e nomes Gotham em dez camadas do ensaio | Aprovação visual ou medição de todas as telas |
| [Teste de leitura do molde](teste_leitura_molde_validador.json) | Quatro grupos e objetos de texto encontrados pelo validador | Importação correta de todos os dados pelo Photopea |
| [Teste negativo](teste_negativo_ausencia.json) | Validador acusa artefatos ausentes | Falha editorial da apresentação ainda em montagem |

Os erros completos de integração estão no diário API. Entre os eventos lidos há timeout, execução destruída por navegação e TypeErrors de propriedades n/Mm. Nenhuma falha foi apagada; o retorno de done ou a existência de um buffer não foi usado como aprovação visual.

O validador está disponível em [validar_entrega_photopea.py](../scripts/validar_entrega_photopea.py). Sua preparação/compilação e os testes acima não são uma execução de QA final do documento V2.

## 5. Molde, dados originais e máscaras

| Evidência | Verificação registrada | Limite |
|---|---|---|
| [Base extraída](../leitura/base_molde_extraida.json) | 33 camadas, 23 folhas, 7 payloads embedded, 6 camadas com máscara e 4 textos | Dados separados, sem composição final |
| [Checagem resumida](checagem_extracao_bases.json) | Grupos, tipos, textos, máscaras e bboxes | Não aprova aparência |
| [Bytes/pixels originais](verificacao_bytes_extracao.json) | 34 comparações de caches, payloads e textos contra o PSD de origem | Não valida o renderizador Photopea |
| [432 arquivos de extração](verificacao_arquivos_extracao.json) | Existência e hashes das fontes/metadados | Nem todos são arquivos finais |
| [Bases compactas](../leitura/bases_montagem.json) | Quatro templates, fundo, textos/runs/transforms, opacidade/fill/blend separados, estatísticas das máscaras | Nenhum gradiente inventado, imagem ou máscara aplicada pelo derivador |
| [Verificação das bases compactas](verificacao_bases_montagem.json) | 34/34 controles aprovados e original intacto | Compatibilidade do conjunto ainda em teste |
| [Inputs com máscaras originais](../leitura/inputs_mascarados.json) | 64/64 verificações, camadas 5/6/28, canais comprimidos/máscaras/bboxes/flags/opacidades/blends preservados | Cópias técnicas perdem Smart Object/histórico de transform, sem substituir os originais |

O PSD fonte permaneceu com hash `357e5af012e7077c074f843f3809daf4978cf51bb794f692efe3da276d90271a` na preparação dos inputs. As máscaras são dados espaciais suaves: as estatísticas não justificam substituí-las por um único gradiente linear. O resultado final precisa respeitar máscara, opacity e fillOpacity como propriedades distintas.

As entradas técnicas em `assets/base_molde_compativel/` são documentos de uma camada, com preview composto transparente intencional. Não são APNs ou páginas finais criadas fora do Photopea. Os payloads embedded e caches originais permanecem em `assets/base_molde/`.

## 6. Inventário dos diários no ponto de corte

| Diário | Registros no snapshot | Fonte/autoria |
|---|---:|---|
| [execucao/principal.jsonl](execucao/principal.jsonl) | 395 | Agente principal |
| [execucao/photopea_api.jsonl](execucao/photopea_api.jsonl) | 783 | Integração/backend |
| [execucao/conteudo.jsonl](execucao/conteudo.jsonl) | 39 | conteudo_novo_v2 |
| [execucao/catalogo.jsonl](execucao/catalogo.jsonl) | 172 | catalogo_novo_v2 |
| [api_validacao.jsonl do pacote](../../../auditoria/execucao/api_validacao.jsonl) | 80 | api_validacao_v2 |

Todos os cinco foram parseáveis como JSONL nesse snapshot. Os hashes do diário são capturas daquele instante, pois os arquivos continuam crescendo. O diário de API/validação fica no nível raiz do pacote, conforme delegação original; seu índice local confirma esse caminho.

O registro literal de comandos, parâmetros e versões deve ser procurado no diário autoral correspondente e em `scripts_executados/`. Este índice não transforma resumos de resultados em outputs integrais. Não foram lidos ou exportados dados de autenticação, mensagens de sistema/desenvolvedor ou raciocínio privado.

## 7. Inventário dos prompts e recuperação

| Arquivo/campo | Conteúdo disponível | Classificação |
|---|---|---|
| [catalogo_novo_v2.json](prompts/catalogo_novo_v2.json) | Delegação inicial do catálogo | Texto legível salvo |
| [conteudo_novo_v2.json](prompts/conteudo_novo_v2.json) | Delegação inicial editorial | Texto legível salvo |
| [api_validacao_v2.json](prompts/api_validacao_v2.json) | Delegação inicial API/validação | Texto legível salvo |
| [api_fontes_followup.json](prompts/api_fontes_followup.json) | Complemento de fontes | Texto legível salvo |
| [api_fontes_followup_02.json](prompts/api_fontes_followup_02.json) | Segundo complemento de fontes | Texto legível salvo |
| [api_extracao_bases.json](prompts/api_extracao_bases.json) | Complemento de extração do molde | Texto legível salvo |
| [catalogo_auditoria_seguimento.json](prompts/catalogo_auditoria_seguimento.json) | Pedido desta documentação | Texto legível salvo |
| [catalogo_recuperacao_delegacoes.json](prompts/catalogo_recuperacao_delegacoes.json) | Autorização de recuperação estrutural | Texto legível salvo |
| [fotos_v2.json](prompts/fotos_v2.json) | Quatro prompts completos de imagem | Texto legível presente também no diário principal |
| Evento `manifest-001` do diário de catálogo | Pedido do manifesto | Literal disponível no contexto e registrado pelo destinatário |
| [delegacoes_recuperadas.jsonl](prompts/delegacoes_recuperadas.jsonl) | 11 arguments armazenados, com linha/timestamp/call_id/fonte | Recuperação posterior do invólucro; message cifrado |
| [Índice da recuperação](prompts/delegacoes_recuperadas_indice.json) | Critério, contagens, hash e metadados permitidos | Limites explícitos |

A recuperação selecionou três spawn_agent, dois send_message e seis followup_task, com namespace collaboration e alvos explícitos V2. Começou na linha 1342 da transcrição indicada pelo principal. Nenhuma mensagem histórica anterior foi exportada.

**Não há prompt plaintext recuperado do campo message cifrado dessas 11 calls.** O invólucro de arguments é literal ao arquivo; os textos legíveis presentes no contexto/arquivos são outra evidência. Não se afirma que foram comparados ao ciphertext ou que a recuperação foi anterior à ação.

Metadados turn_context permitidos registram `gpt-6.1-sol` e `effort: high` nas linhas 1303 e 1993 da thread principal, em 15/10/2026. Trata-se de configuração registrada. Modelo específico dos subagentes e do gerador de imagem: **não informado**; herança, quando relatada, sem identificador confirmado. Não foram usados prompts de sistema como fonte.

## 8. Lacunas e itens que precisam de atualização

- Registro anterior à ação não é universal: bootstraps, algumas mensagens e um complemento de pesquisa receberam registro posterior, declarado nos índices autorais.
- Há saídas truncadas e resultados resumidos. Os comandos e versões executadas estão preservados onde disponíveis; não existe alegação de cópia integral de todos os outputs.
- O filtro de recuperação teve duas tentativas sem corte confiável porque exigia marcador textual cifrado. O diagnóstico teve uma falha de sintaxe; versões e reexecuções permanecem no diário.
- O próprio relatório de sessão registra um erro 206 ao tentar gravar uma saída extensa no comando Windows; a conclusão da leitura foi recuperada em evento posterior.
- A evidência de aprovação explícita do mapa V2 não foi verificada por esta consolidação.
- Os testes atuais não demonstram PSD final reaberto, equivalência completa de capa/agradecimento, prova final de cor, crop seguro das fotos ou PDF fiel aos PNGs.
- Não foi emitido parecer final de QA. Quando montagem/revisão terminarem, adicionar relatórios e hashes novos, sem reclassificar os testes de preparação como validação final.

## 9. Prompt exato recebido para criar estes documentos

Origem: NEW_TASK do principal; literal disponível no contexto e preservado em `documentacao-001` do diário de catálogo.

```text
Prepare auditoria/SESSAO.md e auditoria/INDICE_EVIDENCIAS.md para a V2, sem afirmar conclusão. Use somente evidências presentes: fonte nova9PNGs, sua seleção de catálogo, transcrição40blocos, quatro fotosnovas, testesAPI, limitaçõescompatibilidade e máscarasoriginais. Registre decisões/porquês operacionais, modelos apenas se fonte verificável informar (caso contrário não informado/herdado sem identificador confirmado), prompts literais somente se disponíveis. Faça inventário dos diários e prompts, destaque lacunas sem inventar. Não declare que PSD/PDF final passouQA: ainda em montagem. Esta documentação será atualizada após fechamento. Leia DOCUMENTACAO_DA_EXECUCAO.md; respeite exclusão de mensagens sistema/desenvolvedor e raciocínio privado. Grave este prompt exato no seu diário e arquivos produzidos. Não acessar bridge Photopea nem escrever manifest ou scripts de montagem.
```

## 10. Complemento exato de recuperação

Origem: mensagem do principal, registrada no evento `documentacao-004`.

```text
Para recuperar delegações literais que não foram pré-gravadas no arquivo de prompts, a transcrição corrente está em C:/Users/Murilo/.codex/sessions/2026/10/14/rollout-2026-10-14T17-49-01-01a13c2c-f2f1-7ff2-bc4c-0d1dd4a714d4.jsonl. Leia estruturalmente só registros function_call/tool_call de collaboration.spawn_agent/followup_task/send_message relacionados à V2 desde o pedido Photopea. NÃO extraia mensagens de sistema/desenvolvedor, análise/raciocínio privado, credenciais ou histórico editorial anterior. Preserve arguments literais dos tool calls autorizados em auditoria/prompts/delegacoes_recuperadas.jsonl com linha, timestamp, call_id e fonte, marcando recuperação posterior (não pré-registro). Caso o formato não permita filtro confiável, registre lacuna e não improvise. O identificador de modelo só pode vir de metadados estruturais não protegidos (session_meta/turn_context), e não de prompts de sistema.
```

