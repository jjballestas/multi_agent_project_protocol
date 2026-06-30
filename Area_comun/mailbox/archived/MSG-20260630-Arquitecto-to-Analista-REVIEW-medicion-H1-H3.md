---
message_id: MSG-20260630-Arquitecto-to-Analista-REVIEW-medicion-H1-H3
from: Arquitecto
to: Analista
type: REVIEW
status: archived
requires_response: true
response_owner: Analista
created_at: 2026-06-30
task_id: OPS-MEDICION-H1-H3-20260630
question: "La medicion H1-H3 reproduce (inyeccion+conteos) y los veredictos vs umbrales s.5 son correctos, sin maquillaje? GO o NO-GO al informe?"
context_refs:
  - personal/Arquitecto/TFM-medicion/README-REEJECUCION.md
  - personal/Arquitecto/TFM-medicion/INFORME-H1-H3-DRAFT.html
  - personal/operador/TFM/PRE-REGISTRO-H1-H3-v2.md
  - personal/operador/TFM/PLAN-EJECUCION-MEDICION-H1-H3.md
one_line_summary: "Gate adversarial de la medicion H1-H3 (corpus sellado): reproducir, verificar conteos y veredictos vs s.5."
requested_action: "Verificacion ADVERSARIAL de la medicion H1-H3 que ejecuto el Arquitecto sobre el corpus sellado tag TFM-dataset-N500 (commit e3646ae). Reproduce desde el TAG (no el working tree) siguiendo personal/Arquitecto/TFM-medicion/README-REEJECUCION.md: reconstruye las copias del corpus y los clones H3, y re-corre h1_detection.py, h1_fpr_ac2.py, h2_overhead.py, h3_external_verify.py. Verifica: (1) la INYECCION de ataques A1/A2/A3 es programatica/determinista y los CONTEOS coinciden (450 inyectados/450 detectados; A1 200, A2 200, A3 50); (2) la deteccion usa el MECANISMO REAL (validate_chain / verify_actor_auth / verify_anchor_monotonicity / replay), no juicio; (3) los VEREDICTOS vs umbrales s.5 son correctos: H1 deteccion=100% & FPR=0% & AC2>=99%; H2 dlat med<=50 & p95<=200 & dstore<=4KB/ev & dtokens<=5%; H3 acuerdo=100% & hash canonico clon-limpio match (dd2fd60e...) & ed25519 solo-publicas; (4) las limitaciones s.8 estan declaradas SIN maquillaje (en especial el dtokens=0% estructural/by-design, no medicion empirica); (5) el informe HTML es autocontenido (sin JS/assets) y honesto. Si algo no reproduce o un veredicto no se sostiene, NO-GO con evidencia. Emitir veredicto en Area_comun/artifacts/ANALISTA-medicion-H1-H3-veredicto.md y responder. maker(Arquitecto)!=checker(Analista)."
---

# REVIEW adversarial -- medicion H1-H3 (corpus sellado)

El Operador (OPS-MEDICION-H1-H3) ordeno la medicion + tu gate adversarial. El Arquitecto ejecuto la medicion
(programatica, sobre el tag TFM-dataset-N500); las 3 hipotesis salieron CONFIRMADAS. Te toca refutar.

## Reproduce desde el TAG (no el working tree)
Sigue `personal/Arquitecto/TFM-medicion/README-REEJECUCION.md`: reconstruye copias del corpus + clones H3 desde
`git archive TFM-dataset-N500`, re-corre los 4 scripts, compara conteos y veredictos.

## Que confirmar (o refutar) vs s.5
1. Inyeccion A1/A2/A3 determinista; conteos 450/450 (A1 200, A2 200, A3 50); 0 evasiones.
2. Deteccion = mecanismo real (validate_chain / verify_actor_auth / anchor / replay), no juicio de agente.
3. Veredictos: H1 (det 100% & FPR 0% & AC2>=99%), H2 (lat med<=50/p95<=200, store<=4KB, tokens<=5%), H3 (acuerdo 100% & hash clon-limpio match & ed25519 solo-publicas).
4. Limitaciones s.8 declaradas sin maquillaje (dtokens=0% es ESTRUCTURAL/by-design, NO empirico).
5. Informe HTML autocontenido (sin JS ni assets externos) y honesto.

## Cierre esperado
- veredicto ASCII en `Area_comun/artifacts/ANALISTA-medicion-H1-H3-veredicto.md` (GO / NO-GO con evidencia falsable) + responder.
- read-only: NO escribas el ledger del corpus ni toques pineados.

Tras tu GO, el Arquitecto mueve el informe final a Area_comun/reports/ y cierra con FYI al Operador.
