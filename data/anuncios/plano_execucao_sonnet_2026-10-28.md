# Plano de execução (Sonnet) — 28/10/2026 — Sozinho em Casa: campanha VSL v12 + ajustes da landing
Estratégia já decidida (Fable, aprovada pelo Allan): verba R$ 30/dia × 3 dias; escrita do Windsor LIGADA (15:30). Não reabrir decisões; executar e reportar.

## A. Criar a campanha PAUSADA (Windsor, conector facebook, account 1213984913380523)
Ficha completa: data/anuncios/campanha_vsl_v12_sp.md. Ordem:
1. create_campaign {name:"Sozinho em Casa - VSL v12 - SP apartamento - teste 3 dias", objective:"OUTCOME_SALES", special_ad_categories:[], status:"paused", is_adset_budget_sharing_enabled:false}
2. create_ad_video {name:"VSL_A_v12_Instagram", video_url:"https://raw.githubusercontent.com/allandouradocontato-creator/tutorialpet/media/anuncios/VSL_A_Instagram_v12_tarja_produto_genero_neutro.mp4"} → video_id
3. create_adset {campaign_id, name:"SP 25-55 caes - Reels+Feed", optimization_goal:"OFFSITE_CONVERSIONS", billing_event:"IMPRESSIONS", daily_budget:3000, status:"paused", start_time:<hoje 20:00 -0300>, end_time:<+3 dias 23:59 -0300>, promoted_object:{pixel_id:"2135885120651427", custom_event_type:"INITIATE_CHECKOUT"}, destination_type:"WEBSITE", targeting:{geo_locations:{regions:[{key:"3864"}]}, age_min:25, age_max:55, targeting_automation:{advantage_audience:1}, flexible_spec:[{interests:[<ids de "Cães", "Adestramento de cães", "Petz", "Cobasi", "Petlove" — buscar via Windsor get_options ou usar os nomes que a API aceitar>]}], publisher_platforms:["facebook","instagram"], facebook_positions:["feed","facebook_reels"], instagram_positions:["stream","reels"]}}
   - Região 3864 = estado de São Paulo (confirmar pelo nome na resposta; se a API devolver outro nome, corrigir).
   - Se o Meta exigir BRAZIL_REGULATION/identidade verificada ("Advertiser is missing"), registrar o erro exato em data/anuncios/campanha_vsl_v12_sp.md e parar: isso é pendência do Allan no Gerenciador (Configurações do negócio → Identidades verificadas).
4. create_ad ×2 (page_id "1251330151406637", video_id, image_url da capa https://raw.githubusercontent.com/allandouradocontato-creator/tutorialpet/media/anuncios/VSL_A_v12_thumb_duda.jpg, call_to_action_type "SHOP_NOW", link "https://sozinho.tutorialpet.com.br/?utm_source=facebook&utm_medium=paid&utm_campaign=sozinho_vsl_v12_sp&utm_content=ad_a" (ad_b no segundo), status paused). Textos A e B: ver ficha.
5. Conferir com get_data que campanha/conjunto/anúncios existem PAUSADOS. Não ativar. Reportar ids.
6. Pendências do Allan antes de ativar (só ele faz): marcar "conteúdo gerado por IA" no anúncio no Gerenciador; conferir método de pagamento/saldo da conta.

## B. Landing (repo allandouradocontato-creator/sozinho-em-casa-app, pasta landing/, publica em sozinho.tutorialpet.com.br ao dar push na main)
Edições em landing/index.html (manter o visual; só copy e ordem):
1. Hero (H1 + sub + badge): H1 "Seu cachorro chora, late e destrói quando você sai?" · sub "Sozinho em Casa: plano de 14 dias de atividades práticas, com aplicativo que ajusta os exercícios ao porte, à raça e ao temperamento dele. Manual + app, R$ 27, pagamento único." · badge "Acesso imediato · Garantia de 14 dias (o tempo do plano inteiro)".
2. Vídeo do topo: trocar video-boas-vindas.mp4 pela VSL v12 (landing/vsl-v12.mp4 = cópia de VSL_A_Instagram_v12_tarja_produto_genero_neutro.mp4, ~44 MB; se o Vercel reclamar de tamanho, reencodar a CRF 26 ≈ 15 MB) com poster = quadro da Duda; título da seção "Veja em 1 minuto como funciona" (não "Parabéns por estar aqui"); manter controls + playsinline, preload="metadata".
3. Bloco "O que você recebe": ordem Aplicativo → Manual prático → Base teórica → Garantia. No card do app: "Diagnóstico, plano de 14 níveis ajustado ao porte/raça/temperamento, registro diário, diploma" + 3 telas do app (usar frames da gravação: /home/claude/out/app_rec/app_gravacao_onboarding_guia_telas.webm em 24 s, 41 s e 46 s → PNG 600 px de largura, salvar em landing/fotos/app-tela-1..3.png).
4. FAQ "Como recebo?": "Logo após o pagamento você recebe por e-mail o acesso ao app e o manual em PDF (ler no celular ou imprimir as fichas)."
5. Autoridade/prova: incluir uma frase com fonte sobre ansiedade de separação (pesquisar 1 fonte científica ou de entidade, citar com link; sem promessa de cura, sem "seu cachorro tem") logo abaixo do hero; e, SE o Allan autorizar, o selo "Conteúdo revisado pela Dra. Natasha Braga, CRMV-CE 6174" (perguntar antes de publicar o nome dela).
6. Remover o link de afiliado da Shopee (câmera Wi-Fi) da página de venda (um objetivo só; razão de atenção 1:1 — Unbounce).
7. Rodapé: "Dourado Falcão Educação Corporativa LTDA · CNPJ" (pegar o CNPJ no cartão em documentos_empresa/ do mesmo repo) + e-mail de contato real.
8. Commit "Landing: alinhar com anúncio VSL v12 (hero, app em destaque, prova, rodapé)" e push na main. Conferir a página publicada no celular (playwright 390×844) e mandar o print.

## C. Depois de A e B prontos
- Reportar ao Allan: ids da campanha, print da landing, e o que falta só dele (rótulo IA + ativar).
- Religar o "Auditor de Anúncios" (trig_019JjHRfcjsdBSoWXLQiddsG) com cron diário 09:34 durante os 3 dias do teste (update_trigger enabled:true, cron "CRON_TZ=America/Fortaleza 34 9 * * *") — só depois que o Allan ativar a campanha.
