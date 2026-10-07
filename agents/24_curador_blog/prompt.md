# Agente 24 — Curador do Blog (AdSense, E-E-A-T, SEO e compliance)

Papel: revisar sempre os artigos do blog e barrar o que o Google AdSense reprovaria. Não escreve nada: confere,
aponta e devolve um relatório (data/curador_blog/relatorio.md). Roda por regras, sem LLM (grátis e repetível).

Bloqueante (o artigo não está pronto):
- menos de 850 palavras (conteúdo raso);
- autor preenchido com nome de pessoa, persona ou personagem fictício (a assinatura é "Equipe Tutorial Pet");
- persona citada no título, no corpo ou no front-matter;
- menos de 2 links internos para outros artigos do site, ou link interno para página que não existe;
- sem seção de perguntas frequentes (3 a 5 perguntas) ou sem "Para fechar";
- alegação de credencial ("sou veterinário"), estudo/estatística inventados;
- tema de saúde sem orientação de procurar o médico-veterinário.

Aviso: acima de 1.600 palavras, título acima de 70 caracteres, meta description fora de 60–160 caracteres,
menos de 4 seções H2, parágrafo acima de 130 palavras.

Fora do artigo (conferir a cada rodada semanal): páginas Sobre, Contato, Privacidade e Termos; ads.txt e robots.txt;
aviso de cookies; política editorial; sitemap com todos os artigos.
