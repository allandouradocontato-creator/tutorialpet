"""Fábrica Tutorial Pet na nuvem (GitHub Actions): artigo -> roteiro -> vídeo -> pacote.

Roda sem o PC do Allan. Saída em <saida>/pacotes/<slug>/ : artigo.md, roteiro.json, video.mp4, legenda.txt, manifest.json
Nada é publicado aqui: o pacote fica 'aguardando_revisao' (portão de qualidade do Claude) e depois é agendado no Metricool.
Uso: python fabrica_nuvem.py <pasta_saida>
"""
from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent
RASC = ROOT / "data" / "content_writer" / "rascunhos"


def run(cmd: list[str], env_extra: dict | None = None, limite_s: int = 720) -> None:
    import os
    env = {**os.environ, "PYTHONIOENCODING": "utf-8", **(env_extra or {})}
    print("$", " ".join(cmd), flush=True)
    try:
        # Prazo por etapa: se travar (API fora, TTS parado), vira erro com log em vez de rodada pendurada.
        r = subprocess.run(cmd, cwd=ROOT, env=env, timeout=limite_s)
    except subprocess.TimeoutExpired:
        raise SystemExit(f"TRAVOU: passou de {limite_s}s sem terminar: {' '.join(cmd)}")
    if r.returncode != 0:
        raise SystemExit(f"falhou ({r.returncode}): {' '.join(cmd)}")


def garantir_links_legenda(texto: str, slug: str) -> str:
    """Garante, por código, o link do produto (landing com UTM) e o link do artigo na legenda.

    O gerador de texto às vezes esquece o link do produto; o teste de saúde reprovava a rodada (07/10/2026).
    O Publicador depois move esses links para o primeiro comentário.
    """
    import yaml
    link_produto = ""
    cfg = ROOT / "config" / "produtos_relacionados.yaml"
    if cfg.exists():
        dados = yaml.safe_load(cfg.read_text(encoding="utf-8")) or {}
        for p in dados.get("produtos", []):
            if str(p.get("link", "")).startswith("http"):
                link_produto = p["link"]
                break
    texto = texto.strip()
    if link_produto and link_produto not in texto:
        texto = ("🐾 Seu cachorro sofre quando fica sozinho? Conheça o app Sozinho em Casa — protocolo de 14 dias, "
                 f"de R$ 37 por apenas R$ 9,90. → {link_produto}\n\n{texto}")
    url_artigo = f"https://tutorialpet.com.br/{slug}"
    if url_artigo not in texto:
        texto += f"\n\n📖 Artigo completo: {url_artigo}"
    return texto + "\n"


