# Gargalos — semana 2026-10-23 (Removedor de Gargalos, 1ª rodada, funil em data/auditoria/funil.csv)
- Gargalo nº 1: pacote em aguardando_revisao (4 parados, mais antigo 195 h; 3 reais de 142-168 h, Guardião=revisar, sem aprovado_por). Causa (d/rotina): ninguém dono de revisar e promover; Vigia promove só 2/3 por rodada.
- Feito: funil medido (8 etapas, 1 não medida), curl 404 em comedouro-duplo e xixi-tapete, 200 nos outros 10 aprovados; ficha E56 (dono Vigia/Conferente, 24/10); régua 7: juiz_de_qualidade e audiencia_ganchos_e_cadencia saíram de rascunho.
- Não feito de propósito: promover slugs a blog_aprovados (dispara publicar_blog = publicar).
- Estoque: Zernio até 25/10 23:00Z (~2,4 d), Buffer TikTok até 25/10 23:20Z (~2,5 d); sem post em erro. Próximos: (2) estoque de posts no limite de 2 d; (3) 4 rascunhos reprovados (V07 e 3 sem reescrita).

Dados até 2026-10-20 10:55 (Fortaleza) — Zernio (FB/IG), Buffer (TikTok), Actions (logs reais), manifest da media, 14 rotinas, código do blog e do app lidos agora. Site ao vivo NÃO aberto (WebFetch recusado): HTTP dos artigos conferido só pelo build na main.
# Auditoria semanal — 2026-10-20 (Otimizador de Processo)

## ALERTAS
- 3 ARTIGOS APROVADOS EM 404 HÁ ~26 h: publicar_blog #23 (19/10 11:01Z) FALHOU. O quality_editor reprovou 3 de 6 slugs (guia-peitoral, rampa-pet, sinais-envelhecimento), o script saiu com código 1 e o passo "Gravar na main" nunca rodou: gato-parar-de-arranhar-sofa, patas-no-inverno e legumes-cozidos foram construídos e jogados fora com o runner (não existem em site/build da main). O disparo do Agendador de 08:20 já cita "4 pacotes prontos aguardando artigo 404". 3ª vez em 7 dias (13/10, 16/10, 20/10), causa nova: um reprovado derruba o lote inteiro.
- Os mesmos 3 reprovados voltam a cada dia à lista blog_aprovados.txt (retirados 17, 18 e 19/10): ciclo sem fim.
- Coerência visual DESLIGADA nas nuvens: "GEMINI_API_KEY ausente" no publicar_blog (6 capas "ok - não verificada") e no Guardião do pacote de hoje (espécie "não verificada"). O erro de raça errada de 15/10 pode voltar sem aviso. O publicar_blog.yml não repassa a chave ao passo (env só tem SLUG/INDICE).
- Saldo ElevenLabs segue ilegível: 2 execuções hoje (13:27 e 13:40Z) do creditos_eleven.yml deram 401 "Invalid API key" (19/10 era missing_permissions). Fábrica gastou ~648 créditos hoje (#92).
- Erros de publicação: nenhum (Zernio posts_list_failed vazio; Buffer sem status error). Issues #5 e #6 (15/10) seguem abertas, já resolvidas.

## Rodadas (log real)
fabrica.yml #88–#92 todas verdes (#88 13 min; #89–#91 só a trava de 2 h, 8 s; #92 disparo do Agendador 08:20: 11 min 35 s, produziu "segundo-gato", aprovado pelo Guardião, sem avisos de erro). publicar_blog #19–#23: falharam #19, #21 e #23 (log do #23 lido: reprovação de slug); ok #20 e #22. lote.yml: sem rodada desde 08/10 (6/6 ok). Custo: ~648 créditos ElevenLabs por rodada que produz; saldo desconhecido, renova 07/11.

## Posts × rede (20/09→agora; ≥72h salvo nota)
- Facebook: 69 posts, 11.237 views (51 posts ≥72h: 8.231); 141 reações, 36 comentários, 0 compartilhamentos; últimos 6 dias 150–560 views/post, mediana ~215, estável. Seguidores 7 (+2 em 7 dias).
- Instagram: 45 posts, 2.126 views (19% do FB; ≥72h: 1.141 em 27 posts); skip 44–92%; 29 comentários, 1 compartilhamento; seguidores 0 (44 mídias).
- TikTok (Buffer, 07/10→agora): 30 posts, 7.068 views, 406 reações, 3 comentários, 12 compartilhamentos; ≥72h: 20 posts, mediana 190 views; 13–17/10 mediana 182; 18–20/10 mediana 176 (parciais). Campeões: banho 1.004, "Para de ignorar" 747, gato/água 577. Buffer não devolve tempo médio/% assistido neste endpoint.
- Melhores recentes: TikTok 15/10 13:21 (207 views, 12% engaj.), 16/10 13:21 (159 views, 6 compartilhamentos), 18/10 13:21 (219 views, 25 reações). Facebook 17/10 11:31 "banheiro" 560 views (outlier). Parciais (<48h): ignorar. Sem sinal de que gancho de pergunta vença o meme: amostra pequena.
- Agendados: Zernio 19 (FB+IG) até 25/10, a maior parte memes (1/dia); Buffer 3 TikToks até 21/10 10:20 (≈1 dia).

## 3 maiores gargalos (causa raiz)
1. Publicação do blog é tudo-ou-nada: qualquer slug reprovado faz sair 1 e pula o commit dos bons; e o Conferente reintroduz os reprovados. Resultado: pacote aprovado sem artigo = Agendador travado.
2. Controles cegos que mostram "verde": coerência visual sem chave Gemini, saldo ElevenLabs ilegível, site ao vivo nunca aberto. A rodada passa, mas ninguém prova o resultado.
3. Audiência não cresce: FB 7 seguidores, IG 0, TikTok sem leitura de seguidores na API; 3 comentários em 30 TikToks. Retenção baixa e conteúdo sem convite à resposta; o canal de entrada do produto continua vazio.

## Como ficar mais rápido e gastar menos (máx. 3)
1. Blindar o lote: publicar_blog commita os aprovados mesmo se algum reprovar (`if: always()` no passo de gravar, ou sair 0 quando publicou ≥1) e remove os reprovados da lista. Custo R$ 0. Ganho: fim do 404 por lote (3 casos/7 dias, ~26 h parado agora). Teste: workflow_dispatch com os 3 slugs de hoje e conferir 200. Veredito: fazer hoje.
2. Religar a coerência visual: passar GEMINI_API_KEY (secret que a fábrica já usa) ao passo do publicar_blog e ao Guardião. Custo R$ 0 (cota gratuita). Ganho: bloqueia raça errada antes do ar. Teste: log deve mostrar "coerência verificada". Veredito: fazer esta semana.
3. Economia: pausar o Caçador de referências (depende do PC, 1,5 min sem efeito) e tirar Windsor/Metricool dos conectores das rotinas. Custo R$ 0. Ganho: tokens e ruído. Veredito: aprovar.

## Comprar x produzir / Ferramentas
Nada a assinar (Buffer grátis cobre ~3 dias de TikTok com 10 na fila; Zernio ok). Dispensar: Metricool e Windsor. PLR/produto pronto: reavaliar 24/10 com o molde.

## Tarefas manuais devolvidas ao Allan
0 por falha de processo nesta rodada. Só identidade/login: recriar chave ElevenLabs (user_read) e conferir qual secret o creditos_eleven.yml usa, 2FA, verificação TikTok.
