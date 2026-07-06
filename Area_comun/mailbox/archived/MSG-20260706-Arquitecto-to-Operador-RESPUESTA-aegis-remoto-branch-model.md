---
message_id: MSG-20260706-Arquitecto-to-Operador-RESPUESTA-aegis-remoto-branch-model
from: Arquitecto
to: Operador
type: HANDOFF
status: archived
requires_response: false
created_at: 2026-07-06
context_refs:
  - Area_comun/mailbox/open/MSG-20260706-Operador-to-Arquitecto-ACTION-aegis-remoto-github-llave-provista.md
  - Area_comun/artifacts/CROSS-ATESTACION-hub-aegis-registro.md
  - Area_comun/protocol/RUNBOOK-onboarding-multi-clon-aegis.md
one_line_summary: "Item 4 CERRADO con branch model resuelto: canonica de la instancia = aegis/main (main del remoto NO es auto-init de GitHub: es la historia del repo de PRODUCTO Zeus-Aegis, con su remote identico; no se toca). Ademas: humo e2e 3 firmantes VERDE y DECISION-1001/1002 registradas -- lote items 1, 2 y 4 drenados; solo queda BR-C4."
requested_action: "Ninguna. Si prefieres repo GitHub separado para la instancia en vez de la rama aegis/main, dilo y muevo en 1 comando; si no, el modelo queda como esta documentado."
---

# RESPUESTA - Item 4 cerrado + branch model + estado del lote (05:58 local, 2026-07-06)

## Branch model resuelto (con una correccion factual a la lectura del remoto)

- **`refs/heads/main` = `fb8cc210` NO es un commit inicial auto-creado por GitHub:** es la
  historia del repo de PRODUCTO `D:/Agentes/Zeus/Zeus-Aegis` (su `origin` es EXACTAMENTE esta
  misma URL y su main local esta 21 commits adelante de ese fb8cc210). El repo GitHub
  Zeus-Aegis ya era el remote del producto antes de hoy.
- **Canonica de la INSTANCIA = `aegis/main`** (head `3e9e90b8`). No pusheo la instancia sobre
  `main` (clobbearia el producto) ni pusheo los 21 commits pendientes del producto (carril de
  Codex, no mio). Clones del runbook: `git clone -b aegis/main git@github.com:jjballestas/Zeus-Aegis.git`.
- Deploy key cableada (`core.sshCommand` local), `git-key/` gitignored y leak-check limpio
  (coincide con la verificacion del Asesor), refspec de origin corregido (estaba pineado a
  refs/tags/v1.18.0), tracking `main -> origin/aegis/main`.
- Si prefieres un repo separado (p.ej. `NOVA-Aegis`, evita mezclar producto e instancia en un
  mismo repo), lo muevo con un comando y actualizo el runbook; con la rama dedicada el modelo
  tambien funciona.

## Ademas, desde tu ultima lectura del lote (items 1 y 2 TAMBIEN drenados)

1. **Humo e2e de firmantes VERDE (item 1 completado):** tras tu aprovisionamiento corri
   TASK-9301 en el ledger de Aegis: ciclo completo ready -> done con los 3 firmantes
   (Arquitecto upsert, Codex claim/build-flips/done, Analista ratificacion). Los 14 eventos
   verificados VALIDOS en actor_auth ed25519 + event_auth HMAC; validate 0; drift 0.
   NOTA: el gate del runbook "humo entre DOS clones con llaves separadas por maquina" es un
   paso ADICIONAL que corre antes de la primera tarea real de Contabilidad (este humo probo
   los 3 firmantes en el clon canonico).
2. **DECISION-1001 y DECISION-1002 = accepted y REGISTRADAS** en el ledger de Aegis (intents
   decision firmados, commit Aegis `3e9e90b8`) con tu aprobacion interactiva como approval_ref.
3. **Entrada 1 de cross-atestacion anclada en el hub** (head seq 3475, sha256 del events.jsonl
   completo; ver CROSS-ATESTACION-hub-aegis-registro.md).

## Lote restante

- **BR-C4** (paquete DEC P3.x): unica firma pendiente.
- Opcional: tu preferencia repo-separado vs rama aegis/main (arriba).

-- Arquitecto
