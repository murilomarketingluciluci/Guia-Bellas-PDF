# Direção de fotografia para APNs Bellas

As regras atuais estão em `DECISOES_APN_BELLAS.md`. As fotos finais Optima e seu encaixe podem ser vistos em `exemplos/optima_final/optima_assets/` e `exemplos/optima_final/optima_provas/`.

## Planejar antes de gerar

Antes de escrever prompts individuais, faça uma visão única da sequência de imagens conforme `DIRECAO_DE_ARTE.md`. Para cada foto, registre: ideia que ela torna visível, ação, quantidade de pessoas, cenário, escala de câmera, luz, paleta e páginas vizinhas. Em Crescimento/Luciane, estudo, mentoria e equipe tinham ações distintas, mas três interiores profissionais semelhantes limitaram a variedade. Não resolva isso apenas mudando idade, cabelo ou roupa: mude o gesto, o ambiente ou o enquadramento quando a narrativa permitir. Se a imagem não acrescentar informação, use um recurso tipográfico ou espacial intencional.

1. Identifique a ideia/benefício da tela e o papel da foto: produto, pessoa, ação, ingrediente, contexto ou respiro visual. Planeje **variação ao longo da apresentação**; não repita a mesma pose de axila erguida.
2. Defina o lado e a largura da faixa, full canvas ou modelo recortada. **No encaixe final do slide**, planeje pelo menos **15% da altura acima e 15% abaixo** como área segura para cabeçalho e rodapé: sem rosto, mãos, produto ou foco importante sob as marcas. Roupa, piso e ambiente podem seguir até a borda quando o texto permanece legível. Na foto ambiental, a margem deve ser cenário fotográfico contínuo, sem barra aplicada por cima. No recorte transparente, evite bordas retas do corpo dentro do canvas e deixe a figura sair naturalmente pela borda inferior.
3. Defina contraste com a arte rosa. Fotos menos saturadas, textura natural e luz equilibrada; ambientes **creme, cinza/ardósia ou espresso**. Evite tanto fundo rosa com produto rosa quanto o filtro marrom escuro aplicado a tudo.
4. Defina onde ficam cabeçalho, logotipo e sobreposições. Reserve área legível no fundo da foto. Uma barra pode atravessar a fronteira entre cor e foto se não ocultar o assunto. Faça uma prova com o recorte exato de 1920×1080 antes de aceitar a imagem.

## Produto: proporção primeiro

Use a foto real fornecida pelo usuário como referência de formato. No Optima, a primeira geração alongou demais a tampa; a correção exigiu frasco mais achatado e relação tampa/corpo fiel. A foto real é autoridade para largura, altura, curvatura, plástico acetinado e luz. Gerar **uma cena integral nova**, com a embalagem nesse formato; não colar um recorte de produto sobre um cenário incompatível nem esticar o frasco. Comparar embalagem, ícones, marca e rótulo com a foto real antes de declarar fidelidade. Se os detalhes impressos saírem errados, tratar como problema de produção, não como texto aprovado.

Prompts do caso Optima, adaptáveis:

> Fotografia editorial vertical de produto para faixa de apresentação Bellas. Recriar uma cena integral usando a foto de referência do desodorante para manter exatamente a proporção física: frasco branco compacto, tampa relativamente baixa e larga, transição e base iguais à referência, plástico acetinado, gotículas e luz difusa semelhantes. Ambiente quase creme, pedra clara, sombras suaves, pouca saturação. Frasco inteiro com margem superior, inferior e lateral para recorte. Sem colagem, sem distorção, sem frasco alongado.

> Mesma geometria real do frasco de referência, em uma nova fotografia integral sobre superfície marrom espresso e fundo escuro quente. Iluminação suave lateral, textura realista, saturação contida, frasco inteiro com margem de segurança e contraste com o tema rosa Bellas. Sem colagem e sem tampa alta.

## Pessoas e benefícios

Quando houver foto de uma pessoa indicada pelo usuário, usar a imagem como referência de identidade: preservar traços do rosto, expressão e sinais naturais da idade. Criar uma cena coerente e ampliar o enquadramento suficiente para que testa, cabelo, mãos e corpo não sejam cortados ao aplicar a faixa no slide. A página 5 de Optima mostra a modelo em ambiente neutro claro e foi refeita com margens mais amplas.

Para uma checklist de hidratação, o Optima usou outra linguagem: mulher adulta com copo de água, aloe discreta, cenário espresso. A foto comunica o benefício e oferece um fundo escuro contrastante à faixa rosa. Em novas APNs, faça um brainstorm curto de 2–3 conceitos visuais por tema antes de gerar; escolha a cena que acrescenta informação e melhora a variedade da sequência.

