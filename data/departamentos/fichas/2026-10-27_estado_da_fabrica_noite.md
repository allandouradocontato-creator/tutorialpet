# FICHA — Estado da fábrica 27/10 21:42 (Diretor de Operação e Qualidade)
- Departamento / Diretor / data-hora: Operação e Qualidade / 2026-10-27 21:42 (Fortaleza)
- Assunto e objetivo: tirar a fábrica do vermelho (blog parado ~27 h, vídeo parado) sem devolver etapa manual ao Allan.
- Pareceres: Vigia (27/10 19:19Z SUCCEEDED, V17-V19 abertas, não redisparou por cota/saldo), Executor (27/10 06:53 SUCCEEDED), Diretores Audiência 27/10 ok, Produto 27/10 ok, Conteúdo 26/10 ok (próx 29/10). sem parecer do Medidor (rotina não aparece em list_triggers ativas) e sem parecer do Otimizador.
- Divergências: nenhuma.
- DECISÃO: ALERTA.
  1. Publicar Blog: #60, #61, #62 failure (27/10 09:58Z, 10:21Z, 14:29Z); último success #59 (26/10 18:22Z), sem success depois. Causa registrada pelo Vigia: Gemini 429/503 na capa + quality_editor reprovando.
  2. Anti-gap 24 h: 0 artigo novo no ar nas últimas 24 h (nenhum .html novo em site/build desde 26/10 ~21:00Z; último commit "blog: publica artigo" de 27/10 10:04Z só trouxe vídeo). Home responde 200. Linha E em execucao.md + cobrança ao Diretor de Conteúdo e Blog.
  3. Fábrica: #162-#171 failure (a partir de 27/10 11:22Z, #161 manual foi o último success): preflight de voz (ElevenLabs ~306 créditos, vídeo precisa ~748) + Gemini 429. Sem pacote de vídeo novo desde ~27/10 10:40Z; estoque ~2 dias já declarado pelo Agendador.
  4. Rotinas (list_triggers, 2 páginas, 19 ativas): 0 FAILED; só esta rodada PENDING. Segurança roda 28/10 08:23 (ok). Medidor 21:11 não consta entre as ativas.
- Livro: 14 atrasadas (mesmas). V17, V18, V19 abertas, prazo 28/10.
- Ações: E131 (cobrança ao Executor: V17/V18/V19 em código, sem voz), E132 (cobrança ao Diretor de Conteúdo e Blog: 0 artigos em 24 h), E133 (Medidor ausente: confirmar rotina).
- Pedido ao Allan (dinheiro, único): ElevenLabs sem créditos até 07/11 -> (a) recarregar/subir plano ou (b) autorizar vídeos curtos <=12 s. Já consta em V19; sem outro pedido.
- Status: aprovada pelo Diretor
