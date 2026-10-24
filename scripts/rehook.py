"""Troca o gancho de pacotes presos por abertura banida e remonta o video (voz Marianne).
Uso: python scripts/rehook.py /tmp/media   (le config/rehook.txt)
"""
from __future__ import annotations
import json, os, re, shutil, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
BANIDOS = re.compile(r"^\s*(\[[^\]]*\]\s*)?(esse erro|aquele momento|para de|pare de)", re.I)

def limpar_marca(t: str) -> str:
    t = re.sub(r"\bcãozinhos?\b", lambda m: "cachorrinho" + ("s" if m.group(0).endswith("s") else ""), t, flags=re.I)
    t = re.sub(r"\bcães\b", "cachorros", t, flags=re.I)
    t = re.sub(r"\bcão\b", "cachorro", t, flags=re.I)
    return t

def main() -> int:
    media = Path(sys.argv[1])
    from fabrica_nuvem import garantir_links_legenda
    from core.portao_duda import validar_roteiro
    linhas = [l for l in (ROOT / "config" / "rehook.txt").read_text(encoding="utf-8").splitlines() if l.strip() and not l.startswith("#")]
    falhas = []
    for l in linhas:
        slug, gancho, molde, tag = [x.strip() for x in l.split("|")]
        pkg = media / "pacotes" / slug
        if not pkg.exists():
            falhas.append(f"{slug}: pacote não existe"); continue
        if BANIDOS.match(gancho):
            falhas.append(f"{slug}: gancho novo é banido"); continue
        rot = json.loads((pkg / "roteiro.json").read_text(encoding="utf-8"))
        velho = rot["gancho_3s"]
        for c in rot["cenas"]:
            c["narracao"] = limpar_marca(c["narracao"])
        rot["cenas"][0]["narracao"] = f"[{tag}] {gancho}"
        rot["cenas"][0]["texto_na_tela"] = gancho
        rot["gancho_3s"] = gancho
        rot["molde_gancho"] = molde
        rot["chamada_final"] = limpar_marca(rot["chamada_final"])
        erros = validar_roteiro(rot)
        if erros:
            falhas.append(f"{slug}: roteiro reprovado: {erros}"); continue
        dest = ROOT / "data" / "social" / "roteiros"; dest.mkdir(parents=True, exist_ok=True)
        (dest / f"{slug}.json").write_text(json.dumps(rot, ensure_ascii=False, indent=2), encoding="utf-8")
        r = subprocess.run([sys.executable, "agents/17_video/montar_video6.py", str(dest / f"{slug}.json")], cwd=ROOT)
        video = ROOT / "data" / "social" / "videos" / f"{slug}_v2.mp4"
        if r.returncode != 0 or not video.exists():
            falhas.append(f"{slug}: montagem falhou ({r.returncode})"); continue
        shutil.copy(video, pkg / "video.mp4")
        (pkg / "roteiro.json").write_text(json.dumps(rot, ensure_ascii=False, indent=2), encoding="utf-8")
        legenda = limpar_marca(rot.get("legenda", "")).replace(velho, gancho)
        (pkg / "legenda.txt").write_text(garantir_links_legenda(legenda, slug), encoding="utf-8")
        voz = ROOT / "data" / "social" / "videos" / f"{slug}_v2.voz.json"
        m = json.loads((pkg / "manifest.json").read_text(encoding="utf-8"))
        m.update({"status": "aguardando_revisao", "rehook": {"gancho_antigo": velho, "gancho_novo": gancho}})
        m.pop("guardiao", None); m.pop("aprovado_por", None)
        if voz.exists():
            m["voz"] = json.loads(voz.read_text(encoding="utf-8"))
        (pkg / "manifest.json").write_text(json.dumps(m, ensure_ascii=False, indent=2), encoding="utf-8")
        print("REHOOK OK:", slug, "|", velho, "->", gancho, flush=True)
    if falhas:
        print("FALHAS:\n- " + "\n- ".join(falhas))
    return 1 if falhas and len(falhas) == len(linhas) else 0

if __name__ == "__main__":
    sys.exit(main())
