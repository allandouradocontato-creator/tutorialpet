"""Do artigo ao vídeo: gera roteiro curto (vertical), cenas e legenda com link do produto NO COMEÇO.

Uso: python agents/03_content_writer/roteiro_video.py caminho/do/artigo.md
Saída: data/social/roteiros/<slug>.json
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from core.config import load_env_file  # noqa: E402
from core.llm import gerar_texto  # noqa: E402

SISTEMA = """Você cria roteiros de vídeo vertical (9:16) de 30 a 45 segundos para Reels do Instagram e Facebook, em pt-BR.
O vídeo deve ILUSTRAR exatamente o que o artigo ensina — nada fora do artigo.
Regras: sem inventar estudo ou estatística, sem credencial veterinária, orientar procurar veterinário em saúde.
Responda SOMENTE com JSON válido (sem crases) neste formato:
{"titulo_video": str, "gancho_3s": str,
 "cenas": [{"narracao": str, "visual_busca_banco_livre": str (termos em inglês para Pexels/Pixabay; SOMENTE o animal em cena, nunca pessoas, mãos, donos ou crianças: ex. "puppy chewing toy close up", "dog sleeping on floor"), "texto_na_tela": str}],
 "chamada_final": str, "hashtags": [str]}
Use de 5 a 7 cenas, narração total até 110 palavras."""


def ler_artigo(path: Path) -> tuple[dict, str]:
    texto = path.read_text(encoding="utf-8")
    m = re.match(r"^---\n(.*?)\n---\n(.*)$", texto, re.S)
    fm = yaml.safe_load(m.group(1)) if m else {}
    return fm, (m.group(2) if m else texto)


def produto_principal() -> dict:
    dados = yaml.safe_load((ROOT / "config" / "produtos_relacionados.yaml").read_text(encoding="utf-8")) or {}
    produtos = dados.get("produtos") if isinstance(dados, dict) else dados
    return (produtos or [{}])[0] if isinstance(produtos, list) else {}


def extrair_json(txt: str) -> dict:
    txt = re.sub(r"^```(?:json)?|```$", "", txt.strip(), flags=re.M).strip()
    return json.loads(txt[txt.find("{"): txt.rfind("}") + 1])


def gerar(path: Path) -> Path:
    load_env_file()
    fm, corpo = ler_artigo(path)
    slug = fm.get("slug") or path.stem
    roteiro = extrair_json(gerar_texto(f"ARTIGO:\n{corpo[:6000]}", sistema=SISTEMA, temperatura=0.7))
    prod = produto_principal()
    link_produto = prod.get("link", "")
    chamada = prod.get("chamada_topo", "Conheça o app Sozinho em Casa.")
    # Gancho segue o tema: artigo sobre gato (sem citar cachorro) não abre falando do cachorro do leitor.
    ref = f"{slug} {fm.get('title', '')} {fm.get('titulo', '')}".lower()
    if re.search(r"\b(gato|gata|gatos|felino)", ref) and not re.search(r"cachorr|c[aã]o\b|c[aã]es", ref):
        chamada = prod.get("chamada_topo_outros", chamada)
    url_artigo = f"https://tutorialpet.com.br/{slug}"
    # Regra da casa: link do produto logo no começo da legenda; artigo logo abaixo.
    legenda = f"🐾 {chamada} → {link_produto}\n\n{roteiro.get('gancho_3s', '')}\n\n📖 Artigo completo: {url_artigo}\n\n" + " ".join("#" + str(h).strip().lstrip("#").replace(" ", "") for h in roteiro.get("hashtags", []) if str(h).strip())
    roteiro["legenda"] = legenda.strip()
    roteiro["slug"] = slug
    out = ROOT / "data" / "social" / "roteiros" / f"{slug}.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(roteiro, ensure_ascii=False, indent=2), encoding="utf-8")
    return out


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit("uso: python roteiro_video.py caminho/do/artigo.md")
    print("roteiro salvo em", gerar(Path(sys.argv[1])))
