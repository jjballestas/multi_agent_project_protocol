# APPLY - Ventana de PILOTO de #4 (provisioning -> re-genesis -> piloto REAL -> flip-si-verde)

> GO del operador (GO-piloto-flip-4, 2026-06-19). VENTANA PROPIA: NO combinar con Carril B/connector ni
> SA.4/Capa C/subagents. UN multiplicador. Deadline duro: #4 ON antes del primer handoff gobernado de la
> app (T0, no retrofiteable), objetivo < 2026-06-20 10:00. Operador PRESENTE para el checkpoint.
> Ejecutor = CLON LIMPIO que persiste (C:\\tmp\\protocol-clean o equivalente fuera del mount D: que se
> re-trunca). Base = origin/main v1.13.0 (cargador HMAC ya listo).

## Disciplina (OBLIGATORIA, leccion de la promocion)
Todo en el clon limpio: `git fetch + reset --hard origin/main` (== HEAD v1.13.0) -> verify (py_compile
runtime/*.py + validate --root . verde + drift 0 + git status limpio) -> apply -> read-back en disco ->
commit + push. Si entre verify y commit se re-trunca -> ABORTAR + re-restore + reintentar. NUNCA sobre D:.

## FASE 1 - PROVISIONING (AC1). Mutaciones de config + creacion de claves/anchor.

### 1a. Anchor (Opcion A, decidida por el operador)
- `git init D:\Agentes\audit-anchor` (repo HERMANO, NO anidado en el core; debe EXISTIR antes de
  anchor_enabled=true). Rama por defecto irrelevante; el runtime usa branch audits/default.
- Editar protocol.config.json (puntual): `event_state.anchor_config.remote_url = "D:\\Agentes\\audit-anchor"`
  (ruta absoluta PLANA, NO file://). branch=audits/default, identity=runtime-anchor (ya estan).
- Riesgo residual A3 DECLARADO (mismo disco, DECISION-0029). Fase B (push externo) despues.

### 1b. Firmas Ed25519 por agente (privada FUERA del repo)
- Cada agente del registry acuna su par Ed25519 en SU entorno (privada wrapper-side, via llm_turn_wrapper;
  guardada gitignored, p.ej. secrets/ed25519-<actor>.pem). COORDINACION: Arquitecto y Codex minten cada
  uno el suyo; "runtime" lo minta el ejecutor del clon. Registrar la PUBLICA en
  event_state.signature_config.public_keys[{key_id}] = <pub_b64>.
- Añadir `agent_registry.agents[]` (hoy ausente): por cada actor {id, key_id, auth:{key_id, secret_file}}.
  Actores: Arquitecto, Codex, runtime.

### 1c. HMAC event_auth (via el cargador v1.13.0; secret_file, NO literal)
- Generar un secreto HMAC aleatorio por actor -> secrets/eventauth-<actor>.key (gitignored).
- event_auth.keys[<actor>] = {"key_id": "<actor>:v1", "secret_file": "secrets/eventauth-<actor>.key"}.
  (NO secret literal inline; el gate AC4 dedicado rechaza literales de actor vivo.)
- Asegurar .gitignore cubre secrets/ (y/o .protocol-secrets/). Scan de secretos LIMPIO (cero privadas/
  secretos commiteados; solo refs).

### 1d. Smoke AC1 (negativo + positivo)
- Con (1a)-(1c) provistos: append_event y el PRIMER anclaje NO fallan.
- Sin la clave HMAC del actor: append_event falla "signing key missing/unresolved_key" (negativo).
- Sin anchor_config.remote_url: el primer anclaje falla (negativo).
- scan de secretos limpio.

## FASE 2 - RE-GENESIS (arbol limpio)
Introducir refs/claves/anchor cambia genesis -> `python runtime/regenesis.py` (en el clon limpio) ->
verificar drift 0 + replay == hot. (#4 sigue OFF en este punto: flags aun false.)

## FASE 3 - PILOTO REAL (operador PRESENTE + rollback ARMADO + 1 multiplicador)
Encender temporalmente los 4 flags (chain_enabled + agent_signatures_enabled + anchor_enabled +
event_auth.enabled = true) y correr EN VIVO sobre runs legitimos del propio protocolo:
- AC2 salud >=99% (N=20; denominador derivado del EVENT LOG, independiente del firmante).
- AC3 prueba negativa: 6 vectores (alteracion/borrado/insercion/reordenamiento/llave-no-registrada/
  atribucion-cruzada) RECHAZADOS con clase (binario, bloqueante).
- AC5 rollback ENSAYADO: 4 flags a false -> estado dormido byte-equivalente, replay==hot, drift 0.
- Reportar resultados (AC2 tasa, AC3 6/6, AC5 ok) al operador.
- ROLLBACK ARMADO: si algo falla o el operador aborta -> 4 flags a false + re-restore. NO flip.

## CHECKPOINT HUMANO (operador) - GATE DEL FLIP
PARAR aqui. El operador revisa los resultados del piloto. El flip (FASE 4) SOLO procede con su GO de
checkpoint sobre resultados VERDES. Sin GO -> no flip; rollback dormido; reportar.

## FASE 4 - FLIP (solo con GO de checkpoint del operador sobre piloto VERDE)
- Dejar los 4 flags en true en la instancia viva -> #4 ON.
- SemVer MINOR + CHANGELOG [nueva version] (#4 ON; provisioning; anchor Opcion A; riesgo A3 declarado).
- Cerrar TASK-0117 -> done (submit_intent, reviewer) en la tx atomica.
- read-back en disco: 4 flags true + version nueva + drift 0 + replay==hot. commit + push a canonico.
- Verificar ORIGIN/MAIN: 4 flags true + version nueva + TASK-0117 done. REPORTAR (piloto, version, drift 0).

## LIMITES
#4 ON es el techo: nada mas alla sin GO nuevo (SA.4/Capa C/subagents siguen OFF). DEF-PII (TASK-0118)
diferida; PII de terceros NUNCA al event log (la app leera Seguridad/Presupuesto con PII). NO tocar la DB
de Budget. Carril B PARQUEADO durante esta ventana. Canal ASCII en mailbox/state.
