"""Avisa Bing e outros buscadores (IndexNow) quando entra página nova no sitemap. Sem IA, sem custo.

Criado em 30/10/2026 (estratégia de tráfego). Observação honesta: o Google NÃO usa IndexNow; para o Google valem o
sitemap no Search Console e os links internos. IndexNow cobre Bing (e quem se apoia nele: Copilot, buscadores
alternativos) e é de graça.

Uso:
  python3 scripts/indexnow.py            # URLs novas entre $BEFORE e HEAD (padrão do workflow)
  python3 scripts/indexnow.py --todas    # manda o sitemap inteiro (uma vez, ou depois de grande mudança)
  python3 scripts/indexnow.py --dry      # só mostra o que mandaria
A chave é o arquivo data/platform_compliance/arquivos_tecnicos/<site>/indexnow_<chave>.txt (publicado em /<chave>.txt).
"""
from __future__ import annotations

import glob
import json
import os
import re
import subprocess
import sys
import time
import urllib.request

SITE = "https://tutorialpet.com.br"
HOST = "tutorialpet.com.br"
DRY = "--dry" in sys.argv


def chave() -> str:
    arqs = glob.glob("data/platform_compliance/arquivos_tecnicos/*/indexnow_*.txt")
    if not arqs:
        sys.exit("sem arquivo indexnow_<chave>.txt")
    return os.path.basename(arqs[0])[len("indexnow_"):-4]


def locs(xml: str) -> list[str]:
    return re.findall(r"<loc>([^<]+)</loc>", xml)


def git_show(ref: str) -> str:
    r = subprocess.run(["git", "show", f"{ref}:site/build/sitemap.xml"], capture_output=True, text=True)
    return r.stdout if r.returncode == 0 else ""


def status(url: str) -> int:
    req = urllib.request.Request(f"{url}?v={int(time.time())}", method="HEAD", headers={"User-Agent": "indexnow-tutorialpet"})
    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            return r.status
    except urllib.error.HTTPError as e:
        return e.code
    except Exception:  # noqa: BLE001
        return 0


def main() -> int:
    atual = locs(open("site/build/sitemap.xml", encoding="utf-8").read())
    if "--todas" in sys.argv:
        urls = atual
    else:
        antes = os.environ.get("BEFORE", "") or "HEAD~1"
        if set(antes) <= {"0"}:   # primeiro push de uma branch
            antes = "HEAD~1"
        velho = set(locs(git_show(antes)))
        urls = [u for u in atual if u not in velho]
    print(f"[indexnow] {len(urls)} URL(s) para avisar")
    if not urls:
        return 0
    # só avisa o que já responde 200 (o deploy do site leva alguns minutos depois do push)
    prontas: list[str] = []
    pendentes = list(urls)
    for _ in range(0 if DRY else 18):   # até ~6 min
        pendentes = [u for u in pendentes if status(u) != 200]
        prontas = [u for u in urls if u not in pendentes]
        if not pendentes:
            break
        time.sleep(20)
    if DRY:
        prontas = urls
    print(f"[indexnow] no ar: {len(prontas)}; ainda fora: {pendentes}")
    if not prontas or DRY:
        return 0
    k = chave()
    corpo = json.dumps({"host": HOST, "key": k, "keyLocation": f"{SITE}/{k}.txt", "urlList": prontas[:10000]}).encode()
    req = urllib.request.Request("https://api.indexnow.org/indexnow", data=corpo, method="POST",
                                 headers={"Content-Type": "application/json; charset=utf-8"})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            print(f"[indexnow] resposta {r.status} (200/202 = recebido)")
    except urllib.error.HTTPError as e:
        print(f"[indexnow] ERRO {e.code}: {e.read()[:200]!r}")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
