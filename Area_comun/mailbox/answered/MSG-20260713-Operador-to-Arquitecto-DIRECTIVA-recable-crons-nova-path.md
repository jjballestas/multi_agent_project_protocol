---
message_id: MSG-20260713-Operador-to-Arquitecto-DIRECTIVA-recable-crons-nova-path
from: Operador
to: Arquitecto
type: DIRECTIVA
status: answered
requires_response: true
response_owner: Arquitecto
created_at: 2026-07-13
context_refs:
  - personal/Codex/codex_mailbox_cron.ps1
  - personal/Analista/analista_mailbox_cron.ps1
  - personal/Arquitecto/SESSION_START_PROMPT_20260713b.md
one_line_summary: "Anomalia DECISION-0018: los 2 archivos de cron apuntan a la ruta MUERTA D:/Agentes/Zeus/NOVA-Suite/NOVA; la real es D:/Agentes/NOVA-Suite/NOVA (producto en raiz, gobernanza bajo Aegis/). Sin impacto ahora (agentes STOPPED), pero rompe en la reactivacion. Recablear antes de reactivar."
requested_action: "Recablea la base de ruta en los 2 archivos de cron de D:/Agentes/Zeus/NOVA-Suite/NOVA a D:/Agentes/NOVA-Suite/NOVA, considerando que el producto vive en la raiz y la gobernanza (submit_intent, Area_comun) bajo Aegis/. Idealmente antes de reactivar agentes."
question: "Confirmas el recable de las 2 rutas de cron a D:/Agentes/NOVA-Suite/NOVA (con la gobernanza bajo Aegis/)?"
---

# DIRECTIVA - Recable de ruta NOVA en los dos archivos de cron (anomalia DECISION-0018)

## Anomalia detectada (Asesor, verificada con ls)
Los dos archivos de cron apuntan a una ruta que ya NO existe tras el rename del operador:
- Ruta MUERTA: `D:/Agentes/Zeus/NOVA-Suite/NOVA` (verificado: `D:/Agentes/Zeus/NOVA-Suite` no existe).
- Ruta REAL actual: `D:/Agentes/NOVA-Suite/NOVA` (existe; producto en la raiz, gobernanza bajo `Aegis/`).

## Archivos y lineas
- `personal/Codex/codex_mailbox_cron.ps1`: lineas 352 y 362 (git status + "implementar el codigo requerido en D:/Agentes/Zeus/NOVA-Suite/NOVA").
- `personal/Analista/analista_mailbox_cron.ps1`: linea 371 (clona el repo de producto `D:/Agentes/Zeus/NOVA-Suite/NOVA` a un tmp).

## Contexto
- Rename del operador: repo -> `github.com/jjballestas/NOVA.git`; carpeta -> `D:/Agentes/NOVA-Suite/NOVA`; gobernanza encapsulada bajo `Aegis/` (modelo 2.A, DECISION-0095).
- Tu prompt 713b ya quedo correcto (`D:/Agentes/NOVA-Suite/NOVA`), pero los dos `.ps1` (recableados en ce81bd7 con `Zeus/NOVA-Suite`) quedaron rezagados respecto al rename final.

## Impacto
- Sin impacto en vivo: los agentes estan STOPPED (pausa natural). Rompe en la reactivacion: Codex escribiria en una carpeta inexistente; Analista clonaria una ruta inexistente.

## Accion pedida
Recablea en los 2 `.ps1` la base `D:/Agentes/Zeus/NOVA-Suite/NOVA` -> `D:/Agentes/NOVA-Suite/NOVA`, teniendo en cuenta que el producto vive en la raiz y la gobernanza (submit_intent, `Area_comun`) bajo `Aegis/`; ajusta cada comando segun corresponda. Es tu carril operativo (ciclo de vida de crons), asi que el recable exacto queda a tu criterio; adicionalmente, bajo el modelo dos-trios, confirma si estos crons del hub deben tocar NOVA o si su propio trio lo maneja. Idealmente antes de la reactivacion.

-- Operador (via Asesor)
