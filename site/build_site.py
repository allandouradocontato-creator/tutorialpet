"""Monta o site estático final em site/build/, pronto para deploy.

Este script fica FORA de agents/ e de orchestrator.py de propósito: é uma ferramenta de
montagem de site, não um agente do pipeline de produção. Reaproveita a função pura de
conversão Markdown→HTML do agente 07 (agents/07_publisher/agent.py, markdown_to_html_body
— importada, não copiada nem modificada), mas usa seu PRÓPRIO template de página: sem a
faixa de "prévia/simulação" do agente 07 (que não faz sentido num site pronto para
deploy), com navegação real (início, pilar, rodapé com páginas legais) e URLs/meta tags
apontando para o domínio real do site.

Uso:
    python site/build_site.py --site pets-tutores-iniciantes
"""
from __future__ import annotations

import argparse
import html as html_lib
import importlib.util
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from core.config import load_env_file, load_site, load_yaml  # noqa: E402
from core.markdown import MarkdownError, read_markdown  # noqa: E402
from core.theme import BASE_CSS, GOOGLE_FONT_HEAD, PILAR_VISUAL, PILAR_VISUAL_PADRAO  # noqa: E402

# Google Analytics 4 (propriedade tutorialpet.com.br, criada em 06/10/2026)
GA_ID = "G-HP7ZXLFBXH"
GA_TAG = (
    f'<script async src="https://www.googletagmanager.com/gtag/js?id={GA_ID}"></script>'
    "<script>window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments);}"
    f"gtag('js',new Date());gtag('config','{GA_ID}');</script>"
)

# Microsoft Clarity (projeto Tutorial Pet, criado em 06/10/2026)
CLARITY_ID = "ytjlk68nn4"
CLARITY_TAG = (
    '<script>(function(c,l,a,r,i,t,y){c[a]=c[a]||function(){(c[a].q=c[a].q||[]).push(arguments)};'
    't=l.createElement(r);t.async=1;t.src="https://www.clarity.ms/tag/"+i;'
    'y=l.getElementsByTagName(r)[0];y.parentNode.insertBefore(t,y);'
    f'}})(window,document,"clarity","script","{CLARITY_ID}");</script>'
)

# Google AdSense (conta criada em 14/10/2026; ID de editor do Allan)
ADSENSE_PUB = "pub-7204207473239947"
ADSENSE_TAG = (
    f'<meta name="google-adsense-account" content="ca-{ADSENSE_PUB}">'
    f'<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-{ADSENSE_PUB}" crossorigin="anonymous"></script>'
)

# Banner de consentimento (LGPD): Analytics e Clarity só carregam depois do "Aceitar".
CONSENT_TAG = (
    "<script>(function(){var K='tp_consent';"
    "function load(){if(window.__tpLoaded)return;window.__tpLoaded=1;"
    "var g=document.createElement('script');g.async=1;g.src='https://www.googletagmanager.com/gtag/js?id=" + GA_ID + "';document.head.appendChild(g);"
    "window.dataLayer=window.dataLayer||[];window.gtag=function(){dataLayer.push(arguments);};gtag('js',new Date());gtag('config','" + GA_ID + "');"
    "(function(c,l,a,r,i,t,y){c[a]=c[a]||function(){(c[a].q=c[a].q||[]).push(arguments)};t=l.createElement(r);t.async=1;"
    "t.src='https://www.clarity.ms/tag/'+i;y=l.getElementsByTagName(r)[0];y.parentNode.insertBefore(t,y);})"
    "(window,document,'clarity','script','" + CLARITY_ID + "');}"
    "var v=null;try{v=localStorage.getItem(K);}catch(e){}"
    "if(v==='granted'){load();return;}"
    "if(v==='denied'){return;}"
    "document.addEventListener('DOMContentLoaded',function(){"
    "var b=document.getElementById('tp-consent');if(!b)return;b.hidden=false;"
    "function set(x){try{localStorage.setItem(K,x);}catch(e){}b.hidden=true;if(x==='granted')load();}"
    "document.getElementById('tp-aceitar').onclick=function(){set('granted');};"
    "document.getElementById('tp-recusar').onclick=function(){set('denied');};});"
    "})();</script>"
)
CONSENT_HTML = (
    '<div id="tp-consent" hidden role="dialog" aria-label="Aviso de cookies" style="position:fixed;left:12px;right:12px;bottom:12px;'
    'z-index:9999;max-width:560px;margin:0 auto;background:#fff;color:#1d2433;border:1px solid #d9dde6;border-radius:12px;'
    'padding:14px 16px;box-shadow:0 8px 28px rgba(0,0,0,.18);font:15px/1.45 system-ui,sans-serif">'
    '<p style="margin:0 0 10px">Usamos cookies de medição (Google Analytics e Microsoft Clarity) para entender como o site é usado. '
    'Só ativamos se você aceitar. <a href="/politica-de-privacidade.html" style="color:#c2410c">Política de privacidade</a>.</p>'
    '<div style="display:flex;gap:8px;flex-wrap:wrap"><button id="tp-aceitar" type="button" style="min-height:44px;padding:8px 16px;'
    'border:0;border-radius:8px;background:#c2410c;color:#fff;font:inherit;font-weight:700;cursor:pointer">Aceitar</button>'
    '<button id="tp-recusar" type="button" style="min-height:44px;padding:8px 16px;border:1px solid #c9ced9;border-radius:8px;'
    'background:#fff;color:#1d2433;font:inherit;cursor:pointer">Recusar</button></div></div>'
)

CARROSSEL_JS = (
    "<script>(function(){var c=document.querySelector('.carrossel');if(!c)return;var t=c.querySelector('.slides'),"
    "s=t.children,p=c.querySelectorAll('.ponto'),n=s.length,i=0,h=0,r=matchMedia('(prefers-reduced-motion:reduce)').matches;"
    "function w(k){return t.clientWidth*k}"
    "function ir(k,smooth){i=(k+n)%n;t.scrollTo({left:w(i),behavior:smooth===false||r?'auto':'smooth'});m()}"
    "function m(){for(var k=0;k<n;k++){p[k].setAttribute('aria-current',k===i?'true':'false');s[k].tabIndex=k===i?0:-1}}"
    "function a(){if(r||h)return;clearInterval(a.t);a.t=setInterval(function(){if(!document.hidden&&!h)ir(i+1)},5500)}"
    "c.querySelector('.ant').onclick=function(){ir(i-1);};c.querySelector('.prox').onclick=function(){ir(i+1);};"
    "p.forEach(function(b,k){b.onclick=function(){ir(k)}});"
    "t.addEventListener('scroll',function(){var k=Math.round(t.scrollLeft/t.clientWidth);if(k!==i){i=k;m()}},{passive:true});"
    "['mouseenter','focusin','touchstart'].forEach(function(e){c.addEventListener(e,function(){h=1;clearInterval(a.t)},{passive:true})});"
    "['mouseleave','focusout'].forEach(function(e){c.addEventListener(e,function(){h=0;a()})});"
    "c.addEventListener('touchend',function(){setTimeout(function(){h=0;a()},4000)},{passive:true});"
    "m();a();})();</script>"
)

TV_BTN = ('<a class="tv-flutuante" href="/tv" aria-label="Assistir à Tutorial Pet TV">'
          '<span class="tv-flutuante-ico" aria-hidden="true">\U0001F4FA</span><span class="tv-flutuante-txt">TV</span></a>')

