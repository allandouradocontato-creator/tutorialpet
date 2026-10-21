# Fábrica de Ofertas — departamentos (o que o cliente recebe, mastigado)

Base: inventário real da fábrica Tutorial Pet em 21/10/2026 — 32 agentes no repositório
`tutorialpet/agents`, 22 rotinas na nuvem, 17 agentes em `tutorial-pet/agentes-marketing`,
squad `viral-1`, pack ZX LAB (tráfego). Cada departamento = um botão no painel; cada botão
= agentes que já existem (coluna "Motor"). Lacuna = o que falta construir.

| # | Departamento | O que o cliente recebe (em 1 clique) | Motor (já existe) | Lacuna |
|---|---|---|---|---|
| 1 | **Caçador de Ofertas** | prateleira diária do que vende, por nicho, BR + exterior, com os 9 pontos mapeados; "quero esse" | Pesquisador de Mercado (seg), Pesquisador de Formato (ter/sex), 28_buscador_ofertas, 02_trend_hunter, 01_niche_research, Caçador de atalhos (PLR/white label) | rodar diário; capas geradas; nota de sinal |
| 2 | **Produto** | e-book próprio (voz + foto do cliente), app em HTML/Streamlit, planilha/checklist; adaptação de referência estrangeira | 03_content_writer, 04_quality_editor, montador_de_manual, Produtor de e-book, Construtor de app, 15_visual (capas), 26_guardiao_marca, 19_validador_tema | estudo de voz; checagem anti-repetição; Fábrica de App repetível |
| 3 | **Oferta** | preço-âncora/final, parcelas, bump, upsell, garantia, calculadora de cenários, nome do método | pricing_offer_strategist_agent, 09_monetization, 29_marketing_produto, validador_oportunidade | — |
| 4 | **Criador de Audiência** (orgânico) | calendário de posts em vídeo para FB/IG/TikTok, roteiros na voz do apresentador, memes, mimo/isca por comentário com fluxo de DM, atendimento de comentários, horário de pico | Criador de Audiência (diário), Estrategista de Redes v2, Especialista TikTok v2, Humorista, 32_meme_pet, 20_roteirista_duda, 27_lote_roteiros, 17_video, 21_publicador_video, Agendador de Posts (Zernio/Buffer), Vigia e Guerrilha de Comunidade, Atendente de Comentários, fluxo do mimo (ManyChat) | ligar mimo/ManyChat ao painel; apresentador(a) por cliente (igual à Duda) |
| 5 | **Blog e SEO** | artigos otimizados, links internos, AdSense/E-E-A-T, publicação automática | 03_content_writer, 05_seo_onpage, 24_curador_blog, 07_publisher, Conferente de Estoque v2, Agente de SEO e Tráfego, reforço do blog | opcional por cliente (nem todo nicho precisa) |
| 6 | **Tráfego pago** | criativos estáticos/vídeo, copy, campanha Meta montada, checagem antes de gastar, otimização por regra, auditoria de resultado | gestor_de_anuncio, meta-creative-brief / campaign-launcher / performance-analyzer / budget-optimizer (ZX LAB), 22_guardiao_gasto, Auditor de Anúncios, Criativo de Venda | ativar ZX LAB ou ligar gestor_de_anuncio; CAPI |
| 7 | **VSL** | roteiro (dor → história → método → prova → oferta → garantia), narração na voz do cliente (ElevenLabs) ou apresentador virtual (HeyGen), versão 60 s | Criativo de Venda/VSL (ter), 20_roteirista, 17_video, narracao_app.yml, HeyGen conectado | VSL longa ainda não gerada de ponta a ponta |
| 8 | **Página e checkout** | landing com blocos próprios + Pixel/CAPI + Clarity, publicada em subdomínio grátis ou domínio do cliente (parceiro com desconto); **Cadastrador de plataformas**: produto cadastrado na Kiwify, Hotmart, Eduzz e Monetizze (capa, categoria, área de membros, preço) — 1 plataforma inclusa, extras pagas; a padrão é a que dá melhor comissão/co-produção para a Fábrica; banner de checkout | landing_page_architect_agent, 30_fabrica_landing, 31_aprimorador_landing, Construtor de landing, Clarity já usado | Cadastrador Kiwify automático |
| 9 | **Pós-venda** | bump, carrinho abandonado (WhatsApp + e-mail), entrega + boas-vindas, upsell 7 dias, segmentação | fluxo do mimo (ManyChat), Brevo conectado, Editor de Afiliados | fluxos ainda não gerados por produto |
| 10 | **Suporte** | bot treinado no Livro de Gaps, diagnóstico com estado da conta, humano no nível 3 | 25_auditor_processo, 18_saude_fabrica (checagens), livro-de-gaps.md, suporte.md | bot em si |
| 11 | **Medição** | painel por etapa (gasto, cliques, checkout, vendas), gargalo apontado, recomendação pronta para aplicar, testes de 3 dias | 08_analytics, analytics_bi_agent, 13_supervisor, controle_prova_real, medicao.md | ligar Pixel/Clarity/Kiwify ao painel |
| 12 | **Conformidade** (transversal) | bloqueio de promessa de renda/cura, regras Meta/TikTok/Google/AdSense atualizadas, LGPD/privacidade, checklist antes de publicar e de anunciar | 06_platform_compliance, 10_policy_guardian, compêndio biblioteca/regras_plataformas, Agente de Segurança | atualização trimestral do compêndio |
| 13 | **Decisões e auditoria** (bastidor) | painel de decisões 1–3 por vez, execução automática do que não precisa do cliente, auditoria de processo e custo | Triagem de Decisões, Executor de Decisões (Jev), Otimizador/Auditor, Revisão Estratégica de Renda, 23_acelerador_processos, entrega_direta | — |
| — | **Biblioteca de design** | capas, páginas, criativos, apps e VSL com padrão que converte; aplicar com a marca do cliente | 15_visual, visual_designer, 26_guardiao_marca, templates/ | curadoria inicial |
| 14 | **Cadastros e contas** | a plataforma preenche todo cadastro (Google, Meta, Kiwify, Hotmart, Eduzz, Monetizze, domínio, WhatsApp, e-mail) com os dados principais guardados uma vez; o cliente só entra para senha/2FA; dados bancários e documentos ficam só no dispositivo/nuvem dele; "Afiliar-se" em 1 clique (produtos da Fábrica, Hotmart, Kiwify) | Agente de Segurança, regra "conferir conta existente antes de OAuth", Cadastrador Kiwify (a construir), automação de navegador | cadastrador automático por plataforma |
| — | **Cofre** | o que fica na plataforma (gerações, foto, voz, CNPJ) × só no PC do cliente (chaves, senhas, cartão) | regra já praticada na holding | — |
| — | **Créditos e fornecedores** | carteira única, recarga automática, parceiros com desconto embutidos no passo certo | — | tudo (fase 2) |
| — | **Aprender** | módulos de otimização pós-primeira-venda, feitos do Livro de Gaps | Auditor compila a apostila | — |

## Linha de produção (ordem que o cliente vê)
Caçador → Produto → Oferta → Audiência (orgânico, começa antes do pago) → Tráfego pago → VSL → Página e checkout → Pós-venda → Suporte → Medição.
Conformidade e Decisões rodam por baixo de todas.

## Mastigado = três regras de produto
1. Cada departamento tem **um botão principal** e uma prévia; o resto é avançado, escondido.
2. Nada é publicado ou gasto sem prévia + checagem automática + (quando é dinheiro) o ok do cliente.
3. O painel diz sempre **qual é o próximo clique** (mapa da oferta) — o cliente nunca precisa saber a ordem.

## Uso interno imediato (Sozinho em Casa)
O mesmo painel, com os nossos agentes ligados, é a operação do Sozinho em Casa: Caçador já
roda; Produto pronto; Oferta definida; Audiência rodando (mimo em construção); Tráfego pausado
(regerar landing → testar 3 dias); VSL a gerar; Pós-venda a gerar; Medição ligada.
