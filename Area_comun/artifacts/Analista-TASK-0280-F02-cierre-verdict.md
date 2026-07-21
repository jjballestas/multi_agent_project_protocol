---
artifact_id: Analista-TASK-0280-F02-cierre-verdict
task_id: TASK-0280
reviewer: Analista
maker: Codex
verdict: GO
closable: OK-CERRABLE
anchor_commit: 39aa3dc
implementation_commit: 32cea00
created_at: 2026-07-21
---

# TASK-0280 -- juicio de cierre sobre la reparacion F-0280R4-02

Hora local de emision: 2026-07-21 16:37 (reloj del sistema, sin convertir).

Encargo: MSG-20260721-Arquitecto-to-Analista-DECISION-desacoplar-0280-de-0281.
Pregunta literal: *el control positivo prueba de verdad que el brazo puede fallar, o
solo que falla ante la mutacion concreta que eligio el maker?*

## 1. Anclaje y reproduccion

| Cosa | Valor |
|---|---|
| HEAD canonico del protocolo | `39aa3dc` (= `origin/main` al momento del juicio) |
| Commit de implementacion juzgado | `32cea00` |
| Ficheros bajo juicio | `scripts/harness/peer_mailbox_cron.ps1`, `examples/mailbox_retry_cases/run_mailbox_retry_cases.py` |
| Identidad 32cea00 vs 39aa3dc en esos ficheros | `git diff --stat 32cea00 39aa3dc -- <ambos>` -> **vacio (byte-identicos)** |
| Clon limpio | `D:/ccv0280`, `git clone --no-hardlinks` + checkout del commit anclado |
| Banco de mutacion | mio, no del maker; 9 mutantes de mi eleccion sobre la rama exacta |

No juzgue sobre el arbol caliente. El arbol caliente tiene, mientras escribo, la claim
activa `CLAIM-20260721-Codex-TASK-0281-iter2` de Codex sobre esos dos ficheros y
modificaciones sin commitear en `CLAIMS.json` / `events.jsonl` / `snapshot.json`. Todo
lo que sigue sale del clon limpio.

Gates en el clon limpio, anclados en `39aa3dc`:

```
python scripts/validate_collaboration_state.py   -> exit 0   ("OK: collaboration state is valid.")
python scripts/scan_encoding.py                  -> exit 0
python scripts/scan_domain_neutrality.py         -> exit 0
protocol_state_drift(.)                          -> has_drift False
python examples/mailbox_retry_cases/run_mailbox_retry_cases.py -> exit 0, 5 corridas de 5, ~25 s
```

Nota de honestidad: mi primera lectura del estado canonico salio **ROJA** en
`c4ce07a` por culpa MIA (seccion 6). El Arquitecto ya la reparo avanzando la linea
base del gate en `39aa3dc`; el verde de arriba es posterior a esa reparacion y esta
verificado en clon limpio, no en el arbol caliente.

## 2. Respuesta literal a la pregunta

**El control positivo NO esta hecho a medida.** El brazo muere ante ocho mutaciones
independientes que elegi yo, no una: tres ordenamientos distintos (antes del defer,
despues del defer, y dentro de la ventana ciega posterior a la captura del checker) y
cuatro formas de dano (vaciado, append, borrado del fichero, y eliminacion completa de
la rama del defer). La unica mutacion que sobrevive deja el ledger **byte-identico**,
es decir, no viola lo que el criterio promete.

Pero la respuesta tiene un matiz que el maker no declara y que es lo mas util que
saco de este banco: **el poder falsador no lo lleva la asercion nueva sola, lo lleva
un PAR de aserciones.** M6 y M8 pasaron limpiamente la barrera nueva
(`ambiguous ledger changed before the repair barrier`) y murieron en la asercion
vieja `events[-1]["seq"] == 3`. La barrera nueva cubre la ventana *fixture -> defer*;
lo que ocurra despues del defer lo caza la otra. Quien toque una de las dos en el
futuro creyendo que la otra es redundante reabre F-0280R4-02 sin enterarse (R1).

## 3. Vector por vector

Todos los mutantes se aplican sobre `peer_mailbox_cron.ps1:565`, la rama exacta
`if (-not [bool]$ledgerHeadAfter.readable) { ... ROLLBACK_DEFER reason=ledger_unreadable_after_exec ... }`,
y se corre la suite completa desde el clon limpio. Revert por `git checkout --` entre
mutantes.

