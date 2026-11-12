#!/usr/bin/env python3
"""Anima UMA foto (pessoa + pet) e devolve um MP4 curto, trocando de provedor sozinho.

Cadeia (a primeira que responder vence):
  1. hf   — Wan 2.2 14B no Hugging Face (ZeroGPU), GRÁTIS com HF_TOKEN da conta (cota diária por conta).
  2. fal  — Wan 2.2 no fal.ai, PAGO por clipe (~US$0,40/5 s), só se existir FAL_KEY. Licença comercial.
  (se nenhum animar, sai com código 3 e o orquestrador usa a foto parada com zoom lento, avisando no log.)

Uso: python3 animar_foto.py foto.jpg saida.mp4 [--prompt "..."] [--segundos 3.5] [--provedores hf,fal]
Variáveis: HF_TOKEN, FAL_KEY, CLIPE_HF_SPACE (padrão linoyts/wan2-2-i2v-rCM).
Códigos de saída: 0 ok | 3 nenhum provedor animou.
"""
import argparse, base64, json, os, shutil, sys, time, urllib.request, urllib.error

PROMPT_PADRAO = ("The people and the pet move naturally and affectionately: they smile, breathe, look at each other, "
                 "the pet wags and tilts its head, gentle camera motion, natural subtle motion, "
                 "same faces and same subjects throughout, realistic, no text")


def log(*a):
    print("[animar]", *a, file=sys.stderr, flush=True)


def via_hf(foto, saida, prompt, segundos):
    from gradio_client import Client, handle_file
    token = os.environ.get("HF_TOKEN")
    if not token:
        raise RuntimeError("HF_TOKEN ausente")
    c = Client(os.environ.get("CLIPE_HF_SPACE", "linoyts/wan2-2-i2v-rCM"), token=token)
    job = c.submit(input_image=handle_file(str(foto)), prompt=prompt, steps=6, duration_seconds=float(segundos),
                   randomize_seed=True, api_name="/generate_video")
    out = job.result(timeout=300)  # não deixa o worker travar se a GPU grátis ficar presa na fila
    shutil.copy(out[0], saida)


def _post(url, corpo, chave):
    req = urllib.request.Request(url, data=json.dumps(corpo).encode(), method="POST",
                                 headers={"authorization": f"Key {chave}", "content-type": "application/json"})
    return json.load(urllib.request.urlopen(req, timeout=60))


def via_fal(foto, saida, prompt, segundos):
    chave = os.environ.get("FAL_KEY")
    if not chave:
        raise RuntimeError("FAL_KEY ausente")
    b64 = base64.b64encode(open(foto, "rb").read()).decode()
    modelo = "fal-ai/wan/v2.2-a14b/image-to-video"
    r = _post(f"https://queue.fal.run/{modelo}", {"image_url": f"data:image/jpeg;base64,{b64}", "prompt": prompt,
                                                  "resolution": "480p", "num_frames": 81, "frames_per_second": 16}, chave)
    status, resp = r["status_url"], r["response_url"]
    fim = time.time() + 420
    while time.time() < fim:
        time.sleep(6)
        rq = urllib.request.Request(status, headers={"authorization": f"Key {chave}"})
        s = json.load(urllib.request.urlopen(rq, timeout=60))
        if s.get("status") == "COMPLETED":
            rq = urllib.request.Request(resp, headers={"authorization": f"Key {chave}"})
            url = json.load(urllib.request.urlopen(rq, timeout=60))["video"]["url"]
            urllib.request.urlretrieve(url, saida)
            return
        if s.get("status") in ("FAILED", "ERROR"):
            raise RuntimeError(f"fal falhou: {s}")
    raise RuntimeError("fal: tempo esgotado")


PROVEDORES = {"hf": via_hf, "fal": via_fal}


def animar(foto, saida, prompt=PROMPT_PADRAO, segundos=3.5, provedores=("hf", "fal"), tentativas_hf=2):
    """Retorna o nome do provedor que animou, ou None."""
    for nome in provedores:
        n = tentativas_hf if nome == "hf" else 1
        for t in range(1, n + 1):
            try:
                log(f"{nome}: tentativa {t}/{n}")
                PROVEDORES[nome](foto, saida, prompt, segundos)
                if os.path.exists(saida) and os.path.getsize(saida) > 20000:
                    log(f"{nome}: ok")
                    return nome
                raise RuntimeError("arquivo vazio")
            except Exception as e:  # cota, GPU indisponível, chave ausente etc.
                msg = str(e)[:300].replace("\n", " ")
                log(f"{nome}: falhou ({type(e).__name__}: {msg})")
                if "ausente" in msg:
                    break
                if t < n:
                    time.sleep(20)
    return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("foto")
    ap.add_argument("saida")
    ap.add_argument("--prompt", default=PROMPT_PADRAO)
    ap.add_argument("--segundos", type=float, default=3.5)
    ap.add_argument("--provedores", default="hf,fal")
    a = ap.parse_args()
    p = animar(a.foto, a.saida, a.prompt, a.segundos, tuple(x for x in a.provedores.split(",") if x in PROVEDORES))
    print(p or "")
    sys.exit(0 if p else 3)


if __name__ == "__main__":
    main()
