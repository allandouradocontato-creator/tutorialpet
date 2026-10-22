# Biblioteca de referências de design (início: 22/10/2026)
Regra: cada material novo consulta esta página e `paleta_tutorial_pet.md`. Skill: `biblioteca/habilidades/design_moderno_referencias.md`. Adaptar, nunca copiar (layout, texto, personagem, foto). Nova referência = 1 bloco no formato abaixo, com data e fonte.

## R001 — Kit de fichas visuais de adestramento (anúncio de Facebook)
- Fonte/data: anúncio de Facebook visto pelo Allan, 22/10/2026 (link e anunciante a registrar quando o Allan mandar; abrir pelo Chrome dele).
- O que é: kit de 150 fichas visuais de adestramento. Cada ficha: página com título grande; "Como fazer" em 4 passos com mini-fotos; "O que fazer / O que evitar"; "Dica extra". O reel do anúncio só folheia as fichas.
- Avaliação do Allan: o PRODUTO é bom modelo; o vídeo de venda é fraco.
- O que tem de novo: formato ficha de uma página, escaneável em segundos, fácil de imprimir/guardar; volume (150) comunica valor; folhear mostra o produto sem narrar.
- O que aproveitar: a estrutura de ficha (já é o nosso molde em `data/produtos/ficha_modelo/ficha.html`); passos com foto real; caixas fazer/evitar; dica extra; no vídeo, mostrar 3-4 fichas passando com ritmo e UMA ficha parada em close (resolve a fraqueza do vídeo deles: dar o gancho de dor nos 2 s iniciais, mostrar o resultado, CTA).
- O que NÃO copiar: layout idêntico, textos das fichas, fotos, nome/número do kit (150), identidade visual do anunciante; vídeo que só folheia sem gancho (é o ponto fraco apontado). Nossa ficha usa paleta própria e fotos reais licenciadas.
- Uso previsto: moldes de ficha do Manual Sozinho em Casa; teste A/B de capa de ficha (J3).

## R002 — Página imersiva do anúncio Upward Academy (curso Web Designer do Futuro, R$ 97)
- Fonte/data: anúncio visto pelo Allan, 22/10/2026 (página do curso; registrar link quando enviado).
- O que é: página de venda imersiva: seções de tela cheia em laranja vibrante; frases enormes que mudam conforme se rola a página; galeria horizontal; interação ligada à rolagem (scroll).
- O que o Allan quer: isso feito com IA no NOSSO site e app (Tutorial Pet / Sozinho em Casa).
- O que tem de novo: a página conta uma história por rolagem (1 ideia por tela), em vez de bloco de texto; frase gigante vira o gancho visual; galeria horizontal mostra prova/variedade sem alongar a página.
- O que aproveitar (tradução para nós): 
  - Seções de tela cheia com UMA frase gigante cada, usando o degradê/cores da paleta (laranja #ff6a00 já é nossa cor-base).
  - Frases que trocam ao rolar (CSS scroll-driven animations / IntersectionObserver, leve, sem biblioteca pesada).
  - Galeria horizontal (scroll-snap) para mostrar as fichas do manual com foto real.
  - Ordem sugerida da landing: dor (frase gigante) -> 4 passos de uma ficha -> galeria das fichas -> preço R$ 27 (âncora R$ 97) -> CTA.
  - Precisa carregar rápido no celular (mobile primeiro, sem vídeo pesado de fundo).
- O que NÃO copiar: textos, promessas de renda, estrutura exata de seções, laranja idêntico/identidade da Upward, qualquer imagem ou animação baixada da página deles; nada de depoimento ou número inventado. Prova só com dado real nosso.
- Uso previsto: protótipo da landing do Sozinho em Casa e do app; teste A/B: landing imersiva x landing atual, leitura de clique em horas (UTM por versão).

## Modelo de novo bloco (copiar)
- ID/fonte/data:
- O que tem de novo:
- O que aproveitar:
- O que NÃO copiar:
- Usada em (peça + data) / resultado do A/B:


## Links das referências (conferidos em 22/10/2026 no Chrome do Allan)
- R001: anunciante Pets.apaixonados, "Kit Cão Bem-Educado", https://www.facebook.com/reel/1108887845205327 (5,9 mil visualizações, 1 curtida; preço e link de venda não aparecem na página).
- R002: anunciante Upward Academy, curso "Web Designer do Futuro", R$ 97, 7 dias de garantia, https://www.facebook.com/reel/1413224080316538 (1,6 mil visualizações, 15 curtidas; reel sem áudio).
