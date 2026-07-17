---
message_id: MSG-20260714-Arquitecto-to-Operador-RESP-secuencia-probe-memoria-hibrida
from: Arquitecto
to: Operador
type: RESP
status: archived
requires_response: false
created_at: 2026-07-14
context_refs:
  - Area_comun/mailbox/answered/MSG-20260714-Operador-to-Arquitecto-DIRECTIVA-coordina-probe-memoria-hibrida.md
  - Area_comun/specs/SPEC-MEMORIA-HIBRIDA.md
  - Area_comun/decisions/DECISION-0081-ruta-unica-memoria-hibrida-engram-cerrado.md
  - Area_comun/decisions/DECISION-0096-instancias-born-operational-capa-operacional-export.md
one_line_summary: "CONFIRMO secuencia y scope aislado del Gate-1, con 4 precisiones; secuencia concreta Gate-1 -> nacer Nova-Payroll born-operational -> PREP slice -> Fase A probe con go/no-go por DEMOSTRACION; pido 3 inputs para ejecutar"
---

# RESP - Secuencia del probe de memoria hibrida (coordinada con SPEC-MEMORIA-HIBRIDA v0.2.0)

CONFIRMO la secuencia y el scope AISLADO del Gate-1. El marco coordina 1:1 con la SPEC
(commit 9376bb4): su s.1 ya preveia "build post-ventana O EN INSTANCIA con GO del operador";
el probe ES esa via de instancia. Cuatro precisiones y la secuencia concreta:

## Precisiones (afinan el marco, no lo contradicen)

1. **Cadena de decisiones:** DECISION-0081 YA supersedio a DECISION-0071 (ruta unica). Gate-1
   NO re-supersede: ACTIVA la implementacion que el REQ s.0.4 gateaba
   (implementation_allowed_before_decision:false), con scope de instancia + firewall. Se
   registra como DECISION nueva del hub (capa estudio/metodologia) citando 0081.
2. **El "OFF en hub/medidas" es ESTRUCTURAL, no un flag:** no existe un flag global de memoria
   que scopear. La memoria = scripts + DB local DE LA INSTANCIA; el hub y las instancias
   medidas simplemente NO corren el indexador ni reciben cableado de memoria en sus gates
   (la SPEC I5/s.9 ya lo exige). Gate-1 lo declara y PROHIBE expresamente el cableado en
   hub/medidas durante la ventana + pre-declara el firewall anti-HARKing (nada del probe es
   citable). Cero riesgo al config pineado (2E35F26E intacto; la DECISION vive fuera, patron
   0095/0096).
3. **Un solo DDL master:** el probe implementa el master del hub (SPEC s.3) via el export
   born-operational (DECISION-0096), absorbiendo el port/supersede del memdb ya merged en
   Zeus-protocol-Aegis (hallazgo M6 de la review adversarial). Sin esto naceria un TERCER
   esquema divergente.
4. **Subordinacion operativa:** Gate-1 + nacimiento de la instancia son papel + ceremonia mia
   (no compiten con E2). La Fase A (build+probe) SI compite si la corre el mismo trio/maquina:
   propongo arrancarla tras el sello E2 salvo ventana ociosa, con el freno "Contabilidad gana"
   escrito en el GO de la fase.

## Secuencia concreta propuesta

1. **Gate-1 (hub):** redacto la DECISION de activacion scopeada (autoriza implementar REQ/SPEC
   SOLO en Nova-Payroll; prohibe cableado en hub/medidas durante la ventana; firewall
   anti-HARKing; freno "Contabilidad gana") -> tu firma -> submit_intent decision.
2. **Nacer Nova-Payroll born-operational:** new_instance.py --tier attested (nace con harness
   + skills por DECISION-0096) -> repo propio + Aegis/ + trio propio + genesis fresco;
   cross-atestacion de nacimiento anclada en el hub (patron Entrada 0 de NOVA). El guardrail
   PII de nomina (datos JAMAS al store de memoria; se mide el PROCESO) entra al AGENTS/config
   de la instancia DESDE el nacimiento.
3. **PREP del slice (analogo kit SPEC-CONT):** diseno del nucleo de liquidacion (empleados/
   contratos/conceptos + cabecera 002t / detalle 007t / bases 028t + FindBaseTra + 1
   porcentaje-concepto + 1 consecutivo + 1 control de periodo + 1 reporte RO) desde el legacy
   VB6. Puedo dar el ESQUELETO del kit como PREP del hub si lo pides; la instanciacion es de
   su trio.
4. **Fase A build + probe (en Nova-Payroll, SU ledger):** implementa de la SPEC: F1 (indexador
   read-only + round-trip AC5 + check de drift) + s.5.5 revive_pack (+ F2 minimo si el probe
   lo pide). **Go/no-go por DEMOSTRACION (no estadistica):** (a) round-trip verde; (b) drift 0;
   (c) cold-start recall util (observacion cualitativa); (d) REVIVE demostrable: un peon/agente
   muere -> revive SOLO con su pack -> continua una tarea real del slice correctamente, con el
   pack ATESTADO (procedencia firmada, identidad derivada del chokepoint SPEC I6). Ese (d) es
   exactamente el angulo que Engram no tiene (REVIVE atestado + round-trip integro + procedencia
   firmada).
5. **Tu decision de adopcion** con los indicios. 6. **Post-30 solo con indicios positivos:**
   fase rigurosa; el pre-registro lo redacta el Asesor (confirmado: yo no).

## Para ejecutar necesito (3 inputs)

1. GO para redactar Gate-1 (te entrego el draft de DECISION para tu firma).
2. Nombre/ubicacion del repo: propongo `D:/Agentes/NOVA-Suite/Nova-Payroll` con repo GitHub
   propio (hermano de NOVA, paraguas NOVA-Suite).
3. Roster del trio de Nova-Payroll (mismo patron Arquitecto/Codex/Analista + jball? entra
   Julian como firmante desde el nacimiento o despues?).

-- Arquitecto (hub). Los encargos E2 de NOVA (BR-C4 <=29-jul, corpus <=25-jul) conservan
   prioridad de cola sobre el probe, como ordena la DIRECTIVA.
