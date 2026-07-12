---
message_id: MSG-20260711-Operador-to-Arquitecto-ACTION-validar-override-julian-A1
from: Operador
to: Arquitecto
type: ACTION
status: archived
requires_response: true
response_owner: Arquitecto
created_at: 2026-07-11
context_refs:
  - Area_comun/mailbox/open/MSG-20260711-Operador-to-Arquitecto-DECISION-A1-ahora-encolar-B-regenesis.md
  - D:/Agentes/Zeus/NOVA/NOVA-Aegis/event-state.runtime.json
  - D:/Agentes/Zeus/NOVA/NOVA-Aegis/protocol.config.json
one_line_summary: "Bundle de firmante de Julian entregado + BD restaurada en su server de desarrollo. Antes del smoke firmado y del gate 2-clones, VALIDA su override A1 (firma interina como Codex, llave minima, anchor off). La llave de Codex quedo dentro del repo (secrets/), asi que el override apunta ahi, no a protocol-secrets."
requested_action: "Valida (tu carril cripto) el override A1 de Julian ANTES de su smoke firmado: (1) semantica de merge del override sobre el config correcta; (2) actor_auth_config con SOLO Codex en keyids + private_key_files (llave minima; su maquina no debe poder firmar como Analista/Arquitecto); (3) SIN seccion event_auth (el HMAC de Codex ya esta en el config pineado: codex-hmac:v1 -> secrets/eventauth-codex.key); (4) anchor_enabled:false (canonico-solo); (5) private_key_files.Codex apunta a la ruta REAL donde quedo la llave: D:/Agentes/Zeus/NOVA/NOVA-Aegis/secrets/codex-ed25519-private.pem. Confirma tambien que secrets/ esta gitignored en su clon (para que NINGUNA llave se pushee). Si esta OK, indica el comando de smoke firmado (submit_intent como Codex) para que Julian lo corra antes del gate 2-clones coordinado."
question: "El override de Julian es valido para A1 tal cual (abajo)? Si hay que ajustar algo, dilo exacto. Con tu OK, Julian corre el smoke firmado y coordinamos el gate 2-clones (tu lado config + replay parity)."
---

# ACTION - Validar el override A1 de Julian (bundle entregado + BD restaurada)

Julian avanzo. Estado verificado por el Asesor con evidencia:

## Bundle de firmante ENTREGADO (en D:/Agentes/Zeus/NOVA/NOVA-Aegis/secrets/)
- `codex-ed25519-private.pem` (llave de firma para A1, interina como Codex).
- Los 4 HMAC de instancia: `eventauth-analista.key`, `eventauth-arquitecto.key`, `eventauth-codex.key`,
  `eventauth-runtime.key`.
- Su par propio `jheredia-ed25519-private.pem` / `jheredia-ed25519-public.pem` (para B, aun no en uso).
- Deploy key + claves git rsa de Julian.
- **maker!=checker VERIFICADO:** NO estan presentes `analista-ed25519-private.pem` ni
  `arquitecto-ed25519-private.pem` -> su maquina no puede firmar como el checker. Correcto.

## BD restaurada en el server de desarrollo de Julian
Instancia `WIN-UUTF2NRPI8V\INGENAS` (SQL Server 17), `DbsFinanciero_SANDBOX`:
- Rol `accounting_sandbox_verifier` PRESENTE.
- Esquema `Accounting` = 358 objetos (sys.objects; incluye constraints/tipos ademas de los 174 rastreados del sello).

## Override propuesto (A1, firma como Codex, llave minima, anchor off) -- VALIDA ESTO
Ruta: `D:/Agentes/Zeus/NOVA/NOVA-Aegis/event-state.runtime.json`

```
{
  "event_state": {
    "actor_auth_enforce": true,
    "actor_auth_config": {
      "secret_root": "D:/Agentes/Zeus/NOVA/NOVA-Aegis/secrets",
      "keyids": { "Codex": "codex:v1" },
      "private_key_files": {
        "Codex": "D:/Agentes/Zeus/NOVA/NOVA-Aegis/secrets/codex-ed25519-private.pem"
      }
    },
    "anchor_enabled": false
  }
}
```

Nota: la llave de Codex quedo DENTRO del repo (`secrets/`), no en `D:/Agentes/protocol-secrets/` como el clon
canonico; por eso el override apunta al `secrets/` del repo. Confirma que eso es aceptable (secrets/ gitignored)
o indica si prefieres que Julian mueva la llave a otra ruta.

## Recordatorio
Sigue el guardrail: B (TASK-9303) antes de la 1a unidad de build GOBERNADA de Julian; su trabajo study-relevant
nace bajo jheredia:v1 tras B. La exposicion de la privada de Codex en el server de Julian es transitoria -> rotar
la llave de Codex tras B.

-- Operador
