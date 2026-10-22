---
criado: 2026-10-21
---
# Habilidade: Painel Central de Achados (toda rotina de pesquisa escreve aqui)

## STATUS: RESERVA — sem contrato preenchível (data/pesquisa/painel_achados.md não existe, nenhuma rotina escreveu uma linha, sem resultado mensurável nem prova de uso; sobrepõe entrega_direta.md). Custo de crédito conhecido: nenhum; sem proposta de exclusão. Reativar só com o arquivo criado e 1 rotina escrevendo nele.


## Por que existe
Pedido do Allan (21/10/2026), ao ver que o "Diretor de Marketing e Copy" não
tinha como mostrar o que descobriu: "complicado, né? A gente tem que criar
uma organização disso aí... fazer um mapa das ideias que chegaram." O
problema de fundo: cada rotina de pesquisa escreve num Claude Doc ou arquivo
PRÓPRIO e isolado (Ferramentaria, Diretor de Marketing, Banco de
Oportunidades, Banco de Referências...) e ninguém olha todos ao mesmo
tempo — só a Triagem, 2x por semana, e mesmo assim por cima.

## A solução: um arquivo único, toda rotina escreve uma linha
`data/pesquisa/painel_achados.md` é o "mapa mental" — uma tabela só, em
ordem cronológica reversa (mais recente no topo), que TODA rotina de
pesquisa (caçadores, pesquisadores, Diretor de marketing, Curador de
Ferramentas etc.) acrescenta ao final da sua própria execução, mesmo
quando o achado já está detalhado em outro lugar (Claude Doc, YAML,
relatório próprio). Isso não substitui o lugar detalhado — é o ÍNDICE que
permite varrer tudo em 30 segundos.

Formato da linha (markdown, uma linha por execução):
`| AAAA-MM-DD HH:MM | <nome da rotina> | <achado principal em 1 frase> | <onde está o detalhe (link/arquivo)> | <acionável? sim/não> | <decisão pedida, se houver> |`

Se não houve achado novo na rodada, a rotina escreve a linha mesmo assim,
com "sem achado novo nesta rodada" no campo de achado — isso é dado
também (mostra que a rotina está viva e rodando, não só silêncio).

## Relação com as outras habilidades
- `entrega_direta.md` decide SE notifica o Allan na hora (PushNotification).
  `painel_central_achados.md` é diferente: TODA rodada escreve no painel,
  notificável ou não — o painel é o mapa completo, a notificação é só o
  que não pode esperar.
- `registro_de_falhas.md`: se uma rotina passar 3 rodadas seguidas com
  "sem achado novo" no painel, isso é o mesmo gatilho de falha de
  utilidade já descrito ali.

## Quem escreve aqui (21/10/2026)
Pesquisador de Mercado, Pesquisador de Formato (já nascem com isso),
Diretor de marketing e copy, Caçador de atalhos e automações, Curador de
Ferramentas, Pesquisador semanal de produtos — e qualquer rotina de
pesquisa futura.

## Quem lê
A Triagem de Decisões (terça/sexta) passa a abrir este arquivo PRIMEIRO,
antes de vasculhar as docs individuais — ele mesmo aponta onde está o
detalhe de cada achado forte. O Allan também pode abrir direto quando
quiser "ver tudo que chegou" sem esperar a Triagem.
