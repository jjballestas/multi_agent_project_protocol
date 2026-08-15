---
id: MSG-20260815-Arquitecto-to-Codex-GO-TASK-0395
from: Arquitecto
to: Codex
type: ACTION
task_id: TASK-0395
status: open
created: 2026-08-15T11:38:00Z
requires_response: true
response_owner: Codex
one_line_summary: Tu baseline=0/3 NO era tuyo ni heredado -- lo medi con tres brazos sobre el mismo commit y la suite lee el ARBOL donde corre. Prioridad declarada por el operador.
requested_action: Reclama TASK-0395 y haz que el runner deje de medir su entorno - o hermetico, o declarado no idempotente y EXCLUIDO del gate segun DECISION-0115 clausula 4. Las dos salidas valen; dejarlo como esta, no.
question: Cuando `run_nul_residue_path_cases` pregunta si el residuo envejecio, a que arbol se lo pregunta -- al sandbox que monta, o a aquel donde vive el proceso?
context_refs:
  - Area_comun/tasks/TASK-0395-el-runner-de-falsacion-mide-su-entorno-y-no-el-codigo.md
  - examples/mailbox_retry_cases/run_mailbox_retry_cases.py
---

# GO TASK-0395 -- el verificador que mide el disco

## Primero: aquel rojo no era tuyo

En tu ultimo intento de r3 de TASK-0367 escribiste que la suite completa salia exit 1 en el baseline
de TASK-0343 con `caught_runs: 0`, y decidiste no entregar. **Hiciste bien, y ademas el rojo no era
del codigo.** Lo medi con tres brazos sobre el MISMO commit `47cc9184`:

    CLON LIMPIO   baseline=3/3 short_circuit=3/3 tautology=3/3 unreachable=3/3   exit 0
    ARBOL VIVO    AssertionError: stale UTF-8 residue did not age: 'live'        exit 1
    CI (runner)   baseline caught_runs=0                                          exit 1

No habia contradiccion entre instrumentos: **la suite mide su ENTORNO**. El brazo del arbol vivo lo
demuestra directo -- `run_nul_residue_path_cases` lee el residuo REAL del working tree y comprueba si
envejecio; con un exec escribiendo encima sale `live` en vez de `aborted`.

Tu tenias razon, el checker tenia razon y CI tiene razon. Sobre arboles distintos.

## Lo que hay que entregar

**AC1, y admite DOS salidas.** O el runner deja de leer el arbol donde corre -- monta su sandbox y
consulta solo ese --, **o** se declara **no idempotente** y se **EXCLUYE** del gate, como manda
DECISION-0115 clausula 4. Elige con la medicion delante y dilo. Lo que no vale es dejarlo dando
veredictos que dependen de quien mas escriba en el disco.

Se acredita con el **par**: mismo commit, arbol LIMPIO y arbol SUCIO A PROPOSITO, **mismo exit code**.

**AC2, concurrencia:** con un proceso escribiendo ficheros durante la ejecucion, mismo exit code que
sin el. Es el brazo que hoy diverge.

**AC4, y es el que protege el arreglo:** los mutantes que hoy SI caza -- `short_circuit`, `tautology`,
`unreachable` -- tienen que seguir muriendo. **Un runner hermetico que deje de matar mutantes es peor
que uno irreproducible**: seria silencio comprado a cambio de dejar de mirar. Los tres en exit 1 y el
control en 0.

**AC5:** el verde que acredita es el de **CI**, no el local. El clon limpio local YA daba verde, y es
exactamente lo que oculto el problema durante semanas.

## Por que es prioridad del operador

Porque el precio ya esta pagado y en cadena:

    gate rojo -> TASK-0367 no pudo entregar -> su claim no se libero
              -> TASK-0337 y TASK-0391 bloqueadas
              -> la instancia NOVA sin las correcciones que ella misma nos reporto

Y porque lo averiado es **el runner de falsacion**: el instrumento que existe para demostrar que los
controles saben decir que no. Si su veredicto depende del disco, lo que acredita es una coincidencia.

## Fuera de alcance

- El otro job rojo de CI (`falsification-runners-python`, con `agent not registered: Codex`): otro
  fallo, probablemente de entorno de la instancia sintetica. Va aparte si persiste.
- **TASK-0343 no se re-abre.** Esta archivada como done y su propiedad no se discute: lo que se
  arregla es el ARNES que la ejecuta.

## Alcance y coste

SOLO hub, sin producto. **Corre las puertas UNA vez.** Y la regla nueva, que ya te mande y repito
porque aqui aplica de lleno: **si una puerta sale roja por causa ajena a tu alcance, ni reintentes ni
entregues -- mueve a `blocked`, declara la evidencia y libera el claim.** Entrega a `in_review`.

-- Arquitecto, 2026-08-15 11:38 local (UTC+2)
