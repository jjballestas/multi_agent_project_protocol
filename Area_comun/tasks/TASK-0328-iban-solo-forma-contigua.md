---
task_id: TASK-0328
file: Area_comun/tasks/TASK-0328-iban-solo-forma-contigua.md
title: "El patron estructural de IBAN solo casa la forma contigua: la agrupacion en bloques de cuatro con que se escribe realmente escapa al patron Y a la banda del heuristico de telefono"
status: in_review
type: infra
owner: Codex
reviewer: Analista
priority: high
project: multi_agent_project_protocol
relates_to:
  - TASK-0314
  - TASK-0322
  - TASK-0327
created_at: 2026-08-07
intake:
  type: fix
  goal: >
    `STRUCTURAL_PII_PATTERNS[1]` es `\b[A-Z]{2}\d{2}[A-Z0-9]{10,30}\b`: exige la forma CONTIGUA.
    Un IBAN escrito como lo escriben las personas -- agrupado en bloques de cuatro, que es la
    presentacion estandar -- no casa. Y tampoco lo rescata el heuristico de telefono: ese captura
    la cadena de digitos y espacios pero luego exige entre 9 y 15 digitos, y un IBAN tiene entre
    15 y 34, asi que cae fuera de la banda por arriba.
    Medido: la forma contigua da True; la agrupada da False, tambien embebida en texto corriente.
    El residual se registro en el ledger del port de TASK-0314 como "R2 IBAN solo en forma
    contigua" y no llego a adjudicarse a ninguna tarea.
  acceptance:
    - "AC1 (falsacion previa): se demuestra sobre el motor real que la forma agrupada devuelve False y que no la rescata ninguna otra guarda, incluido el heuristico de telefono. Se declara por que la banda de 9-15 digitos no la alcanza."
    - "AC2 (deteccion de la forma real): el patron pasa a cubrir la agrupacion en bloques con separadores, manteniendo el rango de longitud valido del formato. La deteccion se mide sobre casos de las dos formas."
    - "AC3 (direccion del fallo, con presupuesto declarado): ensanchar un patron de PII sube el riesgo de falso positivo. Se mide la poblacion de cadenas del corpus que pasan a marcarse y se declara el numero; si aparece un falso positivo, se acota con una guarda que falle CERRADO, nunca relajando la deteccion."
    - "AC4 (interaccion con TASK-0322 declarada): 0322 estrecha las bandas del heuristico. Se verifica y se DECLARA si alguna cobertura de esta tarea dependia incidentalmente de ese heuristico, para que el estrechamiento no abra un hueco por la puerta de atras."
    - "AC5 (contrato): negativo permanente con las dos formas del identificador, declarado en el registro y cableado en CI, verificado por MUTACION que cae al revertir el patron."
    - "AC6 (sin regresion): test_memory_db.py, gates del repo y contratos de falsacion exit 0 en clon limpio."
  verification_cmd:
    - "python scripts/memory/test_memory_db.py"
    - "python scripts/check_falsification_contracts.py --root ."
    - "python scripts/validate_collaboration_state.py --root ."
    - "python scripts/scan_domain_neutrality.py --root ."
  scope_routes:
    - scripts/memory/build_memory_db.py
    - scripts/memory/test_memory_db.py
    - Area_comun/protocol/FALSIFICATION_CONTRACTS.json
  out_of_scope: >
    No se toca el paso de terminos de dominio a los call sites (eso es TASK-0327), ni la exencion
    de fecha (0325), ni las bandas del heuristico de telefono (0322). El patron sigue siendo
    ESTRUCTURAL y neutral: cubre la forma de un identificador de cuenta, sin terminos de negocio.
  risk: medium
  estimate: S
---

# TASK-0328 -- el IBAN solo se detecta si esta escrito de corrido

## Evidencia medida (2026-08-07)

    contains_pii("ES9121000418450200051332")                        -> True
    contains_pii("ES91 2100 0418 4502 0005 1332")                   -> False
    contains_pii("cuenta: ES91 2100 0418 4502 0005 1332 del ...")   -> False

