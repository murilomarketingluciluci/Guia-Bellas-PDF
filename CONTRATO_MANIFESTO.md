# Manifesto Bellas final 2.0

Trabalhos novos usam **`schema_version: "2.0"`** e `stage: "final"`. O contrato de marca/processo está em [CONTRATO_ATUAL.md](CONTRATO_ATUAL.md). O formato é independente do editor; um backend recebe este contrato antes da montagem. Manifestos antigos `slides/elements` ou `pages/texts` continuam intactos. `--legacy` permite diagnóstico do esquema antigo, sem homologar entrega nova nem demonstrar planejamento anterior.

## Estrutura

- `canvas`: `[1920,1080]`.
- `template.psd`: caminho relativo até o molde aprovado. Não admite outro PSD doador.
- `sources`: lista de trechos com `id` único, `file` relativo existente dentro do pacote, `page` inteiro positivo e `text` original. Fonte não é validação factual; a transcrição precisa de comparação editorial com o PDF.
- `omitted_sources`: opcional, lista de `{id, reason}` para decisões editoriais de omissão. Cada fonte registrada deve ter destino ou decisão de omissão; uma fonte não pode estar simultaneamente usada e omitida. Isso confere o cadastro, não descobre trechos que o agente esqueceu de transcrever.
- `slides`: sequência `number: 1..N`, `group` igual ao nome da pasta real de topo no PSD, `theme: "claro"|"escuro"` e `elements`.
- Primeira página: `fixed: "cover"`, tema claro e **um único elemento H1**. Última: `fixed: "thanks"`, tema claro, **`elements: []`**. O agradecimento é arte fixa; não recriar um título para satisfazer o esquema. Páginas internas não declaram `fixed`.
- Campos criativos como `gesture`, `dominant`, `photo_function`, `composition_reason`, `neighbor_difference` e candidatas continuam documentando o mapa. A crítica visual deve verificar o resultado, não apenas sua presença.

## Elementos

Cada elemento tem `role` e `rect: [x,y,w,h]` normalizado entre 0 e 1. A caixa permanece dentro do canvas. Os papéis textuais são `h1`, `body`, `bullet`, `card`, `callout` e `quote`; `line`, `chart` e `photo` não são objetos de texto. Gráficos com rótulos editáveis declaram seus rótulos separadamente como texto. Há exatamente um H1 por página variável, em uma camada editável.

Para texto final, acrescente:

```json
{
  "id": "p02_explicacao",
  "role": "body",
  "rect": [0.45, 0.30, 0.48, 0.35],
  "layer": "CONTENT/Explicacao",
  "text": "Texto real conferido com a fonte.",
  "font": "Gotham-Book",
  "color": "FFFFFF",
  "source_ids": ["fonte_p02_bloco01"]
}
```

Esse fragmento explica o formato; não é conteúdo final de uma APN. `id` é único na apresentação; `layer` é o caminho exato relativo à pasta `group`, usando `/`, único naquela página. O validador confere a existência de um objeto `type`, texto, visibilidade dos ancestrais, fonte e cor reais. Texto rasterizado não satisfaz o contrato. Texto variável não declarado no manifesto também é recusado; os textos fixos são comparados com o molde.

`font` usa `Gotham-Book`, `Gotham-Light`, `Gotham-Medium` ou `Gotham-Bold`. `color` é HEX RGB de seis dígitos, com `#` opcional; `body` é sempre `FFFFFF`. Outros papéis seguem a direção de marca e a prova de contraste. Para H1 com ênfases, `runs` contém intervalos `{start,end,font,color}`; início inclusivo e fim exclusivo, por caracteres Unicode do texto. Intervalos não se sobrepõem; campos omitidos herdam a base. O leitor converte os offsets UTF-16 do PSD para conferir caracteres, inclusive caracteres fora do plano básico.

Foto ambiental: `asset` relativo existente, `fit: "cover"`, altura inteira e lateral ou full canvas. Modelo transparente pode declarar `photo_kind: "cutout"` e `fit: "contain"` ou `"cover"`, com outra área; alpha, bordas, luz e margens aplicadas exigem inspeção visual. A imagem fixa esmaecida da capa pertence ao molde e não entra como `photo` nova.

## Comandos e alcance

```powershell
python scripts/verificar_molde.py
python scripts/validar_manifest.py CAMINHO/manifesto_final.json --stage final --require-approved-template
```

Depois de salvar e **reabrir o PSD no editor escolhido**, reexporte todas as páginas para uma pasta separada `reabertura_pngs`, com nomes `pagina_01.png`, etc. Registre a ação no diário e gere seu vínculo de hashes:

```powershell
python scripts/registrar_reabertura.py --psd CAMINHO/final.psd --png-dir CAMINHO/reabertura_pngs --editor Photoshop --output CAMINHO/reabertura.json
python scripts/validar_artefatos_bellas.py --manifest CAMINHO/manifesto_final.json --psd CAMINHO/final.psd --png-dir CAMINHO/provas_png --pdf CAMINHO/final.pdf --reopen-report CAMINHO/reabertura.json --reopen-png-dir CAMINHO/reabertura_pngs --report CAMINHO/qa_tecnico.json
```

O registro de reabertura contém `psd_sha256` e `pages: [{number,sha256}]`, vinculados à versão do PSD e aos PNGs reexportados. O registrador **não abre o editor**; a execução de abertura/exportação deve estar no diário. O QA compara esses hashes e pixels com as provas de entrega. O relatório não é assinatura externa nem comprovação independente de que o comando de exportação foi executado corretamente.

Na validação final nova, sRGB é obrigatório mesmo sem `--require-srgb-icc`: ICC nos PNGs, ICCBased no PDF e pixels renderizados correspondentes. Capa e agradecimento continuam comparados com as provas aprovadas. `--legacy` relaxa apenas o contrato novo de manifesto e a obrigação nova de evidência de reabertura/ICC; preserva as verificações mecânicas aplicáveis e nunca declara aprovação visual. Pode ser combinado com `--require-srgb-icc` para diagnosticar perfis antigos.

O validador não decide anatomia, rótulo de produto, fidelidade semântica, alinhamento óptico, contraste percebido ou qualidade criativa. Esses critérios continuam nos dois pareceres de [QA_FINAL.md](QA_FINAL.md).
