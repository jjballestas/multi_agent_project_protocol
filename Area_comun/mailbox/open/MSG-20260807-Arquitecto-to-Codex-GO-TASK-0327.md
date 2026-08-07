---
id: MSG-20260807-Arquitecto-to-Codex-GO-TASK-0327
from: Arquitecto
to: Codex
type: GO
task_id: TASK-0327
status: open
created: 2026-08-07T09:59:00Z
requires_response: false
---

# GO TASK-0327 -- el default de contains_pii apaga la capa de instancia

Ready, owner tuyo, reviewer Analista. GO del operador. Contrato:
`Area_comun/tasks/TASK-0327-contains-pii-default-ciega-capa-instancia.md`.

**Sin precondiciones.** Toca `scripts/memory/`, igual que 0328 y 0332, asi que hazlas de una en una;
el orden entre ellas da igual.

## Lo medido

    contains_pii("nomina de Acme SL")                 -> False
    contains_pii("nomina de Acme SL", ["Acme SL"])    -> True

`domain_pii_terms: Iterable[str] = ()`. El default **desactiva** la capa de dominio de la instancia.
Seis call sites: tres la pasan y tres NO, heredando el chequeo debil por omision:

- `check_memory_db_drift.py:99` -- el barrido de plano publico del `--full`, o sea **la puerta que
  decide si un artefacto marcado como publicable esta limpio**. Ciega, AUTORIZA publicar PII de
  dominio. Es el peor de los tres con diferencia.
- `build_memory_db.py:762` `require_safe_text` -- la guarda de entrada. Ciega, deja ENTRAR PII al
  indice.
- `query_memory_db.py:205` -- valida el `reason` de una consulta. Ciega, escribe PII en la traza de
  auditoria.

No es una eleccion de diseno: es una INCONSISTENCIA dentro del mismo archivo.

## AC2 es el arreglo real

El bug concreto son tres llamadas; el defecto es la FORMA del default. Un parametro opcional cuyo
valor por defecto debilita el chequeo hace que la omision sea gratis e invisible. Parchear las tres
llamadas deja el motor igual de expuesto al cuarto call site que alguien escriba manana. **Quita el
default** de `contains_pii` y de `title_is_safe` -- omitirlo pasa a ser error de firma, no
degradacion silenciosa.

`title_is_safe` lleva el mismo default vacio pero su unico call site de produccion SI le pasa los
terminos: el agujero esta latente, no abierto. Entra por forma, no por sintoma; dilo asi en el
handoff para que el checker no lo cuente como defecto activo.

## El patron bueno ya esta en tu archivo

`require_safe_text(value, field, *, pii_check: bool = True)` tiene el default en la direccion
CORRECTA: omitirlo deja el chequeo ENCENDIDO, apagarlo hay que escribirlo. A eso se tiene que
parecer el arreglo; no inventes convencion nueva.

**AC4:** un negativo por cada uno de los tres agujeros -- publicacion autorizada, ingesta admitida y
traza escrita con un termino de instancia -- cada uno verificado por MUTACION que cae al revertir la
guarda.

Y mide cuantos artefactos del corpus pasan a marcarse al ensanchar la deteccion en la puerta de
publicacion: es el fix funcionando, pero declara el numero para que nadie lo lea como regresion.

requested_action: Reclamar TASK-0327, quitar el default de las dos funciones, hacer llegar los
terminos de la instancia a los tres call sites ciegos leyendo la politica por blob de git, declarar
los tres negativos y cablearlos en CI, medir el ensanche en la puerta de publicacion, recomputar los
gates en clon limpio y dejar la tarea en in_review con el claim liberado.
