# QA de uma APN final

Registre apresentação, data, manifesto **atual**, PSD, quantidade de telas e responsável pela revisão. A contagem de provas deve coincidir com a de pastas de página e a do manifesto de produção atual; o manifesto histórico Optima de 12 telas não descreve a arte aprovada de 13 páginas.

## Processo e aprovação do mapa

- [ ] No início do trabalho foi solicitado apenas o PDF base sem edição; o agente leu todas as páginas e reviu o repertório visual Bellas pertinente.
- [ ] Um mapa visual com placeholders foi apresentado e aprovado antes da direção final das imagens.
- [ ] As áreas do mapa foram dimensionadas pelo **texto real** em Gotham e escala próxima do PSD; fotos/bullets/páginas foram planejados conforme o espaço efetivo, sem copiar a diagramação amadora da fonte.
- [ ] A capa reutiliza a composição aprovada, com somente o título alterado; a tela final de agradecimento é idêntica à aprovada. A quantidade de telas intermediárias foi definida pelo conteúdo.
- [ ] O PSD de produção deriva de `referencias/molde_bellas_aprovado_capa_temas_agradecimento.psd`: bases vazias claro/escuro foram duplicadas para as páginas intermediárias, sem conteúdo Optima herdado.

## Conteúdo

- [ ] Todos os títulos, parágrafos, bullets, cards e chamadas têm texto real.
- [ ] Nenhum campo `placeholder` no manifesto final nem rótulo H1/BLOCO/ITEM/BULLET/LINHAS visível.
- [ ] Todo trecho relevante do roteiro está coberto, ou tem uma decisão editorial registrada.
- [ ] Números, termos, nomes, atribuições e ressalvas foram comparados com a fonte.
- [ ] Alegações que exigem revisão estão identificadas sem transformar fonte editorial em comprovação.

## Identidade e fotografia

- [ ] Canvas 1920×1080/16:9; cada página no mesmo PSD.
- [ ] Capa com apenas o título do treinamento como texto de conteúdo; nenhuma foto nova ou chamada de benefícios. Grafismos e foto de marca esmaecida do exemplo aprovado permanecem iguais.
- [ ] Alternância de claro/escuro corresponde ao manifesto.
- [ ] Cabeçalho, quadrados, B de fundo e logos/rodapé corretos e visíveis.
- [ ] Gotham presente, peso/estilo coerentes; nenhum fallback silencioso.
- [ ] Cada H1 visual está em um único objeto de texto editável, mesmo com palavra em Bold/cor diferente.
- [ ] Parágrafos corridos estão brancos; apoio escuro no tema claro usa `#B3718E`.
- [ ] Cards/checklists têm retângulos proporcionais ao texto, padding regular e check/numeral alinhado ao eixo do título. Cada bloco completo está agrupado em uma pasta editável e o conteúdo está centralizado opticamente.
- [ ] Foto ambiental em toda a altura tocando lateral ou tela inteira; ou modelo transparente com alpha verdadeiro, luz compatível e sem borda reta visível no corpo.
- [ ] Enquadramento não corta rosto/produto de modo indevido; anatomia, rótulos e embalagem conferidos.
- [ ] **Após o recorte real no slide**, cerca de 15% da altura no topo e no rodapé funcionam como área segura para cabeçalho/assinatura: nenhuma face, mão, produto ou foco importante compete com as marcas; o fundo mantém contraste.
- [ ] A foto é uma cena contínua até as bordas; as margens livres não foram criadas com barra, retângulo escuro ou emenda horizontal artificial.
- [ ] Color grading preserva cor de pele e produto; fotos têm saturação contida e contrastam com o fundo rosa.
- [ ] Sequência de fotos varia assunto/gesto; pessoa fornecida mantém identidade e sinais naturais da idade; produto mantém a proporção da foto real.
- [ ] Mesmo nas fotos sem modelo fornecida, mulheres têm traços individuais, textura de pele e proporções naturais; não parecem retratos genéricos com filtro de beleza.
- [ ] Mulheres estão bem cuidadas, com styling contemporâneo; produto aparece quando a cena comunica seu uso. Recortes transparentes foram gerados do zero em um prompt, sem halo/mancha/matte e sem corpo cortado nas laterais.

## Prova visual e arquivo

- [ ] Todas as telas foram abertas individualmente em resolução útil, além do contato.
- [ ] Sem overflow/clipping, sobreposição de caixas, títulos encostando no cabeçalho ou corpo invadindo rodapé.
- [ ] Quebras e entrelinhas são naturais, hierarquia e contraste legíveis em apresentação.
- [ ] Respiro predominante nas extremidades do conjunto; blocos relacionados mais próximos, com intervalos internos consistentes e legíveis. Não há distribuição vertical artificial para preencher a tela; referências permanecem próximas do trecho correspondente. Páginas já aceitas só são refeitas conforme o pedido atual.
- [ ] Apenas a pasta corrente fica visível nas exportações; nenhuma página mistura conteúdo de outra.
- [ ] Texto variável é editável; grupos e camadas têm nomes estáveis.
- [ ] PSD reaberto e conferido por script; contagem/nome das pastas registrados.
- [ ] Ajustes manuais preexistentes foram preservados; scripts incrementais e provas identificam as páginas tocadas.
- [ ] Fotos utilizadas, manifesto, scripts e log preservados em caminhos relativos.
- [ ] PNGs de todas as páginas saíram por Save for Web PNG24 com `convertToSRGB=true` e `includeProfile=true`, sem atribuir perfil à duplicata do PSD Optima. Conferidos em tamanho real contra a referência visual aprovada: rosa claro próximo de `#FBA9C3`, malva `#BC718C`. Valores do PSD sem perfil e JPEGs antigos não são referência de cor final.
- [ ] Contagem de pastas, PNGs e páginas do PDF coincide com o estado atual do PSD; não fixar 12 páginas. O PDF foi montado sem reamostrar e cada imagem extraída tem RGB idêntico ao PNG de origem (usar `scripts/montar_pdf_dos_pngs.py`). Uma renderização do PDF também foi inspecionada.

## Relatório de entrega

- [ ] Auditoria iniciada na primeira ação e atualizada durante a execução, incluindo principal e subagentes; seguir `DOCUMENTACAO_DA_EXECUCAO.md`.
- [ ] Prompts iniciais/complementares, parâmetros, comandos e versões dos scripts preservados literalmente, com origem e identificação; resultados, erros/reexecuções e decisões vinculados às ações.
- [ ] Configuração de modelo registrada com fonte verificável, quando disponível; nenhuma versão inferida.
- [ ] Cobertura da auditoria conferida contra os registros disponíveis: distinguir literal do registro/contexto, resumo e lacuna; não afirmar documentação integral se houver omissões. Índice e ponto de corte informados.

Informe quais verificações foram concluídas e quais lacunas permanecem. Separe aprovação de composição da revisão editorial. Use os nomes/caminhos exatos do resultado; não chame o PDF/PSD de placeholders de apresentação final.
