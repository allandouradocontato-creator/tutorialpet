"""Edição cirúrgica de um valor escalar dentro de um YAML de configuração, preservando
comentários e formatação — usada pelo agente 13 para os ajustes de Nível 1.

PyYAML (yaml.safe_dump) reescreveria o arquivo inteiro e apagaria todos os comentários
`# explicação` que os outros arquivos de config têm — inaceitável para este projeto, que
trata esses comentários como documentação viva. Por isso, o ajuste é feito por
substituição de linha, via regex sobre a indentação, em vez de reserializar o YAML.

Só funciona para o padrão usado nos arquivos deste projeto: chaves simples
(`campo: valor`) dentro de blocos indentados por 2 espaços — não é um editor de YAML
genérico.
"""
from __future__ import annotations

import re
from pathlib import Path


class YamlEditError(RuntimeError):
    pass


def _format_value(value) -> str:
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, float):
        return f"{value:g}"
    return str(value)


def set_scalar(path: Path, key_path: list[str], new_value) -> str:
    """Localiza `key_path` (ex.: ['default', 'volume_mensal_minimo'] ou
    ['sites', 'pets-tutores-iniciantes', 'volume_mensal_minimo']) navegando pela
    indentação (2 espaços por nível) e troca só o valor daquela linha, preservando
    qualquer comentário à direita. Retorna o valor anterior (como string bruta)."""
    lines = Path(path).read_text(encoding="utf-8").splitlines(keepends=True)
    target_depth = len(key_path) - 1
    target_key = key_path[-1]

    depth = -1  # profundidade do bloco atual sendo rastreado (-1 = raiz)
    matched_ancestors = 0  # quantos níveis de key_path já bateram, em sequência
    for i, raw_line in enumerate(lines):
        stripped = raw_line.rstrip("\n")
        if not stripped.strip() or stripped.lstrip().startswith("#"):
            continue
        indent = len(stripped) - len(stripped.lstrip(" "))
        this_depth = indent // 2
        m = re.match(r"^(\s*)([A-Za-z0-9_\-]+):(\s*)(.*)$", stripped)
        if not m:
            continue
        key = m.group(2)

        if this_depth < matched_ancestors:
            matched_ancestors = this_depth  # subiu na árvore: reseta o quanto já tínhamos casado

        if this_depth == matched_ancestors and matched_ancestors < len(key_path) and key == key_path[matched_ancestors]:
            if matched_ancestors == target_depth and key == target_key:
                comment_match = re.search(r"(\s*#.*)$", m.group(4))
                comment = comment_match.group(1) if comment_match else ""
                old_value = (m.group(4)[: comment_match.start()] if comment_match else m.group(4)).strip()
                new_line = f"{m.group(1)}{key}:{m.group(3)}{_format_value(new_value)}{comment}\n"
                lines[i] = new_line
                Path(path).write_text("".join(lines), encoding="utf-8")
                return old_value
            matched_ancestors += 1

    raise YamlEditError(f"caminho {'.'.join(key_path)} não encontrado em {path} (edição cirúrgica exige a "
                         "mesma indentação/formato já usado no arquivo)")
