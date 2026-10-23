"""Baixa varios clipes verticais de cachorro feliz por cena (Pexels), sem repetir, para a montagem do V1.
Uso: PEXELS_API_KEY=... python3 scripts/clipes_pet.py out 4
Cada cena tem varias buscas (racas e acoes diferentes) para variar o cachorro. Saida: out/cenaN_k.mp4 + out/info.json
"""
import importlib.util, json, os, sys
from pathlib import Path

CENAS = {
    1: ["happy golden retriever running", "cute puppy playing", "labrador smiling happy", "corgi happy running"],
    2: ["dog yawning", "happy dog panting close up", "dog smiling at camera", "cute dog tongue out"],
    3: ["owner petting happy dog", "woman hugging dog", "dog wagging tail happy", "girl playing with puppy"],
    4: ["small dog yorkshire happy", "poodle white fluffy happy", "pomeranian cute", "shih tzu playing"],
    5: ["dog licking lips", "happy dog eating treat", "puppy chewing toy cute", "dog chewing toy"],
    6: ["family with dog park happy", "dog running in field happy", "dog and owner walking", "puppy cuddling owner"],
}

def main():
    out = Path(sys.argv[1]); out.mkdir(parents=True, exist_ok=True)
    por_busca = int(sys.argv[2]) if len(sys.argv) > 2 else 2
    spec = importlib.util.spec_from_file_location("mv6", "agents/17_video/montar_video6.py")
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    chave = os.environ["PEXELS_API_KEY"]
    info = []
    for cena, buscas in CENAS.items():
        for j, b in enumerate(buscas):
            try:
                arqs = m._pexels_videos(b, chave, por_busca, out, f"cena{cena}_{j}")
            except Exception as exc:  # noqa: BLE001
                print("erro", b, exc); arqs = []
            for a in arqs:
                info.append({"cena": cena, "busca": b, "arq": a.name})
    json.dump(info, open(out / "info.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(len(info), "clipes")

main()
