Dados até 2026-10-20 13:29 (Fortaleza)
# Vigia de Rotinas — 20/10/2026 (rodada 13:19)
Número do departamento: 9 rotinas falhando/sem disparar/suspensas hoje (meta 0). Fábrica, blog e redes OK.
Replicar o que funciona: gancho de problema concreto ("cachorro aguenta quantas horas sozinho") saiu nas 3 redes hoje sem erro; memes 8 s seguem no horário. Habilidade que falta: confirmar que as rotinas semanais disparam (reset de 13:02 sem prova ainda). Teste grátis: conferir last_fired_at em 21/10 (V01).

| Rotina/engrenagem | Estado | Último run | Problema | Correção sugerida | Idade do último resultado |
|---|---|---|---|---|---|
| Criador de Audiência (diária 08:23) | NÃO DISPAROU | 16/10 | 17–20/10 perdidos; reagendada 21/10 11:23Z | V01: conferir 21/10 | 4 dias |
| Agente de SEO, Humorista (seg/qui) | NÃO DISPAROU | 15/10 | seg 19/10 perdida; próxima qui 22/10 | V01 | 5 dias |
| Utilidade Pública (ter), Criativo de Venda (ter), Atendente (seg/qua/sex), Caçador de Oportunidades (seg) | NÃO DISPAROU | 15/10 ou nunca | slots de 19–20/10 perdidos; resetadas 13:02 | V01: recriar do prompt em config/prompts/ se seguirem mudas | nunca/5 dias |
| Cobrança, Editor de Afiliados | AGUARDA 1º DISPARO | nunca | sex 23/10 e qui 22/10 | idem | - |
| Executor de Decisões (06:53) | PENDENTE 6 h 27 | 20/10 09:54Z | status PENDING desde o disparo (possível travada) | conferir a sessão cse_01AHyJZrkWX6iVpsJRzw12Q4; se travada, disparar de novo | 6 h |
| Caçador de estilo viral | SUSPENSA (device_absent) | 15/10 | depende do PC | recriar com Zernio+Buffer e busca web | 5 dias |
| Caçador de referências de vídeo | SEM EFEITO provável | 20/10 (1,5 min) | precisa do navegador do PC | trocar por busca web | - |
| Guerrilha de Comunidade (hora a hora) | RISCO | 20/10 12:23 ok | usa Chrome do Allan; sem PC vira FALHA | ler log da próxima hora; pausar se FALHA | 1 h |
| fabrica.yml | OK | #94 20/10 11:27 verde | - | - | 2 h |
| publicar_blog.yml | OK | #26 20/10 12:55 verde | #24 vermelho às 12:18 já corrigido; 0 issues abertas | tirar saída 1 com reprovados (V02) | 0,5 h |
| Blog no ar | OK | artigo 20/10 12:18 | parado de 17/10 a 20/10 (~76 h), resolvido | - | 1 h (site ao vivo não conferido: WebFetch sem permissão; usei commit em site/build) |
| Posts FB/IG/TikTok | OK | FB 12:05, IG 11:04, TikTok 10:21 | 0 erro Zernio/Buffer; agendados 24 h: Zernio 16, Buffer 3 | - | FB/IG 1-2 h, TikTok 3 h |
| ElevenLabs | ATENÇÃO | 20/10 | 21.014 créditos (leitura das 12:24), renova 07/11 | pausar explicador se passar do ritmo | 1 h |
| Estoque de pacotes na media | NÃO CONTADO | - | clone da branch media estourou o tempo | contar na próxima rodada | - |
Windsor.ai: A01 diz reconectado; auditor de anúncios rodou às 12:57 e commitou "Windsor OK".
