# DEBATE: gap de instanciacion -- la capa OPERACIONAL no se exporta (harness + skills)
# 2026-07-14 ~01:50 local. Draft de debate (NO rutear, NO sellar, NO entregar sin orden explicita).
# Disparador: el Arquitecto de NOVA no tiene analista_mailbox_cron.ps1 (ni codex_*), ni .protocol-tmp/.
# Posicion del operador: es una falla de la instanciacion de la metodologia. "Esta mal".

## 1. Coincido en el fondo, con un matiz de diagnostico

La falla es REAL pero no es "el export olvido archivos": es un ERROR DE CAPAS en el hub.
Los harnesses (codex_mailbox_cron.ps1 472L, analista_mailbox_cron.ps1 502L,
arquitecto_cron.ps1 582L) viven en `personal/<peer>/` -- areas PRIVADAS. new_instance.py
(correctamente) NO exporta contenido personal: crea las areas del roster VACIAS
(.gitkeep + LLM_PRESET.md). Consecuencia estructural: infraestructura archivada como
"tooling personal" cae SILENCIOSAMENTE fuera de toda instancia nueva.

Causa raiz: **infraestructura operacional mal archivada en areas privadas.** La regla del
export es correcta; la ubicacion del harness no lo es. (Historia: los .ps1 nacieron como
runners "de cada peer" en su area; nunca se promovieron a capa compartida.)

Mismo patron que ya cazamos con las skills: las 4 skills de metodologia (.claude/skills/)
tampoco se exportan -- por eso las neutralice y copie A MANO a NOVA (5dea820). Ese
pendiente ya existe (cablearlas a new_instance.py, DECISION-0061). El hallazgo del harness
es la MISMA clase de gap, capa distinta.

## 2. Que nace hoy con una instancia vs que no (verificado en new_instance.py)

SI nace (ships hoy):
- Esqueleto de gobierno: Area_comun/ completa, runtime/, scripts/ (validadores+gates),
  protocol.config.json, genesis, CI workflow, .gitattributes LF, Aegis/.claude scaffold.
- Capa de skills NEUTRAL `skills/` (codegen-triage, delegate-to-worker,
  **session-watchdogs** -- las recetas de watchdogs SI existen ahi --, loader).
- personal/<agente>/ del roster (vacias, con LLM_PRESET.md).

NO nace (los gaps):
- **Harnesses de peers** (los 3 cron .ps1) -- el hallazgo de hoy.
- **Skills de agente-ops** (.claude/skills: ledger-ops, monitor-coordina, cron-lifecycle,
  mailbox-hygiene, guarda-estado) -- pendiente DECISION-0061 ya identificado.

NO nace y esta BIEN que no nazca (documentarlo, no "arreglarlo"):
- `.protocol-tmp/` = estado de RUNTIME gitignored que el harness CREA en su primera
  corrida (locks, leases, runs/, seen.json). No es un entregable; su ausencia en NOVA es
  SINTOMA del harness ausente, no un gap propio. (Respuesta directa al Arquitecto de
  NOVA: no lo pidas, nace solo.)
- Llaves/credenciales/overrides locales (out-of-band por diseno).

## 3. La buena noticia: neutralizar el harness es barato

Verificado: la hub-especificidad de los .ps1 es BAJA (2-4 valores cableados por archivo:
ruta del repo, ruta del producto en el texto del prompt, refs GOAL-* en arquitecto_cron).
Toda la maquinaria pesada (lock, lease, seen.json, exec con STDIN, watchdog de deadline,
STOP_JOB endurecido post-0236, runs/*.log) ya es generica. Neutralizacion = parametrizar
root + peer id + comando CLI + plantilla de prompt de instancia. Mismo tratamiento que
las 4 skills.

## 4. Opciones para sellar el fix (cuando salga del debate)

- **A (mi recomendacion): promover el harness a capa compartida versionada del core.**
  Mover los .ps1 a `scripts/harness/` (o `harness/`) como plantillas parametrizadas;
  `personal/` vuelve a ser SOLO privado; new_instance.py los exporta junto con las skills
  de agente-ops neutralizadas. UNA DECISION coherente que cierra las dos capas del gap
  ("instancias born-operational"): extiende/absorbe DECISION-0061.
  Caveat honesto: los .ps1 son Windows-only; el core aspira a neutralidad de plataforma
  (precedente: validador py+ps1). Documentar "harness reference implementation =
  PowerShell; port py = trabajo futuro" y listo -- todas las instancias reales hoy son
  Windows.
- **B: harness como profile** (DECISION-0002 layering): `profiles/windows_ps_harness/`.
  Mas "puro" en neutralidad de plataforma; mas piezas moviles. Diferible: A ahora, B si
  aparece una segunda plataforma.
- **C: no shippear codigo, solo runbook** (el operador copia a mano). RECHAZADA: es
  exactamente la friccion que acabamos de vivir 2 veces (skills, harness).

## 5. NOVA mientras tanto (nada bloqueado)

- TASK-9391 NO depende de esto: el checker one-shot no necesita harness (ya respondido
  en la RESP A-G). El gate puede cerrar hoy.
- Cuando haya orden: entrego a NOVA los harnesses de Codex + Analista NEUTRALIZADOS
  (prep en mi area; mismo pipeline que las skills). El arquitecto_cron NO va por defecto
  (orquestador autonomo; su header dice "lo lanza el operador" y el Arquitecto de NOVA
  corre interactivo).
- `.protocol-tmp/`: nada que entregar; nace en la primera corrida del harness.

## 6. Valor de evidencia (para el log del asesor, no lo escribo yo alli)

Friccion real de transferibilidad cazada por dogfooding: instancia nace sin capa
operacional -> copia manual de skills (13-jul) -> pedido manual de harness (14-jul).
Dos ocurrencias de la misma clase = patron, no accidente. El fix (export de la capa
operacional) es medible: la proxima instancia debe nacer operando sin copias manuales.

## Salida del debate (cuando el operador ordene)

1. GO "prepara/entrega harness a NOVA" -> neutralizo codex+analista .ps1 y los entrego
   (via clon-inject-push a NOVA.git o handoff al Arquitecto de NOVA, a eleccion).
2. GO "sella el fix de instanciacion" -> DECISION (enmienda/extension 0061) + TASK a
   Codex (mover harness a capa compartida + cablear export + test de instanciacion que
   VERIFIQUE que una instancia fresca trae harness+skills) + gate Analista.
3. Sin GO -> queda este draft; nada ruteado.
