# REVIEW - TASK-0301: veredicto OK-CLOSABLE (fixture de re-parentacion de nietos)

- Reviewer: Analista (voz adversarial independiente / checker)
- Hora local: 2026-07-29 15:44 (UTC+2)
- Ancla canonica: clon LIMPIO del hub en `D:/Aegis_Scratch/protocol/ccv0301`, checkout HEAD
  `a5396f818b44e9297bbd3003832aba061c9d913a` (contiene el test entregado, BYTE-IDENTICO a la impl.
  `ccd80b7`; delivery `49b893c`; baseline pre-0301 `2742b58`).
- Alcance declarado por la instruccion: HUB-ONLY, SOLO COBERTURA DE TEST en
  `examples/mailbox_retry_cases/run_mailbox_retry_cases.py`. El `.ps1` NO se toca (el fix de tree-kill
  vive en TASK-0300). Sin producto Zeus/Nova en alcance.

## Veredicto: OK-CLOSABLE

Verifique por COMPORTAMIENTO en clon limpio los 4 AC del intake, ataque la VACUIDAD de AC2 con una
sonda instrumentada independiente (no confie en el nombre ni en el conteo del test), y corri la suite
3 veces para descartar flakiness. Todo verde. Un residual menor de test-hardening, no bloqueante,
declarado abajo.

## Reproduccion (exit codes reales, clon limpio a5396f8)

Gates del hub:
```
python scripts/validate_collaboration_state.py   -> OK: collaboration state is valid.  (exit 0)
python scripts/scan_encoding.py                  -> OK: encoding scan is clean.         (exit 0)
python scripts/scan_domain_neutrality.py         -> (exit 0)
```

Suite de regresion (AC3, sin flakiness):
```
python examples/mailbox_retry_cases/run_mailbox_retry_cases.py  -> PASS  (exit 0)   RUN 1
python examples/mailbox_retry_cases/run_mailbox_retry_cases.py  -> PASS  (exit 0)   RUN 2
python examples/mailbox_retry_cases/run_mailbox_retry_cases.py  -> PASS  (exit 0)   RUN 3
```
`run_complete_tree_kill_case()` registrado e invocado en `main()` (linea 131); tambien
`run_exec_running_heartbeat_case()` (0302), `run_pre_delivery_and_liveness_cases()` (0303/0304),
`run_post_delivery_timeout_case()`. No es funcion muerta.

Sonda adversarial independiente (extraje `Stop-LeaseProcessTree` del `.ps1` del clon, reconstrui el
mutante quitando el barrido, e instrumente el hook con un contador de llamadas a Get-CimInstance y un
mapeo pid->rol root/child/grand):
```
[REAL + intact]            survivors=[]                 get_ciminstance_calls (n/a: sin hook)
[REAL + reparent]  (AC1)   survivors=[]                 get_ciminstance_calls=1
[MUTANT + reparent](AC2)   survivors=['grand']          get_ciminstance_calls=1
[MUTANT + NO reparent]     survivors=['child','grand']  (control)
OVERALL_PROBE_PASS=True   (exit 0)
```

## Ataque a la VACUIDAD (AC2 es el vector critico)

1. **La produccion llama Get-CimInstance SIN CUALIFICAR y EXACTAMENTE UNA VEZ.** Lectura de fuente:
   `Stop-LeaseProcessTree` contiene un unico `Get-CimInstance Win32_Process -ErrorAction Stop` (BFS de
   descendientes construido de ESA sola foto). Confirmado tambien en runtime: mi contador registro
   `get_ciminstance_calls=1`. Por tanto el override del hook (`function Get-CimInstance {...}`) SI
   intercepta -> el hook DE VERDAD re-parenta (mata el hijo intermedio tras capturar el snapshot). No
   es CimCmdlets\Get-CimInstance cualificado, asi que el escenario NO es vacuo.

