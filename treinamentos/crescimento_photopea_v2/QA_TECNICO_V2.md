# QA técnico independente — Crescimento Photopea V2

Revisor: `api_validacao_v2`, 15/10/2026. **Estrutura e integridade dos artefatos: conformes aos controles executados. Identidade RGB com os PNGs Photoshop aprovados: reprovada.** Este relatório não concede aprovação visual final nem chama as duas renderizações de pixel idênticas.

## Arquivos efetivamente verificados

| Artefato | Identificação |
|---|---|
| PSD | `entrega/Crescimento_Photopea_V2.psd` — SHA-256 `ced7857b6168c1a5f008f6775b433191a62bd5562b202f93267ef1ba74470bb7` |
| PDF | `entrega/Crescimento_Photopea_V2.pdf` — SHA-256 `8b091a380833f74827241a89a9b89726226c2ca67a37372e00fc99acea6050d1` |
| Manifesto | `manifest_photopea.json` — SHA-256 `a36e1fa89870094b9a6421d29898e95350236ae663d46f5a4e67ab5d6f57fd55` |
| Provas | `entrega/pngs/pagina_01.png` a `pagina_12.png` |
| Reabertura | `auditoria/reabertura_psd.json` e `auditoria/reabertura_pngs/` |
| Inventário independente | `auditoria/psd_final_camadas.json`, lido diretamente do PSD final por psd-tools |
| Resultado completo | `auditoria/validacao_final_independente.json` |

O validador foi executado com `--compatible-source-inputs`, sem `--psd-audit-only` e sem baseline substituta. Resultado: **1.045 checks aprovados, três checks requeridos reprovados de identidade RGB, cinco diagnósticos binários/kinds não idênticos preservados**. `structural_conformance=passed`, `strict_approved_appearance=failed`, `visual_approval=false`. O programa mantém `status=failed` e código de saída **1**; não houve conversão desse resultado em aprovação total.

## Controles estruturais concluídos

- PSD real aberto independentemente: canvas 1920×1080, 12 pastas de página numeradas, 218 camadas no total, 88 objetos de texto editáveis. Somente a capa está visível no estado salvo.
- Texto previsto por `pages[].texts[]` localizado em objetos editáveis pelos nomes reais; conteúdos, famílias e cores dos runs conferidos. H1s permanecem em um objeto por título. Fontes usadas: Gotham-Book, Gotham-Bold, Gotham-Light e Gotham-Medium.
- Os 40 blocos da transcrição independente `leitura/conteudo_v2.json`, os episódios/atribuições/referências e ocorrências dos números foram encontrados no texto real do PSD. A revisão editorial humana permanece no parecer do agente de conteúdo.
- Não foram encontrados rótulos de planejamento nas camadas de texto visíveis. Isso não é OCR nem garantia automática contra palavras rasterizadas dentro de fotografias.
- Fundos nativos `FUNDO` conferidos em todas as páginas, por extremos dos canais: claro `#FBA9C3`, escuro `#BC718C`. Cores dos objetos de texto e seus destaques correspondem ao manifesto.
- 12 PNGs opacos, RGB/RGBA e 1920×1080, com numeração sequencial.
- PDF com 12 páginas, uma imagem incorporada por página, sem reamostragem detectada: os RGB das 12 imagens extraídas são **idênticos aos 12 PNGs da entrega**.
- Hash do PSD da reabertura corresponde ao PSD final. A listagem real de páginas foi recebida e a reexportação de **12/12 páginas reabertas é idêntica aos PNGs da entrega**.

## Regra explícita de compatibilidade

A importação integral do molde falhou na execução do principal; a reconstrução pela API utilizou caches individuais e três PSDs técnicos de entrada. A flag não dispensa identidade das fontes: o validador abre o molde oficial, confere seu hash com a extração, examina os 23 caches e os três inputs empacotados e compara canais/máscaras reais. Não se limita ao campo `passed` de um JSON.

As camadas nativas `FOTO FIXA ORIGINAL - 5`, `- 6` e `- 28` foram localizadas unicamente nas páginas 12, 12 e 1. **Bbox, opacidade, fillOpacity, blend, pixels RGBA, bbox/background/estado da máscara e pixels da máscara coincidem com a fonte**. Os bytes comprimidos dos inputs também foram vinculados ao original.

Smart Objects, shapes e solid fills originais podem ser PixelLayers nesta rota. Os checks antigos `cover_fixed_layer_kind_counts` e `thanks_fixed_layer_kind_counts` continuam registrados como falsos, mas são diagnósticos sob a flag. Os checks requeridos novos exigem contagem mapeada coerente; a capa só admite as três swatches restauradas conhecidas, com nomes/bboxes conferidos. A perda de editabilidade do conteúdo interno dos SOs nas cópias técnicas está declarada em `leitura/inputs_mascarados.json`; os payloads originais permanecem preservados.

