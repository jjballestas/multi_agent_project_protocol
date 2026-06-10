---
spec_id: SPEC-0072-guia-humana-operativa-generador-html
task_id: TASK-0037
type: design
status: ready
created_at: 2026-06-10
author: Claude (arquitecto)
linked_decisions: [DECISION-0004, DECISION-0019, DECISION-0001, DECISION-0020, DECISION-0006]
relates_to: [TASK-0037, TASK-0013, TASK-0004]
---

> Diseno tecnico de la guia humana operativa neutral + su render HTML. Cierra TASK-0037 (ultimo
> habilitador documental de ADOPCION). Aditivo, off-by-default, neutral de dominio. NO toca runtime
> ni defaults del template.

# Diseno - Guia humana operativa neutral + generador HTML

## 1. Objetivo

Definir el **contrato minimo de documentacion humana** que toda instancia del protocolo completa para
que cualquier persona (u agente nuevo) entienda, al abrir un solo HTML, que es la instancia, que hace,
como se construye/ejecuta/prueba/despliega/opera, como se diagnostica, donde estan las rutas del
protocolo, que roles/capacidades hay, y como retomar el contexto. El HTML es la vista de lectura; el
**.md estructurado es la unica fuente de verdad**; el HTML es un artefacto de build determinista.

## 2. Alcance

- Un esquema de guia con secciones fijas (sec. 4) y tipos de campo (obligatorio/opcional/no-aplica).
- Un generador determinista `.md -> .html` (sec. 5), stdlib-only, sin red, paridad .py/.ps1.
- Plantilla neutral (master), guia llena de esta instancia (dogfooding), y ejemplo ilustrativo (sec. 6).
- Cableado a los gates existentes (neutralidad, encoding) + un control de drift MD<->HTML (sec. 8).
- Tier-awareness: secciones solo-runtime se marcan "no aplica" en instancias coordination.
- Actualizacion de README_INSTANCIACION.md (sec. 11).

## 3. No-alcance

- NO un conversor CommonMark general; es un renderizador de ESQUEMA conocido.
- NO dependencias externas (pandoc, librerias pip, frameworks JS/CSS, CDN).
- NO reglas de negocio, ni stacks concretos, ni nombres de agentes (Claude/Codex). Solo roles
  genericos: agente operativo, agente revisor, operador humano, runtime, instancia, core, protocolo.
- NO cambia comportamiento de runtime ni defaults del template (off-by-default intactos).

## 4. Esquema de la guia (secciones fijas)

Secciones canonicas (orden fijo); cada una marcada [CORE] (propio del metodo, igual en toda instancia)
o [INSTANCIA] (lo llena el adoptante), y con tier de aplicabilidad:

| # | Seccion | Origen | Tier |
|---|---|---|---|
| 1 | Identidad de la instancia | INSTANCIA | todos |
| 2 | Que es esta instancia | INSTANCIA | todos |
| 3 | Que hace | INSTANCIA | todos |
| 4 | Como lo hace | INSTANCIA | todos |
| 5 | Arquitectura | INSTANCIA | todos |
| 6 | Componentes principales | INSTANCIA | todos |
| 7 | Flujo operativo | CORE+INSTANCIA | todos |
| 8 | Flujo de datos | INSTANCIA | todos |
| 9 | Flujo de decisiones | CORE | todos |
| 10 | Como se implementa la metodologia aqui | CORE+INSTANCIA | todos |
| 11 | Como se construye | INSTANCIA | todos |
| 12 | Como se ejecuta localmente | INSTANCIA | todos |
| 13 | Como se prueba | INSTANCIA | todos |
| 14 | Como se despliega o lanza | INSTANCIA | opcional |
| 15 | Como se opera | INSTANCIA | todos |
| 16 | Troubleshooting | INSTANCIA | todos |
| 17 | Rutas relevantes del protocolo | CORE | todos |
| 18 | Roles y capacidades configuradas | CORE+INSTANCIA | todos |
| 19 | Seguridad y datos sensibles | CORE+INSTANCIA | todos |
| 20 | Continuidad, traspaso y recuperacion de contexto | CORE | todos |
| 21 | Historial de cambios | INSTANCIA | todos |

Campos: cada item declara obligatorio / opcional / "no aplica" (con motivo). Secciones solo-runtime
(p.ej. operar autonomia, event log) -> "no aplica" automatico en `adoption_tier=coordination`.
Reglas de de-duplicacion: sec.17 ENLAZA a las rutas reales (AGENTS.md, TASK_PROTOCOL.md,
N_AGENT_RUNTIME.md, RUNBOOK-*); sec.20 ENLAZA a RESUME.md + cold_start_globs; sec.21 es local. La guia
NO reescribe esos docs ni el HUMAN_REPORT_TEMPLATE (que es snapshot por proceso, no mapa vivo).

## 5. Contrato del generador (scripts/generate_human_guide.py + .ps1)

- Entrada: `--in <guia>.md`. Salida: `--out <guia>.html` (o `--check`).
- Stdlib-only, determinista (mismo MD -> HTML byte-identico), sin red, sin timestamp embebido salvo el
  del frontmatter. Paridad `.ps1` (wrapper que delega en el .py, como generate_*).
- Parsea: frontmatter (identidad: nombre, estado, protocol_version, runtime_version, adoption_tier,
  perfiles) + las 21 secciones + marcadores de campo + checklists + callouts de seguridad + placeholders
  `<...>`.
- Render HTML autocontenido, estilo casa (como REPORT-*.html): `<!DOCTYPE>` + `<style>` INLINE, **sin JS,
  sin CDN, sin red**. Incluye: header de identidad; bloque "panorama" arriba; indice navegable por anclas
  (nav en CSS puro); badges obligatorio/opcional/no-aplica; checklists; callouts de seguridad; layout
  imprimible/exportable a PDF; banner "GENERADO - NO EDITAR".
