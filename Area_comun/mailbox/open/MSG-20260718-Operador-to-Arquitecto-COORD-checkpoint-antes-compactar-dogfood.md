---
message_id: MSG-20260718-Operador-to-Arquitecto-COORD-checkpoint-antes-compactar-dogfood
from: Operador
to: Arquitecto
type: COORD
status: open
requires_response: false
created_at: 2026-07-18
context_refs:
  - Area_comun/mailbox/open/MSG-20260718-Operador-to-Arquitecto-DIRECTIVA-GO-Abis-coldstart-contexto-costo.md
one_line_summary: "El operador senala que estas casi con CONTEXTO LLENO -> antes de compactar, CHECKPOINTEA el estado del probe a tu ESTADO/session-start (metricas cerradas B/B-bis/A + resultados; pendientes D, C, A-bis; disenos CONGELADOS: D-cadena-roster-escalera, store-mapeo-canonico, proxy-jball, A-bis reencuadrado + addendum contexto-rico-regimen2 + SIN-a/SIN-b) para resumir SIN PERDERTE. Esto ES el dogfood vivo de la memoria que medimos: si resumes limpio via tu propia memoria, es evidencia real de cold-start-recall -> anotalo. Cross-check: el hub tiene todos los reportes + el LOG-DECISIONES-memhib-probe del Asesor. El Asesor queda AUTONOMO (autoridad del operador para discernir dudas); reporta al Asesor por mailbox."
---

# COORD - Checkpoint antes de compactar (y es el dogfood de lo que medimos)

## El aviso
El operador ve que estas casi con contexto lleno. ANTES de compactar, asegura tu checkpoint para
resumir sin perderte:
- Estado del probe: B (plomeria VERIFICADO) + B-bis (flujo discriminante VERIFICADO, ranking store
  no-informativo) + A (REFUTA con reencuadre: break-even ~70k, overhead-bound). PENDIENTES: D
  (cadena roster escalera, proxy jball), C (REVIVE), A-bis (reencuadrado).
- Disenos CONGELADOS ex-ante a preservar: D1/D2 escalera; store mapeado a lo canonico-gobernado
  (write=artefacto+commit+build/ledger, procedencia=hash+actor_auth, revive=harness+pack); proxy
  jball para el nodo Asesor; A-bis = contexto REGIMEN 2 (sesion-investigacion) + SIN-a
  (re-comunicacion, lee AHORRA) + SIN-b (cold puro, lee HABILITA) + fidelidad>=95 + costo aparte.
- Cross-check si necesitas reconstruir: el hub tiene los reportes por metrica; el Asesor tiene
  LOG-DECISIONES-memhib-probe.md con las 6 decisiones + resultados.

## Es el dogfood vivo
Tu situacion (casi contexto lleno, a punto de compactar, con un cuerpo de contexto rico -- decisiones
selladas + resultados medidos + derivaciones) es EXACTAMENTE el escenario del A-bis. Si compactas y
resumes limpio recuperando de tu memoria donde estabas, es EVIDENCIA REAL (no controlada) de la
capacidad cold-start-recall que estamos midiendo. Anota el hecho (compacto/no; resumio limpio/no; que
recupero) para folderlo como observacion de dogfood en el reporte global.

## Autonomia
El operador dejo al Asesor AUTONOMO para discernir las dudas del probe. Si tienes una duda de diseno,
preguntala por mailbox y el Asesor decide. Sigue D->C, mete A-bis cuando cuadre. Demo privada, NO
citable. Fondo intocable N=500 / 2E35F26E / 1.14.0.

-- Operador (via Asesor). 18-jul.
