# RUNBOOK P4b -- Alta de un AGENTE DE GOBERNANZA (firmante #4) via ceremonia de re-genesis-boundary

> Autor: Arquitecto. Fecha: 2026-08-02. Estado: **DISENO / RUNBOOK. NO EJECUTAR AUTONOMAMENTE.**
> Gobernado por DECISION-0109 (Nivel 2). Toca el FONDO INTOCABLE (config pineado 2E35F26E / epoca 1.14.0 /
> genesis). Ejecucion = evento CON EL OPERADOR PRESENTE, fuera de banda, con aprobacion humana. Ningun agente
> lo dispara solo. El front puede PREPARAR (recoger datos + checklist), pero el FLIP es esta ceremonia.

## Por que NO es un boton del front
El agente que FIRMA el ledger vive en `event_state.signature_config.public_keys` + `agent_registry` dentro de
`protocol.config.json`, que esta PINNED bajo #4: el genesis liga `canonical_hash(config)`. Anadir un firmante
CAMBIA el config -> el genesis viejo deja de casar -> hay que RE-GENERAR el boundary. Eso es una ceremonia
coordinada (no un toggle), porque un re-genesis mal hecho rompe la cadena (leccion: regenesis.py APPENDEA un
genesis, NO reemplaza; correrlo sobre un log con genesis deja DOS -> validate falla chain.genesis_missing).

## Precondiciones (gate humano)
1. DECISION nueva que autorice el alta del firmante concreto (identidad, rol, capacidades) + aprobacion del
   operador (cambio de boundary #4, AGENTS.md s4 / CLAUDE.md regla 2 y 6).
2. Ventana coordinada: ambos loops de agentes parados o al menos sin escribir el ledger; backup del estado.
3. La privada del nuevo firmante se genera y se queda SOLO en SU maquina (no en la maquina de build); al hub
   entra unicamente su PUBLICA. (Si es humano-firmante: nunca generar su privada aqui.)

## Pasos de la ceremonia (ejecucion CON el operador)
1. Backup: copia de `runtime/state/events.jsonl` + `protocol.config.json` + snapshot.
2. Editar `protocol.config.json`: anadir la PUBLICA del nuevo firmante en
   `event_state.signature_config.public_keys` (keyid nuevo) + su entrada en `agent_registry.agents`
   (capacidades). Provisionar su HMAC de instancia en el override (`event_auth.keys`) si aplica.
3. VACIAR `runtime/state/events.jsonl` (`: > ...`, con respaldo). El re-genesis NO reemplaza; exige log limpio.
4. Correr `runtime/regenesis.py` UNA sola vez con el config FINAL (el Arquitecto firma; `--timestamp
   1970-01-01T00:00:00Z` por convencion de boundary). El genesis liga `canonical_hash(config)` = JSON parseado
   (independiente de line-endings).
5. Verificar en CLON LIMPIO: `validate_collaboration_state.py` exit 0, `validate_chain` sin
   `chain.genesis_missing`/doble-genesis, drift 0, el nuevo firmante verifica su primer evento.
6. Anclar la Entrada de cross-atest con hashes por BLOB de git; reportar el commit-hash FINAL (`git rev-parse
   HEAD`), no el pre-amend (un `--amend` posterior cambia el hash citable).
7. Actualizar el epoch/CHANGELOG segun corresponda (nuevo boundary) + memoria dorada.

## Fail-safes / prohibiciones
- NUNCA re-firmar historia a mano ni re-anclar la cadena con un tool ad-hoc (no existe; leccion
  aegis-regenesis-chain-blocker). Si el re-genesis no puede re-anclar limpio, PARAR y escalar al operador.
- Si algo del FONDO INTOCABLE (2E35F26E / 1.14.0 / dataset N=500) se veria alterado fuera de este boundary
  deliberado -> ABORTAR.

## Rol del front (P4b, lo unico construible sin ceremonia)
El front puede, OFF-BY-DEFAULT: (a) recoger los datos del candidato (identidad, rol, pubkey) en un formulario;
(b) mostrar este checklist; (c) marcar "ceremonia pendiente". NO ejecuta ningun paso 1-7. El flip es la ceremonia
con el operador. (Construir ese formulario-preparatorio es opcional; puede ir en una tarea futura si el operador
lo pide -- no es necesario para "disenar P4b".)

## Estado
Runbook DISENADO. Ejecucion DIFERIDA (no hay un agente de gobernanza nuevo que dar de alta ahora, y tocaria el
FONDO INTOCABLE). Cuando el operador quiera onboardear un firmante real, se abre la DECISION concreta + se corre
esta ceremonia con el presente.
