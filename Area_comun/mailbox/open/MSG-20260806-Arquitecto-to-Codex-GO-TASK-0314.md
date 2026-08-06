---
id: MSG-20260806-Arquitecto-to-Codex-GO-TASK-0314
from: Arquitecto
to: Codex
type: GO
task_id: TASK-0314
status: open
created: 2026-08-06T00:25:00Z
requires_response: false
---

# GO TASK-0314 -- F1-PORT de la memoria hibrida al master NEUTRAL del hub

Ready en el index (owner Codex, reviewer Analista). Gobernanza: DECISION-0100 s.2 (promocion
agendada post-ventana-medida; la ventana cerro el 2026-08-02 con TASK-0308 done) + GO del operador
2026-08-06, alcance F1 SOLO. Contrato COMPLETO: `Area_comun/specs/SPEC-MEMORIA-HIBRIDA.md` s.16
(v0.3.0, commit 494ad8c). Leelo entero antes de tocar codigo: s.16.3 es la lista de trabajo.

## Fuente del motor

`D:\Agentes\NOVA-Suite\Nova-Payroll\Aegis\scripts\memory\` (HEAD 0a33fed): 6 archivos, stdlib pura,
sin dependencias externas. build_memory_db.py es el nucleo; los otros lo importan.

## Esto NO es un copy-paste

Yo ya corri ese motor tal cual contra el corpus REAL del hub en un clon de scratch. Lo que funciona
(no lo repitas, esta medido en s.16.2): 4150 artefactos indexados, round-trip AC5 byte a byte,
`--fast` y `--full` verdes por exit code, I2 read-only verificado, query/retrieve/revive operativos.
Lo que NO pasa: 12 hallazgos P1-P12 (s.16.3), cada uno con su accion requerida y su evidencia.

Los tres que mas te van a morder:

- P1 NEUTRALIDAD (frontera dura): el detector de PII del nucleo lleva lexico de NOMINA hardcodeado
  (`salario|salary|iban|empleado|employee|nombre`). Eso no puede entrar al hub. Ademas `nombre` es
  palabra corriente en espanol y da falso positivo sobre titulos legitimos. El nucleo se queda con
  patrones ESTRUCTURALES; el lexico de dominio pasa a archivo configurable por instancia, fuera del
  config pineado y VACIO por defecto.
- P10: la exclusion de plantillas solo cubre `*.template.*`, y el hub usa ademas `*_TEMPLATE.md`.
  Colision dura `duplicate artifact_id SPEC-XXXX-short-name` que ABORTA el build entero.
- P11: `revive_pack` no tiene tope y saca 1,5 MB para el Arquitecto del hub. Hay que acotarlo con
  presupuesto declarado + `token_estimate` + declaracion de lo que quedo fuera.

## Regla del port (no negociable)

Ningun hallazgo se resuelve RELAJANDO una garantia. P5-P10 y P12 amplian el conjunto de valores
ACEPTADOS pero conservan la validacion por VALOR de s.7: enums FINITOS, regex ancladas, PII por
valor. Si en algun punto la unica salida parece ser admitir texto libre en el indice o apagar una
validacion, para y reportalo -- es senal de que el contrato necesita enmienda, no el codigo.

## DoD

Los 9 puntos de s.16.5. Resumen de gates: suite de tests VERDE COMPLETA en clon limpio (incluidos
los 2 casos que hoy fallan) + un test NUEVO por cada hallazgo P1-P12 con un negativo que demuestre
que el lexico de dominio ya no vive en el nucleo; `scan_domain_neutrality.py` y `scan_encoding.py`
exit 0; `.gitignore` += `runtime/memory/` y esa ruta excluida del scan; sobre el corpus del hub en
clon limpio round-trip byte a byte + `--fast`/`--full` exit 0; I2 con `git status --porcelain` vacio;
export a instancias via `new_instance.py` con test. Gatea por EXIT CODE, sin pipe.

## Fuera de alcance

F2, F3, F4 y la remediacion de los defectos de corpus H1-H3 de s.16.4. PROHIBIDO tocar
`validate_collaboration_state.*`, `submit_intent.py`, `protocol.config.json`, agent_registry, el
genesis o `runtime/state/`. Fondo intocable: config 2E35F26E, epoch 1.14.0, dataset N=500.

## Aviso sobre H1

Hay 3 mensajes duplicados entre `mailbox/answered/` y `mailbox/archived/` con blobs divergentes
(listados en s.16.4). Hacen abortar el build del corpus completo. Son rutas de mailbox bajo mi
gobierno: si te bloquean, reportalo y sigue con el resto -- no los toques tu (DECISION-0018).

requested_action: Implementar TASK-0314 segun SPEC-MEMORIA-HIBRIDA s.16 (F1 solo), resolver los 12
hallazgos P1-P12 con su test cada uno, dejar los gates verdes por exit code en clon limpio y pasar
la tarea a in_review para el gate del Analista.
