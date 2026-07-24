---
# Identidad de la instancia (la llena el adoptante). Es la fuente de los campos del header del HTML.
nombre: <NOMBRE_DE_LA_INSTANCIA>
estado: <activo | en-pausa | archivado>
protocol_version: <X.Y.Z>
runtime_version: <X.Y.Z | no-aplica>
adoption_tier: <coordination | runtime>
perfiles: [<perfil-1>, <perfil-2>]
idioma: <es | en | ...>
actualizado: <YYYY-MM-DD>
---

<!--
PLANTILLA MASTER NEUTRAL (regla 5: los *.template.* son masters publicados).
Esta es la GUIA HUMANA OPERATIVA. El .md es la UNICA fuente de verdad; el HTML se GENERA con
scripts/generate_human_guide.py y NUNCA se edita a mano (el HTML lleva un banner "GENERADO - NO EDITAR").
Convenciones para el adoptante y para el generador:
  - Cada seccion lleva una linea de metadatos: <!-- origen: CORE|INSTANCIA|CORE+INSTANCIA | tier: todos|runtime|opcional | campo: obligatorio|opcional|no-aplica[: motivo] -->
  - [CORE] = contenido del metodo, igual en toda instancia (puedes dejarlo tal cual).
  - [INSTANCIA] = lo llenas tu; reemplaza los placeholders <...>.
  - Secciones solo-runtime se marcan "no aplica" automaticamente si adoption_tier = coordination.
  - Las checklists usan "- [ ]"; los callouts de seguridad usan "> [SEGURIDAD] ...".
  - NEUTRAL DE DOMINIO: no escribas nombres de negocio, stack concreto ni nombres propios de agentes
    (usa los roles genericos: agente operativo, agente revisor, operador humano, runtime, instancia,
    core, protocolo). La neutralidad es de dominio, no de idioma.
-->

# Guia humana operativa - <NOMBRE_DE_LA_INSTANCIA>

> Panorama. <Una o dos frases: que es esta instancia y para quien es esta guia. Cualquier persona o
> agente nuevo deberia entender, leyendo este documento, que es, que hace, como se construye/ejecuta/
> prueba/opera, como se diagnostica, donde estan las rutas del protocolo, que roles hay y como retomar
> el contexto.>

- **Instancia:** <NOMBRE_DE_LA_INSTANCIA>  ·  **Estado:** <activo>  ·  **Tier:** <coordination | runtime>
- **Protocol version:** <X.Y.Z>  ·  **Runtime version:** <X.Y.Z | no-aplica>  ·  **Perfiles:** <...>
- **Fuente de verdad:** este `.md`. El `.html` es un artefacto generado (no editar a mano).

## 1. Identidad de la instancia
<!-- origen: INSTANCIA | tier: todos | campo: obligatorio -->

<Nombre, proposito en una linea, responsable(s) humanos, repositorio, licencia. Quien la opera y a
quien se reporta.>

## 2. Que es esta instancia
<!-- origen: INSTANCIA | tier: todos | campo: obligatorio -->

<Descripcion en lenguaje llano: que problema resuelve y en que consiste, sin jerga de stack.>

## 3. Que hace
<!-- origen: INSTANCIA | tier: todos | campo: obligatorio -->

<Capacidades principales / que entrega a sus usuarios. Lista breve de funciones observables.>

## 4. Como lo hace
<!-- origen: INSTANCIA | tier: todos | campo: obligatorio -->

<Enfoque a alto nivel: el approach o estrategia con que cumple lo de la seccion 3, sin entrar todavia
en componentes.>

## 5. Arquitectura
<!-- origen: INSTANCIA | tier: todos | campo: obligatorio -->

<Vista de arquitectura: piezas mayores y como se relacionan. Un diagrama ASCII simple es bienvenido.>

## 6. Componentes principales
<!-- origen: INSTANCIA | tier: todos | campo: obligatorio -->

<Lista de componentes/modulos con una linea cada uno: responsabilidad y ubicacion (ruta).>

## 7. Flujo operativo
<!-- origen: CORE+INSTANCIA | tier: todos | campo: obligatorio -->

