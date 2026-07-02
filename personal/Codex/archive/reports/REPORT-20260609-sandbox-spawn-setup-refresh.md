# Informe - Fallo del sandbox Windows (`spawn setup refresh`)

Fecha: 2026-06-09  
Autor: Codex  
Estado: borrador privado para evaluar una regla de mitigacion

## Resumen ejecutivo

Durante varias verificaciones del repo `multi_agent_project_protocol`, comandos simples ejecutados dentro del
sandbox de herramientas fallaron antes de iniciar el proceso real con el error:

```text
windows sandbox: spawn setup refresh
```

El fallo no parece originarse en el repositorio, ni en PowerShell, Python, Git o `rg`. La evidencia apunta a un
problema del host/sandbox de Codex en Windows: el entorno no logra preparar el contenedor/perimetro de ejecucion
para lanzar procesos. Los mismos comandos funcionaron al reintentarse fuera del sandbox con aprobacion.

## Evidencia observada

- `Write-Output SANDBOX_OK` fallo dentro del sandbox con `windows sandbox: spawn setup refresh`.
- El mismo fallo ocurrio incluso sin `workdir`, por lo que no depende de `D:\Agentes\multi_agent_project_protocol`.
- Comandos afectados en distintos momentos:
  - `Get-Content`
  - `Get-ChildItem`
  - `rg`
  - `python ...`
  - `git log`
  - comandos PowerShell triviales
- `git status --short` a veces si respondio dentro del sandbox, lo que sugiere fallo intermitente/parcial.
- Al ejecutar los mismos comandos con `sandbox_permissions: require_escalated`, funcionaron.
- TEMP era escribible y habia espacio suficiente en disco.
- Se observaron muchos procesos `codex.exe app-server --listen stdio://` vivos desde sesiones anteriores.
- `protocol_state_drift` siguio reportando `has_drift=false`; no hubo evidencia de corrupcion del repo por este
  fallo.

## Causas posibles

1. **App-server de Codex/sandbox helper atascado o en contencion**
   - La presencia de multiples `codex.exe app-server --listen stdio://` de sesiones antiguas sugiere que el
     backend local de Codex puede haber quedado en estado inconsistente.
   - Esto encaja con un fallo de preparacion del sandbox antes de ejecutar el comando.

2. **Limite de recursos o handles por procesos acumulados**
   - Aunque disco y TEMP estaban bien, muchos procesos persistentes pueden agotar handles, locks, pipes stdio o
     recursos internos del host.
   - El fallo intermitente encaja con contencion, no con falta permanente de un binario.

3. **Condicion de carrera al lanzar comandos en paralelo**
   - El primer fallo visible ocurrio durante una lectura paralela amplia.
   - La paralelizacion no necesariamente causo el problema, pero pudo exponerlo o aumentar la probabilidad.

4. **Bug del sandbox Windows en la fase de refresh**
   - El texto `spawn setup refresh` indica una fase interna de preparacion, no el proceso hijo real.
   - Que falle `Write-Output` descarta casi por completo errores del comando solicitado.

5. **Sesion larga de Codex/VS Code**
   - Procesos vivos desde varios dias sugieren que reiniciar la app podria limpiar el estado.
   - La sesion larga tambien aumenta la probabilidad de estado cacheado obsoleto.

## Impacto operativo

- Verificaciones locales pueden producir falsos negativos de herramienta.
- El agente puede pedir aprobaciones `require_escalated` con mas frecuencia, lo que genera ruido para el operador.
- Si no se distingue este fallo de un error real del repo, puede inducir diagnosticos equivocados.
- En modo `event_state.authoritative`, un fallo del sandbox puede bloquear validaciones o `submit_intent` aunque el
  repo este sano.

## Mitigacion inmediata recomendada

1. Ante el primer `windows sandbox: spawn setup refresh`, reintentar una prueba minima:

   ```powershell
   Write-Output SANDBOX_OK
   ```

2. Si la prueba minima falla, clasificar el problema como **fallo del sandbox local**, no del repo.

3. No lanzar baterias largas ni paralelas dentro del sandbox mientras falle la prueba minima.

4. Si el trabajo es urgente y seguro, reintentar comandos concretos con `require_escalated`, explicando que el
   sandbox no logra iniciar procesos.

5. Si el fallo persiste, el operador deberia:
   - cerrar Codex/VS Code;
   - terminar procesos `codex.exe app-server --listen stdio://` antiguos que queden vivos;
   - reabrir Codex;
   - reintentar `Write-Output SANDBOX_OK`.

## Propuesta de regla

Nombre sugerido: **Regla de salud del sandbox antes de escalado**

Texto propuesto:

> Si un comando falla con `windows sandbox: spawn setup refresh`, el agente debe ejecutar una prueba minima
> sandboxed (`Write-Output SANDBOX_OK`). Si la prueba minima tambien falla, debe tratarlo como fallo del sandbox
> local, no como fallo del repositorio. A partir de ese momento no debe lanzar suites largas ni paralelas dentro
> del sandbox; puede reintentar solo comandos necesarios con `require_escalated`, explicando la causa, y debe
> recomendar al operador reiniciar Codex/VS Code y limpiar procesos `codex.exe app-server` antiguos. Una vez
> reiniciado, la primera accion debe ser repetir la prueba minima antes de continuar.

## Reglas complementarias

- **No diagnosticar el repo desde un fallo de spawn.** Un error de `spawn setup refresh` no cuenta como fallo de
  validador, test o script.
- **Escalado minimo y trazable.** Usar `require_escalated` solo para comandos concretos necesarios, no para suites
  amplias por defecto.
- **Paralelismo conservador tras fallo.** Suspender `multi_tool_use.parallel` para shell hasta que la prueba minima
  del sandbox vuelva a pasar.
- **Registro operativo.** Si ocurre durante una verificacion importante, dejar un FYI en mailbox o memoria con:
  comando afectado, texto exacto del error, workaround usado y estado final.

## Criterio de cierre

La situacion se considera mitigada cuando:

- `Write-Output SANDBOX_OK` pasa dentro del sandbox;
- al menos un comando de lectura (`Get-Content AGENTS.md`) pasa dentro del sandbox;
- una validacion corta (`python scripts\validate_collaboration_state.py --root .`) corre sin requerir escalado;
- no quedan procesos `codex.exe app-server --listen stdio://` antiguos no asociados a la sesion activa.

## Decision pendiente

Esta regla puede incorporarse como:

- nota operativa en `personal/Codex/STARTUP_PROMPT.md` (ya reflejada);
- runbook compartido en `Area_comun/protocol/` si el operador quiere que aplique a todos;
- decision formal si se convierte en politica obligatoria del protocolo.

Como afecta a la operacion de agentes y no al contrato del protocolo de negocio, parece suficiente una regla
operativa compartida. Si se vuelve obligatoria para todos los agentes, conviene registrarla por decision.
