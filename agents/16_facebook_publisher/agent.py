"""Agente 16 — Publicação agendada em Página do Facebook (motor genérico).

Lê uma fila de posts já pronta (um arquivo JSON versionado — hoje escrita a partir de
uma revisão manual, mas podendo vir de qualquer processo) e agenda cada post na Graph
API de uma Página do Facebook, um por dia, sempre como publicação AGENDADA. Desenhado
pra virar produto: nenhum nome de página, link, horário ou fuso fica no código — tudo
vem de um arquivo de config (`config.example.yaml` é o template; cada cliente tem o seu
em `config/facebook_publisher/<cliente>.yaml`).

TRAVAS DE SEGURANÇA (cada uma bloqueia a próxima se falhar):
1. Arquivo STOP na raiz do projeto: é a primeira coisa que qualquer execução confere.
   Se existir, o agente sai imediatamente, sem publicar nada — nem em --dry-run.
2. Token de Página (`FACEBOOK_PAGE_ACCESS_TOKEN`/`FACEBOOK_PAGE_ID` no .env) precisa
   existir pra qualquer execução real (não-dry-run). Se não existir, o agente para e
   diz o que falta — nunca cria app nem token sozinho.
3. O nome da Página, confirmado pela própria Graph API, precisa bater exatamente com
   `pagina_esperada` do config. Se não bater, cancela tudo.
4. Só processa itens da fila com `status == "aprovado"` — nada é agendado de verdade
   sem uma aprovação registrada (`--aprovar`), que fica logada em
   `logs/marketing/aprovacoes.jsonl`.
5. Trava dura de no máximo `max_posts_por_dia` (do config) posts agendados por execução
   real por dia civil — verificada dentro do próprio script, olhando a fila e a data de
   hoje no fuso configurado, não apenas confiada ao agendador do sistema operacional.
6. Todo post é enviado com `published=false` e `scheduled_publish_time` no futuro —
   nunca `published=true`.
7. `--dry-run` funciona em qualquer modo, simula a chamada à Graph API sem rede, e não
   precisa de credencial real. O token nunca é impresso, logado, nem incluído em
   nenhum output — mensagens de erro da API têm o `access_token` sempre redigido.

Modos de uso:
    # aprovar um item da fila (registra em logs/marketing/aprovacoes.jsonl)
    python agent.py --config ../../config/facebook_publisher/tutorial_pet.yaml \
        --aprovar SLUG --por "Nome de quem aprovou"

    # execução diária seca (chamada pelo agendador do SO, 1x por dia): processa
    # o próximo item aprovado cuja data prevista já chegou, respeitando a trava diária
    python agent.py --config ../../config/facebook_publisher/tutorial_pet.yaml --processar-fila

    # simulação completa da fila inteira, sem tocar em nada real
    python agent.py --config ../../config/facebook_publisher/tutorial_pet.yaml \
        --confirmar-lote --dry-run
"""
from __future__ import annotations

import argparse
import csv
import json
import logging
import os
import random
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timedelta, timezone
from pathlib import Path
from zoneinfo import ZoneInfo

AGENT_DIR = Path(__file__).resolve().parent
ROOT = AGENT_DIR.parents[1]
for p in (ROOT, AGENT_DIR):
    if str(p) not in sys.path:
        sys.path.insert(0, str(p))

from core.config import load_env_file, load_yaml  # noqa: E402

AGENT_NAME = "16_facebook_publisher"
SCHEMA_VERSION = "2.0"

GRAPH_API_VERSION = "v19.0"
GRAPH_BASE = f"https://graph.facebook.com/{GRAPH_API_VERSION}"
TOKEN_ENV_VAR = "FACEBOOK_PAGE_ACCESS_TOKEN"
PAGE_ID_ENV_VAR = "FACEBOOK_PAGE_ID"

STOP_FILE = ROOT / "STOP"
MARKETING_LOG_DIR = ROOT / "logs" / "marketing"
APROVACOES_LOG = MARKETING_LOG_DIR / "aprovacoes.jsonl"


