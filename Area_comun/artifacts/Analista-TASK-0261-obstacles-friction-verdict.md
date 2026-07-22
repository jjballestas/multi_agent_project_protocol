# Analista - Veredicto adversarial TASK-0261 (C3/C4 validate_mailbox: obstacles + friccion)

- Reviewer: Analista (voz independiente / checker)
- Fecha local: 2026-07-22 23:05 +02:00
- Ancla canonica: impl commit 3e5cb84 ("feat(TASK-0261): validate governed mailbox reports")
- Protocolo HEAD en juicio: 88f16c2. Alcance: PROTOCOLO PURO (sin producto Nova en alcance).
- Veredicto: **NO-GO / CHANGE-REQUIRED**

## Reproduccion (clon limpio, gate por exit code)

Clon limpio de este repo a D:/ccv0261, `git checkout 3e5cb84`. Todas las puertas verdes:

| Gate | Comando | Exit |
|------|---------|------|
| Estado canonico | `python scripts/validate_collaboration_state.py` | 0 |
| Suite mailbox | `python examples/mailbox_report_cases/run_mailbox_report_cases.py` (7/7) | 0 |
| Encoding | `python scripts/scan_encoding.py` | 0 |
| Neutralidad | `python scripts/scan_domain_neutrality.py` | 0 |
| Diff whitespace | `git diff --check` | 0 |
| Arbol vivo | `python scripts/validate_collaboration_state.py` (hub actual) | 0 |

Las puertas pasan. El NO-GO NO surge de las puertas: surge de EJERCITAR LA FAMILIA COMPLETA
que prometen los criterios 3 y 4 (no solo el ejemplo col-0 de los 7 casos). Se importaron las
funciones reales del commit (`validate_governed_mailbox_report`, `parse_mailbox_obstacles`) y se
lanzaron 32 payloads propios; ademas se confirmo por CLI end-to-end con el validador real sobre
fixtures en `minimal_instance`.

## Tabla vector-por-vector (por comportamiento)

| # | Punto del review | Vector | Esperado | Obtenido | Resultado |
|---|------------------|--------|----------|----------|-----------|
| 1 | Grandfathering | REPORTE pre-adopcion (date 07-21, sin marker, con/ sin friccion) en open/answered/archived | verde | verde | PASS |
| 1 | Grandfathering | friction>0 + [] con date vieja (inmune) | verde | verde | PASS |
| 1 | Grandfathering | sin date + sin created_at + sin marker | verde (grandfathered) | verde | PASS (ver Residual R1) |
| 1 | Grandfathering | HUB VIVO: 20+ REPORTE pre-adopcion en archived/ | verde | verde (validate exit 0) | PASS |
| 2 | Opt-in | marker report_schema_version 1.0 (con y sin comillas) + date vieja + friction>0 + [] | FAIL (en regla) | FAIL | PASS |
| 2 | Opt-in | date == 2026-07-22 exacto -> en regla | FAIL (friction>0+[]) | FAIL | PASS |
| 2 | Opt-in | created_at 2026-07-23 -> en regla | FAIL | FAIL | PASS |
| 2 | Opt-in | sin marker + date vieja -> grandfathered | verde | verde | PASS |
| 3 | 4 cuadrantes (col-0) | friction 2 + [] | FAIL accionable | FAIL "friction_count > 0 but obstacles is empty" | PASS |
| 3 | 4 cuadrantes (col-0) | friction 0 + [] | PASA | PASA | PASS |
| 3 | 4 cuadrantes (col-0) | friction 2 + lista valida col-0 | PASA | PASA | PASS |
| 3 | 4 cuadrantes (col-0) | friction 0 + lista valida col-0 | PASA | PASA | PASS |
| 3 | 4 cuadrantes (INDENTADO) | friction 2 + lista VALIDA y COMPLETA con guion indentado (frontmatter) | PASA | **FAIL "obstacles is empty" (FALSO ROJO)** | **SLIP-1** |
| 3 | 4 cuadrantes (INDENTADO) | friction 2 + lista valida indentada en cuerpo | PASA | **FAIL "obstacles is empty"** | **SLIP-1** |
| 4 | Parser 4-campos (col-0) | falta campo / campo extra / valor vacio / enum malo / 2do item malo | FAIL | FAIL | PASS |
| 4 | Parser 4-campos (INDENTADO) | obstacle malformado (faltan 2 campos) con guion indentado + friction 0 | FAIL | **PASA (invisible)** | **SLIP-2** |
| 5 | friction entero | -1 / 1.5 / abc / ausente / 007 | FAIL (007->7) | FAIL | PASS |
| 6 | Limite C4 | doc presencia/forma/consistencia vs veracidad | documentado | TASK_PROTOCOL.md seccion DECISION-0103 C3/C4 | PASS |

## Defecto raiz (una sola causa, dos sintomas)

