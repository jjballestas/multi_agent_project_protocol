---
decision_id: DECISION-0063
title: Launcher del runtime del Arquitecto VIVO (lo que el puente hace spawn) - gobernado, identidad existente, no-bypass, off-by-default, operador presente
status: accepted
ratified_at: 2026-06-26
date: 2026-06-26
deciders: [operador humano, Arquitecto]
supersedes: []
superseded_by: []
relates_to: [DECISION-0062, DECISION-0057, DECISION-0022, DECISION-0040, DECISION-0038, DECISION-0050]
phase: P2
---

# DECISION-0063 - Launcher del runtime del Arquitecto vivo

> ACCEPTED (operador ratifico 2026-06-26). El operador dio GO a "activar el uso de la consola" y eligio CONSTRUIR
> EL LAUNCHER (SDD). La consola (DECISION-0062) ya tiene puente+UI+auditoria, pero el puente hace
> `spawn(config.command)` y no existia un comando que lance un Arquitecto interactivo. Implementacion = SPEC-0101 +
> TASK-0188 (maker=Codex / checker=Arquitecto). La ACTIVACION VIVA real es un paso final con el operador presente.
> Codigo en Zeus-protocol; gobernanza aqui. NO toca #4.

## Contexto

El puente de la consola (DECISION-0062, TASK-0185) mantiene un proceso hijo vivo y le pasa cada mensaje del
operador por stdin, transmitiendo su stdout. Para "uso vivo real" ese hijo debe ser un **runtime interactivo del
Arquitecto** (turno a turno). Hoy no hay tal comando (los crons de Codex/Analista son wrappers de mailbox, no un
Arquitecto interactivo). Construir el launcher es el faltante real.

## Decision

1. **Launcher = wrapper gobernado de larga vida** (en Zeus-protocol) que el puente hace `spawn`. Contrato: lee
   mensajes del operador por **stdin** (uno por `send`), ejecuta un **turno del Arquitecto** invocando el runtime
   de Arquitecto **configurado**, y emite la salida del Arquitecto por **stdout** (que el puente transmite). Larga
   vida = mantiene contexto de la sesion entre turnos.

2. **Identidad EXISTENTE, runtime-only (espejo DECISION-0057/0062).** El launcher ejecuta al Arquitecto con su
   **identidad/keypair YA registrada**; NO crea ni reconfigura identidad/llaves/`agent_registry`. No es alta de
   agente (eso es re-genesis-boundary). El launcher no concede ninguna capacidad que el Arquitecto no tenga.

3. **NO-BYPASS (invariante dura).** El Arquitecto lanzado sigue TODAS las reglas: toda mutacion de estado va por
   `submit_intent` (#4 escritor unico, DECISION-0022). El launcher/consola NO es ruta de escritura al ledger; es
   solo el medio interactivo. El Arquitecto vivo respeta neutralidad del core y narracion minima (DECISION-0038).

4. **Runtime de Arquitecto = dependencia de ENTORNO declarada** (como Ollama para file-ingestion). El binario/CLI
   concreto del Arquitecto se declara en el **runtime config gitignored** (`architect-bridge.runtime.json`:
   `command`/`args`), nunca commiteado. Off-by-default; sin ese config no hay launcher.

5. **Sesion unica del Arquitecto (anti-colision) + AVISO al operador.** A lo sumo UN Arquitecto vivo. El puente
   serializa su propia sesion, PERO no conoce una sesion de Arquitecto externa (VS Code/CLI). **El operador no debe
   tener otra sesion de Arquitecto activa mientras usa la consola viva** (la regla "no dos Arquitectos en
   paralelo"). El launcher documenta y, donde pueda, detecta/rechaza el solapamiento.

6. **Off-by-default, operador presente, cese honrado, auditado.** Nace APAGADO (heredado de DECISION-0062);
   activacion = el operador pone el runtime config + esta presente. La orden de cese finaliza el runtime. La
   conversacion se audita redactada y fuera del #4 (DECISION-0040, pieza 3 ya entregada).

7. **Costo/riesgo.** Es un agente de IA VIVO -> off-by-default + operador presente + sesion unica + cese honrado +
   auditoria. La activacion real es un paso con el operador presente, no un commit.

8. **Repos (DECISION-0050) + SDD por pieza.** Launcher en Zeus-protocol (producto); gobernanza/SPEC aqui. Tras
   ratificar: SPEC-0101 + TASK-0188 (el launcher + su contrato stdin/stdout + sesion unica + identidad existente +
   no-bypass + off-by-default), maker=Codex / checker=Arquitecto. La activacion viva = paso final con el operador.

## Alcance

- **En alcance:** el launcher del runtime del Arquitecto que el puente hace spawn (single-operator, un Arquitecto).
- **Fuera de alcance:** launchers para Codex/Analista/otros; la fabrica NOVA; multi-tenant; alta/baja de agente
  (re-genesis, RF-9); cambiar la identidad/keypair del Arquitecto.

## Consecuencias

- La consola pasa de "fontaneria lista" a "uso vivo posible": el operador puede dirigir al Arquitecto desde el
  front, manteniendo #4 escritor unico, identidad existente y auditoria redactada.
- Coste/riesgo: correr un Arquitecto vivo es la superficie mas potente del sistema -> por eso todas las guardas.

## Alternativas consideradas

- **Comando provisto por el operador (sin construir):** valido si ya hubiera un Arquitecto interactivo en pipe;
  el operador prefirio construir el launcher gobernado (no existe ese comando hoy).
- **Demo con echo:** solo prueba la fontaneria; no es uso vivo real. Descartado como meta (util solo para smoke).
