# Regras das plataformas Google — Tutorial Pet (v2)

v2 de 22/10/2026 (v1 de 21/10/2026). Guia para agentes lerem ANTES de publicar artigo ou rodar anúncio. Paráfrase, sem citação longa.
Marcação: [C] = lido nesta consulta (22/10/2026) na página oficial citada. [N] = não confirmado: ou só título visto, ou lido apenas na v1 (21/10) e ainda não relido. [N] nunca decide sozinho; vai para "validar antes de agir" nas skills.
YouTube saiu deste arquivo: ver `youtube.md`.

---

## 1. Resumo
1. IA pode ajudar a escrever, mas o texto final precisa de valor próprio, revisão e checagem de fatos [C].
2. Gerar muitas páginas para manipular ranking é spam, com ou sem IA (scaled content abuse) [C].
3. Página de afiliado sem conteúdo original (descrição copiada do lojista) é spam "thin affiliation" [C].
4. Doorway: páginas parecidas feitas para ranquear consultas semelhantes e empurrar para outra página [C].
5. Site reputation abuse: terceiro hospedado só pela força do domínio [C]; houve atualização em agosto/2026 cujo texto não foi lido [N].
6. AdSense: conteúdo próprio, de qualidade, acesso ao HTML, cumprir políticas, maior de 18 anos [C].
7. Google Ads: destino que funciona, corresponde ao anúncio, rastreável pelo AdsBot e com conteúdo original [C].
8. Personalização de saúde, verificação de CNPJ e dados pessoais: lidos na v1, ainda a reler [N].
9. Cada artigo que cita raça mostra aquela raça (regra da marca, não do Google).

---

## 2. ADSENSE
### 2.1 Elegibilidade (support.google.com/adsense/answer/9724, 22/10/2026) [C]
- Mínimo 18 anos (menor precisa de responsável adulto).
- Conteúdo seu, de alta qualidade, original, que atraia público.
- Acesso ao código HTML do site.
- Cumprir as políticas do programa, que mudam; manter-se atualizado é responsabilidade do publisher.

### 2.2 Preparar o site (support.google.com/adsense/answer/7299563, 22/10/2026) [C]
- Conteúdo único e relevante, com algo seu: conhecimento, avaliação, perspectiva.
- Cautela com artigos ou vídeos alheios incorporados; anúncios não vão em site com conteúdo raspado ou protegido por direitos autorais, sob pena de anúncios desativados ou conta encerrada.
- Navegação clara, menus funcionando, texto legível; comentários, se houver, moderados.
- Revisar as políticas do programa, as de publisher e as de spam do Search antes de se inscrever.
- A página não define "baixo valor" com números; a ideia central é originalidade.

### 2.3 Posicionamento de anúncios (answer/48182, "Políticas do programa AdSense") [N: lido na v1 em 21/10, não relido]
- Anúncio não pode parecer menu, link de navegação ou botão de download; rótulo só "Publicidade/Anúncios"; sem seta ou imagem chamando clique; sem pop-up; nunca clicar no próprio anúncio.

### 2.4 Processo de aprovação (answer/9130038) [N: v1]
- Site na aba Sites, verificação de posse (snippet, ads.txt ou meta tag), revisão de dias a 2-4 semanas, só pedir revisão com tudo publicado e rastreável.

### 2.5 O que derruba [C/N]
- Conteúdo copiado ou raspado [C, answer/7299563]. Cliques artificiais, bloqueio por robots.txt ou login impedindo a avaliação [N, v1].

---

## 3. GOOGLE SEARCH
### 3.1 Políticas de spam (developers.google.com/search/docs/essentials/spam-policies, 22/10/2026) [C]
- **Scaled content abuse:** muitas páginas feitas principalmente para ranquear, sem ajudar o usuário. Exemplos: IA gerando muitas páginas sem valor, raspar e reescrever ou traduzir conteúdo alheio, costurar trechos de outras páginas, vários sites para esconder a escala. Consequência: cair no ranking ou sair dos resultados.
- **Site reputation abuse:** conteúdo de terceiros hospedado principalmente pela força do domínio. Não é abuso: agências de notícias, sindicação, conteúdo de usuários, trabalho editorial, publieditorial para o leitor e links de afiliado tratados de forma adequada. Fora do EEE pode haver ação manual; avisos chegam pelo Search Console.
- **Thin affiliation:** descrições e avaliações copiadas do lojista, sem valor agregado. Boas práticas citadas: preço, avaliações originais, testes, comparações, navegação por categoria.
- **Doorway:** páginas ou sites feitos para ranquear consultas parecidas e funilar o usuário; inclui páginas por cidade ou região que levam à mesma página.
- Atualização "Update to the Site Reputation Policy" (agosto/2026, developers.google.com/search/blog/2026/08/update-site-reputation-policy): só o título e o mês foram vistos; texto não lido [N].

