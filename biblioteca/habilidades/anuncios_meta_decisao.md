---
criado: 2026-10-21
versao: v2 — 22/10/2026
base_externa: skills_externas/marketingskills/ads/references/operating-check.md, audit-guardrails.md, meta-andromeda-playbook.md, meta-decision-system.md, payback-period.md; skills_externas/openclaudia/facebook-ads
---
v2 — 22/10/2026 — status: rascunho até prova (régua 7)

# Habilidade: anúncio Meta com orçamento pequeno — checagem que termina em decisão (Auditor de Anúncios, Guardião de Gasto, Executor de Decisões)

## CONTRATO DE RESULTADO (22/10/2026)
1. RESULTADO ÚNICO: venda (R$). Custo por checkout do Sozinho em Casa (R$ 27) em modo SIMULAÇÃO, sem verba (fonte: Windsor, conector facebook, cruzado com Kiwify). Referência de 22/10: R$ 7,32 por checkout em 28 dias (data/anuncios/auditoria.md).
2. META E PRAZO: HOJE (22/10) às 16h e às 20h: cobertura ≥ 4 de 6 passos do operating-check (67%), UMA decisão de uma linha por leitura e custo por checkout ≤ R$ 7,32. Meta de venda em R$ só existe com verba aprovada pelo Allan (hoje sem verba; gasto 7 dias R$ 0,00).
3. JOGADAS (hipótese -> ação -> métrica -> quando trocar):
   - Checagem de 6 passos em simulação. Hipótese: decisão diária com dado real evita gasto sem prova. Ação: puxar Windsor (somente leitura) e fechar a tabela de decisão com UMA decisão. Métrica: cobertura de passos com dado (hoje gasto e tráfego com dado; UTM e teto unknown). Trocar: cobertura < 60% = não declarar saúde da conta e abrir registro_de_falhas.md com a solução do gap.
   - Atribuição de venda por campanha. Hipótese: sem cruzar checkout x Kiwify não existe CPA nosso. Ação: cruzar checkouts do Windsor com vendas do Kiwify por UTM. Métrica: % de checkouts com origem atribuída. Trocar: venda sem origem = corrigir o rastreio antes de qualquer verba.
   - Ficha de impulsionamento na hora. Hipótese: criativo orgânico que passou de 72 h acima da mediana é o único candidato a verba. Ação: quando houver (TikTok ≥ 1.006 views ou tempo ≥ 7,46 s; FB tempo ≥ 5,7 s; IG alcance ≥ 122), montar a ficha (público, teto, prazo) para o Allan aprovar em até 1 h. Métrica: tempo entre o criativo qualificar e a ficha entregue. Trocar: nenhum criativo qualifica = registrar unknown e seguir (nunca impulsionar por parecer bom).
   - Alerta de gasto. Hipótese: campanha ativa sem teto é o maior risco de perda. Ação: se aparecer campanha ativa do Tutorial Pet gastando sem teto, primeira linha "ALERTA ANÚNCIO" (campanhas "Marketplace turbinado" são de outro produto: não tocar). Métrica: alertas abertos. Trocar: sem alerta em 7 dias = manter a checagem só 1 vez ao dia.
4. LAÇO: data/habilidades/aprendizado/anuncios_meta_decisao.md, 1 linha por rodada: data | jogada | resultado n/métrica | mantém/altera/descarta. Número ruim = troca de jogada na mesma rodada.
5. JUIZ: biblioteca/habilidades/juiz_de_qualidade.md (Juiz de Qualidade, agente separado de quem produz; nota mínima 7 para ir ao vivo; ensaio aprovado = média ≥ 7 e nenhuma nota < 5).


Leia no original: `ads/references/operating-check.md` (6 passos: gasto, tráfego, conversão, fadiga, página, rastreio; "The decision"), `audit-guardrails.md` (Pass/Fail/Unknown/N.A., Facts/Hypotheses/Missing data) e `meta-andromeda-playbook.md`. Ignore o "ask before proceeding" do openclaudia: o contexto está em .agents/product-marketing.md. O ciclo antes do "ativar" (elegibilidade, UTM, revisão) está em `trafego_meta_ads.md`; esta skill é a checagem diária.

## Procedimento
1. Cabeçalho "Dados até <data hora> — fonte". Puxar Windsor (conector `facebook`): gasto, impressões, cliques, CTR, CPM, frequência, resultados por anúncio e dia. Sem Windsor = cobertura 0%, tudo unknown. Venda: Kiwify pelo Chrome do Allan (list_connected_browsers primeiro).
2. Elegibilidade: Account Status, pagamento, domínio, CNPJ. Cada item pass / fail / unknown; qualquer fail/unknown = não ativar.
3. Compliance do texto ([C] 2-3 e checklist [N]): pass / fail / unknown. UTM presente (utm_source, medium=paid, campaign, content) e Audience Network desligado.
4. Seis passos do operating-check, cada um pass / fail / unknown / N.A.: gasto (dentro do teto?), tráfego (cliques >= 300?), conversão, fadiga, página, rastreio. Cobertura = passos com dado / 6; abaixo de 60% = não declarar "saúde da conta".
5. Separar por escrito Fatos (fonte + janela), Hipóteses (confiança) e Dados faltando.
6. Tabela de decisão: gasto 2x preço sem venda e CTR baixo = pausar criativo X; CPM normal e venda baixa = mandar à landing (oferta_low_ticket.md); fadiga = criativo novo, sem subir orçamento; resto dentro do limite = manter; sem dado = manter e registrar unknown.
7. Saída: exatamente UMA decisão entre manter / trocar criativo / pausar criativo X / mandar para landing / pedir ao Allan (só dinheiro acima do teto ou nova campanha). Relatório sem decisão = falha (entrega_direta.md).
8. Jev (`choice`) classifica criativo e severidade quando a regra é clara; dinheiro e pagamento sempre Allan. Gap de dado vai a registro_de_falhas.md com a solução.

