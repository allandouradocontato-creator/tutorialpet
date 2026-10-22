Dados até 2026-10-22 08:30 (Fortaleza) — Buffer (canal tutorialpetbr, org My organization; métricas atualizadas ~03:06), 20/09 a agora (Buffer só tem posts desde 07/10; Insights grátis = 31 dias). Anterior: 19/10. Zernio só p/ comparação (auditoria 22/10).
Estado: 35 vídeos reais publicados (+ "Teste Buffer" 0 views, ainda público), 8.225 views, alcance 6.367, 482 curtidas, 4 comentários, 15 shares, tempo médio ponderado 2,87 s. 4 agendados (22/10 10:20, 14:20, 20:20; 23/10 10:20), 0 em erro. Fila ACABA 23/10 10:20 (limite grátis 10).
## (a) Nossos números (≥72h valem: 26 vídeos, mediana 192 views; <48h = recente/parcial: 6)
| Vídeo (gancho · CTA) | Postado (idade) | Dur | Views | Curt/Com/Sh | Tempo méd. (% dur.) |
|---|---|---|---|---|---|
| Banho cachorro (pergunta de dor · artigo) | 07/10 (352h) | 44s | 1.006 | 57/0/1 | 5,3s (12%) |
| "Para de ignorar" gato enterra comida (alerta) | 13/10 (204h) | 40s | 747 | 48/0/2 | 2,9s (7%) |
| Gato/água v1 · plantas · gato/água v2 | 08-09/10 (300h+) | 38-52s | 577 · 310 · 281 | 30/1/0 · 19/1/2 · 19/0/0 | 5,6 · 5,1 · 6,8s (13-14%) |
| NOVO melhor retenção: "Cachorro aguenta quantas horas sozinho?" | 20/10 10:21 (46h, parcial) | 47s | 195 | 5/0/0 | 7,46s (16%) |
| Gato bola de pelo (20/10 20:21, 36h parcial) | | 50s | 197 | 27/1/1 | 2,1s |
| "Esse erro tá silenciosamente…" (3 vídeos) | 10/10-17/10 | 46-54s | 191 · 154 · 177 | 10/2/10 | 1,5-1,7s (3%) |
| Demais ≥72h (≈17) | 13-19/10 | 33-55s | 159-282 | 2-25 | 1,5-4,5s |
| Memes 8s (15/10, 17/10, 20/10) | | 8s | 89 · 193 · 102 | 2-11 | 1,5-2,4s (19-30% da duração) |
| Parciais 21/10: comida do gato · sofá · legumes | 22h/18h/12h | 37-42s | 178 · 195 · 126 | 7 · 19 · 11 | 1,5 · 3,1 · 1,7s |
- Piso estável 150-220 views em qualquer hora desde 14/10 (mediana 190 nos 19 vídeos de 14-19/10): sem pico, sem queda. Falta retenção e conversa (4 comentários em 35).
- Campeão (banho 1.006) tem e os outros não: pergunta de situação cotidiana específica, sem alarme, primeiros 3s sem "Para de/Esse erro", e 5+ s de tempo médio. Os 5 vídeos com ≥5 s (banho, gato/água x2, plantas, horas sozinho 7,5 s) são dúvida concreta de tutor; em 3 deles o vídeo entrega um número/limite. Os piores (1,5-1,7s) usam "Esse erro…" ou "Aquele momento em que…". n por variação <5: tendência, NÃO decisão.
- "Horas sozinho" (7,46 s, melhor tempo da conta) é o tema do Sozinho em Casa — mas a legenda e o vídeo não levam ao produto (CTA = só artigo). Sozinho em Casa no TikTok: 1 vídeo (13/10, 14 views).
- Ligação gancho/CTA (roteiro.json no branch media): todos terminam em "consulte o veterinário" + legenda "Confira o artigo completo em tutorialpet.com.br"; nenhum CTA fala do app. Ganchos: pergunta específica > alerta ("Para de…") > "Esse erro…" em tempo médio.
- Vendas atribuídas ao TikTok: sem dado (Kiwify/UTM não legíveis da nuvem; legendas sem UTM). Seguidores TikTok: sem dado no Buffer (Zernio/Allan: 19 em 20/10).
## (b) Regras — o que mudou desde 19/10 (base: biblioteca/regras_plataformas/tiktok.md, 21/10, <60 dias)
1. Link no perfil: fonte nova unil.ink (21/07/2026) diz conta Business libera "Site" clicável SEM mínimo de seguidores (pessoal exige 1.000); Stan (16/09/2026) idem; Shopify BR (03/2025) dizia 1.000. 2 de 3 fontes recentes = Business basta. Oficial (support.tiktok.com) segue ilegível (permissão negada). Ação: Allan ou o Claude da sessão confere o campo no app; se aparecer, "link no perfil" fica verdadeiro.
2. Música: Soundstripe (atualizada 16/09/2026) reconfirma: conta Business = só Commercial Music Library, licença só p/ TikTok (não reaproveitar essa trilha no Instagram/YouTube). Sem mudança de regra. audios_em_alta.yaml segue proibido no TikTok.
3. IA/conteúdo comercial: sem texto novo oficial lido; mantém rótulo IA (voz sintética + clipes) e "Divulgar conteúdo comercial" nos vídeos que citam o Sozinho em Casa. Diretrizes oficiais do TikTok seguem fora da allowlist (tiktok.com negado).
4. ManyChat no TikTok (InstantDM 25/08/2026; ManyChat 07/05/2026): só gatilho por DM recebida ("alguém manda mensagem"); NÃO há comentário→DM nativo no TikTok no Brasil; janela de resposta 48 h, ~10 msgs seguidas. Confirma a decisão de 21/10 (05 Decisões).
5. Animais/saúde: nada novo; manter "consulte o veterinário".
- Riscos nos vídeos atuais: agendado HOJE 10:20 (6ad7bf581a1ce97999a6c7b3) diz "link no perfil" (patas no inverno) — só vale se o campo Site existir; 14:20 (6ad8a1729c5d256f6598ceac) repete "Esse erro tá silenciosamente…" (gancho de pior retenção, banido em E13/E23); "Teste Buffer" público; legenda.txt de pacote antigo no branch media ainda traz "R$ 9,90" + link Kiwify NcQChat (visto em quanto-tempo-um-cachorro…; não foi ao TikTok, mas o gerador pode reaproveitar); vídeo de plantas ("pode ser fatal") no ar.
## (c) Tendências (só com fonte)
1. Vídeo > imagem: 5x views, 6x interações; Para Você = 7 em 10 views [metricool.com/pt/estudo-tiktok, 12/05/2026, mod. 23/06]. Duração: educativo 30-60s (até 60-90s com gancho forte), entretenimento 15-30s [stackinfluence.com, 10/07/2026, fonte de mercado]. Nossos dados: o campeão e os de 5+ s são 40-52s; os memes de 8s não ganharam — não encurtar por reflexo.
2. Referências 2026 (estilo_viral.yaml, 15/10): 9-17s, som original, plano único, legenda só hashtag — para pets fofos/humor; para tutorial a fonte indica o oposto. Dois públicos: humor (shares) vs dúvida (artigo). Nosso erro é misturar: tutorial com ritmo de humor.
3. Hashtags 1-5 de nicho, sem #fyp [Metricool 24/06/2026]; pergunta na legenda gera mais comentário que "curta".
## (d) Testes propostos (grátis; n≥5 por variação ou não decide; julgar só com 72h+)
T1 "Quanto tempo / normal?": 5 vídeos no molde da pergunta-limite ("Seu cachorro aguenta quantas horas sozinho?", "com quantos meses…", "de quanto em quanto banho") vs 5 "Esse erro…/Aquele momento…". Meta: tempo médio ≥5 s e ≥250 views em 72h. Hoje 5 vídeos ≥5 s de tempo médio (banho, gato/água x2, plantas, horas sozinho), todos de dúvida concreta; os 3 "Esse erro…" ficaram em 1,5-1,7 s.
T2 Série "Sozinho em Casa" (3 partes 15-20s, 1 passo cada), pergunta de dor; CTA fixo "manda SOZINHO no direct do @tutorialpetbr" (DM, não comentário). Meta: 1.500 views somadas e ≥5 DMs em 72h.
T3 Duração do mesmo roteiro: 25s vs 44s. Meta: % assistido ≥ a do original (12%).
## (e) Vendas e isca (estado real verificado em 05 Decisões/06 Pendências/fluxo_mimo_fase1.md)
Funil: pergunta de dor (tema horas-sozinho) → 1 passo → "no direct do @tutorialpetbr, mande SOZINHO e eu envio o guia grátis do seu pet" (ManyChat TikTok = só DM; conta tutorialpetbr fb5804905 JÁ tem TikTok conectado) → mimo/isca de audiência (fluxo_mimo_fase1.md, campo origem_mimo=tt_dm) → só depois (horas_sozinho ≥4) oferta Sozinho em Casa R$ 27 na landing com ?utm_source=tiktok&utm_medium=dm&utm_campaign=sozinho_serie. Comentário fixado = pergunta sem link. Meta de teste: 1ª venda real + ≥5 DMs/semana vindos do TikTok; mede: ManyChat (origem tt_dm), visitas por UTM, Kiwify. 1 vídeo em 4 cita o app (hoje 1 em 35).
Estado já resolvido (NÃO pedir): ManyChat conta única e TikTok conectado; Brevo lista criada; preço R$ 27; isca "7 Erros" descartada. Pendente de produção (não do Allan): mimo final + link do arquivo (Fable/Diretor de Audiência).
## (f) Decisão do Allan (só o que for dele)
1. Aprovar T2 (série + CTA "mande SOZINHO no direct") — nada vai ao ar no ManyChat sem o ok dele (regra 11). 2. Conferir no app (30 s, Perfil > Editar perfil) se o campo "Site" aparece com a conta Business: decide se "link no perfil" pode voltar às legendas; 3. Verificação de negócio/CNPJ NÃO é necessária se o campo aparecer (2 fontes 2026). Já pedidas antes e abertas: nenhuma nova.
