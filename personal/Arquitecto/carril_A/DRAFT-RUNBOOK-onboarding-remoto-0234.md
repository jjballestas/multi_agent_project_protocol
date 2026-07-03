# RUNBOOK_ONBOARDING_REMOTO.md - Onboarding remoto de un participante a una instancia de metodologia

> Draft del Arquitecto para TASK-0234 [VISION-NOVA][F2.5]. Destino: Area_comun/protocol/RUNBOOK_ONBOARDING_REMOTO.md
> Dominio-neutral. ASCII puro. Objetivo MEDIDO: onboarding operable <= 1 dia (alimenta HP6).

## 0. Que es esto y para quien

Runbook para que un participante NUEVO (empleado o agente) que **NO construyo la instancia** se una
en FRIO a una instancia de metodologia distribuida (p.ej. la instancia Aegis) usando SOLO Git, y
opere 1 tarea de principio a fin. Objetivo: estar operando en <= 1 dia sin pasos manuales ocultos
ni dependencias de dev. La prueba de que esto funciona es la transferibilidad fuerte (un agente
ajeno a la construccion opera); la MEDICION real (cronometrar a un empleado fresco) es la replica
employee-run pre-registrada, posterior a este doc.

## 1. Precondiciones (lo que el operador provee)

- URL del remoto PRIVADO de la instancia (repo git propio de la instancia; no el hub).
- Credenciales de acceso al remoto (solo lectura/escritura segun rol).
- Tu identificador de participante `<id>` (el que tendras en el registro de agentes de la instancia).
- Git instalado. En Windows: `git config --global core.longpaths true` (rutas largas).

## 2. Paso a paso (onboarding)

1. **Clonar la instancia** (no el hub): `git clone -c core.longpaths=true <URL-remoto-privado> <carpeta>`.
2. **Leer en frio** (orden de arranque, sin asumir contexto): `AGENTS.md` (s.0 How to Start), luego
   `Area_comun/README.md`, `Area_comun/protocol/TASK_PROTOCOL.md`, y el estado en
   `Area_comun/state/` (PROJECT_STATE, TASK_INDEX, CLAIMS) + `Area_comun/mailbox/open/`.
3. **Configurar tu agente** (Git es el adapter; config COMMITEADA): copia/edita tu config en
   `.agents/<id>/config.json` segun el template de la instancia (workspaceRoot, adapter=git,
   committedConfig=true). NO se instalan adapters multi-IDE ni herramientas externas de memoria.
4. **Verificar que el canonico valida verde** antes de tocar nada:
   `python scripts/validate_collaboration_state.py` exit 0 (y encoding/neutralidad).
5. **Registrar tu alta** (si aplica) via el flujo gobernado de la instancia (submit_intent), no a mano.

## 3. Operar 1 tarea completa (ciclo distribuido, solo via Git)

Usa el ciclo pull -> escribir -> push INMEDIATO (harness distribuido de la instancia):
1. `git pull` (trae claims/estado de otros clones).
2. **Claim** la tarea via submit_intent (ventana segura: sin claim de peer sobre tus rutas).
3. `git push` INMEDIATO (tu claim se hace visible a los otros clones; evita colision).
4. Trabaja el entregable; **entrega** a in_review (submit_intent) + handoff autocontenido + envelope
   7 campos como texto final del turno.
5. `git push` inmediato. El checker hace pull, revisa, y su veredicto vuelve por pull.
6. Con GO, el cierre a done ocurre por el flujo gobernado (implementer), coordinado solo via Git.

Regla anti-colision: escribe el ledger solo en ventana segura (peer sin lock, tree sin half-write)
y pushea inmediato; nunca dejes cambios de ledger sin pushear mientras otro clon opera.

## 4. Troubleshooting

- **validate rojo en clon limpio:** hay drift (state sin materializar). Re-materializa desde el
  event log o pide al coordinador que reconcilie; no operes sobre canonico rojo.
- **push rechazado (non-ff):** `git pull --rebase --autostash` y re-push; otro clon escribio primero.
- **claim bloqueado:** otro clon tiene claim activo sobre tus rutas; espera y reintenta (no fuerces).
- **rutas largas (Windows):** `core.longpaths=true` al clonar.

## 5. Definition of Done del onboarding

Estas operando cuando: clonaste la instancia, tu `.agents/<id>/config.json` esta commiteado, el
canonico valida verde en tu clon, y completaste 1 tarea de prueba (claim -> entrega -> cierre) solo
via Git, con tu estado visible en otros clones. Objetivo: <= 1 dia. El tiempo real se registra
(alimenta HP6) cuando la instancia mide el onboarding (replica employee-run).
