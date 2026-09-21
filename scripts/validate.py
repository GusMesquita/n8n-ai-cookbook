"""Valida os workflows de workflows/*/ antes que alguém tente importá-los no n8n.

Roda sem dependências: `python3 scripts/validate.py`.
Sai com status 1 se qualquer arquivo estiver quebrado.
"""

import json
import re
import sys
from pathlib import Path

WORKFLOWS = Path(__file__).resolve().parent.parent / "workflows"

# URL fixa dentro do JSON é o bug que faz o workflow "funcionar na sua máquina":
# quem importa recebe um endpoint que não existe do lado dele. Vai por $env.
HARDCODED_URL = re.compile(r"https?://(?!\{)[^\"\s]+")


def check(path: Path) -> list[str]:
    try:
        wf = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return [f"JSON inválido: {exc}"]

    errors = []
    nodes = wf.get("nodes")
    connections = wf.get("connections")

    if not isinstance(nodes, list) or not nodes:
        return ["sem lista 'nodes' não-vazia — n8n recusa a importação"]
    if not isinstance(connections, dict):
        errors.append("sem objeto 'connections'")

    names = set()
    for i, node in enumerate(nodes):
        for field in ("name", "type", "typeVersion", "position"):
            if field not in node:
                errors.append(f"nodes[{i}] sem '{field}'")
        name = node.get("name")
        if name in names:
            errors.append(f"nome de node duplicado: {name!r}")
        names.add(name)
        # Credencial embutida no arquivo vaza segredo no git; o n8n só precisa da referência.
        for cred in (node.get("credentials") or {}).values():
            if isinstance(cred, dict) and set(cred) - {"id", "name"}:
                errors.append(f"node {name!r} carrega dados de credencial inline")

    # Uma conexão apontando para node inexistente quebra só na hora da execução.
    for source, outputs in (connections or {}).items():
        if source not in names:
            errors.append(f"connections referencia node inexistente: {source!r}")
        for branch in outputs.get("main", []):
            for link in branch or []:
                target = link.get("node")
                if target not in names:
                    errors.append(f"{source!r} conecta em node inexistente: {target!r}")

    # Convenção: nada de endpoint fixo — só $env.
    for match in HARDCODED_URL.findall(json.dumps(wf, ensure_ascii=False)):
        errors.append(f"URL fixa no workflow: {match} — use uma variável de ambiente ($env)")

    if not (path.parent / "README.md").exists():
        errors.append("sem README.md ao lado do workflow.json")

    return errors


def main() -> int:
    files = sorted(WORKFLOWS.glob("*/workflow.json"))
    if not files:
        print(f"nenhum workflow em {WORKFLOWS}", file=sys.stderr)
        return 1

    failed = False
    for path in files:
        errors = check(path)
        if errors:
            failed = True
            print(f"FALHOU {path.parent.name}")
            for err in errors:
                print(f"  - {err}")
        else:
            print(f"ok     {path.parent.name}")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
