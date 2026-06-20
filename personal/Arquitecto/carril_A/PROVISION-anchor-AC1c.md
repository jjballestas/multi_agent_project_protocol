# PROVISION - Ancla externa #4 (SPEC-0081 AC1c) - opcion A, A3 residual declarado

> Instrucciones del operador (2026-06-19). ENCOLADO, NO aplicado. Entra SOLO con: arbol verificado
> limpio == HEAD + GO de provisioning del operador + dentro de la ventana de piloto (bundle con el resto
> del provisioning #4). Ejecutor = MIRROR en checkout fresco. #4 OFF hasta el piloto real.
> CONFIRMADO contra codigo (runtime/eventlog.py:anchor_to_git_remote).

## Pasos

1. **Repo dedicado HERMANO** del protocolo (NO anidado en el repo): `D:\Agentes\audit-anchor`
   - `git init` + crear `anchors.log` vacio inicial (commitear el log vacio).
   - DEBE EXISTIR antes de `anchor_enabled=true` o el primer anclaje falla. (`mkdir` auto-crea el dir,
     pero NO el repo git ni el log -> por eso git init explicito = repo de auditoria real.)

2. **protocol.config.json** -> `event_state.anchor_config` (edicion PUNTUAL):
   - `remote_url`: `"D:\\Agentes\\audit-anchor"`  (ABSOLUTA PLANA; NO `file://` -- el strip `[7:]` de
     file:// se rompe con rutas Windows `D:`; la ruta plana cae en la rama limpia `Path(remote_url)`).
   - `branch`: `"audits/default"`  (metadata; este backend de archivos no la usa)
   - `identity`: `"runtime-anchor"`
   - `interval_seconds`: `3600`
   - (Esta edicion es genesis-afectante -> va con el re-genesis del bundle de provisioning, arbol limpio.)

3. **Smoke AC1c** (con anchor_enabled en la ventana del piloto):
   - POSITIVO: con `remote_url` provisto + repo existente, `append_event` dispara el anclaje y escribe
     `D:\Agentes\audit-anchor\anchors.log` (linea `{ts} {head_digest} runtime-anchor`) + `HEAD`.
   - NEGATIVO: con `remote_url=""`, el primer anclaje falla con
     `EventLogError("anchor git-remote backend requires remote_url")`.

4. **RIESGO RESIDUAL A3 (declarar, NO ocultar):** el ancla vive en el MISMO disco/usuario que el runtime
   -> independencia DEBIL (el escritor unico puede reescribir `anchors.log`; el backend escribe archivos
   directo, no `git push` a un remoto fuera de su control). Aceptable SOLO para probar la metodologia;
   ya declarado en DECISION-0029 (A3-restringido) + SPEC-0081 Risks. **NO afirmar independencia fuerte.**
   Mitigacion parcial: cadencia corta + atestaciones huerfanas del revisor (ventana sin anclar = residual).

## Gating / sequencing
- NO se aplica ahora. Precondicion: (a) loader v1.12.0 (DECISION-0043/SPEC-0082/TASK-0120) RECONCILIADO y
  commiteado (en curso); (b) TASK-0120 implementada (cargador HMAC) -- el ancla AC1c es INDEPENDIENTE del
  cargador, pero el provisioning #4 completo bundlea ambos; (c) arbol limpio == HEAD; (d) GO de
  provisioning del operador; (e) ventana de piloto con operador presente.
- Bundle de provisioning #4 (ventana del operador): public_keys por agente + agent_registry +
  HMAC por `secret_file` gitignored (via cargador TASK-0120) + ESTE ancla -> re-genesis en arbol limpio ->
  piloto REAL (AC2 N=20 / AC3 6 vectores / AC5 rollback) -> flip #4 si verde. #4 OFF hasta ese flip.