[CORE] El trabajo se organiza en tareas de un solo dueño con ciclo de vida
`proposed -> ready -> claimed -> in_progress -> in_review -> done` (ramas `blocked` / `cancelled`); la
coordinacion ocurre en el area comun (estado, claims, buzon, handoffs) y el avance deja señales
verificables.

[INSTANCIA] <Como se ve ese flujo aqui en concreto: quien propone, quien implementa, quien revisa, y
el ritmo de trabajo de esta instancia.>

## 8. Flujo de datos
<!-- origen: INSTANCIA | tier: todos | campo: obligatorio -->

<Que datos entran, como se transforman y que sale; donde viven (rutas/almacenes). Sin secretos.>

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

[INSTANCIA] <Que perfiles/decisiones adopta esta instancia y cualquier ajuste local de la metodologia
(p.ej. gates extra, perfiles profesionales activos).>

## 11. Como se construye
<!-- origen: INSTANCIA | tier: todos | campo: obligatorio -->

<Pasos de build (comandos exactos), prerequisitos/toolchain, artefactos producidos.>

```text
<comando de build>
```

## 12. Como se ejecuta localmente
<!-- origen: INSTANCIA | tier: todos | campo: obligatorio -->

<Como levantar/usar la instancia en local: comandos, variables de entorno (sin valores secretos),
puertos/rutas.>

```text
<comando de ejecucion local>
```

## 13. Como se prueba
<!-- origen: INSTANCIA | tier: todos | campo: obligatorio -->

<Como correr las pruebas/gates de calidad y como leer un resultado verde/rojo.>

```text
<comando de pruebas>
```

- [ ] <gate 1: descripcion y como verificar que pasa>
- [ ] <gate 2>

## 14. Como se despliega o lanza
<!-- origen: INSTANCIA | tier: opcional | campo: opcional: si la instancia no se despliega, marcar no-aplica con motivo -->

<Procedimiento de despliegue/lanzamiento si aplica: entornos, pasos, rollback. Si no aplica (p.ej.
libreria o documento), declarar "no aplica: <motivo>".>

## 15. Como se opera
<!-- origen: INSTANCIA | tier: todos | campo: obligatorio -->

<Operacion del dia a dia: tareas recurrentes, monitoreo, mantenimiento, ritmos. Quien hace que.>

## 16. Troubleshooting
<!-- origen: INSTANCIA | tier: todos | campo: obligatorio -->

<Sintomas comunes -> causa probable -> remedio. Tabla o lista. Incluir como diagnosticar antes de
actuar y a quien escalar.>

| Sintoma | Causa probable | Remedio |
|---|---|---|
| <sintoma> | <causa> | <remedio> |

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

[INSTANCIA] <Que participantes y capacidades estan configurados aqui (segun `agent_registry`), descritos
por ROL y capability, sin acoplar la guia a nombres propios. Ej.: "1 implementador, 1 revisor, 1
operador humano".>

## 19. Seguridad y datos sensibles
<!-- origen: CORE+INSTANCIA | tier: todos | campo: obligatorio -->

[CORE] No se commitean secretos (claves, tokens, material de firma). El material real de firma/credenciales
pertenece al emisor o a su CI y nunca entra al repositorio.

> [SEGURIDAD] <Donde viven los secretos de esta instancia (gestor/variable de entorno), como se rotan,
> y que datos sensibles maneja. Nunca pegues valores reales aqui.>

[INSTANCIA] <Politicas de seguridad/datos especificas de la instancia, si las hay.>

## 20. Continuidad, traspaso y recuperacion de contexto
<!-- origen: CORE | tier: todos | campo: obligatorio -->

[CORE] Un participante que entra en frio retoma leyendo: `AGENTS.md` seccion "How to Start", el estado
vivo en `Area_comun/state/`, el buzon en `Area_comun/mailbox/open/` y el punto de retoma de la instancia
(`RESUME.md` u hoja de arranque equivalente / `cold_start_globs`). Cada tarea y handoff es
autocontenido; nadie asume el contexto de otro.

## 21. Historial de cambios
<!-- origen: INSTANCIA | tier: todos | campo: obligatorio -->

<Bitacora breve y local de cambios de ESTA guia (no del proyecto entero; eso es el CHANGELOG). Fecha +
una linea por cambio relevante de arquitectura/roles/tier.>

| Fecha | Cambio |
|---|---|
| <YYYY-MM-DD> | <cambio> |