class FacebookAPIError(RuntimeError):
    pass


# --------------------------------------------------------------------------- log (mascarado, por dia)
def mask_token(texto: str) -> str:
    """Redige qualquer ocorrência de access_token de uma string antes de logar/relatar."""
    texto = re.sub(r'"access_token"\s*:\s*"[^"]*"', '"access_token":"[REDIGIDO]"', texto)
    texto = re.sub(r'access_token=[^&\s"]+', 'access_token=[REDIGIDO]', texto)
    return texto


def get_marketing_logger() -> logging.Logger:
    """Um arquivo por dia civil (UTC, só pra nome de arquivo estável), sempre mascarado."""
    MARKETING_LOG_DIR.mkdir(parents=True, exist_ok=True)
    nome_arquivo = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    logger = logging.getLogger(f"{AGENT_NAME}.marketing")
    if logger.handlers:
        return logger
    logger.setLevel(logging.DEBUG)
    logger.propagate = False

    class _MaskFilter(logging.Filter):
        def filter(self, record: logging.LogRecord) -> bool:
            record.msg = mask_token(str(record.msg))
            return True

    handler = logging.FileHandler(MARKETING_LOG_DIR / f"{nome_arquivo}.log", encoding="utf-8")
    handler.setFormatter(logging.Formatter("%(asctime)s | %(levelname)-7s | %(message)s"))
    handler.addFilter(_MaskFilter())
    console = logging.StreamHandler(sys.stderr)
    console.setFormatter(logging.Formatter("[%(levelname)s] %(message)s"))
    console.addFilter(_MaskFilter())
    logger.addHandler(handler)
    logger.addHandler(console)
    return logger


# --------------------------------------------------------------------------- STOP
def stop_ativo() -> bool:
    return STOP_FILE.exists()


# --------------------------------------------------------------------------- config
def load_config(path: Path) -> dict:
    cfg = load_yaml(path)
    obrigatorias = ("pagina_esperada", "fuso_horario", "hora_publicacao", "fila", "max_posts_por_dia")
    faltando = [k for k in obrigatorias if k not in cfg]
    if faltando:
        raise RuntimeError(f"Config '{path}' sem chaves obrigatórias: {', '.join(faltando)}")
    return cfg


# --------------------------------------------------------------------------- HTTP (sem libs externas)
def _graph_request(path: str, params: dict, method: str = "GET") -> dict:
    url = f"{GRAPH_BASE}/{path.lstrip('/')}"
    data = urllib.parse.urlencode(params).encode("utf-8")
    if method == "GET":
        req = urllib.request.Request(f"{url}?{data.decode()}", method="GET")
    else:
        req = urllib.request.Request(url, data=data, method=method)
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        raise FacebookAPIError(f"Graph API respondeu {exc.code}: {mask_token(body)}") from None
    except urllib.error.URLError as exc:
        raise FacebookAPIError(f"Falha de rede ao chamar a Graph API: {exc.reason}") from None


# --------------------------------------------------------------------------- credenciais
def check_credenciais() -> tuple[bool, str, str | None, str | None]:
    token = os.environ.get(TOKEN_ENV_VAR, "").strip()
    page_id = os.environ.get(PAGE_ID_ENV_VAR, "").strip()
    if not token:
        return False, f"{TOKEN_ENV_VAR} não está configurado em .env.", None, None
    if not page_id:
        return False, f"{PAGE_ID_ENV_VAR} não está configurado em .env.", None, None
    return True, "", token, page_id


def confirmar_nome_pagina(token: str, page_id: str, nome_esperado: str, dry_run: bool) -> tuple[bool, str]:
    if dry_run:
        return True, f"{nome_esperado} [SIMULADO — não chamado de verdade em --dry-run]"
    info = _graph_request(page_id, {"fields": "name,id", "access_token": token})
    nome_real = info.get("name", "")
    if nome_real.strip().lower() != nome_esperado.strip().lower():
        return False, (f"A página encontrada é '{nome_real}' (id {info.get('id')}), não "
                        f"'{nome_esperado}'. Publicação cancelada por segurança.")
    return True, nome_real


