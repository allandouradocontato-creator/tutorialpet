---
criado: 2026-10-21
---
# Habilidade: Jev para decisão rápida (qualquer rotina pode usar)

"Dev"/Jev = typesafe/jev-1.13 via OpenRouter. Regra do Allan: Jev decide, Claude/agente escreve; quando o Jev não tem certeza, quem decide é o agente (nunca parar e esperar o Allan por causa do Jev).

## POLÍTICA PADRÃO (Allan, 21/10/2026): é regra, não exceção
"Tudo que precisa decidir, que ele [Jev] faça; que ele seja chamado para integrado." Ou seja: NÃO é um recurso usado só quando alguém lembrar — toda rotina que bate numa classificação/escolha simples e básica (não estratégica, não de dinheiro/login) CHAMA o Jev primeiro, por padrão, antes de decidir sozinha. O agente só decide por conta própria quando o Jev voltou com baixa confiança (portão abaixo) ou quando a pergunta exige julgamento complexo demais para uma chamada (aí o agente decide E registra por quê não usou o Jev).
Jev é rápido e barato, não necessariamente o mais acertado — por isso o portão de confiança abaixo existe: pegar as decisões básicas/binárias com ele, deixar o julgamento fino para o agente.

## Onde já está ligado (21/10/2026)
- Executor de Decisões: prioridade entre 2 decisões do mesmo dia.
- Triagem de Decisões (painel): aprovar/testar/fila/descartar cada proposta.
- Criador de Audiência: classificar cada ideia como LIBERADA ou SENSÍVEL antes de produzir.
- Caçador de Oportunidades de Renda (e demais caçadores): julgar se um achado já foi visto/decidido antes de entrar no relatório.

## Quando usar (lista cresce; qualquer rotina nova com decisão básica deve adotar)
Priorizar 2 decisões do mesmo dia, classificar proposta como aprovar/testar/descartar, julgar se uma ideia é "liberada" ou "sensível", julgar se um achado já foi visto antes, decidir qual de duas variações testar primeiro, classificar severidade de um erro/alerta (crítico x menor).

## Como chamar
POST https://openrouter.ai/api/alpha/decisions, body `{"model":"typesafe/jev-1.13","state":<objeto curto em inglês>,"questions":{...}}`, SEM cabeçalho Authorization (o proxy da nuvem injeta a credencial automaticamente nesta sessão). Ver detalhes de tipos de pergunta (choice/score/noul) na skill jev-classify.

## Portão de confiança (não negociar)
- choice/score com confidence < 0,5 → agente decide.
- noul entre 0,25 e 0,75 → agente decide.
- Erro de rede/401/403 → seguir sem Jev, registrar "Jev indisponível: <erro>", nunca travar a rotina por isso.
- NUNCA usar Jev para: dinheiro, compra, login/2FA, identidade, conteúdo sensível (política, religião, tragédia) — essas continuam indo ao Allan sempre.

## Privacidade
Só manda ao Jev o que é público ou já está nos arquivos da fábrica (relatórios, propostas, métricas). Nunca manda dado de cliente/comprador.
