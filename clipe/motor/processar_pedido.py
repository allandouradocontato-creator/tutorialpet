#!/usr/bin/env python3
"""Worker do Clipe do Pet: pega pedidos na fila do site, anima cada foto, monta o clipe com o motor e devolve o MP4.

Roda no GitHub Actions (clipe_worker.yml) a cada ~5 min e também sob demanda (workflow_dispatch).
Variáveis: CLIPE_BASE (padrão https://tutorialpet.com.br), CLIPE_SEGREDO (= TICK_SECRET do Cloudflare),
           HF_TOKEN / FAL_KEY (provedores de animação), CLIPE_COMPLETA=1 (1080x1920 em vez da versão leve),
           CLIPE_MAX_PEDIDOS (padrão 3 por rodada).
Contrato com o site (functions/api/clipe/*):
  GET  /api/clipe/fila                       -> {pedidos:[{id, molde, nome, frase, fotos}]}
  GET  /api/clipe/foto?id=&n=                -> JPEG da foto n (1..fotos)
  POST /api/clipe/andamento?id=&estado=&etapa=&msg=  -> atualiza o acompanhamento (estado: processando | falhou)
  POST /api/clipe/video-upload?id=&animadas=&total=  -> corpo = MP4 final (estado vira "entregue")
"""
import json, os, subprocess, sys, tempfile, time, urllib.parse, urllib.request, urllib.error
from pathlib import Path

AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI))
from animar_foto import animar  # noqa: E402

BASE = os.environ.get("CLIPE_BASE", "https://tutorialpet.com.br").rstrip("/")
SEGREDO = os.environ.get("CLIPE_SEGREDO", "")
COMPLETA = os.environ.get("CLIPE_COMPLETA") == "1"
MAX_PEDIDOS = int(os.environ.get("CLIPE_MAX_PEDIDOS", "3"))


def log(*a):
    print("[worker]", *a, flush=True)


def http(metodo, caminho, dados=None, tipo=None, timeout=120):
    req = urllib.request.Request(BASE + caminho, data=dados, method=metodo,
                                 headers={"authorization": f"Bearer {SEGREDO}", **({"content-type": tipo} if tipo else {})})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read()


def andamento(pid, estado, etapa="", msg=""):
    q = urllib.parse.urlencode({"id": pid, "estado": estado, "etapa": etapa, "msg": msg})
    try:
        http("POST", f"/api/clipe/andamento?{q}", b"")
    except Exception as e:
        log("aviso: não consegui atualizar andamento:", e)


def processar(p):
    pid, n = p["id"], int(p["fotos"])
    log(f"pedido {pid}: molde={p['molde']} fotos={n}")
    with tempfile.TemporaryDirectory() as td:
        td = Path(td)
        fotos, midias = td / "fotos", td / "midias"
        fotos.mkdir(), midias.mkdir()
        andamento(pid, "processando", "Recebendo suas fotos", "Preparando tudo para a animação")
        for i in range(1, n + 1):
            (fotos / f"{i:02d}.jpg").write_bytes(http("GET", f"/api/clipe/foto?id={pid}&n={i}"))
        animadas = 0
        for i in range(1, n + 1):
            andamento(pid, "processando", f"Animando a foto {i} de {n}", "A inteligência artificial está dando vida à sua foto")
            f, saida = fotos / f"{i:02d}.jpg", midias / f"{i:02d}.mp4"
            if animar(str(f), str(saida)):
                animadas += 1
            else:
                log(f"foto {i}: sem animação, usando zoom lento")
                (midias / f"{i:02d}.jpg").write_bytes(f.read_bytes())
        andamento(pid, "processando", "Montando o seu clipe", "Legendas, música e carimbo")
        final = td / "clipe.mp4"
        cmd = [sys.executable, str(AQUI / "montar_clipe.py"), "--molde", p["molde"], "--midias", str(midias),
               "--nome", p.get("nome", ""), "--frase", p.get("frase", ""), "--saida", str(final)]
        if not COMPLETA:
            cmd.append("--leve")
        r = subprocess.run(cmd, capture_output=True, text=True)
        if r.returncode != 0 or not final.exists():
            raise RuntimeError("motor falhou: " + (r.stderr or r.stdout)[-300:])
        tam = final.stat().st_size
        if tam > 24 * 1024 * 1024:
            raise RuntimeError(f"clipe grande demais para entrega ({tam} bytes)")
        http("POST", f"/api/clipe/video-upload?id={pid}&animadas={animadas}&total={n}", final.read_bytes(), "video/mp4", timeout=180)
        log(f"pedido {pid}: entregue ({tam // 1024} KB, {animadas}/{n} animadas)")


def main():
    if not SEGREDO:
        log("CLIPE_SEGREDO ausente: worker desligado")
        return 0
    try:
        fila = json.loads(http("GET", "/api/clipe/fila")).get("pedidos", [])
    except Exception as e:
        log("fila indisponível:", e)
        return 0
    log(f"{len(fila)} pedido(s) na fila")
    for p in fila[:MAX_PEDIDOS]:
        try:
            processar(p)
        except Exception as e:
            log(f"pedido {p['id']} falhou: {e}")
            andamento(p["id"], "falhou", "", str(e)[:200])
    return 0


if __name__ == "__main__":
    sys.exit(main())
