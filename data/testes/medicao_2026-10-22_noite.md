Dados até 2026-10-22 21:12 (Fortaleza) — Zernio (FB/IG, sync 22/10 18:35), Buffer (TikTok; métricas atualizadas só até 22/10 03:06, defasadas), Chrome do Allan (Kiwify, Brevo, ManyChat; list_connected_browsers = 1 Chrome Windows conectado). Rodada 3 (baseline 21/10 14:40). Complementa medicao_2026-10-22.md (11:40).

## Quem entra na conta
Grupo "pós-skills" = publicado depois de 21/10 14:40 (17:40Z) com idade >= 24 h (publicado até 22/10 21:12). n FB = 2 (21/10 20:29 cartão "Erro 1"; 21/10 23:33 "legumes"). n IG = 3 (21/10 15:03 "sofá"; 21/10 17:30 cartão "Erro 1"; 21/10 21:03 "legumes"; o cartão conta: não é falha técnica). n TikTok = 1 (21/10 20:21 "legumes"). Falha técnica: nenhuma (posts_list_failed e Buffer error vazios). Parciais (<24 h, só informação): FB 22/10 "gato novo" 120 views, "escova" 216 views; IG "gato novo" 8 alcance, "escova" 15, "ciência" 30; TikTok 22/10 10:20 "patas" (com "link no perfil", E26 não aplicado) e 14:20 "ração": métrica Buffer ainda 0, defasada.

## Tabela
| teste | antes (baseline) | hoje | n | meta | gatilho | veredito parcial |
|---|---|---|---|---|---|---|
| T1 FB views mediana | 218 | sem mediana (215 no vídeo; cartão 0) | 2 | >=280 | <200 | NEUTRO: amostra insuficiente |
| T2 FB tempo médio | 4,0 s | sem mediana (legumes 3,1 s; cartão 0) | 2 | >=6 s | <4 s | NEUTRO: amostra insuficiente |
| T3 IG alcance mediana / skip | 58 / 66,7% | alcance 4 (25 sofá, 0 cartão, 4 legumes) / skip 92% e 100% nos 2 vídeos | 3 | >=80 e <=55% | <50 ou >70% | PERDEU (alcance 4 < 50; skip 92-100% > 70%) |
| T4 TikTok views / tempo / shares | 174 / 2,56 s / 9 em 24 | 126 / 1,67 s / 1 share (1 post) | 1 | >=300, >=4 s, 1 share/4 posts | tempo <2,5 s | NEUTRO: amostra insuficiente |
| T5 comentários de terceiros | ≈0 | 0 (todo comentário FB/IG = 1 por post de artigo = o nosso link; memes 0; TikTok 0) | FB 2, IG 3, TT 1 | >=1 a cada 5 posts | 0 em 72 h | NEUTRO: sem janela completa (1 dia de 3) |
| T6 seguidores FB / IG / TT | 8 / 0 / 19 | FB 8 (+0), IG 0 (+0), TikTok sem dado (Buffer não informa) | - | +3 / +2 / +6 | 0 novos em 72 h | NEUTRO: sem janela completa |
| T7 cliques blog (72 h) | 6 em 7 dias | Zernio clicks = 0 nos posts do período; sem dado confiável | - | >=10 | 0 | NEUTRO: sem dado |
| T8 funil | 0 vendas, 0 DMs, 0 contatos | Kiwify: 0 vendas nos últimos 7 dias (Vendas aprovadas: 3 no total, todas de 21/09 e 29/09, e-mails do próprio Allan); vendas abandonadas e visitas: sem dado (não lido nesta rodada). ManyChat: contatos 0/1000; execuções da automação GUIA: sem dado (lista de automações não carregou). Brevo: lista "7 Erros - Isca" (id 3) = 0 contatos | - | 1 venda | sem gatilho | NEUTRO: sem janela completa (líderes em 0) |
| T9 processo | (a) falhou 20/10 | (a) OK (b) OK (c) FALHA (d) OK | - | 0 falhas | qualquer falha | PERDEU (item c, já em E31) |

Observação T8 (dado, não ordem): ao abrir o Dashboard da Kiwify, a tela mostrava o bloco "Documentos enviados... verificação de identidade em até 24 h". Não mexi. Vale o Allan conferir se há verificação pendente que bloqueie saques.

## T9 — evidência
- (a) OK: data/tiktok/relatorio.md §(f) e data/audiencia/medicao.md não pedem ao Allan nada que 05 Decisões/06 Pendências já deem como feito. Agentes: Especialista TikTok, Criador de Audiência.
- (b) OK: data/audiencia/ideias.md "Matriz do lote" (gancho em 3 peças, pilares, prova/teste, CTA). Agente: Criador de Audiência.
- (c) FALHA: data/social/estrategia_social.md continua na edição de 22/10 07:35 (arquivo sem mudança desde a rodada da manhã): mantém "Comente GUIA" (IG 6ad7ad34be90a3a9459824fe, FB 6ad7ad32429cabfd5305b7e7, 25/10 17:29) e declara "PC do Allan ausente" sem list_connected_browsers; "isca vigente" não existe em config/prompts nem agents. Agente: Estrategista de Redes Sociais. Já tem E31; a prova é a rodada dele de 23/10 07:35. Sem linha nova para não duplicar.
- (d) OK: recomendações de 22/10 viraram E23-E46 no mesmo dia.

Ressalva: T1-T8 medem o pacote de skills; só o T9 isola por agente. IG: com n=3 contando o cartão, a mediana é 4; sem o cartão (n=2, insuficiente) seria 14,5, ainda abaixo de 50. FB/TikTok: a decisão real cabe nas rodadas de 23 e 24/10.
