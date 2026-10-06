"""Troca o token de usuário de curta duração por um token de Página de longa duração,
e grava o resultado direto no .env. Zero dado de cliente no código — tudo lido do .env:

    FACEBOOK_APP_ID, FACEBOOK_APP_SECRET, FACEBOOK_USER_TOKEN_CURTO, FACEBOOK_PAGE_ID

Passos (cada um só avança se o anterior passar):
  1. Troca o token curto por um token de USUÁRIO de longa duração
     (grant_type=fb_exchange_token). Se FACEBOOK_APP_SECRET estiver vazio, pula a troca
     e usa o token recebido direto como token de usuário (ex: token já estendido pelo
     depurador de Access Token da Meta).
  2. Chama /me/accounts com esse token e procura a Página cujo id bate com
     FACEBOOK_PAGE_ID. Se não achar, para e lista as páginas que vieram (nome + id,
     nunca token).
  3. Valida o token da Página com debug_token: is_valid, type == "PAGE", profile_id
     bate com FACEBOOK_PAGE_ID, expires_at == 0 (não expira). Qualquer coisa fora
     disso, para.
  4. Grava FACEBOOK_PAGE_ACCESS_TOKEN no .env e apaga FACEBOOK_USER_TOKEN_CURTO (a
     linha fica vazia). FACEBOOK_APP_SECRET é mantido — serve pra renovar depois.

Nenhum token é impresso, logado ou incluído em output inteiro em momento nenhum — só
os 4 últimos caracteres, pra permitir identificar qual token é qual sem expor o valor.

Uso:
    python trocar_token.py
"""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path

AGENT_DIR = Path(__file__).resolve().parent
ROOT = AGENT_DIR.parents[1]
for p in (ROOT, AGENT_DIR):
    if str(p) not in sys.path:
        sys.path.insert(0, str(p))

from core.config import load_env_file  # noqa: E402
from agent import GRAPH_BASE, FacebookAPIError, _graph_request, get_marketing_logger  # noqa: E402

ENV_PATH = ROOT / ".env"
AGENT_NAME = "trocar_token"


def ultimos4(valor: str | None) -> str:
    if not valor:
        return "(vazio)"
    return f"...{valor[-4:]}"


def set_env_var(path: Path, key: str, valor: str) -> None:
    """Substitui só a linha 'KEY=...' pelo novo valor, sem tocar no resto do arquivo."""
    linhas = path.read_text(encoding="utf-8").splitlines(keepends=True)
    alvo = f"{key}="
    achou = False
    for i, linha in enumerate(linhas):
        if linha.startswith(alvo):
            quebra = "\n" if linha.endswith("\n") else ""
            linhas[i] = f"{key}={valor}{quebra}"
            achou = True
            break
    if not achou:
        raise RuntimeError(f"Linha '{alvo}' não encontrada em {path} — nada foi alterado.")
    path.write_text("".join(linhas), encoding="utf-8")


def check_credenciais() -> tuple[bool, str, dict]:
    valores = {
        "app_id": os.environ.get("FACEBOOK_APP_ID", "").strip(),
        "app_secret": os.environ.get("FACEBOOK_APP_SECRET", "").strip(),
        "user_token_curto": os.environ.get("FACEBOOK_USER_TOKEN_CURTO", "").strip(),
        "page_id": os.environ.get("FACEBOOK_PAGE_ID", "").strip(),
    }
    # app_id/app_secret são opcionais: sem app_secret, o token recebido já é usado direto
    # como token de usuário de longa duração (pulando a troca fb_exchange_token).
    obrigatorias = ("user_token_curto", "page_id")
    faltando = [k for k in obrigatorias if not valores[k]]
    if faltando:
        return False, f"faltando no .env: {', '.join(faltando)}", valores
    return True, "", valores


def trocar_token_longa_duracao(app_id: str, app_secret: str, token_curto: str) -> str:
    params = {"grant_type": "fb_exchange_token", "client_id": app_id,
              "client_secret": app_secret, "fb_exchange_token": token_curto}
    resposta = _graph_request("oauth/access_token", params, method="GET")
    if "access_token" not in resposta:
        raise FacebookAPIError(f"Resposta sem access_token na troca: {resposta}")
    return resposta["access_token"]


def buscar_pagina(token_usuario: str, page_id: str) -> tuple[dict | None, list[dict]]:
    resposta = _graph_request("me/accounts", {"access_token": token_usuario}, method="GET")
    paginas = resposta.get("data", [])
    achada = next((p for p in paginas if str(p.get("id")) == str(page_id)), None)
    return achada, [{"nome": p.get("name"), "id": p.get("id")} for p in paginas]


