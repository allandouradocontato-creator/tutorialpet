# Campanha Meta Ads — Sozinho em Casa, VSL v12 (preparada em 28/10/2026, aguardando "pode" do Allan)
Fonte das regras: biblioteca/habilidades/trafego_meta_ads.md + anuncios_meta_decisao.md + marketingskills/ads/references/meta-andromeda-playbook.md.
Conta de anúncios 1213984913380523 (Allan Dourado) · Página Tutorial Pet 1251330151406637 · Pixel 2135885120651427 · Landing https://sozinho.tutorialpet.com.br (R$ 27, garantia 14 dias).

## Estrutura (1 campanha, 1 conjunto, 2 anúncios)
- Campanha: "Sozinho em Casa - VSL v12 - SP apartamento - teste 3 dias" · objetivo OUTCOME_SALES · criada PAUSADA.
- Conjunto: otimização INITIATE_CHECKOUT (pixel 2135885120651427; a Kiwify dispara InitiateCheckout e Purchase; histórico: 10 checkouts em 28 dias, 0 compras — Purchase ainda não tem dado para o Meta aprender). Posicionamentos: Reels + Feed (FB/IG); Audience Network desligado. Orçamento R$ 30/dia × 3 dias = R$ 90 (teto da faixa 10–30/dia da skill). Início/fim fixos (3 dias).
- Público (pedido do Allan 25/10 + 28/10): Brasil, estado de São Paulo (RMSP prioridade), 25–55, público Advantage+ com sinais: Cães, Adestramento de cães, Petz/Cobasi/Petlove, Comportamento animal. "Apartamento" não é interesse confiável no Meta: quem seleciona o apartamento é o CRIATIVO (vizinho reclamando, corredor, porta do apartamento) — playbook Andromeda: "creative is the targeting".
- Anúncio A (problema): texto "Travesseiro virou confete, sofá arranhado e o vizinho reclamando do latido? O Sozinho em Casa é um plano de 14 dias de atividades práticas, com app que ajusta os exercícios ao porte, à raça e ao temperamento do seu cachorro. R$ 27, pagamento único. Garantia de 14 dias: fez o plano e não gostou? Devolvemos tudo." · Título "Sozinho em Casa: manual + app, R$ 27" · Botão COMPRAR AGORA.
- Anúncio B (benefício): texto "Em 14 dias, o latido acaba, o vizinho sossega e você sai de casa em paz. Sozinho em Casa: manual + aplicativo, R$ 27 (de R$ 97), pagamento único, garantia de 14 dias sem perguntas." · Título "Plano de 14 dias com app · R$ 27" · Botão COMPRAR AGORA.
- Vídeo: VSL_A_Instagram_v12_tarja_produto_genero_neutro.mp4 (62,7 s, 9:16) — URL pública: https://raw.githubusercontent.com/allandouradocontato-creator/tutorialpet/media/anuncios/VSL_A_Instagram_v12_tarja_produto_genero_neutro.mp4 · capa: .../anuncios/VSL_A_v12_thumb_duda.jpg
- UTM: utm_source={{site_source_name}}&utm_medium=paid&utm_campaign=sozinho_vsl_v12_sp&utm_content={{ad.name}}
- Conformidade: sem "resolve ansiedade de separação", sem "seu cachorro tem…", sem saúde; Duda é IA fotorrealista → marcar "conteúdo gerado por IA" no Gerenciador antes de ativar.

## Critérios de leitura (regra anuncios_meta_decisao, 1 decisão por leitura, diário)
- Gastou R$ 54 (2× preço) sem venda e CTR abaixo da mediana da conta → pausar o anúncio.
- CPM normal e checkout sem venda → problema é landing/oferta, não o anúncio.
- Frequência > 3 e CTR caindo 1/3 → fadiga → criativo novo (não subir verba).
- Desvio combinado em 20/10: ≥ 100 visitas reais e 0 vendas em 3 dias → preço cai para R$ 17 por 3 dias.

## Bloqueio atual
Windsor: "Write actions are disabled" para allandouradocontato@gmail.com. Para o Claude criar a campanha pausada pela API, o Allan liga em https://onboard.windsor.ai/app/settings/account → "Enable write actions for Claude, ChatGPT & API". Alternativa: Claude cria no Gerenciador pelo navegador.

## Criada PAUSADA em 28/10/2026 (Sonnet, via Windsor, conta 1213984913380523)
- Campanha 120253387444780134 · Conjunto 120253387467550134 (R$ 30/dia, 28/10 20:00 → 31/10 23:59 -0300) · Vídeo 2094964854494207
- Anúncio A 120253387470430134 (VSL_A_v12_ad_A_problema) · Anúncio B 120253387471630134 (VSL_A_v12_ad_B_beneficio) · ambos status PAUSED (effective_status IN_PROCESS = Meta processando o criativo).
- Ajustes exigidos pela API: custom_event_type = INITIATED_CHECKOUT (não INITIATE_CHECKOUT); com Advantage+ o controle de idade máxima é 65, então age_min 25 / age_max 65 com age_range [25,55] como SUGESTÃO.
- Interesses (Cães, Adestramento, Petz/Cobasi/Petlove) NÃO aplicados: o Windsor não busca IDs de interesse e a API exige ID. O conjunto roda com Advantage+ aberto (São Paulo, 25-55 sugerido); o criativo faz a segmentação (playbook Andromeda). Se o Allan quiser sinais de interesse, adicionar no Gerenciador.
- BRAZIL_REGULATION / identidade verificada: a API NÃO pediu nada ao criar o conjunto (sem erro "Advertiser is missing").
- Nada ativado. Pendências só do Allan: marcar "conteúdo gerado por IA" nos anúncios; conferir pagamento/saldo; ativar.

