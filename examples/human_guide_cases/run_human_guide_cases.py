#!/usr/bin/env python3
"""Golden cases for the deterministic human guide generator."""

from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "scripts" / "generate_human_guide.py"
PS_SCRIPT = ROOT / "scripts" / "generate_human_guide.ps1"
SECTION_TITLES = (
    (1, "Identidad de la instancia"),
    (2, "Que es esta instancia"),
    (3, "Que hace"),
    (4, "Como lo hace"),
    (5, "Arquitectura"),
    (6, "Componentes principales"),
    (7, "Flujo operativo"),
    (8, "Flujo de datos"),
    (9, "Flujo de decisiones"),
    (10, "Como se implementa la metodologia aqui"),
    (11, "Como se construye"),
    (12, "Como se ejecuta localmente"),
    (13, "Como se prueba"),
    (14, "Como se despliega o lanza"),
    (15, "Como se opera"),
    (16, "Troubleshooting"),
    (17, "Rutas relevantes del protocolo"),
    (18, "Roles y capacidades configuradas"),
    (19, "Seguridad y datos sensibles"),
    (20, "Continuidad, traspaso y recuperacion de contexto"),
    (21, "Historial de cambios"),
)

sys.path.insert(0, str(ROOT))
from runtime.temp_paths import root_temp_dir  # noqa: E402


def run_command(command: list[str], *, expect_success: bool = True) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(command, cwd=ROOT, text=True, encoding="utf-8", capture_output=True)
    if expect_success and result.returncode != 0:
        raise AssertionError(
            f"command failed unexpectedly ({result.returncode}): {' '.join(command)}\n"
            f"STDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}"
        )
    if not expect_success and result.returncode == 0:
        raise AssertionError(f"command succeeded unexpectedly: {' '.join(command)}\n{result.stdout}")
    return result


def ps_command() -> list[str] | None:
    executable = shutil.which("pwsh") or shutil.which("powershell")
    if not executable:
        return None
    args = [executable, "-NoProfile"]
    if Path(executable).name.lower().startswith("powershell"):
        args += ["-ExecutionPolicy", "Bypass"]
    return args + ["-File", str(PS_SCRIPT)]


def frontmatter(kind: str, adoption_tier: str) -> str:
    if kind == "template":
        return """---
nombre: <NOMBRE_DE_LA_INSTANCIA>
estado: <activo | en-pausa | archivado>
protocol_version: <X.Y.Z>
runtime_version: <X.Y.Z | no-aplica>
adoption_tier: <coordination | runtime>
perfiles: [<perfil-1>, <perfil-2>]
idioma: <es | en | ...>
actualizado: <YYYY-MM-DD>
---"""
    return f"""---
nombre: Instancia de ejemplo neutral
estado: activo
protocol_version: 1.0.0
runtime_version: 1.0.0
adoption_tier: {adoption_tier}
perfiles: [base]
idioma: es
actualizado: 2026-06-10
---"""


def section_content(number: int, kind: str, *, placeholder: bool) -> str:
    if kind in {"template", "example"}:
        return f"<Contenido de la seccion {number}>"
    if placeholder and number == 1:
        return "<PENDIENTE>"
    if number in {11, 12}:
        return "```text\npython -m ejemplo\n```"
    if number == 13:
        return "Pruebas deterministas.\n\n- [ ] Ejecutar el gate principal\n- [x] Revisar el resultado"
    if number == 16:
        return "| Sintoma | Causa probable | Remedio |\n|---|---|---|\n| Falla | Configuracion | Revisar el gate |"
    if number == 19:
        return "> [SEGURIDAD] No guardar secretos en el repositorio.\n\nPolitica local documentada."
    return f"Contenido completo de la seccion {number} para una guia viva sin pendientes."


def build_markdown(
    *,
    kind: str = "live",
    adoption_tier: str = "runtime",
    omit_section: int | None = None,
    placeholder: bool = False,
    runtime_section: bool = False,
) -> str:
    lines = [
        frontmatter(kind, adoption_tier),
        "",
        "# Guia humana operativa - Instancia de ejemplo neutral",
        "",
        "> Panorama de una instancia neutral para pruebas deterministas.",
        "",
        "- **Instancia:** Instancia de ejemplo neutral",
        "- **Fuente de verdad:** este `.md`.",
        "",
    ]
    for number, title in SECTION_TITLES:
        if number == omit_section:
            continue
        tier = "runtime" if runtime_section and number == 15 else "todos"
        field = "opcional" if number == 14 else "obligatorio"
        if tier == "runtime":
            field = "obligatorio"
        lines.extend(
            [
                f"## {number}. {title}",
                f"<!-- origen: INSTANCIA | tier: {tier} | campo: {field} -->",
                "",
                section_content(number, kind, placeholder=placeholder),
                "",
            ]
        )
    return "\n".join(lines)


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")


