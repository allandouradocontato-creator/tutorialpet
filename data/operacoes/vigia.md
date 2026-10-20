Dados até 2026-10-20 19:25 (Fortaleza)
# Vigia de Rotinas — 20/10/2026 (rodada 19:19)
Número do departamento: 9 rotinas falhando/sem disparar/suspensas hoje (meta 0). Fábrica, blog e redes OK; o problema é só nas rotinas semanais e no Executor.
Replicar o que funciona: gancho de problema concreto (ração gato/cachorro, bola de pelo) saiu em FB e IG hoje sem erro; fábrica verde 6 de 6 (#93–#98). Habilidade que falta: garantir que rotina recriada dispare no 1º slot. Teste grátis: fire_trigger de 1 rotina muda e ver se roda (V03).

| Rotina/engrenagem | Estado | Último run | Problema | Correção sugerida | Idade do último resultado |
|---|---|---|---|---|---|
| Executor de Decisões (06:53) | TRAVADO | disparou 20/10 09:54Z, ainda PENDING | 12 h 30 sem concluir (era 6 h na rodada das 13:19); V01–V03 e E12–E13 dependem dele | fire_trigger de novo e conferir sessão cse_01AHyJZrkWX6iVpsJRzw12Q4 | 12,5 h |
| Criador de Audiência (diária 08:23) | NÃO DISPAROU | 16/10 | 17–20/10 perdidos; próximo 21/10 08:23 | V01 | 4 dias |
| Agente de SEO, Humorista (seg/qui) | NÃO DISPAROU | 15/10 | seg 19/10 perdida; próxima qui 22/10 | V01 | 5 dias |
| Utilidade Pública, Criativo de Venda (ter) | NÃO DISPAROU | 15/10 / nunca | ter 20/10 perdida; próxima 27/10 | V01: recriar do prompt se seguirem mudas | 5 dias / nunca |
| Atendente (seg/qua/sex), Caçador de Oportunidades (seg) | NÃO DISPAROU | nunca | slots de 19/10 perdidos; Atendente próxima qua 21/10 | V01 | nunca |
| Cobrança (sex), Editor de Afiliados (qui) | AGUARDA 1º DISPARO | nunca | 22 e 23/10 | idem | - |
| Caçador de estilo viral | SUSPENSA (device_absent) | 15/10 | depende do PC do Allan | recriar com Zernio+Buffer e busca web | 5 dias |
| Caçador de referências de vídeo | SEM EFEITO provável | 20/10 (1,5 min) | precisa do navegador do PC | trocar por busca web | - |
| Guerrilha de Comunidade (hora a hora) | OK | 20/10 18:45 (log), run 21:23Z ok | usa Chrome do Allan; sem PC vira FALHA | ler log na próxima hora | 1 h |
| fabrica.yml | OK | #98 20/10 17:48 verde | - | - | 1,5 h |
| publicar_blog.yml | OK | #26 20/10 12:55 verde | #24 vermelho já corrigido; 0 issues abertas | tirar saída 1 com reprovados (V02) | 6,5 h |
| Blog no ar | OK | commit "blog: publica artigo" 20/10 12:18 | limite 30 h respeitado; site ao vivo não conferido (WebFetch sem permissão) | - | 7 h |
| Posts FB/IG/TikTok | OK | FB 19:05, IG 15:03, TikTok 17:10 | 0 erro Zernio/Buffer; agendados: Zernio 20, Buffer 5 (próx. 20:20) | - | FB 0,3 h, IG 4 h, TikTok 2 h |
| ElevenLabs | ATENÇÃO | leitura 12:24: 21.014 créditos | renova 07/11; run de 13:51 sem leitura nova nesta rodada | pausar explicador se passar do ritmo | 7 h |
| Estoque de pacotes na media | NÃO CONTADO | - | clone da media falhou por tempo de novo | contar via API na próxima rodada | - |
Windsor.ai: auditor de anúncios rodou 07:55 (run ok).
