"""Tema visual compartilhado do site publicado — antes desta extração, o CSS existia
duplicado em `site/build_site.py` (site real) e `agents/07_publisher/agent.py` (prévia de
simulação), cada um podendo divergir sem ninguém perceber. Agora os dois importam daqui;
cada consumidor só acrescenta as regras específicas que fazem sentido pra ele (ex.: a
faixa de aviso de prévia do agente 07).

Paleta e tipografia pensadas para "carinho e afetividade com os animais" (referência de
princípio: fotografia real e calor visual de sites como petz.com.br — nunca a estrutura de
e-commerce deles, que não se aplica a um blog editorial).
"""
from __future__ import annotations

# --------------------------------------------------------------------------- fonte de marca
# Fredoka: sans-serif arredondada e amigável, usada só em títulos — o corpo do texto continua
# em fonte de sistema (zero requisição extra, melhor performance de leitura em bloco de texto).
GOOGLE_FONT_HEAD = (
    '<link rel="preconnect" href="https://fonts.googleapis.com">\n'
    '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
    '<link href="https://fonts.googleapis.com/css2?family=Fredoka:wght@500;600;700&display=swap" '
    'rel="stylesheet">'
)

# --------------------------------------------------------------------------- tokens de marca
TOKENS = """
:root {
  --color-primary: #1e2a44;
  --color-primary-dark: #141c30;
  --color-primary-soft: #e9eefa;
  --color-accent: #e8590c;
  --color-accent-dark: #c2410c;
  --color-warning-bg: #fff8ec;
  --color-warning-border: #d99a2b;
  --color-bg: #fffbf2;
  --color-surface: #ffffff;
  --color-border: #f1e7d3;
  --color-sun: #ffc93c;
  --color-text: #1f2330;
  --color-text-muted: #5b6272;
  --font-heading: 'Fredoka', system-ui, -apple-system, sans-serif;
  --font-body: -apple-system, 'Segoe UI', Roboto, Arial, sans-serif;
  --radius: 14px;
  --radius-sm: 8px;
  --shadow-card: 0 1px 3px rgba(30, 42, 68, 0.10), 0 1px 2px rgba(30, 42, 68, 0.06);
}
"""

