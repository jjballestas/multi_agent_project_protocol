---
nombre: multi_agent_project_protocol
estado: activo
protocol_version: 1.14.0
runtime_version: 0.12.0
adoption_tier: runtime
perfiles: [ninguno]
idioma: es
actualizado: 2026-07-27
---

# Guia humana operativa - multi_agent_project_protocol

> Panorama. Este repositorio mantiene y enriquece un protocolo de proyecto multiagente, generico y
> reutilizable, para trabajo de software (ciclo de vida de tareas, claims, buzon, handoffs, decisiones,
> reportes humanos y un validador de estado), y ademas se gestiona a si mismo con su propio protocolo
> (dogfooding). Esta guia permite que cualquier persona o agente nuevo entienda que es la instancia, que
> hace, como se construye/ejecuta/prueba/opera, como se diagnostica, donde estan las rutas del protocolo,
> que roles hay y como retomar el contexto.

- **Instancia:** multi_agent_project_protocol  ·  **Estado:** activo  ·  **Tier:** runtime
- **Protocol version:** 1.14.0 (epoch PINEADO; la linea de releases va aparte y su ultima es v1.19.0)  ·  **Runtime version:** 0.12.0  ·  **Perfiles:** ninguno (instancia core)
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

Cada unidad de trabajo pasa por un **ciclo gobernado de dos capas de revision**: el maker entrega; el
orquestador hace un **recomputo independiente** (corre los money-shots por el entrypoint real, no confia en
la evidencia del maker); un **checker adversarial** de capacidad fuerte y **proveedor diverso** (nunca el
mismo agente que construyo, `maker != checker`) verifica en un clon limpio y emite un veredicto por exit
code; solo entonces se ratifica y se cierra. Un fallo se devuelve como fix-loop (tope de iteraciones antes
de escalar al humano). Las dos capas son complementarias: el recomputo del orquestador caza teatro y
sobre-entregas antes de gastar el ciclo del checker, y el checker adversarial caza defectos semanticos que
el recomputo no ve.

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
un agente implementador (maker) con capabilities de implementador/ingeniero de pruebas; un agente revisor
adversarial (checker) que permanece SIEMPRE en un modelo fuerte; y un operador humano. Politica de roster
vigente: los agentes-peon (modelos debiles, p.ej. locales) son ejecutores de codigo SUBORDINADOS al maker
-- el maker les asigna sub-tareas con especificacion detallada y responde por el resultado ante el revisor;
un peon nunca ocupa rol de revisor, orquestador ni firmante. El metodo tambien soporta instancias nacidas
operativas (born-operational) con su propio trio de agentes y gobernanza encapsulada, coordinadas por
lectura cruzada sin escribir el ledger ajeno. Las transiciones se autorizan por capability segun el
contenido del trabajo, no por el nombre del participante.

### 18.1 Guardarailes: capacidades y politicas configuradas

[INSTANCIA] Los **guardarailes** son los interruptores de configuracion que ARMAN o desarman los dientes
del metodo. Casi todos viven en `protocol.config.json`; unos pocos, pensados para moverse sin re-genesis,
viven en registros externos (`Area_comun/protocol/*.json`). Hay una **cadena dura de dependencias** que el
validador rechaza si se rompe: `authoritative => enforce => materialize => enabled` (poner uno sin su
predecesor es un error de config). En esta instancia las cuatro estan ON. La cadena por hash
(`chain_enabled`) liga el `canonical_hash` del config en el genesis -- por eso el config esta PINEADO (epoch
1.14.0, sha8 2E35F26E) y un cambio real exige un re-genesis coordinado; lo que debe moverse libremente se
mantiene FUERA del config pineado.

#### Capacidades y politicas (banderas)

- **`tool_policy`** (ON) -- Allowlist deny-by-default de herramientas por agente + capability + accion +
  scope: una llamada solo pasa si casa una regla de permiso. *Para* limitar que puede usar cada agente
  (incluidos conectores de accion). *Usar* cuando quieras acotar el acceso (DECISION-0044/0048).
- **`event_state.enforce`** (ON) -- EL hard-gate de escritor unico (B.3): rechaza toda edicion manual del
  ledger que difiera del replay firmado, asi que solo `submit_intent` puede escribir el estado. *Usar* SOLO
  cuando ambos loops de agente ya rutean cada transicion por `submit_intent`; si no, la primera edicion
  manual tras el flip rompe al peer (DECISION-0022/0028).
