#!/usr/bin/env python3
"""Curadoria v4 de virais do TikTok (zero crédito): mede, pontua e lista candidatos.

Uso:
  python3 scripts/curadoria_tiktok.py urls.txt            # lista de links (1 por linha)
  python3 scripts/curadoria_tiktok.py urls.txt --csv saida.csv

Para cada vídeo: views, curtidas, comentários, compartilhamentos, idade, duração,
mediana de views dos últimos 12 vídeos da MESMA conta (viralidade relativa) e a
pontuação automática (parte numérica da v4). A parte de conteúdo (pico, voz do pet,
educativo/ilustrativo/engraçado) é preenchida por quem ASSISTE o vídeo.
Depende de yt-dlp (funciona no sandbox; TikTok avisa sobre impersonation, ignorar).
"""
import json, subprocess, sys, statistics, datetime, csv, re

def ytdlp_json(url, extra=()):
    cmd = ["yt-dlp", "-j", "--no-download", *extra, url]
    out = subprocess.run(cmd, capture_output=True, text=True, timeout=180).stdout
    return [json.loads(l) for l in out.splitlines() if l.startswith("{")]

_median_cache = {}
def account_median(user):
    if user in _median_cache:
        return _median_cache[user]
    rows = ytdlp_json(f"https://www.tiktok.com/@{user}", ("--flat-playlist", "--playlist-end", "12"))
    views = [r.get("view_count") or 0 for r in rows]
    med = statistics.median(views) if views else 0
    _median_cache[user] = med
    return med

def score_numeric(views, likes, com, rep, age_days, med):
    s = {}
    mult = views / med if med else 0
    # momentum absoluto (carona): o que importa é a onda que o público já está vendo
    s["momentum_abs"] = 25 if views >= 1_000_000 else 20 if views >= 500_000 else 12 if views >= 200_000 else 5 if views >= 50_000 else 0
    s["viral_relativa"] = 15 if mult >= 20 else 10 if mult >= 5 else 5 if mult >= 2 else 0
    share = 100 * rep / views if views else 0
    s["compartilhamento"] = 15 if share >= 3 else 10 if share >= 1.5 else 5 if share >= 0.8 else 0
    like_rate = 100 * likes / views if views else 0
    s["curtidas"] = 5 if like_rate >= 10 else 3 if like_rate >= 5 else 0
    s["frescor"] = 10 if age_days <= 3 else 6 if age_days <= 7 else 0
    return s, mult, share, like_rate

def main():
    if len(sys.argv) < 2:
        print(__doc__); sys.exit(1)
    urls = [l.strip() for l in open(sys.argv[1]) if l.strip() and not l.startswith("#")]
    out_csv = sys.argv[sys.argv.index("--csv") + 1] if "--csv" in sys.argv else None
    today = datetime.date.today()
    rows = []
    for u in urls:
        try:
            d = ytdlp_json(u)[0]
        except Exception as e:
            print("ERRO", u, e); continue
        views, likes = d.get("view_count") or 0, d.get("like_count") or 0
        com, rep = d.get("comment_count") or 0, d.get("repost_count") or 0
        age = (today - datetime.datetime.strptime(d["upload_date"], "%Y%m%d").date()).days
        med = account_median(d["uploader"])
        s, mult, share, lr = score_numeric(views, likes, com, rep, age, med)
        num = sum(s.values())  # máximo 70; os 30 restantes vêm da leitura de conteúdo
        rows.append(dict(url=u, user=d["uploader"], id=d["id"], views=views, likes=likes, coment=com,
                         compart=rep, idade_d=age, dur_s=d.get("duration"), mediana_conta=med,
                         multiplo=round(mult, 1), share_pct=round(share, 2), like_pct=round(lr, 1),
                         **s, score_numerico=num, titulo=(d.get("title") or "")[:80].replace("\n", " ")))
    rows.sort(key=lambda r: -r["score_numerico"])
    for r in rows:
        print(f"{r['score_numerico']:>3}/70  {r['views']/1e6:.2f}M  x{r['multiplo']}  share {r['share_pct']}%  "
              f"{r['idade_d']}d {r['dur_s']}s  @{r['user']}  {r['titulo'][:50]}")
    if out_csv:
        with open(out_csv, "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
        print("CSV:", out_csv)

if __name__ == "__main__":
    main()