# --------------------------------------------------------------------------- fila
def load_fila(path: Path) -> list[dict]:
    if path.suffix == ".json":
        return json.loads(path.read_text(encoding="utf-8"))
    with path.open(encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh))


def save_fila(path: Path, rows: list[dict]) -> None:
    if path.suffix == ".json":
        path.write_text(json.dumps(rows, ensure_ascii=False, indent=2), encoding="utf-8")
        return
    with path.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


# --------------------------------------------------------------------------- cross-promoção obrigatória
# Trava adicionada em 28/09/2026: nenhum post de artigo do blog pode ser aprovado sem o
# link de algum produto cadastrado em config/produtos_relacionados.yaml. Antes disso o
# texto_post de cada item vinha de revisão/edição manual sem nenhuma exigência formal, e
# os 20 itens da fila em uso nesse momento tinham 0% de cross-promoção — corrigido
# manualmente uma vez, mas sem essa trava o problema voltaria no próximo lote. Este é o
# único ponto por onde todo item realmente passa antes de virar post de verdade (trava #4
# do cabeçalho), então é aqui que a exigência é forçada, não em algum gerador upstream.
PRODUTOS_RELACIONADOS_PATH = ROOT / "config" / "produtos_relacionados.yaml"
LIMITE_TOPO_POST = 320  # o link do produto precisa aparecer nesses primeiros caracteres (antes do "Ver mais")


def _links_de_produtos_cadastrados() -> list[str]:
    if not PRODUTOS_RELACIONADOS_PATH.exists():
        return []
    cfg = load_yaml(PRODUTOS_RELACIONADOS_PATH) or {}
    return [p["link"] for p in (cfg.get("produtos") or []) if p.get("link")]


def checar_cross_promocao(texto_post: str) -> tuple[bool, str]:
    """Bloqueia a aprovação se nenhum link de produto cadastrado aparecer no texto do post.
    Sem produto cadastrado, não há o que checar (evita travar tudo por um cadastro vazio)."""
    links = _links_de_produtos_cadastrados()
    if not links:
        return True, ""
    if any(link in texto_post[:LIMITE_TOPO_POST] for link in links):
        return True, ""
    if any(link in texto_post for link in links):
        return False, (
            f"o link do produto está no texto, mas não nos primeiros {LIMITE_TOPO_POST} caracteres — "
            "mova a chamada do produto para o COMEÇO do post (regra de 05/10/2026)."
        )
    return False, (
        "texto_post não contém o link de nenhum produto cadastrado em "
        f"{PRODUTOS_RELACIONADOS_PATH.relative_to(ROOT)} — inclua a linha de cross-promoção "
        "do produto antes de aprovar. Ver produtos_relacionados.yaml para o texto padrão."
    )


# --------------------------------------------------------------------------- aprovação
def aprovar_item(fila_path: Path, slug: str, aprovado_por: str, log: logging.Logger) -> dict:
    fila = load_fila(fila_path)
    item = next((r for r in fila if r["slug"] == slug), None)
    if item is None:
        raise RuntimeError(f"Slug '{slug}' não encontrado na fila.")
    if item["status"] != "pendente":
        raise RuntimeError(f"Slug '{slug}' está com status '{item['status']}', não 'pendente' — nada a aprovar.")

    ok, motivo = checar_cross_promocao(item.get("texto_post", ""))
    if not ok:
        raise RuntimeError(f"Aprovação bloqueada para '{slug}': {motivo}")

    agora = datetime.now(timezone.utc).isoformat(timespec="seconds")
    item["status"] = "aprovado"
    item["aprovado_por"] = aprovado_por
    item["aprovado_em"] = agora
    save_fila(fila_path, fila)

    MARKETING_LOG_DIR.mkdir(parents=True, exist_ok=True)
    registro = {"slug": slug, "aprovado_por": aprovado_por, "aprovado_em": agora}
    with APROVACOES_LOG.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(registro, ensure_ascii=False) + "\n")
    log.info(f"[{AGENT_NAME}] aprovado: {slug} por '{aprovado_por}' em {agora}")
    return item


