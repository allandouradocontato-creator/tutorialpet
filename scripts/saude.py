"""Vigia determinístico da fábrica Tutorial Pet (sem IA, sem crédito do Claude).

Criado em 22/10/2026 — padrão "fábrica que não para": "parado" é medido e corrigido por script a cada hora;
humano e Claude só entram quando a correção automática falhou.

O que confere (e corrige):
  1. Produção: cota de 3 pacotes/dia (slots 06h, 10h, 14h de Fortaleza). Se faltar pacote, dispara fabrica.yml.
  2. Blog: todo slug de config/blog_aprovados.txt tem de responder 200 em tutorialpet.com.br. Se não, dispara publicar_blog.yml.
  3. Reprovados: artigo com 3 tentativas de reescrita sem sucesso vira pendência humana.
  4. Falha repetida: se a fábrica falhou 3x seguidas NÃO redispara em loop; abre alerta.
  5. (30/10/2026) Artigo novo hoje: pelo menos 1 após 11h, 2 após 15h e 3 após 19h (Fortaleza); abaixo disso, alerta.
  6. (30/10/2026) Links quebrados: amostra rotativa de 12 URLs do sitemap por rodada; 2 tentativas antes de alertar.
Alerta (só quando não conseguiu consertar): issue "SAUDE (automatico)" + Telegram se TELEGRAM_BOT_TOKEN/CHAT_ID existirem.
Limites: no máximo 6 disparos de fábrica e 3 de publicar_blog por dia (evita laço infinito).
"""
from __future__ import annotations

import datetime as dt
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request

REPO = os.environ.get("GITHUB_REPOSITORY", "allandouradocontato-creator/tutorialpet")
TOKEN = os.environ.get("GITHUB_TOKEN", "")
API = "https://api.github.com"
SITE = "https://tutorialpet.com.br"
SLOTS_Z = [9, 13, 17]          # 06:00, 10:00, 14:00 em Fortaleza (UTC-3)
GRACA_MIN = 100                # tempo para o cron (atrasado) + a rodada de ~25 min terminar
MAX_DISPAROS_FABRICA = 6
MAX_DISPAROS_BLOG = 3
DRY = "--dry" in sys.argv


