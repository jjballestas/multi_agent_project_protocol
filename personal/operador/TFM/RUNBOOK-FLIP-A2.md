# RUNBOOK — Flip A2 (encender actor_auth Ed25519 en turnos vivos) — v2 (por RUNTIME OVERRIDE)

> Autor: Arquitecto · v2 2026-06-27 (reescrito tras TASK-0192). Gobierna: DECISION-0065/0067 (mecanismo +
> override) + DECISION-0045 (ensayo en copia) + DECISION-0046 (secret-indep). **Con el operador presente.**
> **v1 OBSOLETA:** el ensayo (DECISION-0045) demostro que el flag-en-config rompia `chain.genesis`; TASK-0192 lo
> movio a un **runtime override fuera del config pinned**, asi que **el flip YA NO es un re-genesis** — es un
> cambio de runtime limpio. Verificado en re-ensayo: override -> `actor_auth ed25519` + validate exit 0 +
> `protocol.config.json` byte-identico (chain.genesis intacto).

## 0. Naturaleza: cambio de RUNTIME (no toca config ni genesis)

Encender A2 = **crear el archivo gitignored `event-state.runtime.json`** (override). NO se edita
`protocol.config.json` -> `canonical_hash(config)` no cambia -> `chain.genesis` intacto -> **sin re-genesis**,
cadena continua, el dataset abarca el flip sin discontinuidad. Apagar = borrar el override.

## 1. Precondicion (cumplida)

- TASK-0190 (firma A2) + TASK-0192 (override) cerradas. Publicas en `signature_config.public_keys`
  (keyids `arquitecto:v1`/`codex:v1`/`analista:v1`); privadas en `D:/Agentes/protocol-secrets/`
  (`*-ed25519-private.pem`); HMAC secrets en `<repo>/secrets/eventauth-*.key`.
- Pre-registro v2.0 FROZEN+atestado; harness listo. NO combinar con real_invoker/SA (DECISION-0039 §5).

## 2. ENSAYO EN COPIA — recomendado (ya validado por el Arquitecto)

> El Arquitecto ya re-ensayo el flip por override en clon limpio (verde). Re-ensayar de nuevo es opcional pero
> barato; si lo haces, clona a RUTA CORTA (MAX_PATH) y copia `secrets/` + usa `protocol-secrets` (abs).

## 3. Flip en VIVO (operador presente)

1. **Estado de partida sano:** `git status` limpio relevante; `validate` exit 0; drift 0; anota HEAD.
2. **Crear el override** en la raiz del repo: **`event-state.runtime.json`** (gitignored; NO commitear):
   ```json
   {
     "event_state": {
       "actor_auth_enforce": true,
       "actor_auth_config": {
         "secret_root": "D:/Agentes/protocol-secrets",
         "keyids": { "Arquitecto": "arquitecto:v1", "Codex": "codex:v1", "Analista": "analista:v1" },
         "private_key_files": {
           "Arquitecto": "D:/Agentes/protocol-secrets/arquitecto-ed25519-private.pem",
           "Codex": "D:/Agentes/protocol-secrets/codex-ed25519-private.pem",
           "Analista": "D:/Agentes/protocol-secrets/analista-ed25519-private.pem"
         }
       }
     }
   }
   ```
   (El runtime lo lee por defecto en `event-state.runtime.json`, o via `EVENT_STATE_RUNTIME_CONFIG_PATH`.)
3. **NADA de editar el config ni regenesis.** El flip ya esta hecho (el override existe).

## 4. Verificacion post-flip (gates)

- `python scripts/validate_collaboration_state.py` -> **exit 0** (sin "genesis mismatch"); drift 0; `chain.genesis`
  intacto; `protocol.config.json` byte-identico al de antes.
- **Prueba viva A2:** emitir un `submit_intent` real (claim no-op o project_narrative) y confirmar que el evento
  lleva `actor_auth:{method:"ed25519", keyid:<actor>, sig}` verificable con la publica.
- Confirmar que **cada agente** firma con SU privada en su proximo turno; si a uno le falta la privada accesible,
  su `append_event` falla-closed -> provisionar y reintentar.
- **Importante:** cada runtime de agente debe tener el MISMO override activo (o `EVENT_STATE_RUNTIME_CONFIG_PATH`
  apuntando al mismo archivo) para firmar; coordinar que crones/wrappers lo vean.

## 5. A partir de aqui (el experimento)

A2 vivo -> generar el **dataset** (N>=500 turnos, >=2 agentes, sin PII) -> correr el **harness** (TASK-0191) sobre
una **copia** del dataset (inyeccion A1/A2/A3 + deteccion/FPR/sobrecoste + verificador externo) -> comparar con los
umbrales del **pre-registro v2.0** -> redactar.

## 6. ROLLBACK (trivial)

- **Borrar `event-state.runtime.json`** (o poner `actor_auth_enforce:false`) -> los turnos vuelven a
  `not_enforced_phase2` + HMAC (integridad/cadena/ancla siguen vivas); los eventos ya firmados Ed25519 quedan en la
  historia. `validate` exit 0. Reversible, sin re-genesis, sin perder historia.
- **Aborto:** si tras crear el override `validate` se pone rojo o `append_event` falla por privada ausente ->
  borrar el override, diagnosticar en frio, reintentar.

## 7. Resumen (vivo, operador presente)

```bash
# 0. sano
python scripts/validate_collaboration_state.py; echo exit=$?            # 0, drift 0
# 1. crear event-state.runtime.json (override de §3)  [NO commitear]
# 2. verificar
python scripts/validate_collaboration_state.py; echo exit=$?            # 0, SIN genesis mismatch
# 3. prueba viva: un submit_intent y revisar actor_auth.method==ed25519
# 4. (NO se commitea el override ni se toca el config/genesis)
# ROLLBACK: rm event-state.runtime.json ; validate
```
