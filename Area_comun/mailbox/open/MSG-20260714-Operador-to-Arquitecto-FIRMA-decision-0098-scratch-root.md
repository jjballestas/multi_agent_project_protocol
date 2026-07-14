---
message_id: MSG-20260714-Operador-to-Arquitecto-FIRMA-decision-0098-scratch-root
from: Operador
to: Arquitecto
type: RESP
status: open
requires_response: true
response_owner: Arquitecto
created_at: 2026-07-14
context_refs:
  - Area_comun/decisions/DECISION-0098-scratch-root-unico-por-proyecto.md
  - Area_comun/mailbox/open/MSG-20260714-Arquitecto-to-Operador-RESP-scratch-root-ejecutada-decision-0098.md
one_line_summary: "FIRMA del operador: apruebo DECISION-0098 (scratch root unico por proyecto, D:/Aegis_Scratch). Sella via submit_intent y deja activo el cableado template/new_instance/validador. Ordenamiento inicial ya ejecutado queda RATIFICADO."
requested_action: "Sella DECISION-0098 en el ledger del hub (submit_intent intent decision, patron 0095/0096) y deja activo el cableado (template scratch_root + new_instance --scratch-root + validador condicional + gitignore). El fondo pineado NO se toca (campo opcional, sin re-genesis)."
question: "Confirmas sellado + cableado activo, y reportas?"
---

# FIRMA - DECISION-0098 (scratch root unico por proyecto)

FIRMO y apruebo la DECISION-0098 tal como esta redactada. Las 6 clausulas quedan aceptadas sin cambios:

1. Regla todos-los-proyectos: prohibido scratch ad-hoc en la raiz del disco; todo scratch bajo el
   paraguas unico D:/Aegis_Scratch/<proyecto>/<proposito>/ (~/Aegis_Scratch en POSIX).
2. Fuera del arbol atestado (gitignored, guards Aegis_Scratch/ + .protocol-tmp/); el scratch NUNCA
   guarda la unica copia de nada.
3. Declarado al nacer (campo OPCIONAL scratch_root en el template; new_instance --scratch-root);
   configs PINEADOS EXENTOS -- sin re-genesis.
4. Chequeo del validador condicional y aditivo (.py y .ps1, paridad): si el campo existe, ruta
   absoluta host-independiente y fuera del arbol de la instancia; ausente = valida como hoy.
5. Ciclo de vida: limpieza al stand-down (DECISION-0057), reap previa verificacion.
6. Ordenamiento inicial (ejecutado 2026-07-14 ~17:22 con mi autorizacion): RATIFICADO. Raiz limpia
   de nova-*; los 2 residuales quedan en D:/Aegis_Scratch/NOVA-Suite/residue/ (su reap final lo
   decido aparte; por ahora NO reap).

## Efecto que autorizo con esta firma
1. Sella DECISION-0098 en el ledger del hub (submit_intent intent decision).
2. Deja activo el cableado (template + new_instance + validador + gitignore).

El fondo pineado NO se toca (hub 2E35F26E / epoch 1.14.0 / dataset N=500 / sellos intactos).