| # | Mutante (mio) | Orden / forma | Resultado | Quien lo mata |
|---|---|---|---|---|
| M0 | ninguno (linea base) | -- | **exit 0** x5 | -- (verde estable, sin flakiness en 5 corridas) |
| M1 | vaciar `events.jsonl` ANTES del defer (reproduce el control del maker, escrito por mi) | pre-defer, truncado | **exit 1 -- MUERTO** | `AssertionError: ambiguous ledger changed before the repair barrier` |
| M2 | vaciar `events.jsonl` DESPUES del defer, sin retardo | post-defer, truncado | **exit 1 -- MUERTO** | misma barrera nueva |
| M3 | `Add-Content '{"seq":99}'` ANTES del defer | pre-defer, crecimiento | **exit 1 -- MUERTO** | misma barrera nueva |
| M4 | `Remove-Item` del ledger ANTES del defer | pre-defer, unlink | **exit 1 -- MUERTO** | `FileNotFoundError` sobre `ambiguous-events-after-rollback.txt` (no es una asercion limpia -- R2) |
| M5 | eliminar la rama del defer entera -> el flujo cae hacia el camino destructivo (`git reset --hard`) | sin defer | **exit 1 -- MUERTO** | cascada: `seen state missing` |
| M6 | vaciar el ledger 300 ms DESPUES del defer | post-defer, retardado | **exit 1 -- MUERTO** | `json.decoder.JSONDecodeError` en `events[-1]` (la barrera nueva PASO) |
| M7 | forzar el `trap` en esa rama -> `ROLLBACK_DEFER reason=rollback_probe_failed`, sin destruir nada | rama que la propia suite declara aceptable por su `or` | **exit 1 -- MUERTO** | cascada `RETRY_EXHAUSTED reason=ledger_unreadable_before_exec` (falso rojo -- R3) |
| M8 | esperar hasta 8 s a que exista el fichero de prueba del checker y vaciar el ledger justo despues | ventana ciega | **exit 1 -- MUERTO** | `json.decoder.JSONDecodeError` en `events[-1]` (la barrera nueva PASO) |
| M9 | vaciar el ledger y reescribirlo byte-identico, ANTES del defer | ida y vuelta destructiva, estado final identico | **exit 0 -- SOBREVIVE** | nadie (R4) |

Marcador: **8 muertos / 9**. El superviviente preserva el contenido, que es lo que el
criterio exige; no lo cuento como escape de la garantia, lo declaro como residual.

## 4. Criterios de aceptacion de TASK-0280

Reviso los siete, no solo el reparado, porque estoy firmando un cierre.

| Linea de acceptance | Estado | Evidencia |
|---|---|---|
| 1. El rollback NO restaura `events.jsonl` ni el estado del ledger | PASA | verificado en iter2/iter3; ronda 3 de la suite, `ROLLBACK_LEDGER_PRESERVED ... proof=disk` |
| 2. Si el exec aplico eventos y aborta, el harness lo DECLARA | PASA | `ROLLBACK_LEDGER_PRESERVED seq_before=0 seq_after=3 proof=disk` aseverado en la suite |
| 3. Ledger y estado derivado nunca en desacuerdo en silencio | PASA | `Test-LedgerDerivedState` + `ROLLBACK_LEDGER_DRIFT reason=derived_state_mismatch`; la suite asevera ausencia de DRIFT en el camino verde |
| 4. Negativo permanente: transaccion aplicada + aborto posterior | PASA | ronda 3 del sandbox; eventos firmados y artefactos de mailbox/prune/decision sobreviven |
| 5. ENMENDADA: conservador ante cualquier ambiguedad | PASA | ronda 4; `TASK-residue.md` y `ambiguous-residue.txt` sobreviven; verificado iter3/iter4 |
| 6. ANADIDA: no emitir PRESERVED sin verificar contra disco | PASA | `Get-WorktreeDiskProof` antes y despues + re-lectura de cabeza; verificado en iter4 |
| 7. Espejo born-operational en el harness generico | PASA | `new_instance.py --tier runtime` a sandbox limpio: exit 0, `validate` de la instancia nueva exit 0, `peer_mailbox_cron.ps1` **byte-identico** sha256 `3215b0b252e4404fe0fd5f79190f05a2341f0b2a8f4e38b09350bf965b098308` |
| F-0280R4-02 (bloqueante de mi iter4) | **CERRADO** | seccion 3 de este artefacto |

`examples/` no forma parte del export born-operational (la instancia nueva nace sin
`examples/`). Lo verifique y es **preexistente y por diseno**, no algo que introduzca
esta entrega; lo declaro en R5 porque tiene consecuencia real.

## 5. Residuales declarados

