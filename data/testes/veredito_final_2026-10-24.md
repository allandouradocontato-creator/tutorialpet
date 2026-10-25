Dados até 2026-10-24 21:15 (Fortaleza) — Zernio (FB/IG, sync 24/10 20:40 Fortaleza), Buffer (TikTok; métricas só até 24/10 01:08 Fortaleza, defasadas ~20 h), Chrome do Allan (list_connected_browsers = 1 Chrome Windows; Kiwify, ManyChat, Brevo; aba fechada). VEREDITO FINAL do teste de 21/10 (baseline 21/10 14:40). Aviso: add_repo não existe na rotina; o repo já veio no escopo (main = origin/main).

## Quem entra na conta (grupo "pós-skills")
Publicado depois de 21/10 14:40 e com idade >= 24 h (corte 24/10 21:12 menos 24 h). Falha técnica: nenhuma (posts_list_failed e Buffer sem erro). Os cartões de imagem ("Erro 1/2 de 7", "Qual é o cargo do seu pet") contam (precedente das rodadas 22 e 23; não são falha técnica).
- FB n=12; views: 0, 0, 0, 2, 4, 4, 124, 215, 218, 243, 251, 313.
- IG n=12; alcance: 0, 0, 0, 4, 4, 16, 26, 26, 29, 41, 84, 103.
- TikTok n=7 (Buffer, posts enviados 21/10 a 23/10); views 181, 181, 195, 166, 176, 188, 57; tempo médio 2,05 / 1,93 / 2,5 / 3,36 / 2,06 / 1,67 / 2,27 s; shares 1 (legumes) e 0 nos outros 6.
- Parciais (<24 h, não contam): FB 24/10 planta 211, plantão 59, petiscos 219, caixa de transporte 133 views; IG 24/10 alcance 29, 15, 15, 0; TikTok 24/10 sem métrica (Buffer defasado).

## Tabela final
| teste | antes (baseline) | hoje | n | meta | gatilho | veredito FINAL |
|---|---|---|---|---|---|---|
| T1 FB views mediana | 218 | 64 (só os 9 vídeos: 215; os 3 cartões = 0) | 12 | >=280 | <200 | PERDEU (mediana 64 < 200; nos vídeos a base se mantém, 215, mas sem chegar à meta 280) |
| T2 FB tempo médio | 4,0 s | 4,0 s (média dos 9 posts com view; 3,1 a 8,7 s) | 9 | >=6 s | <4 s | NEUTRO (no limite do gatilho: 4,01) |
| T3 IG alcance mediana / skip | 58 / 66,7% | 21 / 72,6% (média dos 9 reels com skip; vídeos sozinhos: mediana 26) | 12 | >=80 e <=55% | <50 ou >70% | PERDEU (alcance 21 < 50 e skip 72,6% > 70) |
| T4 TikTok views/post / tempo / shares | 174 / 2,56 s / 9 em 24 | 163 (mediana 181) / 2,26 s / 1 em 7 | 7 | >=300, >=4 s, 1 share a cada 4 posts | tempo <2,5 s | PERDEU (tempo 2,26 s < 2,5; views e shares abaixo da meta) |
| T5 comentários de terceiros | ≈0 | 0 (todo comentário FB/IG = 1 por post de artigo = o nosso link; memes e cartões 0; TikTok 0 nos 7) | FB 12, IG 12, TT 7 | >=1 a cada 5 posts | 0 em 72 h | PERDEU (janela de 72 h fechou em 24/10 14:40 com 0). Ressalva: autor de cada comentário não listado pelo Zernio; conclusão por contagem (1 por post de artigo = o nosso) |
| T6 seguidores FB / IG / TT | 8 / 0 / 19 | sem dado (accounts_get_follower_stats segue falhando com "unexpected keyword argument 'limit'"; Buffer não informa seguidores) | - | +3 / +2 / +6 | 0 em 72 h | NEUTRO (sem dado; não decido PERDEU sem número) |
| T7 cliques no blog (72 h) | 6 em 7 dias | sem dado (Zernio clicks = 0 em todos os 39 posts, sem rastreio de link) | - | >=10 | 0 | NEUTRO (sem dado) |
| T8 funil | 0 vendas, 0 DMs, 0 contatos | Kiwify: sem dado (Dashboard só mostra "Documentos enviados / verificação de identidade em até 24 h"; não mexi). ManyChat: contatos 0/1000; execuções da automação GUIA sem dado (tela não carrega a lista). Brevo "7 Erros - Isca" (id 3): 0 contatos (Sua primeira lista: 1) | - | 1 venda | sem gatilho | NEUTRO (indicadores líderes em 0; isca GUIA descartada em 21/10 e MIMO sem PDF: E27) |
| T9 processo | (a) falhou 20/10 | 24/10: (a) OK (b) FALHA (c) OK (d) OK; acumulado 21-24/10: falha em 22/10 (c) e em 24/10 (b) | - | 0 falhas | qualquer falha | PERDEU (2 falhas no período) |

