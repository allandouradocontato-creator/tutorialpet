v1 — 22/10/2026 — status: rascunho até prova (régua 7) — dono: Diretor de Conteúdo e Blog; executam SEO, Criador de Audiência, Publicador, Vigia
base: biblioteca/habilidades/plataforma_google_seo_adsense.md (J1–J10), biblioteca/regras_plataformas/google.md §2–3, config/ritmo_blog.yaml, scripts/auditoria_adsense.py, data/auditoria/adsense.md
pedido do Allan (22/10): este blog é o TESTE e o modelo para outros blogs; 4 semanas para avaliar tudo (quantos artigos, qual frequência), variar 3 e 4 artigos/dia, variar temas, fazer enquetes e perguntas, buscar tráfego e fazer SEO.

# Habilidade: operar as 4 semanas até a aprovação do AdSense (e medir o que causou o quê)

## (a) Quando usar
Todo dia (Diretor de Conteúdo, seg e qui; Vigia, 4x/dia) até 18/11/2026; depois vira o molde (molde/skills) para os próximos blogs.

## (b) Entradas
config/ritmo_blog.yaml; data/auditoria/adsense.md (script diário); fila_temas; Search Console (impressões, cliques, páginas indexadas); cliques do blog vindos das redes (UTM); enquetes das redes (Zernio/Buffer analytics); data/testes/adsense_4semanas.md (diário do experimento).

## (c) Regras → jogadas (formato: fazer | alvo ou medir primeiro | troca)
Princípio de bom senso (Allan, 22/10): toda jogada que depende de audiência (enquete, comentário, compartilhamento) só liga depois que o número nosso mostrar que há quem responda; antes, trocar por fonte que não depende de seguidor (Search Console, buscas, perguntas públicas).
J1 (meta do pedido: ritmo variável). Fazer: dia ímpar do ano = 3 artigos, par = 4 (config/ritmo_blog.yaml); nunca abaixo de 3. Alvo: 28 dias com ≥3; ≥12 dias de 4. Troca: 2 dias seguidos abaixo do plano = ALERTA e o Vigia dispara fábrica/promove aprovados na hora (causa a registrar).
J2 (variar tema e formato; scaled content abuse = spam [C, google.md 3.1]). Fazer: rodízio de pilares e de formatos (lista no yaml); 2+ formatos por dia; nenhum tema que responda a mesma pergunta de outro (J1 da habilidade de SEO). Alvo: 0 pares duplicados; 6 pilares em 3 dias. Troca: par duplicado = fundir.
J3 (qualidade antes de volume; "mirar contagem de palavras" é sinal ruim [C]). Fazer: cada artigo passa na auditoria (900+ palavras sem enchimento, ≥3 subtítulos, fonte em saúde, capa que mostra o tema, 2 fotos no corpo). Alvo: 0 FALHA em data/auditoria/adsense.md antes de pedir a revisão. Troca: FALHA aberta >24 h = o Vigia abre ficha.
J4 (bom senso, Allan 22/10: com 8 seguidores no FB, 0 no IG e 19 no TikTok, enquete não tem quem responda). Fazer: enquete própria só quando a audiência permitir: porta = ≥300 seguidores na rede OU média ≥100 visualizações por post nos últimos 7 dias; antes disso, NÃO fazer enquete nem contar com comentário. No lugar, o público vem de perguntas que já existem: (1) Search Console: consultas com impressão; (2) "As pessoas também perguntam" e sugestões do Google para o tema; (3) perguntas reais em posts e comentários de contas grandes do nicho (só ler; a guerrilha de comunidade já faz isso; sem copiar texto); (4) comentários e mensagens que a nossa conta receber. Cada artigo "resposta" cita a pergunta e a fonte dela. Alvo: ≥2 artigos/semana nascidos de pergunta real com fonte registrada. Medir primeiro: seguidores e views por post (já no laboratório). Troca: quando a porta abrir, ligar 1 enquete por semana e comparar com a linha-base.
J5 (pergunta ao leitor no fim do artigo: custo zero, mas sem expectativa de resposta). Fazer: manter 1 pergunta de fechamento convidando a responder no comentário da rede; não medir sucesso por resposta até a porta de J4. Alvo: medir primeiro (0 hoje). Troca: sem mudança até a porta abrir.
J6 (tráfego: o AdSense avalia site com público real; fontes a testar, uma por vez, só gratuitas). Fazer: (1) redes: link no 1º comentário (regra existente); (2) Search Console: enviar sitemap, pedir indexação dos novos, ler consultas com impressão e posição 8–20 e reforçar esses artigos; (3) links internos: cada artigo novo recebe 2 links de artigos antigos do mesmo pilar; (4) Pinterest (fotos de pet funcionam; precisa conta: ficha para o Allan se for adotar) [N: não confirmado, testar 10 pins]; (5) Google Discover [N]: imagem de capa grande (≥1200 px de largura) e meta max-image-preview:large; validar na documentação do Google antes de afirmar. Alvo: ≥10 cliques do blog em 72 h (meta 22/10, linha-base 6 em 7 dias); medir primeiro: impressões/semana. Troca: fonte sem 1 clique em 7 dias = cortar e testar a próxima.
J7 (SEO é rotina, não evento). Fazer: toda semana o agente de SEO (config/prompts/seo.md) entrega: 5 consultas com impressão e pouco clique (reescrever título/meta), 5 artigos a reforçar, 3 temas novos por pergunta real (People Also Ask/Search Console), checagem de canonical/sitemap/404. Alvo: lista de 5+5+3 por semana gravada em data/seo/. Troca: item sem ação em 7 dias = devolve ao dono.
J8 (4 semanas para AVALIAR). Fazer: diário data/testes/adsense_4semanas.md com 1 linha por dia: data | artigos no ar | formatos | pilares | cliques blog | impressões | enquetes/votos | FALHAS da auditoria. Toda segunda: resumo da semana (o que subiu, o que caiu, 1 mudança para a semana seguinte, um fator por vez). Alvo: 28 linhas; 4 resumos. Troca: mudar 2 coisas na mesma semana = invalida a leitura (UNKNOWN).
J9 (quando pedir a revisão do AdSense: processo [N, answer/9130038, reler]). Fazer: pedir só com auditoria sem FALHA, ≥25 artigos originais, ≥14 dias de ritmo sem buraco e tráfego real registrado; confirmar o estado na aba Sites (conta já aberta no Chrome do Allan, pub-7204207473239947). Alvo: pedido na semana 2 ou 3. Troca: reprovado = ler o motivo, corrigir 1 causa, pedir de novo após 7 dias.
J10 (o que o molde herda). Fazer: no fim da semana 4, copiar para molde/skills a versão genérica desta habilidade ({NICHO}, {DOMINIO}) com o que funcionou e o que não. Alvo: 1 arquivo + checklist de lançamento de blog. Troca: sem prova das semanas 1–4, não vai ao molde.