**Pessoas sem referência nominal também precisam parecer reais.** Peça traços individuais, textura de pele, poros, linhas finas, leve assimetria, cabelo natural e expressão espontânea. Beleza e roupa bem cuidada são desejadas, sem filtro plástico nem figurino rústico/antiquado. Em tela de uso do desodorante, mostre o produto no gesto. A mulher com toalha sem frasco da versão anterior da página 10 não comunicava o tema; o usuário pediu uma modelo de referência aplicando Optima em recorte transparente.

Na página 9, a foto ambiental final mostra uma mulher bem arrumada, com traços e sinais naturais, segurando o Optima real num interior neutro de luz equilibrada; o frasco aparece e conserva o formato compacto. O teste separado `exemplos/optima_final/optima_teste_pagina_09_modelo_recortada.jpg` apresenta a alternativa transparente sobre rosa. O primeiro teste tinha a figura terminando numa linha horizontal acima do rodapé; ela foi reenquadrada para continuar fora do canvas. **Teste não substitui automaticamente a versão final.**

## Recorte transparente e cenário real

Quando o layout pedir uma modelo sem fundo, gere mulher, roupa, mãos e produto juntos **num único prompt original** com alpha verdadeiro. A referência de pessoa orienta identidade/pose; a foto do produto orienta forma física. Descreva luz que combine com o fundo do slide e peça folga em todos os lados. Examine o PNG isolado e a prova aplicada: manchas na transparência, halos, braço cortado na lateral, faixa reta na cintura ou embalagem incorreta exigem nova geração original, não remendos. Se a cena precisar parecer um local real, é possível combinar a modelo transparente com uma fotografia separada de ambiente cotidiano com direção de luz coerente, mantendo ambas as camadas editáveis no PSD; a montagem só é aceita quando a prova não denuncia colagem.

Na página 8 do Optima, a foto editorial de vagens e óleo de soja na direita dá contexto aos três benefícios, com bancada naturalmente escura sob LUCI|LUCI. Cada benefício foi agrupado em uma pasta própria e alinhado ao numeral. Na **página 4 aprovada**, a modelo com coque alto, joias e top sem alças aplica o Optima como recorte com alpha verdadeiro diretamente sobre o campo rosa; o banheiro testado antes foi retirado pelo usuário. A prova confirma integração de luz, ausência de corte lateral reto e leitura de BELLAS. A página 10 final usa outra mulher adulta recortada segurando o Optima sobre o malva do slide; o cartão informativo fica livre.

Na revisão seguinte da página 12, o usuário escolheu a pose espontânea de `referencias/optima_dicas_pose_referencia.png` e pediu a mesma atriz aplicando o **frasco Optima real**, sem a tatuagem visível na referência. A foto final está em `exemplos/optima_final/optima_assets/foto_12_ritual_optima_sem_tatuagem.png`: luz de janela mais controlada, cenário espresso, corpo centralizado e balcão escuro no quinto inferior para deixar a assinatura livre. Essa atualização substitui a antiga cena com copo de água na página 12; ela permanece no pacote apenas como histórico.

A foto de pele da página 4 foi reenquadrada numa fase anterior pelo mesmo critério: `exemplos/optima_final/optima_assets/foto_04_espresso_margens_15.png`. A versão anterior continua no pacote como histórico, sem seleção no registro final. A composição aprovada está em `exemplos/optima_final/pngs_aprovados/pagina_04.png` e usa `foto_04_modelo_joias_optima_recorte_final.png` sobre o rosa; `foto_04_ambiente_real_neutro.png` é somente uma tentativa anterior.

## Conferência após gerar

- Conferir anatomia, mãos, axila, expressão, idade e semelhança quando houver pessoa de referência.
- Conferir forma real do produto, tampa/corpo, rótulo e logotipos.
- Conferir saturação e contraste junto à página anterior e à seguinte.
- Conferir o recorte efetivo em 1920×1080: foto toca topo, base e uma lateral; há margem segura; marcas e texto continuam legíveis.
- Medir a área segura **depois do `cover`**: topo e rodapé têm cada um cerca de 15% da altura da faixa sem rosto, mãos, produto ou outro foco importante sob cabeçalho/assinatura; roupa e ambiente podem continuar naturalmente. Inspecionar também fotos antigas antes de reutilizá-las sob esta regra.
- Ampliar a prova na junção da área livre: nenhuma linha horizontal, faixa uniforme ou mudança brusca de textura pode denunciar margem pintada sobre a foto.
- Guardar foto selecionada, referência usada, prompt/direção e prova aplicada. Fotografias não substituem a inspeção da tela completa.
