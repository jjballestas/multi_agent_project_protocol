# PIPELINE - Cierre ventana baseline -> Sprint 1 (tracker vivo del Asesor)

> Tracker de coordinacion del Asesor para la recta final: cierre de la ventana baseline (25-jul),
> reconciliacion (26-29-jul), sello Etapa 2 (29-jul) y apertura de Sprint 1 gobernado (30-jul).
> COMPLEMENTA (no reemplaza) el panel del operador `personal/operador/vision-nova/pipeline-vision-nova.html`
> (ese lo mantiene el Arquitecto). Este lo mantengo YO y lo actualizo a medida que las tareas avanzan.
> Fuente de verdad de fechas = SELLO-ETAPA-1-nova-budget-DRAFT.md (s.3, s.4, s.10, s.11.1).
> Ultima actualizacion: 2026-07-06 03:19 (local, UTC+2).

## Leyenda
`[x]` hecho/verificado  |  `[~]` en curso  |  `[ ]` pendiente  |  `[!]` atencion/decision  |  `[S]` SELLADO (no tocar, pre-registro)

---

## 1. Calendario sellado (CORREGIDO -- ver nota A al final)
| Fecha | Evento | Estado |
|---|---|---|
| <=08-jul | Sello Etapa 1 (sorteo + sha256) | `[x]` ejecutado adelantado 04-jul (DECISION-0091, #4 seq 3831) |
| <=14-jul | Sandbox mutadores + GRANT EXECUTE | `[x]` sellado adelantado 04-jul (df34ec3) |
| <=15-jul | PAR-2 confirma o cae | `[x]` CONFIRMADO adelantado 05-jul (enmienda s.13; 10/10 pruebas DBA) |
| <=17-jul | **Miembro BASELINE de PAR-1** (P4.2 o P4.3 por sorteo) inicia | `[x]` P4.2 done (TASK-0254) -- hito CUMPLIDO adelantado |
| 25-jul | **Cierre DURO ventana baseline** (no se extiende) | `[~]` dev COMPLETO; falta el sellado de integridad (seccion 3) |
| 26-29-jul | Reconciliacion post-ventana (Analista read-only) | `[ ]` pendiente |
| 29-jul | Sello Etapa 2 | `[ ]` draft F3.2 listo; bloqueado por reconciliacion + DEC dominio P3.x |
| 30-jul | **Abre Sprint 1 gobernado** (gate duro; fin linea roja Q4) | `[S]` sellado; piso minimo viable YA cumplido |

---

## 2. Ventana baseline: DEV = COMPLETO (adelantado)
Las 6 unidades baseline de s.3.2 estan done y con evento en el journal (event_seq 1-14):
| Unidad | tarea_id | Rol | Estado |
|---|---|---|---|
| GOAL-P1 (fundacion) | GOAL-P1 | excluida del contraste (piloto) | `[x]` done + atestada sha256 d2a13216 |
| P2.1 read model parametros | TASK-0250 | fuera de contraste | `[x]` done (fix-loop 1/2) |
| P2.2 reporte ejecucion | TASK-0251 | miembro baseline ANCLADO PAR-D | `[x]` done (fix-loop 1/2) |
| P4.1 Apply_Budget_Modification | TASK-0253 | pattern-setter (patron se congela) | `[x]` done (teething arranque 2M) |
| Miembro baseline PAR-1 = P4.2 | TASK-0254 | Apply_Availability_Adjustment | `[x]` done (limpio 431k) |
| Miembro baseline PAR-2 = Annul_Availability_Certificate | TASK-0255 | superficie API | `[x]` done (GO 0 bloqueantes) |

Piso minimo viable (P1 completa + miembro baseline PAR-1) = `[x]` CUMPLIDO.

---

## 3. Cierre DURO ventana baseline (25-jul) -- tareas de SELLADO, no de build
El dev esta completo; el cierre es de INTEGRIDAD. Dueno de la mayoria = Arquitecto/Analista; yo verifico.
| # | Tarea | Dueno | Estado |
|---|---|---|---|
| 3.1 | Confirmar las 6 filas baseline con medicion completa; resolver token=NA (err.log volatil P2.1/P2.2) vs real | Arquitecto | `[x]` RESUELTO por el Arquitecto (tokens_total_atribuibles P2.1/P2.2 corregidos, d3b8ad6) |
| 3.2 | **Resolver cadencia de atestacion del journal** (per-unidad vs checkpoint) -- ver seccion 4 y ask#1 | Arquitecto | `[~]` recomendacion HIBRIDA ruteada; esperando su respuesta |
| 3.3 | Registrar quality-data del baseline sin reabrir unidades: #10 (50212) + #11/#12/#13 (TASK-0255) | Arquitecto/Analista | `[~]` #11-13 CONFIRMADOS + horneados en P4-006 (6i/6j/6k); #10 + los 3 esperan veredicto Analista |
| 3.4 | Confirmar aislamiento de teething: toda unidad pre-30-jul tag=arranque; incidentes -> OVERHEAD-FIJO | Arquitecto | `[x]` convencion aplicada (P4.1 arranque, etc.) |
| 3.5 | Confirmar que ninguna unidad baseline queda a medio vuelo pasado 25-jul (la ventana NO se extiende) | Arquitecto | `[x]` dev completo, nada en vuelo |
| 3.6 | Preparar la reconciliacion 26-29: repo producto mapeable commit/rama/log -> tarea_id (huerfanos = abandonada + se publican) | Arquitecto -> Analista | `[ ]` pendiente (arranca 26-jul) |
| 3.7 | Confirmar patron P4.1 congelado (lo heredan SOLO los gobernados; aislamiento intra-par) | Arquitecto | `[x]` congelado al arrancar PAR-1 |

---

## 4. Coordinacion en vuelo (ahora)
| Item | Estado |
|---|---|
| Senal DECISION-0018 #11/#12/#13 (3 huecos QA de TASK-0255 baseline) al Arquitecto | `[x]` CONFIRMADOS linea-por-linea + horneados en SPEC-NOVA-P4-006 (6i/6j/6k); ruteados al Analista |
| Cadencia de atestacion del journal (ask#1) | `[~]` recomendacion hibrida ruteada al Arquitecto |
| Hallazgo #10 (50212 etiquetado cruzado) | `[~]` Arquitecto lo registro (a2657d5); Analista verifica |
| TASK-0246 (informe adversarial NOVA-DEV) | `[x]` remediacion OK (Analista) + done-flip (8c29bb3) |
| FYI archivo basura `nul` | `[x]` limpiado por el Arquitecto (8321277) |
| EVIDENCIA-VIVA (A1-A9) | `[~]` alimentada cada sesion (directiva operador) |
| Adopcion 4R (gentle-ai): debate APROBADO | `[x]` DECISION-0092 registrada por el Arquitecto (9ca131b); seccion A aplicable-ahora + B diferida a Sprint 1 |
| Cola no-idle del Arquitecto (re-llenado) | `[~]` DIRECTIVA ruteada: (1) actualizar HTML operador stale; (2) materializar contrato de salida/carve-outs de DECISION-0092 A; (3) prep reconciliacion 26-29; (4) prioridad TASK-0178 |

---

## 5. Gate Sprint 1 gobernado (30-jul) -- SELLADO, no adelantable
`[S]` Los MIEMBROS GOBERNADOS (PAR-1 P4.3 Apply_Commitment_Adjustment, PAR-2 Annul_Commitment, PAR-D
Get_*_List, familia P3, pool Q4) son **post-30-jul (sello s.3.3)**. NO se construyen antes (rompe el
pre-registro). Lo unico permitido pre-30-jul = ESCRIBIR SPECs:
| Prep permitida pre-30-jul | Estado |
|---|---|
| SPEC-NOVA-P4-006 (Annul_Commitment gobernado, con auth real) | `[x]` escrita (9bd3587) |
| Resto de SPECs Sprint 1 (P4.3/P3.1/P3.2-4/pool Q4/BR-C3) | `[x]` ya existian escritas (revisado por Arquitecto) |
| Sello Etapa 2 (draft F3.2) | `[ ]` bloqueado hasta reconciliacion + DEC dominio P3.x |
| TASK-0246 relleno de gobernanza | `[~]` in_review |

---

## 6. Pendientes del operador (sin fecha dura)
| Item | Estado |
|---|---|
| Cadencia de atestacion del journal (hibrido -- hash-log commiteado per-unidad + anclaje #4 per-checkpoint) | `[x]` RUTEADA al Arquitecto (95d3e54); esperando su respuesta |
| Refinamientos s.23 (linea isomorfos + procedencia del desempate alfabetico PAR-2) | `[~]` NOTA DE ISOMORFISMO ruteada al Arquitecto para s.23 + s.21 (blindaje, no cambia asignaciones); esperando que la selle |

---

## Nota A -- correccion de calendario (2026-07-06)
Mi calendario personal traia "17-jul = miembros gobernados": ERROR. El sello s.3.2/s.3.3/s.11.1 dice:
17-jul = **miembro BASELINE de PAR-1** (ya cumplido, P4.2/TASK-0254); los **gobernados = Sprint 1,
post-30-jul**. Corregido aqui y en ESTADO-asesor.md. Consecuencia directa: los miembros gobernados NO se
pueden arrancar ahora (ver ask#2).
