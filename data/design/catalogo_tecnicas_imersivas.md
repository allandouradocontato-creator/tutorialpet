---
criado: 2026-10-22
versao: v1 - 22/10/2026
status: rascunho até prova (régua 7), snippets testados em Chromium 390x844 com Playwright
fonte_interna: biblioteca/habilidades/design_moderno_referencias.md, data/design/paleta_tutorial_pet.md
---
# Catálogo de técnicas imersivas (páginas dinâmicas) - Tutorial Pet

Ordem do Allan (22/10/2026): aplicar a TÉCNICA de páginas imersivas/dinâmicas feitas por IA. Aqui entra só a lógica (estrutura, ritmo, interação); nada de copiar anúncio, layout, texto ou página de terceiros. Cores e fonte vêm da paleta oficial (Poppins, #ff6a00, #b026ff, #00d46a, #e6ff00, #1b1b3a). Público é o tutor adulto; sem alegação médica/veterinária; sem urgência falsa; "cão" nunca em gancho.

Como foi testado: cada trecho abaixo é uma página completa e mínima, aberta em Chromium (headless shell) com viewport 390x844, toque ativado, e também com `prefers-reduced-motion: reduce` emulado. Medidas de script/layout: 40 passos de rolagem com CPU limitada a 4x mais lenta (celular médio). Pesos são do trecho (sem a fonte e sem imagens), em bytes brutos e gzip. Zero erros de página em todos.

Cada técnica: o que é | quando usar (Sozinho em Casa e upsells) | código | peso | custo no celular | fallback.

## 1. Entrada ao rolar (IntersectionObserver)
- **O que é:** Elemento fica invisível e sobe 24 px ao entrar na tela; o observer dispara uma vez e para de observar.
- **Quando usar:** Sozinho em Casa: título e prova de cada seção da página de vendas; upsell: bloco "o que você leva a mais". Base de quase todas as outras técnicas.
- **Peso:** 0,5 KB (343 B gzip)
- **Custo no celular:** Baixo: 1,1 ms de script em 40 passos de rolagem com CPU 4x mais lenta; só opacity/transform (GPU).
- **Fallback / reduced-motion:** Bloco `prefers-reduced-motion` mostra tudo já visível, sem transição. Sem JS também deve aparecer: coloque a classe `rv` via JS (`document.documentElement.classList.add("js")` e `.js .rv{...}`) se a página precisar funcionar sem script.

```html
<style>
.rv{opacity:0;transform:translateY(24px);transition:opacity .5s,transform .5s}
.rv.on{opacity:1;transform:none}
@media (prefers-reduced-motion:reduce){.rv{opacity:1;transform:none;transition:none}}
</style>
<div style="height:900px">topo</div><p class=rv id=a>Entrou na tela</p><div style="height:900px"></div>
<script>
const io=new IntersectionObserver(es=>es.forEach(e=>{if(e.isIntersecting){e.target.classList.add('on');io.unobserve(e.target)}}),{threshold:.2});
document.querySelectorAll('.rv').forEach(el=>io.observe(el));
</script>
```

## 2. Animação ligada à rolagem (CSS scroll-timeline) + fallback JS
- **O que é:** A barra de progresso cresce conforme a rolagem usando `animation-timeline:scroll()`, sem JS no Chromium moderno; o JS só roda onde não há suporte (Safari antigo).
- **Quando usar:** Sozinho em Casa: barra de progresso da leitura da página longa (dá sensação de "falta pouco" até a oferta); upsell: barra no checkout do bump.
- **Peso:** 0,7 KB (440 B gzip)
- **Custo no celular:** Mínimo: roda no compositor, 0 ms de JS no caminho feliz. O fallback usa listener passivo.
- **Fallback / reduced-motion:** Reduced-motion esconde a barra (`display:none`). `@supports` garante que quem não tem a API cai no JS.

```html
<style>
.bar{position:fixed;top:0;left:0;height:6px;width:100%;background:#ff0a6c;transform-origin:0 50%;transform:scaleX(0);z-index:9}
@supports (animation-timeline:scroll()){
 .bar{animation:grow linear both;animation-timeline:scroll(root)}
 @keyframes grow{to{transform:scaleX(1)}}
}
@media (prefers-reduced-motion:reduce){.bar{display:none}}
</style>
<div class=bar id=bar></div><div style="height:3000px">rola</div>
<script>
if(!CSS.supports('animation-timeline','scroll()')){ // fallback JS
 const b=document.getElementById('bar');
 addEventListener('scroll',()=>{b.style.transform='scaleX('+scrollY/(document.documentElement.scrollHeight-innerHeight)+')'},{passive:true});
}
</script>
```

## 3. Seções de tela cheia com frases grandes que trocam
- **O que é:** Cada frase ocupa uma tela (100svh), encaixa com scroll-snap `proximity` (não prende o dedo) e aparece quando 60% está visível. Funciona como "storytelling" de 3-5 telas.
- **Quando usar:** Sozinho em Casa: abertura da página de vendas em 3 telas (dor, empatia, promessa) antes do preço. Upsell: 2 telas (ganho extra, prazo). Frases em Poppins 900, fundo da paleta, texto branco só sobre laranja/roxo.
- **Peso:** 0,9 KB (549 B gzip)
- **Custo no celular:** Baixo a médio: 3,2 ms de script no teste; custo real é pintar fundos grandes, então use cores chapadas, não fotos pesadas.
- **Fallback / reduced-motion:** Reduced-motion desliga snap e mostra o texto sem animação. Use `proximity`, nunca `mandatory` no eixo vertical (trava rolagem em telas curtas).

```html
<style>
html{scroll-snap-type:y proximity}
.fs{min-height:100svh;display:grid;place-items:center;padding:24px;box-sizing:border-box;scroll-snap-align:start;
 font:900 clamp(32px,10vw,56px)/1.05 Poppins,Nunito,Arial,sans-serif;text-align:center;background:#ff6a00;color:#fff}
.fs:nth-child(even){background:#b026ff}
.fs span{opacity:0;transform:scale(.92);transition:.5s}
.fs.on span{opacity:1;transform:none}
@media (prefers-reduced-motion:reduce){html{scroll-snap-type:none}.fs span{opacity:1;transform:none;transition:none}}
</style>
<section class=fs><span>Ele chora quando você sai?</span></section>
<section class=fs><span>Você não está sozinho nisso.</span></section>
<section class=fs><span>Veja o passo 1.</span></section>
<script>
const io=new IntersectionObserver(es=>es.forEach(e=>e.target.classList.toggle('on',e.isIntersecting)),{threshold:.6});
document.querySelectorAll('.fs').forEach(s=>io.observe(s));
</script>
```

## 4. Galeria horizontal com scroll-snap
- **O que é:** Carrossel feito só com CSS: o dedo arrasta e o cartão encaixa no centro. Sem biblioteca. (Teste: rolagem de 425 px terminou encaixada em 543 px, no cartão 3.)
- **Quando usar:** Sozinho em Casa: prints do conteúdo do e-book, antes/depois, depoimentos reais com autorização. Upsell: "o que vem no pacote". Mostra 20% do próximo cartão para sinalizar que dá para arrastar.
- **Peso:** 0,5 KB (317 B gzip) mais as imagens (use WebP, 40-60 KB cada, `loading=lazy`)
- **Custo no celular:** Baixo: rolagem nativa no compositor; o peso está só nas imagens.
- **Fallback / reduced-motion:** Já é estático e funciona sem JS. Reduced-motion: sem `scroll-behavior:smooth`. Adicione `aria-label` na galeria.

```html
<style>
.g{display:flex;gap:12px;overflow-x:auto;scroll-snap-type:x mandatory;padding:0 16px;scrollbar-width:none;-webkit-overflow-scrolling:touch}
.g::-webkit-scrollbar{display:none}
.g>div{flex:0 0 78%;aspect-ratio:4/5;scroll-snap-align:center;border-radius:20px;background:#00d9ff;display:grid;place-items:center;font-weight:900}
@media (prefers-reduced-motion:reduce){.g{scroll-behavior:auto}}
</style>
<div class=g id=g><div>1</div><div>2</div><div>3</div><div>4</div></div>
```

## 5. Parallax leve
- **O que é:** O fundo se move a 15% da velocidade da rolagem (translate3d via requestAnimationFrame, listener passivo). Só no topo, só 1 camada.
- **Quando usar:** Sozinho em Casa: faixa em degradê do topo da página e capa. Upsell: nenhuma (não compensa). Use no máximo 1 por página.
- **Peso:** 0,6 KB (419 B gzip)
- **Custo no celular:** Médio-baixo: 4,4 ms de script em 40 passos a 4x de CPU, a maior das técnicas JS. Nunca use `background-attachment:fixed` (quebra no iOS e repinta tudo).
- **Fallback / reduced-motion:** Com reduced-motion o listener nem é registrado (verificado: nenhum transform aplicado).

```html
<style>
.hero{height:60vh;overflow:hidden;position:relative;background:#1b1b3a}
.hero i{position:absolute;inset:-12% 0;background:linear-gradient(135deg,#ffa800,#ff0a6c);will-change:transform}
@media (prefers-reduced-motion:reduce){.hero i{transform:none!important}}
</style>
<div class=hero><i id=p></i></div><div style="height:2000px"></div>
<script>
const p=document.getElementById('p');let t=0;
if(!matchMedia('(prefers-reduced-motion:reduce)').matches)
addEventListener('scroll',()=>{if(!t)t=requestAnimationFrame(()=>{p.style.transform='translate3d(0,'+(scrollY*.15)+'px,0)';t=0})},{passive:true});
</script>
```

## 6. Contador / relógio que avança ao rolar
- **O que é:** O número sobe de 0 até o valor quando 60% do elemento aparece (1,2 s, rAF). Testado: 0 -> 8.
- **Quando usar:** Sozinho em Casa: "8 horas sozinho por dia" (dor) e "4 passos" (solução), contador de dias da garantia. Upsell: contagem de itens do bônus. Regra do Allan: sem urgência falsa; só números verdadeiros.
- **Peso:** 0,7 KB (447 B gzip)
- **Custo no celular:** Baixo: 1 elemento, 72 quadros de texto; evite contadores grandes simultâneos.
- **Fallback / reduced-motion:** Reduced-motion mostra o valor final direto. Mantenha o valor final no HTML (`<span>8</span>`) e zere só via JS, para quem não tem script.

```html
<style>.c{font:900 64px Poppins,Arial,sans-serif;text-align:center;padding:40px 0}</style>
<div style="height:900px"></div>
<div class=c><span id=n data-to=8 data-fmt="h">0</span> horas sozinho</div><div style="height:900px"></div>
<script>
const n=document.getElementById('n'),to=+n.dataset.to;
const run=()=>{if(matchMedia('(prefers-reduced-motion:reduce)').matches){n.textContent=to;return}
 const t0=performance.now();(function f(t){const k=Math.min((t-t0)/1200,1);n.textContent=Math.round(to*k);if(k<1)requestAnimationFrame(f)})(t0)};
new IntersectionObserver((es,o)=>{if(es[0].isIntersecting){run();o.disconnect()}},{threshold:.6}).observe(n);
</script>
```

## 7. Cards que entram em sequência
- **O que é:** A lista dispara uma vez e cada card atrasa 90 ms a mais usando a variável CSS `--i` (efeito cascata sem JS por card).
- **Quando usar:** Sozinho em Casa: os 4 passos "Como fazer" (cada um na cor da paleta), lista de benefícios. Upsell: 3 bônus.
- **Peso:** 0,7 KB (411 B gzip)
- **Custo no celular:** Baixo: 0,1 ms de script, 1,3 ms de layout; limite a 6 cards para a cascata não passar de 0,5 s.
- **Fallback / reduced-motion:** Reduced-motion: cards visíveis sem atraso. Teste: 4 cards chegaram a opacity 1.

```html
<style>
.cd{margin:12px 16px;padding:16px;border-radius:16px;background:#e6ff00;opacity:0;transform:translateY(20px);
 transition:opacity .4s,transform .4s;transition-delay:calc(var(--i)*90ms)}
.in .cd{opacity:1;transform:none}
@media (prefers-reduced-motion:reduce){.cd{opacity:1;transform:none;transition:none}}
</style>
<div style="height:900px"></div>
<div id=l><div class=cd style=--i:0>Passo 1</div><div class=cd style=--i:1>Passo 2</div><div class=cd style=--i:2>Passo 3</div><div class=cd style=--i:3>Passo 4</div></div>
<div style="height:900px"></div>
<script>
const l=document.getElementById('l');
new IntersectionObserver((e,o)=>{if(e[0].isIntersecting){l.classList.add('in');o.disconnect()}},{threshold:.3}).observe(l);
</script>
```

## 8. Botão de compra fixo
- **O que é:** Botão fixo embaixo, respeitando a área segura do iPhone; some (desliza para fora) quando a oferta final já aparece na tela, para não duplicar. Testado: classe `off` ao chegar na oferta.
- **Quando usar:** Sozinho em Casa: aparece desde a 2ª tela até a oferta. Upsell: botão fixo "Sim, quero" com "Não, obrigado" como link discreto no fim da página. Texto do botão = ação + produto, sem prometer cura/resultado médico.
- **Peso:** 0,8 KB (508 B gzip)
- **Custo no celular:** Baixíssimo: 0 ms de script; o observer só alterna uma classe. Cuidado: cobre conteúdo, por isso `padding-bottom` no body.
- **Fallback / reduced-motion:** Reduced-motion tira a transição. O botão é um link comum, funciona sem JS (o JS só o esconde).

```html
<style>
.buy{position:fixed;left:12px;right:12px;bottom:calc(12px + env(safe-area-inset-bottom));z-index:9;display:block;text-align:center;
 padding:16px;border-radius:14px;background:#00d46a;color:#1b1b3a;font-weight:800;text-decoration:none;transition:transform .3s}
.buy.off{transform:translateY(150%)}
body{padding-bottom:88px}
@media (prefers-reduced-motion:reduce){.buy{transition:none}}
</style>
<div style="height:1800px">conteúdo</div><section id=fim style="height:300px;background:#ffe600">Oferta final (botão grande aqui)</section>
<a class=buy id=b href="#fim">Quero o Sozinho em Casa</a>
<script>
new IntersectionObserver(e=>document.getElementById('b').classList.toggle('off',e[0].isIntersecting)).observe(document.getElementById('fim'));
</script>
```

## 9. Reação a toque e mouse (inclinar o cartão)
- **O que é:** O cartão inclina até 7 graus seguindo o ponteiro (`pointermove`, funciona para dedo e mouse); volta ao sair. `touch-action:pan-y` mantém a rolagem vertical livre.
- **Quando usar:** Sozinho em Casa: capa do e-book e selo de garantia. Upsell: cartão do bônus. Efeito decorativo: nunca para coisa essencial, pois no celular só reage com o dedo em cima.
- **Peso:** 0,7 KB (440 B gzip)
- **Custo no celular:** Baixo: calcula só durante o gesto; usa `will-change:transform` em 1 elemento (não em vários).
- **Fallback / reduced-motion:** Com reduced-motion os listeners não são registrados (CSS com transição zerada). Teste: rotateY 6,3 deg / rotateX 5,6 deg.

```html
<style>
.tilt{width:240px;height:160px;margin:60px auto;border-radius:20px;background:linear-gradient(135deg,#ffa800,#ff0a6c);transition:transform .15s;will-change:transform;touch-action:pan-y}
@media (prefers-reduced-motion:reduce){.tilt{transition:none}}
</style>
<div class=tilt id=t></div>
<script>
const t=document.getElementById('t');
if(!matchMedia('(prefers-reduced-motion:reduce)').matches){
 t.addEventListener('pointermove',e=>{const r=t.getBoundingClientRect(),x=(e.clientX-r.left)/r.width-.5,y=(e.clientY-r.top)/r.height-.5;
  t.style.transform='perspective(600px) rotateY('+x*14+'deg) rotateX('+-y*14+'deg)'});
 t.addEventListener('pointerleave',()=>t.style.transform='');
}
</script>
```

## 10. Vídeo de fundo leve
- **O que é:** O vídeo só começa a baixar quando entra na tela, não carrega com dados economizados nem em 2G, e fica escondido com reduced-motion. Poster/fundo sólido aparece antes.
- **Quando usar:** Sozinho em Casa: loop curto (3-5 s) de cachorro/tutor calmo na 1ª dobra de uma página de captura; só com vídeo real de banco livre com licença. Upsell: não usar. Nas redes continua valendo "só vídeo"; aqui é página, então o vídeo é opcional.
- **Peso:** 0,6 KB de código + vídeo: alvo 400-700 KB (720x1280, H.264, 3-5 s, sem áudio, `ffmpeg -an -crf 30`). Nunca acima de 1 MB.
- **Custo no celular:** Médio-alto: decodificar vídeo gasta bateria e CPU; é a técnica mais cara. Nunca na 1ª dobra se o LCP for o alvo (o poster é o LCP).
- **Fallback / reduced-motion:** Dados economizados/2G/reduced-motion: só o poster. `muted`+`playsinline` são obrigatórios para tocar no iOS. Teste: src só carregou na entrada da tela; display:none com reduced-motion.

```html
<style>.bg{position:relative;height:50vh;background:#1b1b3a url(data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7) center/cover}
.bg video{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;opacity:0;transition:opacity .6s}.bg video.ok{opacity:1}
@media (prefers-reduced-motion:reduce){.bg video{display:none}}</style>
<div class=bg><video id=v muted loop playsinline preload=none poster="" data-src="fundo.mp4"></video></div>
<script>
const v=document.getElementById('v'),c=navigator.connection||{};
if(!matchMedia('(prefers-reduced-motion:reduce)').matches&&!c.saveData&&!/2g/.test(c.effectiveType||'')){
 new IntersectionObserver((e,o)=>{if(e[0].isIntersecting){v.src=v.dataset.src;v.play().then(()=>v.classList.add('ok')).catch(()=>{});o.disconnect()}}).observe(v);
}
</script>
```

## 11. Microinterações (botão que afunda, checklist)
- **O que é:** Botão 3D que afunda ao tocar (`:active`), checkbox verde da paleta que risca o passo feito e vibração curta de 15 ms no clique onde houver suporte.
- **Quando usar:** Sozinho em Casa: botões da página e checklist "marque o que já fez" dentro do produto/área de membros. Upsell: botão de aceitar. Feedback imediato aumenta a sensação de qualidade sem peso.
- **Peso:** 0,8 KB (498 B gzip)
- **Custo no celular:** Mínimo: CSS puro; a vibração só dispara no toque.
- **Fallback / reduced-motion:** Reduced-motion zera a transição (o estado `:active` continua, pois é feedback e não movimento). Testado com toque real no emulador: checkbox marcou.

```html
<style>
.btn{display:inline-block;margin:24px;padding:16px 28px;border:0;border-radius:14px;background:#ff6a00;color:#fff;font:800 18px Poppins,Arial,sans-serif;
 transition:transform .12s,box-shadow .12s;box-shadow:0 6px 0 #b34700;-webkit-tap-highlight-color:transparent}
.btn:active{transform:translateY(4px);box-shadow:0 2px 0 #b34700}
.chk{accent-color:#00d46a;width:24px;height:24px}
.chk:checked+b{text-decoration:line-through;opacity:.6}
@media (prefers-reduced-motion:reduce){.btn{transition:none}}
</style>
<button class=btn id=b>Baixar agora</button><label><input type=checkbox class=chk id=k><b> Fiz o passo 1</b></label>
<script>
document.getElementById('b').addEventListener('click',()=>navigator.vibrate&&navigator.vibrate(15));
</script>
```

## Resumo medido (CPU 4x mais lenta, 40 passos de rolagem)
| Técnica | Script (ms) | Layout (ms) | Peso gzip |
|---|---|---|---|
| 1 Entrada ao rolar | 1,1 | 0 | 343 B |
| 3 Frases tela cheia | 3,2 | 0 | 549 B |
| 5 Parallax leve | 4,4 | 0 | 419 B |
| 7 Cards em sequência | 0,1 | 1,3 | 411 B |
| 8 Botão fixo | 0 | 0 | 508 B |
As demais (2, 4, 9, 11 em CSS/eventos pontuais; 6 e 10 pontuais) ficaram fora da medição de rolagem; peso gzip 317-554 B cada. Total das 11 técnicas juntas: cerca de 5 KB gzip, irrelevante perto de imagem e vídeo.

## Ordem de uso (do mais barato e seguro ao mais caro)
1. **Botão de compra fixo (8)** e **microinterações (11)**: custo quase zero, sobem a conversão no celular. Entram em toda página.
2. **Entrada ao rolar (1)** e **cards em sequência (7)**: dão ritmo à página de vendas sem peso.
3. **Frases em tela cheia (3)**: abertura de 3 telas da página do Sozinho em Casa (dor, empatia, promessa) antes do preço.
4. **Contador (6)** e **barra de progresso (2)**: provas e sensação de avanço; só com número verdadeiro.
5. **Galeria com snap (4)**: prova visual (conteúdo, depoimento autorizado); o peso está nas imagens.
6. **Reação a toque (9)** e **parallax leve (5)**: decorativos, máximo 1 de cada, só se sobrar orçamento.
7. **Vídeo de fundo (10)**: por último; só se um teste A/B mostrar ganho, porque é o item mais caro.
Upsell usa só 8, 11, 1, 7 (página curta, 1 decisão, sem enfeite que atrase o "sim").

Teste (regra J3): mudar UMA técnica por versão, UTM `utm_content=<técnica>`, leitura em 1 h, 3 h e 6 h; ruim em 3 h = trocar na hora.

## Regra de orçamento de performance
- **Peso máximo da página (1ª carga, gzip):** 300 KB no total, sendo HTML+CSS+JS próprios até 30 KB e fonte Poppins limitada a 2 pesos (até 40 KB, `font-display:swap`, `preconnect`). Imagens: WebP, 60 KB cada, a 1ª dobra com 1 imagem só; resto `loading=lazy`. Vídeo de fundo, se usado: fora desse teto, mas máx. 700 KB, só carregado ao entrar na tela.
- **LCP-alvo:** até 2,5 s em 4G médio (meta interna 2,0 s); CLS < 0,1; INP < 200 ms. O elemento LCP é texto ou 1 imagem com `fetchpriority=high`, nunca vídeo nem elemento que começa em `opacity:0` (esconder o LCP atrasa a métrica).
- **Animação:** só `opacity` e `transform`; no máximo 3 técnicas ativas por página; `will-change` em no máximo 1 elemento; nenhuma tarefa de JS maior que 50 ms na rolagem.
- **Obrigatório:** toda técnica com bloco `prefers-reduced-motion`; a página tem que ser legível e comprável sem JS e sem animação.
- **Checagem antes de publicar (Juiz de Qualidade, nota >= 7):** Lighthouse mobile ou Playwright 390x844 com CPU 4x; estourou o teto = cortar a técnica mais cara da "ordem de uso" (de baixo para cima) até caber.
