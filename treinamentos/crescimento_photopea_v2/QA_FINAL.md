# QA final — Crescimento Photopea V2

**Entregável concluído e apto editorial/visualmente, com ressalva técnica de fidelidade RGB ao Photoshop histórico. Não homologado como reprodução pixel idêntica do molde aprovado.** Não há placeholder, corte de conteúdo, fonte substituída ou bloqueador visual conhecido nas 12 telas finais.

## Arquivos examinados

- [PDF de 12 páginas](entrega/Crescimento_Photopea_V2.pdf), SHA-256 `8b091a380833f74827241a89a9b89726226c2ca67a37372e00fc99acea6050d1`.
- [PSD com camadas](entrega/Crescimento_Photopea_V2.psd), SHA-256 `ced7857b6168c1a5f008f6775b433191a62bd5562b202f93267ef1ba74470bb7`.
- [PNGs finais](entrega/pngs/), 12 arquivos 1920×1080, opacos; hashes individuais em [hashes_entrega.json](auditoria/hashes_entrega.json).
- [Visão geral](entrega/visao_geral.jpg), somente contato de inspeção, não fonte usada para gerar o PDF.

## Revisões e evidências

| Controle | Resultado | Evidência |
|---|---|---|
| Conteúdo original | 40/40 blocos, 4 preparações, 12 episódios e 15 referências; zero omissões/diferenças editoriais | [QA editorial](leitura/QA_EDITORIAL_V2.md), 85 componentes da fonte e 88 do manifesto comparados ao PSD |
| Texto e estrutura | 12 pastas de página, 218 camadas, 88 textos nativos Gotham; unidades repetidas agrupadas | [QA técnico](QA_TECNICO_V2.md), leitura independente do PSD final |
| Revisão visual | 12 PNGs abertos individualmente; nenhum bloqueador permanece | [Suplemento visual final](leitura/QA_VISUAL_V2_SUPLEMENTO_FINAL.md) |
| Personalização | Listas largas/laterais, faixas com foto, citação compacta, cadeia horizontal e cenas de pessoas/arquitetura/rochas/poço; repetição de títulos apenas como continuação ou conforme fonte | Parecer visual e editorial; [direção de catálogo](leitura/direcao_catalogo_v2.md) |
| Respiro | Folga maior nas extremidades; citações/referências/fechos aproximados; filete da página 11 separado das letras | Revisão visual final e PNG 11 |
| Fotos | Quatro assuntos pertinentes, proporção preservada, fullheight lateral, sem faixa artificial; foto 09 refeita com ~30,3% topo e ~24,1% rodapé livres | Revisão visual e [assets finais](auditoria/assets_selecionados_finais.json) |
| Reabertura Photopea | PSD final reaberto pela API; 12/12 renderizações com RGB idênticos aos PNGs entregues | [Inventário real](auditoria/reabertura_psd.json), [comparação](auditoria/pixels_reabertura.json) |
| PDF | 12 imagens incorporadas sem reamostragem, RGB idênticos aos PNGs; 12 páginas renderizadas para inspeção | Comparador do montador, revisão editorial e `auditoria/pdf_render/` |
| Molde original | Quatro grupos aprovados, 1920×1080, fonte intacta | [Verificação de fechamento](auditoria/verificar_molde_fechamento.txt), hash `357e5af012e7077c074f843f3809daf4978cf51bb794f692efe3da276d90271a` |
| Manifesto legado | Adaptador explícito com textos/bounds do PSD real passou `--stage final --require-approved-template` | [Adaptador](manifesto_validacao_bellas.json), [saída](auditoria/validar_manifest_adaptado.txt) |

O arquivo `manifest_photopea.json` é o input de autoria Photopea e usa `pages/texts`; o gate antigo espera `slides/elements`. A falha inicial de esquema foi conservada em `auditoria/validar_manifest_original_fechamento.txt`. O adaptador não foi usado para fabricar arte nem substitui os checks do PSD.

