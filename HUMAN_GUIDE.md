---
nombre: multi_agent_project_protocol
estado: activo
protocol_version: 1.1.0
runtime_version: 0.11.0
adoption_tier: runtime
perfiles: [ninguno]
idioma: es
actualizado: 2026-06-10
---

# Guia humana operativa - multi_agent_project_protocol

> Panorama. Este repositorio mantiene y enriquece un protocolo de proyecto multiagente, generico y
> reutilizable, para trabajo de software (ciclo de vida de tareas, claims, buzon, handoffs, decisiones,
> reportes humanos y un validador de estado), y ademas se gestiona a si mismo con su propio protocolo
> (dogfooding). Esta guia permite que cualquier persona o agente nuevo entienda que es la instancia, que
> hace, como se construye/ejecuta/prueba/opera, como se diagnostica, donde estan las rutas del protocolo,
> que roles hay y como retomar el contexto.

- **Instancia:** multi_agent_project_protocol  ·  **Estado:** activo  ·  **Tier:** runtime
- **Protocol version:** 1.1.0  ·  **Runtime version:** 0.11.0  ·  **Perfiles:** ninguno (instancia core)
- **Fuente de verdad:** este `.md`. El `.html` es un artefacto generado (no editar a mano).

## 1. Identidad de la instancia
<!-- origen: INSTANCIA | tier: todos | campo: obligatorio -->

Repositorio `multi_agent_project_protocol`. Proposito en una linea: protocolo multiagente neutral de
dominio para coordinar trabajo de software entre agentes y un operador humano. Lo mantiene un arquitecto
(rol revisor/orquestador) con un implementador (rol operativo), bajo aprobacion del operador humano, a
quien se reporta. Licencia propietaria (todos los derechos reservados). Es la instancia viva de referencia
del propio protocolo (dogfooding); los masters publicables son los archivos `*.template.*`.

## 2. Que es esta instancia
<!-- origen: INSTANCIA | tier: todos | campo: obligatorio -->

Un protocolo reutilizable -mas su runtime opcional- que organiza el trabajo de varios agentes y un
operador humano en tareas de un solo dueño con estado compartido, decisiones registradas y traza
verificable. El nucleo es neutral de dominio: no contiene logica de negocio. La primera instancia aplicada
(piloto) fue un proyecto separado; este repositorio es el protocolo en si.

## 3. Que hace
<!-- origen: INSTANCIA | tier: todos | campo: obligatorio -->

- Define y mantiene el ciclo de vida de tareas, claims, buzon, handoffs, decisiones y reportes.
- Provee validadores de estado, escaneo de neutralidad de dominio y de encoding, con paridad `.py`/`.ps1`.
- Provee un runtime opcional event-sourced (escritor unico del estado) y herramientas de release
  (SBOM, manifiesto, procedencia y firma de autenticidad).
- Se publica como masters `*.template.*` para que otras instancias lo adopten.

## 4. Como lo hace
<!-- origen: INSTANCIA | tier: todos | campo: obligatorio -->

Aplica su propio metodo: tareas pequeñas, verificables y de un solo dueño; coordinacion en el area comun;
decisiones registradas antes de aplicarse; gates de calidad que deben quedar en verde. En esta instancia el
runtime esta activo como escritor autoritativo: cada transicion de estado pasa por una transaccion atomica
de intents y la edicion manual del ledger se rechaza como drift.

## 5. Arquitectura
<!-- origen: INSTANCIA | tier: todos | campo: obligatorio -->

```text
AGENTS.md (contrato)        CLAUDE.md (reglas del arquitecto)
      |
      v
Area_comun/  --> protocol/ (docs + *.template.*)
             --> state/    (PROJECT_STATE, TASK_INDEX, CLAIMS)  <-- escritor unico: runtime/submit_intent
             --> mailbox/  open|answered|archived
             --> handoffs/ decisions/ reports/
      |
      v
runtime/  --> submit_intent + apply + eventlog + protocol_replay (event-sourced, drift 0)
scripts/  --> validadores, escaneos, generadores (SBOM/manifiesto/procedencia/firma, guia humana)
examples/ --> instancias de referencia + golden cases
personal/Claude, personal/Codex  --> areas privadas de cada participante
```

## 6. Componentes principales
<!-- origen: INSTANCIA | tier: todos | campo: obligatorio -->

- `AGENTS.md` - contrato compartido (fuente de verdad). `CLAUDE.md` - reglas propias del arquitecto.
- `Area_comun/state/` - estado vivo (tareas, claims, estado del proyecto).
- `runtime/submit_intent.py` + `runtime/apply.py` + `runtime/protocol_replay.py` - ledger event-sourced.
- `scripts/validate_collaboration_state.{py,ps1}` - validador de estado; `scan_domain_neutrality.*`,
  `scan_encoding.*` - escaneos; `generate_sbom/manifest/provenance`, `sign_release`/`verify_release`,
  `generate_human_guide` - herramientas de release y de esta guia.
