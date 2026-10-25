---
criado: 2026-10-21
---
# Habilidade: Registro de falhas (todo agente usa, não só quem é pego numa falha)

## CONTRATO DE RESULTADO (22/10/2026)
1. RESULTADO ÚNICO: tempo: horas entre a falha acontecer e ela virar linha em 07 Erros e lições (hoje quase sempre quem percebe é o Allan; fonte: o próprio 07 Erros e lições.md e as linhas deste arquivo).
2. META E PRAZO: toda falha de rotina de HOJE 22/10 registrada na mesma rodada (zero descoberta primeiro pelo Allan); leitura do 07 Erros e lições às 18:00 e às 21:00; 3 linhas seguidas com a mesma causa viram proposta de skill no mesmo dia.
3. JOGADAS (hipótese -> ação -> métrica -> quando trocar):
   - J1: falha não registrada se repete -> cada rotina fecha a rodada com 'falhei em algo?' e grava a linha (data | erro | causa | como evitar) -> falhas registradas pelo agente / falhas achadas pelo Allan -> trocar o gatilho do registro (fim do passo de resultado) se o Allan achar antes.
   - J2: falha de habilidade é a mais cara -> registrar também o que o agente deixou de propor ou decidiu no escuro -> linhas com causa FALTA DE HABILIDADE por semana -> Triagem transforma 3+ da mesma causa em skill nova.
   - J3: tabela de falhas sem conserto é relatório -> cada linha com ação e data (ex.: E31, E32, E34) -> % de linhas com correção aplicada em 24 h -> escalar ao Removedor de Gargalos o que passar disso.
4. LAÇO: data/habilidades/aprendizado/registro_de_falhas.md, 1 linha por rodada: data | jogada | resultado n/métrica | mantém/altera/descarta. Número ruim = troca de jogada na mesma rodada.
5. JUIZ: biblioteca/habilidades/juiz_de_qualidade.md (Juiz separado de quem produz; nota mínima 7 para ir ao vivo) (critério: a linha tem causa e correção, e a severidade foi checada; Jev só classifica severidade, nunca decide registrar).


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
- 2026-10-22 | Vigia de Rotinas | Encerrou V03/V04 ("Executor disparou 09:54Z") com a sessão ainda PENDING e sem commit; o livro seguiu com 19 linhas vencidas | causa: tratou disparo como conclusão | correção: E34 (encerrar só com SUCCEEDED + commit/arquivo; PENDING > 2 h = ALERTA)
- 2026-10-22 | Executor de Decisões | Sessões de 21/10 e 22/10 PENDING, nenhum "feito"/"ATRASADA" escrito no livro | causa provável: rodada longa sem commit parcial | correção: E32
- 2026-10-22 | Publicar Blog / Reforço do Blog (workflows) | #45 falhou "push 3x": reforço empurrou na main 3 s antes e o loop `pull --rebase && push` repetiu sobre rebase com conflito (as 3 tentativas dão o mesmo erro); issue de alerta não abre (403) | causa: retry sem abortar o rebase + dois workflows gravando na main | correção: E47
- 2026-10-22 | Diretores/Estrategista/Executor | E13, E26 e E42 (editar post já agendado) venceram sem ninguém executar: dono "sessão do Allan" não roda sozinho; 3 posts do teste CTA saíram sem a legenda | causa: ação ligada a uma sessão manual | correção: E48 (só itens não agendados; dono sempre rotina da nuvem)
- 2026-10-22 | Diretores (Produto/Estrategista) | IDs D01/D02 reusados no livro | causa: ID escolhido de memória | correção: E49 (grep do próximo ID livre)
- 2026-10-24 | Criador de Audiência | Rodada de sábado entregou só trends + 3 ideias, sem a matriz (gancho em 3 peças, pilares, prova/teste, CTA); T9 (b) falhou | causa: rodada curta tratada como exceção à matriz | correção: E109 (matriz obrigatória em toda rodada)
- 2026-10-25 | Executor | git pull --rebase estourou 2 min (branch media) | usar fetch origin main + merge --ff-only
