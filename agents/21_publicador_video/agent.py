"""Agente 21 — Publicador de Vídeo (prepara o agendamento Reel Instagram + Reel Facebook).

Pega um pacote aprovado (pacotes/<slug>/ no branch media) e monta o PEDIDO de agendamento do
Metricool (brand 7123441): legenda, URL pública do vídeo, redes e horário livre. Respeita o limite
combinado: no máximo 2 postagens por dia (12:00 e 20:00, America/Fortaleza).

IMPORTANTE (honesto): este agente NÃO envia. Hoje o envio é feito por uma sessão do Claude com o
conector do Metricool (createScheduledPost). Quando existir token da API do Metricool como secret,
basta ligar o envio aqui. Ele só gera pedidos para pacotes com status 'aprovado' no manifest.

Uso:
    python agents/21_publicador_video/agent.py <pasta_media> <slug> [--repo dono/repo] [--dia AAAA-MM-DD]
Saída: <pasta_media>/pacotes/<slug>/pedido_metricool.json e atualiza data/publicador/agenda.json
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import date, datetime, timedelta
from pathlib import Path

AGENT_DIR = Path(__file__).resolve().parent
ROOT = AGENT_DIR.parents[1]
AGENDA = ROOT / "data" / "publicador" / "agenda.json"
BRAND_ID = 7123441
FUSO = "America/Fortaleza"
REPO_PADRAO = "allandouradocontato-creator/tutorialpet"
# Decisão do Allan (08/10/2026), seguindo o Especialista TikTok: 2 vídeos por dia, ESCALONADOS por rede
# (um mesmo vídeo não sai nas 3 redes ao mesmo tempo; assim dá para ler o efeito do horário). Evitar 21h+.
TURNOS = {
    "A": {"facebook": "10:00", "tiktok": "12:00", "instagram": "14:00"},
    "B": {"facebook": "17:00", "tiktok": "18:00", "instagram": "20:00"},
}
LIMITE_DIA = len(TURNOS)
ESTRATEGIA = ROOT / "config" / "estrategia_social.yaml"
DIAS_SEMANA = ["seg", "ter", "qua", "qui", "sex", "sab", "dom"]
import os


def turnos_do_dia(dia: date) -> dict:
    """Horários do Estrategista de Redes Sociais para o dia da semana (config/estrategia_social.yaml).

    Turno A = o horário mais cedo de cada rede; turno B = o mais tarde. Se o arquivo faltar ou estiver
    inválido, cai nos TURNOS fixos acima (nunca deixa o dia sem agendar).
    """
    try:
        import yaml
        h = (yaml.safe_load(ESTRATEGIA.read_text(encoding="utf-8")) or {})["horarios"]
        d = DIAS_SEMANA[dia.weekday()]
        a, b = {}, {}
        for rede in ("facebook", "instagram", "tiktok"):
            hs = sorted(str(x) for x in h[rede][d])
            a[rede], b[rede] = hs[0], hs[-1]
        if all(a[r] != b[r] for r in a):
            return {"A": a, "B": b}
    except Exception:  # noqa: BLE001
        pass
    return TURNOS
TIKTOK_ATIVO = os.environ.get("TIKTOK_ATIVO") == "1" or (ROOT / "config" / "tiktok_ativo.txt").exists()
REDES = ["facebook", "instagram"] + (["tiktok"] if TIKTOK_ATIVO else [])


def agora_fortaleza() -> datetime:
    """Hora local de Fortaleza sem fuso (a nuvem roda em UTC; usar datetime.now() puro erraria o slot em 3h)."""
    from zoneinfo import ZoneInfo
    return datetime.now(ZoneInfo(FUSO)).replace(tzinfo=None)


def carregar_agenda() -> dict:
    if AGENDA.exists():
        return json.loads(AGENDA.read_text(encoding="utf-8"))
    return {}


def proximo_turno(agenda: dict, a_partir_de: date, agora: datetime | None = None) -> tuple[str, str]:
    """Primeiro (dia, turno) livre cujo primeiro horário ainda está pelo menos 30 min no futuro (hora de Fortaleza)."""
    agora = agora or agora_fortaleza()
    for delta in range(0, 60):
        dia = a_partir_de + timedelta(days=delta)
        usados = {x for x in agenda.get(dia.isoformat(), []) if x in TURNOS}
        for turno, horas in turnos_do_dia(dia).items():
            if turno in usados or len(usados) >= LIMITE_DIA:
                continue
            primeira = min(datetime.fromisoformat(f"{dia.isoformat()}T{h}:00") for h in horas.values())
            if primeira > agora + timedelta(minutes=30):
                return dia.isoformat(), turno
    raise SystemExit("sem turno livre nos próximos 60 dias")


def separar_links(legenda: str) -> tuple[str, str]:
    """Regra de alcance (06/10/2026): link no texto derruba o alcance. Linhas com URL vao para o
    PRIMEIRO COMENTARIO; o texto fica so com gancho e hashtags."""
    texto, comentario = [], []
    for linha in legenda.splitlines():
        (comentario if "http" in linha else texto).append(linha)
    corpo = "\n".join(texto).strip()
    # hashtags ficam por ultimo, depois do aviso
    tags = [l for l in corpo.splitlines() if l.strip().startswith("#")]
    sem_tags = "\n".join(l for l in corpo.splitlines() if not l.strip().startswith("#")).strip()
    final = sem_tags + "\n\n👇 Link no primeiro comentário" + ("\n\n" + " ".join(tags) if tags else "")
    return final.strip(), "\n".join(l.strip() for l in comentario).strip()


def legenda_tiktok(pkg: Path) -> str:
    """TikTok (playbook): 1 pergunta + 'veja o artigo no perfil' (sem prometer link clicável) + 2-3 hashtags de nicho."""
    import re
    r = json.loads((pkg / "roteiro.json").read_text(encoding="utf-8"))
    gancho = re.sub(r"\[[^\]]*\]", "", r.get("gancho_3s", "")).strip()
    tags = [t for t in r.get("hashtags", []) if t.lower() not in ("#tutorialpet", "#pets", "#pet")][:3] or r.get("hashtags", [])[:3]
    return f"{gancho} Veja o artigo no perfil. " + " ".join(tags)


def montar_pedido(pkg: Path, slug: str, repo: str, dia: str, turno: str) -> dict:
    legenda_completa = (pkg / "legenda.txt").read_text(encoding="utf-8").strip()
    legenda, primeiro_comentario = separar_links(legenda_completa)
    r = json.loads((pkg / "roteiro.json").read_text(encoding="utf-8")) if (pkg / "roteiro.json").exists() else {}
    titulo = r.get("titulo_video") or slug.replace("-", " ").capitalize()
    posts = []
    for rede in REDES:
        hora = turnos_do_dia(date.fromisoformat(dia))[turno][rede]
        post = {"rede": rede, "agendar_para": f"{dia}T{hora}:00"}
        if rede == "tiktok":
            post.update({"legenda": legenda_tiktok(pkg), "primeiro_comentario": "",
                         "tiktokData": {"privacyOption": "PUBLIC_TO_EVERYONE", "title": titulo[:90], "isAigc": True,
                                        "commercialContentOwnBrand": True}})
        elif rede == "facebook":
            post.update({"legenda": legenda, "primeiro_comentario": primeiro_comentario,
                         "facebookData": {"type": "REEL", "title": titulo}})
        else:
            post.update({"legenda": legenda, "primeiro_comentario": primeiro_comentario,
                         "instagramData": {"type": "REEL", "showReelOnFeed": True, "isAiGenerated": True}})
        posts.append(post)
    return {
        "brand_id": BRAND_ID,
        "timezone": FUSO,
        "turno": turno,
        "posts": posts,
        "video_url_publica": f"https://raw.githubusercontent.com/{repo}/media/pacotes/{slug}/video.mp4",
        "slug": slug,
        "regra": "2 vídeos/dia escalonados por rede; links do produto (landing) e do artigo vão no PRIMEIRO COMENTÁRIO (Instagram/Facebook), nunca no texto; TikTok sem link, com rótulo de IA e 'Sua marca'; criar UM post por rede, cada um no seu horário",
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("media")
    ap.add_argument("slug")
    ap.add_argument("--repo", default=REPO_PADRAO)
    ap.add_argument("--dia", default="")
    a = ap.parse_args()
    pkg = Path(a.media) / "pacotes" / a.slug
    if not pkg.exists():
        sys.exit(f"pacote não encontrado: {pkg}")
    manifest = json.loads((pkg / "manifest.json").read_text(encoding="utf-8"))
    if manifest.get("status") != "aprovado":
        sys.exit(f"pacote com status '{manifest.get('status')}': só 'aprovado' pode ser agendado")
    if (pkg / "pedido_metricool.json").exists():
        sys.exit("este pacote já tem pedido de agendamento (evita postar duas vezes)")

    agenda = carregar_agenda()
    dia, turno = proximo_turno(agenda, date.fromisoformat(a.dia) if a.dia else agora_fortaleza().date())
    pedido = montar_pedido(pkg, a.slug, a.repo, dia, turno)
    (pkg / "pedido_metricool.json").write_text(json.dumps(pedido, ensure_ascii=False, indent=2), encoding="utf-8")
    agenda.setdefault(dia, []).append(turno)
    AGENDA.parent.mkdir(parents=True, exist_ok=True)
    AGENDA.write_text(json.dumps(agenda, ensure_ascii=False, indent=2), encoding="utf-8")
    quando = ", ".join(f"{p['rede']} {p['agendar_para'][11:16]}" for p in pedido["posts"])
    print(f"Pedido pronto para {dia}, turno {turno} ({quando}; {FUSO}): {pkg / 'pedido_metricool.json'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
