# 05_Asistente - GO PRE-AUTORIZADO de #3 (para correr de noche, fail-closed)

> Insumo del operador (asistente Cowork) para el ARQUITECTO (Claude en VS Code).
> El operador da este GO a sabiendas, con condiciones, antes de dormir. Reversible (flag false restaura).
> El asistente no muta estado ni habla con Codex; esto lo ejecuta el arquitecto via submit_intent.
> Fecha: 2026-06-14. Cierra #3; supersede el GO condicional previo en cuanto a cost_tokens.

## Decision cerrada: cost_tokens = OPCION A (tokens_total + context_tokens)
El invoker NO da split prompt/completion, pero el runtime SI mide input-contexto (assembled_context_tokens,
proxy chars/divisor) y hoy solo vive en el run-log efimero (gitignored). Como el log de eventos es inmutable
y mi foco es reducir input-contexto:
- `cost_tokens` = tokens_total (escalar autoreportado por el orquestador). `cost_unit="tokens_total"`.
  Bump `cost_schema` a "2" por el cambio de forma.
- NUEVO campo `context_tokens` = assembled_context_tokens, capturado por handoff desde el dia 1, durable
  en el corpus inmutable.
- HONESTIDAD (analista pasada-3 §3): `context_tokens` es un PROXY (chars/divisor), NO un conteo real.
  Debe llevar su propio unit tag explicito, p. ej. `context_unit="assembled_proxy_chars_div"`. Ni
  `cost_tokens` ni `context_tokens` se nombran "medicion de tokens" en la prosa: son total autoreportado
  y proxy de contexto, respectivamente.
- Es un cambio de esquema mas ANTES de activar (inmutable-safe). Golden cubre la nueva forma.

## GO de activacion (pre-autorizado, en este orden estricto)
1. Implementa la Opcion A (cost_tokens/cost_unit/cost_schema=2 + context_tokens/context_unit) por el metodo:
   actualiza DECISION-0033 / SPEC-0079 / golden. Golden verde, sin regresion (intent_flow, budget, eventlog,
   enforce, observability), validador/encoding/neutralidad verdes, drift 0.
2. Codex re-revisa el codigo endurecido (maker!=checker REAL, no sello). Si Codex objeta algo sustantivo:
   PARA, deja la tarea en su estado, y reporta. No fuerces.
3. Avanza TASK-0111 in_progress -> in_review -> (con tu revision) done, por submit_intent.
4. Activacion: pon `metrics.cost_attribution_enabled=true` SOLO tras (1)-(3). Haz la VERIFICACION EN CALIENTE:
   sobre un evento/handoff real, asierta que lo registrado corresponde al dato real del momento (no un
   literal), con drift 0 y replay==hot. SemVer MINOR 1.6.0 + entrada en CHANGELOG.
5. Cierra. Reporta resultado para mi ratificacion al despertar.

## FAIL-CLOSED (innegociable)
Si CUALQUIER condicion no se cumple -- Codex objeta, golden rojo, drift != 0, replay != hot, la verificacion
en caliente no muestra el dato real, o aparece un hard-fail -- DETENTE, deja todo en estado consistente
(flag en false), y reporta el bloqueo. NO improvises, NO fuerces, NO actives a medias. Prefiero despertar a
"bloqueado, por esto" que a un estado forzado.

## GATE DURO (separado)
NO actives #4 (chain_enabled / agent_signatures_enabled / anchor_enabled) hasta cerrar TASK-0113 (bug
event_without_chain_fields no excluye event_auth). Si no, los cost.attributed del piloto rompen el prev_hash.
TASK-0113 corre en paralelo por Codex (SPEC-0080, golden combinado). SA.4 sigue SIN disparar. subagents OFF.

## Para mi al despertar
- Estado de #3: activado y 1.6.0 cerrado, o bloqueado con motivo.
- Resultado de la verificacion en caliente (el numero real capturado).
- Estado de TASK-0113.
- Cualquier matiz para ratificar o revertir.
```
Resumen para pegar al arquitecto: "GO pre-autorizado de #3 con cost_tokens=Opcion A (tokens_total +
context_tokens proxy, ambos con unit tag honesto, cost_schema=2). Implementa por el metodo, Codex re-revisa
(real), activa SOLO si todo verde + verificacion en caliente con dato real + drift 0 + replay==hot, MINOR
1.6.0 + CHANGELOG, cierra. FAIL-CLOSED: ante cualquier fallo, para y deja flag en false + reporta. NO toques
#4/chain/auth hasta cerrar TASK-0113. SA.4 sin disparar. Reporta para mi ratificacion."
```