### 3.2 Conteúdo útil e E-E-A-T (developers.google.com/search/docs/fundamentals/creating-helpful-content, 22/10/2026) [C]
- O ranking busca conteúdo útil e confiável feito para pessoas.
- Sinais de conteúdo para buscador, não para pessoas: produzir em massa por automação, requentar o trabalho alheio, perseguir tendência, mudar datas artificialmente, mirar contagem de palavras.
- Confiança é o elemento mais importante do E-E-A-T; E-E-A-T não é fator de ranking direto; pesa mais em temas de saúde, finanças e segurança (YMYL).
- Quem: autoria clara, perfil real, link para página do autor. Como: explicar como foi feito, inclusive uso de IA; em avaliação de produto, quantos foram testados, como, com fotos. Por quê: criar para ajudar pessoas.
- Mostrar fontes, histórico do autor, páginas Sobre; sem erros factuais fáceis de verificar.

### 3.3 IA generativa (developers.google.com/search/docs/fundamentals/using-gen-ai-content, 22/10/2026) [C]
- IA serve para pesquisar e estruturar conteúdo original; em massa e sem valor viola scaled content abuse.
- Checar fatos de tudo, inclusive título, meta description, dados estruturados e alt de imagem.
- Dizer ao leitor como o conteúdo foi feito. Imagens geradas por IA levam o metadado IPTC DigitalSourceType = TrainedAlgorithmicMedia (orientação dada para comércio eletrônico; vale como boa prática).

### 3.4 Ainda não lido [N]
- Dados estruturados (Article, FAQPage, Product), Core Web Vitals, sitemap/robots em detalhe, Discover Core Update de fev/2026, o texto do anúncio de março/2024.

---

## 5. GOOGLE ADS
### 5.1 Destino/landing (support.google.com/adspolicy/answer/6368661 e answer/16427718, 22/10/2026) [C]
- A página e seu conteúdo precisam funcionar nos navegadores e aparelhos comuns; erro HTTP para o AdsBot reprova.
- Domínio do anúncio deve bater com o da página final; redirecionar para outro domínio não é permitido; URL com rastreio leva ao mesmo conteúdo.
- Precisa ser rastreável pelo AdsBot e acessível no local de exibição.
- Experiência fácil e segura: sem navegação confusa, sem download direto, sem experiência abusiva.
- Conteúdo original e de valor: reprova página feita para mostrar anúncios, cópia sem valor, redirecionadora, "em construção" ou vazia.
- Violação não suspende na hora: aviso pelo menos 7 dias antes da suspensão da conta.

### 5.2 Personalização de saúde (answer/16701855) [N: v1]
- Saúde é categoria sensível: sem Customer Match, segmentos próprios ou lookalike; sem texto que adivinhe condição; menor de 18 sem personalização; públicos predefinidos continuam permitidos.

### 5.3 Medicamentos veterinários (answer/13557942) [N: v1]
- Regra trata de medicamento com prescrição; certificação citada para EUA e Canadá; Brasil não confirmado. Não se aplica a conteúdo comportamental.

### 5.4 Dados pessoais (answer/1283115) [N: v1]
- Documentos, cartão e dados bancários só por conexão segura (HTTPS).

### 5.5 Verificação de anunciante no Brasil (google-ads/answer/14886971) [N: v1]
- Pessoa jurídica informa CNPJ regular na Receita; registro novo leva 3 a 5 dias úteis; usar o CNPJ da Dourado Falcão Educação Corporativa LTDA, não CPF pessoal.

---

## 6. AFILIADOS NOS ARTIGOS
- Thin affiliation [C, 3.1]: cada artigo com link Shopee/Cobasi traz texto, teste, comparação ou preço próprios.
- `rel="sponsored"` e aviso de divulgação visível: prática interna e orientação geral do Search sobre links patrocinados; página específica não lida nesta consulta [N].
- 1 a 3 links por artigo, dentro do contexto: regra interna, não do Google.

---

## 7. CHECKLISTS (sim/não; qualquer "não" bloqueia)
### 7.1 Artigo
1 valor próprio; 2 raça correta; 3 revisado depois da IA e fatos checados; 4 sem cópia; 5 autoria visível e como foi feito (inclui uso de IA); 6 aviso de afiliado; 7 rel=sponsored; 8 mais que lista de links; 9 fora do robots.txt; 10 título/meta honestos; 11 imagens próprias ou claramente ilustrativas; 12 fonte em afirmação de saúde.
### 7.2 Google Ads
1 sem Customer Match/lookalike; 2 texto sem adivinhar condição; 3 menores sem personalização; 4 destino = anúncio, mesmo domínio, sem redirecionar para outro; 5 AdsBot consegue abrir; 6 privacidade visível; 7 checkout HTTPS; 8 CNPJ validado; 9 saúde animal checada; 10 conferir painel em 24 h e 72 h.

---

## 8. Fontes
Lidas em 22/10/2026 (base das marcas [C]): support.google.com/adsense/answer/9724 e 7299563; developers.google.com/search/docs/essentials/spam-policies, /fundamentals/creating-helpful-content, /fundamentals/using-gen-ai-content; support.google.com/adspolicy/answer/6368661 e 16427718.
Lidas em 21/10/2026 e não relidas (marcadas [N]): adsense/answer/48182, 9130038; adspolicy/answer/16701855, 13557942, 1283115; google-ads/answer/14886971; publisherpolicies/answer/11035931.
Só título visto: developers.google.com/search/blog/2026/08/update-site-reputation-policy; /2024/03/core-update-spam-policies; /2026/02/discover-core-update; adspolicy/answer/6020955 (deturpação) e 16427615 (experiência do destino).