def validar_token_pagina(token_pagina: str, page_id: str) -> dict:
    info = _graph_request("debug_token", {"input_token": token_pagina, "access_token": token_pagina}, method="GET")
    return info.get("data", {})


def main() -> int:
    for stream in (sys.stdout, sys.stderr):
        stream.reconfigure(encoding="utf-8")
    load_env_file()
    log = get_marketing_logger()

    ok, motivo, valores = check_credenciais()
    if not ok:
        print(json.dumps({"status": "aguardando_credenciais", "motivo": motivo}, ensure_ascii=False, indent=2))
        log.warning(f"[{AGENT_NAME}] aguardando_credenciais: {motivo}")
        return 0

    page_id = valores["page_id"]

    if not valores["app_secret"]:
        log.info(f"[{AGENT_NAME}] passo 1: sem FACEBOOK_APP_SECRET — pulando a troca, usando o token "
                 f"recebido direto ({ultimos4(valores['user_token_curto'])}) como token de usuário")
        token_usuario_longo = valores["user_token_curto"]
    else:
        log.info(f"[{AGENT_NAME}] passo 1: trocando token curto ({ultimos4(valores['user_token_curto'])}) "
                 "por token de usuário de longa duração")
        try:
            token_usuario_longo = trocar_token_longa_duracao(valores["app_id"], valores["app_secret"],
                                                               valores["user_token_curto"])
        except FacebookAPIError as exc:
            log.error(f"[{AGENT_NAME}] falha na troca do token: {exc}")
            print(json.dumps({"status": "falha_troca_token", "erro": str(exc)}, ensure_ascii=False, indent=2))
            return 2
        log.info(f"[{AGENT_NAME}] passo 1 ok: token de usuário longo obtido ({ultimos4(token_usuario_longo)})")

    log.info(f"[{AGENT_NAME}] passo 2: procurando a Página {page_id} em /me/accounts")
    try:
        pagina, todas = buscar_pagina(token_usuario_longo, page_id)
    except FacebookAPIError as exc:
        log.error(f"[{AGENT_NAME}] falha ao chamar /me/accounts: {exc}")
        print(json.dumps({"status": "falha_me_accounts", "erro": str(exc)}, ensure_ascii=False, indent=2))
        return 2
    if pagina is None:
        log.error(f"[{AGENT_NAME}] Página {page_id} não encontrada. Páginas retornadas: {todas}")
        print(json.dumps({"status": "pagina_nao_encontrada", "paginas_retornadas": todas},
                          ensure_ascii=False, indent=2))
        return 2
    token_pagina = pagina["access_token"]
    log.info(f"[{AGENT_NAME}] passo 2 ok: página '{pagina.get('name')}' encontrada "
             f"(token {ultimos4(token_pagina)})")

    log.info(f"[{AGENT_NAME}] passo 3: validando o token da página com debug_token")
    try:
        debug = validar_token_pagina(token_pagina, page_id)
    except FacebookAPIError as exc:
        log.error(f"[{AGENT_NAME}] falha ao chamar debug_token: {exc}")
        print(json.dumps({"status": "falha_debug_token", "erro": str(exc)}, ensure_ascii=False, indent=2))
        return 2
    checagens = {
        "is_valid": debug.get("is_valid") is True,
        "tipo_page": debug.get("type") == "PAGE",
        "page_id_bate": str(debug.get("profile_id")) == str(page_id),
        "nao_expira": debug.get("expires_at", -1) == 0,
    }
    if not all(checagens.values()):
        log.error(f"[{AGENT_NAME}] validação do token da página falhou: {checagens} (debug_token: "
                  f"type={debug.get('type')} profile_id={debug.get('profile_id')} "
                  f"expires_at={debug.get('expires_at')} is_valid={debug.get('is_valid')})")
        print(json.dumps({"status": "token_pagina_invalido", "checagens": checagens}, ensure_ascii=False, indent=2))
        return 2
    log.info(f"[{AGENT_NAME}] passo 3 ok: token de página válido, tipo PAGE, page_id bate, não expira")

    log.info(f"[{AGENT_NAME}] passo 4: gravando FACEBOOK_PAGE_ACCESS_TOKEN e limpando "
             "FACEBOOK_USER_TOKEN_CURTO no .env")
    set_env_var(ENV_PATH, "FACEBOOK_PAGE_ACCESS_TOKEN", token_pagina)
    set_env_var(ENV_PATH, "FACEBOOK_USER_TOKEN_CURTO", "")
    log.info(f"[{AGENT_NAME}] passo 4 ok: .env atualizado (FACEBOOK_APP_SECRET mantido)")

    print(json.dumps({
        "status": "ok", "pagina": pagina.get("name"), "page_id": page_id,
        "token_pagina_final": ultimos4(token_pagina),
    }, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
