# DRAFT DECISION-0112 -- la CI canonica pasa a runners propios

    estado        BORRADOR -- requiere aprobacion del operador (AGENTS.md s.4: cambia el host del gate canonico)
    autor         Arquitecto
    fecha         2026-08-12
    supersede     nada; complementa DECISION-0010 (visibilidad privada) y el residual de facturacion de TASK-0354

## 1. El problema, medido

    plan real                     GitHub Free -- 2.000 minutos de Actions/mes
    Copilot Pro (10 $/mes)        aporta CERO minutos de Actions
    cadencia medida               39 y 56 runs/dia (10 y 11 de agosto); 3.208 runs historicos
    coste por run                 ~13 min facturables (4 jobs, cada uno redondeado al minuto,
                                  el de Windows a doble tarifa)
    necesidad                     ~18.000 min/mes  =  NUEVE veces el cupo

Ninguna dieta de triggers cierra un factor nueve. Aunque se eliminara el 100% de los commits de
memoria (211 de 795 en siete dias) y el 45% de corridas superadas, quedarian ~7.000 min/mes.

Las dos salidas descartadas por el operador, y por que:

- **Subir el limite de gasto:** ~130-150 $/mes al ritmo actual, y subiendo -- `validate` abortaba en el
  paso 28 de 77, asi que cuando la cascada cierre cada run durara mas.
- **Hacer publico el repositorio:** daria minutos ilimitados, pero DECISION-0010 fija visibilidad
  privada y licencia propietaria, y la exposicion es irreversible. Ademas **se muerde la cola**: los
  runners propios en un repositorio publico son un agujero de seguridad conocido (un PR ajeno ejecuta
  codigo en la maquina del operador). Publicar prohibiria el arreglo gratuito.

## 2. Lo que ya esta medido, no supuesto

Run `31581821440`, con job de control en la MISMA corrida:

    control  ubuntu-latest (GitHub-hosted)   BLOQUEADO   0/0 pasos   12 s
    probe    self-hosted Linux               SUCCESS     8/8 pasos   16 s
    probe    self-hosted Windows             SUCCESS     8/8 pasos   75 s
    timing.billable  ->  UBUNTU total_ms=0 (el control). Los self-hosted no aparecen en el desglose.

Los pasos no eran simbolicos: checkout, interprete, y el gate real `scan_encoding`. El runner de Linux
ejecuta ademas el gemelo PowerShell sobre Linux; el de Windows acredita PowerShell 5.1.

**El bloqueo por facturacion no alcanza a los runners propios, y sus minutos no se facturan.**

## 3. Decision propuesta

1. El job `falsification-runners` pasa a `[self-hosted, protocol-win]`. **Gana fidelidad**: el
   PowerShell 5.1 del host de produccion real, que es exactamente lo que ese job existe para ejercitar,
   en vez del de un runner efimero.
2. Los jobs `validate`, `powershell-linux-parity` y `falsification-runners-python` pasan a
   `[self-hosted, protocol-linux]`.
3. Se conserva `workflow_dispatch` y la guarda de concurrencia ya existente.
4. **No se retira** la posibilidad de volver a GitHub-hosted: el cambio es una etiqueta en `runs-on`.

## 4. El riesgo que hay que escribir, no suponer

Un runner GitHub-hosted nace limpio en cada corrida. **Uno propio acumula estado entre corridas** --
`_work` reutilizado, caches de pip, `.pyc`, variables de entorno del host, ficheros que un job anterior
dejo a medias. Es exactamente la clase de falso verde que esta instancia lleva semanas cazando:
[[leccion-medir-cobertura-en-clon-limpio]] (los `.pyc` descuadran el conteo),
[[checker-clean-clone-no-residual-artifacts]] (el working tree caliente miente).

**Mitigacion, y va como criterio de aceptacion por CONDUCTA, no como declaracion:**

- AC-A: se ensucia `_work` a proposito antes de un run -- un `.pyc` obsoleto, un artefacto residual de
  un job anterior, un fichero que el gate deberia rechazar -- y **el run lo detecta o lo elimina**. Se
  acredita con el par: sucio -> se detecta; limpio -> pasa. Un run que pase en ambos casos no acredita.
- AC-B: el saldo del job `validate` en el runner propio se compara paso a paso contra
  `replay_validate_job.py` en clon limpio. Divergencia = contaminacion de entorno, y se declara.
- AC-C: el runner declara su entorno en el propio run (version de Python, de pwsh, de PowerShell 5.1),
  de modo que un cambio silencioso del host aparezca en el log y no en un veredicto.

## 5. Lo que esto desbloquea

- **TASK-0340 (AC6)** pide *"el job `validate` sale success en un run REAL de GitHub Actions, y se cita
  el id del run"*. Un runner propio produce un run autentico de Actions, orquestado por GitHub, con
  run_id / job / head_sha citables. **El AC se cumple al pie de la letra**; lo unico que cambia es donde
  ocurre el computo. Sale de `blocked`.
- **TASK-0347 (AC7)**, idem. Su propio texto ya dice que la tarea *"puede entregarse y revisarse sin el,
  pero no cierra sin el"*: lo que estaba bloqueado era el cierre, no el trabajo.
- **TASK-0342** puede cerrar.
- Detras esperan 0349, 0350, 0351 y 0352, los cinco rojos de causa ajena que 0347 dejo fuera de alcance.

## 6. Lo que NO decide esto

- No decide la dieta de triggers (`branches: [main]`, `paths-ignore: personal/**`). Va aparte, porque
  el `paths-ignore` tiene su propio trade -- pierde granularidad de biseccion, el mismo que AC2 de
  TASK-0354 ya acepto para la cancelacion -- y debe declararse, no colarse.
- No decide la persistencia de los runners como servicio: `svc.cmd install` exige consola elevada. Hoy
  arrancan por la carpeta Startup, que sobrevive al reinicio pero no al cierre de sesion sin login.
- No toca la visibilidad del repositorio ni la licencia.

## 7. Reversion

Una linea por job: devolver `runs-on` a `ubuntu-latest` / `windows-latest`. Sin migracion de datos, sin
efecto sobre el ledger. Si el runner propio resultara contaminado, AC-A lo detecta antes de que un
veredicto se apoye en el.
