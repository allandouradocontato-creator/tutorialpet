Dados até 2026-10-22 07:30 (Fortaleza)
# Vigia de Rotinas — 22/10/2026 (rodada 07:19)
Número do departamento: 3 rotinas falhando (Medidor, Guerrilha, Diretor de Operação: USAGE_LIMIT_REACHED na noite de 21/10, 00:12–00:41Z). Meta zero: não atingida.
Já funciona e replicar: fábrica verde (#105, 21/10 20:50Z); FB/IG/TikTok postaram nas últimas 11 h; 0 erro Zernio/Buffer; 0 issue aberta; Estrategista, Publicador e Executor disparam hoje. Replicar = mais do mesmo. Habilidade que falta: tolerar limite de uso (rotina nova some sem aviso). Teste grátis: fire_trigger do Medidor e do Diretor de Operação após o reset e conferir SUCCEEDED.

| Rotina/engrenagem | Estado | Último run | Problema | Correção sugerida | Idade do último resultado |
|---|---|---|---|---|---|
| Medidor de Testes (21:11) | ALERTA | 22/10 00:12Z FALHOU | USAGE_LIMIT_REACHED; 1º disparo perdido | V05: fire_trigger após reset; teste de 72 h (E18) fica sem leitura | nunca rodou |
| Diretor de Operação (21:41) | ALERTA | 22/10 00:41Z FALHOU | USAGE_LIMIT_REACHED; 1º disparo perdido | V05: idem | nunca rodou |
| Guerrilha (hora a hora) | ALERTA | 22/10 00:23Z FALHOU | USAGE_LIMIT_REACHED; balanço diário das 21:23 não saiu; depende do Chrome do Allan | próximo disparo 11:23Z; conferir SUCCEEDED | 10 h |
| Executor de Decisões (06:53) | OK | 22/10 09:54Z PENDING (25 min) | V03/V04 resolvidos: disparo de hoje em curso | confirmar SUCCEEDED na próxima rodada | em curso |
| Demais 25 rotinas (Criador, Humorista, SEO, Utilidade, Criativo, Segurança, Estrategista, Conferente, Agendador, Publicador, Atendente, Auditor, Caçadores, Diretores, etc.) | OK | SUCCEEDED / dentro do prazo | 0 vencida sem disparar, 0 suspensa, 0 desligada | - | < 24 h |
| Diretores Conteúdo/Produto/Audiência, Pesq. Formato/Mercado, Cobrança, Afiliados | AGUARDAM 1º DISPARO | nunca | próximos: Audiência 12:17Z, Conteúdo 14:37Z | acompanhar | - |
| fabrica.yml | OK | #105 21/10 20:50Z verde (6/6 verdes) | - | - | 13,5 h (limite 30 h) |
| publicar_blog.yml | OK | #29 21/10 12:53Z verde | #27/#28 falharam 21/10, #29 passou | monitorar reincidência | 21 h |
| Blog no ar | OK | commit site/build 21/10 14:25Z | home ao vivo não lida (WebFetch sem permissão) | liberar tutorialpet.com.br | 20 h (limite 30 h) |
| Posts FB/IG/TikTok | OK | FB 21/10 23:33Z, IG 22/10 00:03Z, TikTok 21/10 23:21Z | 0 erro; agendados: TikTok 4 (próx. 13:20Z), Zernio 28 | E25: fila TikTok acaba 23/10 10:20 | FB 10,8 h, IG 10,3 h, TikTok 11 h |
| ElevenLabs | OK? | creditos_eleven #7 20/10 13:51Z | sem saída nova; última leitura 21.014 de 39.419 (renova 07/11) | rodar creditos_eleven.yml | 44 h |
| Estoque media (64 pacotes) | OK | 28 agendado, 1 parcial, 7 aprovado, 17 extra_pronto, 11 aguardando_revisao | igual a ontem; 7 aprovados sem post | Conferente cuida | hoje |
