# Botões do painel → agente real (v12)

Legenda de estado: ✅ existe e roda · 🟡 existe, falta ligar/ajustar · 🔴 a construir.
Créditos = o que o botão mostra hoje no protótipo (valores ilustrativos até o estudo de margem).
Repositório de referência: `tutorialpet` (agents/01–32 + workflows em `.github/workflows`).

| Departamento | Botão (como aparece) | Agente/motor | Entrada | Saída | Créd. | Estado |
|---|---|---|---|---|---|---|
| Caçador | Ver no Caçador / Fazer minhas versões → | 28_buscador_ofertas (hoje só Shopee) + 02_trend_hunter + 01_niche_research | nicho, país | `data/ofertas/<data>.json/.md` com nota e 9 pontos | 0 (diário incluso) | 🟡 falta Hotmart + Kindle BR (item 6) |
| Começar | Montar minha oferta → | 19_validador_tema + 01_niche_research | nicho, o que tem, lucro por venda | mapa da oferta com 10 peças | 0 | 🟡 |
| Produto | Produzir · 150 cr / Produzir versões · 150 cr cada | 03_content_writer + 04_quality_editor + 15_visual + 26_guardiao_marca (montador de manual / Produtor de e-book) | referência escolhida, voz/foto do cliente | e-book PDF + capa | 150 | 🟡 estudo de voz e checagem anti-repetição pendentes |
| Produto | Minha voz | ElevenLabs (creditos_eleven.yml, testar_voz.yml) | amostra de voz do cliente | voz clonada | — | 🟡 consentimento explícito do cliente |
| Produto | Apresentador / Criar apresentador | HeyGen + 20_roteirista_duda (padrão Duda) | foto do cliente | avatar | — | 🟡 |
| Oferta | Regerar oferta · 10 cr | 29_marketing_produto + 09_monetization | produto, lucro alvo | preço, parcelas, bump, garantia | 10 | ✅ (prompt.md existe) |
| Oferta | Aplicar · 30 cr | pricing_offer_strategist_agent | cenário escolhido na calculadora | oferta fixada no mapa | 30 | 🟡 |
| Audiência | Gerar semana · 40 cr | 27_lote_roteiros + 20_roteirista_duda + 17_video + Agendador (Zernio/Buffer) | produto, apresentador | 7 reels roteirizados e agendados | 40 | ✅ núcleo / 🟡 painel |
| Audiência | Gerar mimo / Gerar fluxos · 20 cr | fluxo do mimo (ManyChat) | palavra-gatilho, produto | fluxo de DM + isca | 20 | 🔴 ManyChat sem API ligada ao painel |
| Tráfego | Montar campanha · 20 cr | gestor_de_anuncio (plano B) / ZX LAB meta-campaign-launcher | oferta, orçamento/dia | campanha em rascunho, nunca ativa | 20 | 🟡 ZX LAB não ativado |
| Tráfego | Aprovar e ativar | 22_guardiao_gasto (checa regra de gasto) | campanha em rascunho | ativação só com ok humano | 0 | ✅ regra existe |
| VSL | Gerar roteiro · 20 cr / 60 s para reel | Criativo de Venda/VSL + 20_roteirista_duda | oferta, 14 blocos (funis-prontos.md) | roteiro curto 3 min e 60 s | 20 | 🟡 VSL longa ainda sem ponta a ponta |
| Página | Gerar página · 30 cr / Regerar landing | 30_fabrica_landing + 31_aprimorador_landing | oferta, imagens | landing com Pixel/CAPI + Clarity | 30 | ✅ núcleo |
| Página | Cadastrar nas plataformas | Cadastrador Kiwify/Hotmart (automação de navegador) | dados do produto | produto cadastrado | por plataforma | 🔴 para 2FA/senha: sempre o cliente |
| Pós-venda | Gerar fluxos · 20 cr | Brevo + ManyChat | produto | bump, carrinho, entrega, upsell 7 dias | 20 | 🔴 |
| Suporte | (bot) | livro-de-gaps.md + suporte.md + Jev | pergunta + estado da conta | resposta ou escalonamento | 0 | 🔴 bot em si |
| Medição | Ver prévia / painel | 08_analytics + controle_prova_real | Pixel/Clarity/checkout | gargalo + recomendação | 0 | 🟡 ligar fontes |
| Cadastros | Afiliar-se (1 clique) | automação de navegador + Agente de Segurança | dados guardados uma vez | afiliação pedida | 0 | 🔴 para em 2FA/cartão |
| Créditos | Recarregar / Ativar com desconto | carteira + fornecedores (fase 2) | valor | saldo / parceiro com desconto | — | 🔴 fase 2 |

## Observações
- Hoje o agente 28 busca só na Shopee (API de afiliados, exige SHOPEE_APP_ID/SECRET). O Caçador do painel
  precisa de fontes novas; ver `cacador-diario.md` e o workflow proposto em `workflows/cacador-diario.yml`.
- Nenhum botão que gasta dinheiro executa sem prévia + ok. Cadastros e pagamentos param no humano.
- Créditos são placeholders até o estudo de margem (2–4× sobre o custo de API).
