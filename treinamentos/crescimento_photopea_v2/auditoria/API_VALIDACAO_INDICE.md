# Índice — pesquisa API e validação independente

Agente: `api_validacao_v2`. Escopo: estudo oficial da API Photopea, identificação de Gotham local e preparação de verificações que abrem os artefatos reais. Não foi aberta sessão de navegador, usada automação COM ou alterada a arte.

## Evidências

- [Notas de API e ensaios necessários](../leitura/photopea_api_notas.md).
- [Inventário real OpenType/Gotham](../leitura/gotham_inventario.json): nomes PostScript e hashes dos membros do ZIP local, sem extração feita por este agente.
- [Validador](../scripts/validar_entrega_photopea.py): leitura independente via psd-tools; texto/runs/fontes/bounds; cobertura da transcrição nova; capa e agradecimento do molde oficial; sequência de provas; PDF/PNG por pixels; evidência de reabertura Photopea corroborada por reexportação.
- [Teste real de leitura do molde](teste_leitura_molde_validador.json): quatro grupos e quatro objetos de texto, com os quatro pesos Gotham encontrados nos runs.
- [Teste negativo de ausências](teste_negativo_ausencia.json): retorno de relatório `failed` e quatro artefatos ausentes. O wrapper PowerShell devolveu 0; o código de saída específico do Python não foi capturado nesse ensaio. Esse teste não representa validação da arte.
- [Snapshots das versões de script](scripts_executados/): versões imutáveis identificadas por SHA-256. A v1 foi recuperada literalmente do patch inicial após o primeiro ensaio; as versões seguintes foram copiadas antes da compilação correspondente.
- Diário primário do agente: `../../../auditoria/execucao/api_validacao.jsonl`, no nível raiz do pacote, conforme caminho solicitado na delegação.

## Cobertura e limites

O diário conserva comandos operacionais literais dos scans de fontes, consultas locais e ensaios; parâmetros de consultas web; justificativas e resultados resumidos; arquivos e hashes. As ferramentas mantêm as saídas integrais no registro da sessão; o JSONL não duplica todos os outputs nem o invólucro PowerShell inteiro. Os textos novos dos scripts e notas são preservados em arquivos e snapshots.

A leitura de bootstrap de `AGENTS.md` e `DOCUMENTACAO_DA_EXECUCAO.md` ocorreu antes da criação do diário e foi registrada posteriormente, com comando literal recuperado da ferramenta. Uma consulta web complementar também foi registrada após a chamada. Comunicações de acompanhamento entre agentes permanecem no histórico das ferramentas, sem duplicação integral neste diário. Portanto, este índice não afirma documentação integral anterior à ação para todas as chamadas.

Modelo/esforço específico do agente: **não informado** por fonte verificável disponível; não inferido pela capacidade ou pelo nome comercial geral. O material não contém credenciais, dados de autenticação ou instruções internas.

Ponto de corte desta preparação: antes de existir manifesto/PSD/PDF final da arte V2 no diretório inspecionado. Compilação e leitura do molde foram realizadas; a validação real da arte, a reabertura Photopea, a comparação de suas provas e a revisão visual final continuam **pendentes**. O agente principal deve solicitar nova execução quando a arte existir. Um relatório futuro terá sua própria data/hora e hash de script, sem reclassificar os ensaios prévios.

## Adendo — extração individual do molde, sem reconstrução

Pedido complementar do principal após falhas de importação dos PSDs maiores no Photopea. Foi executado [extrair_bases_photopea.py](../scripts/extrair_bases_photopea.py), produzindo [base_molde_extraida.json](../leitura/base_molde_extraida.json) e `assets/base_molde/`: 33 camadas, sendo 10 grupos e 23 folhas com caches individuais; 7 payloads embedded exatos; 6 camadas com máscaras; 4 objetos de texto separados com matriz, EngineDict, FontSet, parágrafos, índices e estilos. Ao todo, 432 arquivos de fonte/metadados, cerca de 23,9 MB; nenhum cache de folha ausente e zero erro de extração.

