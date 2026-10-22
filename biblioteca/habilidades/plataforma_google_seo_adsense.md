---
versao: 1.0
data: 2026-10-22
base: biblioteca/regras_plataformas/google.md (seções 2, 3, 6, 7.1); config/prompts/seo.md
---
# Habilidade: artigo que passa no Google (SEO + AdSense + afiliado) — Agente de SEO, Redator, Revisor

## (a) Quando usar / quem lê
Antes de aprovar tema, ao revisar rascunho, antes de publicar e antes de pedir revisão do AdSense. Lê: Agente de SEO, Redator de artigos, Revisor/Auditor de Processo. Não pesquisar a regra de novo: está aqui.

## (b) Entradas que precisa
Rascunho do artigo (texto, imagens, links), pilar, raça/animal citado, links afiliados (Shopee/Cobasi), `config/fila_temas.yaml`, `robots.txt` e sitemap atuais.

## (c) Procedimento
1. **Valor próprio (PASS/FAIL).** O artigo traz pelo menos 1 item que uma busca genérica não entrega: opinião/experiência da Duda, dado atualizado com fonte, mídia própria ou passo prático testado. Nenhum = FAIL: devolve ao redator, não publica.
2. **Cópia.** Reescrita raspada ou parágrafo copiado de outro site = FAIL imediato (AdSense: conteúdo copiado).
3. **Raça/animal.** Se cita raça, a imagem/vídeo mostra aquela raça. Imagem de outra raça = FAIL. Banco de imagem genérico passando por foto real da marca = FAIL.
4. **Saúde animal.** Afirmação de saúde precisa de fonte (veterinário/estudo) citada no texto. Sem fonte = reescreve como orientação geral ou remove. Nunca diagnosticar nem indicar medicamento.
5. **Revisão humana.** Rascunho de IA só sai após edição que acrescente algo próprio. Sem registro de revisão = UNKNOWN, tratar como FAIL.
6. **Escala (scaled content abuse).** Limite de ritmo: não publicar vários artigos no mesmo dia só para volume; cada tema novo tem intenção de busca distinta (se dois artigos respondem a mesma pergunta, junta). Se a fila tem muitos temas quase iguais, corta e mantém o melhor.
7. **Thin affiliate.** Artigo com link afiliado: texto próprio substancial além do link; 1 a 3 links, dentro do contexto, nunca lista solta. Só lista de links = FAIL.
8. **Divulgação.** Aviso curto ("este artigo contém link de afiliado") no topo ou perto do primeiro link, visível. Todo link Shopee/Cobasi com `rel="sponsored"` (aceitável `nofollow`; preferir sponsored, ou `sponsored nofollow`). Falta de qualquer um = FAIL, nenhum artigo entra na fila sem isso (config/prompts/seo.md).
9. **On-page.** Título e meta description que não prometem o que o texto não entrega; um H1; H2/H3 em ordem; alt em toda imagem; 2+ links internos para o mesmo pilar; pilar só entre alimentacao, comportamento, cuidados_diarios, primeiros_passos_filhotes, produtos_compras.
10. **Rastreio.** Página fora do `robots.txt`, presente no sitemap, sem login. Bloqueada = FAIL (AdSense não avalia e Google não indexa).
11. **Anúncios (quando AdSense ativo).** Nenhum anúncio parecendo menu/botão de download; rótulo só "Publicidade/Anúncios"; sem seta ou imagem chamando clique; nunca clicar no próprio anúncio (nem para testar); sem pop-up.
12. **Aprovação AdSense.** Pedir revisão só quando: site cadastrado e domínio verificado (snippet, ads.txt ou meta tag), páginas Sobre/Privacidade/Contato publicadas, artigos publicados acessíveis aos rastreadores e sem FAIL nos passos 1-10. Prazo normal: dias, até 2-4 semanas; não reenviar antes disso. Se reprovar, ler o motivo, corrigir tudo de uma vez e só então pedir nova revisão.
13. **Decisão final do ciclo:** publicar / devolver com lista completa de correções / cortar tema. Relatório sem uma dessas três é falha.

## (d) Checklist antes de publicar (sim/não; qualquer "não" bloqueia)
1 valor próprio; 2 raça correta; 3 revisão humana; 4 sem cópia; 5 aviso de afiliado; 6 rel=sponsored; 7 não é só link; 8 fora do robots; 9 título/meta honestos; 10 imagens autorais ou claramente ilustrativas; 11 fonte em afirmação de saúde; 12 alt e links internos.

## (e) Erros comuns e o que NÃO fazer
- Não publicar direto o texto da IA. Não encher de keywords. Não criar página só para ranquear (doorway).
- Não aceitar guest post ou seção "parceiro" sem relação com pet e sem supervisão editorial (site reputation abuse).
- Não esconder link afiliado como link editorial comum. Não inflar quantidade de artigos para "ganhar" o AdSense.
- Não dizer "indexado" sem conferir a saída real (site: ou Search Console).

## (f) Laço de aprimoramento
Ao fim de cada ciclo, acrescentar em `data/habilidades/aprendizado/plataforma_google_seo_adsense.md` uma linha: `data | hipótese | resultado (n, métrica) | mantém/altera regra`. Métricas: artigos indexados em 7 dias, impressões/cliques no Search Console, motivo de reprovação AdSense. Quando 3 linhas confirmarem o mesmo padrão, propor a edição desta skill (subir versão e data no topo) e registrar em registro_de_falhas.md se for lacuna.

## (g) Validar antes de gastar (não confirmado em fonte oficial)
- Texto integral das políticas AdSense (1346295), do core update de março/2024 e da orientação de IA de 2023: reler antes de decisão sensível.
- Schema (Article, FAQPage, Product/Review em JSON-LD): boa prática, não confirmada em developers.google.com.
- Core Web Vitals (LCP, INP): direção conhecida, sem limites numéricos confirmados aqui.
- Texto-padrão de divulgação de afiliado e quantidade ideal de links (1-3 é prática interna).
- Critérios do Discover (update de fev/2026).