### Flags das máscaras: diferença documentada, sem tolerância genérica

Nos três casos, o byte original `0x00` passou para `0x10`: somente `parameters_applied` mudou. `pos_relative_to_layer`, `mask_disabled`, `invert_mask`, `user_mask_from_render` e os bits não documentados permanecem iguais. O Photopea acrescentou parâmetros explícitos `user_mask_density=255`, `user_mask_feather=0.0`, sem parâmetros vetoriais. Densidade 255 representa participação 255/255, e feather zero não adiciona suavização.

O check de igualdade binária das flags permanece falso como diagnóstico. O check semântico requerido aceita **exclusivamente** esse bit e esses valores identidade, além de exigir todos os outros dados/pixels da máscara exatos. Não aceita outro bit, densidade menor, feather positivo ou alteração de pixels. Evidência: `auditoria/diferenca_flags_mascaras.json`; interpretação corroborada no código primário instalado psd-tools 1.25.0, `composite.py`, `_get_mask` (`share=density/255`). Nenhum compositor foi chamado nesta revisão.

### Única equivalência de caixa do texto fixo

A fonte contém `obrigada!` com `FontCaps=2`; o texto nativo contém `OBRIGADA!` porque o backend não implementou `TextCase.ALLCAPS`. A equivalência é permitida **somente para essa cadeia e com FontCaps2 comprovado na fonte**. Os demais textos fixos continuam sensíveis à caixa. O sentido não foi alterado. Essa regra não transforma os pixels do texto em idênticos.

## Limitações de identidade RGB mantidas como falhas

As referências independentes são sempre os PNGs aprovados em `exemplos/optima_final/pngs_aprovados/`. O fecho atual nunca foi usado como sua própria baseline.

| Check estrito | Medição contra referência aprovada | Estado |
|---|---|---|
| Fecho vs `pagina_13.png` | 1.717.369 de 2.073.600 pixels diferentes; 82,82065%; MAE RGB 0,688851/255; maior diferença em um canal 90 | **Reprovado** |
| Capa vs `pagina_01.png`, fora da união das caixas do título antigo/novo | 711.665 de 1.867.968 pixels diferentes; 38,09835%; MAE RGB 0,315058/255; maior diferença em um canal 139 | **Reprovado** |
| Swatch 2 da capa, RGB amostrado no centro | Referência `#F3B1C7` (243,177,199); nativa `#F4B1C7` (244,177,199) | **Reprovado** |

MAE baixa não foi usada como tolerância ou aprovação. A quantidade elevada de pixels diferentes tampouco foi omitida. As medições mostram diferenças entre a reconstrução/renderização nativa e a referência Photoshop; não foi atribuída uma causa comprovada a cada pixel.

## Inspeção visual técnica e alcance

Foram abertos o contato geral, os renders do PDF das páginas 1, 6 e 12 em resolução útil e o PNG aprovado de agradecimento. Nessa amostra, título/cabeçalho/marcas permanecem visíveis; na 6, os textos estão sobre as faixas e legíveis; no fecho, a composição é visualmente correspondente à referência, sem que isso elimine a reprovação RGB. O valor de exposição `brightnessEvent=-35` foi relatado pelo principal; não foi deduzido dos pixels por este agente.

Esta amostra não substitui a inspeção integral das 12 telas em resolução útil pelo revisor visual, nem comprova anatomia, margens fotográficas, respiro ou contraste de toda a apresentação. Nenhum PSD, PNG, PDF ou camada da arte final foi alterado nesta auditoria. O bridge ocupado de autoria não foi acessado.

## Auditoria e reprodução

Comando final literal registrado em `auditoria/execucao/api_validacao.jsonl` na raiz do pacote:

```text
python treinamentos/crescimento_photopea_v2/scripts/validar_entrega_photopea.py --project treinamentos/crescimento_photopea_v2 --manifest manifest_photopea.json --psd entrega/Crescimento_Photopea_V2.psd --png-dir entrega/pngs --pdf entrega/Crescimento_Photopea_V2.pdf --reopen-report auditoria/reabertura_psd.json --reopen-png-dir auditoria/reabertura_pngs --compatible-source-inputs --output auditoria/validacao_final_independente.json
```

Versões executadas estão preservadas por hash em `auditoria/scripts_executados/`. Relatórios anteriores não foram apagados: incluem a primeira reprovação de cinco checks e as etapas antes da regra de parâmetros neutros, das verificações de cor e da classificação RGB. O índice `auditoria/API_VALIDACAO_INDICE.md` declara cobertura e lacunas do diário. Modelo/esforço específico do agente: não informado por fonte verificável disponível.