[verificacao_bytes_extracao.json](verificacao_bytes_extracao.json) registra 34 comparações contra nova abertura do PSD fonte: 23 caches em pixels, 7 payloads byte a byte e 4 textos/matrizes/comprimentos dos runs. [verificacao_arquivos_extracao.json](verificacao_arquivos_extracao.json) confere existência e SHA-256 de todos os 432 arquivos. O hash do molde original permaneceu idêntico antes/depois. Não houve `PSDImage.save`, composição de página ou rasterização substituta.

A ordem de irmãos do manifesto é **de baixo para cima**. `opacity_0_255` e `fill_opacity_0_255` permanecem separados; `blend_mode_code` contém o código PSD legível. PNGs de cache não aplicam opacidade de camada/grupo, blend, clipping, efeitos ou máscaras. As máscaras foram salvas separadamente sem redimensionamento; vetores/efeitos estão nos tagged blocks de cada camada. Os arquivos `.tag_*.bin` são serializações da semântica interpretada por psd-tools, não alegações de trechos binários originais. Os payloads `.embedded.*` são bytes originais exatos.

Os grupos originalmente ocultos podem ter `bbox_px` zero porque a biblioteca calcula o bbox do grupo pela visibilidade da fonte. As coordenadas de cada filho e os bboxes dos records foram preservados sem ligar/desligar grupos. Para texto, não foi inferida conversão de pontos para pixels; tamanhos/matriz/runs da fonte permanecem explícitos.

Esta extração é preparação de assets de fonte para uma **alternativa a testar**. Não reconstruiu a base, não alterou a arte final e não demonstrou solução para a falha de importação. A compatibilidade, a fidelidade visual de capa/agradecimento e a reabertura da reconstrução no Photopea continuam pendentes.

## Adendo — JSON compacto e medições somente de leitura

[bases_montagem.json](../leitura/bases_montagem.json), gerado por [derivar_bases_montagem.py](../scripts/derivar_bases_montagem.py), reúne quatro templates: capa (6 folhas), claro (2), escuro (3), agradecimento (11), além do fundo compartilhado. O arquivo minificado tem 77.970 bytes. Textos mantêm FontSet, estilos/runs, índices, matrizes, baseline e bbox visível; tamanhos derivados usam `FontSize × escala vertical da matriz`, conforme pedido explícito. AutoLeading permanece distinguido de leading manual.

Foram lidos todos os 13 PNGs Optima aprovados para contagem/amostragem raw RGB. Confirmação: `#FBA9C3` tem 1.867.590 pixels em `pagina_02.png`; `#BC718C` tem 1.783.431 em `pagina_03.png`. Fundos brutos extraídos medem `#E7A7C1` no claro/capa/agradecimento e `#A9708A` no escuro. São observações e alvos, não uma conversão de perfil demonstrada ou uma autorização para substituir globalmente as cores de fotografias.

Máscaras 5/6/28 têm respectivamente min–max 2–255, 0–255, 0–255 e 254/256/256 níveis; a fração de pixels intermediários é 94,5366% / 81,4117% / 48,2831%. Os perfis médios por linha revertem direção nos três casos. Isso comprova máscaras suaves com dados espaciais, sem identificar uma fórmula única de gradiente linear. Bordas, perfis, offsets, default externo e amostras em coordenadas do canvas constam no JSON. Nenhuma máscara foi aplicada/redimensionada, e nenhuma imagem foi salva/modificada por esse derivador.

[verificacao_bases_montagem.json](verificacao_bases_montagem.json) registra 34/34 controles aprovados, inclusive os 432 assets de fonte, manifesto de extração e PSD original ainda com hashes intactos. Um primeiro comando de impressão falhou por encoding cp1252 e foi reexecutado com JSON escapado ASCII; a falha está registrada sem reclassificação. O bridge Photopea não foi acessado.

## Adendo — empacotamento técnico de três inputs mascarados

