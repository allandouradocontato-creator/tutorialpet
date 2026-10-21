---
criado: 2026-10-21
base_externa: skills_externas/marketingskills/ads/references/operating-check.md, audit-guardrails.md, meta-andromeda-playbook.md, meta-decision-system.md, payback-period.md; skills_externas/openclaudia/facebook-ads
---
# Habilidade: anúncio Meta com orçamento pequeno — checagem que termina em decisão (Auditor de Anúncios, Guardião de Gasto, Executor de Decisões)

## Leia no original antes de auditar ou recomendar
1. `skills_externas/marketingskills/ads/references/operating-check.md` — os 6 passos em ordem (gasto → tráfego → conversão → fadiga → página → rastreio) e "The decision" (toda checagem termina em UMA decisão).
2. `skills_externas/marketingskills/ads/references/audit-guardrails.md` — Pass/Fail/Unknown/N.A., cobertura de evidência separada de saúde, "Facts / Hypotheses / Missing data", lista do que nunca fazer (pausar só por CPA x fixo, mexer em fase de aprendizado por reflexo).
3. `skills_externas/marketingskills/ads/references/meta-andromeda-playbook.md` — estrutura 80% escala / 20% teste, poucos conjuntos, criativo é a segmentação.
4. `skills_externas/openclaudia/facebook-ads/SKILL.md` — objetivos x KPI, públicos, formatos; **ignorar** a parte "ask before proceeding": o contexto está em .agents/product-marketing.md.

## Regras adaptadas ao Tutorial Pet (R$ 10-30/dia, produto R$ 9,90)
1. **Estrutura mínima**: 1 campanha, 1 conjunto amplo (Brasil, 25-55, sem interesse estreito), 3-4 criativos que já provaram tração orgânica (72 h+, comentário/retenção acima da mediana). Otimização para o evento mais barato que a conta consegue aprender: visualização da landing ou início de checkout; "compra" só quando houver 50 compras/semana (não vai acontecer com este orçamento — não fingir que sim).
2. **Regras de decisão (substituem o sistema B2B de meta-decision-system)**:
   - CPA tolerável = até o preço do produto + bump esperado (hoje ≈ R$ 15-20) — acima disso por 3 dias com ≥ 300 cliques, troca o criativo, não a campanha.
   - Criativo gastou 2x o preço do produto sem venda e com CTR abaixo da mediana do lote → pausa só ele.
   - CPM normal e venda baixa → o problema é landing/oferta (manda para Aprimorador de Landing e oferta_low_ticket.md), não o anúncio.
   - Frequência > 3 e CTR caiu ~1/3 em relação à 1ª semana → fadiga: entra criativo novo, não aumenta orçamento.
   - Escalar só +20-30% a cada 2-3 dias e só com CPA abaixo do ticket; nunca mexer em conjunto em fase de aprendizado por reflexo.
   - Teste dura no máximo 3 dias (regra do Allan); número ruim claro muda o caminho na hora, sem esperar o fim.
3. **Toda rodada termina em exatamente uma decisão** da lista: manter / trocar criativo / pausar criativo X / mandar para landing / pedir ao Allan (só se for dinheiro acima do teto ou nova campanha). Relatório sem decisão é falha (entrega_direta.md).
4. **Honestidade de evidência**: cada checagem é Pass, Fail, Unknown ou N.A.; sem dado do Windsor/Meta = Unknown e "MISSING", nunca estimado; não apresentar "saúde da conta" com cobertura < 60%. Separar Fatos (fonte + janela) / Hipóteses (com confiança) / Dados faltando.
5. **Compliance antes de qualquer "ativar"**: biblioteca/regras_plataformas/ (sem alegação de saúde, sem "você sofre de", UTM obrigatória, Audience Network desligado, afiliado sinalizado).
6. **Jev**: classificar cada criativo em "manter / trocar / pausar" quando as regras do item 2 forem claras (`choice` com `other`); classificar severidade de alerta de gasto (`choice` crítico/menor). Dinheiro acima do teto, nova campanha e pagamento: sempre Allan.
7. Falha/gap (ex.: dado que a rotina não consegue puxar) → registro_de_falhas.md com a solução proposta, não só o problema.
