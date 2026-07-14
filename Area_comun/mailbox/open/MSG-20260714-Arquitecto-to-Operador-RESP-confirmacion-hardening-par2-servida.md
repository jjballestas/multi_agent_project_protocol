---
message_id: MSG-20260714-Arquitecto-to-Operador-RESP-confirmacion-hardening-par2-servida
from: Arquitecto
to: Operador
type: RESP
status: open
requires_response: true
response_owner: Operador
created_at: 2026-07-14
context_refs:
  - Area_comun/mailbox/answered/MSG-20260714-Operador-to-Arquitecto-DIRECTIVA-confirmacion-hardening-15jul-par2.md
  - "personal/operador/vision-nova/SELLO-ETAPA-1-nova-budget-DRAFT.md (enmienda s.29 DRAFT PARA FIRMA)"
  - Area_comun/artifacts/DRAFT-SELLO-ETAPA2-estructura-arquitecto.md (s.6 (b) precisada)
one_line_summary: "4 entregables de la DIRECTIVA hardening-15jul: (a) enmienda s.29 DRAFT PARA FIRMA (checkpoint cumplido en plazo, clase de evidencia declarada honesta); (b) cableado real: CDP-annul SI con tests, Annul_Commitment NO cableado (esfuerzo M); (c) verificacion independiente de la entrega PAR-2 = NO EXISTE (solo auto-verificacion del entregador; el guard si esta cubierto por TASK-9392); (d) decision PAR-2 dentro/fuera SERVIDA con costos. Hallazgo: TASK-0254 no es tarea gobernada y a2333dc es solo-docs; inconsistencia 36-vs-30 casos senalada."
requested_action: "Decide: (1) FIRMA de la enmienda s.29 (registra el checkpoint con la evidencia declarada); (2) PAR-2 DENTRO o FUERA del pool Q4 (recomendacion abajo; n=10 no depende de esto). Si eliges DENTRO, ademas decide si ordenas la re-verificacion gobernada (patron TASK-9392) del hardening."
question: "Firmas s.29, y PAR-2 dentro o fuera del pool?"
---

# RESP - Confirmacion gobernada del hardening 15-jul (PAR-2 / Annul_*)

Investigacion read-only sobre NOVA (dos-trios): commit a2333dc, TASK_INDEX, mailbox de la
instancia, y grep completo del codigo de producto. Hora local 20:35.

## (a) Enmienda fechada -> s.29 DRAFT PARA FIRMA
En el doc vivo del sello E1 (patron s.27/s.28). Registra: checkpoint hardening-15-jul CUMPLIDO EN
PLAZO (procs entregados adelantado el 14-jul) con la clase de evidencia DECLARADA: el guard
Assert_Permission sobre los 3 Annul_* tiene verificacion independiente firmada (TASK-9392); la
entrega PAR-2 como tal, NO (ver (c)). No surte efecto de pool: eso es tu decision (d).

## (b) Estado REAL del cableado C#
- `Annul_Availability_Certificate` (CDP-annul): **SI, cableado y verificado.** Vertical completa:
  endpoints annul-preview/annul (NOVA.Api/Program.cs:268,288, THROWs 50281-50287 a ProblemDetails),
  Application + gateway SQL + Contracts + DI + UI (App.tsx), tests unit
  (AvailabilityCertificateAnnulmentServiceTests) + integracion (AnnulAvailabilityCertificateEvidenceTests).
- `Annul_Commitment` (RP-annul): **NO cableado.** Cero referencias en src/ y apps/. Solo proc de
  sandbox. Que falta (regla 8: solo superficie sobre el proc existente): replicar la vertical de
  CDP-annul (endpoint preview+annul, application, gateway, contracts, DI, UI, tests unit+integracion
  + harness F-NOVA-01) con re-confirmacion de SUS THROWs reales contra OBJECT_DEFINITION.
  **Esfuerzo: M** (patron ya existe como plantilla; no es S porque exige mapeo de THROWs propio +
  tests + harness con SQL real; no es L porque no hay diseno nuevo).
- `Annul_Obligation` (OBL-annul): NO cableado (mismo estado que RP-annul; fuera de lo preguntado
  pero lo dejo registrado).

## (c) Verificacion independiente firmada de la entrega PAR-2: NO EXISTE hoy
- Lo que hay: commit `a2333dc` ("TASK-0254/P4.2") = SOLO DOCUMENTACION (+28 lineas en
  docs/budget-parity-harness.md; cero .cs/.sql/tests) + FYI del Arquitecto de NOVA cuya verificacion
  en vivo la hizo EL PROPIO entregador. **TASK-0254 NO existe como tarea gobernada** (sin fila en el
  TASK_INDEX de NOVA, sin DoD, sin checker). No alcanza el estandar TASK-9392.
- Matiz honesto: la pieza de SEGURIDAD (guard Assert_Permission en los 3 Annul_*) SI tiene tercero
  firmado via TASK-9392 (checker analista:v1, smoke 30/0 + control negativo). Lo NO cubierto por
  tercero: la paridad PAR-2 como entrega propia y el estado de cableado C#.
- Que haria falta para el estandar: registrar tarea gobernada en NOVA (su Arquitecto la registra;
  yo doy el PROMPT, dos-trios), maker re-emite la evidencia PAR-2 (preflight de paridad + smoke) y
  checker one-shot en clon limpio la re-verifica y firma (patron exacto TASK-9392). Estimo 1 ciclo
  corto de su trio.
- **Anomalia menor senalada (DECISION-0018, para el Arquitecto de NOVA):** los docs de a2333dc
  citan un smoke de 36 casos; el unico smoke con firma de tercero (TASK-9392) reporta cases=30.
  Hasta reconciliar, el numero citable es 30.

## (d) Decision PAR-2: DENTRO vs FUERA del pool Q4 (tuya; n=10 ya confirmado SIN PAR-2)
- **FUERA (costo ~0):** la enmienda s.29 registra "entregado, fuera del contraste" y listo. El
  estudio sigue con n=10 tal como esta sellado. RP/OBL-annul se pueden cablear DESPUES fuera del
  contraste, cuando convenga al producto. Riesgo: ninguno para el estudio.
- **DENTRO (aditivo, costo real):** exige ANTES del sello E2 (29-jul): (1) re-verificacion gobernada
  firmada del hardening (ciclo trio NOVA, patron TASK-9392); (2) enmienda de pool fechada que anade
  la(s) unidad(es) Annul al pool con su tarea_id (el sorteo sellado les asigna brazo por hash, sin
  re-sorteo); el BUILD del cableado (esfuerzo M) ocurre POST-30-jul dentro de la ventana medida --
  cablearlo antes contaminaria el contraste. Beneficio: pool crece (n=10 -> n=11+). Riesgos: teething
  de una unidad estrenando patron annul en el brazo que le toque + trabajo de verificacion extra en
  la semana del sello.
- Dato para decidir: PAR-2 es opcional y no esta en la ruta critica; la ruta critica sigue siendo
  la reconciliacion 26-29.

NO incorpore PAR-2 al pool ni cablee nada (frontera respetada). s.6(b) del draft E2 quedo
PRECISADA con este cuadro (la version anterior sobrevendia "verificado en vivo" sin decir que era
maker-side).
