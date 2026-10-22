v2 — 22/10/2026 — status: rascunho até prova (régua 7)
base: biblioteca/regras_plataformas/google.md (v2, seções 1-3, 6, 7.1); config/prompts/seo.md; data/memoria/14 Blog e AdSense - aprendizados.md; data/seo_onpage/otimizados (53 artigos).

# Habilidade: artigo que passa no Google (SEO + AdSense + afiliado) — Agente de SEO, Redator, Revisor

## CONTRATO DE RESULTADO (22/10/2026)
1. RESULTADO ÚNICO: clique. Cliques orgânicos do blog tutorialpet.com.br (fonte: Search Console; enquanto a propriedade não estiver verificada, GA4 canal Organic Search).
2. META E PRAZO: ≥ 10 cliques orgânicos em 7 dias (meta do departamento Conteúdo e Blog; linha-base 6 em 7 dias, 21/10) e artigo novo indexado em < 48 h. Primeira leitura HOJE (22/10) até 20h: status de indexação dos artigos publicados hoje + cliques e impressões do dia; segunda leitura 23/10 às 20h (24 h) e terceira em 72 h.
3. JOGADAS (hipótese -> ação -> métrica -> quando trocar):
   - JD1 demanda. Hipótese: o artigo não aparece porque o título não usa o vocabulário da busca (caso cinto: "cadeirinha"/"assento" zero vezes). Ação: reforçar os 5 piores da auditoria de 22/10 (12 artigos de escolha/compra sem comparação, 0 com tabela) com sinônimo popular no título/H1/1º parágrafo e tabela de comparação (reforcar_artigos.py). Métrica: hoje, 5 de 5 reforçados e indexação solicitada até 20h; depois impressões e cliques da URL em 24 h e 72 h. Trocar: 0 impressão em 72 h = reescrever o título pelos termos dos 5 primeiros resultados (seção h, item 2).
   - JD2 fila sem duplicata. Hipótese: pares com a mesma intenção (ração filhote; brinquedos sozinho) diluem indexação. Ação: fundir os 2 pares achados e comparar todo tema novo com os publicados (J1). Métrica: 0 pares na fila; novos indexados em < 48 h (Search Console). Trocar: menos da metade indexada em 14 dias = reduzir ritmo e reforçar os já publicados.
   - JD3 clique de rede para o blog. Hipótese: o link no 1º comentário dos posts de hoje traz os cliques que o orgânico ainda não traz. Ação: link do artigo (UTM) no 1º comentário de todo post do dia (J10). Métrica: cliques do blog vindos das redes (GA4), leitura 1 h, 3 h e 72 h; meta ≥ 10 em 72 h. Trocar: 0 clique em 72 h por 2 rodadas = trocar o gancho do comentário, não o artigo.
   - JD4 cauda longa. Hipótese: disputar "melhor X" com loja grande (Petz, Cobasi) perde; comparação honesta por porte/idade/situação ganha. Ação: antes de aprovar tema, confirmar que as buscas óbvias do pilar já existem; depois escrever pela cauda específica (seção h, itens 1 e 4). Métrica: nº de óbvias do pilar cobertas; impressões da cauda longa no Search Console. Trocar: tema sem impressão em 72 h = ir para o tema óbvio seguinte.
4. LAÇO: data/habilidades/aprendizado/plataforma_google_seo_adsense.md, 1 linha por rodada: data | jogada | resultado n/métrica | mantém/altera/descarta. Número ruim = troca de jogada na mesma rodada.
5. JUIZ: biblioteca/habilidades/juiz_de_qualidade.md (Juiz de Qualidade, agente separado de quem produz; nota mínima 7 para ir ao vivo; ensaio aprovado = média ≥ 7 e nenhuma nota < 5).


## (a) Quando usar
Antes de aprovar tema, ao revisar rascunho, antes de publicar e antes de pedir revisão do AdSense. Não pesquisar a regra de novo: está aqui e em google.md.

## (b) Entradas
Rascunho (texto, imagens, links), pilar, raça citada, links Shopee/Cobasi, config/fila_temas.yaml, robots.txt, sitemap, Search Console (impressões, cliques, indexação).

## (c) Regras [C] → jogadas
Formato: fazer | alvo ou medir primeiro | condição de troca.

J1 (scaled content abuse: muitas páginas para ranquear é spam, mesmo com IA [C]). Fazer: antes de aprovar tema, comparar com os já publicados; dois temas que respondem a mesma pergunta viram um só. Alvo: 0 pares duplicados de intenção na fila; ritmo de publicação — medir primeiro: ler no Search Console, por 14 dias, quantos artigos novos foram indexados por semana. Troca: se menos da metade dos novos for indexada em 14 dias, reduzir o ritmo e reforçar os já publicados (reforcar_artigos.py) em vez de publicar mais.

