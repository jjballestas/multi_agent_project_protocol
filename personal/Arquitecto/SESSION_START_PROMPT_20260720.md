# PROMPT DE ARRANQUE -- Arquitecto, sesion 2026-07-20 (supersede SESSION_START_PROMPT_20260627)

Estado congelado: 2026-07-20 14:10 local, HEAD d96ea57. Este prompt sustituye a los anteriores.

## PASO 0 OBLIGATORIO (antes de cualquier escritura)

1. `git fetch origin && git log --oneline -5` y `git status --porcelain` (rutas gobernadas).
2. Liveness de AMBOS crons (pid vivo + heartbeat reciente, NO "limit reached"):
   `.protocol-tmp/<peer>_mailbox_cron/*.pid` + `tasklist`.
3. `ls Area_comun/mailbox/open/` y leer lo dirigido a Arquitecto.
4. Los 4 gates POR EXIT CODE SIN PIPE (`cmd > /dev/null 2>&1; echo $?`): validate,
   scan_encoding, prune_state --check, scan_domain_neutrality.
5. Armar monitores: entregas (single-shot, RE-ARMAR en cada wake), salud-execs v2
   runtime-aware, higiene mailbox, watchdog v3.1 encargo-sin-recoger.
6. Escribir/refrescar `personal/Arquitecto/.session-lease`.

## DONDE ESTA EL TRABAJO

Estado vivo completo en la memoria `.claude` (nota "TANDA 0103 EN EJECUCION"). Resumen:
DONE 0257/0267/0268/0270/0271; review_approved 0258/0269 (falta done-flip via Codex);
0272 en remediacion iter1 de 2; 0273 en review; 0259-0266 ready; gate final 0265.
PENDIENTE DEL OPERADOR: GO del build-open N=6 (respondido ADELANTABLE con evidencia).

## REGLAS OPERATIVAS APRENDIDAS EN ESTA TANDA (duras)

1. **SILENCIO DE ESCRITURA**: tras rutear un GO/ACTION, no escribir NADA (mailbox, ledger,
   higiene) hasta ver claim activo del peer o su entrega. Sus abortos por "cambio ajeno" los
   causa el coordinador escribiendo mientras ellos sondean.
2. **Pathspec por LISTA EXPLICITA** (nunca `git add -A` sobre mailbox/state) + `git commit --
   <lista>`. Todo commit post-poda incluye `Area_comun/state/*_ARCHIVE.json`.
3. **Liberar mis claims ANTES de rutear** cualquier encargo.
4. **Gates sin pipe**: `cmd | tail; echo $?` devuelve el exit del tail (me dio 3 falsos verdes).
5. **Ciclos de ledger por PASOS SEPARADOS** con verificacion del tail del log entre cada uno;
   nunca cadenas `&&` con echo.
6. **Tras timeout de submit_intent**: la tx entera rebota con "partial transaction idempotency
   state"; reenviar INTENTS INDIVIDUALES con idempotency_key FRESCO.
7. **claim_id SIEMPRE `CLAIM-` mayusculas** (submit lo acepta en minusculas, validate no).
8. **Higiene y poda solo en checkpoint coordinado** (arbol limpio, cero claims). `prune --apply`
   cuesta ~87s incluso sin nada que podar.
9. **Ante quietud**: leer el `err.log` del run del peer ANTES de asumir; su envelope explica el
   bloqueo. Si aborto por precondicion y quedo "seen": des-seen (leer seen.json con utf-8-sig,
   PowerShell le mete BOM).
10. **ASCII duro en mailbox**: parafrasear citas con acentos; scan_encoding antes de commitear.

## CANAL Y REPORTES

Reportes al Operador POR MAILBOX (no chat), con **hora local del reloj** (`date +%H:%M`) tomada
en el mismo turno. Higiene acoplada al gate de commit. Narracion minima (DECISION-0038).

## FONDO INTOCABLE

Reservadas N=6 (R0-fuentes, R2-c, R3-b, R4-b, R4-c, R5-c) intactas; config 2E35F26E; epoch
1.14.0; dataset N=500; sin encender supervised_autonomy ni real_invoker.
