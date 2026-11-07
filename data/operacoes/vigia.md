Dados até 2026-11-07 07:30 (Fortaleza) | CORRIGI: 2 | PRECISO DO ALLAN: 0
Número do dia: rotinas falhando/suspensas = 0 (de 18 ativas; 11 desligadas por decisão de 22/10 e 02/11).
| rotina | estado | último run | problema | correção |
|---|---|---|---|---|
| 17 rotinas ativas (Diária 1+1, Diretores, Operador, Agendador, Medidor, Auditor, Estrategista, Segurança, reservas) | ok | todas SUCCEEDED, nenhuma com next_run vencido | - | - |
| Vigia (esta rodada) | rodando | 07:19 | - | - |
| fabrica.yml | verde, mas cron das 06:00 não disparou hoje (último verde 06/11 13:53 F, 17 h) | 06/11 16:53Z | blog 0/1 hoje às 07:30 | dispatch REST feito 07:21 F, run 42363579635 |
| publicar_blog.yml | verde | 06/11 17:33Z | - | - |
| Blog | 0/1 hoje (ontem 2/1); AdSense 0 FALHA, 121 artigos | último artigo no ar 06/11 14:41 F | piso do dia ainda aberto | promovido 'devolver-um-animal-adotado...' em blog_aprovados.txt (push dispara publicar_blog) |
| FB/IG (Zernio) | ok | 06/11 11:01 F | 8 falhas antigas de mídia (sem novas); 10 agendados | retry proibido (E151) |
| TikTok (Buffer) | ALERTA V2.3 | 06/11 10:21 F | 1 vídeo em 24 h; hoje só fujão 10:20 F; atum 08/11 com erro (E200) | fire_trigger do Operador negado 3x (E210); Operador roda sozinho 07:41 F e a ficha E211 manda completar os 3 vídeos; conferir 11:19 |
| Issues falhou/nao publicou | 21 abertas, última 02/11 | - | histórico | fechar na revisão |
Créditos ElevenLabs: sem saída recente do workflow (não medido).