J2 (thin affiliation: descrição copiada do lojista é spam; vale acrescentar preço, teste, comparação [C]). Fazer: todo artigo com link afiliado leva pelo menos 1 elemento próprio: comparação de 2+ produtos, critério de escolha ou experiência registrada; o link vai dentro do texto. Alvo: 100% dos artigos com afiliado têm o elemento; links por artigo — 1 a 3 (regra interna, não do Google). Troca: artigo só com lista de links = devolver ao redator.

J3 (E-E-A-T: confiança primeiro; autoria clara, perfil real, como foi feito, inclusive IA [C]). Fazer: byline com autor real ou marca assumida, link para página Sobre, linha curta "como produzimos" (rascunho com apoio de IA, revisado). Alvo: 53 de 53 artigos otimizados (nossa base em 22/10) com byline e página Sobre; novos 100%. Troca: perfil de autor fictício apresentado como pessoa real = remover (o Google trata como enganoso).

J4 (saúde/YMYL pede fonte [C]). Fazer: toda afirmação de saúde animal cita veterinário ou estudo no texto; sem fonte, reescrever como orientação geral. Alvo: 100% das afirmações de saúde com fonte. Troca: artigo de saúde sem fonte checável = não publica.

J5 (IA: conferir fatos, título, meta, alt e dados estruturados [C]). Fazer: revisão humana registrada após o rascunho de IA; checar a raça e os fatos. Alvo: 100% com registro de revisão. Troca: sem registro = UNKNOWN, tratar como FAIL.

J6 (conteúdo para pessoas; sinais de busca-primeiro: mudar datas, mirar contagem de palavras, requentar [C]). Fazer: nunca alterar a data de publicação sem mudança real; não esticar texto por tamanho. Alvo: data só muda com edição de conteúdo registrada. Troca: reforço de artigo antigo só com fato novo ou foto própria.

J7 (AdSense: conteúdo próprio e de qualidade, acesso ao HTML, políticas, maior de 18 anos [C]). Fazer: lista de prontidão antes de pedir revisão: domínio verificado, ads.txt 200, Sobre/Privacidade/Contato/Termos, 25+ artigos originais (nossa meta de 14/10), sitemap enviado. Alvo: 25 ou mais artigos úteis publicados e rastreáveis (hoje 53 otimizados; confirmar quantos estão no ar). Troca: se a conta reprovar, ler o motivo, corrigir tudo de uma vez, reaplicar só depois da correção.

J8 (AdSense: sem conteúdo raspado ou protegido por direitos autorais [C]). Fazer: varredura de trechos copiados e de imagens sem licença antes de pedir revisão. Alvo: 0 trechos copiados, 0 imagens sem origem registrada. Troca: item achado = troca ou remove antes do pedido.

J9 (doorway e site reputation abuse [C]). Fazer: não criar páginas por raça/cidade só para ranquear a mesma resposta; não aceitar guest post nem seção de parceiro sem relação com pet e sem edição nossa. Alvo: 0 páginas assim. Troca: página achada = fundir no artigo principal com redirecionamento.

J10 (cliques do blog como termômetro, dado nosso). Fazer: contar cliques do blog vindos das redes (1º comentário) em 72 h por rodada. Alvo: ≥10 cliques em 72 h (meta do plano de 22/10; linha-base 6 em 7 dias, 21/10). Troca: 0 em 72 h por 2 rodadas seguidas = rever o gancho do comentário, não o artigo.

## (f) Procedimento (PASS / FAIL / UNKNOWN)
1. Entrada: rascunho + ficha. Falta algo = UNKNOWN.
2. Valor próprio (J2/J5): existe 1 item que a busca genérica não dá? PASS/FAIL.
3. Cópia: trecho copiado? FAIL imediato (J8).
4. Raça/animal: imagem mostra a raça citada? PASS/FAIL.
5. Saúde: fonte no texto (J4). PASS/FAIL.
6. Intenção duplicada na fila (J1). PASS/FAIL.
7. Afiliado: elemento próprio, aviso visível, `rel="sponsored"` (prática interna). PASS/FAIL.
8. On-page: um H1, alt em toda imagem, 2+ links internos ao mesmo pilar, pilar válido, byline (J3).
9. Rastreio: fora do robots.txt, no sitemap, sem login. PASS/FAIL; "indexado" só com saída real do Search Console.
10. Decisão: publicar / devolver com lista completa / cortar tema.
11. Gravar a saída.

