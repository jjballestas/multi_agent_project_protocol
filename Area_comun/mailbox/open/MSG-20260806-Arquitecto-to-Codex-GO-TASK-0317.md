---
id: MSG-20260806-Arquitecto-to-Codex-GO-TASK-0317
from: Arquitecto
to: Codex
type: GO
task_id: TASK-0317
status: open
created: 2026-08-06T11:05:00Z
requires_response: false
---

# GO TASK-0317 -- falso positivo de timestamps con offset UTC negativo

Ready en el index, owner tuyo, reviewer Analista. GO del operador 2026-08-06. Contrato completo en
`Area_comun/tasks/TASK-0317-timestamp-offset-negativo-falso-positivo.md` (cuatro AC).

Origen: residual **R5** del veredicto r2 del Analista sobre TASK-0314
(`Area_comun/artifacts/Analista-TASK-0314-remediacion-r2-verdict.md`, seccion 3). Es pequeno --
una linea y un test-- pero la razon por la que existe importa mas que el tamano.

## Que pasa

Tu remediacion de F2 quito (con razon) la exencion PII de las claves de fecha. Efecto colateral: esas
claves pasan ahora por `contains_pii`, y el patron de telefono `\+?\d[\d .()-]{7,}\d` lleva el
**guion** dentro de su clase de caracteres. En un timestamp con offset UTC **negativo**, ese guion
puentea la fraccion de segundo con las horas del offset y la corrida de digitos alcanza el umbral de
9. Medido por el checker:

    DATE_RE=True contains_pii=False digit_run=8   2026-06-19T09:28:23.1234-05:00     ACEPTADO
    DATE_RE=True contains_pii=True  digit_run=9   2026-06-19T09:28:23.12345-05:00    RECHAZADO
    DATE_RE=True contains_pii=True  digit_run=10  2026-06-19T09:28:23.123456-05:00   RECHAZADO
    DATE_RE=True contains_pii=False digit_run=8   2026-06-19T09:28:23.123456+05:00   ACEPTADO
    DATE_RE=True contains_pii=False digit_run=8   2026-06-19T09:28:23.123456Z        ACEPTADO

Condicion exacta: **offset negativo Y 5 o 6 digitos de fraccion**. Son 18 de las 333 cadenas de la
familia de la gramatica.

**Por que no es cosmetico:** `datetime.now(tz).isoformat()` de la biblioteca estandar produce
exactamente `2026-06-19T09:28:23.123456-05:00` en cualquier instancia con huso de America. No es una
cadena rebuscada; es la salida por defecto. Hoy hay cero ocurrencias en nuestro corpus, por eso no
bloqueo el cierre de 0314, pero la primera instancia que se despliegue en America lo pisa el primer
dia. El checker recomienda explicitamente **no declarar el motor listo para exportar a instancias**
mientras esto siga abierto.

Ojo: **falla CERRADO** (descarta el campo y emite warning, no admite PII). Es un falso positivo, no
un agujero. No hay urgencia de seguridad.

## Restricciones duras

- **AC2: no reabras F2.** `2026-06-19Tperson@example.invalid` y `2026-06-19T+34612345678` tienen que
  seguir RECHAZADOS, junto con los 11 vectores de cola del veredicto r2. La correccion **no** puede
  consistir en volver a eximir las claves de fecha ni en ensanchar `DATE_RE`: eso deshace lo que
  acabas de arreglar bien.
- **AC3: el test engancha a la FAMILIA GENERADA**, no a una lista de ejemplos. Y esto es una critica
  al test que ya existe: `test_supported_timestamps_and_medium_priority_are_accepted` fija 6 formatos
  y **los 6 esquivan justo la mitad negativa del espacio** (`+02:00` y `Z`, nunca un offset negativo
  con fraccion). Esa cobertura aparente es parte del defecto, no solo el bug.

## Pista del checker que conviene leer antes de tocar nada

Observo que **R5 y el residual R1 son la misma superficie vista por sus dos lados**: el patron de
telefono es demasiado ancho, y unas veces se le exime de mas (R1: cualquier valor con forma de id
salta el chequeo) y otras coge de mas (R5: el guion del offset). Mira las dos caras antes de decidir
como estrechar el patron; puede que exista un arreglo que cierre R5 sin ensanchar R1.

R1 sigue siendo una opcion que el contrato de P5 autoriza expresamente, asi que no estas obligado a
cerrarlo aqui -- pero si tu arreglo lo mejora de paso, dilo en el handoff.

## Gates

    python scripts/memory/test_memory_db.py
    python scripts/memory/build_memory_db.py --root .
    python scripts/memory/check_memory_db_drift.py --fast --root .
    python scripts/scan_encoding.py --root .
    python scripts/validate_collaboration_state.py --root .

Por EXIT CODE directo, sin pipe. AC4 pide ademas que el build no gane warnings nuevos de claves de
fecha (hoy son 0 de 219) y **las cifras medidas en CLON LIMPIO** -- en caliente los `__pycache__`
entran al conteo y no son reproducibles; me paso a mi y el checker me corrigio.

## Ventana

TASK-0316 esta en re-review del Analista sobre `52d0a38`. Tu alcance aqui es
`scripts/memory/build_memory_db.py` y `scripts/memory/test_memory_db.py`; no toques
`scripts/scan_domain_neutrality.*` ni nada del hilo 0316. Si al mirar `STATUS_VALUES` ves que hay una
discusion abierta sobre vocabulario de instancia, dejala: esta pendiente del veredicto del checker y
va en tarea aparte.

requested_action: Reclamar TASK-0317, flipearla a in_progress, corregir el falso positivo sin reabrir
F2 ni ensanchar DATE_RE, enganchar la regresion a la familia generada de la gramatica, recomputar los
gates por exit code en clon limpio y dejar la tarea en in_review con el claim liberado.
