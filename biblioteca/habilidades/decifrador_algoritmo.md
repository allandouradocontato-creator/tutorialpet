---
criado: 2026-10-21
versao: v2 — 22/10/2026
---
v2 — 22/10/2026 — status: rascunho até prova (régua 7)

# Habilidade: decifrar algoritmo com amostra pequena (toda rotina que mede resultado de post)

## CONTRATO DE RESULTADO (22/10/2026)
1. RESULTADO ÚNICO: tempo. Horas entre a publicação de um post e a decisão de troca de UMA peça (fonte: horários do Zernio/Buffer e linha de aprendizado). Hoje o veredito sai com 72 h+; este contrato mede quanto isso encurta.
2. META E PRAZO: HOJE (22/10): 100% dos posts do lote com leitura "informação" a 1 h e 3 h registrada, e troca de UMA peça decidida em até 3 h após o 2º post do formato abaixo do gatilho (FB < 200 views ou < 4 s; IG alcance < 50 ou skip > 70%; TikTok < 2,5 s). Veredito DEFINITIVO continua só com 72 h+ e n ≥ 5 por braço (ver Limites): leitura de 1 h/3 h vale como PARCIAL. Primeira leitura hoje às 22h.
3. JOGADAS (hipótese -> ação -> métrica -> quando trocar):
   - Leitura parcial rápida. Hipótese: 1 h e 3 h bastam para detectar fail claro (2+ posts abaixo do gatilho) sem esperar 72 h. Ação: tabela com idade em horas e marcação informação/parcial/vale. Métrica: horas até a decisão de troca. Trocar: se o parcial de 3 h contradisse o de 72 h em 2 rodadas, voltar a decidir só com 72 h.
   - Uma variável por teste. Hipótese: teste com 2 fatores não ensina nada. Ação: conferir antes de publicar que só gancho, CTA, horário ou formato muda, trocando o lado do braço entre redes. Métrica: % de testes com 1 variável (meta 100%). Trocar: mais de 1 variável = veredito UNKNOWN e refazer o desenho.
   - Causa externa primeiro. Hipótese: alcance baixo pode vir de originalidade, marca d'água, Account Status do IG ou horário colado a outra rede, não do gancho. Ação: listar a causa externa antes de culpar o conteúdo. Métrica: causas listadas por rodada. Trocar: causa externa achada = corrigir antes de qualquer teste de gancho.
   - Campeão contra referência externa. Hipótese: campeão interno só é padrão se estiver perto de uma referência de alto engajamento. Ação: comparar com 1 referência do banco. Métrica: distância do campeão à referência. Trocar: longe = não declarar vitória, manter em observação.
4. LAÇO: data/habilidades/aprendizado/decifrador_algoritmo.md, 1 linha por rodada: data | jogada | resultado n/métrica | mantém/altera/descarta. Número ruim = troca de jogada na mesma rodada.
5. JUIZ: biblioteca/habilidades/juiz_de_qualidade.md (Juiz de Qualidade, agente separado de quem produz; nota mínima 7 para ir ao vivo; ensaio aprovado = média ≥ 7 e nenhuma nota < 5).


Problema recorrente (data/auditoria/semanal.md, data/audiencia/medicao.md): conta nova, pouco dado, e agentes concluíam com n=1 ("meme venceu"). Esta skill diz quando um número decide e quando é só informação. Não pesquisar o algoritmo na web: o que está confirmado e o que não está fica abaixo.

## Procedimento
1. Listar os posts do teste com data de publicação e idade em horas. Saída: tabela com idade.
2. Descartar do veredito os < 24 h (marcar "informação"). Os de 24-72 h: marcar "parcial".
3. Contar n por variação. n < 5 em qualquer braço = veredito unknown ("amostra insuficiente, continuar").
4. Conferir que só UMA variável mudou entre os braços (gancho, CTA, horário, formato). Mais de uma = unknown; refazer o desenho.
5. Conferir causas externas: originalidade, marca d'água, Account Status, erro de publicação, horário colado a outra rede. Qualquer uma = unknown ("causa externa").
6. Comparar cada braço com os limites da tabela (mesma rede, nunca de outra rede). Saída por braço: pass / fail / unknown.
7. Decisão: pass nos dois braços = escalar o melhor (50% da produção seguinte); fail claro (2+ posts abaixo do gatilho em 3 dias) = mudar UMA peça no mesmo dia; resto = continuar mais 72 h trocando 1 fator.
8. Comparar o campeão com 1 referência externa (banco de referências). Longe = não declarar vitória.
9. Gravar o veredito e a linha de aprendizado.