## (h) DEMANDA PRIMEIRO (Allan, 22/10/2026; caso "melhor assento para pet": Petz, Cobasi, Guia o Melhor, My Best, Justos aparecem, nós não)
Causa achada: nosso artigo de cinto (3.500 palavras) tinha "cadeirinha" e "assento" ZERO vezes, título sem acento, e não comparava as opções. Escrevemos pelo nosso vocabulário, não pelo da busca. Regra: tema e texto nascem do que as pessoas digitam, não do que achamos bom explicar.
1. Ordem dos temas: primeiro as buscas ÓBVIAS e de maior volume do nicho (o básico que todo tutor pergunta: quanto tempo sozinho, passeio, banho, ração, vacinas, castração, viagem de carro). Só depois especificidades (raça, idade, situação). Antes de aprovar um tema novo, confirmar que as óbvias do pilar já existem.
2. Por tema, antes de escrever: (a) pesquisar a consulta exata e 2 variações (sinônimo popular, forma em pergunta); (b) listar os 5 primeiros resultados e o TIPO de página (loja, comparador, blog de marca, notícia, fórum); (c) coletar o vocabulário: termos nos títulos e H2 dos concorrentes, perguntas relacionadas e sugestões de busca (no PC do Allan: Chrome com Google; na nuvem: WebSearch); (d) decidir o formato que ganha (comparação "A ou B", lista por porte/idade, passo a passo, tabela).
3. No artigo: o termo principal e o sinônimo popular no título (com acento), no H1, no 1º parágrafo e em 1-2 H2; resposta direta no começo; tabela de comparação quando a busca é de escolha ("X ou Y", "melhor"); seção de perguntas reais (FAQ) com as perguntas coletadas; 2+ links internos.
4. Nicho disputado por loja grande (ex.: "melhor X"): não disputar o termo seco; ir pela cauda longa específica (porte, idade, situação) e pela comparação honesta que a loja não faz.
5. Auditoria dos artigos já no ar: para cada slug, termo-alvo (termo_origem) x palavras que o título/H1/H2 realmente têm; se o sinônimo popular falta, ou não há comparação onde a busca é de escolha, reforçar (reforcar_artigos.py). Registrar em data/seo/auditoria_demanda.md: slug | termo-alvo | sinônimo ausente | ação.
6. Hashtag não existe como mecanismo no Google (só nas redes). O equivalente é: título/H1/meta com o termo, links internos entre artigos do pilar, sitemap enviado e página indexada no Search Console, dados estruturados (FAQ/Article), e link do artigo no 1º comentário dos posts.
7. Medir com dado (Search Console: consulta, impressão, posição, clique) assim que a propriedade for verificada; antes disso, medição só por SERP manual e GA4 (Organic Search).

## (i) TAMANHO DO ARTIGO: o que a regra diz (verificado em 22/10/2026)
- **Google Search Central** (Creating helpful, reliable, people-first content, developers.google.com/search/docs/fundamentals/creating-helpful-content): não define tamanho ideal, mínimo nem máximo. Na seção que trata de escrever para uma contagem, a página responde literalmente "Google has a preferred word count? (No, we don't.)". Os critérios são: útil para o público, mostra experiência e profundidade, o site tem foco claro, o leitor sai com o que precisava e com uma boa experiência.
- **AdSense** (Google Publisher Policies, support.google.com/adsense/answer/10502938): não define número de palavras nem de artigos. Proíbe anúncio em página sem conteúdo do editor ou de baixo valor, com mais anúncio do que conteúdo, ou com conteúdo copiado sem valor agregado.
- **Consequência para nós:** tamanho = o que for preciso para responder o tema por completo, sem encher e sem cortar. Qualquer número de palavras que usarmos é heurística interna de bom senso (Allan, 22/10: 300 é pouco; Curador bloqueia abaixo de 700 e avisa abaixo de 900), nunca regra do Google. O critério real do Juiz é utilidade, profundidade, originalidade, fontes e experiência do leitor.
- Jogada: ao escrever, medir a pergunta respondida (o leitor sai sabendo o que fazer?), não as palavras. Esticar texto por tamanho continua proibido (J6).

## (j) REGRA DE ESCRITA: PERGUNTAS PRIMEIRO (Allan, 22/10/2026)
1. Antes de escrever, transformar o tema em perguntas: 10 a 15 que as pessoas fazem de verdade (o que é, por que acontece, quando, como, quanto, qual a diferença, o que evitar, quando procurar o veterinário, o que fazer primeiro). Fontes das perguntas: busca do Google ("As pessoas também perguntam" e sugestões), FAQ de concorrentes, perguntas em comentários e em nossos dados do Search Console. Guardar a lista em `data/seo/perguntas/<slug>.md`.
2. O artigo se constrói respondendo a essas perguntas: praticamente cada frase ou parágrafo responde uma delas, direto na primeira frase, depois aprofunda (o porquê, o exemplo). Não precisa estar em formato pergunta-e-resposta; precisa ser construído a partir delas.
3. Muita informação útil, bem escrita, sem "blá blá blá" nem repetição. Fontes: citar com link (meta mínima 3 por artigo; mais quando o tema é saúde). Fonte estrangeira é bem-vinda, citada; ressalvar quando não há posição de entidade brasileira.
4. Juiz: conferir quantas das perguntas da lista o artigo responde (meta: todas as principais) e se há enrolação.
5. LACUNA conhecida: o escritor automático da nuvem não navega na web, então não consegue buscar perguntas nem fontes por conta própria. Até existir esse passo, artigo novo com fontes é feito por agente com busca (como o da roupa pet).

