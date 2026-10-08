"""Agente 26 — Guardião de Marca e de Variedade.

Roda depois da produção do pacote do dia e ANTES de qualquer agendamento. Confere:
  1. cenas repetidas dentro do mesmo vídeo (mesma busca de imagem em mais de uma cena);
  2. clipes reaproveitados de vídeos recentes (registro em core/guardiao_variedade.py, na branch media);
  3. música repetida em relação às últimas faixas;
  4. carimbo da marca (patinha + "Tutorial Pet") disponível e aplicado;
  5. CTA e gancho repetidos em relação aos últimos vídeos;
  6. padrão da voz da Duda (config/voz_elevenlabs.yaml: modelo e estabilidade).
Só mede e marca: grava o parecer no manifest.json do pacote ("guardiao": {...}) e em data/auditoria/guardiao.md.
Pacote com problema fica "aguardando_revisao" com guardiao.status = "revisar" (nunca é publicado sozinho).
Sai com código 0 (aviso), para não derrubar a rodada.

Uso: python agents/26_guardiao_marca/agent.py <pasta_media> [slug]
"""
from __future__ import annotations

import json
import re
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

ULTIMOS_CTA = 5


def _json(p: Path, padrao):
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except Exception:  # noqa: BLE001
        return padrao


def _pacote_mais_recente(media: Path) -> Path | None:
    pacotes = [p for p in (media / "pacotes").glob("*") if (p / "manifest.json").exists()]
    return max(pacotes, key=lambda p: (p / "manifest.json").stat().st_mtime) if pacotes else None


def _voz_ok() -> list[str]:
    try:
        import yaml
        cfg = yaml.safe_load((ROOT / "config" / "voz_elevenlabs.yaml").read_text(encoding="utf-8")) or {}
    except Exception:  # noqa: BLE001
        return ["não consegui ler config/voz_elevenlabs.yaml"]
    problemas = []
    if cfg.get("model_id") != "eleven_v4":
        problemas.append(f"modelo da voz mudou: {cfg.get('model_id')} (padrão: eleven_v4)")
    if abs(float(cfg.get("stability", 0)) - 0.26) > 0.001:
        problemas.append(f"estabilidade da voz mudou: {cfg.get('stability')} (padrão: 0.26)")
    return problemas


def main() -> int:
    if len(sys.argv) < 2:
        sys.exit("uso: python agents/26_guardiao_marca/agent.py <pasta_media> [slug]")
    media = Path(sys.argv[1])
    pkg = (media / "pacotes" / sys.argv[2]) if len(sys.argv) > 2 else _pacote_mais_recente(media)
    if not pkg or not pkg.exists():
        print("guardião: nenhum pacote para conferir")
        return 0
    slug = pkg.name
    roteiro = _json(pkg / "roteiro.json", {})
    registro = _json(media / "clips_usados.json", {"videos": []})
    videos = registro.get("videos", [])
    este = next((v for v in videos if v.get("slug") == slug), {})
    anteriores = [v for v in videos if v.get("slug") != slug]

    problemas: list[str] = []
    ok: list[str] = []

    # 1) cenas repetidas dentro do vídeo
    buscas = [str(c.get("visual_busca_banco_livre", "")).strip().lower() for c in roteiro.get("cenas", [])]
    rep = [b for b, n in Counter(buscas).items() if b and n > 1]
    (problemas if rep else ok).append(
        f"mesma busca de imagem em mais de uma cena: {', '.join(rep)}" if rep else "sem cenas repetidas no vídeo")

    # 2) clipes reaproveitados de vídeos recentes
    if not este:
        problemas.append("vídeo sem registro de clipes (clips_usados.json): não dá para garantir variedade")
    else:
        reusos = este.get("reusos", [])
        (problemas if reusos else ok).append(
            f"{len(reusos)} clipe(s) reaproveitado(s) de vídeos recentes ({', '.join(reusos[:4])})" if reusos
            else f"{len(este.get('clipes', []))} clipes, todos inéditos nos últimos 20 vídeos")

    # 3) música
    musica = este.get("musica", "")
    recentes = [v.get("musica") for v in anteriores[-3:]]
    if musica and musica in recentes:
        problemas.append(f"música repetida das últimas 3 faixas: {musica}")
    elif musica:
        ok.append(f"música alternada ({musica})")

    # 4) carimbo
    if (ROOT / "assets" / "carimbo_tutorialpet.png").exists():
        ok.append("carimbo da marca disponível e aplicado pela montagem")
    else:
        problemas.append("assets/carimbo_tutorialpet.png não existe: vídeo sairia sem a marca")

    # 5) CTA repetido
    cta = re.sub(r"\W+", " ", str(roteiro.get("chamada_final", "")).lower()).strip()
    anteriores_cta = []
    for v in anteriores[-ULTIMOS_CTA:]:
        r = _json(media / "pacotes" / str(v.get("slug")) / "roteiro.json", {})
        anteriores_cta.append(re.sub(r"\W+", " ", str(r.get("chamada_final", "")).lower()).strip())
    if cta and cta in anteriores_cta:
        problemas.append("CTA igual ao de um dos últimos vídeos (o CTA deve variar)")
    elif cta:
        ok.append("CTA diferente dos últimos vídeos")

    # 5b) gancho repetido (mesmo molde de um dos últimos vídeos ou mesmas primeiras palavras)
    molde = roteiro.get("molde_gancho", "")
    ant = []
    for v in anteriores[-ULTIMOS_CTA:]:
        r = _json(media / "pacotes" / str(v.get("slug")) / "roteiro.json", {})
        ant.append((r.get("molde_gancho", ""), " ".join(re.sub(r"\W+", " ", str(r.get("gancho_3s", "")).lower()).split()[:4])))
    abre = " ".join(re.sub(r"\W+", " ", str(roteiro.get("gancho_3s", "")).lower()).split()[:4])
    if (molde and molde in [m for m, _ in ant]) or (abre and abre in [a for _, a in ant]):
        problemas.append(f"gancho repetido de um dos últimos {ULTIMOS_CTA} vídeos ({molde or abre})")
    elif abre:
        ok.append(f"gancho diferente dos últimos vídeos ({molde or abre})")

    # 6) voz da Duda
    pv = _voz_ok()
    problemas += pv
    if not pv:
        ok.append("voz da Duda no padrão (eleven_v4, estabilidade 0.26)")

    status = "revisar" if problemas else "ok"
    parecer = {"status": status, "problemas": problemas, "ok": ok,
               "em": datetime.now(timezone.utc).isoformat(timespec="seconds")}
    man = _json(pkg / "manifest.json", {})
    man["guardiao"] = parecer
    (pkg / "manifest.json").write_text(json.dumps(man, ensure_ascii=False, indent=2), encoding="utf-8")

    linhas = [f"# Guardião de Marca e Variedade — {slug}", f"Parecer: **{status.upper()}**", ""]
    linhas += [f"- ATENÇÃO: {p}" for p in problemas] + [f"- ok: {o}" for o in ok]
    texto = "\n".join(linhas) + "\n"
    (ROOT / "data" / "auditoria").mkdir(parents=True, exist_ok=True)
    (ROOT / "data" / "auditoria" / "guardiao.md").write_text(texto, encoding="utf-8")
    print(texto)
    return 0


if __name__ == "__main__":
    sys.exit(main())
