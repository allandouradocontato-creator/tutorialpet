Dados até 2026-10-20 11:41 (Fortaleza) — Zernio (FB/IG) e Buffer (TikTok) ao vivo; Windsor/anúncios e Kiwify: sem dado. Repo main 4708b10 (add_repo indisponível na sessão; clone já existia).
# Revisão Estratégica de Renda — 20/10/2026 (1ª; sem revisão anterior)
## 1. Engajamento e views (teste 15–21/10; só posts ≥72h; mediana de views)
| Rede | slot 1 | slot 2 | slot 3 | Maior/menor |
|---|---|---|---|---|
| FB | 10h: 209 (n3) | 14h: 223 (n3) | 19h: 210 (n4) | 1,07x |
| IG | 11h: 48 (n3) | 15h: 35 (n3) | 20h: 62 (n4) | 1,8x |
| TikTok | 10:20: 177 (n3) | 14:20: 187 (n3) | 20:20: 184 (n4) | 1,06x |
- Regra do teste (≥5 posts e ≥1,5x): NÃO bateu. Faltam 2 posts por horário (fecha ~22–23/10). FB e TikTok: horário não muda nada; IG 1,8x mas com n<5.
- O que pesa é o formato, não a hora: meme 8s no FB (08:30 = 383; 21:00 = 254) bate explicador (~210); IG meme alcance 81–122 vs ~31–50. O slot de meme 12:00 (FB/IG) entregou 0–7 views em 4 posts: suspenso (E02). TikTok: piso 150–210, campeão banho 1.004 e "Para de ignorar" 747 (pergunta de rotina/alerta curto); "Esse erro…" o pior. Comentários: TikTok 3 em 31 posts.
- Mudanças p/ próxima rodada (máx. 3): (a) meme 8–12s em 2 de cada 3 vídeos novos [medir: mediana FB >250 e IG >60 em 3 dias]; (b) trocar "Esse erro…" por pergunta de situação do dia a dia [medir: ≥250 views em 2 de 3 posts]; (c) fechar cada vídeo com pergunta de resposta fácil (ex. "Qual cara o seu fez?" = 383 no FB) [medir: ≥1 comentário a cada 4 posts].
## 2. Otimizador e processo
- Parado >7 dias: recriar Caçador de estilo viral/Agente de Segurança (proposto 16/10; D05/D06 "decidido", prazo hoje, sem evidência) e chave ElevenLabs (401 desde 19/10; saldo ilegível, renova 07/11).
- Mais grave: 3 artigos aprovados em 404 há ~30h (3ª vez em 7 dias: 13/10, 16/10, 20/10); um reprovado derruba o lote do publicar_blog e trava o Agendador. Coerência visual desligada (sem GEMINI_API_KEY).
- Ciclo: fábrica ~0,19h por rodada (#92); ciclo de produto novo ainda não medido. Tarefas burocráticas devolvidas ao Allan: 0 (só login/identidade).
## 3. Departamentos e renda
| Depto | Agente | Estado | Número |
|---|---|---|---|
| Produto | Fábrica de Produtos (qua) | ainda sem 1ª rodada | vendas Sozinho em Casa R$9,90: sem dado; Kiwify duplicado 3JprCCK |
| Blog/AdSense | publicar_blog | FALHOU 19/10 | 3 artigos em 404; AdSense aguardando Google; ads.txt sem ID real: R$ sem dado |
| Redes e vídeo | Agendador/Estrategista | rodou | FB 7 seguidores, IG 0; mediana FB 215, TT ~185, IG ~50 views |
| Funil/landing | Criativo de Venda (ter) | sem registro de rodada | cliques FB: 4 no total; TikTok Sozinho em Casa 14 views, sem UTM |
| Afiliados | Editor de Afiliados (qui) | ainda sem 1ª rodada | 1 link Shopee (R$79,99); plano 14/10 sem ofertas (falta chave Shopee); cliques: sem dado |
| Anúncios | Auditor de Anúncios | CEGO (Windsor.ai a reconectar) | custo: sem dado; 64 campanhas a limpar |
- Sem caminho até o dinheiro: Anúncios (cego, gasto desconhecido) e Afiliados (tema com 67 pts no plano, mas zero link nos artigos). Fazer: Allan reconecta Windsor e cria chave Shopee; Editor de Afiliados (qui 22/10) coloca link com sub_id nos artigos.
## 4. Oportunidades de renda
- Sem dado: data/oportunidades/semana.md não existe e a fila decisoes.md está vazia; o Caçador (seg 19/10) não registrou rodada. Nada a priorizar.
## 5. Riscos e gasto
- Posts em erro: 0 (Zernio e Buffer). Estoque TikTok ~1 dia (agendado até 21/10 10:20); FB/IG até 25/10 (memes).
- Rotinas sem registro de disparo desde 16/10 apesar de agendadas: Vigia (diária), Criador de Audiência (diária), Humorista, Utilidade Pública, SEO, Cobrança, Atendente de Comentários, Auditor de Anúncios, Caçador de Oportunidades, Criativo de Venda. Prevenção: Executor confere last_fired amanhã e recria as que não dispararem. (Lista parcial: 1 página de rotinas não lida.)
- Windsor.ai precisa de login (anúncios cegos desde 15/10). Rotinas ainda citam Metricool/Windsor. Caçador de referências depende do PC: pausar (proposta do Otimizador).
- Créditos: ElevenLabs ~648/rodada, saldo desconhecido. Vídeos no ar: "pode ser fatal" (plantas); "Teste Buffer" público.
## Decisões do Allan
1. Destravar logins (2 min, R$0): reconectar Windsor.ai, chave ElevenLabs com user_read, SHOPEE_APP_ID/SECRET. Motivo: anúncios cegos e afiliados sem chave são os dois elos sem caminho até o dinheiro.
2. OK para blindar o publicar_blog (gravar os aprovados mesmo com reprovado) + passar GEMINI_API_KEY (R$0). Motivo: 3 casos em 7 dias, Agendador travado.
3. OK para a mini-série Sozinho em Casa no TikTok (T2) com UTM tiktok, R$0 + créditos de voz. Motivo: único vídeo com caminho a venda; hoje 14 views.
## Em curso, sem precisar dele
- E01–E05 do Estrategista (memes, slots, legendas TikTok); teste de horário fecha ~22/10; veredito das 7 mudanças e molde em 23/10; Editor de Afiliados qui 22/10; Executor diário.