## (k) LINK DE AFILIADO NO BLOG ENQUANTO SOMOS CANDIDATOS AO ADSENSE (verificado em 22/10/2026)
- **Pode.** AdSense, "Use other ad networks together with AdSense" (support.google.com/adsense/answer/9728): "We do allow affiliate or limited-text links." Condições: seguir as Google Publisher Policies e a política de posicionamento, e nunca ter mais anúncio do que conteúdo na página (inventory value). Não é preciso que só o Google coloque propaganda; o que se proíbe é página de baixo valor.
- **Google Search, spam policies (thin affiliation):** estar em programa de afiliados não é violação. Violação é página que só copia a descrição e as avaliações do lojista, ou conteúdo repetido em vários sites. Afiliado é aceito quando agrega valor: comparação de produtos, avaliações originais, teste prático, navegação por categoria, informação extra de preço. Links de afiliado dentro de uma página são aceitos desde que bem marcados.
- **Marcação:** Google (Qualify outbound links) recomenda `rel="sponsored"` para link pago ou comercial (`nofollow` ainda funciona; `sponsored` é o preferido).
- **Nossas regras decorrentes:** (1) o produto só entra onde o próprio texto o recomenda e explica por quê (comparação, critério de escolha), nunca copiando texto de loja; (2) `rel="sponsored noopener"` e rótulo visível "link de afiliado" (+ nota de transparência no site); (3) nunca perto de bloco de anúncio e com muito mais conteúdo do que link; (4) limite por artigo: 1 bloco de 2 a 4 produtos, no fim do trecho relevante; (5) enquanto a candidatura ao AdSense estiver em análise, entrar com poucos artigos de afiliado (os 5 de escolha de produto) e medir; se a aprovação travar por "conteúdo de baixo valor", tirar os blocos na hora (jogada de troca).
- **Tese:** o que protege a aprovação é a utilidade do artigo, não a ausência de link. Quem trabalha as perguntas do leitor e compara de verdade tem afiliado aceito.

## (l) PERGUNTAS PRIMEIRO TAMBÉM NAS POSTAGENS (Allan, 22/10/2026)
Toda postagem em rede (vídeo, legenda, primeiro comentário) nasce de uma pergunta que as pessoas fazem e responde a ela logo no início; o gancho é a pergunta ou a resposta surpreendente, e o link leva ao artigo que responde às demais perguntas. As perguntas vêm da lista `data/seo/perguntas/<slug>.md` do artigo.

## (g) Saída obrigatória e laço
Linha em `data/habilidades/aprendizado/plataforma_google_seo_adsense.md`: `data | regra/jogada | resultado (n, métrica) | mantém/altera`. Sem a linha, a rodada conta como "não aplicou". 3 linhas com o mesmo padrão = propor edição (v, data, evidência). Sem releitura há 14 dias, tratar [C] como [N].

## Limites (regras de plataforma, validações e números de corte; não são jogadas)
Movido em 22/10/2026 para o fim: o que o agente FAZ está nas jogadas acima; aqui só o que ele não pode ultrapassar.

### (d) Validar antes de agir [N]
Texto do update de site reputation (ago/2026), core update de mar/2024, Discover (fev/2026); dados estruturados; Core Web Vitals; sitemap/robots em detalhe; posicionamento de anúncios (48182), processo de aprovação (9130038) e política de publisher (11035931), lidos só em 21/10; texto-padrão de divulgação de afiliado; `rel="sponsored"` como exigência (orientação geral, página não lida). Até a releitura, seguir como prática interna e não citar como regra do Google.

### (e) Limites de decisão com dados nossos
- Linha-base de cliques do blog: 6 em 7 dias (data/testes/baseline_2026-10-21.md); meta ≥10 em 72 h.
- Indexação e impressões: sem linha-base nossa — medir primeiro: exportar do Search Console por 14 dias, gravar em data/testes/. Até lá, nenhuma decisão de ritmo por "impressão baixa".
- Amostra: n < 3 artigos comparados = UNKNOWN.