## T9 — evidência (rodada de 24/10)
- (a) OK: data/social/estrategia_social.md §5 ("Nenhuma nova. Segue A02 e E13. Não repito pedido de criar ManyChat/isca") e data/audiencia/ideias.md (MIMO conferido por ls, sem pedir ao Allan). Agentes: Estrategista, Criador de Audiência.
- (b) FALHA: data/audiencia/ideias.md de 24/10 é "SÓ TRENDS + 3 IDEIAS (lote completo volta segunda 26/10)": sem matriz (gancho em 3 peças, pilares, prova/teste, CTA). Agente: Criador de Audiência. (Última matriz entregue: 23/10, "Matriz do lote".)
- (c) OK: estrategia_social.md §5 trata a isca MIMO como estado vigente (PDF ausente, E27 aberta) e ideias.md liga MIMO→DM a E27/E29. Agente: Estrategista.
- (d) OK: recomendações de 24/10 (estrategia_social.md, execucao.md) viraram E97-E104 no mesmo dia. Agentes: Estrategista, Diretores.

## Veredito, recomendação e o que mudar na fábrica
| teste | final | recomendação | o que mudar (arquivo/prompt) |
|---|---|---|---|
| T1 FB views | PERDEU | mudar | Nenhum cartão/imagem (E93/E97 já em vigor, mediana dos vídeos 215). Fator novo: no FB, o slot das 15:00 deixa de ser meme 8 s (24/10: 59 views; vídeo de artigo no mesmo dia: 211 e 219) e vira vídeo de artigo com gancho de pergunta. Arquivo: config/estrategia_social.yaml (grade facebook). Linha E105 |
| T2 FB tempo | NEUTRO | continuar 72 h trocando 1 fator | Fator: abrir o vídeo com o resultado/pergunta no 1º segundo (vídeos acima de 5 s: escova 5,6 s e filhote 8,7 s; abaixo: ciência 1,4 s). Prompt: config/prompts/humorista.md e gerador de legenda. Sem linha E nova (NEUTRO; registrar na próxima rodada do Estrategista) |
| T3 IG | PERDEU | mudar | E94 mantida; fator novo: gancho/resultado nos 2 primeiros segundos (skip 72,6%) em todo reel de artigo; cartões já proibidos (E97). Arquivo: config/estrategia_social.yaml (instagram) e config/prompts/humorista.md. Linha E106 |
| T4 TikTok | PERDEU | mudar (já em curso) | E50/E95/E98/E99 já são o fator único (cortes 15-25 s, resultado no segundo 0, cachorro-sozinho). Executor confirma que a fila NÃO agendada de 25-27/10 obedece; prova 27/10: tempo >=2,5 s. Linha E107 |
| T5 comentários | PERDEU | mudar | Fator: CTA binário "1 ou 2?" no fim da legenda e no 1º comentário de todo post não agendado (hoje a pergunta aberta rende 0). Arquivos: config/prompts/atendente_comentarios.md, config/estrategia_social.yaml. Linha E108 |
| T6 seguidores | NEUTRO (sem dado) | continuar; consertar a leitura | Medidor passa a ler seguidores no Chrome (Perfil FB/IG/TikTok) ou fixar kwargs do accounts_get_follower_stats; sem número não há decisão |
| T7 cliques | NEUTRO (sem dado) | continuar; criar medição | Link encurtado/UTM por rede no 1º comentário (arquivo: config/prompts/publicador.md) para o Zernio/GA4 trazerem cliques |
| T8 funil | NEUTRO | continuar | Nada vai ao ar sem E27 (PDF MIMO). Allan precisa concluir a verificação de identidade da Kiwify (E61/06 Pendências) para o Medidor ler vendas |
| T9 processo | PERDEU | mudar | Criador de Audiência: matriz obrigatória em TODA rodada, inclusive curta (mínimo: 1 gancho em 3 peças, 1 pilar, prova/teste, CTA). Arquivo: config/prompts/criador_audiencia.md. Linha E109; falha em biblioteca/habilidades/registro_de_falhas.md |

## Resumo do pacote
PERDEU 5 (T1, T3, T4, T5, T9), NEUTRO 4 (T2, T6, T7, T8), GANHOU 0. Em nenhuma métrica de alcance o pacote bateu a meta; o piso da base (vídeo de artigo no FB ~215) se manteve, e quedas vieram de cartões de imagem (já bloqueados em E97) e de vídeo longo no TikTok. Veredito do pacote: não escalar; manter só o que já tem E.. aberta.

Ressalva: T1-T8 medem o pacote de skills; só o T9 isola por agente. Teste encerrado após esta rodada: nas rodadas seguintes escrever "teste encerrado" e parar.
