---
decision_id: DECISION-0104
title: "Regla global INQUEBRANTABLE: scratch/pruebas/instancias temporales SOLO bajo el scratch root designado, NUNCA en la raiz del disco; ante duda, preguntar al operador (fortalece DECISION-0098)"
status: accepted
date: 2026-07-26
deciders: [operador humano (FIRMADA 2026-07-26 -- 6 clausulas sin enmiendas + 2 diffs de AGENTS + registro del detector a Codex), Arquitecto (redacta)]
supersedes: []
superseded_by: []
relates_to: [DECISION-0098, DECISION-0057, DECISION-0050, DECISION-0018, DECISION-0096]
phase: P2
---

# DECISION-0104 - Regla global inquebrantable de scratch root (fortalece DECISION-0098)

> **FIRMADA por el operador el 2026-07-26** (6 clausulas aceptadas sin enmiendas; OK a los dos
> diffs de AGENTS -- vivo + template; OK para registrar la tarea del detector a Codex). Sellada
> via submit_intent por el Arquitecto. NO toca #4: config hub 2E35F26E / epoch 1.14.0 / dataset
> N=500 / sellos intactos (la politica vive fuera del config pineado; el cableado aplica a
> instancias NUEVAS via template). Fortalece y NO deroga DECISION-0098.

## Contexto

Auditoria de la raiz `D:\` (2026-07-26): ~75 directorios de trabajo de la metodologia acumulados
en la RAIZ del disco entre el 20 y el 24 de julio -- 42 clones del hub (~81 GB, cada clon arrastra
el `.git` completo con miles de eventos del ledger + dataset N=500), repos-probe de test,
instancias generadas y sandboxes -- TODOS posteriores a la firma de DECISION-0098. Causa raiz: los
skills/memorias operativas de los agentes clonaban a ruta corta `/d/ccv` (raiz) por el limite
MAX_PATH de Windows, contradiciendo la 0098. La 0098 fijo el DONDE (bajo `Aegis_Scratch`) y cableo
el campo `scratch_root` en config+validador, pero (a) no era declarada INQUEBRANTABLE, (b) no tenia
clausula de "ante duda, preguntar", y (c) el validador solo ve el campo del config, no la raiz real
del disco -- no habia detector que cazara el desvio. Esta decision cierra el hueco.

## Decision (6 clausulas, FIRMADAS sin enmiendas)

1. **REGLA GLOBAL INQUEBRANTABLE (todos los proyectos, todos los agentes, todos los discos).**
   Ningun agente crea directorios de trabajo, pruebas, clones o instancias temporales en la raiz de
   un disco (`D:/`, `C:/`, home root, etc.). TODO scratch vive bajo el scratch root designado del
   proyecto, nombrado al nacer la instancia. No hay excepcion por "ruta corta", "MAX_PATH" ni "solo
   temporal": la ruta corta se resuelve DENTRO del scratch root, no en la raiz.

2. **ANTE DUDA, PREGUNTAR.** Si un agente no tiene clara la ruta de scratch (p.ej. proyecto nuevo
   sin scratch root declarado), NO improvisa en la raiz: lo trata como `blocked` con una pregunta
   concreta al operador (humano encargado) y espera. Improvisar una carpeta en la raiz es una
   violacion, no un atajo.

3. **DECLARADA AL NACER + HEREDADA POR EL TEMPLATE (neutral de dominio).** La regla viaja en
   `AGENTS.template.md` con redaccion NEUTRA ("designated scratch root declared at instance birth")
   -> toda instancia born-operational nace con ella. El NOMBRE concreto del scratch root es config
   de instancia (en este despliegue: `D:/Aegis_Scratch/<proyecto>/<proposito>/`), nunca hardcodeado
   en el core/template. Complementa el campo `scratch_root` que la 0098 ya cableo (clausulas 3/4).

4. **FUERA DEL ARBOL ATESTADO; NUNCA LA UNICA COPIA; LIMPIEZA AL STAND-DOWN.** (Reafirma
   DECISION-0098 cl.2/5 y DECISION-0057.) El scratch se `rm` al cerrar el proceso que lo creo;
   jamas guarda la unica copia de commits/secretos.

5. **ENFORCEMENT (teeth).** (a) Skills/prompts/runbooks de los agentes clonan/validan SOLO bajo el
   scratch root (Arquitecto: skill+memoria corregidos 2026-07-26; Codex/Analista: notificados por
   mailbox para alinear sus rutas). (b) Detector de higiene (TASK-0295, Codex-maker, ciclo
   gobernado): escanea la raiz del disco y FLAGea como anomalia DECISION-0018 cualquier dir de la
   metodologia fuera del scratch root (reporta al owner; NO borra). (c) Barrido de limpieza de lo ya
   acumulado: SOLO con autorizacion explicita del operador, verificando 1x1, en bloques.

6. **FONDO INTOCABLE.** No toca #4: config hub `2E35F26E` / epoch `1.14.0` / dataset N=500 /
   sellos. La politica vive fuera del config pineado; el cableado aplica a instancias nuevas via
   template.

## Consecuencias

- La regla de scratch root pasa de convencion a INVARIANTE inquebrantable con clausula de duda ->
  preguntar, cortando el modo-fallo real (improvisar en la raiz "por ruta corta").
- Toda instancia born-operational nace con la regla en su contrato de roles (via template neutral).
- La metodologia gana un detector de disco (TASK-0295) que caza el desvio que el validador de config
  no puede ver.
- El basurero ya acumulado se limpia por bloques con aprobacion explicita del operador (no en esta
  decision; ver `personal/Arquitecto/LISTA-candidatos-limpieza-D-raiz.md`).

## Estado

`accepted` (firmada 2026-07-26; sellada via submit_intent). Cableado: skills/memoria del Arquitecto
corregidos; AGENTS.md (vivo) + AGENTS.template.md (neutral) actualizados en el mismo commit
gobernado; TASK-0295 (detector) registrada y en GO a Codex.
