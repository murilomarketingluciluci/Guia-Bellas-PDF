# Fluxo para criar um novo treinamento Bellas

## 0. Abra a auditoria antes de executar

Siga `DOCUMENTACAO_DA_EXECUCAO.md`: inicie um diário incremental no projeto antes da primeira ação. Documente comandos/parâmetros e prompts literalmente antes do uso, versões dos scripts, decisões e motivos operacionais, resultados, falhas e evidências após cada ação. Exija o mesmo dos subagentes. O resumo final não substitui esse registro. Não invente texto ausente; identifique limites e a fonte de qualquer configuração de modelo informada.

## 1. Entrada: peça somente o PDF base

Quando o usuário quiser iniciar outro treinamento, solicite **apenas o PDF original, sem edição ou adaptação prévia**. Não peça que ele prepare roteiro, resuma o conteúdo, escolha layouts, separe imagens ou preencha manifesto. O agente assume essa análise. Use os outros materiais que o usuário oferecer espontaneamente, mas não os transforme em exigência inicial. Se o PDF não estiver disponível, esta é a única informação necessária para começar.

## 2. Releia o repertório antes de desenhar

Em cada novo trabalho, veja **todas as páginas do PDF recebido** e registre conteúdo, sequência, números, ressalvas e potencial de imagem. Veja as 13 páginas de `exemplos/optima_final/pngs_aprovados/` em contato e em resolução útil. Reveja as galerias de 227 telas e 26 arquétipos; abra no tamanho original as páginas dos PDFs Bellas que tiverem estrutura ou assunto semelhante. Consulte o PSD aprovado para entender grupos, tipografia real, cabeçalho, rodapé, B, cores e zonas de foto. O PDF enviado costuma ter diagramação amadora: ele é fonte de conteúdo, **não** uma grade, hierarquia tipográfica ou direção visual a copiar. Não economize leitura nem faça a seleção visual só por texto extraído ou por miniaturas.

## 3. Primeiro entregue um mapa visual com placeholders

Antes de gerar fotos ou produzir a arte final, prepare um mapa de todas as páginas e uma prova visual simples de cada uma. O mapa identifica: página e tema, trechos do PDF de origem, H1 proposto, quantidade e tipo de blocos, texto real que precisará caber, peso estimado da informação, tema claro/escuro, área proposta de foto, posição das marcas e razão para a composição. Os placeholders podem exibir rótulos (`TÍTULO`, `TEXTO`, `FOTO`) na **prova de planejamento**, mas a área de texto deve ser calculada com o conteúdo real do PDF: Gotham, estilos medidos no PSD, quebras e entrelinhas plausíveis, largura de linha e número de linhas. Teste visualmente o texto em escala próxima da final. Não deixe uma caixa pequena só porque o placeholder é curto; não ocupe com texto uma área que poderia comportar uma foto. Se o conteúdo não couber com leitura boa, reparta-o em mais telas.

Planeje a fotografia junto com a distribuição de informação, mesmo antes de escolher a cena. Reserve faixas de altura completa, telas inteiras ou espaço para modelo recortada quando contribuírem para a narrativa. Varie informação e imagem; o primeiro planejamento Optima subestimou a quantidade de fotos que caberia. Use páginas sem foto quando a densidade ou a história justificar, não como padrão automático. Preserve os 15% superiores e inferiores da área fotográfica para cabeçalho e assinatura já no mapa.

**Apresente o mapa e suas provas ao usuário para aprovação antes de avançar.** Corrija o mapa conforme o retorno. Esta aprovação é para a arquitetura das páginas; não transforma placeholders em arte final nem aprova uma imagem que ainda não foi feita.

Ao distribuir os blocos, siga a preferência registrada em `DECISOES_APN_BELLAS.md`, seção 2.1: concentre o maior respiro nas extremidades e aproxime conteúdos relacionados. Não espalhe caixas por toda a altura apenas para ocupar a tela; confira proximidade, hierarquia e legibilidade com o texto real.

## 4. Depois do mapa aprovado, defina a direção de imagens

Para cada espaço de foto aprovado, proponha uma cena coerente com a mensagem da página, o papel da foto, a cor das páginas vizinhas e o nível de realismo Bellas. Registre o assunto, gesto, cenário/recorte transparente, roupa, luz, enquadramento, produto, margem de 15% e motivo de variar em relação às outras fotos. Compare com `skills/bellas-fotos/SKILL.md`. Se o produto precisar de embalagem exata, use a referência real disponível no PDF/repositório; se não existir, sinalize a limitação antes de afirmar fidelidade. Gere cada foto do zero com um prompt coeso; refaça uma geração ruim inteira em vez de criar colagens ou remendos. Inspecione anatomia, rosto, frasco, rótulo, bordas e legibilidade das marcas após o encaixe.

## 5. Produza e confira o PSD final

Comece por uma cópia de `referencias/molde_bellas_aprovado_capa_temas_agradecimento.psd` e siga `MODELO_REUTILIZAVEL.md`. Use o **mesmo grupo/composição da capa aprovada** e altere **somente o texto do título do treinamento**. A capa não ganha resumo, benefícios, subtítulo ou outra foto principal. Reutilize a **mesma página de agradecimento aprovada** sem alterar texto, posição, cores ou elementos; ela é sempre a última tela. Os grupos de tema claro e escuro já estão vazios e prontos para duplicação. Entre esses extremos, a quantidade de páginas de conteúdo varia com o material e a leitura. Não fixar 12 ou 13 como número universal.

Monte cada página de conteúdo em pasta numerada no mesmo PSD. Preserve as camadas fixas. Substitua todos os placeholders por texto real, com H1 em um único objeto de texto com estilos internos. Agrupe cards completos para edição humana. Trabalhe página por página e revise o resultado em tamanho de apresentação, corrigindo quebras, espaçamento, fotos, cor e logos. A meta de entrega é um PSD feminino, refinado, coerente e plenamente editável, não apenas um arquivo que o script conseguiu salvar. É aceitável fazer verificações visuais e ajustes manuais de composição por JSX/COM; não automatize escolhas de hierarquia que pedem julgamento.

Exporte PNG24 pelo método de `scripts/exportar_pngs_bellas.jsx`, compare com os PNGs aprovados e monte o PDF com `scripts/montar_pdf_dos_pngs.py`. Entregue PSD, PDF, provas, contato, assets e registro de QA. Confira a igualdade entre contagem de grupos, provas e páginas e faça uma inspeção visual de **todas** as telas. Para a orientação completa, siga `skills/bellas-apn/SKILL.md`, `DECISOES_APN_BELLAS.md` e `QA_FINAL.md`.
