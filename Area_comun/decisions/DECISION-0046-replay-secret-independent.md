---
decision_id: DECISION-0046
title: Replay secret-independiente - "verificacion no disponible" (clave ausente) != "verificacion fallo" (firma falsa); el estado canonico no debe depender de los secretos
status: proposed
ratified_at:
date: 2026-06-19
deciders: [operador humano, Arquitecto]
supersedes: []
superseded_by: []
relates_to: [DECISION-0045, DECISION-0043, DECISION-0039, DECISION-0022]
phase: P2
---

# DECISION-0046 - Replay secret-independiente

> PROPUESTA (operador GO 2026-06-19, "genera la solucion + Codex verificador"). Corrige el defecto que
> destapo el encendido de #4: el estado materializado depende de la disponibilidad de los secretos, lo que
> rompe la invariante de "validar desde clon limpio". maker = Arquitecto (aplica), checker = Codex (verifica).

## Contexto (el defecto, verificado en codigo)

Con #4 ON, `runtime/eventlog.py:replay_events` (lineas ~428-440) trata CUALQUIER `verify_event_auth` con
`valid != True` de forma identica: registra una rejection `security.unauthenticated_event` Y hace `continue`
(NO aplica el evento al bookkeeping: aggregate_versions / idempotency_keys / leases). Pero `verify_event_auth`
devuelve razones de DOS clases semanticas distintas:

- **Verificacion NO DISPONIBLE en este entorno** (`unresolved_key` = secret_file/secret_env no resoluble;
  `missing_key`): el checkout no tiene el secreto (gitignored). NO es un fallo de seguridad; es una
  limitacion de entorno. El evento es estructuralmente valido y viene del log commiteado (confiado por git).
- **Verificacion FALLO** (`invalid_signature` = firma presente pero HMAC no casa; tamper real;
  `missing_signature` cuando event_auth lo exige): hallazgo de seguridad real.

Consecuencia: un checkout CON secretos (instancia viva D:) reconstruye un estado (eventos aplicados,
rejections=[]); uno SIN secretos (clon limpio / CI) reconstruye OTRO (eventos NO aplicados, rejections con
N entradas). `assert_snapshot_matches` compara el snapshot guardado contra el rebuild del entorno donde
corre -> **ningun snapshot satisface ambos** -> la invariante "validar desde clon limpio sin secretos"
(la red de seguridad que el operador usa, DECISION-0045 leccion) deja de ser satisfacible post-#4.

## Decision

1. **El estado canonico materializado es SECRET-INDEPENDIENTE.** En `replay_events`, una razon de clase
   "verificacion no disponible" (`unresolved_key`, `missing_key`) **NO** registra rejection que mute el
   estado y **NO** salta la aplicacion del evento: el evento se aplica normalmente al bookkeeping (es
   estructuralmente valido y proviene del log commiteado). Asi el hash de estado es identico con o sin
   secretos.

2. **El tamper real sigue siendo un rechazo que muta el estado.** `invalid_signature` (y `missing_signature`
   cuando event_auth exige firma) se siguen registrando como `security.unauthenticated_event` y saltando la
   aplicacion -- ese SI es un hallazgo de seguridad y DEBE afectar el estado (deteccion de falsificacion
   intacta, AC3/A2 de #4 no se debilita).

3. **La verificacion criptografica sigue requiriendo secretos, como capa separada.** El gate de event_auth
   (verificar firmas) es una comprobacion APARTE del estado materializado: en un entorno sin secretos se
   reporta "no verificado aqui (faltan secretos)" como info/warning, NUNCA como fallo duro ni como mutacion
   de estado. La instancia viva (con secretos) SI verifica; cualquiera con los secretos puede verificar.

4. **Invariante restaurada.** Con (1)-(3), `validate_collaboration_state --root .` da exit 0 desde un clon
   limpio SIN secretos (estado reproducible) Y desde la instancia viva CON secretos, con el MISMO hash de
   estado. La "copia limpia" vuelve a ser una red de validacion valida para una instancia #4.

5. **Cambio de runtime -> SDD.** SPEC-0084 (acceptance_criteria + test_plan + goldens) + TASK-0122. maker =
   Arquitecto (implementa), checker = Codex (reproduce independiente, maker!=checker). Aditivo y neutral;
   no toca flags de #4 ni el boundary T0 (DECISION-0045). Al aterrizar, el snapshot canonico pasa a su forma
   secret-independiente (un commit de reconciliacion del snapshot del head).

## Alcance / No-alcance

- **En alcance:** distinguir clase de razon en replay_events; estado secret-independiente; goldens que
  prueban (a) rebuild con==sin secretos, (b) tamper real aun rechazado y state-afectante, (c) validate de
  clon limpio sin secretos exit 0; reconciliar el snapshot del head a su forma secret-independiente.
- **Fuera de alcance:** apagar/cambiar #4 o sus flags; el boundary T0 / sello (DECISION-0045, intacto);
  cambiar el formato de firma o el cargador de secretos (DECISION-0043).

## Consecuencias

- La red de seguridad "validar desde clon limpio" vuelve a funcionar para instancias #4 (sin meter secretos
  al repo).
- La deteccion de falsificacion (tamper) NO se debilita: solo se reclasifica "no puedo verificar (falta
  clave)" como entorno, no como rechazo.

## Alternativas consideradas

- **Exigir secretos para validar (no fix de codigo).** Aceptado como parche INMEDIATO (snapshot del head =
  estado con-secretos 215806be, para que D: valide ya), pero rompe el gate de clon-limpio-sin-secretos; por
  eso esta DECISION es la solucion de fondo.
- **Meter secretos al repo / CI.** Descartado: viola la frontera no-secretos (DECISION-0043).
