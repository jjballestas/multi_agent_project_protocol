---
decision_id: DRAFT-DECISION-0104
title: "Camino de subida: requisitos para promover al master del hub lo que se probo en una instancia (adopcion + demostracion + neutralidad + entrada al conjunto adoptable + coste en tokens declarado)"
status: draft
date: 2026-07-20
author: Asesor
approved_by: "PENDIENTE DE FIRMA DEL OPERADOR"
relates_to: [DECISION-0006, DECISION-0096, DECISION-0100, DECISION-0103]
---

# DRAFT-DECISION-0104 - El camino de subida

> Redactada por el Asesor a peticion del Operador (20-jul-2026). El Asesor NO firma.
> Contrapeso simetrico de la bajada (DECISION-0006 seccion 4 + SPEC-0019 + `upgrade_instance.py`).

## Contexto (verificado en codigo)

La metodologia tiene un **camino de BAJADA** documentado y con herramienta:
`scripts/upgrade_instance.py` compara el master contra una instancia y emite un reporte
de deltas con acciones recomendadas (adopcion asistida, solo lectura; DECISION-0006 seccion 4,
SPEC-0019). El conjunto adoptable esta declarado en `DEFAULT_ADOPTABLE_GLOBS`.

**No tiene camino de SUBIDA.** Lo que se prueba en una instancia asciende al master
porque alguien decide promoverlo a mano. DECISION-0100 dice "promocion al master hub
Fase 3+" y ahi termina el mecanismo: no hay requisitos, ni checklist, ni verificacion.

Dos consecuencias reales, ambas observadas en julio de 2026:

1. **La memoria hibrida esta ADOPTADA (DECISION-0100 active, firmada el 17-jul) y
   demostrada, y sigue viviendo en una instancia local sin remoto.** No es negligencia:
   la ruta no existe.
2. **Una decision nueva puede no viajar y nadie se entera.** La clausula C5 de la
   DECISION-0103 (armar el harness) iba a quedar fuera de las instancias existentes
   porque `.githooks/**` no estaba en el conjunto adoptable y `new_instance.py` no
   cablea `core.hooksPath`. Se detecto por casualidad, revisando otra cosa.

Regla que resume el hueco: **una regla que no viaja no es del protocolo, es de este repo.**

## Decision

### R0 - LA FIRMA DEL OPERADOR ES LA UNICA QUE PROMUEVE (clausula rectora)

Los requisitos R1-R6 son **condicion NECESARIA y NUNCA SUFICIENTE**. Cumplirlos todos
**no promueve nada**: solo hace la pieza ELEGIBLE. La promocion ocurre unicamente cuando
el Operador la firma, y **puede negarla sin causa tecnica** -- por oportunidad, por
secuencia, por riesgo de dominio, o porque no le convence.

Formulacion operativa: **R1-R6 son un FILTRO, no un DISPARADOR.** Ningun agente,
mecanismo, script ni gate promueve una pieza por el hecho de que el checklist salga
verde. Un checklist completo es una PROPUESTA de promocion, no una promocion.

Corolario contra el efecto perverso: nadie puede argumentar "cumple los seis, luego
sube". Si esa frase llegara a tener fuerza, el checklist habria dejado de ser un filtro
para convertirse en un automatismo con pasos intermedios -- exactamente lo que esta
clausula prohibe.

### Requisitos ACUMULATIVOS de ELEGIBILIDAD

Ninguno es opcional. Sin los seis, la pieza no es siquiera elegible.

### R1 - ADOPTADA por decision firmada en la instancia

Existe una DECISION con `status: active` y firma del Operador que adopta la pieza en la
instancia donde se probo. La promocion al master es una decision SEPARADA: adoptar en una
instancia no es adoptar en la metodologia.

### R2 - DEMOSTRADA end-to-end EN LA INSTANCIA, con evidencia atestada

No basta una suite verde: hace falta **uso real** con evidencia atestada (sha, procedencia,
drift 0, round-trip o equivalente del dominio de la pieza). La pieza se gana el ascenso
**usandose**, no proponiendose.

Referencia de lo que cuenta: la memoria hibrida opero el REVIVE 3 veces end-to-end con
cross-atestacion verificada, y el probe de 6 celdas dejo por escrito que demuestra
capacidad y NO demuestra ahorro. Ese nivel de honestidad sobre lo que NO se demostro es
parte del requisito, no un adorno.

