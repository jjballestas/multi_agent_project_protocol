---
decision_id: DECISION-0098
title: "Scratch root unico por proyecto (D:/Aegis_Scratch/<proyecto>/<proposito>/) -- prohibido el scratch ad-hoc en la raiz del disco; declarado al nacer la instancia"
status: proposed-pending-operator-signature
date: 2026-07-14
deciders: [operador humano (FIRMA PENDIENTE; regla ordenada por DIRECTIVA 2026-07-14), Arquitecto (redacta)]
supersedes: []
superseded_by: []
relates_to: [DECISION-0096, DECISION-0057, DECISION-0050, DECISION-0095]
phase: P2
derives_from:
  - "Area_comun/mailbox/answered/MSG-20260714-Operador-to-Arquitecto-DIRECTIVA-scratch-root-policy.md"
---

# DECISION-0098 - Scratch root unico por proyecto (regla de metodologia)

> **DRAFT PARA FIRMA DEL OPERADOR** (la regla en si ya fue decidida por el operador en la
> DIRECTIVA del 2026-07-14; este documento la formaliza como DECISION exportable). NO toca #4:
> config hub 2E35F26E / epoch 1.14.0 / dataset N=500 / sellos intactos (la politica vive fuera
> del config pineado; el cableado de config aplica a instancias NUEVAS via template).

## Contexto

Durante la reorg 2.A / re-genesis de NOVA (13-14 jul) los agentes crearon tres directorios de
trabajo sueltos en la raiz del disco (`D:/nova-a2`, `D:/nova-enc`, `D:/nova-inst-tmp`). No fue
puro descuido: en Windows el limite MAX_PATH (260 chars) revienta clones/validaciones dentro de
rutas profundas, y la raiz del disco es la ruta corta disponible. La regla resuelve ORDEN y RUTA
CORTA a la vez, con adopcion publica futura en mente.

## Decision (6 clausulas)

1. **REGLA (todos los proyectos).** Prohibido crear directorios de trabajo/temporales/clones en
   la raiz del disco de forma ad-hoc. Todo scratch de una instancia de la metodologia vive bajo
   un unico paraguas nombrado en la raiz: `D:/Aegis_Scratch/<proyecto>/<proposito>/` (en hosts
   POSIX: `~/Aegis_Scratch/<proyecto>/<proposito>/`). El paraguas identifica que TODO su
   contenido lo creo la metodologia; clones y work bajo el mismo techo.

2. **FUERA DEL ARBOL ATESTADO.** El scratch root NUNCA entra al ledger #4 ni al repo de la
   instancia; va gitignored (el `.gitignore` que `new_instance.py` asegura en TODOS los tiers
   incluye los guards `Aegis_Scratch/` y `.protocol-tmp/` contra creacion accidental in-tree).
   Contaminar el arbol atestado con scratch es peor que el desorden en disco. El scratch NUNCA
   guarda la UNICA copia de nada (secretos, commits, artefactos): si un contenido importa, su
   lugar es el repo/ledger o el store de secretos de la instancia.

3. **DECLARADO AL NACER (born-operational, DECISION-0096).** La instancia nace declarando su
   scratch root, igual que nace con base/store: campo OPCIONAL `scratch_root` en
   `protocol.config.template.json`, fijado por `new_instance.py` al instanciar (parametro
   `--scratch-root`, default derivado del nombre del proyecto). Los configs PINEADOS existentes
   (hub 2E35F26E y equivalentes) quedan EXENTOS: el campo es opcional y el chequeo del validador
   es condicional (solo aplica si el campo existe) -- no hay re-genesis por esta regla.

4. **CHEQUEO DEL VALIDADOR.** `validate_collaboration_state.py` y `.ps1` (paridad) validan,
   cuando `scratch_root` existe en el config: es ruta ABSOLUTA (formas host-independientes:
   `X:/`, `/`, `~` -- un config nacido en Windows valida igual en el CI POSIX y viceversa) y
   NO apunta dentro del arbol de la instancia (chequeo host-local cuando la ruta es resoluble
   en el host). La defensa contra artefactos de scratch DENTRO del arbol es el guard de
   `.gitignore` de la clausula 2, no un scan del validador. El chequeo es aditivo y
   compatible: instancias sin el campo validan igual que hoy.

5. **CICLO DE VIDA.** El scratch se limpia al stand-down del proceso que lo creo (encaja con
   DECISION-0057: el Arquitecto que para runtimes ociosos tambien reapea su scratch). Nada de
   scratch huerfano acumulandose; un dir de scratch cuyo proceso ya cerro es reapeable previa
   verificacion (repos: 0 commits/ramas/stash fuera del canonico; secretos: solo duplicados).

6. **ORDENAMIENTO INICIAL (una vez) -- EJECUTADO 2026-07-14 ~17:22 con autorizacion explicita
   del operador.** Verificacion ANTES de tocar: `D:/nova-a2` y `D:/nova-enc` = clones de NOVA
   con 0 commits locales fuera de `origin/main` (fdeb99d), arbol limpio, sin stash; sus
   `protocol-secrets/` y los de `D:/nova-inst-tmp` = duplicados byte-identicos (sha256) de los
   vivos en `NOVA-Suite/NOVA/Aegis/protocol-secrets/`; `nova-inst-tmp` = scaffold de
   instanciacion ya consumido por el canonico. Disposicion ejecutada: REAP de los tres
   (mantener copias sueltas de llaves privadas en scratch es un pasivo) + paraguas
   `D:/Aegis_Scratch/` creado con README de convencion. Ademas se hallaron 2 archivos sueltos
   no listados (`D:/nova-9310-tx.json` = tx ya aplicada; `D:/nova-a2-events.bak` = respaldo del
   ledger de 2 eventos del staging A2, verificado NO presente en la historia git de NOVA) ->
   MOVIDOS (sin destruir) a `D:/Aegis_Scratch/NOVA-Suite/residue/`; su reap final queda a
   criterio del operador. Raiz del disco LIMPIA de `nova-*`.

## Consecuencias

- La raiz del disco queda limpia; el unico paraguas visible es `D:/Aegis_Scratch/` (con README
  de convencion).
- Las instancias nuevas nacen con scratch root declarado y MAX_PATH-safe; los clones de
  validacion (`ccv`) dejan de improvisarse en la raiz.
- El validador gana un invariante aditivo sin afectar configs pineados.

## Estado

`proposed-pending-operator-signature`. Al firmar: submit_intent `decision` (patron 0095/0096) +
cableado activo en template/new_instance/validador.
