# Plano de execução B (Sonnet) — 28/10/2026 16:00 — correções pós-auditoria do Fable
Auditoria do Fable sobre o plano A (executado 15:40-15:52). Decisões já tomadas; não reabrir. Ordem obrigatória: 1 → 2 → 3 → 4 → 5 → 6 → 7. Nada é ativado.
Commits: terminar a mensagem com as 2 linhas de atribuição que o sistema pede (Co-Authored-By + Claude-Session).

## O que foi auditado (estado real lido na fonte em 15:55)
- Campanha 120253387444780134, conjunto 120253387467550134, anúncios 120253387470430134 (A) e 120253387471630134 (B), vídeo 2094964854494207: todos PAUSED. OK.
- Orçamento R$ 30/dia, início 2026-10-28T23:00Z (20:00 -03), fim 2026-11-01T02:59Z (31/10 23:59 -03), pixel 2135885120651427 / INITIATED_CHECKOUT, Reels+Feed FB/IG, Advantage+ ligado, idade 25-65 com sugestão 25-55. OK.
- **ERRO GRAVE:** `geo_locations.regions[0]` = key 3864 → o Meta gravou `"name": "Massachusetts", "country": "US"`. O plano A pedia "confirmar pelo nome na resposta"; o Windsor não devolveu o nome no create e ninguém leu de volta. A campanha hoje mira os EUA.
- Landing: 8 itens aplicados e publicados (228ccf0), sem estouro lateral, vídeo 206, imagens 200, Shopee fora, rodapé OK. Dois pontos de copy a corrigir (itens 3 e 4).
- Promessa "ajusta ao porte, à RAÇA e ao temperamento" (anúncios A e B, H1/sub da landing, meta description, card do app) não bate com o app: o onboarding pergunta porte, fase de vida, energia e temperamento; raça não existe. Isso é afirmação falsa em anúncio (política do Meta sobre alegações enganosas + CDC art. 37). Corrigir ANTES de ativar.

## 1. Corrigir a região do conjunto (bloqueante)
- O Windsor não tem busca de geolocalização. Método: `update_adset` {adset_id:"120253387467550134", targeting:{...mesmo targeting atual..., geo_locations:{regions:[{key:"<K>"}]}}} e em seguida `get_data` (fields adset_targeting, filtro adset_id, option include_objects_without_insights=true) para ler o `name`/`country` gravados.
- As keys do Meta são sequenciais por país em ordem alfabética (EUA: Alabama 3843 … Massachusetts 3864). São Paulo é o 25º estado do Brasil em ordem alfabética. Tentar na ordem: 474, 473, 475, 472, 476, 471. Parar na primeira leitura com name "São Paulo" e country "BR". Máximo 6 tentativas.
- Se nenhuma der São Paulo: usar `geo_locations:{countries:["BR"]}` (Brasil inteiro) e registrar na ficha "SP não encontrado por key; rodando Brasil" — decisão do Fable, não perguntar.
- Manter no targeting tudo o que já está (age_min 25, age_max 65, age_range [25,55], advantage_audience 1, plataformas e posições). Reenviar o targeting completo, pois o Meta substitui o objeto inteiro.
- Confirmar por leitura e gravar o JSON lido na ficha.

## 2. Domínio de conversão nos 2 anúncios
- `update_ad` {ad_id, conversion_domain:"tutorialpet.com.br"} em 120253387470430134 e 120253387471630134. Motivo: anúncio de conversão com destino em site precisa de domínio de conversão; sem ele o Meta costuma barrar na ativação ("domínio de conversão obrigatório"). Se a API recusar, registrar o erro exato e seguir.

