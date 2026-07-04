---
message_id: MSG-20260704-Operador-to-Arquitecto-FYI-estimates-q4-locked
from: Operador
to: Arquitecto
type: FYI
status: archived
requires_response: true
response_owner: Arquitecto
created_at: 2026-07-04
context_refs:
  - personal/operador/vision-nova/ESTIMATES-Q4-para-sorteo.md (estimates, coinciden exacto)
  - NOVA_ESTUDIO_Particion_Baseline_vs_Gobernado.md s.3 (sorteo con ancla externa: pre-commit estimates+par_ids+algoritmo+T ANTES de la semilla NIST)
one_line_summary: "El Operador CONFIRMO y LOCKEO los estimates del pool Q4 (2026-07-04), coinciden EXACTO con ESTIMATES-Q4-para-sorteo.md: 6 M + 4 S. Son ANTI-HARKing (congelados antes del sorteo). Metelos en el PRE-COMMIT ATESTADO del sorteo (par_ids + estimates + algoritmo + timestamp T) ANTES de la semilla NIST; alimentan la asignacion ligero/completo ESTRATIFICADA (estrato M=6 diversas, estrato S=4 cluster Get_*_List). Esto CIERRA el input de estimates del sello. Pendiente del operador que queda: sandbox de mutadores (<=14-jul, gatea P4.x)."
requested_action: "El Operador CONFIRMA y LOCKEA los estimates S/M/L del pool Q4 (coinciden exacto con ESTIMATES-Q4-para-sorteo.md, declarados 2026-07-03): (1) P4-004 Apply_Obligation_Adjustment = M; (2) P3-002 Availability Draft/CDP = M; (3) P3-003 Commitment Draft/RP = M; (4) P3-004 Obligation Draft = M; (5) P2-003 UI exploracion shell = M; (6) P6-003 OpenTelemetry/Observabilidad = M; (7) Get_Availability_Certificate_List = S; (8) Get_Commitment_List = S; (9) Get_Obligation_List = S; (10) Get_Payment_List = S. Total 6 M + 4 S. ACCION: metelos en el PRE-COMMIT ATESTADO del sorteo (Particion s.3: par_ids + estimates + algoritmo + timestamp T commiteados y atestados ANTES de que la semilla = primer pulso del NIST Beacon posterior a T). Son ANTI-HARKing: quedan CONGELADOS al commitear, no se tocan despues. Alimentan la asignacion ligero/completo ESTRATIFICADA por familia/tamano: estrato M = 6 (P4-004, P3-002/003/004, P2-003, P6-003, las diversas); estrato S = 4 (los Get_*_List, el cluster casi-isomorfo, n efectivo < 10, en su propio estrato). Esto CIERRA el input de estimates para el sello (uno de los dos pendientes del operador). RESPONDE con: confirmacion de que los estimates quedan en el pre-commit del sorteo (o van al SELLO draft como el artefacto a atestar el dia del sello, antes de la semilla). RECORDATORIO: el otro pendiente del operador es el SANDBOX DE MUTADORES (<=14-jul, backup+GRANT EXECUTE o wrapper TRAN/ROLLBACK) que gatea P4.x."
question: ""
---

# FYI - Estimates del pool Q4 CONFIRMADOS y LOCKED (para el pre-commit del sorteo)

El Operador confirma y lockea los estimates S/M/L del pool Q4 (coinciden exacto con
ESTIMATES-Q4-para-sorteo.md): **6 M + 4 S.**

- **M (6):** P4-004, P3-002, P3-003, P3-004, P2-003, P6-003.
- **S (4):** Get_Availability_Certificate_List, Get_Commitment_List, Get_Obligation_List, Get_Payment_List.

**Accion:** metelos en el PRE-COMMIT ATESTADO del sorteo (par_ids + estimates + algoritmo + timestamp T),
**ANTES** de la semilla NIST (Particion s.3). Son ANTI-HARKing -> congelados al commitear. Alimentan la
asignacion ligero/completo ESTRATIFICADA: estrato M=6 (diversas), estrato S=4 (cluster Get_*_List).

Esto CIERRA el input de estimates del sello. **Pendiente del operador que queda: sandbox de mutadores (<=14-jul).**
