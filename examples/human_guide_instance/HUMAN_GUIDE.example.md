---
nombre: Instancia de ejemplo neutral
estado: activo
protocol_version: 1.1.0
runtime_version: no-aplica
adoption_tier: coordination
perfiles: [base]
idioma: es
actualizado: 2026-06-10
---

# Guia humana operativa - Instancia de ejemplo neutral

> Panorama. Esta es una instancia de EJEMPLO del protocolo, neutral de dominio, para mostrar como se
> instancia la guia humana operativa. Cualquier persona o agente nuevo deberia entender, leyendo este
> documento, que es la instancia, que hace, como se construye/ejecuta/prueba/opera, como se diagnostica,
> donde estan las rutas del protocolo, que roles hay y como retomar el contexto.

- **Instancia:** Instancia de ejemplo neutral  ·  **Estado:** activo  ·  **Tier:** coordination
- **Protocol version:** 1.1.0  ·  **Runtime version:** no-aplica  ·  **Perfiles:** base
- **Fuente de verdad:** este `.md`. El `.html` es un artefacto generado (no editar a mano).

## 1. Identidad de la instancia
<!-- origen: INSTANCIA | tier: todos | campo: obligatorio -->

Instancia de ejemplo del protocolo multiagente. Proposito: servir de referencia neutral de la guia. La
opera un equipo de ejemplo (un operador humano) y se reporta al operador humano. Repositorio y licencia:
los define el adoptante al instanciar.

## 2. Que es esta instancia
<!-- origen: INSTANCIA | tier: todos | campo: obligatorio -->

Un proyecto de software de ejemplo que adopta el protocolo de coordinacion multiagente. En lenguaje llano:
organiza el trabajo de varios agentes y un operador humano en tareas de un solo dueño con estado compartido.

## 3. Que hace
<!-- origen: INSTANCIA | tier: todos | campo: obligatorio -->

- Coordina tareas entre participantes con un ciclo de vida explicito.
- Mantiene un estado vivo compartido (tareas, claims, buzon, decisiones).
- Deja una traza verificable de cada avance y handoff.

## 4. Como lo hace
<!-- origen: INSTANCIA | tier: todos | campo: obligatorio -->

Aplica el metodo del protocolo: tareas pequeñas y verificables de un solo dueño, coordinacion en el area
comun y decisiones registradas antes de aplicarse. Sin automatizacion de runtime (tier coordination).

## 5. Arquitectura
<!-- origen: INSTANCIA | tier: todos | campo: obligatorio -->

```text
participantes ---> Area_comun/ (estado + buzon + decisiones) ---> handoffs ---> entregables
       (operador humano + agentes)            (fuente de verdad compartida)
```

## 6. Componentes principales
<!-- origen: INSTANCIA | tier: todos | campo: obligatorio -->

- Contrato compartido: `AGENTS.md` (las reglas del proyecto).
- Estado vivo: `Area_comun/state/` (tareas, claims, estado del proyecto).
- Coordinacion: `Area_comun/mailbox/`, `Area_comun/handoffs/`, `Area_comun/decisions/`.

## 7. Flujo operativo
<!-- origen: CORE+INSTANCIA | tier: todos | campo: obligatorio -->

[CORE] El trabajo se organiza en tareas de un solo dueño con ciclo de vida
`proposed -> ready -> claimed -> in_progress -> in_review -> done` (ramas `blocked` / `cancelled`); la
coordinacion ocurre en el area comun (estado, claims, buzon, handoffs) y el avance deja señales
verificables.

[INSTANCIA] Aqui un participante propone, otro implementa y un tercero revisa; el ritmo lo marca el
operador humano. La ambiguedad se vuelve `blocked` con una pregunta concreta.

## 8. Flujo de datos
<!-- origen: INSTANCIA | tier: todos | campo: obligatorio -->

Entran tareas y mensajes de coordinacion; se transforman en cambios de estado y entregables; salen a los
artefactos del area comun y al control de versiones. Todo en texto plano, sin secretos.

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

[INSTANCIA] Esta instancia adopta el perfil base y no activa runtime; no hay gates extra mas alla de los
del core.

## 11. Como se construye
<!-- origen: INSTANCIA | tier: todos | campo: obligatorio -->

No requiere build: son artefactos de texto (Markdown + JSON). El toolchain minimo es un interprete para
los validadores.

```text
# no aplica build; validar el estado de coordinacion
python scripts/validate_collaboration_state.py --root .
```

## 12. Como se ejecuta localmente
<!-- origen: INSTANCIA | tier: todos | campo: obligatorio -->

Se "ejecuta" leyendo el estado y operando las tareas; no hay servicio que levantar.

```text
# revisar el estado vivo y el buzon
type Area_comun/state/PROJECT_STATE.json
```

## 13. Como se prueba
<!-- origen: INSTANCIA | tier: todos | campo: obligatorio -->

Las pruebas son los gates de calidad del protocolo. Verde = salida sin errores y codigo de salida 0.

```text
python scripts/validate_collaboration_state.py --root .
```

- [ ] Validador de estado de coordinacion en verde
- [ ] Escaneo de neutralidad sin hallazgos

## 14. Como se despliega o lanza
<!-- origen: INSTANCIA | tier: opcional | campo: opcional: si la instancia no se despliega, marcar no-aplica con motivo -->

No aplica: es un ejemplo documental; no se despliega ni se lanza.

## 15. Como se opera
<!-- origen: INSTANCIA | tier: todos | campo: obligatorio -->

Operacion diaria: revisar el buzon, atender tareas `ready`, dejar una señal de avance por turno y
registrar decisiones cuando cambian limites. El operador humano aprueba politica y cierres.

## 16. Troubleshooting
<!-- origen: INSTANCIA | tier: todos | campo: obligatorio -->

| Sintoma | Causa probable | Remedio |
|---|---|---|
| Validador en rojo | Estado inconsistente entre indice y archivo de tarea | Reconciliar y re-validar |
| Tarea trabada | Ambiguedad sin resolver | Pasar a `blocked` con una pregunta concreta |

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

[INSTANCIA] Aqui hay un operador humano, un agente implementador y un agente revisor, descritos por rol
y capability segun el registro de agentes.

## 19. Seguridad y datos sensibles
<!-- origen: CORE+INSTANCIA | tier: todos | campo: obligatorio -->

[CORE] No se commitean secretos (claves, tokens, material de firma). El material real de firma/credenciales
pertenece al emisor o a su CI y nunca entra al repositorio.

> [SEGURIDAD] Los secretos de esta instancia, si los hubiera, viven en variables de entorno o en un gestor
> externo; nunca se pegan valores reales en la guia.

[INSTANCIA] Sin datos sensibles propios: es un ejemplo documental.

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
| 2026-06-10 | Guia de ejemplo creada como referencia neutral de instanciacion |
