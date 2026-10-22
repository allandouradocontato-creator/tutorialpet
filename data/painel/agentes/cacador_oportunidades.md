# Caçador de Oportunidades de Renda — Departamento Produto e Receita

## CONTRATO DE RESULTADO (22/10/2026)
1. RESULTADO ÚNICO: tempo: itens pendentes de custo R$ 0 com comissão/regra confirmada em página oficial (de 3: Magalu OP-1021-2, Hotmart OP-1021-5, isca digital OP-1021-4). Receita de afiliado hoje: 0 vendas, 0 cliques medidos.
2. META E PRAZO: 2/3 confirmados em fonte oficial até 18:00 de hoje; leituras 15:30 e 18:00.
3. JOGADAS (hipótese -> ação -> métrica -> quando trocar):
   - Jogada 1: Se a comissão oficial muda a decisão -> abrir a página oficial de cada item pendente e marcar dado oficial x secundário -> itens confirmados /3 -> fonte que não abre = 'sem dado' e passa ao próximo.
   - Jogada 2: Se item sem prova pública é ruído -> descartar sem insistir -> itens descartados registrados em decisoes.md -> troca imediata.
   - Jogada 3: Se um item passa de 8/15 e está confirmado -> 1 linha em data/oportunidades/decisoes.md e aviso na hora -> itens com nota >= 8/15 -> cadastro vira pendência do Allan.
4. LAÇO: data/habilidades/aprendizado/cacador_oportunidades.md (1 linha por rodada: data | jogada | resultado n/métrica | mantém/altera/descarta).
5. JUIZ: biblioteca/habilidades/juiz_de_qualidade.md (separado do agente); nota mínima 7 para ir ao vivo.

**Habilidades ligadas:** verificar_antes_de_pedir.md (única citada). O próprio prompt avisa que a rotina foi possivelmente substituída pelo Pesquisador de Mercado e manda confirmar no passo 1 se ainda está ativa; usa o Jev (jev_decisao_rapida.md, referenciado no passo 3) e a entrega do passo 7-9 (similar a entrega_direta.md).
**O que já aprendeu (com prova):** data/oportunidades/decisoes.md (21/10): 6 itens OP-1021-1 a 6, 1 aprovado (Cobasi via Awin, 21/10), 5 pendentes; data/oportunidades/semana.md (21/10 12:50): taxa de pet do Magalu só aparece no painel; Amazon e Mercado Livre sem dado confirmado. SEM PROVA AINDA de que alguma oportunidade gerou receita (0 vendas, 0 cliques de afiliado medidos em data/ofertas/edicoes_propostas.md).
**Habilidades/jogadas que criou ou ganhou hoje (22/10):** nenhuma. git log: config/prompts/cacador_oportunidades.md só no commit de import 603ce8d.
**Como vai aplicar num teste real (resultado em HORAS, não dias; Allan exige):**
- Ação: confirmar na fonte oficial os 3 itens pendentes de custo R$ 0 (Magalu OP-1021-2, Hotmart OP-1021-5, isca digital OP-1021-4) e marcar o que é dado oficial x secundário. Só leitura; nada de cadastro.
- Unidade: item pendente. Métrica: itens com comissão/regra confirmada em página oficial de 3. Leitura: hoje 15:30 e 18:00. Alvo: 2/3 confirmados até 18:00.
- Regra de troca: fonte oficial que não abre = "sem dado" e passa ao próximo; item sem prova pública vira descartado, sem insistir; nota >= 8/15 e confirmado = 1 linha em decisoes.md e aviso na hora.
**Lacunas:** prompt possivelmente redundante com o Pesquisador de Mercado; Shopee sem chave de API; achados baseados em fontes secundárias; nenhuma oportunidade com resultado financeiro.
**Nota de robustez (0–5) e por quê:** 1. Rodou e gerou fila de decisão, mas sem prova de renda e sem habilidade de domínio ligada.

## Limites
- Sem cadastro, compra ou contato; confirmar no passo 1 se o Pesquisador de Mercado já substituiu esta rotina (possível redundância); Shopee sem chave de API; fontes secundárias.
