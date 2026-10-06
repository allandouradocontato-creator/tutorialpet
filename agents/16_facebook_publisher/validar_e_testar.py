"""Comando único de pré-voo, pra rodar uma vez depois de colar o token no .env:
STOP → credenciais → token é de Página, bate com FACEBOOK_PAGE_ID, validade → nome da
Página confirmado → dry-run do post 1 (texto, link, imagem, crosspromo) → relatório.

Só faz chamadas de leitura na Graph API (debug_token, GET da página) e nunca publica —
o dry-run do post 1 não toca a fila real nem a Graph API de escrita. Token nunca é
impresso, nunca é logado.

Uso:
    python validar_e_testar.py --config <config.yaml>
"""
from __future__ import annotations

import argparse
import json
import sys
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

AGENT_DIR = Path(__file__).resolve().parent
ROOT = AGENT_DIR.parents[1]
for p in (ROOT, AGENT_DIR):
    if str(p) not in sys.path:
        sys.path.insert(0, str(p))

from core.config import load_env_file  # noqa: E402
from agent import (  # noqa: E402
    GRAPH_BASE, check_credenciais, confirmar_nome_pagina, get_marketing_logger,
    load_config, load_fila, processar_item, stop_ativo,
)


def debug_token(token: str) -> dict:
    url = f"{GRAPH_BASE}/debug_token?{urllib.parse.urlencode({'input_token': token, 'access_token': token})}"
    with urllib.request.urlopen(url, timeout=30) as resp:
        return json.loads(resp.read().decode("utf-8"))["data"]


def main() -> int:
    parser = argparse.ArgumentParser(description="Validação de pré-voo + dry-run do post 1, sem publicar nada")
    parser.add_argument("--config", required=True)
    args = parser.parse_args()

    load_env_file()
    log = get_marketing_logger()

    if stop_ativo():
        print(json.dumps({"status": "parado_stop"}, ensure_ascii=False))
        return 0

    ok, motivo, token, page_id = check_credenciais()
    if not ok:
        print(json.dumps({"status": "aguardando_credenciais", "motivo": motivo}, ensure_ascii=False))
        return 0

    info = debug_token(token)
    tipo = info.get("type")
    profile_id = info.get("profile_id")
    expires_at = info.get("expires_at", 0)
    validade = "não expira" if not expires_at else datetime.fromtimestamp(expires_at, timezone.utc).isoformat()
    bate_page_id = str(profile_id) == str(page_id)
    log.info(f"[validar_e_testar] debug_token: tipo={tipo} bate_page_id={bate_page_id} validade={validade}")

    relatorio: dict = {
        "validacao_token": {
            "tipo": tipo, "eh_token_de_pagina": tipo == "PAGE",
            "bate_com_page_id_do_env": bate_page_id, "validade": validade,
        }
    }
    if tipo != "PAGE" or not bate_page_id:
        relatorio["status"] = "token_invalido_para_esta_pagina"
        print(json.dumps(relatorio, ensure_ascii=False, indent=2))
        return 0

    config_path = Path(args.config)
    if not config_path.is_absolute():
        config_path = ROOT / config_path
    cfg = load_config(config_path)

    nome_ok, detalhe = confirmar_nome_pagina(token, page_id, cfg["pagina_esperada"], dry_run=False)
    relatorio["nome_da_pagina"] = detalhe
    if not nome_ok:
        relatorio["status"] = "pagina_incorreta"
        print(json.dumps(relatorio, ensure_ascii=False, indent=2))
        return 0

    fila_path = Path(cfg["fila"])
    if not fila_path.is_absolute():
        fila_path = ROOT / fila_path
    fila = load_fila(fila_path)
    pendentes = [r for r in fila if r["status"] in ("pendente", "aprovado")]
    if not pendentes:
        relatorio["status"] = "sem_post_pendente"
        print(json.dumps(relatorio, ensure_ascii=False, indent=2))
        return 0

    post1 = dict(pendentes[0])  # cópia — dry-run não deve mutar a fila real
    processar_item(post1, token, page_id, cfg, True, log)  # dry_run=True, nunca publica

    artigo_path = ROOT / "data" / "seo_onpage" / "otimizados" / f"{post1['slug']}.md"
    tem_crosspromo = ("sozinho-em-casa.netlify.app" in artigo_path.read_text(encoding="utf-8")
                       if artigo_path.exists() else False)

    relatorio["dry_run_post_1"] = {
        "slug": post1["slug"], "texto": post1["texto_post"], "link": post1["url"],
        "imagem": post1.get("imagem_local"), "data_prevista": post1["data_prevista"],
        "crosspromo_sozinho_em_casa_no_artigo": tem_crosspromo,
    }
    relatorio["status"] = "pronto_para_publicar"
    print(json.dumps(relatorio, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