## 3. Copy honesta: "raça" sai, "energia" entra (anúncios + landing)
Texto novo da promessa: "ajusta os exercícios ao porte, à energia e ao temperamento dele".
- Anúncio A: `update_ad_creative` {ad_id:"120253387470430134", message:"Travesseiro virou confete, sofá arranhado e o vizinho reclamando do latido? O Sozinho em Casa é um plano de 14 dias de atividades práticas, com app que ajusta os exercícios ao porte, à energia e ao temperamento do seu cachorro. R$ 27, pagamento único. Garantia de 14 dias: fez o plano e não gostou? Devolvemos tudo."}
- Anúncio B não cita raça: não mexer.
- Landing (repo sozinho-em-casa-app, landing/index.html): trocar "à raça" por "à energia" no `.sub` do hero, na meta description e no card do app ("ajustado ao porte, à energia e ao temperamento"). Conferir com grep que "raça" sumiu da página.
- Depois do `update_ad_creative`, ler os anúncios de volta (campos body/title/link) e conferir que o texto novo e o link com utm_content=ad_a continuam lá (a ação cria criativo novo; verificar que o thumbnail e o botão SHOP_NOW permaneceram).

## 4. Dois ajustes pequenos na landing (mesmo commit do item 3)
- Eyebrow da seção do vídeo está "Como funciona" e a seção dos 3 passos também: trocar o da seção do vídeo para "Em 1 minuto".
- `<title>` para "Sozinho em Casa — manual + app, R$ 27" (igual ao título do anúncio A).
- Fonte da frase sobre ansiedade de separação: tentar substituir por fonte com número. Candidata open access: Salonen et al. 2020, Scientific Reports, "Prevalence, comorbidity, and breed differences in canine anxiety in 13,700 Finnish pet dogs" (nature.com). Só usar se o WebFetch conseguir ler o texto e extrair o número exato de cães com comportamento relacionado à separação; a frase cita o número como o artigo diz, em pt-BR, com link, e termina com "(estudo finlandês)". Se não conseguir ler, manter a frase atual do PubMed. Nunca citar o que não leu.
- Commit "Landing: copy honesta (energia no lugar de raça), título e fonte" + push na main. Conferir em 390×844 com playwright (scripts já em /tmp/claude-0/work/page.py desta sessão; se não existir, refazer: viewport 390×844, print do topo e full page) e mandar o print.

## 5. Conferência final por leitura (não por status verde)
- `get_data` nos 2 anúncios: status PAUSED e effective_status; se "WITH_ISSUES" ou "DISAPPROVED", ler o motivo e registrar.
- `get_data` no conjunto: targeting com São Paulo/BR, orçamento 3000, datas iguais às acima.
- Gravar tudo na ficha data/anuncios/campanha_vsl_v12_sp.md, seção "Estado conferido em 28/10 <hora>".

## 6. Registro de erros e lições (mesmo dia, regra 17)
Em data/memoria/07 Erros e lições.md, 1 linha cada:
- 28/10: key de região do Meta (3864) era Massachusetts, não São Paulo; criado o conjunto sem ler o nome de volta. Lição: ID de geolocalização só vale depois de ler `name` + `country` na resposta.
- 28/10: evento de otimização é INITIATED_CHECKOUT (não INITIATE_CHECKOUT); com Advantage+ o age_max mínimo é 65 (faixa menor entra como age_range).
- 28/10: `pkill -f` com padrão que casa a própria linha de comando mata o shell da sessão; usar `pkill -f "http.server 8765" ` fora de comando composto ou `kill` pelo PID.
- 28/10: copy prometeu "raça" sem o app ter esse campo; lição: toda promessa de funcionalidade em anúncio/landing é conferida contra o produto real antes de publicar.
Em biblioteca/regras_de_ouro.md, 1 linha nova: "35. (28/10/2026) ID de geolocalização, interesse ou público do Meta só é aceito depois de ler o nome de volta na API; promessa de funcionalidade em anúncio/landing é conferida no produto antes de publicar."
Atualizar data/memoria/17 Retomada (3 linhas: campanha pausada pronta, landing publicada, o que falta só do Allan).

## 7. Relatório ao Allan (curto)
- Região gravada (nome lido), ids, print da landing, e só o que depende dele: marcar "conteúdo gerado por IA" nos 2 anúncios, conferir pagamento/saldo, ativar.
- Parte C continua igual: só depois que o Allan ativar, `update_trigger` no Auditor de Anúncios (trig_019JjHRfcjsdBSoWXLQiddsG) enabled:true, cron "CRON_TZ=America/Fortaleza 34 9 * * *".