- **`authoritative`** (ON) -- Marcador declarativo del modo runtime-authoritative; no tiene dientes propios
  (los pone `enforce`). *Usar* junto a `enforce` para formalizar el modo; encenderlo solo se rechaza.
- **`supervised_autonomy`** (OFF) -- Habilita el bucle autonomo multi-turno ACOTADO (caps de turnos /
  checkpoint humano cada k / wall-clock). *Usar* solo con decision + aprobacion humana + caps + rollback
  ensayado. Riesgo: ejecucion desatendida (DECISION-0024/0027).
- **`real_invoker`** (OFF) -- Permite que el runtime llame a un LLM REAL (subproceso) en vez del invoker de
  replay. *Usar* solo para correr los presets CLI en vivo; requiere activacion + aprobacion. Riesgo: gasto
  y efectos reales. (La ejecucion autonoma real exige `real_invoker` Y `supervised_autonomy` -- ninguno solo
  la desbloquea.)
- **`sdd`** (NO adoptado aqui) -- Spec-Driven Development: exige campos de especificacion en las tareas
  implementables. *Usar* anadiendo el bloque `sdd` para forzar specs (DECISION-0004). En esta instancia NO
  se aplica (no hay bloque).
- **`intake_gate`** (ON, registro externo `INTAKE_GATE.json`, desde TASK-0238) -- Exige un intake DoR
  completo (8 campos) antes de `proposed -> ready`. *Usar* para forzar el Definition-of-Ready; vive fuera
  del config pineado para poder activarlo/avanzarlo sin re-genesis.
- **`maintenance`** (ON) -- Politica de poda/higiene: presupuesto de cold-start, cuantas tareas done /
  claims liberados quedan calientes, y las ventanas de las vistas slim. *Usar* para mantener el estado
  caliente eficiente en frio (lo consume `prune_state.py`).
- **`anchor_enabled`** (ON, remote local) -- Ancla periodica del head del log a un backend externo (git
  remote) + un evento `chain.anchor`. *Usar* para evidencia de manipulacion; requiere un remote alcanzable.
- **`slim_views_enabled`** (ON) -- Materializa las vistas podadas `*.slim.json` (solo tareas/claims
  calientes + colas recientes) para un cold-start barato. Depende de `materialize`.
- **`subagents_enabled`** (OFF) -- Habilita que el orquestador del runtime delegue subtareas a subagentes
  resumidores acotados. *Usar* para descargar subtrabajo con resumen acotado.
- **`compaction_enabled`** (ON) -- Compactacion de contexto (resumenes rodantes) y ademas EXIGE un
  `task_close_summary` al cerrar una tarea a done. *Usar* para mantener el contexto en presupuesto
  multi-turno.
- **`cost_attribution_enabled`** (ON) -- Emite eventos `cost.attributed` (marcados `applied:false`, no
  mutan el estado ni causan drift) con telemetria de coste por handoff/decision/agente. *Usar* para
  capturar coste en vivo (DECISION-0033).

#### Subsistemas

- **`runtime` (`adoption_tier`)** (ON) -- Declara la instancia tier-runtime (event-sourced + `submit_intent`
  + ledger atestado). Casi todos los gates `event_state.*` dependen de este tier; coordination-tier = flujo
  de ledger manual.
- **`event_auth`** (ON) -- Autenticacion HMAC de CADA evento con claves por agente (los secretos viven fuera
  del repo; nunca se commitean valores literales).
- **`event_state.enabled`** (ON) -- Switch maestro del subsistema de estado event-sourced; base de la cadena
  de dependencias.
- **`event_state.materialize`** (ON) -- Permite que el replay escriba el estado caliente (`Area_comun/
  state/*.json` + slim) en disco de forma atomica. Requiere un evento `protocol.genesis` primero.