# --------------------------------------------------------------------------- trava diária
def hoje_no_fuso(fuso_horario: str) -> str:
    return datetime.now(ZoneInfo(fuso_horario)).strftime("%Y-%m-%d")


STATUS_QUE_CONTAM_NA_TRAVA_DIARIA = {"agendado", "agendado_sem_confirmacao", "publicado", "publicado_sem_confirmacao"}


def contagem_agendados_hoje(fila: list[dict], fuso_horario: str) -> int:
    hoje = hoje_no_fuso(fuso_horario)
    return sum(1 for item in fila
               if item.get("status") in STATUS_QUE_CONTAM_NA_TRAVA_DIARIA and item.get("data_real", "").startswith(hoje))


def log_slot_perdido(log: logging.Logger, item: dict, previsto: datetime, real: datetime, motivo: str) -> None:
    log.warning(f"[{AGENT_NAME}] slot_perdido slug={item['slug']} previsto={previsto.strftime('%Y-%m-%d %H:%M %z')} "
                f"real={real.strftime('%Y-%m-%d %H:%M %z')} motivo={motivo}")


def atingiu_trava_diaria(fila: list[dict], cfg: dict) -> bool:
    return contagem_agendados_hoje(fila, cfg["fuso_horario"]) >= cfg["max_posts_por_dia"]


# --------------------------------------------------------------------------- horário variado
def horario_aleatorio_na_janela(janela: list[str], semente: int) -> tuple[int, int]:
    """Minuto aleatório dentro de [início, fim], em passos de 5 min. Determinístico pela
    semente: mesma semente sempre gera o mesmo horário — auditável, não puramente
    imprevisível pra quem opera."""
    h_ini, m_ini = (int(x) for x in janela[0].split(":"))
    h_fim, m_fim = (int(x) for x in janela[1].split(":"))
    minuto_ini, minuto_fim = h_ini * 60 + m_ini, h_fim * 60 + m_fim
    escolhido = random.Random(semente).randrange(minuto_ini, minuto_fim + 1, 5)
    return divmod(escolhido, 60)


# --------------------------------------------------------------------------- itens atrasados
def proxima_data_rotacao(ordem: int, cfg: dict, agora: datetime, log: logging.Logger | None = None) -> datetime:
    """Ordem 1 é sempre a exceção de hoje (1 post, na janela que ainda cabe hoje); a partir
    da ordem 2, cada dia sorteia max_posts_por_dia horários (1 por janela de
    janelas_horarios), com semente = semente_aleatoria + dia_index*10 + slot_index — fórmula
    documentada em config/ pra auditoria. Usada tanto pra gerar a fila quanto pra calcular o
    "próximo horário livre" de um item atrasado (empurrado pro fim da fila)."""
    janelas = list(cfg["janelas_horarios"].values())
    semente_base = cfg.get("semente_aleatoria", 0)
    tamanho_dia = cfg["max_posts_por_dia"]

    if ordem == 1:
        # hoje: só as janelas que ainda não passaram, a última se nenhuma sobrar
        agora_min = agora.hour * 60 + agora.minute
        candidatas = [j for j in janelas if agora_min < int(j[1].split(":")[0]) * 60 + int(j[1].split(":")[1])]
        janela = candidatas[0] if candidatas else janelas[-1]
        h, m = horario_aleatorio_na_janela(janela, semente_base)
        dia = agora.replace(hour=0, minute=0, second=0, microsecond=0)
    else:
        posicao = ordem - 2
        dia_index, slot_index = divmod(posicao, tamanho_dia)
        janela = janelas[slot_index % len(janelas)]
        semente = semente_base + dia_index * 10 + slot_index
        h, m = horario_aleatorio_na_janela(janela, semente)
        dia = agora.replace(hour=0, minute=0, second=0, microsecond=0) + timedelta(days=1 + dia_index)

    resultado = dia.replace(hour=h, minute=m)
    if log:
        log.info(f"[{AGENT_NAME}] horario_sorteado ordem={ordem} janela={janela} -> {resultado.strftime('%Y-%m-%d %H:%M %z')}")
    return resultado