RADIO_HTML = (
    '<div id="tp-radio" class="radio" hidden>'
    '<button type="button" class="radio-btn" id="tp-radio-play" aria-label="Ligar a Rádio Tutorial Pet" aria-pressed="false"><span class="radio-ico" aria-hidden="true">\u266a</span><span class="radio-txt">Rádio Tutorial Pet</span></button>'
    '<div class="radio-painel" id="tp-radio-painel" hidden>'
    '<div class="radio-faixa" id="tp-radio-faixa" aria-live="polite">—</div>'
    '<div class="radio-ctl"><button type="button" id="tp-radio-prev" aria-label="Faixa anterior">\u23ee</button>'
    '<button type="button" id="tp-radio-pp" aria-label="Pausar">\u23f8</button>'
    '<button type="button" id="tp-radio-next" aria-label="Próxima faixa">\u23ed</button>'
    '<input type="range" id="tp-radio-vol" min="0" max="100" value="35" aria-label="Volume"></div>'
    '<div class="radio-cred">Músicas livres de direitos autorais (licença Pixabay). Créditos: <span id="tp-radio-cred"></span></div>'
    '</div></div>'
)
RADIO_JS = (
    "<script>(function(){var w=document.getElementById('tp-radio');if(!w)return;w.hidden=false;"
    "var K='tp_radio',S={};try{S=JSON.parse(localStorage.getItem(K)||'{}')}catch(e){}"
    "var a=null,L=null,i=S.i||0,b=document.getElementById('tp-radio-play'),p=document.getElementById('tp-radio-painel'),"
    "pp=document.getElementById('tp-radio-pp'),f=document.getElementById('tp-radio-faixa'),v=document.getElementById('tp-radio-vol');"
    "v.value=S.v==null?35:S.v;"
    "function sv(){try{localStorage.setItem(K,JSON.stringify({on:!!(a&&!a.paused),i:i,t:a?a.currentTime:0,v:+v.value,open:!p.hidden}))}catch(e){}}"
    "function ui(){var on=a&&!a.paused;b.setAttribute('aria-pressed',on?'true':'false');w.classList.toggle('tocando',!!on);pp.textContent=on?'\\u23f8':'\\u25b6';pp.setAttribute('aria-label',on?'Pausar':'Tocar')}"
    "function load(cb){if(L){cb();return}fetch('/radio/faixas.json').then(function(r){return r.json()}).then(function(j){L=j;"
    "document.getElementById('tp-radio-cred').textContent=j.map(function(x){return x.autor}).filter(function(x,k,r){return r.indexOf(x)===k}).join(', ');cb()}).catch(function(){})}"
    "function set(k,t,go){i=(k+L.length)%L.length;if(!a){a=new Audio();a.preload='none';a.addEventListener('ended',function(){set(i+1,0,true)});"
    "a.addEventListener('pause',function(){ui();sv()});a.addEventListener('play',ui);setInterval(function(){if(a&&!a.paused)sv()},4000)}"
    "a.src=L[i].arquivo;a.volume=v.value/100;f.textContent=L[i].titulo+' \\u2014 '+L[i].autor;"
    "if(t){a.addEventListener('loadedmetadata',function h(){try{a.currentTime=t}catch(e){}a.removeEventListener('loadedmetadata',h)})}"
    "if(go){var r=a.play();if(r&&r.catch)r.catch(function(){ui()})}ui();sv()}"
    "b.onclick=function(){load(function(){if(!a){p.hidden=false;set(i,S.t||0,true)}else if(a.paused){p.hidden=false;a.play()}else{a.pause();p.hidden=true}sv()})};"
    "pp.onclick=function(){if(!a)return;if(a.paused)a.play();else a.pause()};"
    "document.getElementById('tp-radio-next').onclick=function(){load(function(){set(i+1,0,true)})};"
    "document.getElementById('tp-radio-prev').onclick=function(){load(function(){set(i-1,0,true)})};"
    "v.oninput=function(){if(a)a.volume=v.value/100;sv()};"
    "addEventListener('pagehide',sv);if(S.on){load(function(){p.hidden=false;set(i,S.t||0,true)})}"
    "})();</script>"
)

OTIMIZADOS_DIR = ROOT / "data" / "seo_onpage" / "otimizados"
LEGAL_DIR = ROOT / "data" / "platform_compliance" / "paginas_legais"
TECH_DIR = ROOT / "data" / "platform_compliance" / "arquivos_tecnicos"
BUILD_DIR = ROOT / "site" / "build"
PRODUTOS_PATH = ROOT / "config" / "produtos_relacionados.yaml"

LEGAL_PAGES_ORDER = ["sobre", "revisao-veterinaria", "contato", "politica-de-privacidade", "termos", "disclaimer"]
LEGAL_PAGES_TITULOS = {"sobre": "Sobre", "contato": "Contato",
                        "politica-de-privacidade": "Política de Privacidade", "termos": "Termos de Uso",
                        "disclaimer": "Disclaimer", "revisao-veterinaria": "Revisão veterinária"}

CATEGORIAS_PATH = ROOT / "config" / "categorias.yaml"


def _load_categorias() -> dict:
    try:
        return load_yaml(CATEGORIAS_PATH) or {}
    except Exception:
        return {}


CATEGORIAS = _load_categorias()


COLUNA_VET = "pergunte-a-veterinaria"   # coluna fora dos pilares (nao entra no rodizio da fabrica)


def cat_slug(pilar_key: str) -> str:
    """Slug da página de categoria (config/categorias.yaml; sem entrada, troca _ por -)."""
    return str((CATEGORIAS.get(pilar_key) or {}).get("slug") or pilar_key.replace("_", "-"))


def cat_url(pilar_key: str) -> str:
    return f"/categoria/{cat_slug(pilar_key)}"


def _load_videos_artigos() -> dict:
    f = ROOT / "config" / "sites" / "videos_artigos.json"
    try:
        return json.loads(f.read_text(encoding="utf-8")) if f.exists() else {}
    except Exception:
        return {}


VIDEOS_ARTIGOS = _load_videos_artigos()


def _load_equipe() -> dict:
    f = ROOT / "config" / "sites" / "equipe.json"
    try:
        return json.loads(f.read_text(encoding="utf-8")) if f.exists() else {}
    except Exception:
        return {}


EQUIPE = _load_equipe()

# 25/10/2026 (AdSense "conteudo de baixo valor"): os 72 artigos terminavam no mesmo H2 "Para fechar".
# O titulo do fechamento passa a variar por artigo (escolha estavel pelo slug); o texto do fechamento nao muda.
# 28/10/2026 (reavaliacao AdSense): o checklist pede uma secao final chamada "Conclusao"; as variacoes de titulo
# ("O que levar daqui", "Proximo passo"...) deixavam de ser reconhecidas como conclusao. O markdown segue com
# "## Para fechar" (o curador do blog exige) e o build publica como "Conclusão".
FECHOS = ["Conclusão"]


def _variar_fecho(body: str, slug: str) -> str:
    import re as _r, zlib
    novo = FECHOS[zlib.crc32(slug.encode("utf-8")) % len(FECHOS)]
    return _r.sub(r"^## Para fechar\s*$", f"## {novo}", body, count=1, flags=_r.M)


