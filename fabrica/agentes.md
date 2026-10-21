# Mapa botão → agente existente

| Aba | Botão | Agente/pipeline já existente | Onde | Fornecedor + afiliado (ver fornecedores.md) |
|---|---|---|---|---|
| Estratégia | Escolher produto da biblioteca | biblioteca.json (esta pasta) | fabrica-saas | — |
| Estratégia | Validar ideia / briefing | validador_oportunidade.yaml, cacador_de_tendencias.yaml | agencia/squads/viral-1 | Gemini/OpenRouter (Jev) — revenda de créditos: a conferir nos termos |
| Estratégia | Calculadora de cenários | pricing_offer_strategist_agent (+ calculadora.py local) | tutorial-pet/agentes-marketing | — |
| Oferta | Gerar e-book/manual | montador_de_manual.yaml | agencia/squads/viral-1 | Gemini/Claude API; ElevenLabs só se virar audiolivro (afiliado até 22%, 12 meses) |
| Oferta | Gerar app HTML | gerador de app HTML (Projeto Fábrica de Oferta — a construir) | tutorialpet (nuvem) | Vercel/Cloudflare Pages para publicar (afiliado não verificado) |
| Oferta | Gerar landing (blocos próprios, Pixel/CAPI, Clarity) | landing_page_architect_agent | tutorial-pet/agentes-marketing | Hostinger (a partir de 40%, 1ª venda, cookie 30 dias; sem PPC) |
| Oferta | Preço, parcelas, bump, garantia | pricing_offer_strategist_agent | tutorial-pet/agentes-marketing | Kiwify/Hotmart (ver regras-plataformas.md) |
| Marketing | Criativos estáticos + copy de anúncio | copywriter, visual_designer, meta-creative-brief | viral-1 + trafego-pago (ZX LAB) | Gemini imagem/Flux/Ideogram (afiliado não verificado) |
| Marketing | Montar campanha Meta | meta-campaign-launcher (ZX LAB, não ativado) / gestor_de_anuncio.yaml | trafego-pago / viral-1 | Meta Ads via Windsor.ai (afiliado não verificado) |
| Marketing | Publicar página no domínio | deploy Vercel (padrão atual) | agencia | Hostinger / Registro.br (.br só no Registro.br) |
| Marketing | Painel de resultados | analytics_bi_agent | tutorial-pet/agentes-marketing | Windsor.ai, Clarity (grátis) |

Lacunas reais (só estas precisam de construção): gerador de app HTML; ativação
do ZX LAB (ou gestor_de_anuncio como plano B); cadastro automático na Kiwify.

## Fornecedores por categoria de botão ainda não ligados
- Áudio/voz (VSL, apresentador): ElevenLabs (até 22%, 12 meses) e HeyGen (35%, 3 meses; exige 5 mil seguidores e vídeo original).
- DM/WhatsApp (mimo, pós-venda): ManyChat (30–50%, 12 meses). E-mail (carrinho, entrega): Brevo (CPA fixo, cookie 90 dias; sem PPC).
- Regra geral: nenhum desses links pode ser usado em anúncio pago nosso ou do cliente; só dentro do app e em conteúdo orgânico.
