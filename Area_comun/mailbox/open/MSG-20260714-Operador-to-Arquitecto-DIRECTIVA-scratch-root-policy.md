---
message_id: MSG-20260714-Operador-to-Arquitecto-DIRECTIVA-scratch-root-policy
from: Operador
to: Arquitecto
type: DIRECTIVA
status: open
requires_response: true
response_owner: Arquitecto
created_at: 2026-07-14
context_refs:
  - D:/nova-a2 (scratch repo reorg A2, drive root - MAL UBICADO)
  - D:/nova-enc (scratch repo encapsulado Aegis, drive root - MAL UBICADO)
  - D:/nova-inst-tmp (scratch instancing born-operational, drive root - MAL UBICADO)
  - DECISION-0096 (instancias born-operational)
  - DECISION-0057 (Arquitecto activa/para runtimes)
one_line_summary: "REGLA DE METODOLOGIA (todos los proyectos, con adopcion publica futura en mente): prohibido crear directorios de trabajo/temporales/clones en la raiz del disco de forma ad-hoc. Toda instancia usa UN scratch root unico bajo el paraguas D:/Aegis_Scratch/<proyecto>/<proposito>/. Ademas: ordenar YA los 3 dirs nova-* que quedaron sueltos en D:/."
requested_action: "1) Formaliza la regla como DECISION (aplica a TODOS los proyectos, no solo NOVA). 2) Realiza el ordenamiento: reconcilia y mueve/reap D:/nova-a2, D:/nova-enc, D:/nova-inst-tmp al nuevo esquema, VERIFICANDO antes que los repos git (nova-a2, nova-enc) no tengan commits/trabajo que no este en el NOVA canonico. 3) Cablea el scratch root en el template (born-operational lo declara al nacer) + .gitignore + chequeo del validador."
question: "Confirmas la regla + entregas la DECISION draft para firma, y ejecutas el ordenamiento de los 3 dirs sueltos?"
---

# DIRECTIVA - Scratch root unico por proyecto (regla de metodologia)

## Contexto (lo que esta mal hoy)
Los agentes crearon en la RAIZ del disco tres directorios de trabajo sueltos durante la reorg 2.A /
re-genesis de NOVA (13-14 jul):
- `D:/nova-a2`      -- clon/staging de la topologia A2 (dos-trios). Repo git.
- `D:/nova-enc`     -- retrofit de gobernanza encapsulada bajo `Aegis/`. Repo git.
- `D:/nova-inst-tmp`-- scratch de instancing born-operational (protocol-secrets/, runtime/). No es repo git.

Esto ensucia la raiz del disco y deja mal visto el orden de la metodologia. NO fue puro descuido: en
Windows el limite MAX_PATH (260 chars) revienta cuando se clona/valida dentro de rutas profundas
(`D:/Agentes/multi_agent_project_protocol/...` o `D:/Agentes/NOVA-Suite/Nova-Payroll/...`), y los
agentes huyeron a la raiz para tener ruta corta. La regla debe resolver ORDEN y RUTA CORTA a la vez.

## La regla (decision del operador)
Un unico **scratch root** por proyecto, bajo un paraguas nombrado en la raiz del disco:

    D:/Aegis_Scratch/<proyecto>/<proposito>/

- **Paraguas unico `Aegis_Scratch`:** identifica que TODO lo que hay ahi lo creo Aegis (la metodologia);
  clones Y work bajo el mismo techo, no mas carpetas ad-hoc dispersas en la raiz.
- **Ruta corta:** al colgar de la raiz (no de `D:/Agentes/NOVA-Suite/...`) es MAX_PATH-safe para clones
  y validaciones -- resuelve la razon por la que se fueron a la raiz.
- **Fuera del arbol atestado:** el scratch root NUNCA entra al ledger #4 ni al repo; va gitignored.
  Contaminar el arbol atestado con scratch es peor que el desorden en disco.
- **Declarado al nacer:** la metodologia se instancia DENTRO de un proyecto, pero al ejecutarse crea/
  usa su scratch root para lo temporal o adicional (crons independientes, pruebas, clones de validacion).
  Encaja con born-operational (DECISION-0096): la instancia nace declarando su scratch root, igual que
  nace con base/store.
- **Ciclo de vida:** el scratch se limpia al stand-down del proceso (encaja con DECISION-0057: el
  Arquitecto para runtimes ociosos -> tambien reap su scratch). Nada de scratch huerfano acumulandose.

Para NOVA, el mapeo esperado seria del estilo:
`D:/Aegis_Scratch/NOVA-Suite/a2/`, `.../enc/`, `.../inst-tmp/` (o el `<proposito>` que corresponda).

## Lo que pido (2 cosas separadas, no mezclar)
1. **La regla (a futuro):** formalizala como **DECISION** (aplica a TODOS los proyectos; pensada para
   adopcion publica). Entrega el draft para firma del operador. Cablea: campo de scratch root en el
   template/config (born-operational lo fija al nacer), `.gitignore` del template, y un chequeo del
   validador que rechace artefactos de scratch dentro del arbol o dirs de trabajo en la raiz del disco.
2. **Los 3 dirs actuales (ordenamiento YA):** reconcilia y mueve/reap `D:/nova-a2`, `D:/nova-enc`,
   `D:/nova-inst-tmp` al nuevo esquema. ANTES de mover/reap, VERIFICA que los repos git (nova-a2,
   nova-enc) no tengan commits/ramas/trabajo que no este ya en el NOVA canonico; si hay algo no
   integrado, senalalo antes de tocar (no perder trabajo). El fondo pineado (hub 2E35F26E / epoch
   1.14.0 / dataset N=500) NO se toca.

## Frontera
No toca #4 ni el estudio medido. Es politica de disco + template + validador.