## Landing publicada em 28/10/2026 (commit 228ccf0, repo sozinho-em-casa-app)
- Aplicados os 8 itens do plano; VSL v12 reencodada (720x1280, CRF 26, 8,5 MB) em landing/vsl-v12.mp4; 3 telas do app em landing/fotos/app-tela-1..3.png; Shopee removida; rodapé com razão social + CNPJ 65.211.970/0001-81 + e-mail.
- Fonte da frase sobre ansiedade de separação: PubMed 18672155 (só o resumo foi lido; afirma "especialmente prevalentes", sem número). A PMC8868415 bloqueou leitura (reCAPTCHA) e não foi usada.
- Tela do plano do app capturada rolada para não exibir o cartão "Sinais de ansiedade de separação" (evita afirmar algo sobre o cachorro).
- ATENÇÃO (decisão do Fable mantida, mas conferir): o texto do anúncio e da landing diz que o app ajusta ao porte, "à raça" e ao temperamento, porém o onboarding do app pergunta porte, fase, energia e temperamento (não raça).

## Estado conferido em 28/10/2026 ~16:25 (plano B, Sonnet; leitura via get_data)
- REGIÃO CORRIGIDA: a key 3864 gravada no create era Massachusetts/US (o Windsor não devolve o nome no create). Tentadas as keys 474, 473, 475, 472, 476, 471 em update_adset: todas recusadas pelo Meta com "Regiões não são suportadas no país selecionado" (code 100, subcode 1487130); nenhuma foi gravada. Fallback decidido pelo Fable aplicado: geo_locations.countries ["BR"] (Brasil inteiro). Lido de volta: {"countries":["BR"],"location_types":["frequently_in","home","recent"]}. SP-only NÃO foi obtido: para restringir a SP o Allan escolhe "São Paulo" no Gerenciador (Conjunto > Público > Locais), 1 clique.
- Conjunto 120253387467550134: PAUSED, R$ 30/dia (3000), 28/10 23:00Z → 01/11 02:59Z (20:00 → 23:59 -03), INITIATED_CHECKOUT pixel 2135885120651427, Reels+Feed FB/IG, Advantage+ idade 25-65 com sugestão 25-55.
- Conversion domain tutorialpet.com.br aplicado nos 2 anúncios (update_ad OK).
- Anúncio A 120253387470430134: criativo novo 1820010209034624 (texto "porte, à energia e ao temperamento"); lido de volta: body novo, título, CTA SHOP_NOW e destino com utm_content=ad_a mantidos; PAUSED, effective_status PENDING_REVIEW (revisão normal do Meta).
- Anúncio B 120253387471630134: sem "raça" no texto; destino com utm_content=ad_b; PAUSED.
- Landing (commit f2258ec): "à raça" → "à energia" (meta, hero, card do app; 0 ocorrências de "raça" na página publicada), eyebrow "Em 1 minuto", title "Sozinho em Casa — manual + app, R$ 27". Frase de ansiedade de separação MANTIDA com PubMed 18672155: o estudo finlandês (Salonen 2020, Sci Rep) não pôde ser lido (nature.com fora da lista; resumos em portais não trazem a % de separação; só 32% para ruídos), então não foi citado número.
- Nada ativado. Só o Allan: marcar "conteúdo gerado por IA", conferir pagamento/saldo, (opcional) restringir o local a São Paulo, ativar.

## Região SP corrigida e conferida em 28/10/2026 16:17 (Sonnet)
- Conjunto 120253387467550134 agora: geo_locations.regions [{key 460, name "São Paulo (state)", country BR}] (lido de volta; substitui o fallback Brasil inteiro). Orçamento 3000, PAUSED, início 28/10 23:00Z.
- Mapa de keys de região do Meta (BR) lido na API: Ceará 443, Piauí 453, Rio Grande do Sul 456, São Paulo (state) 460, Goiás 462. (Deduzido pela ordem alfabética; 471-476 e 3864 pertencem a outros países; 3864 = Massachusetts/US.)
- Atenção na leitura: o Windsor guarda em cache a resposta de consultas IDÊNTICAS (mesmos campos/filtros/período); para ler o estado novo depois de um update, mudar a lista de campos ou o date_preset.
- Pendência única: rótulo "conteúdo gerado por IA" nos 2 anúncios (só pelo Gerenciador, perfil Allan Dourado). Regra 26: não ativar antes. Depois: ativar campanha+conjunto+2 anúncios e religar o Auditor (trig_019JjHRfcjsdBSoWXLQiddsG, 09:34 Fortaleza).

## ATIVADA em 28/10/2026 16:40 (ordem do Allan: "ative assim mesmo", sem rótulo de IA)
- enable_adset 120253387467550134 e enable_campaign 120253387444780134 executados (Windsor). Leitura: os 2 anúncios passaram de ADSET_PAUSED para ACTIVE/ACTIVE (pais ativos). Início da veiculação 28/10 20:00 (-03), fim 31/10 23:59.
- Rótulo "conteúdo gerado por IA": caixa não encontrada pelo Allan (editor em massa e edição); pesquisa indica que só é obrigatória em anúncio político e que, em comercial no Brasil, o Meta pode não oferecê-la. Exceção à regra 26 autorizada pelo Allan. Frase "Duda é personagem criada com IA" proposta e NÃO aplicada.
- Auditor de Anúncios religado (trig_019JjHRfcjsdBSoWXLQiddsG, cron 09:34 Fortaleza, próxima 29/10 09:34).
- Pendente só do Allan: verificação de organização (CNPJ) no Meta, saldo/pagamento.
