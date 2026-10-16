Dados até 2026-10-16 07:20 (Fortaleza)
# Vigia de Rotinas — 16/10/2026
Número do departamento: 4 rotinas/processos com problema hoje (meta 0): 1 suspensa, 2 sem conector, 1 workflow atrasado.
Replicar o que funciona: gancho de problema concreto em pergunta (banho de cachorro, 988 views no TikTok, nota 05/15-10) — mais do mesmo, mais rápido. Habilidade que falta: ler anúncios (Windsor caiu); teste grátis = reconectar o Windsor.

| Rotina | Estado | Último run | Problema | Correção sugerida |
|---|---|---|---|---|
| Caçador de referências de vídeo | SUSPENSA (device_absent) | 13/10 | precisa do navegador do PC do Allan; suspensa hoje 07:20 | ligar o PC/app desktop e reativar, ou trocar por busca web |
| Auditor diário de anúncios | cega | 15/10 10:56 (18 s) | Windsor.ai pede reconexão; run de 18 s sugere sem dados | Allan reconecta o Windsor |
| Auditor de Anúncios (seg/qui) | cega | nunca rodou | mesmo Windsor | idem |
| Workflow fabrica.yml | ATRASADO | #64 em 15/10 20:30Z | cron 09:00Z e reserva 09:37Z de hoje não rodaram (como em 10/10); próximas 13:00/13:37Z | se não rodar até 13:40Z, disparar via config/fabrica_disparo.txt |
| Caçador de estilo viral | enabled, degradada | 15/10 | usa navegador/Chrome do PC e métricas do Metricool (fora); sem Zernio/Buffer | recriar com Zernio+Buffer; passo navegador depende do PC |
| Diretor de marketing, Segurança, Triagem | enabled, parcial | 13-14/10 | prompts citam Metricool (fora) | ajustar prompts quando der |
| Demais ~28 rotinas ativas | OK | último run SUCCEEDED, next_run futuro | — | — |

Posts em erro: Zernio sem falhas; Buffer sem erro; 22 agendados no Zernio (FB+IG).
GitHub Actions: fabrica #55 e #57 falharam em 15/10 01:xx UTC (pilar saude_basica já corrigido; #57 gerou pacote mas abriu issue #6, ainda aberta); #56 e #58-#64 OK. publicar_blog: 6 últimas OK.
Obs.: add_repo indisponível nesta rotina; repo já estava clonado (main 6f0f165).
