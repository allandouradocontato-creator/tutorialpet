v2 — 22/10/2026 — status: rascunho até prova (régua 7)
base: biblioteca/regras_plataformas/google.md (v2, seções 1-3, 6, 7.1); config/prompts/seo.md; data/memoria/14 Blog e AdSense - aprendizados.md; data/seo_onpage/otimizados (53 artigos).

# Habilidade: artigo que passa no Google (SEO + AdSense + afiliado) — Agente de SEO, Redator, Revisor

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

## (d) Validar antes de agir [N]
Texto do update de site reputation (ago/2026), core update de mar/2024, Discover (fev/2026); dados estruturados; Core Web Vitals; sitemap/robots em detalhe; posicionamento de anúncios (48182), processo de aprovação (9130038) e política de publisher (11035931), lidos só em 21/10; texto-padrão de divulgação de afiliado; `rel="sponsored"` como exigência (orientação geral, página não lida). Até a releitura, seguir como prática interna e não citar como regra do Google.

## (e) Limites de decisão com dados nossos
- Linha-base de cliques do blog: 6 em 7 dias (data/testes/baseline_2026-10-21.md); meta ≥10 em 72 h.
- Indexação e impressões: sem linha-base nossa — medir primeiro: exportar do Search Console por 14 dias, gravar em data/testes/. Até lá, nenhuma decisão de ritmo por "impressão baixa".
- Amostra: n < 3 artigos comparados = UNKNOWN.

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

## (g) Saída obrigatória e laço
Linha em `data/habilidades/aprendizado/plataforma_google_seo_adsense.md`: `data | regra/jogada | resultado (n, métrica) | mantém/altera`. Sem a linha, a rodada conta como "não aplicou". 3 linhas com o mesmo padrão = propor edição (v, data, evidência). Sem releitura há 14 dias, tratar [C] como [N].
