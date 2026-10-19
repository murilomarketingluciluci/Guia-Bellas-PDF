# Registro da integração - 14/10/2026

## Concluído no pacote

- Regras/prompts atualizados para **APN final com conteúdo real**; placeholders apenas na fase de planejamento.
- 15 PDFs integrais e 227 miniaturas, CSV com 227 referências únicas e galeria offline com links para página original.
- Catálogo de 26 arquétipos e galeria de layouts preservados.
- Molde e PSD Rosângela, dump de 518 camadas/67 textos e estilos com bounds/transformações/leading/tracking/resolução. Zero erros de leitura de estilo nos 67 textos.
- Fotos originais do estudo, referência de produto e recortes de 730×1080, 700×1080 e 680×1080 preservados.
- Manifesto Optima com textos reais integrais e proveniência por página/bloco preparado; validador em estágio final passou.
- PSD/provas históricos de placeholders preservados em `exemplos/planejamento/` com identificação explícita.
- Validação de pacote passou: 15 fontes, 227 telas únicas, 26 layouts e links locais presentes.

## Estado da primeira integração histórica

O arquivo `exemplos/optima_manifest_conteudo_real.json` era uma entrada de conteúdo real; naquela integração, a geometria ainda precisava de validação no Photoshop. Essa fase **não executou Photoshop**. O PSD em `exemplos/planejamento/` contém placeholders e não é final. A execução posterior está registrada na seção seguinte.

O agente responsável pela execução naquela integração não retornou arquivos: a sessão foi reportada com erro `Bad Request`. Posteriormente, a APN Optima foi produzida e revista em outra etapa.

## Execução posterior: Optima final

Na **integração histórica anterior à página de agradecimento**, o exemplo foi incorporado em `exemplos/optima_final/` com 12 pastas e 12 JPEGs em `optima_provas/`. Essa descrição registra o estado daquela etapa, substituído na revisão de 13 páginas ao fim deste arquivo. O registro de saída preserva caminhos relativos ao exemplo, mas não é um manifesto de entrada no esquema do validador. O ZIP contém scripts incrementais de fotos, títulos, cartões, cor e exportação; seus caminhos locais são históricos e exigem adaptação antes de reuso. Foram preservadas capturas de correções do usuário e referências de produto/retrato.

O trabalho atual de documentação registrou as decisões adicionais do usuário em `DECISOES_APN_BELLAS.md`, atualizou manuais conflitantes e criou `skills/bellas-apn/SKILL.md`. O PSD final é o exemplo de resultado; os JSX históricos de planejamento não são scripts de regeneração desse PSD. Qualquer novo ajuste no PSD deve partir do arquivo corrente e atuar página por página.

Revisão posterior: a página 12 foi atualizada por `exemplos/optima_final/scripts_incrementais/replace_photo_12_ritual.jsx`. A nova foto mostra a atriz de `referencias/optima_dicas_pose_referencia.png` aplicando Optima, sem tatuagem, com espaço de pelo menos 15% no topo e rodapé do recorte final. PSD, prova 12, PDF, contato e registro de saída foram atualizados juntos. A antiga foto com copo de água permanece em `optima_assets/` como histórico, mas não está selecionada no registro final. A regra de 15% entrou em `skills/bellas-fotos/SKILL.md` e no QA.

A página 4 também foi reenquadrada por `exemplos/optima_final/scripts_incrementais/replace_photo_04_margens.jsx`, pois a foto anterior cortava a cabeça no topo. A nova prova preserva a margem vertical e os textos existentes. PSD, prova 4, PDF, contato e registro de saída foram atualizados novamente. A versão antiga da foto permanece como histórico.

## Scripts e comandos verificados

```powershell
python scripts/validar_manifest.py exemplos/optima_manifest_placeholders.json --stage planejamento
python scripts/preparar_optima_conteudo_real.py
python scripts/validar_manifest.py exemplos/optima_manifest_conteudo_real.json --stage final
python scripts/validar_pacote.py
python scripts/inspecionar_psd.py referencias/rosangela_editavel.psd referencias/rosangela_estilos_medidos.json
python scripts/inspecionar_psd.py referencias/molde_v1_0_base.psd referencias/molde_camadas_medidas.json
python scripts/empacotar.py
```

Galeria gerada com `scripts/gerar_galeria_227.py` e Poppler. Os scripts Python foram compilados para verificação de sintaxe. `scripts/executar_jsx.ps1` é o controlador reutilizável COM; não foi invocado por esta integração.

`scripts/planejamento/criar_optima_placeholders_historico.jsx` deriva do JSX que produziu o PSD histórico; caminhos foram adaptados para distribuição. Essa variante portátil ainda não foi reexecutada e permanece exclusivamente um exemplo de planejamento. Seu estilo/tamanho foi escolhido para rótulos curtos; não aplique aos parágrafos reais como se fosse especificação final.

## Limites e pendências para novos trabalhos

1. Em novas APNs, conferir rótulo/embalagem das fotos geradas contra a referência real; as imagens de exemplo não são packshots oficiais certificados.
2. Gotham licenciada precisa estar disponível no computador que editará o PSD; os binários de fonte não são distribuídos.
3. A revisão factual das alegações de saúde do conteúdo fonte não fez parte do escopo pedido para Optima.

## Revisão final de cor e documentação — 13 páginas

Depois das etapas históricas descritas acima, o usuário acrescentou uma tela de agradecimento e salvou **13 PNGs aprovados**. Eles foram preservados em `exemplos/optima_final/pngs_aprovados/`; o PSD corrente foi copiado para `exemplos/optima_final/optima_apn_bellas_final.psd` com 13 pastas numeradas, sem mexer no arquivo aberto do usuário. `optima_visao_geral.jpg` foi refeito com essas 13 páginas. O PDF final foi montado diretamente dos PNGs, sem reamostragem, e cada imagem extraída do PDF foi comparada pixel a pixel com o PNG de origem. O inventário atualizado está em `optima_registro_final.json`.

O teste de exportação revelou que atribuir sRGB a uma duplicata do PSD sem perfil e usar `saveAs` JPEG/PNG gerava malva `#A9708A` e aspecto opaco. O caminho `ExportOptionsSaveForWeb` PNG24, com `convertToSRGB=true` e `includeProfile=true`, **sem atribuição de perfil à duplicata**, produziu as 13 páginas com RGB idêntico aos PNGs aprovados. A cor dominante final é `#FBA9C3` no claro e `#BC718C` no escuro. Por isso `scripts/exportar_pngs_bellas.jsx` e `scripts/montar_pdf_dos_pngs.py` são a receita atual; `scripts_incrementais/export_all_srgb.jsx`, `build_srgb_pdf.py` e `optima_provas/*.jpg` permanecem apenas como registro da tentativa rejeitada. Para documentos novos, comparar uma página exportada com a referência visual antes de seguir.