`parse_mailbox_obstacles` reconoce items de bloque SOLO con el guion en la columna 0
(`item_start = ^-\s+...`). `field_line`/`continuation` solo tratan campos indentados de items
que ya empezaron en columna 0. Una secuencia YAML con el guion INDENTADO (`  - what:`) --que es
YAML valido, es la forma natural de una lista en frontmatter, y es EXACTAMENTE la convencion que
estos mismos mensajes de mailbox usan para `context_refs`-- rompe el bucle en el primer item y
retorna `([], None)` SIN error: la lista no vacia se interpreta como VACIA, en silencio.

De esa mala clasificacion silenciosa salen dos contradicciones de criterios que se me pidio gatear:

- **SLIP-1 (FALSO ROJO -- reintroduce el riesgo central de la unidad).** Un REPORTE post-adopcion
  que documenta honestamente un obstaculo completo en forma indentada (frontmatter o cuerpo) con
  `friction_count > 0` es enrojecido con "friction_count > 0 but obstacles is empty". Contradice el
  punto 3 ("friction>0 con lista no vacia -> PASA") y la propia razon de ser de la unidad: NO
  enrojecer el canal vivo. Hoy el hub vivo esta verde porque todos sus REPORTE son pre-adopcion
  (grandfathered); pero el PRIMER REPORTE gobernado post-adopcion escrito con la convencion
  indentada (la misma de `context_refs`) rojo el estado canonico y para el pipeline.
- **SLIP-2 (SILENCIOSO -- burla la garantia de 4 campos).** Un obstacle malformado (faltan campos)
  en forma indentada con `friction_count 0` PASA. Contradice el punto 4 ("obstacle malformado ->
  FAIL") y el acceptance linea 19 ("sin bloque obstacles bien formado -> exit != 0 accionable").

Ambos sintomas son INVISIBLES a los 7 casos enviados porque la suite solo ejercita la forma col-0.

## Falsabilidad (como refutar mi hallazgo)

Si en un clon limpio de 3e5cb84 se corre:
`obstacles:` seguido de `  - what: X` / `    root_cause: Y` / `    resolution: Z` /
`    recurrence_risk: low` con `friction_count: 2` y `date: 2026-07-22`, el validador debe salir 0
(lista valida no vacia). Sale 1 con "obstacles is empty". Reproducido 2x (frontmatter y cuerpo).
Con la variante malformada y `friction_count: 0` debe salir 1; sale 0. Si alguien reproduce lo
contrario, mi NO-GO cae.

## Puntos que SI pasan (no re-abrir)

Grandfathering (riesgo central) mitigado; opt-in por marker/fecha correcto en ambos bordes;
los 4 cuadrantes en forma col-0 correctos; friction_count entero no negativo correcto; limite
C4 documentado. El defecto es de ROBUSTEZ del parser ante la forma indentada, no del diseno de
grandfathering.

## Residuales declarados (no bloqueantes)

- **R1.** Un REPORTE post-adopcion que OMITE date + created_at + report_schema_version escapa la
  regla entera (grandfathered por ausencia de ancla temporal). No enrojece nada, pero es una via
  de evasion declarativa. Recomendacion (no bloqueante): documentar que el marker/fecha es
  obligatorio en la plantilla de TASK-0262.
- **R2.** El gate solo aplica a `type: REPORTE` con `\bTASK-\d{4}\b`; una entrega tipada HANDOFF
  (como la propia entrega de 0261) o que referencia TASK-EXTRACT-hex no entra. Es alcance de
  diseno, coherente con la unidad, se anota.

## Remediacion esperada (loop de correccion, max 2 iteraciones)

1. En `parse_mailbox_obstacles`: (a) reconocer items de secuencia de bloque con guion a
   cualquier indentacion consistente; y CRITICO (b) si hay contenido NO en blanco tras
   `obstacles:` que produce cero items parseados, FALLAR con mensaje accionable
   ("unrecognized obstacles format; use a YAML list of what/root_cause/resolution/recurrence_risk")
   en vez de retornar `[]` en silencio. Esa regla (b) sola convierte SLIP-1 en error accionable
   corregible por el autor y caza SLIP-2.
2. Anadir a `run_mailbox_report_cases.py` casos indentados (frontmatter y cuerpo): valido+friction>0
   -> PASA; malformado+friction 0 -> FAIL.
3. Gates afectados a re-verificar: `run_mailbox_report_cases.py`, `validate_collaboration_state.py`,
   `scan_encoding.py`, `scan_domain_neutrality.py` (todos exit 0) sobre clon limpio del nuevo commit.
4. Re-juicio: re-corro mi arnes adversarial (P6 frontmatter/cuerpo + P7 + la familia completa)
   sobre el commit de remediacion ANTES de cualquier commit de cierre. Maximo 2 iteraciones; un
   2do NO-GO escala al operador humano.

## Recomendacion de cierre

**CHANGE-REQUIRED.** El grandfathering (riesgo central) funciona, pero el parser mis-clasifica en
silencio la forma YAML indentada -- convencion ya usada en estos mismos mensajes -- produciendo un
falso rojo del canal vivo (punto 3) y una evasion de la garantia de 4 campos (punto 4). No cerrable
hasta que la remediacion pase el re-juicio.

-- Analista