def load_agent07_markdown_converter():
    """Importa agents/07_publisher/agent.py só para reaproveitar markdown_to_html_body —
    não instancia nem chama nada que dependa do gate de aprovação do agente 07."""
    path = ROOT / "agents" / "07_publisher" / "agent.py"
    spec = importlib.util.spec_from_file_location("agent_07_publisher_reuso", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.markdown_to_html_body


# CSS unificado em core/theme.py (paleta de marca + tipografia), compartilhado com o
# agente 07 — antes cada um tinha sua própria cópia quase idêntica, que podia divergir
# sem ninguém perceber.
CSS = BASE_CSS


_PILARES_GLOBAL: dict = {}


def render_header(site_nome: str, pilares: dict[str, str]) -> str:
    links = "".join(f'<a href="{cat_url(key)}">{html_lib.escape(nome)}</a>' for key, nome in pilares.items()) + f'<a href="{cat_url("pet-celebridade")}">Pet Celebridade</a><a href="{cat_url(COLUNA_VET)}">Pergunte à veterinária</a><a href="/tv">TV</a>'
    return f"""<header class="site">
<a href="/" class="brand">{html_lib.escape(site_nome)}</a>
<nav>{links}</nav>
{render_redes(compacto=True)}
</header>"""


def render_footer(pilares: dict | None = None) -> str:
    pilares = pilares or _PILARES_GLOBAL
    cats = "".join(f'<a href="{cat_url(k)}">{html_lib.escape(n)}</a>' for k, n in pilares.items())
    cats = f'<nav class="footer-cats" aria-label="Categorias">{cats}<a href="{cat_url("pet-celebridade")}">Pet Celebridade</a><a href="{cat_url(COLUNA_VET)}">Pergunte à veterinária</a></nav>' if cats else ""
    links = "".join(
        f'<a href="/{slug}">{LEGAL_PAGES_TITULOS[slug]}</a>' for slug in LEGAL_PAGES_ORDER
    )
    ano = datetime.now(timezone.utc).year
    return (f'<footer class="site">{render_redes()}{cats}{links}<p>© {ano} Tutorial Pet — conteúdo informativo, '
            f'não substitui orientação veterinária profissional.</p></footer>')


def page_shell(title: str, meta_description: str, canonical: str, og_type: str, body_html: str,
               extra_head: str = "", og_image: str = "") -> str:
    og_image_tag = f'<meta property="og:image" content="{html_lib.escape(og_image)}">' if og_image else ""
    return f"""<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html_lib.escape(title)}</title>
<meta name="description" content="{html_lib.escape(meta_description)}">
<link rel="canonical" href="{html_lib.escape(canonical)}">
<meta property="og:type" content="{og_type}">
<meta property="og:title" content="{html_lib.escape(title)}">
<meta property="og:description" content="{html_lib.escape(meta_description)}">
<meta property="og:url" content="{html_lib.escape(canonical)}">
<meta property="og:locale" content="pt_BR">
{og_image_tag}
{GOOGLE_FONT_HEAD}
{ADSENSE_TAG}
{CONSENT_TAG}
{extra_head}
<style>{CSS}{CAT_CSS}{PESSOA_CSS}</style>
</head>
<body>
{body_html}
{CONSENT_HTML}
{RADIO_HTML}{RADIO_JS}
{'' if canonical.rstrip('/').endswith('/tv') else TV_BTN}
</body>
</html>
"""


def load_produto_destaque(fm: dict) -> dict | None:
    """Escolhe o produto cadastrado em config/produtos_relacionados.yaml que mais combina com o
    artigo (por palavras-chave); empate ou nenhuma palavra casando cai no primeiro produto."""
    try:
        cfg = load_yaml(PRODUTOS_PATH) or {}
    except Exception:
        return None
    produtos = [p for p in (cfg.get("produtos") or []) if p.get("link")]
    if not produtos:
        return None
    texto = " ".join(str(fm.get(k, "")) for k in ("slug", "titulo", "titulo_seo", "meta_description")).lower()
    return max(produtos, key=lambda p: sum(1 for kw in (p.get("palavras_chave") or []) if str(kw).lower() in texto))


def render_produto_topo(produto: dict | None) -> str:
    """Faixa do produto, usada NO COMEÇO e no fim de todo artigo (regra de 05/10/2026)."""
    if not produto:
        return ""
    chamada = produto.get("chamada_topo") or f"Conheça {produto['nome']}"
    botao = produto.get("botao_topo") or "Conhecer"
    return (f'<aside class="produto-topo"><p class="produto-topo-texto">🐾 {html_lib.escape(chamada)}</p>'
            f'<a class="btn" rel="noopener" href="{html_lib.escape(produto["link"])}">{html_lib.escape(botao)}</a></aside>')


def build_article_page(fm: dict, body: str, structured_data: dict, site: dict, pilares: dict,
                        md_to_html) -> str:
    dominio = site["dominio"].rstrip("/")
    slug = fm["slug"]
    pilar_key = fm.get("pilar", "")
    pilar_titulo = pilares.get(pilar_key, pilar_key.replace("_", " ").title())
    canonical = f"{dominio}/{slug}"
    titulo_seo = fm.get("titulo_seo") or fm["titulo"]

    jsonld_scripts = "\n".join(
        f'<script type="application/ld+json">{json.dumps(v, ensure_ascii=False)}</script>'
        for v in structured_data.values()
    )

    jsonld_scripts = jsonld_scripts.replace(
        '{"@type": "Person", "name": "PREENCHER_APOS_APROVACAO_HUMANA"}',
        '{"@type": "Organization", "name": "Tutorial Pet"}')

    autor = (fm.get("autor") or "").strip()
    _ed = (EQUIPE.get("editor") or {})
    if autor:
        byline = f'<p class="byline">Por {html_lib.escape(autor)}</p>'
    elif _ed.get("nome"):
        byline = (f'<p class="byline">Por <a href="{html_lib.escape(_ed.get("pagina", "/sobre#equipe"))}" rel="author">'
                  f'{html_lib.escape(_ed["nome"])}</a>, {html_lib.escape(_ed.get("funcao", "editor responsável")).lower()}</p>')
    else:
        byline = f'<p class="byline">Por {html_lib.escape((fm.get("assinatura") or "Equipe Tutorial Pet").strip())}</p>'
    # Selo de revisão veterinária: SÓ com revisado_por + revisado_em no frontmatter (regra inegociável, 28/10/2026).
    selo_revisao = ""
    _revisao = _revisao_do_artigo(fm)
    if _revisao:
        _rp, _rd = _revisao
        _crmv = _crmv_txt(_rp)
        selo_revisao = (f'<p class="revisado-por">Revisado por <a href="/revisao-veterinaria">{html_lib.escape(_rp["nome"])}</a>, '
                        f'{html_lib.escape(_rp.get("titulo_curto", "médica veterinária"))}'
                        + (f' ({html_lib.escape(_crmv)})' if _crmv else "") + f' em {_rd}</p>')
        _pessoa_ld = {"@type": "Person", "name": _rp["nome"], "jobTitle": "Médica Veterinária"}
        if _rp.get("instagram"):
            _pessoa_ld["url"] = _rp["instagram"]
        if _rp.get("crmv"):
            _pessoa_ld["identifier"] = _crmv
        for _sd in structured_data.values():
            if isinstance(_sd, dict) and _sd.get("@type") in ("Article", "BlogPosting", "NewsArticle"):
                _sd["reviewedBy"] = _pessoa_ld
        jsonld_scripts = "\n".join(
            f'<script type="application/ld+json">{json.dumps(v, ensure_ascii=False)}</script>'
            for v in structured_data.values())
        jsonld_scripts = jsonld_scripts.replace(
            '{"@type": "Person", "name": "PREENCHER_APOS_APROVACAO_HUMANA"}',
            '{"@type": "Organization", "name": "Tutorial Pet"}')
    if _ed.get("nome"):  # dados estruturados: autor pessoa real em vez de "Equipe Tutorial Pet"
        jsonld_scripts = jsonld_scripts.replace(
            '{"@type": "Organization", "name": "Equipe Tutorial Pet"}',
            json.dumps({"@type": "Person", "name": _ed["nome"], "url": dominio + "/sobre#equipe"}, ensure_ascii=False))

    pub, atu = _data_br(_data_iso(fm)), _data_br(fm.get("atualizado_em") or "")
    if pub:
        datas = f'Publicado em <time datetime="{_data_iso(fm)}">{pub}</time>'
        if atu and atu != pub:
            datas += f' · Atualizado em <time datetime="{str(fm.get("atualizado_em"))[:10]}">{atu}</time>'
        byline = byline.replace("</p>", f" · {datas}</p>", 1)

    breadcrumb = (f'<div class="breadcrumb"><a href="/">Início</a> &gt; '
                  f'<a href="{cat_url(pilar_key)}">{html_lib.escape(pilar_titulo)}</a> &gt; {html_lib.escape(fm["titulo"])}</div>')
    cat_linha = (f'<p class="categoria-link">Categoria: <a href="{cat_url(pilar_key)}">{html_lib.escape(pilar_titulo)}</a></p>')

    imagem_capa = fm.get("imagem_capa")
    og_image = f"{dominio}/{imagem_capa}" if imagem_capa else ""
    hero_img = ""
    if imagem_capa:
        hero_img = f'<img class="hero-img" src="/{imagem_capa}" alt="{html_lib.escape(fm["titulo"])}">'
        fotografo, fonte_url = fm.get("imagem_fotografo"), fm.get("imagem_fotografo_url")
        if fm.get("imagem_fonte") == "ia":   # 22/10: foto gerada por IA (plano B) sempre se declara
            hero_img += '<p class="image-credit">Imagem ilustrativa gerada por inteligência artificial</p>'
        elif fotografo and fonte_url:
            fonte_nome = (fm.get("imagem_fonte") or "").capitalize()
            hero_img += (f'<p class="image-credit">Foto: <a href="{html_lib.escape(fonte_url)}">'
                         f'{html_lib.escape(fotografo)}</a> via {html_lib.escape(fonte_nome)}'
                         + (' · Foto ilustrativa: não é o animal citado no texto' if fm.get("foto_ilustrativa") else '') + '</p>')

    extras_artista = ""
    fa = fm.get("foto_artista")
    if isinstance(fa, dict) and fa.get("arquivo"):
        extras_artista += (f'<figure class="foto-artista"><img src="/{fa["arquivo"]}" alt="{html_lib.escape(str(fa.get("legenda", "")))}" loading="lazy">'
                           f'<figcaption>{html_lib.escape(str(fa.get("legenda", "")))} Foto: <a href="{html_lib.escape(str(fa.get("fonte_url", "")))}">{html_lib.escape(str(fa.get("autor", "")))}</a>, '
                           f'<a href="{html_lib.escape(str(fa.get("licenca_url", "")))}">{html_lib.escape(str(fa.get("licenca", "")))}</a>, via Wikimedia Commons.</figcaption></figure>')
    ig = str(fm.get("embed_instagram") or "").strip()
    if ig:
        extras_artista += (f'<div class="ig-embed"><button type="button" class="btn" onclick="this.parentNode.innerHTML=\'<iframe src=&quot;https://www.instagram.com/{html_lib.escape(ig)}/embed&quot; '
                           f'width=&quot;400&quot; height=&quot;480&quot; frameborder=&quot;0&quot; scrolling=&quot;no&quot; loading=&quot;lazy&quot; allowtransparency=&quot;true&quot;></iframe>\'">'
                           f'📷 Ver o perfil oficial no Instagram (@{html_lib.escape(ig)})</button>'
                           f'<p class="image-credit">Conteúdo do perfil oficial, exibido pela incorporação do Instagram. <a href="https://www.instagram.com/{html_lib.escape(ig)}/">Abrir no Instagram</a></p></div>')

    selo_celeb = ""
    if fm.get("serie") == "pet-celebridade" and fm.get("artista"):
        selo_celeb = (f'<div class="celeb-selo"><span class="celeb-serie">Pet Celebridade · Celebrity Pets</span>'
                      f'<span class="celeb-nome">{html_lib.escape(str(fm["artista"]))}</span>'
                      f'<span class="celeb-pet">e {html_lib.escape(str(fm.get("pet_nome", "o pet")))}, {html_lib.escape(str(fm.get("pet_raca", "seu melhor amigo")))}</span></div>')

    video_html = ""
    video_url = fm.get("video_url") or (f"/videos/{slug}.mp4" if (BUILD_DIR / "videos" / f"{slug}.mp4").exists() else None) or VIDEOS_ARTIGOS.get(slug)
    if video_url:
        poster = f' poster="/{imagem_capa}"' if imagem_capa else ""
        video_html = (f'<figure class="article-video"><video controls playsinline preload="none"{poster} '
                      f'src="{html_lib.escape(video_url)}" style="width:100%;max-width:420px;display:block;margin:12px auto"></video>'
                      f'<figcaption style="text-align:center;font-size:.9rem">Veja em vídeo (30 segundos)</figcaption></figure>')

    body_html = md_to_html(_variar_fecho(body, slug))
    # Links de afiliado (Shopee): sempre rel="sponsored nofollow noopener" e nova aba, mesmo que o markdown traga o link simples.
    import re as _raf
    body_html = _raf.sub(r'<a href="(https://s\.shopee\.com\.br/[^"]+)">',
                         r'<a href="\1" rel="sponsored nofollow noopener" target="_blank">', body_html)
    # Imagens no meio do artigo (Allan, 22/10/2026): front-matter imagens_corpo: [{arquivo, alt, fotografo, fonte_url}]
    _ic = [x for x in (fm.get("imagens_corpo") or []) if isinstance(x, dict) and x.get("arquivo")]
    if _ic:
        import re as _re2
        _pos = [m.start() for m in _re2.finditer(r"<h2\b", body_html)]
        _alvos = []
        for n, _x in enumerate(_ic):
            _idx = 2 + 2 * n          # antes do 3o, 5o... subtitulo
            _alvos.append((_pos[_idx] if _idx < len(_pos) else (_pos[-1] if _pos else len(body_html)), _x))
        for _p_, _x in sorted(_alvos, key=lambda t: -t[0]):
            _cred = (f' Foto: <a href="{html_lib.escape(str(_x.get("fonte_url", "")))}">{html_lib.escape(str(_x.get("fotografo", "")))}</a> via Pexels'
                     if _x.get("fotografo") else "")
            _fig = (f'<figure class="foto-corpo"><img src="/{_x["arquivo"]}" alt="{html_lib.escape(str(_x.get("alt", fm["titulo"])))}" loading="lazy" width="940" height="627">'
                    f'<figcaption>{html_lib.escape(str(_x.get("alt", "")))}.{_cred}</figcaption></figure>')
            body_html = body_html[:_p_] + _fig + body_html[_p_:]
    produto_faixa = render_produto_topo(load_produto_destaque(fm))
    _ed2 = (EQUIPE.get("editor") or {})
    _atu = _data_br(fm.get("atualizado_em") or "") or _data_br(_data_iso(fm))
    transparencia = ('<aside class="transparencia" style="margin:24px 0;padding:14px 16px;border-left:4px solid #f97316;background:#fff7ed;font-size:.92rem">'
                     '<strong>Como este guia foi feito.</strong> Escrito com apoio de IA, com as fontes citadas acima, sob responsabilidade editorial de '
                     f'<a href="/sobre#equipe">{html_lib.escape(_ed2.get("nome", "Equipe Tutorial Pet"))}</a>. '
                     f'Atualizado em {_atu}. Não substitui a consulta com um médico-veterinário. '
                     'Viu algum erro? <a href="/contato">Avise a gente</a>.</aside>')
    cta = (f'<div class="cta-box"><p>Gostou deste guia? Tem mais conteúdo sobre '
           f'{html_lib.escape(pilar_titulo.lower())} esperando por você.</p>'
           f'<a class="btn" href="{cat_url(pilar_key)}">Ver mais sobre {html_lib.escape(pilar_titulo)}</a></div>')
    main = f"""{render_header(site["nome"], pilares)}
{breadcrumb}
<main class="article">
{selo_celeb}
{produto_faixa}
{hero_img}
{byline}
{selo_revisao}
{cat_linha}
{extras_artista}
{video_html}
{body_html}
{transparencia}
{produto_faixa}
{cta}
{render_redes("Gostou? Siga o Tutorial Pet e receba um vídeo novo por dia")}
</main>
{render_footer()}"""
    return page_shell(titulo_seo, fm.get("meta_description", ""), canonical, "article", main, jsonld_scripts,
                       og_image=og_image)


# ---- Revisão veterinária (28/10/2026): parceria com a médica veterinária Natasha Braga ----
# REGRA INEGOCIÁVEL: o selo "Revisado por" só aparece em artigo com revisado_por E revisado_em no frontmatter.
def _pessoa(pid) -> dict | None:
    p = ((EQUIPE.get("pessoas") or {}).get(str(pid or "").strip()))
    return p if isinstance(p, dict) and p.get("nome") else None


def _crmv_txt(p: dict) -> str:
    if not p.get("crmv"):
        return ""
    uf = str(p.get("crmv_uf") or "").strip().upper()
    return f"CRMV-{uf} {p['crmv']}" if uf else f"CRMV {p['crmv']}"


def _data_num(valor) -> str:
    """'2026-10-28' -> '28/10/2026' ('' se nao der para ler)."""
    try:
        a, m, d = str(valor)[:10].split("-")
        return f"{int(d):02d}/{int(m):02d}/{a}"
    except Exception:
        return ""


def _revisao_do_artigo(fm: dict) -> tuple[dict, str] | None:
    """(pessoa, data DD/MM/AAAA) se o artigo tem revisado_por E revisado_em validos; senao None."""
    # Atenção: o agente 04 (editor de qualidade) já grava revisado_em com HORA (timestamp) em quase todo artigo.
    # Só vale a data pura AAAA-MM-DD da revisão veterinária; timestamp nunca gera selo.
    import re as _rr
    p = _pessoa(fm.get("revisado_por"))
    v = str(fm.get("revisado_em") or "").strip()
    d = _data_num(v) if _rr.fullmatch(r"\d{4}-\d{2}-\d{2}", v) else ""
    return (p, d) if p and d else None


def _iniciais(nome: str) -> str:
    partes = [x for x in str(nome).split() if x[:1].isalpha()]
    return "".join(x[0].upper() for x in (partes[:1] + partes[-1:])) if partes else ""


def render_pessoa_card(p: dict) -> str:
    foto = str(p.get("foto") or "").strip()
    avatar = (f'<img class="pessoa-foto" src="/{html_lib.escape(foto.lstrip("/"))}" alt="{html_lib.escape(p["nome"])}" width="96" height="96" loading="lazy">'
              if foto else f'<div class="pessoa-foto pessoa-iniciais" aria-hidden="true">{html_lib.escape(_iniciais(p["nome"]))}</div>')
    crmv = _crmv_txt(p)
    linhas = [f'<strong class="pessoa-nome">{html_lib.escape(p["nome"])}</strong>',
              f'<span>{html_lib.escape(p.get("papel", ""))}</span>']
    if crmv:
        linhas.append(f'<span>{html_lib.escape(crmv)}</span>')
    if p.get("bio"):
        linhas.append(f'<p>{html_lib.escape(p["bio"])}</p>')
    if p.get("instagram"):
        usuario = p.get("instagram_usuario") or "Instagram"
        linhas.append(f'<a href="{html_lib.escape(p["instagram"])}" rel="noopener" target="_blank">Instagram {html_lib.escape(usuario)}</a>')
    return f'<div class="pessoa-card">{avatar}<div class="pessoa-info">{"".join(linhas)}</div></div>'


PESSOA_CSS = (".pessoa-card{display:flex;gap:16px;align-items:flex-start;margin:16px 0;padding:16px;border:1px solid #e5e7eb;border-radius:12px;background:#fafafa}"
              ".pessoa-foto{width:96px;height:96px;border-radius:50%;object-fit:cover;flex:none}"
              ".pessoa-iniciais{display:flex;align-items:center;justify-content:center;background:var(--color-primary,#f97316);color:#fff;font-size:1.8rem;font-weight:700}"
              ".pessoa-info{display:flex;flex-direction:column;gap:2px}.pessoa-info p{margin:6px 0}"
              ".revisado-por{font-size:.92rem;margin:-6px 0 12px;color:var(--color-text-muted,#555)}"
              "@media(max-width:520px){.pessoa-card{flex-direction:column;align-items:center;text-align:center}}")


def build_revisao_page(fm: dict, body: str, site: dict, pilares: dict, md_to_html, artigos: list[dict]) -> str:
    """Página /revisao-veterinaria: política (markdown) + cartão da revisora + lista automática dos artigos revisados."""
    dominio = site["dominio"].rstrip("/")
    p = _pessoa(EQUIPE.get("revisora_veterinaria"))
    quem = f'<h2 id="quem-revisa">Quem revisa</h2>{render_pessoa_card(p)}' if p else ""
    revisados = sorted(((f, _revisao_do_artigo(f)) for f in artigos if _revisao_do_artigo(f)),
                       key=lambda t: (t[1][1][6:] + t[1][1][3:5] + t[1][1][:2]), reverse=True)
    if revisados:
        itens = "".join(f'<li><a href="/{f["slug"]}">{html_lib.escape(f["titulo"])}</a> '
                        f'<span class="revisado-por">revisado em {d}</span></li>' for f, (_p, d) in revisados)
        lista = f'<h2 id="artigos-revisados">Artigos revisados</h2><ul>{itens}</ul>'
    else:
        lista = ('<h2 id="artigos-revisados">Artigos revisados</h2>'
                 '<p>Os primeiros artigos revisados saem em breve. Assim que a médica veterinária aprovar o primeiro, ele aparece nesta lista, com a data da revisão.</p>')
    main = f"""{render_header(site["nome"], pilares)}
<main class="legal">
{md_to_html(body)}
{quem}
{lista}
</main>
{render_footer()}"""
    return page_shell(fm.get("titulo", "Revisão veterinária") + " | " + site["nome"],
                      "Como funciona a revisão veterinária dos guias do Tutorial Pet: o que é revisado, quem revisa e como ler o selo.",
                      f"{dominio}/revisao-veterinaria", "website", main)


def build_legal_page(slug: str, fm: dict, body: str, site: dict, pilares: dict, md_to_html) -> str:
    dominio = site["dominio"].rstrip("/")
    canonical = f"{dominio}/{slug}"
    body_html = md_to_html(body)
    body_html = body_html.replace("<h2>Quem escreve e responde pelo conteúdo</h2>", '<h2 id="equipe">Quem escreve e responde pelo conteúdo</h2>')
    main = f"""{render_header(site["nome"], pilares)}
<main class="legal">
{body_html}
</main>
{render_footer()}"""
    return page_shell(fm.get("titulo", slug), site["nicho"][:150], canonical, "website", main)


# ---- Ícones de seguir (15/10/2026): redes do Tutorial Pet, com clique direto ----
ICONE_REDE = {
    "Instagram": '<svg viewBox="0 0 24 24" width="22" height="22" aria-hidden="true" fill="none" stroke="#fff" stroke-width="2"><rect x="3" y="3" width="18" height="18" rx="5"/><circle cx="12" cy="12" r="4"/><circle cx="17.3" cy="6.7" r="1" fill="#fff" stroke="none"/></svg>',
    "TikTok": '<svg viewBox="0 0 24 24" width="22" height="22" aria-hidden="true" fill="none" stroke="#fff" stroke-width="2.4" stroke-linecap="round"><path d="M14 4v10.5a3.5 3.5 0 1 1-3.5-3.5"/><path d="M14 4c.4 2.4 2 4 4.5 4.3"/></svg>',
    "Facebook": '<svg viewBox="0 0 24 24" width="22" height="22" aria-hidden="true" fill="#fff"><path d="M13.5 21v-7.5H16l.5-3h-3V8.7c0-.9.3-1.5 1.6-1.5h1.5V4.5c-.3 0-1.2-.1-2.2-.1-2.3 0-3.9 1.4-3.9 4v2.1H8v3h2.5V21z"/></svg>',
}
COR_REDE = {"Instagram": "#c13584", "TikTok": "#111111", "Facebook": "#1877f2"}


def render_redes(titulo: str = "Siga o Tutorial Pet", compacto: bool = False) -> str:
    cfg = ROOT / "config" / "redes_sociais.yaml"
    redes = [r for r in ((load_yaml(cfg) or {}).get("redes", []) if cfg.exists() else []) if (r.get("url") or "").strip()]
    if not redes:
        return ""
    itens = "".join(
        f'<a class="rede" href="{html_lib.escape(r["url"])}" target="_blank" rel="noopener me" aria-label="Seguir o Tutorial Pet no {html_lib.escape(r["nome"])}" '
        f'style="background:{COR_REDE.get(r["nome"], "#444")}">{ICONE_REDE.get(r["nome"], "")}'
        + ("" if compacto else f'<span>{html_lib.escape(r["nome"])}<small>{html_lib.escape(r.get("handle", ""))}</small></span>') + '</a>'
        for r in redes)
    cab = "" if compacto else f'<p class="redes-titulo">{html_lib.escape(titulo)}</p>'
    return f'<div class="redes{" redes-compacto" if compacto else ""}">{cab}<div class="redes-lista">{itens}</div></div>'


MESES = ["janeiro", "fevereiro", "março", "abril", "maio", "junho", "julho", "agosto", "setembro", "outubro", "novembro", "dezembro"]


def _data_br(valor) -> str:
    """'2026-10-15' -> '15 de outubro de 2026' ('' se nao der para ler)."""
    try:
        a, m, d = str(valor)[:10].split("-")
        return f"{int(d)} de {MESES[int(m) - 1]} de {a}"
    except Exception:
        return ""


def _data_iso(fm: dict) -> str:
    return str(fm.get("data") or str(fm.get("gerado_em") or "")[:10])[:10]


def render_destaque_novo(artigos_por_pilar: dict) -> str:
    """Regra do Allan (15/10/2026): o artigo mais novo vai sozinho para a capa, com a data."""
    todos = [fm for itens in artigos_por_pilar.values() for fm in itens]
    todos = [fm for fm in todos if _data_iso(fm)]
    if not todos:
        return ""
    novo = sorted(todos, key=lambda f: (_data_iso(f), str(f.get("gerado_em") or "")), reverse=True)[0]
    img = (f'<img src="/{novo["imagem_capa"]}" alt="{html_lib.escape(novo["titulo"])}" width="940" height="627">'
           if novo.get("imagem_capa") else "")
    resumo = html_lib.escape((novo.get("meta_description") or "")[:180])
    return (f'<section class="novo-destaque" aria-label="Artigo mais recente"><a href="/{novo["slug"]}">{img}'
            f'<span class="novo-texto"><span class="novo-selo">Novo · {html_lib.escape(_data_br(_data_iso(novo)))}</span>'
            f'<span class="novo-titulo">{html_lib.escape(novo["titulo"])}</span>'
            f'<span class="novo-resumo">{resumo}</span><span class="slide-cta">Ler o artigo →</span></span></a></section>')


def render_pet_celebridade(artigos_por_pilar: dict) -> str:
    """Seção fixa 'Pet Celebridade · Celebrity Pets' (ordem do Allan, 15/10/2026): artista em destaque."""
    itens = [fm for l in artigos_por_pilar.values() for fm in l if fm.get("serie") == "pet-celebridade" and fm.get("artista")]
    itens.sort(key=lambda f: (_data_iso(f), str(f.get("gerado_em") or "")), reverse=True)
    if not itens:
        return ""
    cards = "".join(
        f'<div class="card celeb-card"><a class="card-link" href="/{fm["slug"]}">'
        + (f'<img class="card-cover" src="/{fm["imagem_capa"]}" alt="{html_lib.escape(fm["titulo"])}">' if fm.get("imagem_capa") else "")
        + f'<div class="card-body"><div class="celeb-nome-card">{html_lib.escape(str(fm["artista"]))}</div>'
          f'<div class="card-title">{html_lib.escape(fm["titulo"])}</div>'
          f'<div class="card-data">{html_lib.escape(_data_br(_data_iso(fm)))}</div></div></a></div>' for fm in itens)
    return (f'<section class="pilar-section" id="pet-celebridade"><h2>Pet Celebridade <span class="pilar-tag">Celebrity Pets</span></h2>'
            f'<p class="celeb-sub">O melhor amigo dos famosos: quem é o pet, a raça e o que ele ensina para o seu.</p>'
            f'<div class="card-grid">{cards}</div></section>')


def render_ultimos(artigos_por_pilar: dict, n: int = 6) -> str:
    todos = [fm for itens in artigos_por_pilar.values() for fm in itens if _data_iso(fm)]
    todos = sorted(todos, key=lambda f: (_data_iso(f), str(f.get("gerado_em") or "")), reverse=True)[1:n + 1]
    if not todos:
        return ""
    cards = "".join(
        f'<div class="card"><a class="card-link" href="/{fm["slug"]}">'
        + (f'<img class="card-cover" src="/{fm["imagem_capa"]}" alt="{html_lib.escape(fm["titulo"])}">' if fm.get("imagem_capa") else "")
        + f'<div class="card-body"><div class="card-data">{html_lib.escape(_data_br(_data_iso(fm)))}</div>'
          f'<div class="card-title">{html_lib.escape(fm["titulo"])}</div></div></a></div>' for fm in todos)
    return f'<section class="pilar-section" id="ultimos"><h2>Últimos artigos</h2><div class="card-grid">{cards}</div></section>'


# ---- Tutorial Pet TV (15/10/2026): playlist dos nossos proprios videos, carregada so no clique ----
TV_JSON = ROOT / "config" / "sites" / "videos_tv.json"
RAW_MEDIA = "https://raw.githubusercontent.com/allandouradocontato-creator/tutorialpet/media/pacotes"
TV_STATUS_OK = {"ok", "aprovado", "agendado", "agendado_parcial", "publicado"}


def _tv_lista(artigos_por_pilar: dict) -> list[dict]:
    """Videos da TV, do mais novo para o mais antigo. Se a branch media estiver clonada (TV_MEDIA_DIR ou
    /tmp/media, como no workflow publicar_blog), regrava config/sites/videos_tv.json; senao usa o json salvo."""
    import os
    media = Path(os.environ.get("TV_MEDIA_DIR", "/tmp/media")) / "pacotes"
    itens = []
    if media.exists():
        for pasta in media.iterdir():
            man, vid = pasta / "manifest.json", pasta / "video.mp4"
            try:
                m = json.loads(man.read_text(encoding="utf-8"))
            except Exception:
                continue
            if vid.exists() and m.get("status") in TV_STATUS_OK:
                itens.append({"slug": pasta.name, "criado_em": str(m.get("criado_em") or "")})
        if itens:
            itens.sort(key=lambda x: x["criado_em"], reverse=True)
            TV_JSON.write_text(json.dumps(itens, ensure_ascii=False, indent=1), encoding="utf-8")
    elif TV_JSON.exists():
        try:
            itens = json.loads(TV_JSON.read_text(encoding="utf-8"))
        except Exception:
            itens = []
    por_slug = {fm["slug"]: fm for lst in artigos_por_pilar.values() for fm in lst}
    saida = []
    for it in itens:  # so entra video cujo artigo ja esta no ar
        fm = por_slug.get(it["slug"])
        if fm:
            saida.append({"slug": it["slug"], "titulo": fm["titulo"], "capa": fm.get("imagem_capa") or "",
                          "video": (f'/videos/{it["slug"]}.mp4' if (BUILD_DIR / "videos" / f'{it["slug"]}.mp4').exists() else f'{RAW_MEDIA}/{it["slug"]}/video.mp4'), "data": _data_br(_data_iso(fm))})
    return saida


def render_tv_home(tv: list[dict]) -> str:
    if not tv:
        return ""
    v = tv[0]
    img = f'<img src="/{v["capa"]}" alt="{html_lib.escape(v["titulo"])}" loading="lazy" width="940" height="627">' if v["capa"] else ""
    return (f'<section class="tv-home" aria-label="Tutorial Pet TV"><a href="/tv">{img}'
            f'<span class="tv-home-texto"><span class="novo-selo">▶ Tutorial Pet TV</span>'
            f'<span class="novo-titulo">Vídeos curtos de cuidados com cães e gatos, um atrás do outro</span>'
            f'<span class="slide-cta">Assistir agora →</span></span></a></section>')


TV_JS = """<script>(function(){var p=document.getElementById('tvPlayer');if(!p)return;
var it=[].slice.call(document.querySelectorAll('.tv-item')),t=document.getElementById('tvTitulo'),l=document.getElementById('tvLer'),x=document.getElementById('tvProx'),i=0;
function go(n,play){i=(n+it.length)%it.length;var b=it[i];p.poster=b.getAttribute('data-capa')||'';p.src=b.getAttribute('data-video');
t.textContent=b.getAttribute('data-titulo');x.textContent=it[(i+1)%it.length].getAttribute('data-titulo');l.href='/'+b.getAttribute('data-slug');it.forEach(function(x){x.classList.remove('ativo')});b.classList.add('ativo');
if(play){var r=p.play();if(r&&r.catch)r.catch(function(){})}}
it.forEach(function(b,k){b.addEventListener('click',function(){go(k,true);p.scrollIntoView({behavior:'smooth',block:'center'})})});
p.addEventListener('ended',function(){go(i+1,true)});go(0,false)})();</script>"""


def build_tv_page(site: dict, pilares: dict, tv: list[dict]) -> str:
    dominio = site["dominio"].rstrip("/")
    itens = "".join(
        f'<button type="button" class="tv-item" data-slug="{v["slug"]}" data-video="{html_lib.escape(v["video"])}" '
        f'data-capa="/{v["capa"]}" data-titulo="{html_lib.escape(v["titulo"])}">'
        + (f'<img src="/{v["capa"]}" alt="" loading="lazy" width="160" height="107">' if v["capa"] else "")
        + f'<span class="tv-item-texto"><span class="card-data">{html_lib.escape(v["data"])}</span>'
          f'<span class="card-title">{html_lib.escape(v["titulo"])}</span></span></button>' for v in tv)
    corpo = f"""{render_header(site["nome"], pilares)}
<main class="tv">
<h1 class="tv-h1">📺 Tutorial Pet TV</h1>
<p class="tv-sub">Vídeos curtos de cuidados com cães e gatos. Toque no play: ao terminar, o próximo começa sozinho.</p>
<div class="tv-set">
  <div class="tv-topo"><span class="tv-logo">📺 TUTORIAL PET TV</span><span class="tv-no-ar"><i></i> NO AR</span></div>
  <div class="tv-tela"><video id="tvPlayer" controls playsinline preload="none"></video></div>
  <div class="tv-rodape"><span class="tv-rotulo">AGORA PASSANDO</span><strong id="tvTitulo"></strong>
  <a id="tvLer" href="/">Ler o artigo completo →</a><span class="tv-prox">A seguir: <span id="tvProx"></span></span></div>
  <div class="tv-pe"></div>
</div>
{render_redes("Gostou da TV? Siga o Tutorial Pet")}
<h2>Na programação</h2>
<div class="tv-lista">{itens}</div>
</main>
{render_footer()}{TV_JS}"""
    return page_shell("Tutorial Pet TV: vídeos de cuidados com cães e gatos | " + site["nome"],
                      "Assista aos vídeos curtos do Tutorial Pet sobre cuidados, comportamento e rotina de cães e gatos, um atrás do outro.",
                      f"{dominio}/tv", "website", corpo)


def render_carrossel(artigos_por_pilar: dict) -> str:
    """Banner rotativo no topo da home: cada slide divulga um artigo (config/home_destaques.yaml)."""
    cfg = ROOT / "config" / "home_destaques.yaml"
    if not cfg.exists():
        return ""
    por_slug = {fm["slug"]: fm for itens in artigos_por_pilar.values() for fm in itens}
    slides = []
    for d in (load_yaml(cfg) or {}).get("destaques", []):
        fm = por_slug.get(d.get("slug"))
        if not fm or not fm.get("imagem_capa"):
            continue
        i = len(slides)
        slides.append(
            f'<a class="slide" href="/{fm["slug"]}" aria-label="{html_lib.escape(fm["titulo"])}"{"" if i == 0 else " tabindex=\"-1\""}>'
            f'<img src="/{fm["imagem_capa"]}" alt="{html_lib.escape(fm["titulo"])}"'
            f'{"" if i == 0 else " loading=\"lazy\""} width="940" height="627">'
            f'<span class="slide-texto"><span class="slide-rotulo">{html_lib.escape(d.get("rotulo", ""))}</span>'
            f'<span class="slide-titulo">{html_lib.escape(d.get("chamada") or fm["titulo"])}</span>'
            f'<span class="slide-cta">Ler o guia →</span></span></a>')
    if len(slides) < 3:
        return ""
    pontos = "".join(f'<button type="button" class="ponto" aria-label="Banner {i + 1}"></button>' for i in range(len(slides)))
    return (f'<section class="carrossel" aria-roledescription="carrossel" aria-label="Destaques do blog">'
            f'<div class="slides">{"".join(slides)}</div>'
            f'<button type="button" class="seta ant" aria-label="Banner anterior">‹</button>'
            f'<button type="button" class="seta prox" aria-label="Próximo banner">›</button>'
            f'<div class="pontos">{pontos}</div></section>' + CARROSSEL_JS)


def build_home_page(site: dict, pilares: dict, artigos_por_pilar: dict, tv: list | None = None) -> str:
    dominio = site["dominio"].rstrip("/")
    sections = []
    for pilar_key, titulo in pilares.items():
        itens = artigos_por_pilar.get(pilar_key, [])
        if not itens:
            continue
        visual = PILAR_VISUAL.get(pilar_key, PILAR_VISUAL_PADRAO)
        cards = "".join(
            f'<div class="card"><a class="card-link" href="/{fm["slug"]}">'
            + (f'<img class="card-cover" src="/{fm["imagem_capa"]}" alt="{html_lib.escape(fm["titulo"])}">'
               if fm.get("imagem_capa") else
               f'<div class="card-cover" style="background:{visual["bg"]}">{visual["emoji"]}</div>')
            + f'<div class="card-body"><div class="card-data">{html_lib.escape(_data_br(_data_iso(fm)))}</div>'
            f'<div class="card-title">{html_lib.escape(fm["titulo"])}</div></div>'
            f'</a></div>'
            for fm in itens
        )
        sections.append(
            f'<section class="pilar-section" id="{pilar_key}">'
            f'<h2><a href="{cat_url(pilar_key)}">{html_lib.escape(titulo)}</a> <span class="pilar-tag">{len(itens)} artigo(s)</span></h2>'
            f'<div class="card-grid">{cards}</div></section>'
        )

    main = f"""{render_header(site["nome"], pilares)}
<main class="home">
{render_tv_home(tv or [])}
{render_destaque_novo(artigos_por_pilar)}
{render_pet_celebridade(artigos_por_pilar)}
{render_carrossel(artigos_por_pilar)}
<div class="hero"><h1>{html_lib.escape(site["nome"])}</h1><p>{html_lib.escape(site["nicho"])}</p>{render_redes("Siga o Tutorial Pet")}</div>
{render_ultimos(artigos_por_pilar)}
{''.join(sections)}
</main>
{render_footer()}"""
    return page_shell(site["nome"], site["nicho"][:155], f"{dominio}/", "website", main)


def _resumo_artigo(body: str, limite: int = 170) -> str:
    """Primeiro parágrafo de texto do artigo, sem markdown, cortado em fim de palavra."""
    import re as _r
    for bloco in _r.split(r"\n\s*\n", body):
        b = bloco.strip()
        if not b or b.startswith(("#", "-", "*", ">", "|", "!")):
            continue
        b = _r.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", b)
        b = _r.sub(r"[*_`]", "", b)
        b = " ".join(b.split())
        if len(b) <= limite:
            return b
        corte = b[:limite].rsplit(" ", 1)[0].rstrip(",;:- ")
        return corte + "…"
    return ""


CAT_CSS = (".categoria-link{margin:-4px 0 14px;font-size:.88rem;color:var(--color-text-muted)}"
           ".categoria-link a{color:var(--color-primary);font-weight:600}"
           ".footer-cats{display:flex;flex-wrap:wrap;justify-content:center;gap:6px 16px;margin:10px 0}"
           ".cat-intro{max-width:760px;margin:0 auto 8px}.cat-intro p{line-height:1.65}"
           ".card-resumo{font-size:.86rem;line-height:1.45;color:var(--color-text-muted,#555);margin-top:6px}"
           ".cat-outras{margin-top:2.4em}.cat-outras a{display:inline-block;margin:4px 10px 4px 0}")


def build_category_page(key: str, titulo: str, itens: list[dict], site: dict, pilares: dict) -> str:
    dominio = site["dominio"].rstrip("/")
    cfg = CATEGORIAS.get(key) or {}
    paras = cfg.get("descricao") or []
    intro = "".join(f"<p>{html_lib.escape(str(x))}</p>" for x in paras)
    itens = sorted(itens, key=lambda f: (_data_iso(f), str(f.get("gerado_em") or "")), reverse=True)
    visual = PILAR_VISUAL.get(key, PILAR_VISUAL_PADRAO)
    cards = "".join(
        f'<div class="card"><a class="card-link" href="/{fm["slug"]}">'
        + (f'<img class="card-cover" src="/{fm["imagem_capa"]}" alt="{html_lib.escape(fm["titulo"])}" loading="lazy">'
           if fm.get("imagem_capa") else
           f'<div class="card-cover" style="background:{visual["bg"]}">{visual["emoji"]}</div>')
        + f'<div class="card-body"><div class="card-title">{html_lib.escape(fm["titulo"])}</div>'
          f'<div class="card-resumo">{html_lib.escape(fm.get("_resumo", ""))}</div></div></a></div>'
        for fm in itens)
    outras = "".join(f'<a href="{cat_url(k)}">{html_lib.escape(n)}</a>' for k, n in pilares.items() if k != key)
    if key != "pet-celebridade":
        outras += f'<a href="{cat_url("pet-celebridade")}">Pet Celebridade</a>'
    if key != COLUNA_VET:
        outras += f'<a href="{cat_url(COLUNA_VET)}">Pergunte à veterinária</a>'
    canonical = f"{dominio}{cat_url(key)}"
    extra_head = ""
    if itens:
        secao = (f'<section class="pilar-section"><h2>Artigos de {html_lib.escape(titulo)} <span class="pilar-tag">{len(itens)} artigo(s)</span></h2>'
                 f'<div class="card-grid">{cards}</div></section>')
    else:   # coluna ainda sem resposta publicada: nao entra no sitemap e fica noindex ate o 1o artigo revisado
        secao = ('<section class="pilar-section"><h2>As primeiras respostas saem em breve</h2>'
                 '<p>Estamos reunindo as perguntas mais frequentes dos tutores para a médica veterinária responder. '
                 'Quer ver a sua dúvida aqui? Envie pela página de <a href="/contato">Contato</a>, com o assunto "Pergunta para a veterinária".</p>'
                 '<p>Enquanto isso, saiba <a href="/revisao-veterinaria">como funciona a revisão veterinária</a> dos nossos guias.</p></section>')
        extra_head = '<meta name="robots" content="noindex">'
    meta = (paras[0] if paras else titulo)[:155]
    main = f"""{render_header(site["nome"], pilares)}
<div class="breadcrumb"><a href="/">Início</a> &gt; {html_lib.escape(titulo)}</div>
<main class="home categoria">
<div class="cat-intro"><h1>{html_lib.escape(titulo)}</h1>{intro}</div>
{secao}
<nav class="cat-outras" aria-label="Outras categorias"><h2>Outras categorias</h2>{outras}</nav>
</main>
{render_footer(pilares)}"""
    return page_shell(f"{titulo}: guias para cães e gatos | {site['nome']}", meta, canonical, "website", main, extra_head)


def build_sitemap(site: dict, artigos: list[dict], tv: bool = False, categorias: list[str] | None = None) -> str:
    dominio = site["dominio"].rstrip("/")
    urls = [f"{dominio}/"] + [f"{dominio}/{slug}" for slug in LEGAL_PAGES_ORDER] + \
           [f"{dominio}{cat_url(k)}" for k in (categorias or [])] + \
           [f"{dominio}/{fm['slug']}" for fm in artigos] + ([f"{dominio}/tv"] if tv else [])
    entries = "\n".join(f"  <url>\n    <loc>{u}</loc>\n  </url>" for u in urls)
    return (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        f"{entries}\n"
        "</urlset>\n"
    )


def build_robots(site: dict) -> str:
    dominio = site["dominio"].rstrip("/")
    return f"User-agent: *\nAllow: /\n\nSitemap: {dominio}/sitemap.xml\n"


def run(site_id: str) -> dict:
    site = load_site(site_id)
    md_to_html = load_agent07_markdown_converter()
    pilares = site.get("pilares", {})
    _PILARES_GLOBAL.clear()
    _PILARES_GLOBAL.update(pilares)

    artigos = []
    for path in sorted(OTIMIZADOS_DIR.glob("*.md")):
        try:
            fm, body = read_markdown(path)
        except MarkdownError:
            continue
        jsonld_path = ROOT / fm.get("dados_estruturados_arquivo", "")
        structured_data = json.loads(jsonld_path.read_text(encoding="utf-8")) if jsonld_path.exists() else {}
        artigos.append((fm, body, structured_data))

    BUILD_DIR.mkdir(parents=True, exist_ok=True)

    # 25/10/2026: os video.mp4 da branch media somem com o tempo e a TV/artigos ficavam com video morto.
    # Copia para o proprio site (Cloudflare Pages, limite 25 MB por arquivo) os videos de artigos que ja estao no ar.
    import os as _os
    _media = Path(_os.environ.get("TV_MEDIA_DIR", "/tmp/media")) / "pacotes"
    if _media.exists():
        (BUILD_DIR / "videos").mkdir(exist_ok=True)
        for _fm, _b, _sd in artigos:
            _v = _media / _fm["slug"] / "video.mp4"
            _d = BUILD_DIR / "videos" / f'{_fm["slug"]}.mp4'
            if _v.exists() and not _d.exists() and _v.stat().st_size <= 24 * 1024 * 1024:
                _d.write_bytes(_v.read_bytes())

    artigos_por_pilar: dict[str, list[dict]] = {}
    for fm, body, structured_data in artigos:
        pilar_key = fm.get("pilar", "outros")
        fm["_resumo"] = _resumo_artigo(body)
        artigos_por_pilar.setdefault(pilar_key, []).append(fm)
        html_out = build_article_page(fm, body, structured_data, site, pilares, md_to_html)
        (BUILD_DIR / f"{fm['slug']}.html").write_text(html_out, encoding="utf-8")

    legal_gerados = []
    legal_dir = LEGAL_DIR / site_id
    for slug in LEGAL_PAGES_ORDER:
        legal_path = legal_dir / f"{slug}.md"
        if not legal_path.exists():
            continue
        fm, body = read_markdown(legal_path)
        if slug == "revisao-veterinaria":
            html_out = build_revisao_page(fm, body, site, pilares, md_to_html, [a[0] for a in artigos])
        else:
            html_out = build_legal_page(slug, fm, body, site, pilares, md_to_html)
        (BUILD_DIR / f"{slug}.html").write_text(html_out, encoding="utf-8")
        legal_gerados.append(slug)

    n_imagens = 0
    imagens_src = ROOT / "data" / "visual" / "imagens"
    if imagens_src.exists():
        imagens_dst = BUILD_DIR / "imagens"
        imagens_dst.mkdir(parents=True, exist_ok=True)
        for fm, _, _ in artigos:
            _fa = fm.get("foto_artista")
            if isinstance(_fa, dict) and _fa.get("arquivo"):
                _o = imagens_src / Path(_fa["arquivo"]).name
                if _o.exists():
                    (imagens_dst / _o.name).write_bytes(_o.read_bytes())
            for _ib in (fm.get("imagens_corpo") or []):
                if isinstance(_ib, dict) and _ib.get("arquivo"):
                    _o = imagens_src / Path(_ib["arquivo"]).name
                    if _o.exists():
                        (imagens_dst / _o.name).write_bytes(_o.read_bytes())
            imagem_capa = fm.get("imagem_capa")
            if not imagem_capa:
                continue
            nome_arquivo = Path(imagem_capa).name
            origem = imagens_src / nome_arquivo
            if origem.exists():
                (imagens_dst / nome_arquivo).write_bytes(origem.read_bytes())
                n_imagens += 1

    # 404 de verdade: o Cloudflare Pages só devolve status 404 se existir 404.html na raiz (sem ele, qualquer
    # endereço inexistente respondia 200 com a página inicial: soft-404 ruim para SEO e AdSense).
    dominio_404 = site["dominio"].rstrip("/")
    corpo_404 = f"""{render_header(site["nome"], pilares)}
<main class="legal">
<h1>Página não encontrada</h1>
<p>Não achamos esse endereço. Ele pode ter mudado ou nunca ter existido.</p>
<p><a href="/">Voltar para a página inicial</a> e escolher um guia para o seu pet.</p>
</main>
{render_footer()}"""
    (BUILD_DIR / "404.html").write_text(
        page_shell("Página não encontrada | " + site["nome"], "Página não encontrada.", dominio_404 + "/", "website",
                   corpo_404, extra_head='<meta name="robots" content="noindex">'), encoding="utf-8")

    # Páginas de categoria (/categoria/<slug>): uma por pilar com artigos + a série Pet Celebridade
    (BUILD_DIR / "categoria").mkdir(exist_ok=True)
    cats_geradas = []
    for key, titulo in pilares.items():
        if artigos_por_pilar.get(key):
            (BUILD_DIR / "categoria" / f"{cat_slug(key)}.html").write_text(
                build_category_page(key, titulo, artigos_por_pilar[key], site, pilares), encoding="utf-8")
            cats_geradas.append(key)
    celeb = [fm for l in artigos_por_pilar.values() for fm in l if fm.get("serie") == "pet-celebridade" and fm.get("artista")]
    if celeb:
        (BUILD_DIR / "categoria" / "pet-celebridade.html").write_text(
            build_category_page("pet-celebridade", "Pet Celebridade", celeb, site, pilares), encoding="utf-8")
        cats_geradas.append("pet-celebridade")

    coluna = [fm for l in artigos_por_pilar.values() for fm in l if fm.get("coluna") == COLUNA_VET]
    (BUILD_DIR / "categoria" / f"{cat_slug(COLUNA_VET)}.html").write_text(
        build_category_page(COLUNA_VET, "Pergunte à veterinária", coluna, site, pilares), encoding="utf-8")
    if coluna:   # vazia = fora do sitemap
        cats_geradas.append(COLUNA_VET)

    tv = _tv_lista(artigos_por_pilar)
    if tv:
        (BUILD_DIR / "tv.html").write_text(build_tv_page(site, pilares, tv), encoding="utf-8")
    (BUILD_DIR / "index.html").write_text(build_home_page(site, pilares, artigos_por_pilar, tv), encoding="utf-8")
    (BUILD_DIR / "sitemap.xml").write_text(build_sitemap(site, [fm for fm, _, _ in artigos], bool(tv), cats_geradas), encoding="utf-8")
    (BUILD_DIR / "robots.txt").write_text(build_robots(site), encoding="utf-8")

    # Cache das capas: o nome do arquivo nao muda quando a foto e trocada; sem versao, o navegador do leitor
    # (Cache-Control 4 h) e o Cloudflare seguem mostrando a capa antiga. Acrescenta ?v=<hash do arquivo> em cada <img>.
    import hashlib, re as _re
    _hash = {f.name: hashlib.md5(f.read_bytes()).hexdigest()[:8] for f in (BUILD_DIR / "imagens").glob("*") if f.is_file()}
    for _h in BUILD_DIR.rglob("*.html"):
        _t = _h.read_text(encoding="utf-8")
        _n = _re.sub(r'(/imagens/([^"\'?\s)]+))(?=["\'\s)])', lambda m: m.group(1) + ("?v=" + _hash[m.group(2)] if m.group(2) in _hash else ""), _t)
        if _n != _t:
            _h.write_text(_n, encoding="utf-8")
    ads_txt_src = TECH_DIR / site_id / "ads.txt"
    if ads_txt_src.exists():
        (BUILD_DIR / "ads.txt").write_text(ads_txt_src.read_text(encoding="utf-8"), encoding="utf-8")

    for _g in (TECH_DIR / site_id).glob("google*.html"):
        (BUILD_DIR / _g.name).write_text(_g.read_text(encoding="utf-8"), encoding="utf-8")

    radio_src = ROOT / "site" / "radio"
    if radio_src.exists():
        radio_dst = BUILD_DIR / "radio"
        radio_dst.mkdir(parents=True, exist_ok=True)
        for arq in radio_src.iterdir():
            (radio_dst / arq.name).write_bytes(arq.read_bytes())

    (BUILD_DIR / "vercel.json").write_text(json.dumps({"cleanUrls": True, "trailingSlash": False}, indent=2),
                                            encoding="utf-8")

    return {
        "n_artigos": len(artigos), "n_paginas_legais": len(legal_gerados), "n_imagens": n_imagens,
        "arquivos_gerados": sorted(p.name for p in BUILD_DIR.iterdir()),
        "build_dir": str(BUILD_DIR.relative_to(ROOT)),
    }


def main() -> int:
    for stream in (sys.stdout, sys.stderr):
        stream.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description="Monta o site estático final em site/build/")
    parser.add_argument("--site", required=True, help="site_id (arquivo em config/sites/)")
    args = parser.parse_args()

    load_env_file()
    resultado = run(args.site)
    print(f"Site montado em {resultado['build_dir']}")
    print(f"  Artigos: {resultado['n_artigos']}")
    print(f"  Páginas legais: {resultado['n_paginas_legais']}")
    print(f"  Imagens publicadas: {resultado['n_imagens']}")
    print(f"  Arquivos: {', '.join(resultado['arquivos_gerados'])}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
