---
id: TASK-0364
title: La CI canonica pasa a runners propios, y el estado acumulado entre corridas se vigila por conducta
status: in_progress
owner: Codex
type: infra
file: Area_comun/tasks/TASK-0364-la-ci-canonica-pasa-a-runners-propios.md
created: 2026-08-12
intake:
  type: infra
  goal: >
    Ejecuta DECISION-0112. El cupo de Actions de esta cuenta (GitHub Free, 2.000 min/mes) es nueve
    veces menor que lo que la cadencia consume (~18.000 min/mes: 39-56 runs/dia por ~13 minutos
    facturables), y el operador descarta tanto subir el limite (~130-150 $/mes) como hacer publico el
    repositorio -- que ademas prohibiria los runners propios por seguridad. Hay dos runners propios
    registrados y en verde, `protocol-win` y `protocol-linux`, y esta medido con control en la misma
    corrida (run 31581821440) que un job self-hosted arranca y ejecuta pasos reales mientras el job
    GitHub-hosted del mismo run queda bloqueado a 0 pasos, sin consumir facturacion. Esta tarea mueve
    los cuatro jobs de `.github/workflows/validate.yml` a los runners propios. El riesgo NO es el
    coste sino el opuesto: un runner GitHub-hosted nace limpio en cada corrida y uno propio NO, asi
    que el estado acumulado entre corridas puede producir un verde que el arbol limpio no produciria.
    Ese riesgo se cierra por CONDUCTA, con un par sucio/limpio, no con una declaracion de higiene.
  acceptance:
    - "AC1 (colocacion por dependencia REAL, derivada): cada job se coloca en el runner que su dependencia exige y se declara uno a uno por que va donde va. `falsification-runners` va a protocol-win porque ejercita Windows PowerShell 5.1 -- el interprete real de produccion, mas fiel que windows-latest. `powershell-linux-parity` va a protocol-linux porque existe para probar pwsh 7 SOBRE LINUX. No se coloca nada por donde estaba antes."
    - "AC2 (el entorno sucio se detecta, medido con el PAR): se ensucia el arbol de trabajo del runner a proposito antes de un run -- un `.pyc` obsoleto de un modulo que despues cambia, y un artefacto residual que el gate deberia rechazar -- y el run lo detecta o lo elimina. Se acredita con las DOS corridas: sucio -> el run lo caza; limpio -> pasa. Un run que pase en los dos casos NO acredita nada y es el falso verde que este AC existe para impedir."
    - "AC3 (el saldo se compara contra el clon limpio): el saldo paso a paso del job `validate` en el runner propio se compara con `scripts/replay_validate_job.py` sobre un clon limpio del MISMO ancla. Se reporta la tabla de divergencias. Cualquier paso que pase en el runner y falle en el clon limpio (o al reves) es contaminacion de entorno y se declara con su causa; no se ajusta el clon limpio para que coincida."
    - "AC4 (el entorno se publica en el propio run): cada job declara en su log la version de su interprete -- Python, pwsh y, en el de Windows, PowerShell 5.1 -- de modo que un cambio silencioso del host aparezca en el run y no en un veredicto tres semanas despues."
    - "AC5 (cero perdida de cobertura): el conjunto de pasos ejecutados tras el cambio es el MISMO que antes. Se acredita comparando los dos conjuntos derivados del YAML, no afirmando que no se quito nada."
    - "AC6 (la reversion es una etiqueta): se acredita que devolver un job a GitHub-hosted es un cambio de una linea en `runs-on`, sin migracion ni efecto sobre el ledger. Se prueba revirtiendo uno y volviendolo a mover."
    - "AC7 (cerrado en un run REAL, citado): los cuatro jobs se observan en un run real de GitHub Actions sobre los runners propios, citando la terna run_id + job + head_sha, y se acredita con `timing.billable` que el consumo facturado es cero."
  verification_cmd:
    - "python scripts/replay_validate_job.py --root ."
    - "python scripts/validate_collaboration_state.py --root ."
    - "python scripts/scan_encoding.py --root ."
  scope_routes:
    - .github/workflows/validate.yml
  out_of_scope:
    - "La dieta de triggers (`branches: [main]`, `paths-ignore: personal/**`): tiene su propia contrapartida de granularidad de biseccion y va en decision aparte, no se cuela aqui."
    - "Los rojos de fondo del job `validate`: son TASK-0340, TASK-0347 y la cascada 0349-0352. Esta tarea cambia el HOST, no arregla los pasos. Es esperable que el job siga rojo por esas causas, y eso NO la bloquea."
    - "La persistencia de los runners como servicio del sistema: es operativa, exige consola elevada y no es protocolar."
    - "La visibilidad del repositorio y su licencia, fijadas por DECISION-0010."
  risk: medium
  estimate: S
---

# TASK-0364 -- el host de la puerta canonica

## Por que ahora

DECISION-0112, aprobada por el operador el 2026-08-12. La medicion que la sostiene esta en el run
`31581821440`, y lo que la hace valer es el **control en la misma corrida**:

    control  ubuntu-latest (GitHub-hosted)   BLOQUEADO   0/0 pasos   12 s
    probe    self-hosted Linux               SUCCESS     8/8 pasos   16 s
    probe    self-hosted Windows             SUCCESS     8/8 pasos   75 s
    timing.billable  ->  UBUNTU total_ms=0 (el control). Los self-hosted no aparecen.

## Lo que esta tarea NO es

No es una optimizacion de coste que se acredita enseniando una factura mas baja. **El coste ya esta
resuelto por construccion**: los minutos propios no se miden. Lo que esta tarea tiene que acreditar es
lo contrario: que el ahorro **no se paga en fiabilidad**.

## El riesgo, dicho sin rodeos

Un runner GitHub-hosted nace limpio en cada corrida. Uno propio **no**: reutiliza `_work`, conserva
caches de pip, `.pyc`, variables de entorno del host y lo que un job anterior dejo a medias. Esta
instancia lleva semanas cazando exactamente esa clase de falso verde -- los `.pyc` que descuadran un
conteo, el arbol caliente que miente, el verde que el codigo viejo tambien produce.

Por eso el AC2 no pide higiene: pide el **par**. Sucio tiene que cazarse, limpio tiene que pasar. Un
instrumento que da verde en los dos casos no distingue nada, y ya nos ha pasado.

## Lo que desbloquea

    TASK-0340  AC6  "un run REAL de GitHub Actions, citando el id"   -> se cumple al pie de la letra
    TASK-0347  AC7  idem                                            -> sale de blocked
    TASK-0342                                                       -> puede cerrar

Un run en runner propio es un run autentico de Actions, orquestado por GitHub, con `run_id`, `job` y
`head_sha` citables. Lo unico que cambia es donde ocurre el computo.

## Precedencia

Va **despues** de que TASK-0354 cierre: comparten `.github/workflows/validate.yml`, y su checker esta
juzgando ahora mismo un texto cuya afirmacion central es que ese fichero no se toca.
