"""Aplica o padrão do Tutorial Pet ao roteiro do dia: GANCHO universal -> CONTEÚDO -> CTA, na voz da Duda.

Reescreve data/social/roteiros/<slug>.json IN-PLACE (guarda a cópia original em <slug>.original.json):
- gancho_3s: molde de config/ganchos_universais.yaml (alterna, nunca repete o do dia anterior), até ~12 palavras;
- cenas[].narracao: mesmo conteúdo factual, com tags de emoção da Duda (config/duda.yaml, registros_de_voz);
- chamada_final: CTA curto (config/ganchos_universais.yaml) + assinatura da Duda.
Se qualquer passo falhar ou a validação reprovar, NÃO mexe no roteiro (a fábrica segue com o original).
Uso: python agents/20_roteirista_duda/aplicar_padrao.py <slug>
"""
from __future__ import annotations

import json
import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(Path(__file__).resolve().parent))

import yaml  # noqa: E402
from agent import BLOQUEIO_TOM, norm  # noqa: E402

SAUDE = re.compile(r"veterin|vacina|doen|sintoma|remédio|remedio|engasg|vômit|vomit|diarre|intoxic", re.I)


def escolher_molde(g: dict, slug: str) -> dict:
    estado = ROOT / "data" / "social" / "duda" / "_ultimo_gancho.txt"
    # só moldes validados que NÃO prometem resultado/prazo (evita alegação de saúde inventada); ordem = mais fortes primeiro
    seguros = ["abertura_idade", "abertura_erro", "abertura_pensar", "abertura_lista_ninguem_conta", "abertura_pare",
               "abertura_dor", "abertura_situacao", "abertura_chamada_direta", "abertura_pov"]
    existentes = {m["id"] for m in g["moldes"]}
    ids = [i for i in seguros if i in existentes]
    ultimo = estado.read_text(encoding="utf-8").strip() if estado.exists() else ""
    prox = ids[(ids.index(ultimo) + 1) % len(ids)] if ultimo in ids else ids[0]
    estado.parent.mkdir(parents=True, exist_ok=True)
    estado.write_text(prox, encoding="utf-8")
    return next(m for m in g["moldes"] if m["id"] == prox)


def escolher_cta(g: dict) -> str:
    estado = ROOT / "data" / "social" / "duda" / "_ultimo_cta.txt"
    ctas = g["cta_moldes"]
    try:
        i = (int(estado.read_text(encoding="utf-8").strip()) + 1) % len(ctas)
    except (OSError, ValueError):
        i = 0
    estado.parent.mkdir(parents=True, exist_ok=True)
    estado.write_text(str(i), encoding="utf-8")
    return ctas[i]


def validar(r: dict, d: dict, g: dict) -> list[str]:
    erros = []
    permitidas = set(d["tags_elevenlabs_permitidas"])
    textos = [r.get("gancho_3s", ""), r.get("chamada_final", ""), *[c.get("narracao", "") for c in r.get("cenas", [])]]
    if not r.get("cenas"):
        erros.append("sem cenas")
    for t in textos:
        for tag in re.findall(r"\[([^\]]*)\]", t):
            if tag.strip().lower() not in permitidas:
                erros.append(f"tag não permitida: [{tag}]")
        for pad in BLOQUEIO_TOM:
            if re.search(pad, norm(t)):
                erros.append(f"alegação/tom proibido ({pad})")
    if len(re.sub(r"\[[^\]]*\]", "", r.get("gancho_3s", "")).split()) > 14:
        erros.append("gancho com mais de 14 palavras")
    if sum(t.count("[excited]") for t in textos) > 1:
        erros.append("mais de um [excited]")
    if re.search(r"\[[^\]]*\]", r.get("gancho_3s", "")) and "[excited]" in r.get("gancho_3s", ""):
        erros.append("gancho sem [excited]")
    if re.search(r"em \d+ dias|em poucos dias|resultado garantido|cura|garant", norm(r.get("gancho_3s", ""))):
        erros.append("gancho promete resultado/prazo")
    if "[laughs]" in " ".join(textos):
        erros.append("risada proibida")
    return erros


