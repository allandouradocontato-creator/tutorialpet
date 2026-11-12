#!/usr/bin/env python3
"""Comparativo de provedores (pedido fixo de referência: Thor e Mel).
Roda cada adaptador pelo endpoint protegido /api/musica/teste-provedor (as chaves ficam só no Cloudflare),
baixa o arquivo, converte para MP3 se preciso (ffmpeg) e salva como data_pet_provedor_estilo.mp3.
Uso: MUSICA_TICK_SECRET=... python3 comparativo.py <pasta_saida> [base_url] [provedores,separados,por,virgula]"""
import json, os, subprocess, sys, time, urllib.request
from datetime import date

saida = sys.argv[1]
base = (sys.argv[2] if len(sys.argv) > 2 else "https://tutorialpet.com.br").rstrip("/")
provs = (sys.argv[3] if len(sys.argv) > 3 else "fal,mureka,elevenlabs").split(",")
seg = os.environ["MUSICA_TICK_SECRET"]
os.makedirs(saida, exist_ok=True)
REF = {
    "thor": dict(nomePet="Thor", especie="cachorro", raca="", manias=["rouba meias e sai correndo", "late para o carteiro", "dorme de barriga para cima"],
                 tutor="Allan", estilo="pop alegre", voz="masculina", clima="animada", idioma="pt-BR", duracaoAlvo=150),
    "mel": dict(nomePet="Mel", especie="cachorro", raca="", manias=["pula, pula, pula quando vê a coleira", "persegue a própria sombra", "ama um colo"],
                tutor="", estilo="pop alegre", voz="feminina", clima="animada", idioma="pt-BR", duracaoAlvo=150),
}
H = {"authorization": f"Bearer {seg}", "content-type": "application/json"}
resumo = []
for prov in provs:
    for pet, pedido in REF.items():
        nome = f"{date.today():%Y-%m-%d}_{pet}_{prov}_{pedido['estilo'].replace(' ', '-')}"
        chave = nome.replace("-", "_").lower()
        req = urllib.request.Request(f"{base}/api/musica/teste-provedor", data=json.dumps({"provedor": prov, "pedido": pedido, "nome": chave}).encode(), headers=H, method="POST")
        try:
            r = json.loads(urllib.request.urlopen(req, timeout=420).read())
        except Exception as e:
            corpo = getattr(e, "read", lambda: b"")().decode("utf-8", "ignore")[:300]
            print(f"[{prov}/{pet}] FALHOU: {e} {corpo}"); resumo.append((prov, pet, "falhou", corpo)); continue
        get = urllib.request.Request(f"{base}/api/musica/teste-provedor?nome={chave}", headers=H)
        dados = urllib.request.urlopen(get, timeout=120).read()
        tmp = os.path.join(saida, f"_tmp_{chave}.bin"); open(tmp, "wb").write(dados)
        destino = os.path.join(saida, nome + ".mp3")
        if "mpeg" in r["tipo"] or "mp3" in r["tipo"]:
            os.replace(tmp, destino)
        else:
            subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", tmp, "-codec:a", "libmp3lame", "-b:a", "192k", destino], check=True); os.remove(tmp)
        open(os.path.join(saida, nome + ".letra.txt"), "w", encoding="utf-8").write(f"{r.get('titulo','')}\n\n{r.get('letra','')}")
        print(f"[{prov}/{pet}] ok {r['segundos']}s -> {destino}"); resumo.append((prov, pet, "ok", f"{r['segundos']}s"))
print("\nRESUMO"); [print(" ", *x) for x in resumo]
