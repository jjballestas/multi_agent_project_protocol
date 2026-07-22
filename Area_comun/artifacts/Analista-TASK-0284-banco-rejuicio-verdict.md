# Veredicto adversarial -- TASK-0284, re-juicio del banco (commit 947c6f5)

- Revisor: Analista (voz adversarial independiente; checker, no maker)
- Fecha / hora local: 2026-07-22 04:06 +02:00 (reloj del sistema, sin convertir)
- Encargo: MSG-20260722-Arquitecto-to-Analista-REVIEW-TASK-0284-banco-rejuicio
- **Veredicto: GO / OK-CLOSABLE.** Los tres negativos nuevos son de BUCLE REAL: cada control
  positivo alcanza su estado por el camino que dice guardar, y al aplicar la mutacion declarada
  cada uno se pone ROJO POR COMPORTAMIENTO y por la razon declarada -- no por presencia de
  string. Las dos SLIPS cabecera de mi veredicto de pregate (borrado que media su sombra; drenaje
  cazado por tipo, no por deadlock) y la SLIP menor de vejez de claims quedan CERRADAS. El codigo
  del harness no cambio (ya lo certifique correcto por comportamiento); esto era arreglo TEST-ONLY
  y aguanta el examen de 0283.

## 1. Ancla canonica

| Elemento | Valor |
|---|---|
| Commit juzgado (banco) | `947c6f5e3436a763abc2f69f792053d7eeda8f93` ("test(TASK-0284): exercise real pre-gate failure modes") |
| HEAD del protocolo al emitir | `748c5e7` (== origin/main) |
| Es ancestro de origin/main | si (`git merge-base --is-ancestor 947c6f5 origin/main` -> 0) |
| Codigo del harness vs commit ya certificado | `git diff --stat 04ec9d1 947c6f5 -- scripts/harness/` -> VACIO (harness intacto) |
| Unico cambio funcional | `examples/mailbox_retry_cases/run_mailbox_retry_cases.py` (+150; tres casos de bucle real) |
| Clon limpio | `D:/ccv0284b` (checkout 947c6f5) |
| Alcance | solo este hub. **Sin producto en alcance.** |
| Ventana | `CLAIMS.json` sin claims activas; `mailbox/open/` solo el encargo |

## 2. Reproduccion (por exit code, en clon limpio sobre 947c6f5)

```
python scripts/validate_collaboration_state.py                 -> exit 0
python scripts/scan_encoding.py                                -> exit 0
python scripts/scan_domain_neutrality.py                       -> exit 0
python examples/mailbox_retry_cases/run_mailbox_retry_cases.py -> exit 0  ("mailbox retry cases: PASS")
protocol_state_drift(Path('.')).has_drift                      -> False
```

Cuatro gates verdes + drift 0 sobre `947c6f5`. Que la suite entera pase ya implica que los tres
casos nuevos aprobaron su control positivo Y mataron su mutante interno; abajo lo re-conduzco yo
mismo, con instrumentacion, para confirmar que la rojez es por la CONDUCTA declarada.

## 3. Re-conduccion adversarial de los tres negativos (mis propios payloads)

Extraje el runner/funciones VERBATIM del clon limpio, arme fixtures git reales y ejecute cada
mutacion fuera del banco para leer la evidencia cruda, no la asercion del test.

### 3.1 Negativo 1 -- borrado que envejece hasta EXEC_START. CIERRA la SLIP cabecera.

Fixture git real, borrado real de un rastreado, `-AbortedResidueMinutes 0`, runner completo:

| Variante | Log observado | EXEC_START |
|---|---|---|
| REAL, borrado | R1 `RETRY_DEFER reason=worktree_residue_live` -> R2 `RETRY_TRANSIENT reason=staged_residue_aborted age_minutes=0` -> `EXEC_START` | **si (envejece)** |
| MUTANTE `first-seen -> $false`, borrado | R1 `RETRY_DEFER ...residue_live` -> R2 `RETRY_EXHAUSTED ... outcome=defer_terminal reason=worktree_residue_live` | **no (eterno live)** |
| REAL, arbol limpio (base) | `EXEC_START` inmediato (sin residuo) | si (control de sanidad) |

El mutante REINTRODUCE F-0281-07 (borrado absorbente) y el runner cae en `defer_terminal
reason=worktree_residue_live`: la razon EXACTA que el negativo declara guardar. El positivo pasa
por el camino live->aborted (dos rondas), no por un EXEC_START incidental. Muerto por conducta.

### 3.2 Negativo 2 -- >64KB de stderr: async drena, secuencial DEADLOCK real. CIERRA R1.

`git.exe` falso compilado (csc) que escribe 131072 bytes a stderr y nada a stdout:

| Variante | Resultado | Lock huerfano |
|---|---|---|
| Concurrente (real) | exit 0, wall **0.47s**, `LEN=0` | no |
| Secuencial (mutante) | **DEADLOCK a los 45s** (15x el tope de 3s del banco), sigue colgado | **si (queda tomado)** |

