---
criado: 2026-10-21
---
# Habilidade: Jev para decisão rápida (qualquer rotina pode usar)

"Dev"/Jev = typesafe/jev-1.13 via OpenRouter. Regra do Allan: Jev decide, Claude/agente escreve; quando o Jev não tem certeza, quem decide é o agente (nunca parar e esperar o Allan por causa do Jev).

## Quando usar
Qualquer rotina na nuvem que precise ESCOLHER entre opções conhecidas, sem gasto de dinheiro nem login envolvido: priorizar 2 decisões do mesmo dia (Executor), classificar proposta como aprovar/testar/descartar (Triagem — já em uso), julgar se uma ideia é "liberada" ou "sensível" (Criador de Audiência pode adotar), julgar se um achado de oportunidade já foi visto antes (Caçadores).

## Como chamar
POST https://openrouter.ai/api/alpha/decisions, body `{"model":"typesafe/jev-1.13","state":<objeto curto em inglês>,"questions":{...}}`, SEM cabeçalho Authorization (o proxy da nuvem injeta a credencial automaticamente nesta sessão). Ver detalhes de tipos de pergunta (choice/score/noul) na skill jev-classify.

## Portão de confiança (não negociar)
- choice/score com confidence < 0,5 → agente decide.
- noul entre 0,25 e 0,75 → agente decide.
- Erro de rede/401/403 → seguir sem Jev, registrar "Jev indisponível: <erro>", nunca travar a rotina por isso.
- NUNCA usar Jev para: dinheiro, compra, login/2FA, identidade, conteúdo sensível (política, religião, tragédia) — essas continuam indo ao Allan sempre.

## Privacidade
Só manda ao Jev o que é público ou já está nos arquivos da fábrica (relatórios, propostas, métricas). Nunca manda dado de cliente/comprador.
