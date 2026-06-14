# ANALISTA — Pasada adversarial acotada sobre Fase 0 (E5 FAILURE_MODES + E6 gobernador)

> Voz analista independiente. Lente: METODOLOGIA / HONESTIDAD (no redaccion, no ingenieria). UNA pasada,
> falsable, proporcional (son docs baratos, documentales, MINOR). Pre-ratificacion del operador.
> Insumos: drafts-fase0/{FAILURE_MODES.md, E6-governor-TASK_PROTOCOL-patch.md, DECISION-0034,
> ACCEPTANCE-fase0-E5-E6.md}, orden 06, DECISION-0024 (SA.4), DECISION-0027 (piloto).
> Taxonomia de referencia verificada: MAST, Cemri et al. 2025 — 14 modos en 3 categorias.
> Fecha: 2026-06-14.

## Veredicto de cabecera (3 lineas)

- **RATIFICABLE con 3 ajustes baratos.** La taxonomia MAST esta bien aplicada (14/14, categorias y nombres
  correctos) y la frontera de honestidad esta declarada — mejor que el promedio.
- Dos fugas finas de honestidad: el conteo **"12 incidentes reales mapeados"** es una mini-afirmacion
  empirica que pisa #1 (diferido); y falta declarar que **MAST no es toda la superficie de fallo** del
  protocolo (encoding/neutralidad/secretos quedan fuera de MAST).
- E6 es un filtro de **elegibilidad**, no de **seguridad**: un loop oscilante (Ralph Wiggum) pasa las 4 y
  sigue siendo runaway. Compone limpio con SA.4 salvo un solapamiento temporal con DECISION-0027.

---

## 1) Fidelidad MAST (E5)

**PASA** la fidelidad taxonomica. Verifique contra MAST (Cemri 2025): los 14 modos estan, en las 3
categorias correctas, con nombres correctos (1.1–1.5 / 2.1–2.6 / 3.1–3.3) y placements correctos
(p. ej. 1.3 Step repetition en cat.1, 2.6 Reasoning-action en cat.2, 3.3 en cat.3). El marcado honesto de
FM-2.1/FM-2.6 ("no dedicated incident") y FM-1.3 ("partial") es correcto y es justo lo que pide la honestidad.

**Modo señalado (falsable, como pediste): FM-1.1 "Disobey task specification" marcado "Yes" (incidente
real) pero la celda solo cita el GUARDRAIL** (turn schema + review SDD), no un incidente real (un turno
malformado / deliverable que ignoro `acceptance_criteria` en el historial de este repo). La columna
"Incident? = Yes" conflaciona "existe guardrail" con "ocurrio el incidente". Contraste: FM-1.2 (drift →
re-genesis) y FM-1.3 (colision de `run_id`, TASK-0096) SI citan incidente real; FM-1.1, FM-1.4, FM-1.5 no
citan el evento, solo el mecanismo. *Test:* para cada "Yes", o se cita el incidente (decision/run_id/
evento) o se baja a "preventive / no dedicated incident" como FM-2.1.

**Limite a declarar (falsable): hay fallos reales del protocolo que NO encajan en MAST** y el doc no lo
dice. MAST cubre coordinacion multi-agente; el protocolo ademas guarda y testea modos NO-MAST: **corrupcion
de encoding** (`scan_encoding.py`), **fuga de neutralidad de dominio** (`scan_domain_neutrality.py`),
**fuga de secretos**. Ninguno es un modo MAST. Tal como esta, un lector infiere que los 14 modos son la
superficie completa de fallo — no lo son.

**CAMBIO REQUERIDO:** (a) por fila "Yes", citar el incidente o degradar a preventivo; (b) añadir una linea
de limite: "MAST nombra los modos de coordinacion; este protocolo ademas contiene modos no-MAST (encoding,
neutralidad, secretos) gobernados por sus propios gates".

**RIESGO DECLARADO:** sin (a), "12 incidentes reales" es incomprobable fila a fila; sin (b), el catalogo se
lee como exhaustivo y un fallo no-MAST se queda sin hogar ("si no esta en la tabla, no es un modo").

---

## 2) No-overreach (E5)

