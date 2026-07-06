---
message_id: MSG-20260706-Arquitecto-to-Operador-LOTE2-PENDIENTE-onboarding-remoto-dba-identidad-anchor
from: Arquitecto
to: Operador
type: HANDOFF
status: open
requires_response: true
response_owner: Operador
created_at: 2026-07-06
context_refs:
  - "D:/Agentes/Zeus/NOVA/Aegis/Area_comun/protocol/RUNBOOK-onboarding-multi-clon-aegis.md"
  - Area_comun/mailbox/open/MSG-20260706-Operador-to-Arquitecto-ACTION-onboarding-remoto-checklist-huecos.md
  - Area_comun/artifacts/NOTA-DISENO-peones-vs-tokens-sello-etapa2.md
one_line_summary: "Onboarding remoto integrado: huecos 2/3/4 cerrados en el runbook (s.8), hueco 6 anadido al diseno del sello (s.4b). LOTE2-PENDIENTE-OPERADOR = 3 decisiones/encargos tuyos: (5) encargo DBA acceso BD remoto (camino critico, mayor lead time); + 2 requisitos enforce+authoritative que el checklist no listaba: identidad-nueva-firmante toca el config pineado (re-genesis), y el anchor apunta a un path local tuyo."
requested_action: "Drenar el LOTE2 cuando entres: (5) dar el encargo DBA de acceso BD remoto (opciones abajo); (A) decidir identidad del empleado (bajo identidad existente = sin re-genesis, vs propia = re-genesis coordinado); (B) decidir el anchoring del clon remoto (solo clon canonico vs remoto compartido). Nada frena la cola."
question: "(5) VPN al sandbox actual o copia sanitizada restaurada local con grants patron budget_sandbox_verifier? (A) el empleado opera bajo Codex/Analista (sin re-genesis) o estrena identidad propia (re-genesis)? (B) el anchor lo corre solo el clon canonico, o migras remote_url a un remoto compartido?"
---

# LOTE2-PENDIENTE-OPERADOR - Onboarding remoto (17:05 local, 2026-07-06)

## Integrado a la cola SIN frenarla (mi parte, hecha)
- **Huecos 2/3/4 (runbook, mios):** cerrados en `RUNBOOK-onboarding-multi-clon-aegis.md` s.8
  (alta del participante + llaves en su maquina; capabilities y reparto maker!=checker
  separado fisicamente; disciplina distribuida CON el requisito enforce+authoritative:
  runtime Python + smoke submit_intent en su maquina, gate e2e entre los DOS clones reales
  antes de la primera tarea de Contabilidad, huso UTC-5 vs mis reportes UTC+2).
- **Hueco 6 (sello, mio):** requisito de pre-registro de participantes/maquinas/roles anadido
  a la nota de diseno del sello Etapa 2 (s.4b): la composicion del equipo se nombra ANTES de
  sellar (un segundo humano es variable del estudio).
- **Hueco 1 (tuyo, tramite corto):** el origin de Aegis ya apunta a tu repo GitHub; falta
  confirmar visibilidad privada + invitar al empleado. Nada que hacer de mi lado.

## LOTE2 - lo que espera tu mano (3 items; el 5 es camino critico)

### (5) Encargo DBA - acceso BD sandbox remoto (MAYOR LEAD TIME del checklist)
Nada preparado (ni VPN, ni copia, ni grants remotos, ni sanitizacion). Las pruebas de paridad
de Contabilidad lo necesitaran. Opciones para el DBA:
- VPN al sandbox actual (DbsFinanciero_SANDBOX) con login verificador remoto patron
  budget_sandbox_verifier (grants minimos EXECUTE/SELECT/VIEW DEFINITION), o
- copia sanitizada del sandbox restaurada LOCAL en la maquina del empleado con esos grants.
- **Nota de confidencialidad (dura):** datos de entidades publicas colombianas -> si van a
  maquina ajena, copia SANITIZADA (sin PII real), nunca el sandbox con datos reales.
Registralo con su lead time; es infraestructura fuera del protocolo -> arrancar YA.

### (A) Identidad del empleado firmante (bifurcacion enforce+authoritative, NO listada)
Con `actor_auth_enforce:true`, un evento firmado por una identidad cuya pubkey ed25519 no esta
en `signature_config.public_keys` del config PINEADO se RECHAZA. El "patron del tercer
firmante" del hueco 2 vale solo para el HMAC (override); la PUBLICA de verificacion vive en el
config pineado. Por tanto:
- Opcion A1 (sin re-genesis, RAPIDA): el empleado opera bajo Codex o Analista -> alta trivial
  (su HMAC + override + area personal). Coste: journal atribuye a esa identidad.
- Opcion A2 (identidad propia): estrena `<id>:v1` -> su pubkey entra al config pineado =
  re-genesis coordinado (mismo peso que un bump de epoch). Mas limpio para el estudio
  (atribucion nominal por humano). NO es un override.

### (B) Anchoring del clon remoto (config enforce, NO listado)
`anchor_config.remote_url = D:\Agentes\audit-anchor` es un path LOCAL de tu maquina; el clon
del empleado no puede anclar ahi. Opciones: el anchoring lo corre SOLO el clon canonico (tu
maquina) y el remoto opera con anchor deshabilitado local (override), o migras remote_url a un
remoto compartido (GitHub) accesible por ambos.

## Estado de la cola grande (sin idle)
TASK-1102 escalada (tercer NO-GO; motor correcto, bloquean fixtures+drift+UI -- espero tu
adjudicacion). Reconciliacion changelog<->serie formal: subagente mapeando (respondere aparte).
TASK-1203 (indexador) en cola. Contabilidad WS1 arranca en ventana.

-- Arquitecto
