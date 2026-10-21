# Aprimorador de Landing (agente 31)

Papel: ler cliques e vendas de cada landing, calcular conversão e propor UMA mudança testável por rodada.
Regra de divisão: o script mede e escolhe a alavanca; o Claude (Sonnet) escreve o texto da variante B; o Allan só decide estratégia (aprovar a proposta).

## Leitura obrigatória antes de escrever a variante B (criado 21/10/2026)
biblioteca/habilidades/oferta_low_ticket.md — estrutura de página low-ticket (gancho na linguagem do público, promessa de primeiro resultado, prova honesta, preço com âncora, 1 CTA, FAQ curto) e anatomia da oferta (bônus/garantia/urgência real) para a alavanca "OFERTA" do diagnóstico abaixo.

## Entrada
- `data/landing/metricas.csv` com colunas `data,slug,visitas,cliques_checkout,vendas` (uma linha por dia e landing).
- `config/produtos_landing/<slug>.yaml` (texto atual).

## Métricas
- taxa de clique = cliques_checkout / visitas
- taxa de compra = vendas / cliques_checkout
- conversão = vendas / visitas

## Diagnóstico (escolher UMA alavanca, nesta ordem)
1. Poucas visitas (< 100 na janela): não mudar nada, dado insuficiente. Ação é gerar tráfego/medir.
2. Taxa de clique baixa (< 3%): problema de atenção/promessa -> testar o TÍTULO (promessa) ou a ORDEM das seções (oferta/VSL mais cedo).
3. Taxa de clique ok, taxa de compra baixa (< 5%): problema na oferta/checkout -> testar a OFERTA (preço de/por, garantia em destaque, bônus).
4. Ambas ok mas conversão total < 1,5%: testar PROVA SOCIAL (só depoimento real e autorizado; nunca inventar).
5. Tudo acima da meta: manter e testar o título para ganho incremental.

## Regras
- Uma mudança por rodada; sem promessa de cura ou alegação médica; preço sem "por dia/mês"; nada de prova social inventada.
- Teste grátis: variante B no mesmo YAML (`variantes.B`), gerada em `saida/<slug>/b/`, com `utm_content=...-var-b` no checkout. Dividir o tráfego por link: anúncios/posts A apontam para a URL normal, B para a URL `/b/`.
- Critério de decisão: mínimo de 100 visitas por variante e pelo menos 7 dias; B vence se a conversão for maior E a diferença for maior que 30% relativos (ou 3 vendas a mais); senão mantém A e testa outra alavanca.
- A proposta sai em `data/landing/proposta_<slug>.md` com hipótese, o que muda, como testar de graça e critério de decisão.
