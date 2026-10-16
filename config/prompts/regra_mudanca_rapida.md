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
