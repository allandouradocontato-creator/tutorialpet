# Regra de mudança rápida (decisão do Allan, 16/10/2026)

Vale para o Estrategista de Redes Sociais e para o Executor de Decisões. Onde houver conflito com instruções antigas ("julgar só com 72h", "teste de 7 dias", "esperar até 22/10"), esta regra vence.

Motivo: resultado terrível não pode esperar semanas. Quando o número mostra que o caminho não funciona, a fábrica desvia no mesmo dia.

## 1. Testes curtos
- Teste dura no MÁXIMO 3 dias (antes 7). O teste de horários de 15-21/10 encerra em 18/10.
- Indicadores líderes lidos já com 24h: tempo médio assistido, % assistido, skip rate (IG), compartilhamentos e salvamentos. Views absolutos só entram como apoio.
- Amostra pequena não impede agir: impede AFIRMAR causa. Agir com hipótese e medir de novo em 24-48h.

## 2. Gatilho de mudança (qualquer um, em 2 ou mais posts do mesmo formato nos últimos 3 dias)
- Facebook: tempo médio assistido abaixo de 6 s.
- Instagram: skip rate acima de 70%.
- TikTok: tempo médio abaixo de 4 s, ou menos de 1 compartilhamento a cada 4 posts.
- Qualquer rede: mediana de views abaixo da meta do painel (config/estrategia_social.yaml).

Gatilho acionado = plano de mudança NA MESMA RODADA, sem esperar a próxima:
1. PARAR: o que sai da produção já (formato, duração, abertura, legenda), com o dado.
2. TESTAR: no máximo 3 testes radicalmente diferentes (não variação de horário), cada um com hipótese, formato exato, nº de posts, redes, medição e critério de decisão em 24-48h. Base em referências reais de pet brasileiro que já engajam (link e número).
3. APLICAR: o que mudar na fábrica (qual arquivo/prompt/config).

## 3. Para onde vai a recomendação (ciclo fechado)
- O Estrategista escreve o plano em data/social/plano_de_mudanca_AAAA-MM-DD.md e acrescenta cada ação executável em data/decisoes/execucao.md (ID E01, E02...; "decidido em"; ação; dono "nuvem"; prazo de até 1 dia; status "decidido"; origem "Estrategista, autorização permanente do Allan de 16/10/2026").
- O Executor de Decisões roda às 06:53 e às 10:53 (Fortaleza), executa essas linhas e só marca "feito" com evidência (commit, id de rotina, URL 200).
- AUTORIZAÇÃO PERMANENTE DO ALLAN: vale para ações reversíveis, gratuitas e dentro das regras da casa (editar config e prompts, trocar formato/gancho/legenda/duração de itens que AINDA NÃO foram agendados, ajustar rotinas, mudar a fila de produção).
- CONTINUA PRECISANDO DO ALLAN: gastar dinheiro, anúncio pago, login/2FA/identidade, conteúdo sensível (política partidária, religião, saúde humana, tragédia, menores, crítica a pessoas reais, lei/benefício), apagar ou mexer em post já publicado.
- Posts JÁ agendados que o plano mandar trocar: o Estrategista e o Executor não mexem; listam no plano com id e horário e o Claude da sessão do Allan executa.

## 4. Resultado ao Allan
Até 8 linhas: o que está ruim (com número), o que parou, o que entrou no lugar, quando sai a próxima leitura e no máximo 3 decisões (cada uma com recomendação).

## 5. CICLO DE EXPLORAÇÃO CONTÍNUA (ordem do Allan, 20/10/2026; VALE SOBRE TUDO ACIMA E SOBRE QUALQUER "CAMPANHA DE N DIAS")
Allan descartou campanhas de duração fixa (7 ou 14 dias). O Estrategista roda 2x ao dia (07:07 e 17:07 Fortaleza) e trabalha em ciclo, sem ficar preso a erro:
1. LER cada post publicado com 6-24h (parcial) e fechar o veredito com 24h: tempo médio %, skip, shares, saves, comentários de terceiros. Cada post vira UMA linha em data/social/laboratorio.md: id, rede, hora, formato, gancho, CTA, voz (voz.json do manifest), imagem/cena, tema, resultado, veredito (GANHOU / NEUTRO / PERDEU).
2. PERDEU ou NEUTRO = não repetir o mesmo fator. O próximo post da fila já troca UM fator diferente (gancho, formato, duração, voz/emoção, tipo de imagem, tema, CTA, tipo de postagem). Nunca dois posts seguidos com a mesma hipótese que perdeu.
3. PESQUISAR a cada rodada (máx. 6 buscas, só o que for novo): 3 a 5 referências reais do TikTok/IG/FB pet Brasil (link + número) com gancho, duração, voz, imagem e CTA; ao final de cada rodada acrescente em data/social/referencias_virais.md o que for novo e transforme em variações prontas para a fábrica.
4. PORTFÓLIO: manter sempre 5 variações em teste (mínimo 4 fatores diferentes), cada uma com hipótese de 1 linha. Nada de testar só horário.
5. GANHOU = escalar: repetir o fator vencedor em 3 variações novas e dar a ele 50% da produção seguinte; os outros 50% seguem em exploração. Dois GANHOU seguidos no mesmo fator viram regra em config/estilo_viral.yaml.
6. CAMINHO ÚNICO ATÉ A FÁBRICA: toda troca vira linha E.. em data/decisoes/execucao.md (prazo ≤ 1 dia) + edição de config/estilo_viral.yaml / prompts, para a próxima produção já sair diferente. Itens já agendados que perderam: listar ids para o Allan trocar.
7. Sem anúncio pago até haver GANHOU repetido em 2 fatores e mediana acima da meta nas 3 redes (decisão do Allan; ele autoriza quando o Estrategista provar isso).
8. Voz: só Duda com tags (portão da Duda). Vídeo sem a voz padrão não conta como amostra de formato.
Resultado ao Allan: até 6 linhas (o que perdeu, o que entrou no lugar, o que ganhou e escalou, próxima leitura).

## 6. LINHA DE BASE DE SEGUIDORES (Allan, 20/10/2026 11:20, conferido por ele nas contas): Facebook 7 (seguindo 49), TikTok 10, Instagram 0.
- Diagnóstico: a conta é nova e minúscula; a mediana de 215 views no FB e 46 no IG já é entrega para NÃO seguidores. Falha = converter view em seguidor, comentário e compartilhamento. Seguidor novo por dia e seguidores por 1.000 views entram no painel (todas as rodadas anotam o número de seguidores por rede em data/social/laboratorio.md).
- Meta de arranque (hipótese, sem prometer): +5 seguidores/dia somando as 3 redes nas próximas rodadas; se após 5 vídeos de formatos diferentes seguir/1.000 views < 3, trocar a PROMESSA de seguir (série nomeada, 'amanhã tem parte 2'), não só o gancho.
- Todo vídeo precisa de UM motivo para seguir (série com nome e promessa de continuação), dito no fim e escrito na legenda.
- Crescimento orgânico sem custo para propor ao Allan (nada executa sem a autorização dele): comentários úteis e curtos, pela conta da marca, em 10 posts/dia de páginas pet brasileiras do mesmo porte ou maiores; seguir e interagir com perfis de tutores de primeira viagem; Reels em collab; responder todo comentário em até 1h. Proibido: comprar seguidores, seguir/desseguir em massa, mensagem em massa.
