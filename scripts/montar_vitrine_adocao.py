#!/usr/bin/env python3
"""Monta o rascunho semanal da vitrine "Pets para adoção em São Paulo".

Lê data/adocao/envios/*.json (formato em data/adocao/envios/README.md), usa o molde
templates/vitrine_adocao.md e grava em
data/content_writer/rascunhos/pets-para-adocao-em-sao-paulo-edicao-AAAA-MM-DD.md.

Regras: só entra envio com "aprovado": true; envios com "exemplo": true são ignorados,
exceto com --teste (que grava só em --saida, nunca em rascunhos); só campos de
config/adocao.yaml campos_visiveis entram no texto; dado de pessoa física é recusado.
Uso: python3 scripts/montar_vitrine_adocao.py [--data AAAA-MM-DD] [--teste --saida DIR]
Não publica nada: o rascunho segue a curadoria humana.
"""
import argparse
import datetime as dt
import json
import re
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
MOLDE = RAIZ / "templates" / "vitrine_adocao.md"
ENVIOS = RAIZ / "data" / "adocao" / "envios"
RASCUNHOS = RAIZ / "data" / "content_writer" / "rascunhos"

# Campos que podem aparecer no artigo (espelham config/adocao.yaml campos_visiveis).
CAMPOS_VISIVEIS = [
    "entidade_nome", "entidade_cidade_uf", "contato_publico_entidade",
    "especie", "nome_animal", "porte", "idade_aproximada", "sexo",
    "temperamento", "saude_vacinas", "foto_url",
]
OBRIGATORIOS = CAMPOS_VISIVEIS + ["tipo_entidade", "contato_e_da_entidade",
                                  "responsavel_confirmado", "autoriza_publicacao"]
TIPOS_ENTIDADE = {"ong", "abrigo", "grupo_protetores"}
ESPECIES = {"Cachorro", "Gato"}
PORTES = {"Pequeno", "Médio", "Grande"}
SEXOS = {"Macho", "Fêmea"}
RE_CPF = re.compile(r"\b\d{3}\.?\d{3}\.?\d{3}-?\d{2}\b")
RE_RG = re.compile(r"\b(rg|cpf)\b\s*[:nº.]*\s*\d", re.I)
RE_EMAIL = re.compile(r"[\w.+-]+@[\w-]+\.[\w.-]+")

ABERTURA = (
    "Adotar um cão ou um gato é um compromisso que pode durar mais de uma década: "
    "vale conhecer o animal, conversar com a entidade e combinar a escolha com a "
    "sua rotina e a sua casa. Reunimos abaixo animais enviados por ONGs, abrigos e "
    "grupos de proteção de São Paulo e região, com o contato oficial de cada entidade."
)


def validar(envio):
    """Devolve lista de motivos de recusa (vazia se o envio é aceitável)."""
    erros = []
    for campo in OBRIGATORIOS:
        if campo not in envio or envio[campo] in ("", None):
            erros.append(f"campo ausente: {campo}")
    if erros:
        return erros
    if envio["tipo_entidade"] not in TIPOS_ENTIDADE:
        erros.append("tipo_entidade fora de ong/abrigo/grupo_protetores (pessoa física não entra)")
    for flag in ("contato_e_da_entidade", "responsavel_confirmado", "autoriza_publicacao"):
        if envio[flag] is not True:
            erros.append(f"{flag} precisa ser true")
    if envio["especie"] not in ESPECIES:
        erros.append("especie inválida")
    if envio["porte"] not in PORTES:
        erros.append("porte inválido")
    if envio["sexo"] not in SEXOS:
        erros.append("sexo inválido")
    if not str(envio["foto_url"]).startswith(("https://", "/")):
        erros.append("foto_url precisa ser https:// ou caminho do site")
    for campo in CAMPOS_VISIVEIS:
        texto = str(envio[campo])
        if RE_CPF.search(texto) or RE_RG.search(texto):
            erros.append(f"documento pessoal (CPF/RG) em {campo}")
    # E-mail no contato é permitido só se parecer da entidade; pessoal comum vira recusa.
    contato = str(envio["contato_publico_entidade"])
    for email in RE_EMAIL.findall(contato):
        if email.split("@")[1].lower() in {"gmail.com", "hotmail.com", "outlook.com", "yahoo.com", "yahoo.com.br", "icloud.com"}:
            erros.append("e-mail de provedor pessoal no contato; usar WhatsApp/Instagram/site da entidade")
    return erros