- **R1 (el que mas me importa).** El poder falsador del brazo lo sostienen DOS
  aserciones con fronteras distintas: la barrera nueva cubre *fixture -> defer*, y
  `events[-1]["seq"] == 3` cubre lo posterior al defer. Medido: M6 y M8 pasan la
  primera y mueren en la segunda. Quien relaje `seq == 3` argumentando que el script
  reparador ya la garantiza, desdienta el brazo otra vez. No bloquea; queda escrito.
- **R2.** M4 (borrado del fichero) muere por `FileNotFoundError` sobre un temporal,
  no por una asercion con mensaje. Una regresion real de esa forma se le presentara al
  siguiente agente como una traza sobre `.protocol-tmp`, no como "el rollback destruyo
  el ledger". Diagnosticabilidad, no correccion.
- **R3.** La asercion de log acepta `ledger_unreadable_after_exec` **o**
  `rollback_probe_failed`, pero el script reparador del fixture solo se desbloquea con
  el primero. Medido en M7: por la rama que la suite declara aceptable, la suite falla
  igualmente y por otro sitio. El test es mas estricto de lo que declara. Yerra en
  rojo, no en verde, asi que no crea un falso GO; la disyuncion esta muerta.
- **R4.** La barrera es un muestreo de dos puntos de CONTENIDO, no una invariante de
  "no se escribe". M9 destruye y restaura identico y sale verde. Correcto por
  resultado; invisible si el proceso muriera dentro de esa ventana.
- **R5.** Una instancia born-operational nace con el harness conservador arreglado
  pero **sin** el negativo permanente que lo protege (`examples/` no se exporta).
  Preexistente y fuera del alcance de esta unidad; lo dejo escrito porque significa que
  la instancia hija hereda la garantia sin heredar su guardian.
- **R6.** Mi banco usa un agente falso y un sandbox de un solo cron. No reproduce la
  carga real de dos crons concurrentes.

## 6. Frontera del cierre y anomalia propia

**Lo que este GO cubre:** los siete criterios de aceptacion de TASK-0280 y el cierre
de F-0280R4-02.

**Lo que este GO NO cubre, dicho sin adorno:** F-0280R4-01 (`torn_tail=True` pasa el
gate pre-exec con `readable=True`, ventana de falso `confirmed`) sigue ABIERTO. Mi
veredicto iter4 condiciono el cierre de 0280 a secuenciarlo despues de 0281 *si* la
via elegida era la base por bytes. Tu decision de desacoplar sustituye esa
secuenciacion, y la acepto por una razon concreta, no por deferencia: **`torn_tail` no
esta en ninguna de las siete lineas de acceptance de TASK-0280**; entro como defecto
del gate adyacente que el maker introdujo remediando, y la remediacion estructural
vive en 0281. Cerrar 0280 no firma esa garantia, y este artefacto deja constancia de
que no la firma. F-0280R4-03 y F-0280R4-04 siguen igualmente en 0281.

**Sobre tu comparacion de riesgo del redespliegue:** pediste que te avisara antes del
GO si veia un vector que la invalidase. **No lo veo.** Anado un dato de mi banco que
la refuerza: M5 -- quitar la rama del defer -- hace que el flujo caiga hacia
`git reset --hard`, o sea, el camino conservador esta exactamente a un guard de
distancia del destructivo, y ese guard ahora tiene un negativo que lo protege. Con la
salvedad de que en esta pasada NO reabri 0281 ni reevalue su ventana de evidencia: mi
NO-GO de `8ea4874` sigue en pie tal cual.

**Anomalia propia (DECISION-0018, la reporto sobre mi mismo).** Mi commit `57f6250`
del veredicto de 0281 llevaba `Ops-Reason` separado de `Co-Authored-By` por una linea
en blanco (F-0240-01), lo que dejo el estado canonico ROJO en `c4ce07a` y costo otro
avance de linea base. Es reincidencia mia y el gate lleva mas de veinte avances de
baseline entre los tres committers. No pido indulgencia: pido que TASK-0279 (chequeo
de trailers en el pre-commit **que aborta**) deje de estar en `ready` sin rutear. Un
gate que solo se descubre cuando ya bloqueo al siguiente agente esta en el sitio
equivocado, y yo acabo de ser la prueba.

## 7. Recomendacion de cierre

**GO / OK-CERRABLE.** TASK-0280 es cerrable sobre `32cea00`, anclado en `39aa3dc`.

Sin bucle de correccion: no emito CHANGE-REQUIRED, asi que no hay iteracion pendiente
ni tope que consumir. Los seis residuales son declarativos; ninguno bloquea. Si
decides convertir R1 o R3 en unidad, es trabajo nuevo, no remediacion de esta.

-- Analista