- VALIDACION DE ESQUEMA integrada (doble funcion validador): si falta una seccion obligatoria, o queda un
  `<PLACEHOLDER>` en una guia *live*, o el tier exige una seccion ausente -> exit!=0 con diagnostico. En
  plantilla/ejemplo los placeholders son validos.
- Tier-aware: lee adoption_tier (frontmatter o protocol.config.json) y pinta secciones solo-runtime como
  "no aplica" en coordination.

## 6. Artefactos y ubicacion (resueltos, ver sec. 13)

- Plantilla master neutral: `Area_comun/protocol/HUMAN_GUIDE.template.md` + `HUMAN_GUIDE.template.html`
  (generado).
- Guia llena de ESTA instancia (dogfooding): `HUMAN_GUIDE.md` + `HUMAN_GUIDE.html` en la **raiz del repo**
  (entrada humana visible, junto a AGENTS.md/RESUME.md).
- Ejemplo ilustrativo: `examples/human_guide_instance/HUMAN_GUIDE.example.md` + `.example.html`.
- Generador: `scripts/generate_human_guide.py` + `scripts/generate_human_guide.ps1`.
- Golden: `examples/human_guide_cases/` (determinismo + validacion de esquema + paridad).

## 7. Invariantes (no negociables)

1. MD = fuente unica; HTML = artefacto generado, jamas editado a mano (banner lo declara).
2. Determinista: mismo MD -> HTML byte-identico (habilita el control de drift).
3. HTML autocontenido: inline CSS, sin JS/CDN/red.
4. Stdlib-only, sin deps externas; paridad .py/.ps1.
5. Neutral de dominio: el master `*.template.*` no contiene specifics; placeholders `<...>`.
6. Off-by-default y aditivo: no cambia runtime ni defaults; reversible (borrar artefactos no rompe nada).

## 8. Gates y CI

- Neutralidad: anadir `HUMAN_GUIDE.template.{md,html}` a `neutrality.scan_globs`; las versiones llenas
  (raiz `HUMAN_GUIDE.*` y `examples/.../*.example.*`) a `exempt_globs`. Pasa `scan_domain_neutrality.py`.
- Encoding: pasa `scan_encoding.py`.
- Drift MD<->HTML: `generate_human_guide.py --check` regenera en memoria y compara byte a byte; falla si
  difiere. Cableado en `.github/workflows/validate.yml` (CI) y `.githooks/pre-commit` (local).
- Validacion de esquema/completitud: la del propio generador (sec.5), config-gated por instancia.

## 9. Tests (golden determinista, sin red)

- Render byte-identico desde un MD fixture (determinismo).
- `--check` detecta drift (HTML alterado a mano -> fail).
- Validacion: seccion obligatoria ausente -> fail; placeholder en live -> fail; tier coordination ->
  secciones runtime marcadas no-aplica.
- Plantilla/ejemplo: placeholders validos -> pass. Paridad .py/.ps1.
- Neutralidad y encoding verdes sobre los `*.template.*`.

## 10. SemVer y neutralidad

MINOR (aditivo, off-by-default, opt-in, reversible). Neutral de dominio. DECISION-0001/0004/0006.

## 11. README_INSTANCIACION.md

Anadir seccion "Guia humana operativa": que es, cuando completarla (al instanciar y como parte del DoD
de cada release / cambio de arquitectura/roles/tier), como generar el HTML (`generate_human_guide.py`),
que el HTML no se edita a mano, y que el `--check` corre en CI.

## 12. Criterios de completitud / validacion / cierre

- Completitud: las 21 secciones presentes en la plantilla con sus tipos de campo; generador + .ps1 +
  golden + gates cableados; README actualizado; ejemplo ilustrativo lleno; guia dogfooding de esta
  instancia generada.
- Validacion: golden 100% verde; neutralidad 0 sobre templates; encoding limpio; `--check` verde;
  determinismo confirmado.
- Cierre: plantilla + generador + ejemplo + guia dogfooding + README + CI, todo ratificado
  adversarialmente (neutralidad + determinismo + no-drift). TASK-0037 -> done.

## 13. Decisiones resueltas (operador + arquitecto, 2026-06-10)

1. **Ubicacion**: NO se crea un arbol `docs/` (evita una DECISION estructural). Plantilla en
   `Area_comun/protocol/`; guia llena de esta instancia en la **raiz** (`HUMAN_GUIDE.{md,html}`, junto a
   AGENTS.md/RESUME.md); ejemplo en `examples/`. Coherente con la convencion existente.
2. **Idioma canonico**: **espanol** (idioma de trabajo del repo). El esquema es agnostico de idioma: un
   adoptante puede traducir sin romper el generador. La neutralidad es de DOMINIO, no de idioma.
3. **Validador**: integrado DENTRO del generador (`--check` hace drift + esquema en una sola herramienta);
   no se crea un script de validacion aparte.

## 14. Recomendacion de implementacion

Dividir: el ARQUITECTO (Claude) fija el esquema (sec.4), redacta la plantilla `.template.md` neutral, el
README y la guia dogfooding de esta instancia; el IMPLEMENTADOR (Codex) construye
`generate_human_guide.py` + `.ps1` + golden + cableado CI/githook. Encolar de a una bajo SDD: SPEC ready
-> tarea de plantilla -> tarea de generador -> tarea de cableado/gates -> cierre. Cada una con claim,
gates verdes, handoff, ratificacion adversarial. Neutralidad innegociable; `*.template.*` son masters
(regla 5).
