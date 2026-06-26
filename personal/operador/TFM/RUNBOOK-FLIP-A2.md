# RUNBOOK — Flip A2 (encender actor_auth Ed25519 en turnos vivos)

> Autor: Arquitecto · 2026-06-27 · Para: operador. Gobierna: DECISION-0065 (mecanismo) + DECISION-0039 §5 (ventana
> de riesgo) + DECISION-0045 (nunca pilotar contra el log vivo; ensayar en copia) + DECISION-0047 (época/genesis).
> Es el paso de ACTIVACIÓN del cutover A2 del TFM. **Con el operador presente. NO autónomo.**

## 0. Naturaleza: NO es un flag-toggle, es un RE-GÉNESIS-BOUNDARY

Verificado: el flag `event_state.actor_auth_enforce` vive **solo en `protocol.config.json`** (sin override de
runtime), y el **genesis = `canonical_hash(protocol.config.json)`**. Por tanto **editar el flag cambia el hash del
config → invalida `chain.genesis`** salvo que se reescriba el genesis con **`runtime/regenesis.py`** (mismo
mecanismo que la activación #4, DECISION-0045). Es decir: el flip es una **ceremonia de re-génesis-boundary**, no
un toggle. Trátalo como tal: ensayo en copia + operador presente + rollback armado + una sola ventana de riesgo.

## 1. Precondición (ya cumplida)

- Mecanismo A2 construido off-by-default (TASK-0190; camino OFF byte-idéntico verificado).
- Claves: públicas Ed25519 en `signature_config.public_keys`; privadas por agente en `D:/Agentes/protocol-secrets/`.
- Pre-registro v2.0 FROZEN + atestado (#4), atestación medida = `actor_auth` Ed25519.
- Harness de medición listo (TASK-0191).
- **NO combinar** con `real_invoker`/`supervised_autonomy` ni cambios de `authoritative` (DECISION-0039 §5: un solo
  multiplicador por ventana).

## 2. ENSAYO EN COPIA DESECHABLE — OBLIGATORIO ANTES DEL VIVO (DECISION-0045)

> Nunca el primer flip sobre el log vivo. Ensaya el ciclo completo en una copia y solo entonces hazlo en vivo.

```bash
# clon limpio a RUTA CORTA (Windows MAX_PATH; lección TASK-0190)
git -c core.longpaths=true clone D:/Agentes/multi_agent_project_protocol C:/t/flipA2
cd C:/t/flipA2
# (provisionar acceso a las privadas como en el vivo, o usar fixtures)
```
En la copia, ejecutar los pasos 3–5 completos + el rollback (paso 6) y confirmar: validate exit 0, drift 0, los
turnos llevan `actor_auth.ed25519`, y el rollback restaura el estado dormido. Si algo falla → diagnosticar en frío;
NO tocar el vivo hasta que el ensayo sea verde end-to-end.

## 3. Flip en VIVO (operador presente)

1. **Backup/punto de retorno:** anota el HEAD de git y el `canonical_hash` actual del config; confirma working
   tree limpio, `validate` exit 0, drift 0 (estado de partida sano).
2. **Editar el config:** en `protocol.config.json`, `event_state.actor_auth_enforce` → **true** (y completar
   `event_state.actor_auth_config` si el ensayo mostró que hace falta: rutas de privadas por agente, keyids).
3. **Re-génesis** (re-ancla el genesis al nuevo hash del config; preserva el event-log):
   ```bash
   python runtime/regenesis.py --actor-id Arquitecto --timestamp <UTC ISO> --commit flip-a2-regenesis
   ```
   Verificar en la salida: `drift_before` → `drift_after = 0`.
4. **Decisión de época (DECISION-0047):** el re-génesis es un cambio de época. Decide si bumpear `protocol_version`
   para marcar la época A2 (recomendado, p.ej. una MINOR nueva) o dejarlo; reconciliar AGENTS.md ↔ config ↔
   CHANGELOG si bumpeas (la verdad de versión ya está sincronizada).

## 4. Verificación post-flip (gates)

- `python scripts/validate_collaboration_state.py` → exit 0 (con y sin secretos en clon limpio).
- drift 0; `chain.genesis` nuevo coherente; `event_auth` HMAC + anchor siguen ON.
- **Prueba viva de A2:** emitir un `submit_intent` real (p.ej. un `project_narrative` o un claim no-op) y confirmar
  que el evento lleva `actor_auth: {method:"ed25519", keyid:<actor>, sig:...}` **verificable con la pública**.
- Confirmar que **otro agente** (Codex/Analista), al escribir su próximo turno, también firma Ed25519 (cada runtime
  accede a SU privada). Si un agente no tiene su privada accesible → su `append_event` falla-closed: provisionar y
  reintentar.

## 5. A partir de aquí (el experimento)

Con A2 vivo: generar el **dataset** (N≥500 turnos, ≥2 agentes, sin PII) → correr el **harness** (TASK-0191) sobre
una **copia** del dataset (inyección A1/A2/A3 + detección/FPR/sobrecoste + verificador externo) → comparar con los
umbrales del **pre-registro v2.0** → redactar.

## 6. ROLLBACK armado

- **Reverso:** `event_state.actor_auth_enforce` → **false** (revertir el config) + `python runtime/regenesis.py
  --actor-id Arquitecto --timestamp <UTC> --commit rollback-a2-regenesis` → drift 0.
- Resultado: los turnos vuelven a `not_enforced_phase2` + HMAC (integridad/cadena/ancla **siguen vivas**); los
  eventos ya firmados con Ed25519 quedan en la historia (no se pierden). Reversible.
- **Criterio de aborto:** si tras el flip `validate` se pone rojo, `append_event` falla por privada ausente, o
  drift ≠ 0 → ejecutar el rollback, diagnosticar en frío, reintentar (idealmente re-ensayando en copia).

## 7. Resumen de comandos (vivo, con operador presente)

```bash
# 0. estado sano
git rev-parse HEAD; python scripts/validate_collaboration_state.py; echo exit=$?
# 1. editar protocol.config.json: event_state.actor_auth_enforce=true   (editor)
# 2. re-génesis
python runtime/regenesis.py --actor-id Arquitecto --timestamp 2026-06-27T..:..:00Z --commit flip-a2-regenesis
# 3. verificar
python scripts/validate_collaboration_state.py; echo exit=$?     # esperado 0, drift 0
# 4. prueba viva A2: un submit_intent y revisar actor_auth.method==ed25519
# 5. commit del flip (config + genesis + state) con rutas explícitas, y push
# ROLLBACK si hace falta: flag=false + regenesis + validate
```
