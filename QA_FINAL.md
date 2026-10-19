# QA de uma APN Bellas

Aplicação do [contrato vigente](CONTRATO_ATUAL.md). Registre projeto, versão do contrato, fonte editorial, manifesto, PSD, provas/PDF e revisores. Separe os estados **planejado**, **executado**, **conferido tecnicamente** e **aprovado visualmente**. Não preencher aprovação humana inexistente.

## 1. Processo e direção

- [ ] Diário incremental iniciado; pedido, exceções, versões e comandos/prompts operacionais preservados conforme `DOCUMENTACAO_DA_EXECUCAO.md`.
- [ ] Fonte integral lida; 13 PNGs aprovados e acervo pertinente consultados. Camadas novas derivam do molde aprovado, com hash conferido; ajustes manuais existentes preservados.
- [ ] Mapa com áreas medidas pelo texto real/Gotham, gesto, foco, função da foto e diferença para vizinhas; candidatas integrais e escolhas/descarte registrados por página interna não seriada.
- [ ] Provas no editor de tela densa/impacto e de cor exportada feitas antes do lote. H1 comparado em 1920×1080 e no contato.
- [ ] Mapa aprovado antes das fotos, ou dispensa expressa documentada com crítica interna preservada. Alterações de instruções durante o trabalho foram registradas/reavaliadas.

## 2. Integridade técnica

- [ ] Manifesto final 2.0 validado com `--stage final --require-approved-template`: fontes registradas, cobertura/omissões justificadas, IDs e caminhos de camadas, fontes/cores e estilos internos. Conversão histórica não é prova do planejamento.
- [ ] PSD único 1920×1080, pastas numeradas e nomes conforme manifesto; texto variável existe em objetos editáveis únicos, com conteúdos, fontes e cores conferidos diretamente. Sem texto oculto legado ou conteúdo variável não declarado.
- [ ] Capa altera só o título; agradecimento é idêntico ao aprovado. Elementos fixos e grupos de cards/checklists preservados.
- [ ] PSD salvo/reaberto no editor e todas as páginas reexportadas em pasta separada. Registro da ação e hashes identificam o PSD atual; `registrar_reabertura.py` apenas vincula os arquivos dessa ação.
- [ ] `validar_artefatos_bellas.py` executado com manifesto, PSD, PNGs, PDF, relatório e PNGs da reabertura. Contagens, textos/camadas e pixels das provas correspondem; não usar apenas inventário antigo.
- [ ] PNGs novos opacos, sequenciais, com ICC sRGB presente; PDF com ICCBased correspondente e pixels renderizados iguais, sem reamostragem. Provas aprovadas antigas sem ICC não foram alteradas.
- [ ] Editor alternativo tem prova prévia de importação/reabertura, texto, editabilidade, marca e exportação. Perdas de Smart Objects, aparência ou perfil são declaradas; aproximação permanece experimental até correção/decisão explícita.

## 3. Parecer editorial e visual comparativo

- [ ] Todos os pontos relevantes, números, nomes, atribuições e ressalvas comparados com a fonte. Nenhum placeholder, clipping, fonte substituída ou afirmação inventada. Revisão factual só quando solicitada; reprodução não é comprovação.
- [ ] A função editorial é preservada: condição/restrição não aparece como passo de execução; citação/referência permanecem próximas. Justificativa do manifesto corresponde à arte observada.
- [ ] Todas as telas abertas em tamanho útil e depois em contato. H1, corpo, ênfase e contraste comparados com referência aprovada de função semelhante e alternativas do mapa; a mudança de grade melhora a comunicação.
- [ ] Blocos relacionados próximos e maior respiro nas extremidades; números/cards alinhados opticamente. Séries têm caminho de leitura estável ou variação justificada. Repetição de H1/cenas em assuntos distintos foi criticada.
- [ ] Fotos acrescentam informação e variam por ação/contexto; anatomia, identidade, idade, embalagem e rótulo conferidos. Continuidade/alpha e luz preservados; pelo menos 15% no topo/rodapé livres de assunto importante após o recorte, sem faixas pintadas ou emendas.
- [ ] Cabeçalho, quadrados, B e logos legíveis; cores exportadas correspondem às provas. Gotham e corpo branco, apoio escuro `#B3718E` no claro. Nenhuma página mistura conteúdo de outra.

## 4. Entrega e alcance

Registre separadamente **parecer técnico** e **crítica visual comparativa**, com evidências, limitações e correções. Um resultado `passed` do script é técnico; `visual_approval: false` indica que o programa não concede aprovação visual.

- [ ] PSD, manifesto, fotos utilizadas, PNGs, contato, PDF e auditoria presentes em caminhos relativos. Hashes/ponto de corte e cobertura do diário conferidos; lacunas declaradas.
- [ ] O usuário aprovou o que estiver marcado como aprovação humana; páginas anteriormente aceitas foram preservadas conforme o pedido atual.
- [ ] Distribuição usa seleção controlada e inventário novo por versão, sem Git/credenciais/fontes nem sobrescrita do histórico.

O diagnóstico `--legacy` mantém o escopo histórico e não satisfaz o contrato final novo. Não alterar artes aceitas apenas para fazer um manifesto antigo passar no esquema novo.
