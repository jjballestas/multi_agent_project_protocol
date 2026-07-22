# VERDICT - TASK-0275 (residual de cuarentena) - Analista

- Reviewer: Analista (adversarial checker)
- Fecha: 2026-07-22 17:39 hora local del sistema (UTC+2)
- Instruccion: MSG-20260722-Arquitecto-to-Analista-REVIEW-TASK-0275-cuarentena-residual
- Recomendacion de cierre: **OK-CLOSABLE (GO)** con un residual declarado (retencion es
  documental, no maquinal; crecimiento sin cota posible por diseno de la reduccion).

## Anchor canonico y reconciliacion

- Commit citado para el comportamiento: **81fe270** (impl: log quarantine recovery paths).
- HEAD canonico al revisar: **c6b1af5**.
- El runner, el harness y el README son **byte-identicos** entre 81fe270 y c6b1af5:
  - `examples/mailbox_retry_cases/run_mailbox_retry_cases.py`: sha256
    `bb150dbfd2184d05fc5f8ccfed019024d7f60613b5aa192c012fd3e3d56830a2` en ambos.
  - `scripts/harness/peer_mailbox_cron.ps1` y `scripts/harness/README.md`: diff 81fe270..c6b1af5 vacio.
- Por tanto ejecuto los gates de comportamiento contra codigo byte-identico al citado, y los
  gates de protocolo contra el estado canonico (HEAD). El anclaje es solido.
- **CLON LIMPIO** a ruta corta `D:/ccv-0275`, checkout c6b1af5. Todos los exit codes de abajo
  son del clon limpio, no del arbol caliente. SIN PRODUCTO EN ALCANCE (no hay repo de producto tocado).

## Reproduccion (exit codes en clon limpio c6b1af5)

| Gate | Comando | Exit |
|------|---------|------|
| validate | `python scripts/validate_collaboration_state.py` | 0 |
| encoding | `python scripts/scan_encoding.py` | 0 |
| neutrality | `python scripts/scan_domain_neutrality.py` | 0 |
| drift | arbol tracked del clon limpio == HEAD (sin edits gobernados sin commitear) | CLEAN |
| suite comportamiento | `python examples/mailbox_retry_cases/run_mailbox_retry_cases.py` | 0 |

## Tabla vector por vector

| # | Criterio de la instruccion | Metodo | Veredicto |
|---|----------------------------|--------|-----------|
| 1 | Log EN EXITO: ruta original + ruta de cuarentena tras cada move acierto | E2E real + lectura de harness | PASS |
| 2 | Politica de retencion declarada (cuando/quien limpia, no crece sin fin) | README + grep de auto-borrado | PASS (declarada) |
| 3 | Negativo permanente con mutacion: quitar el log de exito enrojece | 2 mutaciones independientes por comportamiento | PASS |

## Evidencia por vector

### Vector 1 - Log en exito (recuperable sin arqueologia)

- `scripts/harness/peer_mailbox_cron.ps1:745`: dentro del `foreach` de cuarentena, tras un
  `Move-Item ... -ErrorAction Stop` exitoso, emite
  `Write-Log "ROLLBACK_QUARANTINED path=$path quarantine_path=$quarantineRelative"`.
- Al estar DENTRO del bucle, **cada** fichero puesto en cuarentena deja su linea (no solo el primero).
- E2E real (`run_mailbox_retry_cases.py:938-971`): el fake-agent crea `residue.txt` (untracked
  nacido DURANTE la ventana del exec, count==2), el exec devuelve `OUTCOME: transient` (aborta),
  el rollback:
  - saca `residue.txt` de su ruta original (assert 963),
  - lo deja en `.protocol-tmp/rollback-quarantine/<id>/residue.txt` con contenido "residue" (964-967),
  - loguea `ROLLBACK_QUARANTINED path=residue.txt quarantine_path=<relative>` (968-971).
  - En paralelo, `MSG-window.md` (mailbox gobernado depositado en la ventana) NO se pone en
    cuarentena (allowlist `Test-LedgerManagedPath`), y `TASK-residue.md` junto a eventos firmados
    se preserva. Es la FAMILIA completa del criterio, no solo el ejemplo.
