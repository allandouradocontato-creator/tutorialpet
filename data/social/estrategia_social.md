Dados até 2026-10-20 10:15 (Fortaleza) — Zernio (FB, IG) e Buffer (TikTok), 20/09 a agora. 7ª edição (anterior 16/10).
## 0. Erros e estado (topo)
- Erros de publicação: nenhum (Zernio posts_list_failed vazio; Buffer sem post em error).
- ALERTA NOVO: slot de meme do meio-dia falha. FB 12:00 (17, 18 e 19/10): 7, 0 e 0 views; IG 13:00: 131, 0 e 0. Os outros 5 slots do FB têm 206-383 (mediana). Status "published", mas Meta não entregou. Verificar os 3 vídeos na página (formato/arquivo?) antes de repetir o slot.
- Agendados: Zernio 19 (9 FB + 10 IG; ids no plano); Buffer TikTok 4: 20/10 17:10 (meme), 20:20 (bolas de pelo, 50s), 21/10 10:20 (comida cão+gato). A de 20/10 10:20 já saiu (cachorro sozinho, 48s).
- Regra (a)/(d): legendas TikTok de "cachorro sozinho" (publicada) e "bolas de pelo" (agendada 20:20) ainda dizem "link no perfil".
## 1. Nossos números (17-20/10; posts <24h = parcial)
| Rede | Posts | Resultado | Retenção |
|---|---|---|---|
| FB | 18 | views mediana 215 (0-559); 24 reações, 9 com. (todos nossos), 4 cliques | tempo médio 2,6-5,2 s (meme 8s e explicador iguais) |
| IG | 17 | alcance mediana 46 (0-106); 7 curtidas, 9 com. (nossos), 0 salvos, 0 shares | skip 44-100% |
| TikTok | 6 (18-19/10) | views 90-219; 3-25 curtidas; 0 shares, 0 com. | tempo médio 1,4-4,3 s de 36-50 s |
- FORMATO (achado forte, n=17 IG): IG meme 8s: alcance mediana 86, skip 55%, tempo médio 4,3 s; IG explicador 34-55s: alcance 31, skip 76%. FB 8s nos slots 08:30 e 21:00: 383 e 254 de mediana vs 206-216 nos explicadores de 10/14/19h. Melhor FB: meme "Seu gato também cobra presença" 559.
- TikTok: nenhum 8s no período (último: 72-192 views). Explicadores longos: piso 90-219, tempo médio 1,4-4,3 s (3-9% do vídeo), 0 shares nos 6.
- Por tema (gato x cachorro): sem separação; amostra pequena, sem causa. Cliques: FB 4 no total; vendas Sozinho em Casa: sem dado.
## 2. Gatilho de mudança (regra_mudanca_rapida.md): DISPAROU
- FB tempo médio <6 s: 15 de 18 posts. IG skip >70%: 8 de 9 explicadores. TikTok tempo médio <4 s: 5 de 6 e 0 shares em 6 (limite 1 a cada 4). Mediana abaixo da meta: FB 215 (<250), IG 46 (<50), TikTok ~190 (<350).
- Plano: data/social/plano_de_mudanca_2026-10-20.md; ações E01-E05 em data/decisoes/execucao.md.
## 3. Horários (Fortaleza)
| Rede | Melhor 1 | Melhor 2 | Nota |
|---|---|---|---|
| FB | 08:30 (383) | 21:00 (254); 10:00/19:00 ~210 | 12:00 suspenso |
| IG | 08:40 (alcance ~85) | 21:10 (~85-105) | 13:00 suspenso; 11:00/20:00 ~35-55 |
| TikTok | 10:20 | 20:20 | sem dado novo; 17:10 só meme |
- Os melhores slots são os dos MEMES de 8s, então formato e horário se misturam: não afirmar horário como causa. Zernio best_time (UTC): 1-4 posts por slot, inconclusivo. Grade igual para todos os dias da semana (amostra não separa dias). Nunca duas redes no mesmo horário (conferido nos publicados).
## 4. Hashtags e legenda
- Quantidade: IG 3-5, TikTok 3-5, FB 0-3 [metricool.com/how-many-hashtags-to-use, 29/06/2026]. Sem fonte aberta nova para páginas pet BR; busca de 20/10 só trouxe guias genéricos. Conjuntos e 3 modelos por rede: config/estrategia_social.yaml (sem mudança).
- Legenda: gancho de 1ª linha em pergunta sobre o bicho; CTA fixo "Confira o artigo completo em tutorialpet.com.br"; nunca "link no perfil".
## 5. Interação e isca digital
- Comentário de terceiro: 0 em 41 posts FB/IG/TikTok desde 17/10 (os 18 comentários são nossos). Perguntas por tema no YAML; priorizar pergunta de escolha de 1 palavra ("gato ou cachorro?", "Sim ou não?").
- Isca (regras Meta/TikTok e LGPD como em 16/10): sem comentário orgânico não há o que automatizar; adiar.
## 6. Painel (metas 2 semanas, hipóteses)
- FB: tempo médio ≥40% da duração; views mediana ≥250; comentários de terceiros ≥1/sem. IG: skip ≤55%; alcance mediana ≥50; salvos+shares ≥1/sem. TikTok: tempo médio ≥50% da duração; shares ≥1 a cada 2 posts; views mediana ≥350.
- Trocar gancho/formato/CTA: 3 posts com gatilho em 24-48h (regra_mudanca_rapida.md); amostra pequena não afirma causa.
## 7. Decisões do Allan (máx. 3)
1. Trocar na fila 7 explicadores longos já agendados (ids no plano): 5 FB/IG (bolas de pelo, ração cão x gato, cachorro sozinho) e 2 TikTok (20/10 20:20 "bolas de pelo" com link no perfil; 21/10 10:20 comida cão+gato). Recomendo sim: retenção 3x pior que o meme. Só você mexe em agendado.
2. Dizer quantos seguidores FB/IG/TikTok têm (pendente desde 16/10).
3. Verificar na página do FB os 3 vídeos de 12:00 (7, 0, 0 views): se estiverem quebrados, apagar (post publicado = só você).
## 8. Sem dado
Seguidores, % assistido FB/IG, horários dos agendados FB/IG, vendas Sozinho em Casa, regras oficiais Meta/TikTok (só fontes secundárias).
