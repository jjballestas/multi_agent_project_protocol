---
id: TASK-0390
title: F3 piloto -- primer enfriado REAL, lote acotado a 20 con stub-espejo, rehidratacion byte a byte y vuelta atras probada
status: proposed
owner: Codex
type: implementation
file: Area_comun/tasks/TASK-0390-f3-piloto-de-enfriado-real-acotado.md
created: 2026-08-15
reviewer: Analista
intake:
  type: feature
  goal: >
    Ejecuta DECISION-0116, que activa F3 tras el cierre de F2 (TASK-0373) y con GO explicito del
    operador. Es la PRIMERA operacion del sistema que quita informacion de donde estaba: F1 anadia
    indice, F2 construyo el camino en seco sin mover un byte, y esto mueve artefactos canonicos a
    `Area_comun/archive/cold-packs/` dejando stubs en su lugar. La regla habilitada propone 273
    candidatos; el piloto se acota a **20** por decision del Arquitecto, porque estrenar el mecanismo
    con la poblacion entera convierte la primera ejecucion en el cambio mas grande jamas hecho. El
    lote no se elige por comodidad: DEBE ejercitar la REGLA DE ORO anti-B1 (s.5.3), que existe para
    los artefactos CON punteros del indice fusionado -- un piloto de artefactos sin referencias no
    prueba nada.
  acceptance:
    - "AC1 (lote acotado y REPRESENTATIVO): maximo 20 artefactos, e incluye obligatoriamente al menos
      una tarea referenciada por `file`, una tarea done con `deliverables`, una con `id > TASK-0238`
      y una con `id <= TASK-0238`. Se acredita listando el lote y la razon de cada inclusion ANTES de
      mover. Un lote que esquive los punteros no acredita."
    - "AC2 (la REGLA DE ORO, por conducta): tras el `git mv`, todo puntero `file`/`deliverables` del
      indice fusionado sigue resolviendo a un fichero real, y `validate_collaboration_state.py` da
      exit 0 **en CLON LIMPIO**. No en el arbol caliente: en clon limpio, que es donde el gate del
      peer corre."
    - "AC3 (rehidratacion byte a byte): al menos un artefacto del lote se rehidrata con su
      `rehydration_command` tal como esta escrito, y el resultado es IDENTICO al original por
      sha256 -- no equivalente, no semanticamente igual. Con los dos hashes en la evidencia."
    - "AC4 (la vuelta atras se prueba ANTES de necesitarla): en clon de prueba se ejecuta la
      reversion completa -- rehidratar el lote entero y dejar el arbol como estaba -- y se comprueba
      por `git status` y por sha256 que no queda diferencia. Se acredita ejecutandola, no
      documentandola."
    - "AC5 (AC10 medido con punto de partida): baseline del HOT MAP REAL de s.2.1 ANTES y DESPUES.
      Si no existe baseline previo, se computa antes de mover. Un numero posterior sin punto de
      partida no es un delta."
    - "AC6 (drift y manifiestos): `check_memory_db_drift` verde; cada artefacto movido tiene su fila
      en `pack.manifest.json`, su entrada en `manifest-index.json` y su fila reconstruible en
      `cold_packs`. Sin huerfanos en ninguna direccion."
    - "AC7 (gobernado): tarea con claim sobre rutas origen Y destino, commit con pathspec explicito,
      y NINGUNA ruta bajo claim ajeno tocada. Se acredita con el claim y el pathspec."
  verification_cmd:
    - "python scripts/memory/build_memory_db.py --propose-cold --root ."
    - "python scripts/memory/check_memory_db_drift.py --root . --fast"
    - "python scripts/validate_collaboration_state.py --root ."
    - "python scripts/memory/test_memory_db.py"
    - "python scripts/scan_encoding.py --root ."
  scope_routes:
    - Area_comun/archive
    - scripts/memory/build_memory_db.py
  out_of_scope:
    - "Ensanchar el lote mas alla de 20. Ensanchar es decision posterior CON la medicion delante, y
      exige ademas cerrar TASK-0389 (la frontera de intake duplicada), porque a partir de ahi una
      divergencia silenciosa empieza a mover ficheros de verdad."
    - "El validador archive-aware. La SPEC lo declara tarea F3+ separada con su propia DECISION; el
      piloto se acredita con el validador ACTUAL en verde, sin tocarlo."
    - "F4 (busqueda avanzada) y F5 (operacion). Post-F3."
  risk: high
  estimate: M
---

# TASK-0390 -- el primer enfriado real

## Por que riesgo alto

Porque es la primera vez que este sistema **quita algo de donde estaba**. Todo lo anterior anadia o
derivaba: un indice mal construido se reconstruye, una propuesta en seco se descarta. Un `git mv`
mal hecho deja un puntero colgando en el estado canonico, y el gate que lo detecta es el mismo que
bloquea a los peones.

De ahi que las condiciones que mas pesan no sean las del movimiento sino las de la **vuelta**: AC3
(rehidratacion identica por sha256) y AC4 (reversion completa ejecutada en clon de prueba antes de
tocar el arbol real). La diferencia entre mover y perder es poder deshacerlo, demostrado antes de
necesitarlo.

## Autorizacion

DECISION-0116, con GO explicito del operador el 2026-08-15 tras acreditarse F2.
