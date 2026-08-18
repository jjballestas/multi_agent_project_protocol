---
decision_id: DECISION-0121
title: "Camino de subida: requisitos para promover al master del hub lo que se probo en una instancia (adopcion + demostracion + neutralidad + entrada al conjunto adoptable + coste declarado + registro fuera del config pineado)"
status: accepted
date: 2026-07-20
revised: 2026-08-18
author: Asesor
approved_by: "operador humano (FIRMADA 2026-08-18, en persona)"
relates_to: [DECISION-0006, DECISION-0047, DECISION-0096, DECISION-0100, DECISION-0103, DECISION-0104, DECISION-0110, DECISION-0117, DECISION-0118, TASK-0394, TASK-0417]
---

# DRAFT-DECISION-0121 - El camino de subida

> Redactada por el Asesor a peticion del Operador (20-jul-2026). El Asesor NO firma.
> Contrapeso simetrico de la bajada (DECISION-0006 seccion 4 + SPEC-0019 + `upgrade_instance.py`).
> **Cirugia 2026-08-18**: veredicto adversarial BLOQUEA (tres revisores, unanimidad; dos
> bloqueantes verificados contra el genesis real). El canal asesor ACEPTO el bloqueo por
> delegacion del operador y aplico las enmiendas E1-E8 del veredicto. Renumerada de 0104
> a 0121 (0104 = scratch-root; 0120 = clausula de poda).

## Contexto (verificado en codigo; re-verificado 18-ago)

La metodologia tiene un **camino de BAJADA** documentado y con herramienta:
`scripts/upgrade_instance.py` compara el master contra una instancia y emite un reporte
de deltas (adopcion asistida, solo lectura; DECISION-0006 seccion 4, SPEC-0019). El
conjunto adoptable se deriva en codigo (TASK-0394; desde v1.19.1 transporta arnes y
skills).

**No tiene camino de SUBIDA.** Lo que se prueba en una instancia asciende al master
porque alguien decide promoverlo a mano, sin requisitos ni verificacion. Evidencia
fresca (18-ago): NOVA opera 3 skills que jamas pasaron por el master y su
mailbox-hygiene es un tercer estado; 5 skills vivas del hub no tienen master.

Regla que resume el hueco: **una regla que no viaja no es del protocolo, es de este repo.**

## Decision

### R0 - LA FIRMA DEL OPERADOR ES LA UNICA QUE PROMUEVE (clausula rectora)

Los requisitos R1-R7 son **condicion NECESARIA y NUNCA SUFICIENTE**. Cumplirlos todos
**no promueve nada**: solo hace la pieza ELEGIBLE. La promocion ocurre unicamente cuando
el Operador la firma, y **puede negarla sin causa tecnica**.

Formulacion operativa: **R1-R7 son un FILTRO, no un DISPARADOR.** Un checklist completo
es una PROPUESTA de promocion, no una promocion.

**Limite declarado (E3, medido 18-ago):** la firma del Operador es hoy un acto FUERA del
ledger que ningun gate comprueba. El Operador NO es actor registrado en `agent_registry`
(`human_owner` es un string suelto, no una fila), y el unico actor que puede sellar un
intent `decision` es el Arquitecto. Dotar a R0 de mecanismo exige dar de alta un actor
`human_owner` en el registry, que vive DENTRO del config pineado: esa alta es **llave
exclusiva del operador humano** y solo entra por una re-genesis coordinada futura (queda
en su agenda, sin reloj). Hasta entonces: el sello mecanico lo ejecuta el Arquitecto POR
ORDEN escrita del Operador en el mailbox, y esta clausula LO DECLARA en lugar de afirmar
un mecanismo que no existe.

### Requisitos ACUMULATIVOS de ELEGIBILIDAD

Ninguno es opcional. Sin los siete, la pieza no es siquiera elegible.

### R1 - ADOPTADA por decision firmada en la instancia

Existe una DECISION con `status: active` y firma del Operador que adopta la pieza en la
instancia donde se probo. La promocion al master es una decision SEPARADA.

### R2 - DEMOSTRADA end-to-end EN LA INSTANCIA, con evidencia atestada

No basta una suite verde: hace falta **uso real** con evidencia atestada (sha,
procedencia, drift 0, round-trip o equivalente del dominio de la pieza).

**Unidad contable (E5):** la evidencia declara **N eventos de tipo T en el log
atestado**, con T nombrado por la propia pieza en su intake. Si T no puede nombrarse,
el intake lo ADMITE como juicio humano documentado -- no lo disfraza de medicion.

### R3 - NEUTRALIDAD DE DOMINIO

Toda pieza que sube trae su **generalizacion** hecha: fuera nombres, reglas y supuestos
del dominio de origen.