def gh(caminho: str, metodo: str = "GET", dados: dict | None = None):
    req = urllib.request.Request(f"{API}{caminho}", method=metodo,
                                 data=json.dumps(dados).encode() if dados is not None else None,
                                 headers={"Authorization": f"Bearer {TOKEN}", "Accept": "application/vnd.github+json",
                                          "X-GitHub-Api-Version": "2022-11-28", "Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            corpo = r.read().decode()
            return json.loads(corpo) if corpo else {}
    except urllib.error.HTTPError as exc:
        print(f"[gh] {metodo} {caminho} -> HTTP {exc.code}: {exc.read().decode()[:200]}")
        return None


def inicio_do_dia_local(agora: dt.datetime) -> dt.datetime:
    base = agora.replace(hour=3, minute=0, second=0, microsecond=0)   # meia-noite de Fortaleza = 03:00Z
    return base if agora >= base else base - dt.timedelta(days=1)


def parse(ts: str) -> dt.datetime:
    return dt.datetime.fromisoformat(ts.replace("Z", "+00:00"))


def runs(workflow: str, desde: dt.datetime) -> list[dict]:
    q = urllib.parse.quote(">=" + desde.strftime("%Y-%m-%dT%H:%M:%SZ"))
    r = gh(f"/repos/{REPO}/actions/workflows/{workflow}/runs?per_page=50&created={q}")
    return (r or {}).get("workflow_runs", [])


def produziu(run_id: int) -> bool:
    r = gh(f"/repos/{REPO}/actions/runs/{run_id}/jobs?per_page=20")
    return any(j["name"] == "produzir" and j["conclusion"] == "success" for j in (r or {}).get("jobs", []))


def disparar(workflow: str) -> bool:
    if DRY:
        print(f"[dry] dispararia {workflow}")
        return True
    r = gh(f"/repos/{REPO}/actions/workflows/{workflow}/dispatches", "POST", {"ref": "main"})
    return r is not None


def http_ok(slug: str, agora: dt.datetime) -> int:
    url = f"{SITE}/{slug}?v={int(agora.timestamp())}"
    req = urllib.request.Request(url, method="HEAD", headers={"User-Agent": "saude-tutorialpet"})
    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            return r.status
    except urllib.error.HTTPError as exc:
        return exc.code
    except Exception:  # noqa: BLE001
        return 0


def ler(caminho: str) -> list[str]:
    try:
        return open(caminho, encoding="utf-8").read().splitlines()
    except FileNotFoundError:
        return []


def main() -> int:
    agora = dt.datetime.now(dt.timezone.utc)
    ini = inicio_do_dia_local(agora)
    acoes: list[str] = []
    alertas: list[str] = []

    # 1) PRODUÇÃO ---------------------------------------------------------------------------------
    esperados = sum(1 for h in SLOTS_Z if ini + dt.timedelta(hours=h - 3, minutes=GRACA_MIN) <= agora)
    rr = runs("fabrica.yml", ini)
    ativos = [r for r in rr if r["status"] in ("queued", "in_progress")]
    feitos = sum(1 for r in rr if r["conclusion"] == "success" and r["status"] == "completed" and produziu(r["id"]))
    disp_hoje = sum(1 for r in rr if r["event"] in ("workflow_dispatch", "push"))
    ultimas = [r for r in rr if r["status"] == "completed"][:3]
    falhou_3x = len(ultimas) == 3 and all(r["conclusion"] == "failure" for r in ultimas)
    print(f"[producao] esperados={esperados} feitos={feitos} ativos={len(ativos)} disparos_hoje={disp_hoje} falhou_3x={falhou_3x}")
    if feitos < esperados:
        if ativos:
            print("[producao] ja existe rodada em andamento; aguardando")
        elif falhou_3x:
            alertas.append("Fábrica falhou 3 vezes seguidas; não vou redisparar em laço. Ver o log da última rodada.")
        elif disp_hoje >= MAX_DISPAROS_FABRICA:
            alertas.append(f"Fábrica: {feitos}/{esperados} pacotes de hoje e o limite de {MAX_DISPAROS_FABRICA} disparos automáticos foi atingido.")
        elif disparar("fabrica.yml"):
            acoes.append(f"fabrica.yml disparada (pacotes hoje: {feitos}/{esperados})")
        else:
            alertas.append("Não consegui disparar fabrica.yml (permissão ou API).")

    # 2) BLOG -------------------------------------------------------------------------------------
    reprov = {l.split()[0] for l in ler("config/blog_reprovados.txt") if l.split() and not l.startswith("#")}
    slugs = []
    for l in ler("config/blog_aprovados.txt"):
        t = l.split()
        if t and not t[0].startswith("#") and t[0] not in reprov and t[0] not in slugs:
            slugs.append(t[0])
    fora = [s for s in slugs if http_ok(s, agora) != 200]
    print(f"[blog] aprovados={len(slugs)} fora_do_ar={fora}")
    if fora:
        pb = runs("publicar_blog.yml", ini)
        ativo_pb = any(r["status"] in ("queued", "in_progress") for r in pb)
        recente = any(parse(r["created_at"]) > agora - dt.timedelta(minutes=40) for r in pb)
        disp_pb = sum(1 for r in pb if r["event"] in ("workflow_dispatch", "push"))
        if ativo_pb or recente:
            print("[blog] publicar_blog rodou ou roda agora; aguardando propagacao")
        elif disp_pb >= MAX_DISPAROS_BLOG:
            alertas.append(f"Blog: {len(fora)} artigo(s) aprovado(s) fora do ar após {disp_pb} tentativas hoje: {', '.join(fora[:5])}.")
        elif disparar("publicar_blog.yml"):
            acoes.append(f"publicar_blog.yml disparada ({len(fora)} aprovado(s) fora do ar)")

    # 3) REPROVADOS SEM CONSERTO -----------------------------------------------------------------
    humanos = [l.split()[0] for l in ler("config/blog_reprovados.txt")
               if len(l.split()) > 1 and l.split()[1].isdigit() and int(l.split()[1]) >= 3 and not l.startswith("#")]
    if humanos:
        alertas.append(f"Artigo(s) reprovado(s) que a reescrita automática não resolveu (3 tentativas): {', '.join(humanos)}.")

    # 4) ARTIGO NOVO HOJE (30/10/2026, Allan: "alguém tem que conferir o que deveria ter acontecido e não aconteceu") -----
    local = agora - dt.timedelta(hours=3)
    hoje_local = local.strftime("%Y-%m-%d")
    novos_hoje = 0
    try:
        import glob
        import re as _re
        for f in glob.glob("data/seo_onpage/otimizados/*.md"):
            cab = open(f, encoding="utf-8").read(600)
            m = _re.search(r"^data:\s*'?(\d{4}-\d{2}-\d{2})", cab, _re.M)
            if m and m.group(1) == hoje_local:
                novos_hoje += 1
    except Exception as exc:  # noqa: BLE001
        print(f"[artigos] nao consegui contar: {exc}")
    meta_dia = 3 if local.hour >= 19 else (2 if local.hour >= 15 else (1 if local.hour >= 11 else 0))
    print(f"[artigos] novos_hoje={novos_hoje} esperados_ate_agora={meta_dia}")
    if novos_hoje < meta_dia:
        alertas.append(f"Blog: só {novos_hoje} artigo(s) novo(s) hoje; o esperado até agora era {meta_dia} (ritmo fixo de 3/dia). Conferir a fábrica e o publicar_blog.")

    # 5) LINKS QUEBRADOS: amostra rotativa de 12 URLs do sitemap por rodada (o site todo gira em ~8 rodadas) ------------
    quebrados: list[str] = []
    try:
        import re as _re2
        req = urllib.request.Request(f"{SITE}/sitemap.xml", headers={"User-Agent": "saude-tutorialpet"})
        locs = _re2.findall(r"<loc>([^<]+)</loc>", urllib.request.urlopen(req, timeout=20).read().decode("utf-8", "ignore"))
        if locs:
            passo = 12
            ini_i = (int(agora.timestamp() // 3600) * passo) % len(locs)
            amostra = [locs[(ini_i + k) % len(locs)] for k in range(min(passo, len(locs)))]
            for u in amostra:
                slug = u.replace(SITE, "").lstrip("/")
                cod = http_ok(slug, agora)
                if cod != 200:
                    cod = http_ok(slug, agora)   # 2a tentativa antes de acusar
                if cod != 200:
                    quebrados.append(f"{u} ({cod})")
        print(f"[links] sitemap={len(locs)} quebrados={quebrados}")
    except Exception as exc:  # noqa: BLE001
        print(f"[links] nao consegui ler o sitemap: {exc}")
    if quebrados:
        alertas.append("Link(s) do sitemap fora do ar: " + "; ".join(quebrados[:5]))

    # RESUMO + ALERTA ----------------------------------------------------------------------------
    linhas = [f"Saúde da fábrica — {agora:%Y-%m-%d %H:%M}Z",
              f"- pacotes hoje: {feitos}/{esperados}; artigos aprovados fora do ar: {len(fora)}; artigos novos hoje: {novos_hoje}; links quebrados na amostra: {len(quebrados)}"]
    linhas += [f"- ação: {a}" for a in acoes] + [f"- ALERTA: {a}" for a in alertas]
    texto = "\n".join(linhas)
    print(texto)
    if os.environ.get("GITHUB_STEP_SUMMARY"):
        open(os.environ["GITHUB_STEP_SUMMARY"], "a", encoding="utf-8").write(texto + "\n")
    if alertas and not DRY:
        avisar(texto, agora)
    elif not DRY:
        fechar_alerta_resolvido()
    return 0


def avisar(texto: str, agora: dt.datetime) -> None:
    abertas = gh(f"/repos/{REPO}/issues?state=open&per_page=30") or []
    existente = next((i for i in abertas if i["title"].startswith("SAUDE (automatico)") and "pull_request" not in i), None)
    novo_alerta = True
    if existente:
        # não repetir o mesmo aviso: só comenta se passou 6 h do último comentário
        ultimo = parse(existente.get("updated_at", existente["created_at"]))
        novo_alerta = agora - ultimo > dt.timedelta(hours=6)
        if novo_alerta:
            gh(f"/repos/{REPO}/issues/{existente['number']}/comments", "POST", {"body": texto})
    else:
        gh(f"/repos/{REPO}/issues", "POST", {"title": f"SAUDE (automatico) {agora:%Y-%m-%d}", "body": texto})
    token, chat = os.environ.get("TELEGRAM_BOT_TOKEN"), os.environ.get("TELEGRAM_CHAT_ID")
    if token and chat and novo_alerta:
        corpo = urllib.parse.urlencode({"chat_id": chat, "text": "Tutorial Pet — " + texto}).encode()
        try:
            urllib.request.urlopen(f"https://api.telegram.org/bot{token}/sendMessage", data=corpo, timeout=20)
        except Exception as exc:  # noqa: BLE001
            print("[telegram] falhou:", str(exc)[:100])


def fechar_alerta_resolvido() -> None:
    abertas = gh(f"/repos/{REPO}/issues?state=open&per_page=30") or []
    for i in abertas:
        if i["title"].startswith("SAUDE (automatico)") and "pull_request" not in i:
            gh(f"/repos/{REPO}/issues/{i['number']}/comments", "POST", {"body": "Resolvido automaticamente: tudo verde na última checagem."})
            gh(f"/repos/{REPO}/issues/{i['number']}", "PATCH", {"state": "closed"})


if __name__ == "__main__":
    sys.exit(main())