def run_generator(input_path: Path, output_path: Path, *, kind: str) -> None:
    run_command(
        [
            sys.executable,
            str(SCRIPT),
            "--root",
            str(ROOT),
            "--in",
            str(input_path),
            "--out",
            str(output_path),
            "--kind",
            kind,
        ]
    )


def run_check(input_path: Path, output_path: Path, *, kind: str, expect_success: bool = True) -> None:
    run_command(
        [
            sys.executable,
            str(SCRIPT),
            "--root",
            str(ROOT),
            "--in",
            str(input_path),
            "--out",
            str(output_path),
            "--kind",
            kind,
            "--check",
        ],
        expect_success=expect_success,
    )


def run_report(input_path: Path, output_path: Path) -> None:
    run_command(
        [
            sys.executable,
            str(SCRIPT),
            "--root",
            str(ROOT),
            "--mode",
            "report",
            "--updated",
            "2026-06-29T12:34:56Z",
            "--in",
            str(input_path),
            "--out",
            str(output_path),
        ]
    )


def main() -> int:
    with root_temp_dir(ROOT, ".human-guide-cases-") as temp_root:
        live_md = temp_root / "HUMAN_GUIDE.md"
        live_a = temp_root / "HUMAN_GUIDE-a.html"
        live_b = temp_root / "HUMAN_GUIDE-b.html"
        write(live_md, build_markdown())

        run_generator(live_md, live_a, kind="live")
        run_generator(live_md, live_b, kind="live")
        if live_a.read_bytes() != live_b.read_bytes():
            raise AssertionError("same markdown did not produce byte-identical HTML")
        run_check(live_md, live_a, kind="live")

        live_a.write_text(live_a.read_text(encoding="utf-8") + "\n<!-- drift -->\n", encoding="utf-8")
        run_check(live_md, live_a, kind="live", expect_success=False)

        missing_md = temp_root / "missing-section.md"
        write(missing_md, build_markdown(omit_section=21))
        run_command(
            [sys.executable, str(SCRIPT), "--root", str(ROOT), "--in", str(missing_md), "--kind", "live"],
            expect_success=False,
        )

        placeholder_md = temp_root / "placeholder-live.md"
        write(placeholder_md, build_markdown(placeholder=True))
        run_command(
            [sys.executable, str(SCRIPT), "--root", str(ROOT), "--in", str(placeholder_md), "--kind", "live"],
            expect_success=False,
        )

        template_md = temp_root / "HUMAN_GUIDE.template.md"
        template_html = temp_root / "HUMAN_GUIDE.template.html"
        write(template_md, build_markdown(kind="template"))
        run_generator(template_md, template_html, kind="template")
        run_check(template_md, template_html, kind="template")

        example_md = temp_root / "HUMAN_GUIDE.example.md"
        example_html = temp_root / "HUMAN_GUIDE.example.html"
        write(example_md, build_markdown(kind="example"))
        run_generator(example_md, example_html, kind="example")

        coordination_md = temp_root / "coordination-runtime-section.md"
        coordination_html = temp_root / "coordination-runtime-section.html"
        write(coordination_md, build_markdown(adoption_tier="coordination", runtime_section=True))
        run_generator(coordination_md, coordination_html, kind="live")
        coordination_text = coordination_html.read_text(encoding="utf-8")
        if "coordination tier" not in coordination_text or "no-aplica" not in coordination_text:
            raise AssertionError("coordination tier did not mark runtime section as no-aplica")

        ps = ps_command()
        if ps is not None:
            ps_html = temp_root / "HUMAN_GUIDE-ps.html"
            run_command(
                ps
                + [
                    "-InputPath",
                    str(live_md),
                    "-OutputPath",
                    str(ps_html),
                    "-Root",
                    str(ROOT),
                    "-Kind",
                    "live",
                ]
            )
            run_generator(live_md, live_b, kind="live")
            if ps_html.read_bytes() != live_b.read_bytes():
                raise AssertionError("PowerShell wrapper output differs from Python output")

        report_md = temp_root / "REPORT.md"
        report_out = temp_root / "REPORT.out.md"
        write(
            report_md,
            "# Reporte humano - ejemplo\n\n"
            "- **Fecha:** 2026-06-29\n"
            "- **Dataset actualizado:** 1/500 stale.\n\n"
            "## Resultado\n\n"
            "Contenido.\n",
        )
        run_report(report_md, report_out)
        report_text = report_out.read_text(encoding="utf-8")
        if "- **Fecha:**" in report_text:
            raise AssertionError("stale date-only report metadata was not removed")
        if "- **Updated:** 2026-06-29T12:34:56Z" not in report_text:
            raise AssertionError("report updated timestamp with time was not injected")
        if "Dataset actualizado:" not in report_text or "/500 elegibles" not in report_text:
            raise AssertionError("dataset X/500 status was not injected")
        if "Arquitecto:" not in report_text or "Codex:" not in report_text:
            raise AssertionError("dataset per-agent breakdown was not injected")

        print("OK: human guide generator cases passed.")
        return 0


if __name__ == "__main__":
    raise SystemExit(main())
