# Guia Bellas para IA

## Baixar o pacote completo do GitHub

Os arquivos PSD, PSB e PDF usam Git LFS. Com [Git LFS](https://git-lfs.com/) instalado, execute:

```powershell
git lfs install
git clone https://github.com/murilomarketingluciluci/Guia-Bellas-PDF.git
cd Guia-Bellas-PDF
git lfs pull
```

Para obter os editáveis e PDFs completos, prefira esse procedimento ao botão de baixar ZIP. Depois siga o fluxo abaixo.

**Base de criação atual:** `referencias/molde_bellas_aprovado_capa_temas_agradecimento.psd`. É o PSD com capa, duas páginas vazias (clara/escura) e agradecimento. O PDF fornecido para cada tarefa é apenas fonte de conteúdo. Comece com `python scripts/verificar_molde.py`; não use o PSD final Optima, Rosângela, o molde v1 nem um PSD de treinamento anterior como fonte de camadas. Veja `MODELO_REUTILIZAVEL.md` e `DIRECAO_DE_ARTE.md`.

Repositório para outra IA produzir **APNs finais com conteúdo real**. O caminho padrão usa scripts no Photoshop; outro editor pode ser usado quando solicitado, após provar compatibilidade com o molde e as exigências de QA. Inclui referências de identidade, 227 telas históricas, 26 arquétipos, planejamento Optima e um fluxo de produção/QA. Placeholders servem para planejar o layout; uma apresentação final contém o texto real da palestrante.

## Para iniciar um teste

Abra a tarefa com **esta pasta como workspace**, anexe o PDF original e escreva apenas: **“Crie o treinamento Bellas a partir deste PDF, seguindo o AGENTS.md.”** O agente deve ler o repertório e apresentar primeiro o mapa visual com placeholders dimensionados pelo texto real. Você aprova ou corrige esse mapa; depois ele faz a direção das imagens e finaliza PSD, provas e PDF. Não precisa preparar roteiro, selecionar fotos ou repetir a identidade visual na mensagem inicial. Se faltar uma referência indispensável de produto ou pessoa, o agente identifica isso durante a análise e explica a limitação concreta.

## Comece aqui

1. `AGENTS.md`, `FLUXO_NOVO_TREINAMENTO.md`, `DIRECAO_DE_ARTE.md`, `MODELO_REUTILIZAVEL.md`, `skills/bellas-apn/SKILL.md`, `skills/bellas-fotos/SKILL.md` e `DECISOES_APN_BELLAS.md`: contrato, intenção visual antes de arquétipos, mapa com aprovação, molde de quatro grupos, produção e fotografia.
2. `PROMPT_DE_USO.md`, `MANUAL_IDENTIDADE.md` e `FONTES_E_EVIDENCIAS.md`: fluxo, Gotham, posições, cores e origem das medidas.
3. `galeria_227_telas.html`: referências históricas por página; `galeria_layouts.html`: 26 arquétipos adaptados às regras atuais.
4. `CASO_OPTIMA_12_TELAS.md` e `exemplos/optima_final/pngs_aprovados/`: aplicação concreta, com 12 telas de conteúdo e a 13ª de agradecimento adicionada depois; as 13 provas aprovadas são a referência de aparência e cor.
5. `EXECUCAO_PHOTOSHOP.md`, `GERACAO_DE_FOTOS.md` e `QA_FINAL.md`: manifesto, scripts, imagem e revisão.

## Estrutura

| Caminho | Uso |
|---|---|
| `referencias/molde_bellas_aprovado_capa_temas_agradecimento.psd` | **molde operacional** 1920×1080: capa aprovada, tema claro vazio, tema escuro vazio e agradecimento aprovado |
| `referencias/molde_bellas_aprovado_contato.jpg` | contato das quatro partes do molde operacional |
| `referencias/molde_v1_0_base.psd` | base histórica anterior com grupos claro/escuro; consultar apenas para origem |
| `referencias/rosangela_original.pdf` | referência visual principal de 15 páginas |
| `referencias/rosangela_editavel.psd`, `referencias/rosangela_camadas_medidas.txt`, `referencias/rosangela_estilos_medidos.json` | fonte editável e registro offline de Gotham, tamanhos, bounds, leading, tracking e transformações |
| `referencias/pdfs_15/`, `referencias/telas_227/` | PDFs históricos disponíveis e miniaturas individuais |
| `referencias/contatos_15_pdfs/` | mosaicos das 227 telas |
| `indice_227_telas.csv`, `fontes_15_pdfs.json` | origem, página e caminhos relativos de cada referência |
| `catalogo_atual_26_layouts.json`, `galeria_layouts.html` | arquétipos atuais; geometria aproximada, não régua tipográfica |
| `referencias/catalogo_historico_26_layouts.*` | abstração histórica; seis layouts exigiram adaptação da foto |
| `referencias/exemplos/` | provas do molde/Rosângela e estudos de fotos |
| `exemplos/optima_manifest_placeholders.json` | etapa de planejamento, jamais manifesto final |
| `exemplos/optima_manifest_conteudo_real.json` | texto real integral preparado; ainda requer geração/ajuste e prova visual no Photoshop |
| `exemplos/planejamento/` | PSD, PNGs e contato históricos com placeholders, preservados como planejamento |
| `exemplos/optima_final/` | PSD/PDF com 13 páginas, registro de saída, fotos usadas, 13 PNGs aprovados, contato e capturas de correções do usuário |
| `exemplos/optima_final/pngs_aprovados/` | fonte visual final; os JPEGs em `optima_provas/` são uma exportação histórica com cor rejeitada |
| `exemplos/optima_final/optima_codigo_historico.zip` | scripts incrementais efetivamente usados como referência de método; possuem caminhos locais antigos e não devem ser executados diretamente |
| `DECISOES_APN_BELLAS.md`, `skills/bellas-apn/SKILL.md`, `skills/bellas-fotos/SKILL.md` | regras confirmadas após correções do usuário e fluxos de APN/fotografia para novos agentes |
| `referencias/optima_frasco_proporcao_real.png`, `referencias/optima_modelo_referencia.png` | imagens fornecidas pelo usuário que orientaram produto e retrato no caso Optima |
| `referencias/optima_dicas_pose_referencia.png` | atriz e gesto de aplicação usados na revisão posterior da página 12; a tatuagem foi removida na nova foto |
| `scripts/` | validação, geração por script e prova |

`REGISTRO_DA_EXECUCAO.md` distingue o estudo histórico da APN Optima produzida posteriormente. O PSD com 13 pastas, o PDF e os PNGs aprovados estão em `exemplos/optima_final/`. O exemplo em `exemplos/planejamento/` contém placeholders e não é entrega final.

`exemplos/optima_manifest_conteudo_real.json` é um **manifesto histórico de entrada** de 12 telas que passa no validador, mas conserva geometria do planejamento, conteúdo antigo da capa e não inclui a página 13 adicionada depois. Não o execute como se reproduzisse a arte aprovada. `exemplos/optima_final/optima_registro_final.json` é um **registro da saída executada** (textos, 13 provas e assets), não usa o esquema `template/slides/elements` e não deve ser passado a `validar_manifest.py`.

## Regras obrigatórias

Capa com somente o título do treinamento como texto de conteúdo, podendo preservar imagem de marca muito esmaecida já aprovada no molde; alternância rosa claro/malva escuro; fotos com altura completa tocando lateral ou recorte transparente bem integrado; Gotham e estilos do PSD; corpo branco; `#B3718E` para apoio escuro em fundo claro; H1 em uma camada de texto; cabeçalho/rodapé preservados; cada página em uma pasta no mesmo PSD. Edite Photoshop exclusivamente por JSX/COM, uma página de cada vez quando o PSD já contém ajustes manuais. Leia o conteúdo real antes de definir as telas. A prova final não pode mostrar rótulos H1/BLOCO/ITEM.

Para cada treinamento novo, **solicite apenas o PDF original sem edição**. Releia as páginas do material e o repertório Bellas. Apresente primeiro um mapa com placeholders **dimensionados pelo texto real em Gotham** e aguarde sua aprovação; depois dirija as imagens e finalize o PSD. Reutilize a capa aprovada mudando somente o título e a página de agradecimento aprovada sem qualquer mudança. O número de páginas intermediárias depende do conteúdo, não do caso Optima.

**Cor e exportação:** no Optima, os PNGs aprovados têm rosa claro dominante `#FBA9C3` e malva `#BC718C`. Atribuir sRGB ao PSD sem perfil e usar `saveAs` gerou uma versão opaca, rejeitada. `scripts/exportar_pngs_bellas.jsx` usa Save for Web PNG24 numa duplicata sem alterar perfil; seus 13 resultados foram iguais aos PNGs aprovados pixel a pixel. `scripts/montar_pdf_dos_pngs.py` junta os PNGs sem reamostrar e confere os pixels extraídos do PDF. Para uma apresentação nova, confira uma página de teste antes de exportar todas.

## Portabilidade e instalação

Gere o pacote com `python scripts/empacotar.py`. Extraia `Guia_Bellas_IA.zip` em um **caminho curto**, por exemplo `C:\Bellas\`, mantendo a pasta `Criador de PDF Agente/` como raiz, e abra **essa pasta** como workspace. Alguns arquivos históricos têm nomes longos e uma extração dentro de pastas já profundas pode atingir o limite de caminho do Windows. Execute `python -m pip install -r requirements.txt`, `python scripts/verificar_molde.py` e `python scripts/validar_pacote.py` após a extração. O ZIP inclui o molde, referências, documentação, skills, scripts e exemplos; o inventário `inventario_sha256.json` registra os arquivos incluídos. Os caminhos operacionais são relativos à raiz. Para produção padrão, instale Photoshop no Windows e as fontes Gotham licenciadas; o ZIP **não distribui os arquivos de fonte** presentes em registros históricos. O controlador COM requer PowerShell e Photoshop com automação COM disponível.

As imagens de produto geradas são estudos: compare rótulo/embalagem com a referência real. Os PDFs são material do usuário para uso no projeto; o pacote não concede direitos adicionais de redistribuição. As medidas de texto registradas no PSD precisam ser interpretadas junto à transformação e à resolução do documento. A geração de miniaturas históricas pode requerer Poppler (`pdftoppm`). Photopea foi usado em um experimento autorizado, mas seus scripts históricos não constituem um montador de produção portátil: um novo agente deve testar a API, a reabertura do PSD, a editabilidade, a capa/agradecimento e os perfis ICC antes de adotá-lo.

Para um manifesto **novo**, use `python scripts/validar_manifest.py CAMINHO --stage final --require-approved-template`. Após produzir, execute `scripts/validar_artefatos_bellas.py` conforme `EXECUCAO_PHOTOSHOP.md`: ele lê o PSD diretamente, acusa textos ocultos legados e confere ICC e PDF renderizado. A crítica de variedade visual é feita no contato, conforme `DIRECAO_DE_ARTE.md`.

## Comandos de pré-checagem

```powershell
python scripts/verificar_molde.py
python scripts/validar_pacote.py
# Exemplo histórico de sintaxe, não ponto de partida de novo treinamento:
python scripts/validar_manifest.py exemplos/optima_manifest_placeholders.json --stage planejamento
```

Após aprovar o mapa e produzir a apresentação real, execute o validador com `--stage final` e o manifesto **atual**, depois siga `EXECUCAO_PHOTOSHOP.md`. Para o PDF, use `python scripts/montar_pdf_dos_pngs.py PASTA_DOS_PNGS ARQUIVO_SAIDA.pdf`; o comando verifica igualdade de RGB. Um retorno de sucesso do Photoshop ou do validador não substitui a inspeção de todas as provas.