def main() -> int:
    slug = sys.argv[1]
    rot = ROOT / "data" / "social" / "roteiros" / f"{slug}.json"
    r = json.loads(rot.read_text(encoding="utf-8"))
    d = yaml.safe_load((ROOT / "config" / "duda.yaml").read_text(encoding="utf-8"))
    g = yaml.safe_load((ROOT / "config" / "ganchos_universais.yaml").read_text(encoding="utf-8"))
    molde = escolher_molde(g, slug)
    cta = escolher_cta(g)
    saude = bool(SAUDE.search(json.dumps(r, ensure_ascii=False)))
    registro = d["registros_de_voz"]["serio" if saude else "alegre"]
    from core.llm import gerar_texto

    base = {"titulo": r.get("titulo_video"), "gancho_original": r.get("gancho_3s"),
            "cenas": [{"narracao": c.get("narracao")} for c in r["cenas"]], "chamada_original": r.get("chamada_final")}
    falha = ""
    for _ in range(3):
        prompt = (
            "Você adapta o roteiro de um vídeo curto do Tutorial Pet para a voz da Duda (jovem brasileira, simpática, natural).\n"
            f"ESTRUTURA FIXA: GANCHO -> CONTEÚDO -> CTA. O gancho serve só para reter; o assunto (pet) entra no conteúdo.\n"
            f"GANCHO: use este molde, preenchendo com o assunto do vídeo, até 12 palavras faladas: \"{molde['molde']}\"\n"
            f"CONTEÚDO: mantenha EXATAMENTE os mesmos fatos e a mesma ordem das cenas ({len(r['cenas'])} cenas); só deixe a fala natural e curta. "
            "Não invente fatos, números, estudos nem alegue ser veterinária.\n"
            f"CTA (chamada para ação, obrigatória, sempre no fim): use ESTA, com as suas palavras mas o mesmo pedido: \"{cta}\"; depois a assinatura \"{d['assinatura']}\". Dita com sorriso, [smiling] ou [warmly].\n"
            f"TAGS de emoção (ElevenLabs): só entre {d['tags_elevenlabs_permitidas']}. Registro: {registro}. "
            "No máximo UM [excited] no vídeo inteiro, e NUNCA no gancho (só perto do fim); o gancho NÃO promete resultado, prazo nem cura de saúde; sem risadas; sem tom triste ou dramático. Use as tags com economia (1 por trecho).\n"
            + (f"A versão anterior foi recusada: {falha}. Corrija.\n" if falha else "")
            + f"\nROTEIRO:\n{json.dumps(base, ensure_ascii=False)}\n\n"
            'Responda SÓ com JSON: {"gancho_3s": "...", "cenas": ["narração da cena 1", ...], "chamada_final": "..."}')
        try:
            bruto = gerar_texto(prompt, sistema="Você escreve falas curtas, calorosas e honestas em pt-BR. Responde só JSON.",
                                temperatura=0.7, max_tokens=1500)
            novo = json.loads(re.search(r"\{.*\}", bruto, re.S).group(0))
            if len(novo["cenas"]) != len(r["cenas"]):
                raise ValueError("número de cenas diferente")
            cand = json.loads(json.dumps(r))
            cand["gancho_3s"] = novo["gancho_3s"].strip()
            cand["chamada_final"] = novo["chamada_final"].strip()
            for c, n in zip(cand["cenas"], novo["cenas"]):
                c["narracao"] = str(n).strip()
        except Exception as e:  # noqa: BLE001
            falha = f"{type(e).__name__}: {e}"
            continue
        erros = validar(cand, d, g)
        if not erros:
            shutil.copy(rot, rot.with_suffix(".original.json"))
            rot.write_text(json.dumps(cand, ensure_ascii=False, indent=2), encoding="utf-8")
            print(f"PADRÃO APLICADO ({molde['id']}, registro {'sério' if saude else 'alegre'}): {cand['gancho_3s']}")
            return 0
        falha = "; ".join(erros)
    print(f"padrão NÃO aplicado (roteiro original mantido): {falha}")
    return 1


if __name__ == "__main__":
    sys.exit(main())