A versão final do manifesto é SHA-256 `98e986cc2b5c33c7c4862966f0a57ca2078e7b9a8d3a6d67b07f9604b326d457`. O relatório técnico independente também conserva o hash anterior `a36e1f…`, antes do acréscimo do campo de proveniência `template`; não houve mudança na arte. O principal repetiu o validador completo com a versão final em [validacao_fechamento_principal.json](auditoria/validacao_fechamento_principal.json): mesmos 1.045 controles aprovados, três falhas RGB requeridas, estrutura aprovada e hashes de PDF/PSD idênticos.

## Ressalvas mantidas, sem falsa aprovação

O [validador independente](auditoria/validacao_final_independente.json) registra **1.045 controles aprovados** e conformidade estrutural aprovada. O estado global permanece `failed`/código 1 por **três exigências de identidade RGB**:

1. Capa fora do título: diferença média absoluta por canal **0,315058/255** em relação ao PNG Photoshop aprovado.
2. Agradecimento: diferença média absoluta por canal **0,688851/255**. A composição é visualmente fiel; os pixels não são iguais.
3. Segundo quadrado da capa: canal R **244** no novo render, **243** na referência medida; G177/B199 iguais.

Há ainda cinco diagnósticos binários/tipos de camada falsos que não são mascarados como sucesso: três bytes de flags de máscara e duas contagens de kinds originais. A exceção técnica é explícita e verifica canais, máscaras, bounds, opacidades e blend em vez de presumir Smart Objects ainda presentes. O bit de máscara mudou de 0x00 para 0x10 com parâmetros neutros densidade255/feather0; os outros bits, pixels e geometria foram preservados. A regra aceita apenas essa normalização específica.

O [validador Bellas original sem alterações](auditoria/validacao_bellas_original_final.json) também mantém as duas reprovações estritas de aparência de capa/agradecimento. Nenhuma baseline nova foi chamada de aprovada pelo usuário. A aprovação visual independente é uma avaliação da nova versão, não equivalência matemática ao Photoshop.

O Photopea não abriu o PSD completo do molde neste ensaio. A solução técnica extraiu inputs originais separados; três Smart Objects fixos foram convertidos em PixelLayers com máscaras preservadas nas cópias. Payloads originais permanecem no pacote. O PSD salvo foi validado em Photopea e psd-tools; não foi feito teste de round-trip no aplicativo Adobe Photoshop. O PDF é raster, sem texto selecionável.

## Agentes e documentação

O principal executou a integração e a montagem; `conteudo_novo_v2` refez a transcrição e a revisão editorial; `catalogo_novo_v2` selecionou outros layouts, escreveu o manifesto e fez crítica visual; `api_validacao_v2` estudou a API, preparou inputs técnicos e validou artefatos independentemente. Os três receberam contexto inicial novo e não usaram a arte da versão anterior de Crescimento.

A configuração observável da thread principal é `gpt-6.1-sol`/`high`, vinculada aos metadados de sessão no índice de evidências. Não houve override de modelo/esforço nas delegações; o identificador individual de execução dos subagentes e o modelo interno do serviço de imagem não foram confirmados separadamente.

[Decisões finais](auditoria/DECISOES_FINAIS.md), [índice de evidências](auditoria/INDICE_EVIDENCIAS.md), [prompts](auditoria/prompts/) e [diários](auditoria/execucao/) registram o que foi executado, rejeitado e revisado. Mensagens cifradas e ausência de alguns snapshots separados de Python são lacunas declaradas; não se afirma cobertura literal de 100% dos atos da sessão. Raciocínio privado, instruções protegidas e credenciais não fazem parte da auditoria.

**Corte da arte:** os hashes acima permanecem estáveis após a revisão final. Documentos e diários de fechamento podem crescer depois desse corte; não alteram o PDF/PSD revisados.