# --------------------------------------------------------------------------- agendamento
def _scheduled_time_unix(item: dict, cfg: dict) -> int:
    if item.get("scheduled_publish_time_unix"):
        return int(item["scheduled_publish_time_unix"])
    # recalcula a partir de data_prevista + hora_publicacao do config, se necessário
    tz = ZoneInfo(cfg["fuso_horario"])
    data = datetime.strptime(item["data_prevista"][:10], "%Y-%m-%d")
    hora, minuto = (int(x) for x in cfg["hora_publicacao"].split(":"))
    quando = data.replace(hour=hora, minute=minuto, tzinfo=tz)
    return int(quando.timestamp())


def agendar_post(token: str, page_id: str, item: dict, cfg: dict, dry_run: bool) -> dict:
    scheduled_unix = _scheduled_time_unix(item, cfg)
    if dry_run:
        quando_legivel = datetime.fromtimestamp(scheduled_unix, ZoneInfo(cfg["fuso_horario"]))
        return {
            "id": "[SIMULADO]", "simulado": True,
            "preview": {
                "pagina": cfg["pagina_esperada"], "slug": item["slug"],
                "mensagem": item["texto_post"], "link": item["url"],
                "agendado_para": quando_legivel.strftime("%Y-%m-%d %H:%M %Z"),
                "published": False,
            },
        }
    params = {
        "message": item["texto_post"], "link": item["url"], "published": "false",
        "scheduled_publish_time": str(scheduled_unix), "access_token": token,
    }
    resposta = _graph_request(f"{page_id}/feed", params, method="POST")
    if "id" not in resposta:
        raise FacebookAPIError(f"Resposta sem id de post: {resposta}")
    return resposta


def confirmar_agendado(token: str, post_id: str, dry_run: bool) -> bool:
    if dry_run:
        return True
    info = _graph_request(post_id, {"fields": "is_published,scheduled_publish_time", "access_token": token})
    return info.get("is_published") is False and bool(info.get("scheduled_publish_time"))


def publicar_imediato(token: str, page_id: str, item: dict, dry_run: bool) -> dict:
    """Recuperação de atraso dentro da tolerância: o horário previsto já passou, então
    não faz sentido mandar `scheduled_publish_time` pro passado (a Graph API rejeitaria) —
    publica direto, `published=true`, sem agendamento."""
    if dry_run:
        return {
            "id": "[SIMULADO]", "simulado": True,
            "preview": {
                "slug": item["slug"], "mensagem": item["texto_post"], "link": item["url"],
                "published": True, "modo": "recuperacao_imediata",
            },
        }
    params = {"message": item["texto_post"], "link": item["url"], "published": "true", "access_token": token}
    resposta = _graph_request(f"{page_id}/feed", params, method="POST")
    if "id" not in resposta:
        raise FacebookAPIError(f"Resposta sem id de post: {resposta}")
    return resposta


def confirmar_publicado(token: str, post_id: str, dry_run: bool) -> bool:
    if dry_run:
        return True
    info = _graph_request(post_id, {"fields": "is_published", "access_token": token})
    return info.get("is_published") is True


LEAD_TIME_MINIMO_SEGUNDOS = 600  # a Graph API rejeita scheduled_publish_time a menos de 10 min do agora


