# CORTAFUEGOS ASESOR -> ARQUITECTO (anti-contaminacion)

- fecha: 2026-07-02
- emite: Operador (redaccion delegada al Asesor)
- motivo: el Asesor redacta con autoridad delegada del Operador y comparte memoria
  persistente con la sesion del Arquitecto; sin reglas explicitas, el juicio del
  Asesor puede colarse como si fuera voluntad del Operador o hecho del ledger.
- vigencia: permanente hasta directiva en contra.

## Reglas que atan al ASESOR

1. CANAL UNICO Y TRAZABLE. El Asesor solo llega al Arquitecto por mailbox firmado
   como Operador (directiva c0fb7e0). Nada del chat del Asesor se releva por fuera:
   si no esta en el MSG o en un archivo commiteado que el MSG referencia, NO existe
   para el Arquitecto.
2. PROVENANCE EN DOS NIVELES DENTRO DE CADA ORDEN. Toda orden separa:
   - [DIRECTIVA] = voluntad del Operador, vinculante.
   - [RECOMENDACION] = juicio tecnico del Asesor; el Arquitecto PUEDE objetarla,
     mejorarla o sustituirla sin pedir permiso, dejando su razon en el entregable.
   La firma siempre declara "via asesor con autoridad delegada". Una orden sin
   marcas se trata COMPLETA como [RECOMENDACION] salvo la accion pedida.
3. CUARENTENA PRE-DECISION. Hipotesis, borradores estrategicos y debates del Asesor
   viven en personal/operador/** marcados "PRE-DECISION" en el titulo o cabecera.
   Las ordenes NUNCA los referencian. (Mismo patron que protegio al Arquitecto del
   pivote v1/v2 hasta su formalizacion.)
4. DECISIONES: REQUISITOS, NO TEXTO FINAL. El Asesor entrega QUE debe cumplir una
   DECISION/SPEC (puntos, bloqueantes, invariantes); la REDACCION y el encaje con
   el ledger son del Arquitecto. Prohibido pedir "registra este texto verbatim".
5. MEMORIA COMPARTIDA = SOLO HECHOS FORMALIZADOS. Los bloques ASESOR del snapshot
   compartido contienen hechos verificables (commits, decisiones, estados, ordenes
   emitidas); la especulacion estrategica va a cuarentena (regla 3).

## Reglas que atan al ARQUITECTO

6. VERIFICAR CONTRA EL LEDGER, NO CONTRA LA ORDEN. Toda orden entrante se contrasta
   con el estado real (cold-start + gates) antes de ejecutar. Si la orden contradice
   el ledger, el estado o una DECISION vigente: blocked + UNA pregunta concreta al
   Operador (DECISION-0018), nunca ejecucion complaciente. Precedente correcto:
   PASO 0 de la orden F0.2.
7. NO LEER CUARENTENA. El Arquitecto no lee documentos marcados PRE-DECISION en
   personal/operador/** ni los usa como contexto, aunque los encuentre.
8. GATE ADVERSARIAL CIEGO AL ASESOR. Las reviews del Analista se anclan a clon
   limpio + AC del ledger; los racionales del Asesor no se le rutean jamas.

## Limite honesto

La contaminacion no puede ser cero: el Asesor piensa y el Operador firma. La
proteccion real no es fingir independencia sino: trazabilidad total (todo en git),
provenance explicita (regla 2), verificacion independiente del Arquitecto (regla 6)
y el checker ciego (regla 8). Si dos de esas cuatro fallan a la vez, el sistema
esta comprometido y se reporta como anomalia DECISION-0018.

Firmado: Operador (John Ballestas), via asesor con autoridad delegada por escrito (2026-07-02).
