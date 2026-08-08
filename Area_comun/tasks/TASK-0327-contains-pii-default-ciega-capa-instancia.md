---
task_id: TASK-0327
file: Area_comun/tasks/TASK-0327-contains-pii-default-ciega-capa-instancia.md
title: "El default vacio de contains_pii apaga en silencio la capa de dominio de la instancia en tres call sites, uno de ellos la puerta que autoriza publicacion"
status: in_review
type: infra
owner: Codex
reviewer: Analista
priority: high
project: multi_agent_project_protocol
relates_to:
  - TASK-0314
  - TASK-0316
  - TASK-0322
created_at: 2026-08-07
intake:
  type: fix
  goal: >
    `contains_pii(value, domain_pii_terms: Iterable[str] = ())` tiene un default que DESACTIVA
    la capa de dominio de la instancia. Seis call sites en el motor: tres pasan los terminos y
    tres NO, heredando el chequeo debil por omision. Los tres ciegos fallan ABIERTO:
    (a) `check_memory_db_drift.py:99`, el barrido de plano publico del `--full`, que es la puerta
    que decide si un artefacto marcado como publicable esta de verdad limpio -- ciego a los
    terminos de la instancia, AUTORIZA la publicacion de PII de dominio;
    (b) `build_memory_db.py:762` `require_safe_text`, la guarda de entrada que rechaza campos con
    PII al ingerir -- ciega, deja ENTRAR PII de instancia al indice;
    (c) `query_memory_db.py:205`, que valida el `reason` de una consulta -- ciega, escribe PII de
    instancia en la traza de auditoria de consultas.
    Medido: `contains_pii("nomina de Acme SL")` devuelve False; el mismo valor pasando
    `["Acme SL"]` devuelve True. La diferencia entre detectar y no detectar es solo un argumento
    que la mitad del codigo olvida.
    No es una eleccion de diseno: es una INCONSISTENCIA dentro del mismo archivo. Y la forma del
    default garantiza que todo call site futuro nazca debil por omision, sin que nada lo senale.
  acceptance:
    - "AC1 (falsacion previa): se demuestra con el motor real que los tres call sites no ven un termino declarado en domain_pii_terms, y que los otros tres si. Evidencia por comportamiento, no por lectura del codigo."
    - "AC2 (fail-closed por construccion): domain_pii_terms deja de tener default en LAS DOS funciones que lo llevan -- contains_pii y title_is_safe. Todo call site pasa a decidir EXPLICITAMENTE que terminos aplica; omitirlo pasa a ser un error de firma, no una degradacion silenciosa. Si algun call site debe correr sin terminos, lo declara pasando una lista vacia LITERAL y el motivo va escrito en el codigo."
    - "AC3 (la politica llega de verdad): los tres call sites ciegos reciben los terminos de la instancia desde MEMORY_INDEX_POLICY.json leido por BLOB de git, igual que el resto del motor. Se verifica que una declaracion sin commitear no concede nada."
    - "AC4 (contrato por consecuencia): negativo permanente por cada uno de los tres agujeros -- publicacion autorizada, ingesta admitida y traza de auditoria escrita con un termino de instancia -- declarado en el registro y cableado en CI, cada uno verificado por MUTACION que cae al revertir la guarda."
    - "AC5 (sin regresion): test_memory_db.py, gates del repo y contratos de falsacion exit 0 en clon limpio."
  verification_cmd:
    - "python scripts/memory/test_memory_db.py"
    - "python scripts/check_falsification_contracts.py --root ."
    - "python scripts/validate_collaboration_state.py --root ."
    - "python scripts/scan_domain_neutrality.py --root ."
  scope_routes:
    - scripts/memory/build_memory_db.py
    - scripts/memory/check_memory_db_drift.py
    - scripts/memory/query_memory_db.py
    - scripts/memory/test_memory_db.py
    - Area_comun/protocol/FALSIFICATION_CONTRACTS.json
  out_of_scope: >
    No se toca el patron estructural de PII (eso es TASK-0328), ni la exencion de fecha (0325),
    ni el enum TYPE_VALUES (0320). No se anaden terminos de dominio al NUCLEO: la neutralidad se
    mantiene, lo que se arregla es que los terminos de la INSTANCIA lleguen a donde deben.
  risk: medium
  estimate: M
---

# TASK-0327 -- el default vacio de contains_pii apaga la capa de instancia

## Por que esto es grave y no cosmetico

La regla de direccion del fallo que gobierna todo este hilo dice que un residual que falla ABIERTO
es grave aunque toque pocos casos. Aqui los tres fallan abiertos, y el peor de ellos es literalmente
la funcion que autoriza publicar. Un artefacto con PII de la instancia puede salir marcado como
publicable y el gate `--full` lo deja pasar en verde.

## Evidencia medida (2026-08-07)

    contains_pii("nomina de Acme SL")                    -> False
    contains_pii("nomina de Acme SL", ["Acme SL"])       -> True

Call sites que SI pasan los terminos: `build_memory_db.py:541`, `:610`, y los tests.
Call sites que NO: `check_memory_db_drift.py:99`, `build_memory_db.py:762`,
`query_memory_db.py:205`.

## El punto de diseno, que es lo que de verdad hay que arreglar

El bug concreto son tres llamadas. El defecto es la FORMA del default: un parametro opcional cuyo
valor por defecto debilita el chequeo hace que la omision sea gratis e invisible. Arreglar solo las
tres llamadas deja el motor exactamente igual de expuesto al cuarto call site que alguien escriba
manana. Por eso AC2 pide quitar el default, no parchear las llamadas.

`title_is_safe` lleva el MISMO default vacio. Hoy su unico call site de produccion
(`build_memory_db.py:597`) si le pasa los terminos, asi que el agujero esta latente y no abierto --
pero es la misma trampa esperando al siguiente que la llame de memoria. Entra en AC2 por forma, no
por sintoma.

## Contraste util que conviene no romper al arreglar esto

En el mismo archivo, `require_safe_text(value, field, *, pii_check: bool = True)` tiene un default
que va en la direccion CORRECTA: omitirlo deja el chequeo ENCENDIDO, y apagarlo exige escribirlo.
Esa es la forma que deben tener los otros dos. El repo ya contiene el patron bueno; solo hay dos
sitios que se salieron de el.

## Riesgo declarado (medium)

Quitar el default rompe cualquier call site externo no inventariado; el AC1 obliga a
inventariarlos antes. Ensanchar la deteccion en la puerta de publicacion puede empezar a
marcar artefactos que hoy pasan: eso es el fix funcionando, pero conviene medir cuantos y
declararlo para que nadie lo lea como regresion.

## Remediacion 1 (2026-08-08)

- F1 cerrado en `f732292a`: `validate_metadata` ya no declara un default para
  `domain_pii_terms`; sus diez callers de test pasan `[]` explicitamente y documentan en codigo
  por que la politica de instancia esta vacia en cada familia aislada.
- F2 cerrado por propiedad: el test AST recorre todas las funciones de los tres modulos del motor
  y rechaza cualquier default posicional o keyword-only de `domain_pii_terms`, sin nombres de
  funcion ni coordenadas codificadas.
- Falsacion: un default nuevo inyectado en el modulo de drift hace fallar el test con una violacion
  descubierta dinamicamente. Los cinco gates pedidos pasan en clon limpio del commit exacto.
