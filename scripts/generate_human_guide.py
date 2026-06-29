#!/usr/bin/env python3
"""Generate deterministic self-contained HTML for HUMAN_GUIDE markdown files."""

from __future__ import annotations

import argparse
import hashlib
import html
import json
import re
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable


SECTION_TITLES: tuple[tuple[int, str], ...] = (
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
REQUIRED_FRONTMATTER = (
    "nombre",
    "estado",
    "protocol_version",
    "runtime_version",
    "adoption_tier",
    "perfiles",
    "idioma",
    "actualizado",
)
VALID_ADOPTION_TIERS = {"coordination", "runtime"}
DATASET_TARGET = 500
DATASET_MIN_SEQ = 2221

SECTION_RE = re.compile(r"^##\s+(\d+)\.\s+(.+?)\s*$")
META_RE = re.compile(
    r"^<!--\s*origen:\s*(?P<origin>[^|]+?)\s*\|\s*tier:\s*(?P<tier>[^|]+?)\s*\|\s*campo:\s*(?P<field>.*?)\s*-->\s*$",
    re.IGNORECASE,
)
PLACEHOLDER_RE = re.compile(r"<([^>\n]+)>")
INLINE_CODE_RE = re.compile(r"`[^`\n]+`")
HTML_COMMENT_RE = re.compile(r"<!--.*?-->", re.DOTALL)


class GuideError(RuntimeError):
    """Base error for guide generation."""


class GuideValidationError(GuideError):
    """Raised when the markdown does not match the guide schema."""


@dataclass(frozen=True)
class SectionMeta:
    origin: str
    tier: str
    field: str


@dataclass(frozen=True)
class Section:
    number: int
    title: str
    meta: SectionMeta
    content_lines: tuple[str, ...]
    heading_line: int
    meta_line: int


@dataclass(frozen=True)
class GuideDocument:
    source_text: str
    frontmatter: dict[str, object]
    body: str
    title: str
    panorama: str
    sections: tuple[Section, ...]
    adoption_tier: str
    kind: str


def normalize_newlines(text: str) -> str:
    return text.replace("\r\n", "\n").replace("\r", "\n")


def parse_frontmatter_value(value: str) -> object:
    stripped = value.strip()
    if stripped.startswith("[") and stripped.endswith("]"):
        inner = stripped[1:-1].strip()
        if not inner:
            return []
        return [item.strip().strip("'\"") for item in inner.split(",")]
    return stripped.strip("'\"")


def split_frontmatter(text: str) -> tuple[str, str]:
    lines = text.split("\n")
    if not lines or lines[0].strip() != "---":
        raise GuideValidationError("frontmatter is required and must start with ---")
    for index in range(1, len(lines)):
        if lines[index].strip() == "---":
            return "\n".join(lines[1:index]), "\n".join(lines[index + 1 :])
    raise GuideValidationError("frontmatter closing --- not found")


def parse_frontmatter(text: str) -> dict[str, object]:
    result: dict[str, object] = {}
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        key = key.strip()
        if key:
            result[key] = parse_frontmatter_value(value)
    return result


def normalize_token(value: object) -> str:
    if isinstance(value, list):
        return ", ".join(str(item).strip() for item in value if str(item).strip())
    return str(value or "").strip()


def parse_meta(line: str, line_number: int) -> SectionMeta:
    match = META_RE.match(line.strip())
    if not match:
        raise GuideValidationError(
            f"section metadata expected at line {line_number}: "
            "<!-- origen: ... | tier: ... | campo: ... -->"
        )
    return SectionMeta(
        origin=match.group("origin").strip(),
        tier=match.group("tier").strip(),
        field=match.group("field").strip(),
    )


def parse_sections(body: str) -> tuple[Section, ...]:
    lines = body.splitlines()
    headings: list[tuple[int, re.Match[str]]] = []
    for index, line in enumerate(lines):
        match = SECTION_RE.match(line)
        if match:
            headings.append((index, match))

    sections: list[Section] = []
    for position, (heading_index, match) in enumerate(headings):
        end_index = headings[position + 1][0] if position + 1 < len(headings) else len(lines)
        section_lines = lines[heading_index + 1 : end_index]
        meta_offset = None
        for offset, line in enumerate(section_lines):
            if line.strip():
                meta_offset = offset
                break
        if meta_offset is None:
            raise GuideValidationError(f"section {match.group(1)} has no metadata line")
        meta_line_number = heading_index + 2 + meta_offset
        meta = parse_meta(section_lines[meta_offset], meta_line_number)
        content = tuple(section_lines[meta_offset + 1 :])
        sections.append(
            Section(
                number=int(match.group(1)),
                title=match.group(2).strip(),
                meta=meta,
                content_lines=content,
                heading_line=heading_index + 1,
                meta_line=meta_line_number,
            )
        )
    return tuple(sections)


def extract_title_and_panorama(body: str) -> tuple[str, str]:
    lines = body.splitlines()
    title = "Guia humana operativa"
    h1_index = 0
    for index, line in enumerate(lines):
        if line.startswith("# "):
            title = line[2:].strip() or title
            h1_index = index
            break

    panorama_lines: list[str] = []
    in_quote = False
    for line in lines[h1_index + 1 :]:
        if line.startswith("## "):
            break
        stripped = line.strip()
        if stripped.startswith(">"):
            in_quote = True
            panorama_lines.append(stripped[1:].strip())
            continue
        if in_quote:
            if not stripped:
                break
            if stripped.startswith(">"):
                panorama_lines.append(stripped[1:].strip())
                continue
            break
    panorama = " ".join(item for item in panorama_lines if item).strip()
    return title, panorama


def load_config_tier(root: Path) -> str | None:
    config_path = root / "protocol.config.json"
    if not config_path.exists():
        return None
    try:
        config = json.loads(config_path.read_text(encoding="utf-8-sig"))
    except (OSError, json.JSONDecodeError):
        return None
    tier = str(config.get("adoption_tier") or "").strip().lower()
    return tier if tier in VALID_ADOPTION_TIERS else None


def detect_kind(path: Path, explicit: str) -> str:
    if explicit != "auto":
        return explicit
    name = path.name.lower()
    parts = {part.lower() for part in path.parts}
    if ".template." in name or name.endswith(".template.md"):
        return "template"
    if ".example." in name or "examples" in parts:
        return "example"
    return "live"


def resolve_adoption_tier(frontmatter: dict[str, object], root: Path) -> str:
    frontmatter_tier = normalize_token(frontmatter.get("adoption_tier")).lower()
    if frontmatter_tier in VALID_ADOPTION_TIERS:
        return frontmatter_tier
    config_tier = load_config_tier(root)
    if config_tier:
        return config_tier
    return "coordination"


def parse_document(path: Path, *, root: Path, kind: str) -> GuideDocument:
    source_text = normalize_newlines(path.read_text(encoding="utf-8-sig"))
    frontmatter_text, body = split_frontmatter(source_text)
    frontmatter = parse_frontmatter(frontmatter_text)
    title, panorama = extract_title_and_panorama(body)
    detected_kind = detect_kind(path, kind)
    document = GuideDocument(
        source_text=source_text,
        frontmatter=frontmatter,
        body=body,
        title=title,
        panorama=panorama,
        sections=parse_sections(body),
        adoption_tier=resolve_adoption_tier(frontmatter, root),
        kind=detected_kind,
    )
    validate_document(document)
    return document


def field_kind(value: str) -> str:
    normalized = value.split(":", 1)[0].strip().lower()
    if normalized in {"obligatorio", "opcional", "no-aplica"}:
        return normalized
    return "opcional"


def effective_field(section: Section, adoption_tier: str) -> tuple[str, str | None]:
    tier = section.meta.tier.strip().lower()
    if tier == "runtime" and adoption_tier == "coordination":
        return "no-aplica", "coordination tier"
    return field_kind(section.meta.field), None


def strip_for_placeholder_scan(text: str) -> str:
    without_comments = HTML_COMMENT_RE.sub(" ", text)
    return INLINE_CODE_RE.sub(" ", without_comments)


def placeholder_findings(text: str) -> list[str]:
    clean = strip_for_placeholder_scan(text)
    findings: list[str] = []
    for match in PLACEHOLDER_RE.finditer(clean):
        value = match.group(1).strip()
        if value.lower().startswith(("http://", "https://", "mailto:")):
            continue
        findings.append(match.group(0))
    return findings


def section_has_content(section: Section) -> bool:
    return bool("\n".join(section.content_lines).strip())


def validate_document(document: GuideDocument) -> None:
    errors: list[str] = []

    for key in REQUIRED_FRONTMATTER:
        if key not in document.frontmatter or not normalize_token(document.frontmatter.get(key)):
            errors.append(f"missing frontmatter field: {key}")

    expected_numbers = [number for number, _ in SECTION_TITLES]
    found_numbers = [section.number for section in document.sections]
    if found_numbers != expected_numbers:
        missing = [str(number) for number in expected_numbers if number not in found_numbers]
        extras = [str(number) for number in found_numbers if number not in expected_numbers]
        if missing:
            errors.append(f"missing required sections: {', '.join(missing)}")
        if extras:
            errors.append(f"unexpected sections: {', '.join(extras)}")
        if not missing and not extras:
            errors.append("sections are not in canonical order")

    expected_titles = dict(SECTION_TITLES)
    for section in document.sections:
        expected_title = expected_titles.get(section.number)
        if expected_title and section.title != expected_title:
            errors.append(
                f"section {section.number} title mismatch: expected {expected_title!r}, got {section.title!r}"
            )

    if document.adoption_tier not in VALID_ADOPTION_TIERS:
        errors.append(f"invalid adoption_tier: {document.adoption_tier}")

    if document.kind == "live":
        placeholders = placeholder_findings(document.source_text)
        if placeholders:
            sample = ", ".join(sorted(set(placeholders))[:5])
            errors.append(f"live guide contains placeholder(s): {sample}")
        for key in REQUIRED_FRONTMATTER:
            placeholders = placeholder_findings(normalize_token(document.frontmatter.get(key)))
            if placeholders:
                errors.append(f"live frontmatter field contains placeholder: {key}")
        for section in document.sections:
            effective, _ = effective_field(section, document.adoption_tier)
            if effective == "obligatorio" and not section_has_content(section):
                errors.append(f"section {section.number} is mandatory but empty")
            if (
                section.meta.tier.strip().lower() == "runtime"
                and document.adoption_tier == "runtime"
                and not section_has_content(section)
            ):
                errors.append(f"section {section.number} is required for runtime tier but empty")

    if errors:
        raise GuideValidationError("\n".join(f"- {item}" for item in errors))


def slug_for(section: Section) -> str:
    base = f"{section.number}-{section.title}".lower()
    normalized = re.sub(r"[^a-z0-9]+", "-", base).strip("-")
    return normalized or f"section-{section.number}"


def esc(value: object) -> str:
    return html.escape(normalize_token(value), quote=True)


def render_inline(text: str) -> str:
    parts = text.split("`")
    rendered: list[str] = []
    for index, part in enumerate(parts):
        if index % 2:
            rendered.append(f"<code>{html.escape(part, quote=False)}</code>")
            continue
        escaped = html.escape(part, quote=False)
        escaped = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", escaped)
        rendered.append(escaped)
    return "".join(rendered)


def split_table_row(line: str) -> list[str]:
    stripped = line.strip()
    if stripped.startswith("|"):
        stripped = stripped[1:]
    if stripped.endswith("|"):
        stripped = stripped[:-1]
    return [cell.strip() for cell in stripped.split("|")]


def is_table_separator(line: str) -> bool:
    cells = split_table_row(line)
    return bool(cells) and all(re.fullmatch(r":?-{3,}:?", cell.strip()) for cell in cells)


def is_block_start(lines: list[str], index: int) -> bool:
    stripped = lines[index].strip()
    if not stripped:
        return True
    if stripped.startswith("```") or stripped.startswith(">") or stripped.startswith("|"):
        return True
    if re.match(r"^\s*-\s+(\[[ xX]\]\s+)?", lines[index]):
        return True
    if re.match(r"^#{3,6}\s+", stripped):
        return True
    return False


def render_table(lines: list[str], start: int) -> tuple[str, int]:
    header = split_table_row(lines[start])
    index = start + 2
    rows: list[list[str]] = []
    while index < len(lines) and lines[index].strip().startswith("|"):
        rows.append(split_table_row(lines[index]))
        index += 1
    out = ["<table>", "<thead><tr>"]
    out.extend(f"<th>{render_inline(cell)}</th>" for cell in header)
    out.append("</tr></thead>")
    out.append("<tbody>")
    for row in rows:
        out.append("<tr>")
        out.extend(f"<td>{render_inline(cell)}</td>" for cell in row)
        out.append("</tr>")
    out.append("</tbody></table>")
    return "\n".join(out), index


def render_code_block(lines: list[str], start: int) -> tuple[str, int]:
    fence = lines[start].strip()
    language = fence[3:].strip() or "text"
    index = start + 1
    code_lines: list[str] = []
    while index < len(lines):
        if lines[index].strip().startswith("```"):
            index += 1
            break
        code_lines.append(lines[index])
        index += 1
    code = html.escape("\n".join(code_lines), quote=False)
    language_class = re.sub(r"[^a-zA-Z0-9_-]", "", language) or "text"
    return f'<pre><code class="language-{language_class}">{code}</code></pre>', index


def render_quote(lines: list[str], start: int) -> tuple[str, int]:
    index = start
    quote_lines: list[str] = []
    while index < len(lines) and lines[index].strip().startswith(">"):
        quote_lines.append(lines[index].strip()[1:].strip())
        index += 1
    text = " ".join(item for item in quote_lines if item)
    if text.startswith("[SEGURIDAD]"):
        text = text[len("[SEGURIDAD]") :].strip()
        return (
            '<div class="callout safety"><div class="callout-title">SEGURIDAD</div>'
            f"<p>{render_inline(text)}</p></div>",
            index,
        )
    return f"<blockquote>{render_inline(text)}</blockquote>", index


def render_list(lines: list[str], start: int) -> tuple[str, int]:
    index = start
    items: list[str] = []
    while index < len(lines):
        checklist = re.match(r"^\s*-\s+\[([ xX])\]\s+(.*)$", lines[index])
        bullet = re.match(r"^\s*-\s+(.*)$", lines[index])
        if checklist:
            checked = checklist.group(1).lower() == "x"
            attr = " checked" if checked else ""
            text = render_inline(checklist.group(2).strip())
            items.append(f'<li class="check"><input type="checkbox" disabled{attr}> <span>{text}</span></li>')
        elif bullet:
            items.append(f"<li>{render_inline(bullet.group(1).strip())}</li>")
        else:
            break
        index += 1
    return "<ul>\n" + "\n".join(items) + "\n</ul>", index


def render_heading(line: str) -> str:
    level = len(line) - len(line.lstrip("#"))
    level = min(max(level, 3), 6)
    text = line[level:].strip()
    return f"<h{level}>{render_inline(text)}</h{level}>"


def render_paragraph(lines: list[str], start: int) -> tuple[str, int]:
    index = start
    paragraph: list[str] = []
    while index < len(lines) and not is_block_start(lines, index):
        paragraph.append(lines[index].strip())
        index += 1
    text = " ".join(item for item in paragraph if item).strip()
    return f"<p>{render_inline(text)}</p>", index


def render_blocks(lines: Iterable[str]) -> str:
    materialized = list(lines)
    rendered: list[str] = []
    index = 0
    while index < len(materialized):
        stripped = materialized[index].strip()
        if not stripped:
            index += 1
            continue
        if stripped.startswith("```"):
            block, index = render_code_block(materialized, index)
        elif stripped.startswith(">"):
            block, index = render_quote(materialized, index)
        elif (
            stripped.startswith("|")
            and index + 1 < len(materialized)
            and is_table_separator(materialized[index + 1])
        ):
            block, index = render_table(materialized, index)
        elif re.match(r"^\s*-\s+(\[[ xX]\]\s+)?", materialized[index]):
            block, index = render_list(materialized, index)
        elif re.match(r"^#{3,6}\s+", stripped):
            block = render_heading(stripped)
            index += 1
        else:
            block, index = render_paragraph(materialized, index)
        rendered.append(block)
    return "\n".join(rendered)


def css() -> str:
    return """  :root{
    --bg:#101418; --panel:#172028; --panel2:#1f2a33; --ink:#e9eef4; --muted:#9aa8b6;
    --line:#2d3a45; --accent:#56a6ff; --ok:#3fb950; --warn:#d29922; --danger:#f85149;
    --chip:#253340; --paper:#f7f8fa; --paper-ink:#20262d;
  }
  *{box-sizing:border-box}
  html{scroll-behavior:smooth}
  body{margin:0;background:var(--bg);color:var(--ink);
    font:15px/1.6 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;}
  .wrap{max-width:1120px;margin:0 auto;padding:28px 22px 80px}
  header{border-bottom:1px solid var(--line);padding-bottom:20px}
  .generated{display:inline-block;border:1px solid rgba(86,166,255,.45);background:rgba(86,166,255,.12);
    color:#b9ddff;border-radius:6px;padding:4px 9px;font-size:12px;font-weight:700;letter-spacing:.04em}
  h1{font-size:28px;line-height:1.18;margin:14px 0 8px;letter-spacing:0}
  h2{font-size:20px;margin:0}
  h3{font-size:16px;margin:18px 0 8px}
  p{margin:10px 0}
  a{color:#9ed0ff}
  code{background:#0b0f14;border:1px solid var(--line);border-radius:4px;padding:1px 5px;
    font-family:SFMono-Regular,Consolas,"Liberation Mono",monospace;font-size:12.5px;color:#d8e6f3}
  pre{overflow:auto;background:#0b0f14;border:1px solid var(--line);border-radius:8px;padding:13px 15px}
  pre code{background:transparent;border:0;padding:0}
  .sub{color:var(--muted);font-size:13.5px}
  .meta{display:flex;flex-wrap:wrap;gap:8px;margin-top:14px}
  .chip,.badge{display:inline-flex;align-items:center;border:1px solid var(--line);background:var(--chip);
    border-radius:6px;padding:3px 9px;color:var(--muted);font-size:12.5px;white-space:nowrap}
  .chip b{color:var(--ink);font-weight:650;margin-left:4px}
  .badge.required{color:#d8f5df;border-color:rgba(63,185,80,.4);background:rgba(63,185,80,.14)}
  .badge.optional{color:#ffe2a3;border-color:rgba(210,153,34,.42);background:rgba(210,153,34,.14)}
  .badge.na{color:#c7d0d9;border-color:rgba(154,168,182,.35);background:rgba(154,168,182,.1)}
  .panorama{margin:22px 0;border-left:4px solid var(--accent);background:var(--panel);
    border-radius:8px;padding:16px 18px;color:#d4e1ed}
  .layout{display:grid;grid-template-columns:280px minmax(0,1fr);gap:24px;margin-top:24px}
  nav{position:sticky;top:16px;align-self:start;border:1px solid var(--line);background:var(--panel);
    border-radius:8px;padding:14px}
  nav h2{font-size:14px;text-transform:uppercase;color:var(--muted);letter-spacing:.05em;margin-bottom:8px}
  nav ol{margin:0;padding-left:24px}
  nav li{margin:7px 0;color:var(--muted)}
  nav a{color:var(--ink);text-decoration:none}
  nav a:hover{text-decoration:underline}
  section{border-top:1px solid var(--line);padding:24px 0}
  .section-head{display:flex;align-items:flex-start;justify-content:space-between;gap:16px;margin-bottom:8px}
  .section-meta{display:flex;gap:6px;flex-wrap:wrap;margin:4px 0 12px}
  blockquote{margin:14px 0;border-left:3px solid var(--accent);padding:5px 0 5px 14px;color:#cbd8e4}
  .callout{border:1px solid rgba(248,81,73,.38);border-left:4px solid var(--danger);border-radius:8px;
    padding:12px 14px;background:rgba(248,81,73,.10);margin:14px 0}
  .callout-title{font-weight:750;color:#ffb4ae;font-size:12px;letter-spacing:.05em;margin-bottom:4px}
  ul{padding-left:24px}
  li{margin:6px 0}
  li.check{list-style:none;margin-left:-22px;display:flex;gap:8px;align-items:flex-start}
  li.check input{margin-top:4px}
  table{width:100%;border-collapse:collapse;margin:12px 0;font-size:13.8px}
  th,td{text-align:left;vertical-align:top;padding:8px 10px;border-bottom:1px solid var(--line)}
  th{background:var(--panel2);color:var(--muted);font-weight:650}
  footer{margin-top:42px;border-top:1px solid var(--line);padding-top:14px;color:var(--muted);font-size:12.5px}
  @media (max-width: 860px){
    .layout{grid-template-columns:1fr}
    nav{position:static}
    .section-head{display:block}
  }
  @media print{
    body{background:#fff;color:var(--paper-ink);font-size:12px}
    .wrap{max-width:none;padding:0}
    nav{display:none}
    header,section,footer{border-color:#c9d1d9}
    .panorama,section{break-inside:avoid}
    code,pre{background:#f0f3f6;color:#111;border-color:#c9d1d9}
    .chip,.badge{border-color:#c9d1d9;background:#fff;color:#333}
    a{color:#111;text-decoration:none}
  }"""


def badge_class(field: str) -> str:
    if field == "obligatorio":
        return "required"
    if field == "no-aplica":
        return "na"
    return "optional"


def display_frontmatter(document: GuideDocument, key: str, fallback: str = "no-aplica") -> str:
    value = normalize_token(document.frontmatter.get(key))
    return value or fallback


def render_toc(document: GuideDocument) -> str:
    out = ["<nav aria-label=\"Indice\">", "<h2>Indice</h2>", "<ol>"]
    for section in document.sections:
        effective, note = effective_field(section, document.adoption_tier)
        title = html.escape(section.title)
        suffix = f" ({html.escape(note)})" if note else ""
        out.append(
            f'<li><a href="#{slug_for(section)}">{section.number}. {title}</a> '
            f'<span class="badge {badge_class(effective)}">{html.escape(effective)}{suffix}</span></li>'
        )
    out.extend(["</ol>", "</nav>"])
    return "\n".join(out)


def render_section(section: Section, adoption_tier: str) -> str:
    effective, note = effective_field(section, adoption_tier)
    badges = [
        f'<span class="badge">{html.escape(section.meta.origin)}</span>',
        f'<span class="badge">{html.escape(section.meta.tier)}</span>',
        f'<span class="badge {badge_class(effective)}">{html.escape(effective)}</span>',
    ]
    if note:
        badges.append(f'<span class="badge na">{html.escape(note)}</span>')
    body = render_blocks(section.content_lines)
    if not body.strip() and effective == "no-aplica":
        body = "<p>No aplica para este tier.</p>"
    elif not body.strip():
        body = "<p><em>Sin contenido.</em></p>"
    meta_comment = (
        f"<!-- origen: {section.meta.origin} | tier: {section.meta.tier} | campo: {section.meta.field} -->"
    )
    return "\n".join(
        [
            meta_comment,
            f'<section id="{slug_for(section)}">',
            '<div class="section-head">',
            f"<h2>{section.number}. {html.escape(section.title)}</h2>",
            "</div>",
            f'<div class="section-meta">{" ".join(badges)}</div>',
            body,
            "</section>",
        ]
    )


def render_html(document: GuideDocument) -> str:
    source_hash = hashlib.sha256(document.source_text.encode("utf-8")).hexdigest()[:16]
    language = display_frontmatter(document, "idioma", "es").split("|", 1)[0].strip("<> ") or "es"
    page_title = display_frontmatter(document, "nombre", document.title)
    perfiles = display_frontmatter(document, "perfiles", "no-aplica")
    panorama = document.panorama or "Panorama no informado."
    sections = "\n".join(render_section(section, document.adoption_tier) for section in document.sections)
    content = f"""<!DOCTYPE html>
<html lang="{html.escape(language, quote=True)}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(document.title)} - {esc(page_title)}</title>
<style>
{css()}
</style>
</head>
<body>
<div class="wrap">
<header>
  <span class="generated">GENERADO - NO EDITAR</span>
  <h1>{html.escape(document.title)}</h1>
  <div class="sub">HTML autocontenido generado desde el markdown fuente de la guia humana operativa.</div>
  <div class="meta">
    <span class="chip">Instancia <b>{esc(page_title)}</b></span>
    <span class="chip">Estado <b>{esc(display_frontmatter(document, "estado"))}</b></span>
    <span class="chip">Tier <b>{html.escape(document.adoption_tier)}</b></span>
    <span class="chip">Protocol <b>{esc(display_frontmatter(document, "protocol_version"))}</b></span>
    <span class="chip">Runtime <b>{esc(display_frontmatter(document, "runtime_version"))}</b></span>
    <span class="chip">Perfiles <b>{esc(perfiles)}</b></span>
    <span class="chip">Actualizado <b>{esc(display_frontmatter(document, "actualizado"))}</b></span>
  </div>
</header>
<div class="panorama">{render_inline(panorama)}</div>
<div class="layout">
{render_toc(document)}
<main>
{sections}
</main>
</div>
<footer>
  Generado por <code>scripts/generate_human_guide.py</code>. Fuente unica: el archivo <code>.md</code>.
  Hash de fuente: <code>{source_hash}</code>. Sin JavaScript, CDN ni recursos externos.
</footer>
</div>
</body>
</html>
"""
    return content.replace("\r\n", "\n")


def default_output_path(input_path: Path) -> Path:
    if input_path.name.endswith(".md"):
        return input_path.with_suffix(".html")
    return input_path.with_name(input_path.name + ".html")


def generate(input_path: Path, *, root: Path, kind: str) -> str:
    document = parse_document(input_path, root=root, kind=kind)
    return render_html(document)


def utc_timestamp() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def dataset_status(root: Path) -> tuple[int, dict[str, int]]:
    events_path = root / "runtime" / "state" / "events.jsonl"
    counts: dict[str, int] = {}
    if not events_path.exists():
        return 0, counts
    for line in events_path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            continue
        if int(event.get("seq") or 0) < DATASET_MIN_SEQ:
            continue
        if event.get("type") != "intent.applied" or event.get("applied") is not True:
            continue
        actor_auth = event.get("actor_auth")
        if not isinstance(actor_auth, dict) or actor_auth.get("method") != "ed25519":
            continue
        actor = str(event.get("actor") or "unknown").strip() or "unknown"
        counts[actor] = counts.get(actor, 0) + 1
    return sum(counts.values()), dict(sorted(counts.items()))


def dataset_status_line(root: Path) -> str:
    total, counts = dataset_status(root)
    breakdown = ", ".join(f"{actor}: {count}" for actor, count in counts.items()) or "sin eventos elegibles"
    return (
        f"- **Dataset actualizado:** {total}/{DATASET_TARGET} elegibles "
        f"(seq>={DATASET_MIN_SEQ} AND intent.applied AND ed25519; {breakdown})."
    )


def inject_report_metadata(text: str, *, updated: str, dataset_line: str) -> str:
    normalized = normalize_newlines(text)
    lines = normalized.split("\n")
    output: list[str] = []
    inserted = False
    skip_next_blank = False
    for line in lines:
        if re.match(r"^-\s+\*\*?(Fecha|Date|Actualizado|Updated|Dataset actualizado|Dataset status):\*\*?", line):
            skip_next_blank = False
            continue
        output.append(line)
        if not inserted and line.startswith("# "):
            output.extend(["", f"- **Updated:** {updated}", dataset_line])
            inserted = True
            skip_next_blank = True
            continue
        if skip_next_blank:
            skip_next_blank = False
    if not inserted:
        output = [f"- **Updated:** {updated}", dataset_line, ""] + output
    return "\n".join(output).rstrip() + "\n"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate deterministic HUMAN_GUIDE HTML.")
    parser.add_argument("--root", default=".", help="Repository or instance root for protocol.config.json fallback.")
    parser.add_argument("--in", dest="input_path", required=True, help="Input HUMAN_GUIDE markdown path.")
    parser.add_argument("--out", dest="output_path", help="Output HTML path. Defaults to input with .html suffix.")
    parser.add_argument("--check", action="store_true", help="Validate and fail if output HTML differs.")
    parser.add_argument(
        "--mode",
        choices=("guide", "report"),
        default="guide",
        help="Generate a human guide HTML or normalize a markdown report header.",
    )
    parser.add_argument("--updated", help="Report updated timestamp. Defaults to current UTC time.")
    parser.add_argument(
        "--kind",
        choices=("auto", "template", "example", "live"),
        default="auto",
        help="Guide kind. Auto uses file name/path.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = Path(args.root).resolve()
    input_path = Path(args.input_path)
    if not input_path.is_absolute():
        input_path = (Path.cwd() / input_path).resolve()
    output_path = Path(args.output_path) if args.output_path else default_output_path(input_path)
    if not output_path.is_absolute():
        output_path = (Path.cwd() / output_path).resolve()

    if args.mode == "report":
        try:
            source = input_path.read_text(encoding="utf-8-sig")
        except OSError as exc:
            print(f"ERROR: cannot read report: {input_path} ({exc})", file=sys.stderr)
            return 1
        updated = args.updated or utc_timestamp()
        rendered = inject_report_metadata(source, updated=updated, dataset_line=dataset_status_line(root))
    else:
        try:
            rendered = generate(input_path, root=root, kind=args.kind)
        except GuideError as exc:
            print(f"ERROR: {exc}", file=sys.stderr)
            return 1

    rendered_bytes = rendered.encode("utf-8")
    if args.check:
        try:
            current = output_path.read_bytes()
        except OSError as exc:
            print(f"ERROR: cannot read output for --check: {output_path} ({exc})", file=sys.stderr)
            return 1
        if current != rendered_bytes:
            print(f"ERROR: generated HTML is out of date: {output_path}", file=sys.stderr)
            return 1
        print(f"OK: {output_path} is up to date.")
        return 0

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_bytes(rendered_bytes)
    print(f"Wrote {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