- `examples/` - instancias de referencia (`minimal_instance`, `minimal_sdd_instance`, `human_guide_instance`)
  y golden cases.

## 7. Flujo operativo
<!-- origen: CORE+INSTANCIA | tier: todos | campo: obligatorio -->

[CORE] El trabajo se organiza en tareas de un solo dueño con ciclo de vida
`proposed -> ready -> claimed -> in_progress -> in_review -> done` (ramas `blocked` / `cancelled`); la
coordinacion ocurre en el area comun (estado, claims, buzon, handoffs) y el avance deja señales
verificables.

[INSTANCIA] El arquitecto propone, descompone y revisa; el implementador reclama tareas `ready` y entrega
a `in_review` con handoff; el arquitecto ratifica adversarialmente y cierra a `done`. El operador humano
aprueba politica, cambios incompatibles y releases. El implementador trabaja empujado por el operador
(push-driven). Toda transicion de estado pasa por `runtime/submit_intent.py`.

## 8. Flujo de datos
<!-- origen: INSTANCIA | tier: todos | campo: obligatorio -->

Entran tareas, decisiones y mensajes de coordinacion. Se transforman en intents que el runtime valida y
materializa al estado (`Area_comun/state/*.json`), dejando eventos en `runtime/state/events.jsonl` y un
snapshot reconstruible (replay == estado materializado, drift 0). Salen entregables al control de versiones
y, en releases, la cadena `dist/<version>/` (SBOM, manifiesto, procedencia, firma). Todo en texto, sin
secretos.

## 9. Flujo de decisiones
<!-- origen: CORE | tier: todos | campo: obligatorio -->

[CORE] Las decisiones de protocolo/limites se registran como DECISIONES en `Area_comun/decisions/`
(una por archivo) antes de aplicarse; los cambios incompatibles requieren ademas aprobacion del
operador humano. Las tareas enlazan las decisiones que las gobiernan. La ambiguedad se vuelve `blocked`
con una pregunta concreta, no una suposicion.

## 10. Como se implementa la metodologia aqui
<!-- origen: CORE+INSTANCIA | tier: todos | campo: obligatorio -->

[CORE] El contrato compartido es `AGENTS.md`; el estado vivo y los artefactos de coordinacion estan en
`Area_comun/`; cada participante mantiene su area privada en `personal/<id>/`. La fuente de verdad de
los masters publicados son los archivos `*.template.*`.

[INSTANCIA] Esta instancia no adopta perfiles profesionales (es el core). Activa el runtime como escritor
autoritativo (`event_state` con `enforce` + `authoritative`): el gate de sombra duro rechaza la edicion
manual del ledger. Hay una regla anti-colision para escrituras concurrentes (staging por rutas explicitas,
nunca `git add -A`) y la regla de memoria post-commit (actualizar la memoria propia tras cada commit).

## 11. Como se construye
<!-- origen: INSTANCIA | tier: todos | campo: obligatorio -->

No requiere compilacion: son artefactos de texto (Markdown + JSON) y scripts en Python/PowerShell. El
prerequisito es un interprete de Python 3 (y opcionalmente PowerShell para la paridad de scripts).

```text
# no hay build; instanciar un nuevo proyecto desde los masters
python scripts/new_instance.py --help
```

## 12. Como se ejecuta localmente
<!-- origen: INSTANCIA | tier: todos | campo: obligatorio -->

No hay servicio que levantar. Para "ejecutar" el runtime de coordinacion se emiten intents y se valida el
estado. El orquestador opcional se invoca explicitamente y solo escribe con gates por turno.

```text
# emitir una transaccion de estado (escritor unico)
python runtime/submit_intent.py --intents transaccion.json
# verificar consistencia event-sourced
python runtime/protocol_replay.py --check
```

## 13. Como se prueba
<!-- origen: INSTANCIA | tier: todos | campo: obligatorio -->

Las pruebas son los gates de calidad y los golden cases. Verde = salida sin errores y codigo de salida 0;
rojo = el gate imprime el motivo y devuelve codigo distinto de 0.

```text
python scripts/validate_collaboration_state.py --root .
python scripts/scan_domain_neutrality.py --root .
python scripts/scan_encoding.py --root .
python runtime/protocol_replay.py --check
python examples/release_sign_cases/run_release_sign_cases.py
python examples/human_guide_cases/run_human_guide_cases.py
```

- [ ] Validador de estado de coordinacion en verde
- [ ] Escaneo de neutralidad de dominio sin hallazgos
- [ ] Escaneo de encoding limpio (ASCII en el canal entre agentes)
- [ ] Replay event-sourced sin drift (`has_drift=false`)
- [ ] Golden cases (release tooling, guia humana, sign/verify) en verde

## 14. Como se despliega o lanza
<!-- origen: INSTANCIA | tier: opcional | campo: opcional: si la instancia no se despliega, marcar no-aplica con motivo -->

El "despliegue" es el corte de release: se regenera la cadena verificable en `dist/<version>/` (SBOM,
manifiesto, procedencia) sobre un HEAD estable, el emisor la firma con un backend externo (firma keyless,
material fuera del repo) y se etiqueta la version con aprobacion del operador humano. Rollback = no etiquetar
/ revertir el commit de release.

