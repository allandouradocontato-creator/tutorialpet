# Suporte — serviço automatizado, mas serviço

Princípio: a plataforma é serviço. Se der problema, o cliente precisa de resposta
rápida e certa. Suporte bom é o que mantém a assinatura.

## Níveis
| Nível | Quem resolve | O que cobre | Meta de tempo |
|---|---|---|---|
| 0 — Prevenção | O próprio produto | Checagens automáticas antes de cada botão (preço, link, página no ar, conta conectada) | antes do erro |
| 1 — Bot de suporte | Agente treinado com o Livro de Gaps + docs do painel | Dúvidas de uso, erros conhecidos, "como faço" | < 1 min, 24h |
| 2 — Diagnóstico automático | Agente com acesso ao estado da conta do cliente (gerações, créditos, conexões) | "minha página não publicou", "crédito sumiu", "campanha não ativou" | < 15 min |
| 3 — Humano (Allan/equipe) | Só o que o bot não fechou | Reembolso, bug novo, caso sensível | < 24h útil |

## Automação (grátis primeiro)
- Canal: WhatsApp (ManyChat já conectado) + chat dentro do painel.
- Motor: modelo barato (Jev/OpenRouter) com busca no Livro de Gaps e nos docs; sobe para modelo forte só em diagnóstico.
- Cada atendimento do nível 3 vira linha nova no Livro de Gaps no mesmo dia.
- Métricas semanais no analytics_bi_agent: tickets por tipo, % resolvido pelo bot, tempo médio, gap mais frequente.

## Regras
- Nunca pedir ao cliente para "achar" uma tela: o bot manda o link direto ou executa.
- Nunca dizer "funcionou" sem conferir a saída real (gap #12).
- Crédito não é debitado se a geração falhar (gap #13).
- Resposta sempre em português simples, sem jargão técnico.