def processar_item(item: dict, token: str | None, page_id: str | None, cfg: dict,
                    dry_run: bool, log: logging.Logger) -> None:
    if not dry_run:
        agora = datetime.now(ZoneInfo(cfg["fuso_horario"])).timestamp()
        folga = _scheduled_time_unix(item, cfg) - agora
        if folga < LEAD_TIME_MINIMO_SEGUNDOS:
            log.warning(f"[{AGENT_NAME}] '{item['slug']}' com só {int(folga // 60)} min de folga até o "
                        f"horário previsto — abaixo do mínimo de 10 min da Graph API. Não tentado agora; "
                        "item continua aprovado, pode ser retomado numa próxima execução com mais folga.")
            return
    try:
        resposta = agendar_post(token, page_id, item, cfg, dry_run)
        post_id = resposta["id"]
        confirmado = confirmar_agendado(token, post_id, dry_run)
        item["status"] = "agendado" if confirmado else "agendado_sem_confirmacao"
        item["post_id"] = post_id
        item["data_real"] = datetime.now(ZoneInfo(cfg["fuso_horario"])).isoformat(timespec="seconds")
        if dry_run:
            log.info(f"[{AGENT_NAME}] [DRY-RUN] '{item['slug']}' -> {json.dumps(resposta['preview'], ensure_ascii=False)}")
        else:
            log.info(f"[{AGENT_NAME}] '{item['slug']}' agendado para {item['data_prevista']} "
                     f"(post_id={post_id}, confirmado={confirmado})")
    except FacebookAPIError as exc:
        item["status"] = "falha"
        item["erro"] = str(exc)
        log.error(f"[{AGENT_NAME}] falha ao agendar '{item['slug']}': {exc}")