## 15. Como se opera
<!-- origen: INSTANCIA | tier: todos | campo: obligatorio -->

Operacion diaria: el arquitecto revisa estado y buzon, descompone backlog y ratifica entregas; el
implementador atiende tareas `ready` empujado por el operador y deja una señal de avance por turno;
mantenimiento periodico (poda sistematica del estado vivo) bajo capability de orquestador. El operador
humano marca el alcance por turno y aprueba releases. Un solo multiplicador de riesgo activo por ventana.

## 16. Troubleshooting
<!-- origen: INSTANCIA | tier: todos | campo: obligatorio -->

| Sintoma | Causa probable | Remedio |
|---|---|---|
| Validador en rojo por mismatch de estado | Indice y archivo de tarea discrepan | Reconciliar via `submit_intent`; nunca editar el JSON a mano bajo `enforce` |
| `protocol_replay --check` reporta drift | Edicion manual del ledger o base sucia | Regenerar genesis (`runtime/regenesis.py`) y volver a emitir por intents |
| Escaneo de neutralidad con hallazgos | Termino de dominio en un archivo del core o `*.template.*` | Quitar el termino o moverlo a un perfil/ejemplo |
| Encoding en rojo | Caracter no-ASCII en el canal entre agentes | Reemplazar por ASCII (regla del canal entre agentes) |
| `prune --check` en rojo (poda debida) | Acumulacion de claims liberados / tokens de arranque | Ejecutar `protocol_prune` por `submit_intent` (capability orquestador) |

Diagnostico antes de actuar: leer el mensaje del gate y el estado vivo; escalar al operador humano si el
cambio toca limites o requiere aprobacion.

## 17. Rutas relevantes del protocolo
<!-- origen: CORE | tier: todos | campo: obligatorio -->

[CORE] Esta seccion ENLAZA a los documentos vivos del protocolo (no los reescribe):

- Contrato compartido: `AGENTS.md`
- Protocolo de tareas: `Area_comun/protocol/TASK_PROTOCOL.md`
- Estado vivo: `Area_comun/state/` (PROJECT_STATE, TASK_INDEX, CLAIMS)
- Buzon y handoffs: `Area_comun/mailbox/`, `Area_comun/handoffs/`
- Decisiones y reportes: `Area_comun/decisions/`, `Area_comun/reports/`
- Runtime (solo tier runtime): `Area_comun/protocol/N_AGENT_RUNTIME.md`, runbooks `Area_comun/protocol/RUNBOOK-*`

## 18. Roles y capacidades configuradas
<!-- origen: CORE+INSTANCIA | tier: todos | campo: obligatorio -->

[CORE] Roles genericos del metodo: **operador humano** (aprueba politica, cambios incompatibles y
releases), **agente operativo/implementador** (ejecuta el trabajo), **agente revisor/arquitecto**
(diseña, revisa y mantiene la coherencia y la neutralidad). La capability requerida sale del CONTENIDO
del trabajo, no del nombre del participante.

[INSTANCIA] Configurados aqui: un agente arquitecto con capabilities de arquitecto/orquestador/qa/revisor;
un agente implementador con capabilities de implementador/ingeniero de pruebas; y un operador humano. Las
transiciones se autorizan por capability segun el contenido del trabajo, no por el nombre del participante.

## 19. Seguridad y datos sensibles
<!-- origen: CORE+INSTANCIA | tier: todos | campo: obligatorio -->

[CORE] No se commitean secretos (claves, tokens, material de firma). El material real de firma/credenciales
pertenece al emisor o a su CI y nunca entra al repositorio.

> [SEGURIDAD] La firma de releases usa un backend externo configurable (firma keyless): la identidad y el
> material de firma viven en el emisor/CI (OIDC del emisor), nunca en el repositorio. Las areas privadas
> `personal/<id>/` no se comparten entre participantes. Nunca se pegan valores reales de secretos en esta guia.

[INSTANCIA] El repositorio no maneja datos de usuario: son artefactos de protocolo en texto. El unico
material sensible (claves/identidad de firma) es del emisor y queda fuera del repo por diseño.

## 20. Continuidad, traspaso y recuperacion de contexto
<!-- origen: CORE | tier: todos | campo: obligatorio -->

[CORE] Un participante que entra en frio retoma leyendo: `AGENTS.md` seccion "How to Start", el estado
vivo en `Area_comun/state/`, el buzon en `Area_comun/mailbox/open/` y el punto de retoma de la instancia
(`RESUME.md` u hoja de arranque equivalente / `cold_start_globs`). Cada tarea y handoff es
autocontenido; nadie asume el contexto de otro.

## 21. Historial de cambios
<!-- origen: INSTANCIA | tier: todos | campo: obligatorio -->

| Fecha | Cambio |
|---|---|
| 2026-06-10 | Guia dogfooding creada para la instancia viva (tier runtime, protocol 1.1.0) via el generador |