[preparar_inputs_mascarados.py](../scripts/preparar_inputs_mascarados.py) gerou `assets/base_molde_compativel/camada_005.psd`, `camada_006.psd` e `camada_028.psd`. Cada documento tem canvas RGBA 1920×1080 e **uma camada de pixels**, com canais comprimidos RGB/alpha e máscara copiados diretamente da fonte, sem conversão por PIL, composição, aplicação de máscara, recorte ou alteração de cor/nitidez.

O registro PSD foi escrito diretamente; não foi chamado `PSDImage.save()`, pois esse método gera preview composto automaticamente. O merged-data inicial é vazio/transparente, codificado em RLE para reduzir cerca de 8 MB por arquivo, com `has_composite=false`. Não constitui página composta. O principal precisa testar leitura/renderização desses inputs no Photopea.

[inputs_mascarados.json](../leitura/inputs_mascarados.json) contém hashes, detalhes e **64/64 verificações após reabertura**: 21 por camada e integridade do PSD original. Foram conferidos inclusive os bytes comprimidos de todos os canais, pixels RGBA, bytes da máscara, máscara/bbox/background/flags/offset, opacity/fillOpacity/blend e ausência de camada de fundo. Os arquivos finais medem 7.504.378 / 10.485.366 / 9.856.002 bytes.

A perda de Smart Object é deliberada e restrita a essas cópias técnicas: elas usam os pixels de cache atuais; não mantêm o link editável para o payload, histórico de transformação/warp nem metadados não essenciais. As tags removidas estão listadas por arquivo e os payloads originais permanecem preservados separadamente. Nenhuma página final ou composição APN foi criada fora do Photopea, e o bridge não foi acessado.

## Fechamento — auditoria dos artefatos definitivos

[QA_TECNICO_V2.md](../QA_TECNICO_V2.md) e [validacao_final_independente.json](validacao_final_independente.json) registram a avaliação do PSD final de SHA-256 `ced7857b6168c1a5f008f6775b433191a62bd5562b202f93267ef1ba74470bb7`, PDF, PNGs, manifesto e reabertura. Inventário independente: [psd_final_camadas.json](psd_final_camadas.json), 218 camadas/88 textos/12 grupos de página.

A flag `--compatible-source-inputs` introduz regra auditável em `scripts/validacao_inputs_compativeis.py`: vínculo dos hashes, 23 caches e canais dos três inputs, geometria/opacidade/blend e máscara/pixels das três camadas nativas. Contagens originais de SO/shape não idênticas permanecem registradas; contagens mapeadas e três swatches conhecidas são exigidas. A única equivalência de caixa fixa é `obrigada!` + FontCaps2 para `OBRIGADA!` nativo.

A diferença de flags `0x00→0x10` das máscaras foi investigada antes de qualquer regra: somente parâmetros identidade density255/feather0 foram acrescentados. Diagnósticos binários continuam falsos; um novo check semântico específico requer todos os demais bits/pixels/dados intactos. Relatório inicial de cinco falhas foi preservado em `validacao_psd_atual_antes_regra_parametros.json` e as etapas intermediárias do resultado final também permanecem em arquivos separados.

Resultado final: 1.045 checks aprovados, **três falhas requeridas de identidade RGB**, cinco diagnósticos não idênticos. `structural_conformance=passed`, `strict_approved_appearance=failed`, `status=failed`, código1 e `visual_approval=false`. PDF/PNG e reabertura/PNG passaram 12/12. As falhas contra capa/fecho aprovados e a swatch2 (R244 versus R243) não foram abafadas por tolerância. Não foi criada baseline aprovada nova nem usado o fecho atual como referência independente.

Inspeção visual deste agente: contato geral, renders finais PDF 1/6/12 e fecho aprovado, sem promessa de revisão integral das 12 provas. Não houve alteração da arte final nem acesso ao bridge. O ponto de corte final e hashes do QA/relatório estão no evento `fechamento_auditoria_final_v2` do diário.
