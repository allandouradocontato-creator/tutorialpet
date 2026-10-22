---
criado: 2026-10-21
---
# Habilidade: Registro de falhas (todo agente usa, não só quem é pego numa falha)

## Por que existe
Pedido do Allan (21/10/2026): os agentes falharam muito (ver histórico em
data/memoria/07 Erros e lições.md) e quase sempre é ELE quem percebe primeiro
(ex.: Estrategista de Redes Sociais nunca propôs a tática óbvia de isca via
comentário→DM; o Allan viu num vídeo externo, não um agente apontando o
próprio limite). Isso significa que a fábrica está "no escuro" sobre os
próprios gaps. Esta habilidade fecha esse buraco: cada rotina passa a
registrar sozinha quando NÃO conseguiu fazer algo que era esperado dela —
não só quando dá erro técnico, mas quando falta know-how/método (uma
"falha de habilidade").

## Regra
Toda rotina, ao final do seu passo de resultado, se perceber que:
- deixou de propor algo que seu objetivo deveria cobrir (ex.: tática conhecida
  do nicho que não apareceu), ou
- teve que decidir "no escuro" por falta de método/referência, ou
- repetiu um erro já listado em 07 Erros e lições.md,

então ACRESCENTA uma linha nova em `data/memoria/07 Erros e lições.md`, no
mesmo formato do arquivo (`data | erro | causa | como evitar`), com a causa
escrita como FALTA DE HABILIDADE quando for o caso (não só bug/dado errado).
Isso é tão rotina quanto escrever o relatório — não precisa perguntar ao
Allan, só registrar.

## Portão de honestidade (não maquiar)
Não vale registrar só falha pequena/tecnica para parecer que está tudo bem.
Se a rotina sabe que entregou abaixo do esperado em algo estratégico
(oferta fraca, gancho sem método, audiência sem embasamento), ela registra
isso TAMBÉM, mesmo sem ninguém ter reclamado ainda. Jev pode ajudar a
classificar severidade (crítico x menor) — ver jev_decisao_rapida.md — mas
a decisão de registrar ou não a falha NUNCA passa pelo Jev: isso é
julgamento sobre o próprio trabalho, sempre feito pelo agente.

## Quem já está puxando dessa lista
Triagem de Decisões e o Otimizador de Processos devem ler 07 Erros e
lições.md periodicamente e transformar um padrão repetido (3+ ocorrências
da mesma causa) em proposta de nova habilidade/skill para biblioteca/habilidades/,
igual este arquivo nasceu de uma falha registrada.

- 2026-10-22 | Estrategista de Redes Sociais | T9(c): não usou a isca vigente como entrada da matriz e manteve CTA "GUIA" da isca descartada; disse "PC ausente" sem list_connected_browsers (repete a regra de ouro 5) | ação: E31, plano em data/testes/plano_2026-10-22.md
