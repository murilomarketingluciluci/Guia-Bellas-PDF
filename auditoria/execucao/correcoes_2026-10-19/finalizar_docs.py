"""Atualiza entrada e checklist com o contrato consolidado e comandos verificáveis."""
from pathlib import Path
ROOT = Path(__file__).resolve().parents[3]
(ROOT/"README.md").write_text("""# Guia Bellas PDF

Base para um agente produzir APNs Bellas com conteúdo real, identidade aprovada e PSD editável. O pacote reúne molde, documentação, scripts, 227 telas de referência de 15 PDFs, 26 arquétipos e exemplos executados. O julgamento de composição continua com o agente e com a revisão visual.

## Começar

Abra esta pasta como workspace, anexe somente o PDF original e peça: **“Crie o treinamento Bellas a partir deste PDF, seguindo o AGENTS.md.”** O agente apresenta o mapa antes das imagens e da arte final, salvo dispensa expressa. Para continuar um trabalho, indique o PSD corrente e as alterações desejadas.

- [AGENTS.md](AGENTS.md): entrada e rotas de leitura.
- [Contrato vigente 2.0](CONTRATO_ATUAL.md): fonte única das regras de marca/processo.
- [Fluxo](FLUXO_NOVO_TREINAMENTO.md), [direção de arte](DIRECAO_DE_ARTE.md) e [molde](MODELO_REUTILIZAVEL.md): execução e decisões de composição.
- [Manifesto final 2.0](CONTRATO_MANIFESTO.md): proveniência e vínculo entre texto, PSD e provas.
- [QA](QA_FINAL.md) e [auditoria](DOCUMENTACAO_DA_EXECUCAO.md): evidências e limites da aprovação.

## Baixar e instalar

PSDs, PSBs e PDFs usam [Git LFS](https://git-lfs.com/). Com Git e Git LFS instalados:

```powershell
git lfs install
git clone https://github.com/murilomarketingluciluci/Guia-Bellas-PDF.git
cd Guia-Bellas-PDF
git lfs pull
python -m pip install -r requirements.txt
python scripts/verificar_molde.py
python scripts/validar_pacote.py
```

Prefira clonagem com LFS ao botão ZIP do GitHub para obter todos os editáveis. Use um caminho curto, como `C:\\Bellas`, pois há nomes históricos longos. Photoshop/COM no Windows e Gotham licenciada são necessários para o backend padrão; o pacote não redistribui fontes. Editor alternativo exige escolha do usuário e prova de compatibilidade antes do lote.

## Referências e históricos

| Caminho | Função |
|---|---|
| `referencias/molde_bellas_aprovado_capa_temas_agradecimento.psd` | Única base de camadas para treinamento novo: capa, dois temas vazios e agradecimento |
| `exemplos/optima_final/pngs_aprovados/` | 13 provas aprovadas de acabamento/cor; não regravar |
| `galeria_227_telas.html`, `indice_227_telas.csv` | Repertório completo e localização de fontes/páginas |
| `galeria_layouts.html`, `catalogo_atual_26_layouts.json` | Índice resumido de 26 arquétipos, sem substituir a capa aprovada |
| `MANUAL_IDENTIDADE.md`, `referencias/rosangela_estilos_medidos.json` | Estilos Gotham e medidas de referência |
| `DECISOES_APN_BELLAS.md`, `FONTES_E_EVIDENCIAS.md` | Proveniência das decisões e limites das fontes |
| `treinamentos/` | Trabalhos e auditorias específicos; não usar como doadores de páginas |

`exemplos/planejamento/`, os JPEGs `optima_provas/`, o molde v1 e scripts históricos são estudos ou tentativas anteriores. O manifesto Optima de 12 telas não reproduz a arte aprovada de 13 páginas. O registro final Optima é evidência de saída, não manifesto 2.0. Inspeção antiga usa `--legacy` explicitamente e preserva suas reprovações; não homologa um final novo.

## Testes e distribuição

```powershell
python -m unittest discover -s tests -v
python scripts/empacotar.py --dry-run
python scripts/empacotar.py
```

O empacotador usa arquivos rastreados pelo Git e respeita exclusões locais; arquivos novos precisam estar adicionados ao índice. Outros trabalhos não rastreados ficam fora. Recusa credenciais reconhecidas, assets LFS ainda não baixados e entradas inseguras; não substitui uma auditoria de segredos. Não inclui `.git`, caches nem arquivos de fontes. Em pacote extraído sem Git, use `--filesystem` explicitamente.

A saída nova fica em `dist/`, com nome por data/hora e um inventário próprio dentro do ZIP e em arquivo lateral. `--output CAMINHO.zip` permite escolher o destino, recusando sobrescrita. `--report CAMINHO.json` grava uma conferência em arquivo novo. O inventário histórico `inventario_sha256.json` permanece intacto.
""",encoding="utf-8")
(ROOT/"QA_FINAL.md").write_text("""# QA de uma APN Bellas

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
""",encoding="utf-8")
print("README e QA atualizados; originais preservados no snapshot.")