# --------------------------------------------------------------------------- entrypoint
def run(context: dict) -> dict:
    log = context["logger"]

    if stop_ativo():
        log.warning(f"[{AGENT_NAME}] arquivo STOP encontrado em {STOP_FILE} — encerrando sem publicar nada.")
        return {"agent": AGENT_NAME, "schema_version": SCHEMA_VERSION, "status": "parado_stop"}

    config_path = Path(context["config"])
    if not config_path.is_absolute():
        config_path = ROOT / config_path
    cfg = load_config(config_path)
    fila_path = Path(context.get("fila") or cfg["fila"])
    if not fila_path.is_absolute():
        fila_path = ROOT / fila_path
    dry_run = context.get("dry_run", False)

    # --- modo: aprovar item ---------------------------------------------------------------
    if context.get("aprovar"):
        item = aprovar_item(fila_path, context["aprovar"], context["por"], log)
        return {"agent": AGENT_NAME, "schema_version": SCHEMA_VERSION, "status": "aprovado", "item": item}

    # --- credenciais (só exigidas em execução real) ---------------------------------------
    token = page_id = None
    if not dry_run:
        ok, motivo, token, page_id = check_credenciais()
        if not ok:
            log.warning(f"[{AGENT_NAME}] aguardando_credenciais: {motivo}")
            return {
                "agent": AGENT_NAME, "schema_version": SCHEMA_VERSION, "status": "aguardando_credenciais",
                "pendencia_humana": (f"{motivo} É preciso um token de Página com a permissão "
                                      "'pages_manage_posts' e o ID dessa Página, para "
                                      f"'{cfg['pagina_esperada']}'."),
            }

    nome_ok, detalhe = confirmar_nome_pagina(token, page_id, cfg["pagina_esperada"], dry_run)
    if not nome_ok:
        log.error(f"[{AGENT_NAME}] pagina_incorreta: {detalhe}")
        return {"agent": AGENT_NAME, "schema_version": SCHEMA_VERSION, "status": "pagina_incorreta", "detalhe": detalhe}
    log.info(f"[{AGENT_NAME}] página confirmada: '{detalhe}' (dry_run={dry_run})")

    fila = load_fila(fila_path)

    # --- modo: processar-fila (uso diário real, pelo agendador do SO) ---------------------
    if context.get("processar_fila"):
        if not dry_run and atingiu_trava_diaria(fila, cfg):
            log.warning(f"[{AGENT_NAME}] trava diária: já foram agendados {cfg['max_posts_por_dia']} "
                        f"post(s) hoje para '{cfg['pagina_esperada']}'.")
            return {"agent": AGENT_NAME, "schema_version": SCHEMA_VERSION, "status": "trava_diaria"}
        hoje = hoje_no_fuso(cfg["fuso_horario"])
        candidatos = [r for r in fila if r["status"] == "aprovado" and r["data_prevista"][:10] <= hoje]
        if not candidatos:
            log.info(f"[{AGENT_NAME}] processar-fila: nenhum item aprovado e devido agora — nada a fazer.")
            return {"agent": AGENT_NAME, "schema_version": SCHEMA_VERSION, "status": "sem_itens_devidos"}
        item = sorted(candidatos, key=lambda r: r["data_prevista"])[0]

        # Janela de tolerância: se o horário previsto já passou, decide entre publicar na
        # recuperação (atraso curto, mesmo dia, trava do dia ainda permite) ou reagendar pro
        # fim da fila (atraso longo, virou o dia, ou a trava do dia já foi atingida) — nunca
        # publica em rajada, nunca mais que max_posts_por_dia no dia.
        if not dry_run:
            tz = ZoneInfo(cfg["fuso_horario"])
            agora_dt = datetime.now(tz)
            previsto_dt = datetime.fromtimestamp(_scheduled_time_unix(item, cfg), tz)
            atraso_horas = (agora_dt - previsto_dt).total_seconds() / 3600
            mesmo_dia = agora_dt.strftime("%Y-%m-%d") == previsto_dt.strftime("%Y-%m-%d")
            tolerancia = cfg.get("tolerancia_horas", 3)

            if atraso_horas > 0:
                if atraso_horas <= tolerancia and mesmo_dia and not atingiu_trava_diaria(fila, cfg):
                    log_slot_perdido(log, item, previsto_dt, agora_dt, "maquina_dormindo_recuperado")
                    try:
                        resposta = publicar_imediato(token, page_id, item, dry_run)
                        post_id = resposta["id"]
                        confirmado = confirmar_publicado(token, post_id, dry_run)
                        item["status"] = "publicado" if confirmado else "publicado_sem_confirmacao"
                        item["post_id"] = post_id
                        item["data_real"] = agora_dt.isoformat(timespec="seconds")
                        log.info(f"[{AGENT_NAME}] '{item['slug']}' publicado na recuperação "
                                 f"(atraso {atraso_horas:.1f}h, post_id={post_id}, confirmado={confirmado})")
                    except FacebookAPIError as exc:
                        item["status"] = "falha"
                        item["erro"] = str(exc)
                        log.error(f"[{AGENT_NAME}] falha ao publicar na recuperação '{item['slug']}': {exc}")
                    save_fila(fila_path, fila)
                    return {"agent": AGENT_NAME, "schema_version": SCHEMA_VERSION, "status": item["status"],
                            "slug": item["slug"]}

                motivo = "fora_da_tolerancia" if (atraso_horas > tolerancia or not mesmo_dia) else "trava_diaria_atingida"
                log_slot_perdido(log, item, previsto_dt, agora_dt, motivo)
                antiga = item["data_prevista"]
                nova_ordem = max((r.get("ordem", 0) for r in fila), default=0) + 1
                nova_data = proxima_data_rotacao(nova_ordem, cfg, agora_dt, log)
                item["ordem"] = nova_ordem
                item["data_prevista"] = nova_data.strftime("%Y-%m-%d %H:%M %z")
                item["scheduled_publish_time_unix"] = int(nova_data.timestamp())
                save_fila(fila_path, fila)
                log.warning(f"[{AGENT_NAME}] '{item['slug']}' estava atrasado ({antiga}, motivo={motivo}) — "
                            f"reagendado para {item['data_prevista']}, sem publicar em rajada.")
                return {"agent": AGENT_NAME, "schema_version": SCHEMA_VERSION, "status": "item_atrasado_reagendado",
                        "slug": item["slug"], "de": antiga, "para": item["data_prevista"], "motivo": motivo}

        processar_item(item, token, page_id, cfg, dry_run, log)
        if not dry_run:
            save_fila(fila_path, fila)
        return {"agent": AGENT_NAME, "schema_version": SCHEMA_VERSION, "status": item["status"], "slug": item["slug"]}

    # --- modo: confirmar-lote (só faz sentido de verdade em --dry-run) --------------------
    if context.get("confirmar_lote"):
        if not dry_run:
            return {
                "agent": AGENT_NAME, "schema_version": SCHEMA_VERSION, "status": "bloqueado",
                "motivo": ("--confirmar-lote fora de --dry-run violaria a trava de "
                           f"{cfg['max_posts_por_dia']} post(s)/dia. Use --processar-fila, "
                           "chamado uma vez por dia pelo agendador do sistema."),
            }
        pendentes = [r for r in fila if r["status"] in ("pendente", "aprovado")]
        resultados = []
        for item in pendentes:
            processar_item(item, token, page_id, cfg, dry_run, log)
            resultados.append({"slug": item["slug"], "status": item["status"]})
        # dry-run nunca escreve de volta na fila real
        return {"agent": AGENT_NAME, "schema_version": SCHEMA_VERSION, "status": "ok_dry_run", "resultados": resultados}

    # --- modo padrão: teste único (primeiro pendente/aprovado) ----------------------------
    pendentes = [r for r in fila if r["status"] in ("pendente", "aprovado")]
    if not pendentes:
        return {"agent": AGENT_NAME, "schema_version": SCHEMA_VERSION, "status": "sem_pendentes"}
    item = pendentes[0]
    if not dry_run and item["status"] != "aprovado":
        return {
            "agent": AGENT_NAME, "schema_version": SCHEMA_VERSION, "status": "bloqueado_sem_aprovacao",
            "slug": item["slug"], "motivo": "Item ainda 'pendente' — aprove com --aprovar antes de agendar de verdade.",
        }
    if not dry_run and atingiu_trava_diaria(fila, cfg):
        return {"agent": AGENT_NAME, "schema_version": SCHEMA_VERSION, "status": "trava_diaria"}
    processar_item(item, token, page_id, cfg, dry_run, log)
    if not dry_run:
        save_fila(fila_path, fila)
    return {"agent": AGENT_NAME, "schema_version": SCHEMA_VERSION, "status": item["status"], "slug": item["slug"]}


