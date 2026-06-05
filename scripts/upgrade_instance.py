#!/usr/bin/env python3
"""upgrade_instance.py - Reporte de adopcion asistida entre versiones del protocolo.

Compara el conjunto adoptable de archivos del master (este repo) contra una instancia y
emite un reporte de deltas con acciones recomendadas. NO modifica la instancia: solo lee
(y, si se pide --report, escribe ese archivo de reporte).

Ver DECISION-0006 §4 y Area_comun/specs/SPEC-0019-upgrade-asistido.md. Neutral de dominio.

Uso:
    python scripts/upgrade_instance.py --instance <ruta> [--master <ruta>] [--report <archivo>]
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

# Conjunto adoptable (DISENO-robustez-operacional.md §1.2): archivos genericos/masters que una
# instancia copia verbatim a la misma ruta relativa. Configurable via master
# protocol.config.json -> {"upgrade": {"adoptable_globs": [...]}}.
DEFAULT_ADOPTABLE_GLOBS = [
    "AGENTS.template.md",
    "CLAUDE.template.md",
    "protocol.config.template.json",
    "Area_comun/README.template.md",
    "Area_comun/state/*.template.json",
    "Area_comun/protocol/*.md",
    "Area_comun/specs/*_TEMPLATE.md",
    "profiles/PROFILE_TEMPLATE/**/*",
    "scripts/*.py",
    "scripts/*.ps1",
]


def read_protocol_version(root: Path) -> str:
    cfg = root / "protocol.config.json"
    if not cfg.is_file():
        return "unknown"
    try:
        data = json.loads(cfg.read_text(encoding="utf-8-sig"))
    except (ValueError, OSError):
        return "unknown"
    return str(data.get("protocol_version", "unknown"))


def adoptable_globs(master: Path) -> list[str]:
    cfg = master / "protocol.config.json"
    if cfg.is_file():
        try:
            data = json.loads(cfg.read_text(encoding="utf-8-sig"))
            globs = data.get("upgrade", {}).get("adoptable_globs")
            if isinstance(globs, list) and globs:
                return [str(g) for g in globs]
        except (ValueError, OSError):
            pass
    return DEFAULT_ADOPTABLE_GLOBS


def collect_files(root: Path, globs: list[str]) -> set[str]:
    """Rutas relativas (posix) de los archivos que matchean los globs adoptables."""
    found: set[str] = set()
    for pattern in globs:
        for path in root.glob(pattern):
            if path.is_file():
                found.add(path.relative_to(root).as_posix())
    return found


def normalized(path: Path) -> str:
    """Contenido con EOL+BOM normalizado para comparar sin falsos 'cambiado' por CRLF/LF/BOM."""
    try:
        text = path.read_text(encoding="utf-8-sig")
    except (OSError, UnicodeDecodeError):
        text = path.read_bytes().decode("utf-8-sig", errors="replace")
    return text.replace("\r\n", "\n").replace("\r", "\n")


def classify(master: Path, instance: Path, rel_files: set[str]) -> list[tuple[str, str]]:
    rows: list[tuple[str, str]] = []
    for rel in sorted(rel_files):
        m = master / rel
        i = instance / rel
        if not m.exists() and i.exists():
            rows.append((rel, "eliminado"))
        elif not i.exists():
            rows.append((rel, "nuevo"))
        elif normalized(m) != normalized(i):
            rows.append((rel, "cambiado"))
        else:
            rows.append((rel, "igual"))
    return rows


def render_report(master_v: str, instance_v: str, rows: list[tuple[str, str]]) -> str:
    counts = {"nuevo": 0, "cambiado": 0, "igual": 0, "eliminado": 0}
    for _, status in rows:
        counts[status] = counts.get(status, 0) + 1
    action = {
        "nuevo": "anadir a la instancia (decision de adopcion)",
        "cambiado": "revisar delta y decidir adopcion",
        "igual": "sin accion",
        "eliminado": "revisar remocion del master y decidir retirada",
    }
    lines = [
        "# Reporte de adopcion asistida",
        "",
        f"- Version de la instancia: `{instance_v}`",
        f"- Version del master: `{master_v}`",
        f"- Conjunto adoptable: {len(rows)} archivos "
        f"(nuevo={counts['nuevo']}, cambiado={counts['cambiado']}, "
        f"igual={counts['igual']}, eliminado={counts['eliminado']})",
        "",
        "> La herramienta informa; la instancia adopta por decision (DECISION-0001). No se modifico nada.",
        "",
        "| Archivo | Estado | Accion recomendada |",
        "|---------|--------|--------------------|",
    ]
    for rel, status in rows:
        if status == "igual":
            continue
        lines.append(f"| `{rel}` | {status} | {action[status]} |")
    if counts["nuevo"] == 0 and counts["cambiado"] == 0 and counts["eliminado"] == 0:
        lines.append("| (ninguno) | igual | la instancia esta al dia |")
    return "\n".join(lines) + "\n"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Reporte de adopcion asistida entre versiones.")
    parser.add_argument("--instance", required=True, help="Ruta a la instancia a comparar.")
    parser.add_argument("--master", default=None, help="Ruta al master del protocolo (def: raiz del repo del script).")
    parser.add_argument("--report", default=None, help="Archivo donde escribir el reporte (def: stdout).")
    args = parser.parse_args(argv)

    instance = Path(args.instance).resolve()
    master = Path(args.master).resolve() if args.master else Path(__file__).resolve().parent.parent
    if not instance.is_dir():
        print(f"ERROR: instancia no encontrada: {instance}", file=sys.stderr)
        return 2
    if not master.is_dir():
        print(f"ERROR: master no encontrado: {master}", file=sys.stderr)
        return 2

    master_v = read_protocol_version(master)
    instance_v = read_protocol_version(instance)
    globs = adoptable_globs(master)
    rel_files = collect_files(master, globs) | collect_files(instance, globs)
    rows = classify(master, instance, rel_files)
    report = render_report(master_v, instance_v, rows)

    if args.report:
        Path(args.report).write_text(report, encoding="utf-8")
        print(f"OK: reporte escrito en {args.report}")
    else:
        print(report, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