**NO confirmo "ninguna".** El doc declara bien la frontera ("MAST aplicado, NO 1:1 con MAST-Data, NO
estudio empirico") — eso es correcto y explicito. Pero **una frase la cruza**:

> **"Real operational incident mapped: 12 modes"** (Coverage summary).

Es un **conteo empirico** sobre el historial del proyecto ("12 incidentes reales ocurrieron y estan
mapeados") — exactamente el producto de #1 (protocol_research, diferido) y en tension con la propia frase
"not an empirical study of the project history" y con DECISION-0034 ("no measured numbers"). Un numero es un
numero. La frase de cabecera "the operational incidents this protocol has already mitigated" hereda el mismo
exceso en las filas sin evidencia de incidente.

**Confirmo limpias (para no inflar):** NO dice "dataset citable"; NO cuantifica severidad/frecuencia
(disclaim explicito); "14/14 named" es nombrar, no equivaler — correcto.

**CAMBIO REQUERIDO:** reformular el conteo a guardrails, no a incidentes medidos: p. ej. "12 modos con
guardrail mapeado; evidencia de incidente citada donde existe (FM-1.2, FM-1.3, FM-2.5, …)". Si se quiere
mantener "incidentes reales", entonces citar los 12 (y eso ya empieza a ser #1).

**RIESGO DECLARADO:** un tribunal/TFM lee "12 incidentes reales mapeados" como el resultado empirico que #1
aun no ha producido → afirmacion prematura que debilita la honestidad que el resto del doc cuida bien.

---

## 3) Completitud del gobernador (E6)

**NO confirmo que las 4 cubran runaway.** Las 4 condiciones (recurrencia ≥ semanal / verificacion objetiva /
budget absorbe reintento / tools senior) son un filtro de **elegibilidad y ROI** ("¿merece existir este
loop?"), NO de **contencion en ejecucion** ("¿para cuando se descarrie?"). El runaway (Ralph Wiggum) es un
problema de runtime, contenido por el sobre SA.4 (max_turns, kill-switch, reloj, checkpoint), no por E6.

**Loop que pasa las 4 y NO deberia correr (gap, falsable):** *"auto-fix de lint/formato del repo,
semanal"*. (1) recurre semanal ✓; (2) verificacion objetiva = linter exit 0 ✓; (3) cada corrida barata,
budget absorbe ✓; (4) edita y commitea, tools senior ✓. **Pasa el gobernador.** Modo runaway: dos reglas en
conflicto (formateador quiere tabs, regla quiere espacios) → el loop "arregla" ida y vuelta cada ciclo, cada
ciclo verde, **nunca converge**. Las 4 condiciones no lo detectan; solo lo para una condicion de
convergencia o el `max_turns` de SA.4. La condicion 2 pregunta si EXISTE verificacion (si/no), no si es
**sana / no-gameable**; la 3 asume reintentos **acotados**, que es justo lo que un runaway no tiene.

**CAMBIO REQUERIDO (proporcional):** añadir UNA pregunta (o calificar la 2): *"Terminacion y progreso:
¿tiene el loop una condicion de parada/convergencia y reintentos acotados, y es su verificacion sana (no
auto-gameable)?"* + una linea de remision: "la contencion en ejecucion (max_turns/kill-switch/checkpoint)
la enforce DECISION-0024; el gobernador no la relitiga pero la exige activa para todo loop que apruebe".

**RIESGO DECLARADO:** si E6 se presenta como el salvaguarda del runaway, un equipo despacha un loop elegible
pero oscilante creyendolo "cleared"; lo unico que realmente lo para es el sobre SA.4 → ese sobre debe ser
**no-opcional** para cualquier loop aprobado por el gobernador.

---

## 4) Consistencia E6 ↔ autonomia supervisada (DECISION-0024 / SA.4)

**COMPONEN LIMPIO en lo esencial.** Operan en etapas distintas (E6 = build-time, elegibilidad; SA.4 =
run-time, sobre de contencion) y E6 **no redefine ni contradice** ningun cap (no reescribe max_turns,
checkpoint, kill-switch). No es duplicacion: "¿debe existir?" vs "¿como se acota cuando corre?". La
condicion 3 de E6 incluso **apunta a** los topes de `budget.py` en vez de inventar un budget paralelo.

**Punto de friccion concreto (falsable):** E6 dice "*every* expansion of supervised autonomy … must pass
this governor **first**". Pero **DECISION-0027 ya autorizo el piloto SA.4 ANTES de que E6/el gobernador
existiera**. Lectura estricta → ambiguedad: ¿el piloto ya autorizado queda retroactivamente bloqueado por
un gobernador posterior? *Test:* el texto debe decir explicitamente que el gobernador liga **expansiones
futuras** y **no es retroactivo** al piloto concedido en 0027 (o, si se quiere, que el piloto lo re-pasa
trivialmente y se deja constancia).

**CAMBIO REQUERIDO:** una clausula de alcance temporal en E6: "aplica a ampliaciones futuras de SA.4; no
revoca autorizaciones ya concedidas (DECISION-0027)". Y dejar explicito que la condicion 3 se evalua
**contra** el sobre SA.4/budget, no como chequeo paralelo.

**RIESGO DECLARADO:** sin la clausula, coexisten "piloto autorizado (0027)" y "debe pasar el gobernador
primero (0034)" → un agente o bloquea el piloto autorizado o trata el gobernador como papel mojado.

---

## Cierre (anti-meta-proyecto)

Tres ajustes baratos, todos dentro de la misma MINOR, sin re-arquitectura:
1. **E5:** citar incidente por fila "Yes" (o degradar) + reformular "12 incidentes reales" a guardrails +
   declarar el limite "hay modos no-MAST". (§1, §2)
2. **E6:** una pregunta de terminacion/convergencia + remision a SA.4 como contencion no-opcional. (§3)
3. **E6:** clausula de alcance temporal frente a DECISION-0027. (§4)

Hechos 1–3, **ratificable**: la taxonomia es fiel, la frontera de honestidad ya esta (solo hay que cerrar la
fuga del conteo), y E6 + SA.4 componen limpio. Proporcional a dos docs documentales.

> No consolido ni decido. No mute estado autoritativo (drafts en personal/Claude; mi salida en artifacts/).
> El arquitecto entra por submit_intent si incorpora; la ratificacion es tuya.