def main() -> int:
    for stream in (sys.stdout, sys.stderr):
        stream.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description="Agente 16 — publicação agendada em Página do Facebook")
    parser.add_argument("--config", required=True, help="Caminho do config.yaml (ver config.example.yaml)")
    parser.add_argument("--fila", help="Sobrescreve o caminho de fila definido no config")
    parser.add_argument("--dry-run", action="store_true", help="Simula tudo, nunca chama a Graph API de verdade")
    parser.add_argument("--aprovar", metavar="SLUG", help="Aprova um item pendente da fila")
    parser.add_argument("--por", metavar="NOME", help="Nome de quem aprova (obrigatório com --aprovar)")
    parser.add_argument("--processar-fila", action="store_true",
                         help="Modo diário: processa 1 item aprovado e devido, respeitando a trava diária")
    parser.add_argument("--confirmar-lote", action="store_true",
                         help="Processa todos os pendentes/aprovados — só tem efeito real junto com --dry-run")
    args = parser.parse_args()

    if args.aprovar and not args.por:
        parser.error("--aprovar exige --por \"Nome de quem aprovou\"")

    load_env_file()
    log = get_marketing_logger()
    if args.processar_fila:
        # Batimento: toda execução do agendador do SO grava uma linha, mesmo sem nada a
        # fazer — silêncio no log passa a significar falha (máquina dormindo, tarefa não
        # disparou), não ausência de trabalho.
        log.info(f"[{AGENT_NAME}] processar-fila: batimento — execução iniciada")
    output = run({
        "config": args.config, "fila": args.fila, "dry_run": args.dry_run,
        "aprovar": args.aprovar, "por": args.por,
        "processar_fila": args.processar_fila, "confirmar_lote": args.confirmar_lote,
        "logger": log,
    })
    print(json.dumps(output, ensure_ascii=False, indent=2))
    return 0 if output["status"] not in ("pagina_incorreta",) else 2


if __name__ == "__main__":
    sys.exit(main())
