# Guia Bellas PDF

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

Prefira clonagem com LFS ao botão ZIP do GitHub para obter todos os editáveis. Use um caminho curto, como `C:\Bellas`, pois há nomes históricos longos. Photoshop/COM no Windows e Gotham licenciada são necessários para o backend padrão; o pacote não redistribui fontes. Editor alternativo exige escolha do usuário e prova de compatibilidade antes do lote.

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