- **`event_state.chain` (`chain_enabled`)** (ON) -- Encadena por hash el log (la cadena #4): cada evento
  liga su `prev_hash` y el genesis liga `canonical_hash(config)`. Da integridad append-only tamper-evident;
  consecuencia: config PINEADO (un bump real = re-genesis).
- **`event_state.agent_signatures` (`agent_signatures_enabled`)** (ON, 3 pubkeys) -- Atestacion ed25519 de
  los eventos `agent.attestation` (las afirmaciones firmadas de review/QA -- el "dataset"). Requiere las
  pubkeys en `signature_config`; las privadas quedan fuera del arbol.
- **`agent_registry`** (ON, 3 agentes) -- Fuente de verdad de QUIEN puede actuar y con QUE capability;
  `submit_intent` gatea cada intent contra ella (p.ej. task_upsert/decision exigen `orchestrator`; review/QA
  exigen `reviewer`/`qa`). Roster: Arquitecto (architect/reviewer/orquestador/qa), Codex (implementer),
  Analista (reviewer).
- **`attested_instancing`** (AUSENTE aqui) -- Ceremonia de instanciacion atestada (firmantes con llave,
  peones keyless, invariante de frontera). Solo se acuna en instancias PRODUCTO via `new_instance.py`
  (DECISION-0069/0095/0096). Este repo es el HUB de gobernanza neutral (DECISION-0050), no una instancia
  producto -- por eso el bloque no existe aqui.
- **`domain_neutrality`** (ON, denylist de 5 terminos) -- Guarda el core contra terminos de negocio/dominio
  (denylist + scan sobre templates/runtime/scripts). Una de las dos puertas de calidad nombradas
  (DECISION-0002).
- **`quality_policy`** (ON, caps 3/3) -- Acota los fix-loops de review/QA (`max_review_cycles` /
  `max_qa_cycles`) y PROHIBE self-review y self-QA; fuerza un checkpoint humano al agotar los ciclos.
  Guarda contra bucles infinitos y contra el rubber-stamping.

> **Como leer esto:** los guardarailes en OFF o ausentes (`supervised_autonomy`, `real_invoker`, `sdd`,
> `subagents_enabled`, `attested_instancing`) son capacidades DISPONIBLES no activadas aqui -- muestran el
> techo del metodo, no un hueco. Los ON son los dientes vivos de esta instancia. Encender los de mas riesgo
> (autonomia real, escritor-unico) exige decision registrada + aprobacion humana + rollback ensayado.

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
| 2026-07-17 | Actualizada al estado real: epoch 1.14.0 (pineado; releases aparte, ultima v1.19.0), runtime 0.12.0. Novedades de metodo: capa operacional exportable e instancias born-operational con trio propio; politica de roster peon-subordinado-al-maker con revisor siempre en modelo fuerte; capacidad de memoria persistente (repositorio caliente + indice derivado reconstruible + packs de revive con atestacion por fuente) ADOPTADA por demostracion, con su promocion al master planificada para una fase posterior a la ventana de medicion. |
| 2026-07-24 | Endurecimiento del gate local y consolidacion del export born-operational, todo por el ciclo gobernado de dos capas (recomputo del orquestador + checker adversarial). (1) El gate local en modo completo (`HOOK_FULL`) dejo de sobre-rechazar arboles limpios y **acota** la materializacion del snapshot a los deliverables realmente indexados, sin debilitar el rechazo de estado roto. (2) El estado gobernado con **JSON malformado** ahora falla de forma **graceful** (mensaje que nombra el archivo, exit no-cero, sin traceback) en el validador y en la poda, conservando el rechazo (integridad intacta). (3) El `prune --check` tambien **nombra** los archivos de archivo (`*_ARCHIVE.json`) malformados. (4) La **politica de roster** de la norma (agente-trabajador subordinado al maker; maker fuerte que gobierna y da especificacion completa; checker adversarial siempre fuerte, `maker != checker`) se **espeja** en el `AGENTS.template` con el que nace cada instancia nueva → toda instancia born-operational lo lleva en su contrato de roles, con la **fila del checker** añadida a la tabla de roles y la muestra generada minima y coherente. Evidencia viva del ciclo de dos capas: el recomputo del orquestador cazo un test con fixture auto-invalidante que rompia CI y una sobre-materializacion de la muestra (+20K lineas) antes de gastar el ciclo del checker; el checker adversarial cazo una colision de vocabulario (el termino "worker" capturaba al human owner) que el recomputo no vio. |
| 2026-07-27 | Nuevo apartado **18.1 Guardarailes: capacidades y politicas configuradas** (subseccion de "Roles y capacidades") -- referencia didactica de los interruptores del metodo (tool_policy, event_state.enforce/enabled/materialize/chain/agent_signatures, authoritative, supervised_autonomy, real_invoker, sdd, intake_gate, maintenance, anchor/slim/subagents/compaction/cost_attribution, runtime, event_auth, agent_registry, attested_instancing, domain_neutrality, quality_policy): que es, para que sirve, cuando usarlo y su estado en esta instancia, con la cadena dura de dependencias `authoritative => enforce => materialize => enabled` y la nota de config pineado. Fuente citada al codigo (rutas de config + `file:line` + DECISIONes). |
