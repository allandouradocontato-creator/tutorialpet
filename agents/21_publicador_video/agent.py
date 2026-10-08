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
SLOTS = ["09:00", "12:00", "17:00", "20:00"]  # 4 posts/dia (decisao do Allan 08/10/2026: volume p/ analise por ~3 dias)
LIMITE_DIA = 4
FUSO = "America/Fortaleza"
import os
REDES = ["instagram_reel", "facebook_reel"] + (["tiktok"] if os.environ.get("TIKTOK_ATIVO") == "1" or (ROOT / "config" / "tiktok_ativo.txt").exists() else [])  # TikTok entra criando config/tiktok_ativo.txt apos aprovacao da conta
REPO_PADRAO = "allandouradocontato-creator/tutorialpet"


def carregar_agenda() -> dict:
    if AGENDA.exists():
        return json.loads(AGENDA.read_text(encoding="utf-8"))
    return {}


def proximo_slot(agenda: dict, a_partir_de: date, agora: datetime | None = None) -> tuple[str, str]:
    """Primeiro (dia, hora) livre, no futuro, respeitando LIMITE_DIA por dia."""
    agora = agora or datetime.now()
    for delta in range(0, 60):
        dia = a_partir_de + timedelta(days=delta)
        usados = set(agenda.get(dia.isoformat(), []))
        for hora in SLOTS:
            if hora in usados or len(usados) >= LIMITE_DIA:
                continue
            quando = datetime.fromisoformat(f"{dia.isoformat()}T{hora}:00")
            if quando > agora + timedelta(minutes=30):
                return dia.isoformat(), hora
    raise SystemExit("sem horário livre nos próximos 60 dias")


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


def montar_pedido(pkg: Path, slug: str, repo: str, dia: str, hora: str) -> dict:
    legenda_completa = (pkg / "legenda.txt").read_text(encoding="utf-8").strip()
    legenda, primeiro_comentario = separar_links(legenda_completa)
    return {
        "brand_id": BRAND_ID,
        "timezone": FUSO,
        "agendar_para": f"{dia}T{hora}:00",
        "redes": REDES,
        "legenda": legenda,
        "primeiro_comentario": primeiro_comentario,
        "video_url_publica": f"https://raw.githubusercontent.com/{repo}/media/pacotes/{slug}/video.mp4",
        "slug": slug,
        "regra": "máx. 4 posts/dia; links do produto (landing) e do artigo vao no PRIMEIRO COMENTARIO, nunca no texto (conferido pelo agente 18 em legenda.txt)",
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("media")
    ap.add_argument("slug")
    ap.add_argument("--repo", default=REPO_PADRAO)
    ap.add_argument("--dia", default=date.today().isoformat())
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
    dia, hora = proximo_slot(agenda, date.fromisoformat(a.dia))
    pedido = montar_pedido(pkg, a.slug, a.repo, dia, hora)
    (pkg / "pedido_metricool.json").write_text(json.dumps(pedido, ensure_ascii=False, indent=2), encoding="utf-8")
    agenda.setdefault(dia, []).append(hora)
    AGENDA.parent.mkdir(parents=True, exist_ok=True)
    AGENDA.write_text(json.dumps(agenda, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Pedido pronto para {dia} {hora} ({FUSO}): {pkg / 'pedido_metricool.json'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
