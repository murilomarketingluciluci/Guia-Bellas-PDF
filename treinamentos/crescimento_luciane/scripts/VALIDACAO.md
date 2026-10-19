# Validação independente da entrega

`validar_entrega.py` importa o contrato de `scripts/validar_manifest.py` do pacote. Execute com o Python que tenha Pillow e PyMuPDF:

```powershell
python scripts/validar_entrega.py . --manifest manifesto_final.json --inventory inventario_final.json --pngs provas --pdf treinamento_final.pdf
```

O diretório passado é o projeto `treinamentos/crescimento_luciane`. Todos os argumentos de artefato são relativos a ele. O script pode ser executado de outra pasta passando o caminho completo do projeto. Os caminhos no manifesto são relativos ao próprio manifesto; os do inventário, relativos ao projeto. Referências a `../../referencias/` são permitidas, pois permanecem no pacote. Caminhos absolutos são aceitos somente dentro de campos explícitos `provenance`, `proveniencia`, `historical` ou `historico`; não são arquivos operacionais nem evidência verificada.

## Contrato do inventário

O inventário deve sair de uma leitura por JSX/COM do PSD final **reaberto após o salvamento**. `visible` é a visibilidade efetiva considerando todos os pais; `layers` é uma lista achatada, inclusive subpastas. Texto fixo herdado de marca pode usar `variable:false`. Texto de conteúdo (inclusive o H1 de agradecimento herdado) usa `variable:true`. A correspondência de cada texto de manifesto exige uma camada com o texto integral, normalizando apenas espaços e quebras de linha.

```json
{
  "psd": "crescimento_luciane.psd",
  "psd_sha256": "SHA256_DO_ARQUIVO_SALVO",
  "reopened": true,
  "canvas": [1920, 1080],
  "top_level_groups": ["01 Capa", "02 Conteúdo", "03 Agradecimento"],
  "pages": [
    {
      "number": 1,
      "group": "01 Capa",
      "layers": [
        {
          "name": "H1",
          "type": "text",
          "role": "h1",
          "variable": true,
          "visible": true,
          "text": "Crescimento",
          "font": "Gotham-Book",
          "font_runs": [{"font": "Gotham-Book"}, {"font": "Gotham-Bold"}],
          "missing_font": false,
          "bounds": [130, 180, 1400, 600]
        }
      ]
    }
  ],
  "template_evidence": {
    "cover": {
      "reference_png": "../../exemplos/optima_final/pngs_aprovados/pagina_01.png",
      "title_masks": [[100, 180, 1750, 650]]
    },
    "thanks": {
      "reference_png": "../../exemplos/optima_final/pngs_aprovados/pagina_13.png"
    }
  },
  "visual_review": {
    "all_pages_inspected": false,
    "pdf_render_inspected": false
  }
}
```

O exemplo omite as demais páginas: a lista real deve conter todas. Bounds usam `[left,top,right,bottom]` em pixels. Para fotografia, registrar `role:"photo"`, `asset_status:"final"` e `placeholder:false`; um status ausente reprova. Não classifique fotografias provisórias como finais. Cada H1 precisa ser uma camada de texto única. Todos os intervalos tipográficos devem ser lidos, porque o atributo `textItem.font` isolado pode ocultar uma substituição parcial.

Para a capa, a comparação RGB ignora exclusivamente as regiões declaradas em `title_masks`, abrangendo os títulos antigo e novo. A união dessas máscaras deve ocupar até 40% da tela. A definição da máscara também precisa ser revisada visualmente; ela não pode esconder mudanças nas marcas ou fundo. O agradecimento é comparado integralmente, pixel a pixel.

## O que a execução verifica

- Manifesto final válido, nenhum campo placeholder e arquivos operacionais relativos existentes.
- Canvas 1920×1080, numeração 1..N, contagem e correspondência entre manifesto, grupos de topo, inventário, PNGs e PDF.
- PSD presente, hash coincidente com o arquivo inventariado e registro de reabertura.
- Textos reais presentes em camadas editáveis, H1 único, Gotham em todos os intervalos, ausência de rótulos temporários e bounds dentro do canvas.
- Capa com um único elemento variável (o título), ausência de foto nova e identidade fixa comparada à referência.
- Agradecimento sem alterações de pixels.
- PNGs opacos, sequenciais, 1920×1080; cada página do PDF contém exatamente uma imagem RGB cobrindo a página, com pixels idênticos ao PNG de origem.
- Registro de revisão visual de todas as páginas e de uma renderização do PDF.

O relatório `validacao_entrega.json` inclui cada verificação, falhas e SHA-256 dos artefatos utilizados. O código 0 indica apenas que as verificações mecânicas passaram. `final_approval` permanece falso: o validador não atribui aprovação visual por log nem preenche automaticamente o QA. A prova visual/editorial deve vir de inspeção independente e ser registrada no QA de entrega. Conservar os arquivos PNG e PSD após a execução; qualquer alteração exige novo inventário e nova validação.