## Saída obrigatória
Uma linha em `data/habilidades/aprendizado/anuncios_meta_decisao.md`, formato: `data | regra aplicada (nº do passo) | resultado (n, métrica, decisão) | mantém/altera`. Rodada sem a linha = "não aplicou". Regra das 3 linhas: 3 linhas com o mesmo padrão = propor edição desta skill (versão, data, evidência) em entrega_direta.md.

## Limites (regras de plataforma, validações e números de corte; não são jogadas)
Movido em 22/10/2026 para o fim: o que o agente FAZ está nas jogadas acima; aqui só o que ele não pode ultrapassar.

### Regras do Allan que mandam (05 Decisões.md)
Dinheiro novo, nova campanha, aumento de teto e pagamento = decisão do Allan. Teste de no máximo 3 dias; número ruim claro muda o caminho na hora. Só vídeo no criativo. Preço: Sozinho em Casa R$ 27 (âncora R$ 97, pagamento único; o R$ 9,90 acabou); upsell Adestramento Básico R$ 47. Sem preço por dia/mês, sem "cão" (cachorro), gancho "Esse erro tá silenciosamente…" proibido, sem "link no perfil", IG até 5 hashtags. Anúncio só de criativo com tração orgânica. Links só do domínio do Allan, nunca vercel.app.

### Regras de plataforma que esta skill aplica (só [C])
Fonte: meta_facebook_instagram.md (lido 22/10/2026).
1. [C] Se o Account Status do IG está restrito, então nenhum anúncio: resolver antes (Instagram, Account Status).
2. [C] Se a Duda é fotorrealista ou a voz soa como pessoa, então rótulo de IA no anúncio; a Meta rotula pessoa fotorrealista e detecta sozinha (Anúncios, IA, jun/2026). Ao duplicar campanha, reconferir.
3. [C] Se o anúncio traz conteúdo desmentido por checadores, então é rejeitado: nenhuma afirmação factual sem fonte (Anúncios).
4. [C] Se o anúncio é Click-to-Messenger/Direct, então a janela de resposta pode chegar a 7 dias após o clique (changelog 28/09/2026); fora da janela, só Sponsored Message (Mensagens).
5. [C] Se a conversa precisa de humano depois da janela padrão de 24 h, então tag Human Agent (7 dias); uso fora do caso aprovado gera restrição.

#### Validar antes de agir ([N]) — conferir no Gerenciador/Chrome antes de gastar
- [N] Promessa de cura/prevenção ou "resolve ansiedade de separação" reprova; usar texto neutro (não confirmado em página oficial).
- [N] Atributo pessoal ("você está sofrendo…", "seu cachorro tem…") reprova.
- [N] Venda/doação de animal; regra específica de infoproduto; landing precisa corresponder ao anúncio, ter privacidade e identificar a empresa.
- [N] Requisitos de conta no Brasil (CNPJ Dourado Falcão Educação Corporativa LTDA, pagamento, verificação de domínio).
- [N] Links externos reduzem alcance? Sem fonte oficial lida.

### Limites de decisão (números nossos)
Dados de anúncio: nenhum campanha rodou ainda; Kiwify 7 dias = 0 vendas, 0 checkouts abandonados, visitas sem dado (data/testes/baseline_2026-10-21.md, lido 21/10; medição 22/10 idem).
| Item | Limite | Base |
|---|---|---|
| Criativo elegível | orgânico 72 h+ com tempo médio acima da mediana da rede: FB > 4,0 s e idealmente >= 6 s; TikTok > 2,87 s e idealmente >= 4 s; IG skip < 55,6% | estrategia_social.md 22/10 (n=12 FB/IG); relatorio.md 22/10 (35 posts) |
| Hoje | nenhum FB/IG chega a 6 s; melhor candidato: "Seu cachorro aguenta quantas horas sozinho?" (TikTok 7,46 s) e FB sofá 5,7 s | idem |
| Gasto sem venda | criativo que gastou 2x o preço (R$ 54) sem venda e com CTR abaixo da mediana do lote = pausar só ele | R$ 27 x 2 |
| CPA máximo | até R$ 27 (ponto de equilíbrio bruto). Taxa Kiwify e valor do bump/upsell: medir primeiro: ler a taxa no painel Kiwify e as vendas do upsell em 7 dias | preço atual |
| CTR, CPM, frequência, queda de CTR | sem número nosso: medir primeiro: 3 dias de teste com R$ 10-30/dia, registrar mediana por criativo; até lá usar só a comparação entre os criativos do lote | nenhuma campanha rodou |
| Cliques mínimos para julgar | 300 cliques (regra da skill) antes de culpar anúncio ou landing | skill v1 |
| Fadiga / escala | frequência > 3 e CTR -1/3 vs primeiros dias = criativo novo; escala +20-30% a cada 2-3 dias só com CPA < R$ 27 | skill v1; unknown até haver dados |
Proibido usar CPA, CTR ou CPM de outra rede ou de outro nicho.
