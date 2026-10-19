# Crescimento — versão Photopea V2

Apresentação com 12 telas em 1920×1080, refeita a partir das nove artes originais de Luciane, com novas composições do catálogo Bellas e quatro cenas fotográficas novas.

- [PDF](Crescimento_Photopea_V2.pdf)
- [PSD com camadas](Crescimento_Photopea_V2.psd)
- [Visão geral](visao_geral.jpg)
- [PNGs finais](pngs/)
- [Auditoria e decisões](../auditoria/DECISOES_FINAIS.md)
- [QA final](../QA_FINAL.md)
- [Relatório editorial](../leitura/QA_EDITORIAL_V2.md)
- [Relatório visual](../leitura/QA_VISUAL_V2.md)
- [Revisão visual final das 12 telas](../leitura/QA_VISUAL_V2_SUPLEMENTO_FINAL.md)
- [Relatório técnico](../QA_TECNICO_V2.md)

O PSD contém uma pasta numerada por página, textos novos em Gotham nativo e unidades repetidas em pastas próprias. Para visualizar uma página no editor, deixe visível somente a pasta correspondente. As fontes usadas estão em assets/fonts/ do pacote de trabalho; são necessárias para editar e renderizar o texto em outro ambiente.

A montagem e as exportações foram executadas pela API do Photopea. O PSD salvo foi reaberto no Photopea e as 12 renderizações foram comparadas pixel a pixel. O PDF incorpora os PNGs finais sem reamostragem e preserva seus RGB; é uma apresentação raster, sem texto selecionável.

O molde Photoshop completo não abriu neste ensaio. A solução usou camadas/inputs originais preparados separadamente e manteve os arquivos de origem. Três Smart Objects fixos ficaram como camadas de pixels com máscaras originais nas cópias técnicas; seus payloads originais estão preservados no pacote de trabalho. Não foi comprovado um round-trip no aplicativo Adobe Photoshop.

A capa e o agradecimento conservam a composição da referência, mas o render Photopea não é pixel idêntico ao Photoshop histórico. O teste estrito de igualdade RGB permanece reprovado nesses dois pontos; as diferenças e métricas constam da auditoria. Não se declara equivalência total entre os dois editores.

A auditoria distingue prompts literais, registros recuperados depois, resumos e lacunas de mensagens cifradas. Não contém raciocínio privado, credenciais nem mensagens protegidas. O índice histórico SESSAO.md possui seu próprio corte intermediário; QA_FINAL.md e hashes_entrega.json identificam a versão entregue.