## (d) Validar antes de agir [N]
Processo e prazo da aprovação (answer/9130038); posicionamento de anúncios (48182); política de publisher; Discover; texto da atualização de site reputation (ago/2026). O Atualizador de Skills relê toda semana.

## (e) Limites de decisão com dados nossos
Linha-base cliques: 6 em 7 dias (21/10). Impressões, votos de enquete, comentários: medir primeiro na semana 1. Amostra: menos de 3 artigos por variação = UNKNOWN.

## (f) Procedimento diário (Diretor de Conteúdo; Vigia confere)
1. Qual é o plano de hoje (3 ou 4)? Quantos já estão no ar (curl 200 + git log site/build)? Faltando = promover aprovados / disparar fábrica.
2. Formatos e pilares do dia respeitam J2? Ajustar a fila.
3. Rodar scripts/auditoria_adsense.py; cada FALHA vira ação.
4. Enquete da semana programada? (J4) Se não, ficha para o Criador de Audiência.
5. Gravar a linha do dia em data/testes/adsense_4semanas.md e a linha de aprendizado.

## (g) Saída obrigatória e laço
`data/habilidades/aprendizado/blog_adsense_4_semanas.md`: `data | jogada | resultado (n, métrica) | mantém/altera`. 3 linhas com o mesmo padrão = propor edição da skill. Sem a linha, a rodada conta como "não aplicou".

## v1.2 (22/10/2026, ensaio do Juiz: 3 artigos em 3 moldes, média 7,67) — regras novas
- D3 obrigatório: artigo que fala de saúde, limite de tempo ou comportamento cita pelo menos 1 fonte NOMEADA (entidade, estudo, manual de referência, com link). "Consulte o veterinário" não é fonte. Campo `autor` nunca vazio.
- Variedade de fecho: nunca repetir o mesmo H2 de encerramento em artigos seguidos ("Para fechar"); alternar 4 fechos (pergunta ao leitor, checklist de 3 itens, erro mais comum, próximo passo). "Quando procurar o veterinário" muda de posição.
- Título promete = texto entrega: se o título diz "5 primeiros minutos", os 5 minutos ocupam a 1ª metade do texto.
- História composta: dizer que é composta é obrigatório e o desfecho não pode trazer número de resultado ("em uma semana parou").
- Foto de corpo coerente com o H2 onde entra (rubrica B), 1 por artigo no mínimo.
