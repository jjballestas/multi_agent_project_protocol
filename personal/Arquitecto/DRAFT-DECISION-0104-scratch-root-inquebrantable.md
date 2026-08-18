# DRAFT DECISION-0104 -- Regla global INQUEBRANTABLE de scratch root (para FIRMA del Operador)

> BORRADOR en area del Arquitecto. NO sellado. Redactado a peticion del Operador (directiva 2:
> "quiero una REGLA A NIVEL GLOBAL QUE SEA INQUEBRANTABLE: los agentes deben tener una carpeta
> especifica para desplegar sus pruebas o instancias temporales, nunca en la raiz del disco; si no
> lo tienen claro deben preguntar al operador").
> Fortalece y NO deroga DECISION-0098 (scratch root unico por proyecto, firmada 2026-07-14).
> Se sella via submit_intent (decision) SOLO tras tu FIRMA, con AGENTS.md/AGENTS.template.md en el
> mismo commit gobernado.

## Frontmatter propuesto
```
decision_id: DECISION-0104
title: "Regla global inquebrantable: scratch/pruebas/instancias temporales SOLO bajo el scratch root
  designado, NUNCA en la raiz del disco; ante duda, preguntar al operador"
status: accepted
date: 2026-07-26
deciders: [operador humano (FIRMA pendiente), Arquitecto (redacta)]
relates_to: [DECISION-0098, DECISION-0057, DECISION-0050, DECISION-0018]
supersedes: []
phase: P2
```

## Contexto
Auditoria de `D:\` (2026-07-26): ~75 directorios de trabajo de la metodologia creados en la RAIZ del
disco entre el 20 y el 24 de julio (42 clones del hub ~81 GB + probes + instancias), TODOS posteriores a
la firma de DECISION-0098. Causa raiz: los skills/memorias operativas de los agentes clonaban a ruta
corta `/d/ccv` (raiz) por MAX_PATH, contradiciendo la 0098. La 0098 fijo el DONDE pero no era
inquebrantable ni tenia teeth ni clausula de "ante duda, preguntar". Esta decision cierra el hueco.

## Decision (clausulas)
1. **REGLA GLOBAL INQUEBRANTABLE (todos los proyectos, todos los agentes, todos los discos).** Ningun
   agente crea directorios de trabajo, pruebas, clones o instancias temporales en la raiz de un disco
   (`D:/`, `C:/`, home root, etc.). TODO scratch vive bajo el scratch root designado del proyecto,
   nombrado al nacer la instancia. No hay excepcion por "ruta corta", "MAX_PATH" ni "solo temporal": la
   ruta corta se resuelve DENTRO del scratch root, no en la raiz.
2. **ANTE DUDA, PREGUNTAR.** Si un agente no tiene clara la ruta de scratch (p.ej. proyecto nuevo sin
   scratch root declarado), NO improvisa en la raiz: lo trata como `blocked` con una pregunta concreta
   al operador (humano encargado) y espera. Improvisar una carpeta en la raiz es una violacion, no un
   atajo.
3. **DECLARADA AL NACER + HEREDADA POR EL TEMPLATE (neutral de dominio).** La regla viaja en
   `AGENTS.template.md` (redaccion neutra: "designated scratch root declared at instance birth") -> toda
   instancia born-operational nace con ella. El NOMBRE concreto del scratch root es config de instancia
   (en este despliegue: `D:/Aegis_Scratch/<proyecto>/<proposito>/`), nunca hardcodeado en el core/template.
4. **FUERA DEL ARBOL ATESTADO; NUNCA LA UNICA COPIA; LIMPIEZA AL STAND-DOWN.** (Reafirma DECISION-0098
   cl.2/5 y DECISION-0057.) El scratch se `rm` al cerrar el proceso que lo creo; jamas guarda la unica
   copia de commits/secretos.
5. **ENFORCEMENT (teeth).** (a) Skills/prompts/runbooks de los agentes clonan/validan SOLO bajo el
   scratch root (Arquitecto: corregido 2026-07-26; Codex/Analista: notificados por mailbox para alinear
   sus rutas). (b) Detector de higiene (tarea Codex-maker, ciclo gobernado): escanea la raiz del disco y
   FLAGea como anomalia DECISION-0018 cualquier dir de la metodologia fuera del scratch root (reporta al
   owner; NO borra). (c) Barrido de limpieza de lo ya acumulado: SOLO con autorizacion explicita del
   operador, verificando 1x1.
6. **FONDO INTOCABLE.** No toca #4: config hub `2E35F26E` / epoch `1.14.0` / dataset N=500 / sellos. La
   politica vive fuera del config pineado; el cableado aplica a instancias nuevas via template.

---

## Diff propuesto -- AGENTS.md (instancia viva), seccion 4, nuevo bullet ANTES de "Changes to these boundaries"
```
- **Scratch discipline (DECISION-0098 + DECISION-0104, inviolable):** agents MUST NOT create
  work/temp/clone/test/instance directories at any disk root (`D:/`, `C:/`, home root). All scratch
  lives under this instance's single designated scratch root `D:/Aegis_Scratch/<project>/<purpose>/`
  (short path = MAX_PATH-safe), outside the attested tree, never the only copy, cleaned at stand-down.
  If the scratch path is unclear (e.g. a new project without a declared scratch root), the agent MUST
  ask the human owner and wait -- it never improvises at a disk root.
```

## Diff propuesto -- AGENTS.template.md (master neutral), seccion 4, nuevo bullet ANTES del placeholder
```
- **Scratch discipline (inviolable, domain-neutral):** agents MUST NOT create work/temp/clone/test/
  instance directories at any disk root. All scratch lives under the project's single designated
  scratch root (a named umbrella declared at instance birth; short path = MAX_PATH-safe), outside the
  attested tree, never the only copy, cleaned at stand-down. If the scratch path is unclear, the agent
  MUST ask the human owner and wait -- it never improvises at a disk root.
```

## Unidad de enforcement (tarea Codex-maker, a registrar tras tu FIRMA)
- TASK-XXXX (infra): detector de higiene de scratch root. Escanea la raiz de disco(s) y lista dirs con
  huella de metodologia (`.git` con remote al hub/producto, o nombres de patron `ccv*`, `bench*`, etc.)
  fuera del scratch root -> emite anomalia DECISION-0018 al owner. NO borra. Neutral (el scratch root es
  parametro). Ciclo gobernado normal (maker Codex -> recomputo -> checker Analista -> cierro).

## Que necesito de ti (Operador)
1. FIRMA de las 6 clausulas (o enmiendas).
2. OK a los dos diffs de AGENTS (vivo + template).
3. OK para registrar la tarea del detector a Codex.
Con eso sello DECISION-0104 + aplico los diffs en un commit gobernado + registro la tarea. La limpieza
del basurero va por separado (ver LISTA-candidatos-limpieza-D-raiz.md; SOLO con tu autorizacion).
