"""Agente 27 — Gerador de lote de roteiros (escala).

Gera de uma vez N roteiros de vídeo (padrão 30 = um mês de conteúdo a 1/dia, ou 15 dias a 2/dia), prontos para
o Allan avaliar no Painel de Decisões e para a fábrica renderizar e agendar nos horários de pico. Cada roteiro já sai:
  - com um molde de gancho diferente dos vizinhos (rodízio de config/ganchos_universais.yaml, só moldes seguros);
  - com um CTA diferente dos vizinhos (cta_moldes);
  - na voz da Duda (config/duda.yaml: tags permitidas, tom proibido, registro sério para saúde);
  - com buscas de imagem distintas (cena do gancho própria, sem repetir busca no vídeo);
  - validado pelas mesmas regras do padrão diário (agents/20_roteirista_duda/aplicar_padrao.py: validar()).
Nada é publicado, agendado, renderizado nem comprado aqui: só texto. Um LLM grátis (Gemini) escreve; o Guardião
confere a variedade do lote inteiro e o Claude/Allan só avaliam.

Temas: fila config/fila_temas.yaml (pendentes e rascunho_pronto, na ordem); se faltar, pede reposição ao agente 19.
Saída: <pasta>/lote/AAAA-MM/NN-<slug>.json + indice.md (tabela e relatório de variedade).

Uso: python agents/27_lote_roteiros/gerar_lote.py <pasta_saida> [--n 30] [--mes AAAA-MM] [--simulado]
  --simulado: não chama o LLM (roteiros de teste) para validar o encanamento e a variedade.
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import re
import subprocess
import sys
import time
import unicodedata
from collections import Counter
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import yaml  # noqa: E402

PALAVRAS_MIN, PALAVRAS_MAX_CARACTERES = 120, 480   # ~30 s. Os vídeos de hoje têm 444-646 caracteres (30-50 s); as referências de maior share têm 8-25 s


def _padrao():
    """Reaproveita validar() e a lista de moldes seguros do padrão diário (uma só fonte de regras)."""
    p = ROOT / "agents" / "20_roteirista_duda" / "aplicar_padrao.py"
    spec = importlib.util.spec_from_file_location("aplicar_padrao", p)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def slugify(txt: str) -> str:
    s = unicodedata.normalize("NFD", txt.lower())
    s = "".join(c for c in s if unicodedata.category(c) != "Mn")
    return re.sub(r"-+", "-", re.sub(r"[^a-z0-9]+", "-", s)).strip("-")


def carregar_temas(n: int) -> list[dict]:
    fila = ROOT / "config" / "fila_temas.yaml"
    dados = yaml.safe_load(fila.read_text(encoding="utf-8")) or {}
    temas = [t for t in dados.get("temas", []) if t.get("status") in ("pendente", "rascunho_pronto")]
    if len(temas) < n:
        faltam = n - len(temas)
        print(f"fila com {len(temas)} temas; pedindo {faltam} ao agente 19 (reposição)", flush=True)
        r = subprocess.run([sys.executable, "agents/19_validador_tema/agent.py", "--repor", str(faltam)], cwd=ROOT)
        if r.returncode == 0:
            dados = yaml.safe_load(fila.read_text(encoding="utf-8")) or {}
            temas = [t for t in dados.get("temas", []) if t.get("status") in ("pendente", "rascunho_pronto")]
    return temas[:n]


def distribuir(n: int, moldes: list[str], ctas: list[str]) -> list[tuple[str, int]]:
    """Molde e CTA por vídeo: rodízio contínuo, então vizinhos nunca repetem (e cada molde aparece quase o mesmo nº de vezes)."""
    return [(moldes[i % len(moldes)], i % len(ctas)) for i in range(n)]


def animal_do_tema(tema: str) -> str:
    return "kitten" if re.search(r"\b(gat[oa]s?|gatinh[oa]s?)\b", tema.lower()) else "puppy"


def prompt_roteiro(tema: str, molde: dict, cta: str, d: dict, saude: bool) -> str:
    registro = d["registros_de_voz"]["serio" if saude else "alegre"]
    return (
        "Você escreve um roteiro de vídeo curto (25 a 35 s) do Tutorial Pet, narrado pela Duda (jovem brasileira, simpática, natural).\n"
        f"TEMA: {tema}\n"
        "ESTRUTURA FIXA: GANCHO -> CONTEÚDO -> CTA. O gancho só retém; o assunto (pet) entra no conteúdo.\n"
        f"GANCHO: use este molde, preenchido com o assunto, até 12 palavras faladas: \"{molde['molde']}\"\n"
        "CONTEÚDO: 4 cenas com fatos corretos, simples e conhecidos de cuidado com pets; fala natural e curta (uma ideia por cena). TOTAL de fala (gancho + cenas + CTA) de no máximo 420 caracteres, sem as tags. "
        "Não invente números, estudos nem diga que é veterinária. Se tocar em saúde, diga para consultar o médico-veterinário.\n"
        f"CTA (sempre no fim, com as suas palavras mas o mesmo pedido): \"{cta}\"; depois a assinatura \"{d['assinatura']}\".\n"
        f"TAGS de emoção (ElevenLabs): só entre {d['tags_elevenlabs_permitidas']}. Registro: {registro}. No máximo UM [excited] no vídeo, "
        "nunca no gancho; o gancho NÃO promete resultado, prazo nem cura; sem risadas; sem tom triste ou dramático.\n"
        "IMAGENS: para cada cena, 'visual_busca_banco_livre' em inglês, 4 a 7 palavras, DIFERENTE em todas as cenas, mostrando só o animal "
        "(sem pessoas, mãos ou pernas), fofo e saudável (nada de animal doente, abrigo ou doação). "
        "Inclua também 'visual_gancho': uma busca em inglês, diferente das das cenas, com um close fofo e curioso do animal ligado ao tema.\n"
        'Responda SÓ com JSON: {"titulo_video": "...", "gancho_3s": "...", "visual_gancho": "...", "cenas": [{"narracao": "...", "visual_busca_banco_livre": "...", '
        '"texto_na_tela": "até 4 palavras"}], "chamada_final": "...", "hashtags": ["#..."]}'
    )


def roteiro_simulado(tema: str, molde: dict, cta: str, d: dict, i: int) -> dict:
    a = animal_do_tema(tema)
    return {"titulo_video": tema.capitalize(), "gancho_3s": "Com quantos anos você descobriu isso?", "visual_gancho": f"cute {a} hook {i}",
            "cenas": [{"narracao": f"Dica simples e curta número {k} para o seu pet.",
                       "visual_busca_banco_livre": f"cute {a} scene {i}-{k}", "texto_na_tela": f"Dica {k}"} for k in range(1, 5)],
            "chamada_final": f"{cta} {d['assinatura']}", "hashtags": ["#tutorialpet", "#pets"]}


def montar(tema: str, bruto: dict, molde: dict, cta_idx: int, ordem: int, saude: bool) -> dict:
    """Formato final igual ao do padrão diário: cena 0 = gancho falado, com busca de imagem própria."""
    cenas = [dict(c) for c in bruto["cenas"]]
    gancho_tela = re.sub(r"\s+", " ", re.sub(r"\[[^\]]*\]", "", bruto["gancho_3s"])).strip()
    cenas.insert(0, {"narracao": bruto["gancho_3s"].strip(), "visual_busca_banco_livre": str(bruto.get("visual_gancho") or f"cute {animal_do_tema(tema)} looking at camera").strip(),
                     "texto_na_tela": gancho_tela})
    slug = slugify(tema)
    tags = " ".join(bruto.get("hashtags", [])[:6])
    return {"slug": slug, "titulo_video": bruto.get("titulo_video", tema), "gancho_3s": gancho_tela, "cenas": cenas,
            "chamada_final": bruto["chamada_final"].strip(), "hashtags": bruto.get("hashtags", []),
            "legenda": f"{gancho_tela}\n\n{tags}".strip(), "molde_gancho": molde["id"], "cta_indice": cta_idx,
            "registro_voz": "sério" if saude else "alegre", "ordem_no_lote": ordem, "tema": tema}


def validar_lote(roteiros: list[dict]) -> list[str]:
    """Variedade entre os vídeos do lote (o que o Guardião confere um a um, aqui conferido no conjunto)."""
    avisos = []
    for a, b in zip(roteiros, roteiros[1:]):
        if a["molde_gancho"] == b["molde_gancho"]:
            avisos.append(f"moldes iguais seguidos: {a['slug']} e {b['slug']}")
        if a["cta_indice"] == b["cta_indice"]:
            avisos.append(f"CTA igual em vídeos seguidos: {a['slug']} e {b['slug']}")
    inicios = Counter(" ".join(re.sub(r"\W+", " ", r["gancho_3s"].lower()).split()[:4]) for r in roteiros)
    avisos += [f"{n} ganchos começam com '{k}'" for k, n in inicios.items() if n > 4]
    buscas = Counter(c["visual_busca_banco_livre"].strip().lower() for r in roteiros for c in r["cenas"])
    avisos += [f"busca de imagem repetida {n}x no lote: '{k}' (clipes diferentes, mas o visual tende a se parecer)"
               for k, n in buscas.items() if n > 3]
    return avisos


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("saida")
    ap.add_argument("--n", type=int, default=30)
    ap.add_argument("--mes", default=datetime.now().strftime("%Y-%m"))
    ap.add_argument("--simulado", action="store_true")
    a = ap.parse_args()

    padrao = _padrao()
    d = yaml.safe_load((ROOT / "config" / "duda.yaml").read_text(encoding="utf-8"))
    g = yaml.safe_load((ROOT / "config" / "ganchos_universais.yaml").read_text(encoding="utf-8"))
    por_id = {m["id"]: m for m in g["moldes"]}
    moldes = [i for i in padrao.MOLDES_SEGUROS if i in por_id]
    ctas = g["cta_moldes"]
    temas = carregar_temas(a.n)
    if not temas:
        print("sem temas: nada a gerar")
        return 1
    plano = distribuir(len(temas), moldes, ctas)
    pasta = Path(a.saida) / "lote" / a.mes
    pasta.mkdir(parents=True, exist_ok=True)

    from core.llm import gerar_texto
    roteiros, falhas = [], []
    for i, (t, (molde_id, cta_idx)) in enumerate(zip(temas, plano), 1):
        tema = t["termo"]
        molde, cta = por_id[molde_id], ctas[cta_idx]
        saude = bool(padrao.SAUDE.search(tema))
        erro, r, erros = "", None, []
        for tentativa in range(3):
            try:
                if a.simulado:
                    bruto = roteiro_simulado(tema, molde, cta, d, i)
                else:
                    txt = gerar_texto(prompt_roteiro(tema, molde, cta, d, saude) + (f"\nA versão anterior foi recusada: {erro}. Corrija.\n" if erro else ""),
                                      sistema="Você escreve falas curtas, calorosas e honestas em pt-BR. Responde só JSON.",
                                      temperatura=0.8, max_tokens=1800)
                    bruto = json.loads(re.search(r"\{.*\}", txt, re.S).group(0))
                r = montar(tema, bruto, molde, cta_idx, i, saude)
                erros = padrao.validar(r, d, g)
                chars = sum(len(re.sub(r"\[[^\]]*\]", "", c["narracao"])) for c in r["cenas"]) + len(r["chamada_final"])
                if chars > PALAVRAS_MAX_CARACTERES:
                    erros.append(f"fala longa demais ({chars} caracteres; máximo {PALAVRAS_MAX_CARACTERES})")
                if chars < PALAVRAS_MIN:
                    erros.append("fala curta demais")
                buscas = [c["visual_busca_banco_livre"].strip().lower() for c in r["cenas"]]
                if len(set(buscas)) != len(buscas):
                    erros.append("busca de imagem repetida dentro do vídeo")
                if not erros:
                    break
                erro = "; ".join(erros)
            except Exception as e:  # noqa: BLE001
                erro = f"{type(e).__name__}: {e}"
            r = None
        if r and not erros:
            (pasta / f"{i:02d}-{r['slug']}.json").write_text(json.dumps(r, ensure_ascii=False, indent=2), encoding="utf-8")
            roteiros.append(r)
            print(f"[{i}/{len(temas)}] ok  {molde_id:30s} {r['gancho_3s']}", flush=True)
        else:
            falhas.append((tema, erro))
            print(f"[{i}/{len(temas)}] FALHOU {tema}: {erro}", flush=True)
        if not a.simulado:
            time.sleep(2)  # respeita a cota grátis do Gemini

    avisos = validar_lote(roteiros)
    linhas = [f"# Lote de roteiros {a.mes} — {len(roteiros)} prontos, {len(falhas)} com falha", "",
              "| # | Tema | Gancho (molde) | CTA | Registro |", "|---|---|---|---|---|"]
    linhas += [f"| {r['ordem_no_lote']} | {r['tema']} | {r['gancho_3s']} ({r['molde_gancho']}) | #{r['cta_indice'] + 1} | {r['registro_voz']} |" for r in roteiros]
    linhas += ["", "## Variedade do lote", f"- moldes usados: {dict(Counter(r['molde_gancho'] for r in roteiros))}"]
    linhas += [f"- ATENÇÃO: {x}" for x in avisos] or ["- sem problemas de variedade"]
    if falhas:
        linhas += ["", "## Falhas (precisam de nova tentativa)"] + [f"- {t}: {e}" for t, e in falhas]
    (pasta / "indice.md").write_text("\n".join(linhas) + "\n", encoding="utf-8")
    print("\n".join(linhas[-6:]))
    return 0 if roteiros else 1


if __name__ == "__main__":
    sys.exit(main())
