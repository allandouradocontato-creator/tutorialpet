# Registro de mudanças do Otimizador (Revisor do Processo)
Regra: toda mudança aprovada entra aqui com base de hoje, métrica de sucesso, data do veredito e regra de decisão. O Otimizador revisa na sexta e escreve MANTER / AJUSTAR / DESFAZER. Foco do Allan (16/10): engajamento, audiência e agilidade do processo (não venda direta; sem anúncios).

| # | Mudança (aprovada 16/10) | Base de hoje | Sucesso | Veredito |
|---|---|---|---|---|
| 1 | publicar_blog: push com --autostash + 3 tentativas + erro claro | 3 artigos em 404 (push falhou) | 0 artigos aprovados em 404 | 23/10 |
| 2 | Gancho curto (25–35 s) de humor no TikTok, 1 variável por vez | TikTok 72–202 views, tempo médio 2,1–2,8 s | tempo médio >4 s e >150 views, 5 posts | 23/10 |
| 3 | Pular vídeo novo com ≥5 dias de pacotes prontos; usar 9 memes | ~711 créditos/rodada | rodadas de produção -50% sem buraco | 23/10 |
| 4 | Instagram: reels curtos 7 dias; se pulo >70%, 1 post/dia | IG 11% das views do FB, pulo 68–90% | pulo <60% ou corte para 1/dia | 23/10 |
| 5 | Mais humor no Facebook (semana de teste) | reações 1–6 (tutorial) x 16 (meme, 18 h) | mediana de reações do humor >2x a do tutorial | 23/10 |
| 6 | Audiência: seguidores, comentários e compartilhamentos por rede como números principais (Zernio follower-stats, Buffer) | seguidores sem leitura nesta rodada | série semanal registrada | 23/10 |
| 7 | Agilidade: tempo de ciclo registrado em ciclo.csv | ver ciclo.csv | cada etapa com horas; meta -50% no próximo produto | 23/10 |

## Execuções do Otimizador
- 2026-10-19 | requirements.txt do app sozinho-em-casa-app fixado (streamlit==1.66.0, pillow==12.3.0; antes >=) após smoke test AppTest sem exceção | sucesso: deploy do Streamlit sem quebra; conferir o app ao vivo | veredito 23/10.
- 2026-10-20 | Leitura intermediária (veredito oficial 23/10): #1 publicar_blog autostash: push ok, mas surgiu nova causa de 404 (lote com reprovado, #23) → AJUSTAR (if: always() + limpar lista). #3 pular vídeo com estoque ≥5 dias: Allan trocou por reserva curta de 2 dias; rodadas de produção seguem (#88, #92). #2/#4/#5: amostra pequena (TikTok mediana 176–190, IG skip 44–92%, FB reações 141/69 posts); sem base para MANTER/DESFAZER ainda. #6 audiência registrada (FB 7, IG 0). #7 ciclo.csv atualizado.