## Por que no lo rescata el heuristico de telefono

`PHONE_CANDIDATE_RE` si captura la cadena de digitos y espacios, pero el filtro posterior exige
`9 <= digitos <= 15`. Un IBAN tiene entre 15 y 34 digitos segun el pais; el del ejemplo tiene 22.
Se sale de la banda por arriba, asi que el candidato se descarta. La guarda existe, mira el valor
correcto y lo deja pasar.

## La ironia que conviene registrar

La forma que el patron SI detecta -- todo de corrido -- es la que produce una maquina. La que NO
detecta es la que produce una persona copiando de su banco, que es exactamente el caso por el que
existe un detector de PII en un corpus de artefactos escritos a mano.

## Riesgo declarado (medium)

Ensanchar un patron con separadores puede empezar a casar cadenas que no son cuentas
(referencias con prefijo de dos letras y bloques numericos). El AC3 obliga a medir la
poblacion afectada y a declarar el numero antes de dar la tarea por cerrada, en vez de
descubrirlo como ruido en produccion.

## Implementacion y medicion de Codex (2026-08-08)

- La deteccion ahora liga la propiedad estructural: prefijo ASCII de dos letras, dos
  digitos de control y cuerpo alfanumerico de 10 a 30 caracteres. Los separadores
  horizontales admitidos pueden aparecer con agrupaciones arbitrarias y mezclarse:
  espacio, tabulador, espacio no separable, espacio fino, espacio fino no separable,
  punto, guion, barra y barra inversa.
- La guarda de checksum sobre el identificador compactado evita aceptar referencias
  ordinarias que solo tienen la misma silueta. Ante un candidato estructural, solo un
  checksum valido abre la deteccion; la evaluacion no degrada silenciosamente a otra
  heuristica.
- AC3 medido sobre las 22,176 cadenas de metadata elegibles del corpus gobernado en
  HEAD: el patron ampliado produjo 10 candidatos nuevos brutos; la guarda rechazo los
  10; cadenas nuevas marcadas: 0; falsos positivos nuevos observados: 0.
- AC4 medido: ni la forma contigua ni la agrupada entra en la banda telefonica de
  9 a 15 digitos. Con el detector estructural desactivado, ambas devuelven False. La
  cobertura de esta tarea no depende del heuristico estrechado por TASK-0322.
- AC5 queda en `NEG-MEMORY-ACCOUNT-IDENTIFIER-PRESENTATION`. El mutante conserva el
  nuevo patron en una rama inalcanzable y restaura como rama viva el patron contiguo:
  la forma contigua sigue dando True y la agrupada cae a False.

## Remediacion 1: limite de avidez y delta bidireccional (2026-08-08)

- El candidato amplio ya no decide por su coincidencia completa. La guarda examina
  prefijos de longitud valida y solo acepta un prefijo con checksum correcto que
  termine ante un separador permitido o el final real de la cadena. Asi, el texto
  posterior puede estar dentro del candidato avido sin contaminar el identificador.
- La expresion conserva el maximo estructural de 34 caracteres compactados. Si el
  candidato termina porque alcanzo ese maximo, la guarda tambien mira el caracter
  siguiente del texto original y rechaza una continuacion alfanumerica sin separar.
- Comparacion bidireccional sobre el mismo corpus gobernado de metadata de HEAD,
  seleccionado con `iter_source_paths` y las claves de `ALLOWLIST_KEYS`: 22,342
  cadenas evaluadas por ambos motores; ganadas: 0; perdidas: 0.
- Corpus permanente de seis fronteras: ganadas frente al motor anterior: 2 (forma
  agrupada aislada y agrupada embebida); perdidas: 1. La unica perdida es una forma
  contigua extendida con `A` cuyo checksum es invalido; se conserva como rechazo
  deliberado. Todos los positivos validos del motor anterior permanecen detectados.
- El mutante permanente sustituye la validacion por prefijo por el checksum de la
  coincidencia completa: las formas aisladas siguen pasando, pero la forma contigua
  embebida vuelve a escapar. El contrato liga directamente la regresion observada.