def limpar(envio):
    """Mantém só os campos visíveis, em uma linha, sem marcação que quebre o markdown."""
    saida = {}
    for campo in CAMPOS_VISIVEIS:
        valor = re.sub(r"\s+", " ", str(envio[campo])).strip()
        saida[campo] = valor.replace("[", "(").replace("]", ")") if campo != "foto_url" else valor
    return saida


def carregar(pasta, incluir_exemplos):
    aceitos, recusados, ignorados = [], [], []
    for arq in sorted(pasta.glob("*.json")):
        try:
            envio = json.loads(arq.read_text(encoding="utf-8"))
        except json.JSONDecodeError as e:
            recusados.append((arq.name, [f"JSON inválido: {e}"]))
            continue
        if envio.get("exemplo") is True and not incluir_exemplos:
            ignorados.append((arq.name, "exemplo"))
            continue
        if envio.get("aprovado") is not True:
            ignorados.append((arq.name, "não aprovado"))
            continue
        erros = validar(envio)
        if erros:
            recusados.append((arq.name, erros))
        else:
            aceitos.append(limpar(envio))
    return aceitos, recusados, ignorados


def montar(molde, fichas, data):
    ini, fim = "<!-- FICHA_INICIO -->", "<!-- FICHA_FIM -->"
    antes, resto = molde.split(ini)
    bloco, depois = resto.split(fim)
    texto_fichas = "".join(
        re.sub(r"\{\{(\w+)\}\}", lambda m: f[m.group(1)], bloco) for f in fichas
    )
    n = len(fichas)
    gatos = sum(f["especie"] == "Gato" for f in fichas)
    caes = n - gatos
    partes = []
    if caes:
        partes.append(f"{caes} {'cachorro' if caes == 1 else 'cachorros'}")
    if gatos:
        partes.append(f"{gatos} {'gato' if gatos == 1 else 'gatos'}")
    ents = len({f["entidade_nome"] for f in fichas})
    resumo = (" e ".join(partes) + f" de {ents} " + ("entidade" if ents == 1 else "entidades")
              + " de São Paulo e região.")
    texto = antes + texto_fichas + depois
    texto = re.sub(r"^# MOLDE[^\n]*\n", "", texto, flags=re.M)  # comentário do molde não vai ao rascunho
    subs = {
        "DATA_ISO": data.isoformat(), "DATA_DDMM": data.strftime("%d/%m"),
        "GERADO_EM": dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat(),
        "ABERTURA": ABERTURA, "RESUMO_EDICAO": resumo,
    }
    return re.sub(r"\{\{(\w+)\}\}", lambda m: subs.get(m.group(1), m.group(0)), texto)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--data", default=dt.date.today().isoformat(), help="AAAA-MM-DD da edição")
    ap.add_argument("--envios", default=str(ENVIOS))
    ap.add_argument("--teste", action="store_true", help="inclui envios de exemplo; exige --saida")
    ap.add_argument("--saida", help="pasta de saída (obrigatória com --teste)")
    args = ap.parse_args(argv)

    data = dt.date.fromisoformat(args.data)
    if args.teste and not args.saida:
        ap.error("--teste exige --saida (o teste nunca grava em rascunhos)")
    destino = Path(args.saida) if args.saida else RASCUNHOS

    aceitos, recusados, ignorados = carregar(Path(args.envios), args.teste)
    for nome, motivo in ignorados:
        print(f"ignorado: {nome} ({motivo})")
    for nome, erros in recusados:
        print(f"RECUSADO: {nome}: " + "; ".join(erros))
    if not aceitos:
        print("Nenhum envio aprovado e válido; nada gerado.")
        return 0
    destino.mkdir(parents=True, exist_ok=True)
    saida = destino / f"pets-para-adocao-em-sao-paulo-edicao-{data.isoformat()}.md"
    saida.write_text(montar(MOLDE.read_text(encoding="utf-8"), aceitos, data), encoding="utf-8")
    print(f"gerado: {saida} ({len(aceitos)} animal(is))")
    return 0


if __name__ == "__main__":
    sys.exit(main())
