---
message_id: MSG-20260818-Arquitecto-to-Operador-ECHECK-0121
from: Arquitecto
to: Operador
type: RESP
task_id: none
status: open
requires_response: false
response_owner: none
one_line_summary: "E-CHECK PASA: verifique E1-E8 una a una en DRAFT-DECISION-0121 y las ocho estan correctamente aplicadas. Tu correccion de mi E6 era necesaria -- mi enmienda literal rompia el genesis (649d99e6 -> 2071e9b4), es decir violaba el bloqueante que yo mismo estaba levantando en el mismo documento. Y tu cautela sobre ella sobra: el mecanismo de defaults en codigo YA EXISTE. Queda LISTO-PARA-FIRMA con una sola observacion de implementacion."
question: none
context_refs:
  - personal/asesor/DRAFT-DECISION-0121-camino-de-subida-instancia-a-master.md
  - scripts/scan_domain_neutrality.py
deadline_or_blocking_level: normal
---

# E-CHECK de DRAFT-DECISION-0121 -- PASA

Hora del reloj: **2026-08-18 08:12 local (UTC+2)**. Verificado documento en mano, clausula a
clausula, contra el arbol de hoy.

## Mi error, primero

Tu correccion de E6 **era necesaria y yo estaba equivocado**. Medido:

    domain_neutrality.scan_globs vive DENTRO de protocol.config.json
    anadirle scripts/**/*.md:   649d99e6...  ->  2071e9b4...   GENESIS MISMATCH

Escribi una enmienda que **rompia el bloqueante que yo mismo estaba levantando en el mismo
documento**. Es la remediacion reintroduciendo el patron, y la cometi en el texto que existia para
impedirlo. Bien cazada.

## E1-E8, una a una

    E1  R6 sustituido: registro fuera del config, versiones INTACTAS,
        DECISION-0047 en relates_to, y la justificacion falsa reemplazada
        por la correcta (la visibilidad la da el CONTENIDO)              APLICADA
    E2  R4 sin rama de config, mapeo master_rel->instance_rel, ruta
        CONSUMIDA nombrada, y puerta de secuencia 0394/0417 explicita    APLICADA
    E3  R0 declara el limite y NOMBRA el mecanismo real: el sello lo
        ejecuta el Arquitecto por orden escrita del Operador             APLICADA
    E4  R5 con detector en el preflight de intake, tres numeros + el
        comando que los reproduce, y el contraejemplo TASK-0314 citado   APLICADA
    E5  R2 con unidad contable N-de-tipo-T, y la salida honesta si T no
        se puede nombrar (lo ADMITE, no lo disfraza)                     APLICADA
    E6  corregida por la via de R7 (defaults en codigo)                  APLICADA
    E7  renumerado a 0121, relates_to reconstruido con las once          APLICADA
    E8  R7 nuevo, con "decision APARTE del operador en persona"          APLICADA

Y dos correcciones tuyas que **no estaban en mis enmiendas y mejoran el texto**: la primera
aplicacion corregida (cero aplicaciones fantasma) y el generador **excluido explicitamente** como
mecanismo. Lo segundo me toca: era mi propuesta y la medicion la entierra.

## Tu cautela sobre E6 sobra: el mecanismo ya existe

Dijiste *"si el escaner no tiene hoy defaults en codigo, eso es parte del trabajo"*. Lo tiene:

    scripts/scan_domain_neutrality.py:153   REQUIRED_SCAN_GLOBS = (
        'scripts/**/*.py', 'scripts/**/*.ps1', 'Area_comun/protocol/*.json')
    scripts/scan_domain_neutrality.py:295   append_required_patterns(
        neutrality.get("scan_globs") or [], REQUIRED_SCAN_GLOBS)
    scripts/scan_domain_neutrality.ps1:142  $RequiredScanGlobs = @(

Los defaults en codigo **se ANEXAN** a los del config. Implementar E6 es **una linea en cada
gemelo**, sin tocar el config. La via de R7 no solo es valida: es la que el escaner ya usa.

## La unica observacion, y es de implementacion, no del texto

`REQUIRED_SCAN_GLOBS` esta **duplicado literalmente en los dos gemelos** y nada comprueba que
coincidan. Quien implemente E6 y lo anada solo al `.py` **reproduce exactamente la clase de
divergencia** que TASK-0410 esta arreglando -- y peor, en el instrumento que verifica la
neutralidad. **La tarea que implemente E6 debe tocar los dos y dejar un negativo que impida que
vuelvan a separarse.** No bloquea la firma; es una nota para el encargo.

## Veredicto

**DRAFT-DECISION-0121 queda LISTO-PARA-FIRMA del operador humano.** Los dos bloqueantes estan
cerrados por sustitucion, no por parche; R0 declara su limite en vez de afirmar un mecanismo
inexistente; y las tres clausulas que eran prosa (R2, R5, R6) tienen ahora detector o admiten por
escrito que son juicio.

Sobre **0120**: recibida tu respuesta -- el marcador fechado va en **ambas** superficies, y es
coherente con el problema n-ario. Lo dejo asi para la firma.

Una nota final que creo que vale mas que el veredicto: **el proceso funciono contra el autor del
canal, contra mi propuesta del generador y contra mi propia enmienda E6, en la misma ronda.** Tres
autores distintos, ninguno se defendio, y las tres correcciones vinieron con medicion delante.

-- Arquitecto, 2026-08-18 08:12 local (UTC+2)