- Recuperabilidad robusta: aun sin el log, los ficheros estan fisicamente en
  `.protocol-tmp/rollback-quarantine/<id>/<ruta-relativa>` y se descubren con un listado; el log
  lo vuelve un one-liner. No encontre escape de perdida silenciosa en el camino de exito.

### Vector 2 - Retencion (declarada)

- `scripts/harness/README.md:149-155`: "retained for 30 days. Only the human operator or
  Arquitecto may remove an entry, during an explicit maintenance checkpoint and only after
  confirming that its contents have been recovered or are no longer needed; the peer loop never
  deletes it."
- Verifique que **ningun** camino del harness auto-borra la cuarentena:
  `grep -niE 'remove-item|rmdir|del|rd' ... | grep quarantine` => NONE.
  El unico match de `rollback-quarantine` con verbo de borrado es la frase "moved, never deleted"
  del propio README.
- `AbortedResidueMinutes` (harness:16,573,850) NO toca la cuarentena: es el cutoff de vejez del
  residuo staged en la puerta de reintento, no un GC de la cuarentena.
- Coincide exacto con la acceptance reducida ratificada (task lineas 62-64): retencion 30 dias,
  limpieza manual de operador/Arquitecto en checkpoint explicito, el loop nunca elimina
  automaticamente la cuarentena.

### Vector 3 - Negativo permanente killeado por mutacion (por comportamiento)

Dos mutaciones independientes que YO aplique al harness en el clon limpio y re-corri la suite:

- **Mutacion A** - borrar la linea del log de exito por completo:
  suite ROJA, exit 1, revienta en `run_nondestructive_rollback_contract` linea 258
  ("non-destructive rollback contract is incomplete"). El contrato estatico caza la ausencia del
  string.
- **Mutacion B** - dejar el string EXACTO presente pero guardarlo con `if ($false) { Write-Log ... }`
  para que nunca se emita en exito: el contrato estatico PASA (el string sigue en el texto), pero
  la suite igual queda ROJA, exit 1, revienta en `main` linea 969
  ("successful quarantine did not log both recovery paths"). Esto prueba que el E2E es el diente
  real de comportamiento, no una prueba por-nombre / por-presencia-de-string.
- Conclusion: la garantia esta protegida en DOS capas independientes (contrato estatico + E2E
  real). Quitar el log de exito enrojece por ambas. El negativo es permanente y esta declarado en
  el docstring `PERMANENT_NEGATIVE: ... retry-quarantine-success-log`.
- Tras cada mutacion restaure el harness pristino y confirme `git status --short` limpio (sin
  residuo de mis pruebas en el arbol).

## Residual declarado

- **R1 (aceptable, por diseno):** la retencion es **documental/gobernanza, no maquinal**. No hay
  GC automatico; la cuarentena crece sin cota hasta que un humano/Arquitecto la limpie. Esto es
  exactamente lo ratificado en el alcance reducido (el loop NO debe auto-borrar, para no
  re-introducir destruccion silenciosa). Lo dejo declarado, no es bloqueante: la unica cota
  automatica posible seria re-abrir la clase de dano que esta tarea existe para cerrar.

## Cierre

Los tres puntos que pedia la instruccion se cumplen por comportamiento sobre estado canonico y
clon limpio: (1) el rollback loguea ruta original y ruta de cuarentena EN EXITO y es recuperable
sin arqueologia; (2) hay politica de retencion declarada (30 dias, manual, loop nunca auto-borra);
(3) el negativo permanente enrojece al quitar el log, verificado con mutacion demostrada en dos
capas. Gates de protocolo verdes. Recomendacion: **GO / OK-CLOSABLE**.

-- Analista