### R3 - NEUTRALIDAD DE DOMINIO

El hub es neutral de dominio y lo verifica en el gate (`scan_domain_neutrality`). Toda
pieza que sube trae su **generalizacion** hecha: fuera nombres, reglas y supuestos del
dominio de origen.

Consecuencia concreta para la primera aplicacion: las reglas de PII de la memoria hibrida
son de NOMINA. Generalizarlas es trabajo real, no un copiar y pegar, y es la primera
unidad de su promocion.

### R4 - ENTRADA EXPLICITA AL CONJUNTO ADOPTABLE

Toda promocion responde POR ESCRITO, y la respuesta es parte del entregable:

- **?que globs** entran a `DEFAULT_ADOPTABLE_GLOBS` (o a `upgrade.adoptable_globs` del
  `protocol.config.json`)?
- **?que cablea `new_instance.py`** al instanciar? (copiar un fichero no arma nada: la
  leccion de `core.hooksPath`).
- **?que reporta `upgrade_instance.py`** como delta a las instancias existentes?

Verificacion: `upgrade_instance.py` corrido contra una instancia real muestra el delta de
la pieza. Si no aparece, la pieza no ha subido -- esta en este repo, nada mas.

### R5 - COSTE EN TOKENS DECLARADO

**Toda pieza que sube al master declara su delta de tokens medido.** No estimado, no
"deberia ser menor": medido, con brazos comparables.

Alcance obligatorio de la medicion -- las tres, no solo la primera:

1. **Coste de USO** (consulta / ejecucion por operacion).
2. **Coste de CONSTRUCCION** (indexar, poblar, inicializar).
3. **Coste de MANTENIMIENTO** (reindexado, drift, actualizacion).

Razon de que las tres sean obligatorias: el resultado de la celda A del probe de memoria
fue "REFUTADO, **overhead-bound por diseno**" -- el coste fijo del mecanismo se comio la
ganancia. Medir solo el uso permite declarar una victoria ignorando el peaje, que es el
mismo error del reves.

**El signo del delta NO es criterio de rechazo.** Una pieza puede subir siendo mas cara si
compra capacidad, correccion o integridad; lo que no puede es subir **sin que se sepa**.
Lo que esta clausula prohibe no es el coste: es la sorpresa.

Metrica recomendada cuando la pieza afecta a recuperacion de contexto: **fidelidad por
token inyectado** -- captura en un solo numero las dos formas de ganar (misma fidelidad
con menos tokens = ahorro; mas fidelidad con los mismos tokens = capacidad) y no permite
elegir a posteriori cual favorece.

### R6 - SUBE LA VERSION DE PROTOCOLO

La promocion incrementa `protocol_version` (y `runtime_version` si toca `runtime/**`),
para que las instancias vean el delta y `upgrade_instance.py` tenga contra que comparar.

## Lo que esta decision NO hace

- **No automatiza la promocion** (ver R0, que es la clausula rectora). Esto fija los
  requisitos de ELEGIBILIDAD, no un mecanismo que promueva solo. Checklist verde =
  propuesta; firma del Operador = promocion.
- **No obliga a promover.** Una pieza puede quedarse en su instancia para siempre; esta
  decision solo dice que si sube, sube completa.
- **No es retroactiva por si sola.** Lo ya promovido no se re-audita salvo orden expresa.

## Primera aplicacion prevista

**La memoria hibrida**, tras el cierre de la ventana de medicion. Su promocion se
descompone naturalmente en las unidades que exigen R3 (generalizacion de dominio, con las
reglas de PII de nomina fuera), R4 (globs + `new_instance` + delta de `upgrade_instance`)
y R5 (los tres costes medidos). R1 y R2 ya los cumple: DECISION-0100 firmada y probe de
6 celdas con lo demostrado y lo NO demostrado por escrito.

Al completarse R1-R6, la memoria hibrida quedara ELEGIBLE. Nada mas. Subira el dia que el
Operador lo firme, y no antes -- aunque el checklist lleve semanas en verde.

-- Asesor, 20-jul-2026. Pendiente de firma del Operador.
