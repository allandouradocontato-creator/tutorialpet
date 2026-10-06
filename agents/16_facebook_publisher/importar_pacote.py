"""Converte um pacote de publicação (contrato v1.0, ver squads/viral-1/docs/contrato-publicacao.md)
em itens da fila do Agente 16. Filtra só `plataforma == "facebook"` — o pacote pode ter itens
de outras plataformas, que não são deste publicador. Idempotente pelo `id` do contrato: um
`id` já presente na fila nunca é duplicado.

O caminho de imagem é conferido em disco antes de entrar na fila (o próprio contrato exige
isso de quem gera o pacote — aqui é a segunda checagem, do lado de quem consome).

Uso:
    python importar_pacote.py --pacote <pacote.json> --config <config.yaml>
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path

AGENT_DIR = Path(__file__).resolve().parent
ROOT = AGENT_DIR.parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from core.config import load_yaml  # noqa: E402
from agent import get_marketing_logger  # noqa: E402

CONTRATO_VERSAO_SUPORTADA = "1.0"


def carregar_fila(path: Path) -> list[dict]:
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else []


def converter_item(item: dict, ordem: int) -> dict:
    quando = datetime.fromisoformat(item["publicar_em"])
    return {
        "ordem": ordem,
        "slug": item["id"],
        "titulo": item.get("pilar", item["id"]),
        "pilar": item.get("pilar", ""),
        "url": item.get("link"),
        "imagem_local": item.get("imagem"),
        "texto_post": item["texto"],
        "data_prevista": quando.strftime("%Y-%m-%d %H:%M %z"),
        "scheduled_publish_time_unix": int(quando.timestamp()),
        "status": "pendente",
        "aprovado_por": None,
        "aprovado_em": None,
        "data_real": None,
        "post_id": None,
        "erro": None,
        "origem_contrato": {"cta": item.get("cta"), "hashtags": item.get("hashtags", [])},
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Importa um pacote de publicação (contrato) para a fila do Agente 16")
    parser.add_argument("--pacote", required=True, help="Caminho do JSON do pacote de publicação")
    parser.add_argument("--config", required=True, help="Caminho do config.yaml do Agente 16")
    parser.add_argument("--fila", help="Sobrescreve o caminho de fila definido no config")
    args = parser.parse_args()

    log = get_marketing_logger()
    cfg = load_yaml(Path(args.config))
    fila_path = Path(args.fila or cfg["fila"])
    if not fila_path.is_absolute():
        fila_path = ROOT / fila_path

    pacote = json.loads(Path(args.pacote).read_text(encoding="utf-8"))
    if pacote.get("contrato_versao") != CONTRATO_VERSAO_SUPORTADA:
        log.error(f"[importar_pacote] contrato_versao '{pacote.get('contrato_versao')}' não suportada "
                  f"(esperado '{CONTRATO_VERSAO_SUPORTADA}')")
        print(json.dumps({"status": "contrato_incompativel"}, ensure_ascii=False))
        return 2

    fila = carregar_fila(fila_path)
    ids_existentes = {r["slug"] for r in fila}
    ordem_base = max((r.get("ordem", 0) for r in fila), default=0)

    importados, ignorados = [], []
    for item in pacote.get("itens", []):
        if item.get("plataforma") != "facebook":
            continue
        if item["id"] in ids_existentes:
            ignorados.append({"id": item["id"], "motivo": "já existe na fila"})
            log.info(f"[importar_pacote] '{item['id']}' ignorado — já está na fila")
            continue
        imagem = item.get("imagem")
        if imagem and not (ROOT / imagem).exists():
            ignorados.append({"id": item["id"], "motivo": f"imagem não encontrada: {imagem}"})
            log.error(f"[importar_pacote] '{item['id']}' ignorado — imagem não encontrada: {imagem}")
            continue
        ordem_base += 1
        fila.append(converter_item(item, ordem_base))
        importados.append(item["id"])
        log.info(f"[importar_pacote] '{item['id']}' importado do pacote pra fila (status=pendente)")

    fila_path.parent.mkdir(parents=True, exist_ok=True)
    fila_path.write_text(json.dumps(fila, ensure_ascii=False, indent=2), encoding="utf-8")

    resultado = {"status": "ok", "importados": importados, "ignorados": ignorados, "total_na_fila": len(fila)}
    print(json.dumps(resultado, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