def main() -> int:
    if len(sys.argv) < 2:
        sys.exit("uso: python fabrica_nuvem.py <pasta_saida>")
    saida = Path(sys.argv[1])
    pronto = ROOT / "config" / "fabrica_pronto.txt"  # modo teste: usa artigo+roteiro ja prontos, sem Gemini
    if pronto.exists() and pronto.read_text(encoding="utf-8").strip():
        slug = pronto.read_text(encoding="utf-8").strip()
        artigo = RASC / f"{slug}.md"
        print(f"MODO PRONTO: usando artigo e roteiro existentes de {slug}", flush=True)
        if not artigo.exists():
            raise SystemExit(f"artigo pronto nao encontrado: {artigo}")
    else:
        inicio = time.time() - 2
        run([sys.executable, "rotina_diaria.py"], {"WRITER_MODE": "llm"}, limite_s=1500)
        # artigo produzido nesta rodada = arquivo novo OU reescrito depois do início
        novos = [p for p in RASC.glob("*.md") if p.stat().st_mtime >= inicio]
        if not novos:
            print("nenhum artigo novo produzido")
            return 1
        artigo = max(novos, key=lambda p: p.stat().st_mtime)
        slug = artigo.stem
    roteiro = ROOT / "data" / "social" / "roteiros" / f"{slug}.json"
    if not roteiro.exists():
        raise SystemExit(f"roteiro não gerado: {roteiro}")
    # PORTÃO DA DUDA (20/10/2026): gancho universal -> conteúdo -> CTA com tags de emoção. Antes, se o padrão falhasse a
    # fábrica seguia com o roteiro original (sem emoção) e gastava créditos; 4 vídeos do TikTok saíram assim.
    # Agora: tenta aplicar até 2 vezes; se o roteiro continuar reprovado, a rodada PARA aqui (0 créditos, vira alerta).
    from core.portao_duda import validar_roteiro
    problemas: list[str] = []
    for tentativa in (1, 2):
        dados = json.loads(roteiro.read_text(encoding="utf-8"))
        if dados.get("molde_gancho"):  # já aplicado (reexecução): não insere o gancho duas vezes
            problemas = validar_roteiro(dados)
            break
        try:
            run([sys.executable, "agents/20_roteirista_duda/aplicar_padrao.py", slug], limite_s=300)
        except (Exception, SystemExit) as e:  # noqa: BLE001
            print(f"aviso: padrao da Duda nao aplicado na tentativa {tentativa} ({type(e).__name__})", flush=True)
        problemas = validar_roteiro(json.loads(roteiro.read_text(encoding="utf-8")))
        if not problemas:
            break
    if problemas and not os.environ.get("PERMITIR_ROTEIRO_SEM_PADRAO"):
        raise SystemExit("PORTÃO DA DUDA REPROVOU O ROTEIRO — não narrado, 0 créditos gastos, nada entregue:\n- "
                         + "\n- ".join(problemas))
    print("PORTÃO DA DUDA: roteiro aprovado", flush=True)
    # Preflight da voz (sem gastar crédito): chave, voz e saldo conferidos ANTES de narrar
    from core.portao_duda import preflight_voz
    falhas_voz = preflight_voz(json.loads(roteiro.read_text(encoding="utf-8")))
    if falhas_voz and not os.environ.get("PERMITIR_VOZ_GRATIS"):
        raise SystemExit("PREFLIGHT DA VOZ REPROVOU — não narrado, 0 créditos gastos:\n- " + "\n- ".join(falhas_voz))
    print("PREFLIGHT DA VOZ: chave, voz e saldo ok", flush=True)
    run([sys.executable, "agents/17_video/montar_video6.py", str(roteiro)])
    video = ROOT / "data" / "social" / "videos" / f"{slug}_v2.mp4"
    legenda = ROOT / "data" / "social" / "videos" / f"{slug}_v2.legenda.txt"
    if not video.exists():
        raise SystemExit("vídeo não gerado")
    pkg = saida / "pacotes" / slug
    pkg.mkdir(parents=True, exist_ok=True)
    shutil.copy(artigo, pkg / "artigo.md")
    shutil.copy(roteiro, pkg / "roteiro.json")
    shutil.copy(video, pkg / "video.mp4")
    (pkg / "legenda.txt").write_text(
        garantir_links_legenda(legenda.read_text(encoding="utf-8"), slug), encoding="utf-8")
    # Fotos candidatas para a capa do artigo no blog (a escolha, só animal, é do Publicador)
    try:
        run([sys.executable, "blog_imagens_nuvem.py", slug])
        cand = ROOT / "data" / "visual" / "candidatos" / slug
        if cand.exists():
            shutil.copytree(cand, pkg / "imagens_candidatas", dirs_exist_ok=True)
    except SystemExit as exc:
        print("AVISO: sem fotos candidatas:", exc, flush=True)
    voz_arq = ROOT / "data" / "social" / "videos" / f"{slug}_v2.voz.json"  # quem realmente narrou (montar_video6)
    voz = json.loads(voz_arq.read_text(encoding="utf-8")) if voz_arq.exists() else {"motor": "desconhecido"}
    (pkg / "manifest.json").write_text(json.dumps({
        "slug": slug, "status": "aguardando_revisao",
        "criado_em": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "artigo_url_futura": f"https://tutorialpet.com.br/{slug}",
        "voz": voz,
    }, ensure_ascii=False, indent=2), encoding="utf-8")
    print("PACOTE PRONTO:", pkg)
    return 0


if __name__ == "__main__":
    sys.exit(main())
