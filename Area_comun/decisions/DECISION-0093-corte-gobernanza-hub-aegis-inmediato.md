---
decision_id: DECISION-0093
title: "Corte de gobernanza hub->Aegis INMEDIATO (complemento formal de DECISION-0088): lo medido de Etapa 1 permanece en el hub; toda gobernanza nueva de la suite Nova nace en la instancia Aegis, con cross-atestacion dual cableada desde el arranque"
status: accepted
date: 2026-07-06
deciders: [operador humano, Arquitecto]
supersedes: []
supersedes_partial: [DECISION-0088]
superseded_by: []
relates_to: [DECISION-0088, DECISION-0050, DECISION-0085, DECISION-0087, DECISION-0091, GOAL-VISION-NOVA-001]
phase: P2
scope: governance
approval_ref: "Ordenado por el Operador (John Ballestas) 2026-07-06: DIRECTIVA MSG-20260706-Operador-to-Arquitecto-ACTION-corte-aegis-cola-reqs-contabilidad (commit 30a4252, seccion 1: 'formaliza el corte como complemento FORMAL de DECISION-0088 -- es formalizacion NECESARIA, no opcional') + autorizacion explicita de la verificacion de firmantes (MSG-20260706-Operador-to-Arquitecto-ACTION-autoriza-aegis-firmantes-paso2-recuerda-html, commit b715d95). Frontera de governance -> aprobacion humana registrada."
---

# DECISION-0093 - Corte de gobernanza hub->Aegis inmediato (complemento de DECISION-0088)

> Contexto: DECISION-0088 fijo el escalonamiento hub-ahora / instancia-despues con trigger de
> migracion "tras SELLAR y MEDIR la Etapa 1" (su punto 4). El Operador, tras revisar el alcance
> total del legado Ingenas (~13 modulos, ~452 formularios; Nova-Budget cubre ~25%) y confirmar el
> brazo BASELINE completo, ordeno ejecutar el corte AHORA con una particion mas fina que el texto
> de 0088 autorizaba explicitamente: lo que el estudio mide sigue en el hub hasta terminar; lo
> NUEVO de la suite (Contabilidad en adelante, REQs de instancia/producto) nace directamente en
> Aegis. Sin este complemento quedaria drift ("el corte contradijo 0088"). Esta decision es ese
> complemento formal; no es un cambio de rumbo sino un refinamiento del trigger.

## Decision

1. **Particion por CONTENIDO, no solo por tiempo (refina 0088 punto 3/4):**
   - **Hub (este repo) = Etapa 1 COMPLETA + protocolo neutral.** Permanecen en el hub hasta su
     cierre natural: el sello de Etapa 1 (DECISION-0091), el sorteo, el journal de medicion, el
     Sprint 1 gobernado (abre 2026-07-30), la reconciliacion 26-29-jul, el reporte de Etapa 1, y
     la evolucion del nucleo neutral del protocolo. El asiento del ESTUDIO no se mueve a mitad
     de medicion (misma razon dura de 0088 punto 3).
   - **Instancia Aegis (`D:/Agentes/Zeus/NOVA/Aegis`, pin v1.18.0, perfil governed-instance) =
     TODA gobernanza nueva de la suite Nova.** Nacen en el ledger de Aegis, no en el hub: tareas,
     claims, mailbox y atestacion de Contabilidad en adelante (modulos 2..11 del orden de negocio
     fijado por el Operador), y las DECISIONes de los REQs futuros cuando su ambito sea
     instancia/producto (anti-vibecoding, intake profesional, memoria hibrida).
2. **El corte NO es solo levantar un segundo ledger: cablea la cross-atestacion dual de 0088
   punto 5 DESDE EL ARRANQUE.** El ledger #4 del hub registra el sha256 de las atestaciones de
   Aegis por gate. Prohibido operar Aegis como cadena #4 independiente sin ese enlace (los dos
   ledgers podrian divergir sin traza).
3. **Precondicion operativa antes de la primera tarea real en Aegis:** verificar los 3 firmantes
   operativos (llaves event_auth/actor_auth), capabilities maker/checker cruzado equivalentes al
   hub, y un ciclo e2e de humo (task_upsert -> claim -> flip -> release) verde en el ledger de
   Aegis, INCLUYENDO la verificacion del enlace de cross-atestacion hub->Aegis. Autorizado
   explicitamente por el Operador (commit b715d95).
4. **Cero tareas huerfanas entre ledgers:** verificado a la fecha del corte que el hub no tiene
   ninguna tarea de Contabilidad ni de ambito Aegis encolada (`TASK_INDEX.json`, 2026-07-06). Si
   algo de ese ambito aparece encolado en el hub antes de que Aegis opere, se migra el asiento de
   forma gobernada dejando traza en ambos ledgers.
5. **Prioridad dura post-30-jul (regla del Operador):** desde el 30-jul el Sprint 1 gobernado del
   hub tiene prioridad DURA sobre Contabilidad y los REQs, por el SLA del sello (adversarial 48h,
   veredicto 48h, una gracia 72h/ventana, STOP total por reincidencia). Ninguna cola de Aegis
   justifica incumplir ese SLA.

## Alcance y limites

- Complementa DECISION-0088; su punto 4 ("migracion post-sello") queda refinado asi: la migracion
  del BUILD de Nova-Budget a Aegis sigue siendo post-Etapa-1 (sin cambio), pero la gobernanza de
  trabajo NUEVO de la suite (Contabilidad en adelante, REQs de instancia) nace en Aegis desde ya,
  sin esperar ese trigger. Nada de lo YA medido/sellado se mueve.
- No toca el epoch pineado (1.14.0), el N=500 sellado, la cadena #4 existente del hub, ni el
  calendario del sello (reconciliacion 26-29-jul y Sprint 1 30-jul INTACTOS; el Operador fijo
  explicitamente "SIN enmienda al sello").
- El nucleo del protocolo sigue dominio-neutral; esta decision es de la instancia viva (dogfooding),
  no del core `*.template.*`.

## Consecuencias

- (+) Cero costura de atestacion a mitad del estudio: el hub conserva el asiento unico de lo medido.
- (+) Contabilidad y los REQs arrancan sin esperar el cierre de Etapa 1, en el asiento correcto y
  con cross-atestacion verificable por terceros desde el primer gate.
- (+) Elimina el drift potencial "el corte contradijo 0088" con traza formal.
- (-) Dos ledgers activos en paralelo durante la ventana 06-jul..cierre de Etapa 1: exige la
  disciplina de cross-atestacion del punto 2 y la prioridad dura del punto 5.
