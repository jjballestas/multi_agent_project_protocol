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
from pathlib import PurePosixPath

# Criterio adoptable (DISENO-robustez-operacional.md §1.2): masters explicitos y todo
# fichero bajo los arboles de herramientas reutilizables. Los arboles son recursivos por
# definicion: un subdirectorio nuevo de scripts, skills, hooks o runtime tambien se exporta.
# La seleccion puede declararse en protocol.config.json, pero se comprueba contra este
# criterio para que una lista obsoleta falle en vez de omitir carga silenciosamente.
ADOPTABLE_MASTER_FILES = (
    "AGENTS.template.md",
    "CLAUDE.template.md",
    "protocol.config.template.json",
    "Area_comun/README.template.md",
    "Area_comun/state/*.template.json",
    "Area_comun/protocol/*.md",
    "Area_comun/specs/*_TEMPLATE.md",
    "profiles/PROFILE_TEMPLATE/**/*",
    ".github/workflows/validate.yml",
)
ADOPTABLE_RECURSIVE_ROOTS = (
    "scripts",
    "skills",
    ".githooks",
    "runtime",
)
NON_DISTRIBUTABLE_ROOTS = {
    ".agents",
    ".git",
    ".github",
    ".claude",
    ".protocol-tmp",
    "Area_comun",
    "connectors",
    "dist",
    "examples",
    "personal",
    "pre_t0_ledger_seal",
    "profiles",
    "research",
    "secrets",
    "tests",
}
DEFAULT_ADOPTABLE_GLOBS = [
    *ADOPTABLE_MASTER_FILES,
    *(f"{root}/**" for root in ADOPTABLE_RECURSIVE_ROOTS),
]


def read_config(root: Path) -> dict:
    cfg = root / "protocol.config.json"
    if not cfg.is_file():
        return {}
    try:
        return json.loads(cfg.read_text(encoding="utf-8-sig"))
    except (ValueError, OSError):
        return {}


def read_protocol_version(root: Path) -> str:
    data = read_config(root)
    return str(data.get("protocol_version", "unknown"))


def read_runtime_version(root: Path) -> str:
    data = read_config(root)
    return str(data.get("runtime_version", "unknown"))


def adoption_tier(root: Path) -> str:
    tier = str(read_config(root).get("adoption_tier", "coordination") or "coordination")
    return tier if tier in {"coordination", "runtime"} else "coordination"


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


def runtime_tier_path(rel: str) -> bool:
    return rel.startswith("runtime/") or rel == ".github/workflows/validate.yml"


def excluded_runtime_artifact(rel: str) -> bool:
    parts = PurePosixPath(rel).parts
    return (
        rel.startswith("runtime/state/")
        or rel.startswith("runtime/runs/")
        or "__pycache__" in parts
    )


def adoptable_for_instance(rel: str, instance_tier: str) -> bool:
    if excluded_runtime_artifact(rel):
        return False
    if instance_tier != "runtime" and runtime_tier_path(rel):
        return False
    return True


def collect_files(root: Path, globs: list[str]) -> set[str]:
    """Rutas relativas (posix) de los archivos que matchean los globs adoptables."""
    found: set[str] = set()
    for pattern in globs:
        if "**" in pattern:
            base = pattern.split("**", 1)[0].rstrip("/")
            base_path = root / base if base else root
            matches = base_path.rglob("*") if base_path.exists() else []
        else:
            matches = root.glob(pattern)
        for path in matches:
            if path.is_file():
                found.add(path.relative_to(root).as_posix())
    return found


def uncovered_adoptable_files(master: Path, globs: list[str]) -> set[str]:
    """Reusable-tree files required by the criterion but omitted by the effective globs.

    A generic payload is any file below a top-level tree that has not been declared
    instance-only. Root-level protocol masters remain explicit because they mix live and
    template artifacts. This tree rule deliberately ignores names and suffixes: removing an
    entire declared export root (including extensionless hooks) must make the control fail.
    """
    required: set[str] = set()
    for path in master.rglob("*"):
        if not path.is_file():
            continue
        rel_path = path.relative_to(master)
        rel = rel_path.as_posix()
        if len(rel_path.parts) < 2 or rel_path.parts[0] in NON_DISTRIBUTABLE_ROOTS:
            continue
        if not excluded_runtime_artifact(rel):
            required.add(rel)
    return required - collect_files(master, globs)


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


def render_report(
    master_v: str,
    instance_v: str,
    rows: list[tuple[str, str]],
    *,
    instance_tier: str = "coordination",
    master_runtime_v: str = "unknown",
    instance_runtime_v: str = "unknown",
) -> str:
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
        "- Criterio: masters declarados y arboles reutilizables completos bajo "
        "`scripts/`, `skills/`, `.githooks/` y `runtime/`.",
        "- Fuera del conjunto: estado vivo y ejecuciones (`runtime/state/`, `runtime/runs/`), "
        "estado/coordinacion de instancia (`Area_comun/` salvo masters declarados), "
        "`personal/`, `examples/`, `research/`, `connectors/`, `tests/` y artefactos "
        "locales; no son carga generica.",
    ]
    if instance_tier == "runtime":
        lines.extend(
            [
                f"- Adoption tier de la instancia: `{instance_tier}`",
                f"- Runtime version de la instancia: `{instance_runtime_v}`",
                f"- Runtime version del master: `{master_runtime_v}`",
            ]
        )
    lines.extend(
        [
        "",
        "> La herramienta informa; la instancia adopta por decision (DECISION-0001). No se modifico nada.",
        "",
        "| Archivo | Estado | Accion recomendada |",
        "|---------|--------|--------------------|",
        ]
    )
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
    instance_tier = adoption_tier(instance)
    globs = adoptable_globs(master)
    uncovered = uncovered_adoptable_files(master, globs)
    if uncovered:
        print("ERROR: ficheros genericos fuera del conjunto adoptable:", file=sys.stderr)
        for rel in sorted(uncovered):
            print(f"- {rel}", file=sys.stderr)
        return 1
    rel_files = {
        rel
        for rel in collect_files(master, globs) | collect_files(instance, globs)
        if adoptable_for_instance(rel, instance_tier)
    }
    rows = classify(master, instance, rel_files)
    report = render_report(
        master_v,
        instance_v,
        rows,
        instance_tier=instance_tier,
        master_runtime_v=read_runtime_version(master),
        instance_runtime_v=read_runtime_version(instance),
    )

    if args.report:
        Path(args.report).write_text(report, encoding="utf-8")
        print(f"OK: reporte escrito en {args.report}")
    else:
        print(report, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