**Precondicion de instrumento (E6, corregida contra R7):** medido 18-ago,
`scan_domain_neutrality` escanea 0 de 198 ficheros bajo `claude-skills` -- el gate NO
cubre los masters. Antes de invocar el escaner como verificacion de R3, su cobertura se
amplia a `scripts/**/*.md` **por la via que R7 permite** (defaults en el CODIGO de los
dos gemelos del escaner, nunca via `domain_neutrality.scan_globs` del config pineado --
la formulacion original de esta enmienda chocaba con el genesis). Mientras esa ceguera
exista, la neutralidad de un master se verifica con revision humana DECLARADA en el
intake.

### R4 - ENTRADA EXPLICITA AL CONJUNTO ADOPTABLE (E2)

Toda promocion responde POR ESCRITO, y la respuesta es parte del entregable:

- que globs entran a `DEFAULT_ADOPTABLE_GLOBS` **en el codigo de los DOS gemelos**
  (`upgrade_instance.py` y `.ps1`) -- **nunca** via `protocol.config.json` (ver R7);
- que cablea `new_instance.py` al instanciar (copiar un fichero no arma nada);
- el **mapeo `master_rel -> instance_rel`** declarado, y que reporta
  `upgrade_instance.py` como delta **sobre la ruta CONSUMIDA**
  (`<gov>/.claude/skills/...`), no sobre la ruta de staging del hub.

**Puerta de secuencia:** R4 no es exigible hasta que TASK-0394 y TASK-0417 esten en
`done` -- hoy el instrumento que R4 nombra esta medido como falso en los dos sentidos
(corrupto = "igual"; correcto = "nuevo").

### R5 - COSTE EN TOKENS DECLARADO

**Toda pieza que sube declara su delta de tokens medido.** Las tres dimensiones,
no solo la primera: (1) coste de USO, (2) coste de CONSTRUCCION, (3) coste de
MANTENIMIENTO. El signo del delta NO es criterio de rechazo: lo que se prohibe no es el
coste, es la sorpresa.

**Detector (E4, falsabilidad):** el intake de la tarea de promocion contiene los TRES
numeros y el COMANDO que los reproduce; el preflight de intake enrojece si falta
cualquiera de los cuatro. Sin detector, esta clausula seria prosa -- y la memoria
hibrida ya subio sin medirlos (TASK-0314), que es el contraejemplo que este detector
existe para impedir.

### R6 - LA PROMOCION SE REGISTRA FUERA DEL CONFIG PINEADO (E1; sustituye a la version bloqueada)

La promocion se registra en el **CHANGELOG** (linea de release) y en los registries que
viven **FUERA** de `protocol.config.json` (patron DECISION-0047: los dos ejes de
versionado; el epoch solo se mueve en re-genesis). `protocol_version` y
`runtime_version` **NO se tocan**: bajo el pin del genesis, moverlas exige re-genesis, y
una promocion jamas justifica una. La visibilidad para las instancias la da el
**CONTENIDO** (`upgrade_instance` compara ficheros, no versiones -- hub y NOVA declaran
la misma version y difieren en decenas de ficheros) mas la nota de version adoptable.

### R7 - NINGUNA PROMOCION TOCA protocol.config.json (E8)

Si una pieza necesita una clave nueva en el config pineado, la pieza **NO es elegible**:
se rehace para vivir en codigo o en un registry externo, o se escala como re-genesis --
que es una decision APARTE, del operador humano en persona, y nunca parte de una
promocion. Medido tres veces esta semana: cualquier escritura al config produce
`genesis mismatch` sobre la cadena entera.

## Lo que esta decision NO hace

- **No automatiza la promocion** (R0 es la clausula rectora).
- **No obliga a promover.** Una pieza puede quedarse en su instancia para siempre.
- **No es retroactiva por si sola.** Lo ya promovido no se re-audita salvo orden expresa.
- **No incluye el generador de masters como mecanismo**: la medicion del 18-ago mostro
  que el 86,2 por ciento del hueco vivo-master es juicio editorial sin token derivable
  (el mejor oraculo construible cubre el 4,6 por ciento). Si algun dia existe un
  generador, entrara por su propia decision con su propia medicion.

## Primera aplicacion prevista (corregida 18-ago)

La **PROXIMA promocion que ocurra** -- candidatas reales: las skills del conjunto de
masters (cuando 0394/0417 cierren la puerta de secuencia de R4) y las piezas de la ola
v1.19.2. La memoria hibrida **ya subio sin este camino** (TASK-0314 `done` 2026-08-06,
sin mediciones de coste): NO se re-audita salvo orden expresa del Operador, y su deuda
R5 queda anotada como candidata a esa orden. Este parrafo existe para que la decision no
nazca afirmando una aplicacion que ya se consumio.

-- Asesor, 20-jul-2026; cirugia E1-E8 del 18-ago-2026. Pendiente de firma del Operador.
