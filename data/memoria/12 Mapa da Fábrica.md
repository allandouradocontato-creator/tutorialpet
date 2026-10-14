# Mapa da Fábrica (ordem do Allan, 14/10/2026)
Modelo: um NICHO (hoje pet) com guarda-chuva Tutorial Pet. A fábrica = produtos + sistema de venda + artigos + posts/vídeos + audiência. Meta: tudo pronto em ~3 dias por produto/nicho, medido pelo Otimizador (config/auditor_processo.yaml, tempo_de_ciclo).

| Peça | Estado em 14/10 | Falta |
|---|---|---|
| Marca/nicho Tutorial Pet | pronta (blog, FB, IG, TikTok) | replicar para outro nicho: parametrizar config por nicho |
| Fábrica de produtos | 1 produto (Sozinho em Casa R$9,90, e-book 53 pág, app, landing, Kiwify) | agente que faça demanda -> e-book/app -> landing -> Kiwify em horas; hoje é manual |
| Afiliados Shopee | 1 link (câmera R$79,99) na landing | catálogo de produtos por tema, link nos artigos, sub_id por artigo, medição de cliques; Allan: pagamento/fiscal Shopee |
| Fábrica de artigos | 38 no ar, agentes 01-06 e 24, Gemini grátis | fila de temas com reserva de 5+ dias; links de afiliado dentro dos artigos |
| Blog + AdSense | páginas, ads.txt, sitemap ok; aguardando o Google | conferir banner de cookies e anúncio nos artigos |
| Fábrica de vídeos/posts | roteiro, vídeo, Duda, Agendador (Zernio+Buffer) | estoque 3-4 dias, meta 5+ |
| Buscador de cortes virais | NÃO EXISTE (só config de ganchos e áudios em alta, e o Especialista TikTok semanal) | agente curador de referências virais do nicho (padrão de gancho, duração, formato), recriar em versão original |
| Estrategista de redes | rotina recriada com Zernio+Buffer, 1ª rodada v2 sexta | ligar as recomendações ao Agendador; engajamento (comentários, isca digital) sem decisão |
| Sistema de venda | landing, Kiwify, anúncios Meta (64 campanhas, a limpar) | Auditor de Anúncios, order bump, conta de anúncios com verificação pendente |
| Medição | Otimizador mede tempo de ciclo | série em data/auditoria/ciclo.csv ainda vazia |

## Fluxo completo: da dor do tutor à venda (14/10/2026, ordem do Allan)
1. AGENTE DE MARKETING DE PRODUTO (NOVO, falta criar): escolhe a dor/assunto pensando em venda. Para cada assunto decide: produto próprio (e-book + app) ou produto de afiliado Shopee. Pontua por dor, intenção de compra, comissão e preço. Acompanha o resultado em dinheiro e realimenta a escolha.
2. BLOG escolhe assuntos já ligados a um produto (tabela tema -> produto -> link -> CTA). Ex.: xixi no lugar certo -> tapete higiênico/educador; conforto e lugar seguro para dormir -> caminha.
3. FÁBRICA DE E-BOOK/MANUAL (parcial): cada manual vira
4. FÁBRICA DE APLICATIVO (NOVA, falta criar: hoje só o app do Sozinho em Casa, feito à mão), e
5. FÁBRICA DE LANDING (NOVA, falta criar: hoje feita à mão), com
6. APRIMORADOR DE LANDING (NOVO: lê cliques/vendas e propõe mudança de texto, oferta e ordem; teste A/B grátis primeiro).
7. Checkout (Kiwify, cadastro hoje manual) e afiliado (Shopee: link com sub_id por artigo).
8. Posts/vídeos e Buscador de cortes virais puxam audiência para o artigo; Estrategista otimiza.
9. Auditor mede venda por etapa; Otimizador mede tempo de ciclo (meta ~3 dias por produto).
Ordem de construção proposta: (a) catálogo tema->produto Shopee/e-book e links nos artigos; (b) Agente de Marketing de Produto; (c) Fábrica de landing + aprimorador; (d) Fábrica de app; (e) Buscador de cortes virais.

## Buscador de Ofertas (agente 28, criado 14/10/2026)
Cloud: páginas da Shopee exigem JavaScript (WebFetch não lê). Caminho que funciona em nuvem: API aberta de Afiliados da Shopee (productOfferV2) rodando no GitHub Actions (buscar_ofertas.yml, segundas 06:17 Fortaleza), com segredos SHOPEE_APP_ID e SHOPEE_SECRET (só o Allan cria/cadastra). Sem a chave, o navegador do computador do Allan (portal de afiliados) cobre, só com o computador ligado. Catálogo: config/catalogo_tema_produto.yaml.

## Agente de Marketing de Produto (agente 29, criado 14/10/2026)
agents/29_marketing_produto (prompt.md + agent.py, sem LLM pago). Liga cada tema da fila a produto próprio ou afiliado Shopee, pontua (dor, intenção, comissão, preço, oferta) e grava data/marketing/plano_semana.md; acrescenta temas novos ao catálogo. Falta: ler vendas (Kiwify/Shopee sub_id) para realimentar a pontuação e ligar ao fluxo diário/workflow.

## Série "Pet Celebridade da Semana" (ideia do Allan, 14/10/2026)
- Um artigo por semana sobre o pet de um artista brasileiro: raça, convivência, o que o pet mudou na vida dele.
- Especificação em `config/serie_pet_celebridade.yaml` (regras: só fatos públicos com fonte, sem foto do artista, sem inventar fala).
- Primeiro passo: artigo-piloto com 6 a 8 artistas; depois uma edição por semana, ligada ao catálogo tema→produto.
