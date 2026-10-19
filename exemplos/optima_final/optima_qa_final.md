# APN Optima Bellas — estado aprovado

- 13 páginas de 1920×1080: 12 de conteúdo e uma de agradecimento adicionada pelo usuário.
- `optima_apn_bellas_final.psd`: cópia do estado corrente com 13 pastas numeradas; texto e elementos permanecem editáveis. O arquivo de trabalho do usuário não foi alterado nesta revisão.
- `pngs_aprovados/pagina_01.png` … `pagina_13.png`: cópias dos PNGs salvos pelo usuário; autoridade para composição e cor.
- `optima_apn_bellas_final.pdf`: montado dos 13 PNGs sem reamostragem. Imagens extraídas das páginas comparadas pixel a pixel com os respectivos PNGs; igualdade de RGB confirmada.
- `optima_visao_geral.jpg`: contato reconstruído das 13 provas aprovadas.
- A capa exibe somente o título do treinamento como conteúdo, com o grafismo/imagem de marca muito esmaecidos na base. A página 4 exibe a modelo recortada diretamente sobre rosa. As páginas 8, 9, 10 e 12 mostram, respectivamente, cartões de soja com foto, mulher com produto em interior neutro, modelo recortada com cartão de duração e dicas com aplicação espontânea do Optima.
- A direção aprovada usa Gotham, H1 em uma camada de texto com estilos internos, corpo branco, apoio `#B3718E` no claro, cartões agrupados e alinhados, frasco compacto conforme referência e margem de segurança nas fotos.
- O texto de saúde/comércio do roteiro original foi preservado conforme o escopo editorial anterior; não houve revisão factual nesta etapa.

## Cor e exportação

O PSD Optima está em RGB/8 sem perfil atribuído. A rota de atribuir sRGB à duplicata e salvar JPEG/PNG por `saveAs` gerou aparência opaca: malva `#A9708A`. Os JPEGs em `optima_provas/` e os scripts `scripts_incrementais/export_all_srgb.jsx` / `build_srgb_pdf.py` são **históricos e rejeitados como referência visual**.

Em teste controlado, `ExportOptionsSaveForWeb` PNG24 com `convertToSRGB=true` e `includeProfile=true`, executado numa duplicata sem atribuir perfil, reproduziu os 13 PNGs aprovados **pixel a pixel**. A cor dominante aprovada é rosa `#FBA9C3` e malva `#BC718C`. O método reproduzível está em `../../scripts/exportar_pngs_bellas.jsx`; `../../scripts/montar_pdf_dos_pngs.py` também confere os pixels incorporados no PDF. Antes de reutilizar em outro PSD/perfil, valide uma página de teste.

## Limite da conferência

Esta revisão certifica a igualdade raster entre PNGs aprovados e PDF, a contagem de 13 páginas e a documentação da receita de exportação. A inspeção visual das páginas segue os PNGs aceitos pelo usuário; ela não substitui conferência editorial ou factual do texto.