2. **El unico survivor del mutante es GENUINAMENTE el nieto re-parentado (pids[2]), no un crash del
   probe.** Mi sonda mapeo el pid superviviente a su rol: `survivors=['grand']`. Como Get-CimInstance
   se llama una sola vez, el `Stop-Process -Id $IntermediatePid -ErrorAction Stop` del hook se ejecuta
   una sola vez sobre un hijo VIVO -> no hay segundo kill de un proceso ya muerto -> el probe no aborta
   -> el survivor NO es espurio. La preocupacion "Get-CimInstance >1 vez -> throw -> survivor por la
   razon equivocada" no se materializa.

3. **El `assert len(mutant_survivors) == 1` es un DISCRIMINADOR REAL de re-parentacion, no un conteo
   debil.** Control independiente: MUTANTE + SIN re-parentacion da `['child','grand']` = 2 survivors
   (el hijo no muere temprano, ambos sobreviven al quitar el barrido). Es decir: si el hook fuese vacuo
   (Get-CimInstance cualificado, o no llamado) el conteo seria 2 y el `assert len==1` FALLARIA. Y un
   crash del probe daria 2 o 3 survivors, tampoco 1. El unico camino que produce exactamente 1 es el
   intencional: hijo muerto por el hook (prueba que el hook disparo) + nieto huerfano superviviente
   porque se quito el barrido. El test no puede pasar por vacuidad.

## Tabla vector-por-vector

| Vector | Criterio | Resultado | Evidencia |
|--------|----------|-----------|-----------|
| AC1 | arbol raiz->hijo->nieto; hijo muerto tras snapshot y antes del kill; nieto re-parentado; helper REAL asevera 0 survivors | PASS | suite 3x exit 0; sonda `[REAL + reparent] survivors=[]`, hook disparo (calls=1) -> el barrido recoge al nieto |
| AC2 | falsable NO VACUA: mutante (barrido eliminado) + re-parentacion => EXACTAMENTE 1 survivor, genuinamente el nieto | PASS | sonda `[MUTANT + reparent] survivors=['grand']`; control no-reparent=2 survivors prueba discriminacion; produccion Get-CimInstance sin cualificar, 1 sola llamada -> sin crash |
| AC3 | suite exit 0; 0300 intacto (asercion reparent=False), 0302/0303/0304 verdes; estable 2-3 corridas | PASS | 3 corridas consecutivas exit 0; `run_complete_tree_kill_case` invocado L131; asercion intact-tree `exercise(real, reparent=False)==[]` preservada |
| AC4 | solo run_mailbox_retry_cases.py cambio vs baseline; config y .ps1 byte-identicos; fondo intocable | PASS | `git diff 2742b58 HEAD` fuera de ledger => solo el test; hash-object base==head: config `81cf406e...`, .ps1 `d54febc6...` IDENTICOS |
| Gates | validate + scan_encoding + scan_domain_neutrality exit 0 | PASS | los tres exit 0 en clon limpio |

Ninguna fuga (SLIP) detectada.

## Residual declarado (no bloqueante)

- **R1 (test-hardening, cosmetico):** el test asevera `len(mutant_survivors) == 1` (CONTEO), no
  `mutant_survivors == [pids[2]]` (IDENTIDAD). Mi sonda confirma que HOY el survivor ES el nieto y que
  el conteo==1 es un discriminador robusto (no-reparent->2, crash->distinto de 1), asi que la cobertura
  actual es CORRECTA y FALSABLE. Es solo que un refactor futuro podria, en teoria, satisfacer
  conteo==1 por otro camino sin que el test lo note. Sugerencia OPCIONAL para un endurecimiento
  posterior: fijar la identidad (`mutant_survivors == [pids[2]]`). NO cambia el veredicto: la
  falsabilidad requerida por AC2 esta satisfecha por comportamiento.

## Recomendacion de cierre

**OK-CLOSABLE.** Los 4 AC verificados por comportamiento en clon limpio; AC2 (el vector critico) es
falsable y NO vacuo con evidencia instrumentada de re-parentacion real e identidad del survivor;
sin regresion y sin flakiness en 3 corridas; alcance test-only con config y `.ps1` byte-identicos y
fondo intocable. Residual R1 es un nit opcional de endurecimiento, no un defecto.

-- Analista