## Saída obrigatória
Uma linha em `data/habilidades/aprendizado/decifrador_algoritmo.md`, formato: `data | regra aplicada (nº do passo) | resultado (n, métrica) | mantém/altera`. Rodada sem a linha = "não aplicou". Regra das 3 linhas: 3 linhas com o mesmo padrão = propor edição desta skill (versão, data, evidência) em entrega_direta.md.

## Limites (regras de plataforma, validações e números de corte; não são jogadas)
Movido em 22/10/2026 para o fim: o que o agente FAZ está nas jogadas acima; aqui só o que ele não pode ultrapassar.

### Regras do Allan que mandam (05 Decisões.md)
Teste dura no máximo 3 dias; número ruim claro muda o caminho na hora, sem esperar o fim. Só vídeo. FB/IG/TikTok nunca no mesmo horário (>= 10 min). Gancho "Esse erro tá silenciosamente…" proibido. Sem "cão" (usar "cachorro"). Fase atual: audiência real antes de vender; ordem de sinal: comentário > compartilhamento > seguidor > venda.

### Regras de plataforma que esta skill aplica (só [C])
Fonte: biblioteca/regras_plataformas/meta_facebook_instagram.md (lido 22/10/2026).
1. [C] Se a pergunta é "o que a Meta pesa em Reels", então usar reshares, assistir inteiro, curtidas e visitas ao áudio como sinais de leitura; a Meta não publica pesos (meta_facebook_instagram.md, sinais de Reels).
2. [C] Se o post não é original (repost, compilado, só borda/legenda/velocidade), então a causa de alcance baixo já está explicada: não testar gancho nele, corrigir a originalidade primeiro (Facebook, Originalidade).
3. [C] Se o alcance do IG está baixo, então ler o Account Status (app) uma vez por semana antes de culpar o conteúdo; restrito = causa externa ao gancho (Instagram, elegibilidade).
4. [C] Se quer teste barato de gancho no IG, então Trial Reel (só não seguidores) isola o efeito do gancho do efeito da base de seguidores (Instagram, Trial reels).
5. [C] Facebook estima a chance de engajamento por pessoa (autor, horário, tema, histórico): se o horário muda e o tema muda juntos, o teste não vale (Facebook, distribuição).

#### Validar antes de agir ([N])
- [N] TikTok: conclusão do vídeo e tempo assistido pesam mais, depois salvar e compartilhar (socialpilot, mercado; tiktok.md §7).
- [N] TikTok: distribuição inicial para subconjunto de seguidores; conta pequena não penalizada; duração e frequência ideais.
- [N] Peso exato de tempo assistido na Meta; punição por repost (imprensa).
- [N] Melhores horários públicos (Loggi 09/02/2026; SocialPilot) coincidem só em 20h e sex 13-15h: sem base para trocar nossa grade.

### Limites de decisão (números nossos)
| Item | Regra | Base |
|---|---|---|
| Idade do post | < 24 h = informação; 24-72 h = parcial (pode orientar teste, não decide); >= 72 h = vale | regra do Allan, testes de 72 h |
| n por variação | < 5 posts = "amostra insuficiente"; nunca inventar causa | data/testes/baseline_2026-10-21.md |
| "Rede X não funciona" | só com >= 10 posts de 72 h+ na rede | hoje FB n=26, IG n=25, TikTok n=35 |
| Ruído natural | TikTok piso 150-220 views em qualquer hora desde 14/10 (mediana 190, 19 vídeos); só mudança acima de 300 views ou tempo >= 4 s conta como efeito | data/tiktok/relatorio.md 22/10 |
| FB | mediana 227 views (n=12, 19-20/10); fail < 200, pass >= 280; tempo 4,0 s, fail < 4 s, pass >= 6 s | estrategia_social.md 22/10 |
| IG | alcance mediana 60 (n=12); fail < 50, pass >= 80; skip 55,6%, fail > 70%, pass <= 55% | idem |
| TikTok | tempo médio 2,87 s (35 posts); fail < 2,5 s, pass >= 4 s; melhor 7,46 s | relatorio.md 22/10 |
- Comparação com fonte externa: o campeão interno só vira "padrão" se estiver perto de 1 referência externa de alto engajamento; senão o teto não foi atingido.
- Janela mínima para leitura de seguidores: 3 dias (T6, baseline 21/10: FB 8, IG 0, TikTok 19).
- Sem número para: tamanho de efeito mínimo por rede além dos acima. Medir primeiro: 5 posts de 72 h+ por variação, até 3 dias, registrar mediana e dispersão.
