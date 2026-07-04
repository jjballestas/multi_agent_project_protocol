---
message_id: MSG-20260704-Arquitecto-to-Operador-FYI-medicion-real-goalp1-datos-hallazgos
from: Arquitecto
to: Operador
type: FYI
status: open
requires_response: true
response_owner: Operador
created_at: 2026-07-04
context_refs:
  - MSG-20260704-Operador-to-Arquitecto-DIRECTIVA-medicion-real-goalp1-y-adversarial-p2 (respondida)
  - personal/Arquitecto/TFM-medicion/corpus/medicion/ (journal reseteado)
  - .protocol-tmp/codex_mailbox_cron/runs/ (err.log de la sesion real de Codex)
one_line_summary: "ACCION A: journal RESETEADO (smoke archivado, journal limpio) + datos REALES de la sesion de Codex + HALLAZGOS de capturabilidad del piloto. ACCION B: adversarial-separado CONFIRMADO, lo horneo en las SPECs/GOs de P2+. Pregunta: quien cierra la fila real (tu con medir-goalp1.ps1, o la cierro yo) y como se maneja la degradacion de cubetas."
requested_action: "Confirma: (1) quien cierra la fila real de GOAL-P1 con estos datos -- tu corres medir-goalp1.ps1 (te doy los valores abajo) o me delegas el cierre y tu ratificas; (2) como se maneja el hallazgo de degradacion de cubetas (abajo) para el freeze del schema v1.0. Cuando la fila real cierre, tomo el sha256 y lo atesto via submit_intent al #4 del hub."
question: "Cierras tu la fila real de GOAL-P1 (te paso los valores) o me delegas? Y aceptas tokens_total_atribuibles como degradacion sellada (el desglose por cubeta no es capturable del runtime)?"
---

# FYI - Medicion real GOAL-P1: reset + datos reales + hallazgos del piloto

## ACCION A.1 - Journal RESETEADO (hecho)
La fila SMOKE (clave GOAL-P1: OPEN/UPDATE/CLOSE x2, tokens_dev=12000, fecha_fin=08-jul) ocupaba la clave y
estaba cerrada (append-only). La archive y deje el journal LIMPIO:
- Smoke -> `personal/Arquitecto/TFM-medicion/corpus/medicion/medicion_journal.smoke.csv` (5 lineas).
- `medicion_journal.csv` = solo header. `medicion.csv` re-materializada = 0 filas. `verificar` = journal vacio, OK.
El corpus es gitignored (como el N=500); el reset es local. Listo para abrir la fila REAL de GOAL-P1 sin colision.

## ACCION A.2 - Datos REALES de la sesion de Codex (build TASK-0247)
De los logs de la sesion real (pid exec 19032, err.log):
- **tiempo_pared:** EXEC_START 2026-07-04T02:53:43Z -> EXEC_EXIT 03:05:39Z = **~12 min (0.20 h)** el build.
  (Hubo un false-start pid 141936 auto-sanado a los 38s, no cuenta como trabajo. El done-flip fue sesion aparte
  02:53... perdon, 03:10:40->03:15:13 ~4.5 min = ledger/coordinacion, no build.)
- **sesiones_n:** 1 (build). **orchestration_mode:** mono. **reworks_n:** 0 (entrega limpia, sin NO-GO; mi
  verificacion independiente paso a la primera). **secuencia_veredictos:** APROBADO. **estado_final:** done.
  **fecha_fin:** 2026-07-04. **brazo:** baseline. **par_id:** NA. **criticidad:** fundacion. **estimate:** L.
- **checker_formal = 0** y **coordinacion_gobierno = 0** (baseline, por definicion sellada).
- **tokens (ver hallazgo):** la sesion del build reporto **~165.844 tokens** ('tokens used' en el err.log de
  codex). El done-flip reporto ~140.224 (sesion de ledger, no build).

## ACCION A.3 - HALLAZGOS DE CAPTURABILIDAD (el proposito del piloto, para el freeze del schema)
1. **El desglose por CUBETA no es capturable del runtime.** codex exec emite UN solo numero cumulativo
   ('tokens used') por sesion, en STDERR (no stdout) -- e incluye lecturas de contexto/cache, no 'tokens_dev
   limpio'. Las 4 cubetas (dev / adversarial_informal / checker_formal / coordinacion_gobierno) NO se separan
   en la fuente. Por la REGLA DE DEGRADACION EX-ANTE sellada, esto colapsa a **tokens_total_atribuibles**
   (~165.844 para el build). RECOMENDACION: sellar tokens_total_atribuibles como la moneda confirmatoria para
   el brazo baseline (el desglose fino no es viable con este runtime), y anotarlo en el schema v1.0.
2. **La captura vive en err.log (stderr), no out.log.** medir-goalp1.ps1 / el mecanismo de captura debe leer
   el err.log de la sesion. (out.log solo tiene el envelope final.)
3. **tokens_adversarial_informal NO separable en GOAL-P1:** el adversarial de 12 puntos (docs/adversarial-
   goalp1.md, verdict APPROVED) corrio DENTRO de la misma sesion de codex del maker -> sus tokens no se
   distinguen de tokens_dev. Esto REFUERZA la ACCION B: de P2 en adelante el adversarial debe ser SESION
   SEPARADA para que tokens_adversarial_informal sea taggable (y para no contaminar el brazo).
4. **tokens_cache_reads:** el numero incluye lecturas de cache; no se aisla -> NA o subsumido en el total.

## ACCION B - Adversarial-separado para P2+ (confirmado, lo horneo)
Confirmado: para P2.1/P2.2/P4.1/pares el adversarial informal de 12 puntos = AGENTE SEPARADO en contexto limpio
(dev != adversarial, nunca self-review). Lo HORNEO como campo explicito en las SPECs/GOs de esas unidades
('adversarial = sesion separada, contexto limpio') y taggeare tokens_adversarial_informal a esa sesion. GOAL-P1
quedo OK (excluido del contraste + re-verifique independiente); de P2 en adelante es la '1 adversarial' del
brazo baseline y sera sesion separada. Esto entra en las SPECs P2.1/P2.2 que preparo (cola item 4).

## Pendiente
Cuando confirmes quien cierra la fila real (con tokens_total_atribuibles) y la degradacion, tomo el sha256 del
journal y lo atesto via submit_intent al #4 del hub (corpus del sello). Sin eso, no cierro la fila (para no
pre-sellar la decision de degradacion que es tuya en el freeze).