# --------------------------------------------------------------------------- base compartilhada
BASE_CSS = TOKENS + """
* { box-sizing: border-box; }
body { margin: 0; font-family: var(--font-body); background: var(--color-bg); color: var(--color-text); }

header.site { background: linear-gradient(100deg, #6b46c1 0%, #8b68dd 55%, #ad8eeb 100%); color: #fff; padding: 16px 24px; border-bottom: 5px solid var(--color-sun); }
header.site .brand { font-family: var(--font-heading); font-weight: 600; font-size: 1.25rem; }
header.site a { color: #fff; text-decoration: none; }
header.site nav { margin-top: 8px; font-size: 0.9rem; }
header.site nav a { margin-right: 16px; opacity: 0.95; padding-bottom: 2px; border-bottom: 2px solid transparent; }
header.site nav a:hover { opacity: 1; border-bottom-color: var(--color-sun); }

.breadcrumb { max-width: 760px; margin: 18px auto 0; padding: 0 20px; font-size: 0.8rem; color: var(--color-text-muted); }
.breadcrumb a { color: var(--color-primary); text-decoration: none; }
.breadcrumb a:hover { text-decoration: underline; }

main.article, main.legal { max-width: 760px; margin: 0 auto; padding: 16px 20px 56px; }
main.home { max-width: 1080px; margin: 0 auto; padding: 8px 20px 56px; }

h1 { font-family: var(--font-heading); font-weight: 600; font-size: 2.1rem; line-height: 1.2; color: var(--color-primary-dark); }
h2 { font-family: var(--font-heading); font-weight: 600; font-size: 1.5rem; line-height: 1.3; margin-top: 2em; color: var(--color-primary-dark); }
h3 { font-family: var(--font-heading); font-weight: 500; font-size: 1.15rem; margin-top: 1.4em; }
p { line-height: 1.75; font-size: 1.05rem; }
a { color: var(--color-accent-dark); }
ul { line-height: 1.75; }

blockquote { border-left: 4px solid var(--color-warning-border); background: var(--color-warning-bg);
  margin: 1.5em 0; padding: 0.9em 1.3em; font-size: 0.98rem; border-radius: 0 var(--radius-sm) var(--radius-sm) 0; }

.byline { font-size: 0.88rem; color: var(--color-text-muted); margin-top: -0.4em; }

/* botão / CTA — usado ao fim de cada artigo e em elementos de ação da home */
.btn { display: inline-block; background: var(--color-accent); color: #fff; text-decoration: none;
  font-weight: 600; padding: 12px 22px; border-radius: 999px; transition: background 0.15s ease; }
.btn:hover { background: var(--color-accent-dark); color: #fff; }
.cta-box { margin: 2.5em 0 0.5em; padding: 24px; background: var(--color-primary-soft);
  border-radius: var(--radius); text-align: center; }
.cta-box p { margin: 0 0 14px; color: var(--color-primary-dark); font-size: 1.05rem; }

/* faixa do produto — no começo e no fim de todo artigo */
.produto-topo { display: flex; align-items: center; justify-content: space-between; gap: 16px; flex-wrap: wrap;
  margin: 0 0 20px; padding: 14px 18px; background: var(--color-primary-soft);
  border: 1px solid var(--color-border); border-radius: var(--radius); }
.produto-topo-texto { margin: 0; flex: 1 1 260px; font-weight: 600; font-size: 1rem; line-height: 1.4;
  color: var(--color-primary-dark); }
.produto-topo .btn { padding: 10px 18px; white-space: nowrap; }

/* grid de cards da home — cada pilar vira uma seção, cada artigo um card */
.pilar-section { margin-top: 2.8em; }
.pilar-section h2 { display: flex; align-items: center; gap: 10px; border-bottom: 2px solid var(--color-border); padding-bottom: 10px; }
.pilar-tag { font-size: 0.7rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.03em;
  background: var(--color-primary-soft); color: var(--color-primary-dark); padding: 3px 10px; border-radius: 999px; }
.card-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(230px, 1fr)); gap: 18px; margin-top: 18px; }
.card { background: var(--color-surface); border: 1px solid var(--color-border); border-radius: var(--radius);
  overflow: hidden; box-shadow: var(--shadow-card); transition: transform 0.15s ease, box-shadow 0.15s ease; }
.card:hover { transform: translateY(-2px); box-shadow: 0 6px 16px rgba(30, 42, 68, 0.16); }
.card a.card-link { text-decoration: none; color: inherit; display: block; }
.card-cover { height: 120px; width: 100%; display: flex; align-items: center; justify-content: center; font-size: 2.4rem; object-fit: cover; }
.hero-img { width: 100%; max-height: 320px; object-fit: cover; border-radius: var(--radius); margin: 4px 0 4px; display: block; }
.image-credit { font-size: 0.75rem; color: var(--color-text-muted); margin: 0 0 20px; }
.image-credit a { color: var(--color-text-muted); }
.card-body { padding: 14px 16px 18px; }
.card-body .card-data { font-size: .78rem; color: var(--color-muted, #6b6b6b); margin-bottom: 4px; }
.tv-home { margin: 0 0 20px; }
.tv-home a { position: relative; display: block; border-radius: 14px; overflow: hidden; text-decoration: none; color: #fff; background: #222; }
.tv-home img { width: 100%; height: auto; display: block; aspect-ratio: 3 / 1.4; object-fit: cover; opacity: .75; }
.tv-home-texto { position: absolute; inset: 0; padding: 18px 20px; display: flex; flex-direction: column; justify-content: flex-end; gap: 6px; }
.tv-home .slide-cta { font-weight: 700; border-bottom: 2px solid #fff; align-self: flex-start; }
.tv-h1 { text-align: center; }
.tv-set { max-width: 480px; margin: 14px auto 22px; background: linear-gradient(#2b2b2f, #151517); border-radius: 22px; padding: 12px 12px 8px; box-shadow: 0 10px 28px rgba(0,0,0,.35); color: #fff; }
.tv-topo { display: flex; justify-content: space-between; align-items: center; padding: 2px 6px 10px; font-weight: 800; letter-spacing: .08em; font-size: .85rem; }
.tv-no-ar { background: #d62828; padding: 3px 10px; border-radius: 6px; font-size: .75rem; display: inline-flex; align-items: center; gap: 6px; }
.tv-no-ar i { width: 8px; height: 8px; border-radius: 50%; background: #fff; display: inline-block; animation: tvpisca 1.2s infinite; }
@keyframes tvpisca { 50% { opacity: .25; } }
.tv-tela { border: 4px solid #000; border-radius: 12px; overflow: hidden; background: #000; }
.tv-tela video { width: 100%; display: block; aspect-ratio: 9 / 16; max-height: 70vh; background: #000; }
.tv-rodape { display: flex; flex-direction: column; gap: 4px; padding: 12px 8px 6px; }
.tv-rotulo { font-size: .72rem; font-weight: 800; letter-spacing: .12em; color: #ffd166; }
.tv-rodape strong { font-size: 1.15rem; line-height: 1.3; }
.tv-rodape a { color: #fff; text-decoration: underline; }
.tv-prox { font-size: .85rem; opacity: .8; }
.tv-pe { height: 6px; width: 40%; margin: 8px auto 0; background: #3a3a3f; border-radius: 4px; }
.foto-artista { margin: 16px 0; } .foto-artista img { width: 100%; height: auto; border-radius: 12px; display: block; }
.foto-artista figcaption { font-size: .85rem; color: #555; margin-top: 6px; }
.ig-embed { margin: 16px 0; text-align: center; }
main.tv { max-width: 760px; margin: 0 auto; padding: 16px; }
.tv-sub, .tv-atual { text-align: center; }
.tv-lista { display: grid; gap: 10px; }
.tv-item { display: flex; gap: 12px; align-items: center; text-align: left; background: none; border: 1px solid rgba(0,0,0,.12); border-radius: 10px; padding: 8px; cursor: pointer; font: inherit; color: inherit; }
.tv-item.ativo { border-color: var(--color-accent, #c0392b); background: rgba(0,0,0,.04); }
.tv-item img { width: 96px; height: auto; border-radius: 8px; flex: none; object-fit: cover; }
.tv-item-texto { display: flex; flex-direction: column; gap: 2px; }
.novo-destaque { margin: 0 0 20px; }
.novo-destaque a { position: relative; display: block; border-radius: 14px; overflow: hidden; text-decoration: none; color: #fff; background: #222; }
.novo-destaque img { width: 100%; height: auto; display: block; aspect-ratio: 3 / 2; object-fit: cover; max-height: 420px; }
.novo-texto { position: absolute; left: 0; right: 0; bottom: 0; padding: 18px 20px; display: flex; flex-direction: column; gap: 6px; background: linear-gradient(transparent, rgba(0,0,0,.78)); }
.novo-selo { align-self: flex-start; background: #fff; color: #222; font-weight: 700; font-size: .8rem; padding: 3px 10px; border-radius: 999px; }
.novo-titulo { font-size: 1.35rem; font-weight: 700; line-height: 1.25; }
.novo-destaque .slide-cta { font-weight: 700; font-size: .95rem; border-bottom: 2px solid #fff; align-self: flex-start; }
.novo-resumo { font-size: .95rem; opacity: .95; }
.card-body .card-title { font-family: var(--font-heading); font-weight: 500; font-size: 1rem; line-height: 1.35; color: var(--color-primary-dark); }

/* carrossel de banners da home */
.carrossel { position: relative; margin: 22px 0 6px; border-radius: 20px; overflow: hidden; box-shadow: var(--shadow-card); background: var(--color-primary-dark); }
.carrossel .slides { display: flex; overflow-x: auto; scroll-snap-type: x mandatory; scrollbar-width: none; overscroll-behavior-x: contain; }
.carrossel .slides::-webkit-scrollbar { display: none; }
.carrossel .slide { position: relative; flex: 0 0 100%; scroll-snap-align: start; display: block; height: clamp(240px, 46vw, 420px); color: #fff; text-decoration: none; }
.carrossel .slide img { position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; }
.carrossel .slide::after { content: ""; position: absolute; inset: 0; background: linear-gradient(0deg, rgba(20,28,48,.88) 0%, rgba(20,28,48,.45) 45%, rgba(20,28,48,0) 75%); }
.carrossel .slide-texto { position: absolute; z-index: 1; left: 0; right: 0; bottom: 0; padding: 18px 64px 40px 22px; display: flex; flex-direction: column; gap: 8px; align-items: flex-start; }
.carrossel .slide-rotulo { background: var(--color-accent); color: #fff; font-size: .75rem; font-weight: 700; text-transform: uppercase; letter-spacing: .05em; padding: 4px 12px; border-radius: 999px; }
.carrossel .slide-titulo { font-family: var(--font-heading); font-weight: 600; font-size: clamp(1.25rem, 3.6vw, 2.2rem); line-height: 1.2; max-width: 640px; text-shadow: 0 2px 10px rgba(0,0,0,.4); }
.carrossel .slide-cta { font-weight: 700; font-size: .95rem; border-bottom: 2px solid var(--color-accent); }
.carrossel .seta { position: absolute; top: 50%; transform: translateY(-50%); z-index: 2; width: 44px; height: 44px; border: 0; border-radius: 50%; background: rgba(255,255,255,.9); color: var(--color-primary-dark); font-size: 1.7rem; line-height: 1; cursor: pointer; }
.carrossel .ant { left: 10px; } .carrossel .prox { right: 10px; }
.carrossel .pontos { position: absolute; z-index: 2; left: 0; right: 0; bottom: 12px; display: flex; justify-content: center; gap: 4px; }
.carrossel .ponto { width: 28px; height: 28px; border: 0; background: none; padding: 0; cursor: pointer; position: relative; }
.carrossel .ponto::after { content: ""; position: absolute; left: 50%; top: 50%; width: 10px; height: 10px; margin: -5px; border-radius: 50%; background: rgba(255,255,255,.55); transition: all .2s; }
.carrossel .ponto[aria-current="true"]::after { background: var(--color-accent); width: 24px; margin-left: -12px; border-radius: 6px; }
@media (max-width: 600px) { .carrossel { border-radius: 14px; } .carrossel .seta { display: none; } .carrossel .slide-texto { padding-right: 18px; } }
@media (prefers-reduced-motion: reduce) { .carrossel .slides { scroll-behavior: auto; } }

.hero { padding: 44px 0 16px; }
.hero h1 { font-size: 2.5rem; }
.hero p { font-size: 1.15rem; color: var(--color-text-muted); max-width: 640px; }

/* Rádio Tutorial Pet: player opcional, começa desligado */
.radio { position: fixed; left: 14px; bottom: 14px; z-index: 900; font-family: var(--font-body); }
.radio-btn { display: flex; align-items: center; gap: 8px; min-height: 44px; padding: 8px 16px 8px 12px; border: 0; border-radius: 999px; background: linear-gradient(100deg, #6b46c1, #ad8eeb); color: #fff; font-weight: 700; font-size: .9rem; cursor: pointer; box-shadow: 0 6px 18px rgba(107,70,193,.35); }
.radio-ico { width: 28px; height: 28px; border-radius: 50%; background: var(--color-sun); color: var(--color-primary-dark); display: grid; place-items: center; font-size: 1.1rem; }
.radio.tocando .radio-ico { animation: radio-pulsa 1s ease-in-out infinite; }
@keyframes radio-pulsa { 50% { transform: scale(1.18); } }
.radio-painel { margin-bottom: 8px; width: min(300px, calc(100vw - 28px)); background: var(--color-surface); border: 1px solid var(--color-border); border-radius: 16px; padding: 12px 14px; box-shadow: 0 10px 28px rgba(20,28,48,.22); position: absolute; bottom: 52px; left: 0; }
.radio-faixa { font-weight: 700; font-size: .92rem; color: var(--color-primary-dark); margin-bottom: 8px; }
.radio-ctl { display: flex; align-items: center; gap: 6px; }
.radio-ctl button { width: 40px; height: 40px; border: 0; border-radius: 50%; background: var(--color-primary-soft); color: var(--color-primary-dark); font-size: 1rem; cursor: pointer; }
.radio-ctl input { flex: 1; min-width: 0; accent-color: var(--color-accent); }
.radio-cred { margin-top: 8px; font-size: .72rem; color: var(--color-text-muted); line-height: 1.35; }
@media (prefers-reduced-motion: reduce) { .radio.tocando .radio-ico { animation: none; } }

footer.site { max-width: 1080px; margin: 40px auto 0; padding: 22px 20px 44px; font-size: 0.85rem;
  color: var(--color-text-muted); border-top: 1px solid var(--color-border); }
footer.site a { color: var(--color-text-muted); margin-right: 14px; }
"""

# Cor de fundo do "card-cover" (placeholder até o agente de imagem existir) e emoji temático
# por pilar — trocar pelo <img> real assim que a Fase 2 (agente de imagem) estiver pronta.
PILAR_VISUAL = {
    "alimentacao": {"bg": "#ffe8cc", "emoji": "🍖"},
    "comportamento": {"bg": "#dbe7ff", "emoji": "🐾"},
    "cuidados_diarios": {"bg": "#d9f2e6", "emoji": "🛁"},
    "primeiros_passos_filhotes": {"bg": "#ffe0e6", "emoji": "🐶"},
    "produtos_compras": {"bg": "#ece2ff", "emoji": "🛍️"},
}
PILAR_VISUAL_PADRAO = {"bg": "#efece5", "emoji": "🐾"}
