---
message_id: MSG-20260817-Operador-to-Arquitecto-DIRECTIVA-higiene-working-tree-por-dueno
task_id: none
type: DIRECTIVA
from: Operador
to: Arquitecto
status: open
requires_response: true
response_owner: Arquitecto
one_line_summary: "DIRECTIVA de higiene del WORKING TREE (medido por el operador: 1.415 ficheros untracked -- 1.351 de personal/Codex (95%), 52 de personal/Arquitecto, 9 de personal/operador, 1 de personal/Analista; CERO tracked modificados: el arbol gobernado esta limpio). Regla: drenaje POR DUENO con pathspec explicito en el proximo checkpoint de cada agente, Codex primero por volumen. PROHIBIDO git clean (el precedente de las claves eventauth: lo untracked borrado no vuelve) y PROHIBIDO el add -A masivo por quien no es dueno (la anomalia de absorcion de ayer, a escala). Prioridad: ventanas quietas, NUNCA compitiendo con el ciclo r3 de 0414."
requested_action: "Coordina el drenaje con estas clases y tratamientos: (1) EVIDENCIAS (MEMORY-*, HANDOFF-*, DIAG-*): commit por lotes con pathspec del dueno -- es el espiritu de DECISION-0026, es material del dataset, y lo untracked NO tiene backup (las claves de NOVA lo demostraron; y el caso analista-hmac_v1 de anoche demostro que material no versionado rompe la verificabilidad por terceros). (2) RECIBOS repetitivos (task*_delivery*.json, *_claim_result*.json...): decide tu la clase -- un commit historico unico O regla de .gitignore para que dejen de acumular; lo que no vale es el goteo eterno. (3) FIXTURES DE INSTANCIA (p.ej. personal/Codex/task0294_attested/, una instancia Aegis COMPLETA con claves eventauth dentro): a D:/Aegis_Scratch segun DECISION-0104 -- ni commiteadas (contienen material de firma) ni sueltas en personal; ATENCION al detalle de que llevan claves: moverlas, no publicarlas. (4) Anade a .gitignore las clases de residuo recurrente que identifiques, para que esta directiva no haga falta dos veces. (5) Los 9 de personal/operador los revisara el canal del operador. (6) Secuencia: cada agente drena SU area en su proximo checkpoint de ventana quieta; Codex puede necesitar 2-3 lotes. Reporta cierre cuando el arbol quede en decenas, no miles."
question: "Que clases mandas a .gitignore y en cuantos lotes planificas el drenaje de Codex?"
context_refs:
  - Area_comun/protocol/TASK_PROTOCOL.md
  - .gitignore
deadline_or_blocking_level: low
---

# DIRECTIVA -- el working tree se drena por dueno, con las claves como leccion

La medicion que motiva esto, hecha por el operador sobre git status:

    1.415 untracked totales
      1.351  personal/Codex     (memorias, handoffs, diagnosticos, recibos JSON,
                                 y el fixture task0294_attested CON claves dentro)
         52  personal/Arquitecto (drafts y deltas)
          9  personal/operador
          1  personal/Analista
          2  Area_comun          (el veredicto r2 en vuelo -- se resolvio solo)
          0  tracked modificados (el arbol gobernado, impecable)

El argumento de fondo no es estetico: **untracked = sin backup y sin
verificabilidad**. Ayer se perdieron cuatro claves sin dejar rastro ni en la
papelera, y anoche un clon limpio se puso rojo porque material de verificacion
vivia en un fichero no versionado. La evidencia de dos meses de trabajo de
Codex esta hoy en esa misma situacion de fragilidad. Se protege commiteando
por su dueno -- no con un clean que la borre ni con un add masivo que la
atribuya mal.

Sin urgencia: es deuda de higiene, no incidente. Ventanas quietas, r3 primero.
