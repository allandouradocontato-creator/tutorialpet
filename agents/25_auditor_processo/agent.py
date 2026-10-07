"""Agente 25 — Auditor de Processo da fábrica.

Depois de cada rodada, mede o pacote do dia contra o PADRÃO da fábrica e escreve um relatório curto
(data/auditoria/ultimo.md, e no resumo da execução). Nasceu dos erros de 07/10/2026 que ninguém via:
música inaudível, gancho só em texto, modelo de voz errado, volume baixo, tags na tela.
Só mede e avisa: nunca corrige, nunca publica. Sai com código 0 (aviso), a menos que --estrito.

Uso: python agents/25_auditor_processo/agent.py <pasta_media> [slug]
"""
from __future__ import annotations

import json
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SAIDA = ROOT / "data" / "auditoria"
CTA_VERBOS = re.compile(r"segue|comenta|compartilha|salva|manda|conta nos|tutorialpet\.com\.br|vem com a gente", re.I)


def lufs(video: Path) -> float | None:
    r = subprocess.run(["ffmpeg", "-nostats", "-i", str(video), "-af", "ebur128", "-f", "null", "-"],
                       capture_output=True, text=True, errors="replace")
    achados = re.findall(r"^\s+I:\s+(-?\d+(?:\.\d+)?)\s+LUFS", r.stderr, re.M)
    return float(achados[-1]) if achados else None


def duracao(video: Path) -> float:
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(video)],
                       capture_output=True, text=True)
    try:
        return float(r.stdout.strip())
    except ValueError:
        return 0.0


def pacote_mais_novo(media: Path) -> Path | None:
    cand = []
    for m in (media / "pacotes").glob("*/manifest.json"):
        try:
            cand.append((json.loads(m.read_text(encoding="utf-8")).get("criado_em", ""), m.parent))
        except ValueError:
            pass
    return max(cand)[1] if cand else None


def main() -> int:
    media = Path(sys.argv[1])
    pkg = media / "pacotes" / sys.argv[2] if len(sys.argv) > 2 else pacote_mais_novo(media)
    if not pkg or not pkg.exists():
        print("auditor: nenhum pacote encontrado")
        return 0
    linhas, falhas = [], 0

    def item(ok: bool | None, texto: str) -> None:
        nonlocal falhas
        marca = "OK " if ok else ("AVISO" if ok is False else "INFO")
        if ok is False:
            falhas += 1
        linhas.append(f"- **{marca}** {texto}")

    rot = json.loads((pkg / "roteiro.json").read_text(encoding="utf-8"))
    cenas = rot.get("cenas", [])
    video = pkg / "video.mp4"

    # --- vídeo ---
    if video.exists():
        d = duracao(video)
        item(15 <= d <= 60, f"duração {d:.0f} s (padrão: 15 a 60 s)")
        l = lufs(video)
        item(l is not None and -17 <= l <= -12, f"volume geral {l} LUFS (padrão: -17 a -12; abaixo disso o vídeo soa fraco)")
    else:
        item(False, "video.mp4 ausente")

    # --- gancho ---
    gancho = re.sub(r"\[[^\]]*\]", "", rot.get("gancho_3s", "")).strip()
    primeira = re.sub(r"\[[^\]]*\]", "", cenas[0].get("narracao", "")).strip() if cenas else ""
    item(bool(gancho) and gancho.lower().rstrip("?.! ") in primeira.lower(), "gancho é FALADO na 1ª cena (não só texto na tela)")
    item(len(gancho.split()) <= 14, f"gancho com {len(gancho.split())} palavras (padrão: até ~12)")
    item(not re.search(r"em \d+ dias|poucos dias|garant|cura", gancho.lower()), "gancho sem promessa de resultado/prazo")

    # --- tela e voz ---
    item(not any("[" in (c.get("texto_na_tela") or "") for c in cenas), "nenhuma tag de emoção aparece na tela")
    todas = " ".join(c.get("narracao", "") for c in cenas) + " " + rot.get("chamada_final", "")
    tags = re.findall(r"\[([^\]]*)\]", todas)
    permitidas = {"warmly", "smiling", "excited", "thoughtful", "softly", "happy", "short pause"}
    item(all(t.strip().lower() in permitidas for t in tags), f"tags usadas: {sorted(set(tags)) or 'nenhuma'}")
    item("[laughs]" not in todas and tags.count("excited") <= 1, "sem risada e no máximo um [excited]")
    item(bool(tags), "narração tem tags de emoção (a Duda sorri pela tag)")

    # --- CTA ---
    cta = rot.get("chamada_final", "") or (cenas[-1].get("narracao", "") if cenas else "")
    item(bool(CTA_VERBOS.search(cta)), "CTA presente (seguir, comentar, compartilhar, salvar ou blog)")
    item("Duda" in cta, "CTA com a assinatura da Duda")

    # --- legenda ---
    leg = (pkg / "legenda.txt").read_text(encoding="utf-8") if (pkg / "legenda.txt").exists() else ""
    item("tutorialpet.com.br/" in leg, "legenda com o link do artigo")
    item("sozinhoemcasa" in leg or "kiwify" in leg, "legenda com o link do produto (landing)")

    # --- custo de voz ---
    chars = len(re.sub(r"\s+", " ", re.sub(r"\[[^\]]*\]", "", todas)).strip())
    item(None, f"créditos ElevenLabs estimados nesta rodada: ~{chars} (saldo do plano: ver painel)")

    cab = f"# Auditoria do processo — {datetime.now(timezone.utc):%Y-%m-%d %H:%M} UTC\n\nPacote: `{pkg.name}` — {falhas} aviso(s)\n\n"
    texto = cab + "\n".join(linhas) + "\n"
    SAIDA.mkdir(parents=True, exist_ok=True)
    (SAIDA / "ultimo.md").write_text(texto, encoding="utf-8")
    print(texto)
    return 0


if __name__ == "__main__":
    sys.exit(main())