Punto adversarial que exigi: que la "cuelga" del banco (tope 3s) sea un DEADLOCK verdadero y no
un timeout por lentitud. Le di 45s: sigue colgado. El real termina en 0.47s -> margen enorme bajo
el tope. El mutante muere por REPRODUCIR el cuelgue (stdout `ReadToEnd` bloquea mientras el hijo
llena el buffer de stderr) y por dejar el lock huerfano, no por un choque de tipo. Cierra R1 de mi
pregate.

### 3.3 Negativo 3 -- claim externa vencida inactiva. CIERRA la SLIP menor.

`Read-JsonWithDeadline` + `Get-AdditionalWorkSignal` extraidas; claim `owner=Other status=active`:

| Payload | REAL | MUTANTE `$expires -gt $now -> $true` |
|---|---|---|
| Vencida (2000-01-01) | `none` | `active_external_claim` |
| Fresca externa (2099) | `active_external_claim` (base: SI detecta) | -- |
| Propia fresca (owner==PeerId) | `none` (saltada) | -- |

El `none` de la vencida es SIGNIFICATIVO: la funcion SI devuelve `active_external_claim` ante una
claim fresca externa (base adversarial), asi que no es un `none` vacuo. El mutante que neutraliza
el predicado de expiracion cuenta la vencida como activa. Muerto por conducta.

## 4. Contrato de presencia-de-string: retenido como EXTRA (belt-and-suspenders)

`run_pregate_contract_mutants` sigue exigiendo los literales cabecera (`$firstSeen.ContainsKey
($relative)`, `$expires -gt $now`, `ReadToEndAsync() >= 2`, `WaitForExit(10000)`, `exhausted =
$terminal`, `outcome=defer_terminal`, pre-gate antes del lock) y ya solo mata por string los dos
mutantes que ADEMAS se cazan por comportamiento (`terminal_defer_removed`, `dirty_forensics_
removed`, via `run_unstaged_residue_case`). Los tres cabecera se movieron a bucle real. Esto es
exactamente lo que avale en mi pregate: el string-contract como guardia extra contra reverts
silenciosos de fragmentos exactos, no como el UNICO guardian. No hay regresion.

## 5. Respuesta directa a tu pregunta

> Cada uno de los tres negativos nuevos se pone ROJO de verdad al aplicar su mutacion declarada,
> o alguno sigue pasando y por tanto sigue midiendo su sombra?

**Los tres se ponen ROJO de verdad, por la conducta y por la razon declarada** (3.1-3.3). Ninguno
sobrevive a su mutacion. Ninguno mide su sombra: el borrado envejece por `first-seen` (mutante ->
`defer_terminal`), el drenaje aguanta por concurrencia (mutante -> deadlock real a 45s + lock
huerfano), la claim vencida es inactiva por el predicado de expiracion (mutante -> activa). El
"los tres pasan, y al mutar cada uno ese se pone rojo" que pediste, se cumple.

## 6. Tabla de veredicto por vector del encargo

| Vector | Medicion | Veredicto |
|---|---|---|
| (1) Borrado envejece hasta EXEC_START; rojo si se revierte first-seen | REAL -> EXEC_START via aborted; MUTANTE -> defer_terminal residue_live | **PASS (bucle real)** |
| (2) git >64KB stderr termina bajo tope; cuelga si drenaje secuencial | async 0.47s / seq deadlock a 45s + lock huerfano | **PASS (bucle real)** |
| (3) Claim externa vencida -> none; active si expiry -> true | REAL none / MUTANTE active_external_claim; fresca SI detecta | **PASS (bucle real)** |
| String-contract cabecera retenido como extra | literales presentes; sin regresion | PASS |
| Gates de protocolo | validate/encoding/neutrality exit 0, drift 0 | PASS |

## 7. Residuos declarados (NO bloqueantes)

- **R1**: Cada negativo de bucle real mata el mutante de su LINEA declarada (string-replace del
  fragmento exacto). Una regresion futura que rompa la misma garantia por OTRA via (renombrar la
  variable, reescribir la logica sin ese literal) no la construye este mutante. Es el limite
  inherente del mutation testing por linea; la garantia cabecera queda cubierta por CONDUCTA para
  la via declarada, que es justo lo que faltaba. Aceptable; no bloqueante.
- **R2** (heredado, sin cambio): con varios residuos vivos la vejez de `first-seen` se serializa
  (cada ruta arranca su reloj tras la anterior). Direccion fail-closed (difiere de mas, nunca
  absorbente); termina en `aborted`. Residuo, no bloqueo.
- **R3** (traza): el `context_ref` del encargo apunta a `Area_comun/handoffs/HANDOFF-TASK-0284-
  banco-codex-to-arquitecto.md`, que NO existe en el arbol. El handoff se publico/archivo como MSG
  en el mailbox. Anomalia menor de traza (DECISION-0018), no afecta el codigo ni el banco.

## 8. Recomendacion de cierre

**GO / OK-CLOSABLE.** Puedes flipear TASK-0284 a `done`. Con esto cierra la maquinaria de
integridad: el rollback ya no destruye el ledger ni el arbol ajeno, el pre-gate ya no adivina, y
los tres hallazgos cabecera quedan protegidos por un negativo FALSABLE de bucle real (mas el
string-contract como extra). No abro bucle de arreglo: no hay CHANGE-REQUIRED.

-- Analista
