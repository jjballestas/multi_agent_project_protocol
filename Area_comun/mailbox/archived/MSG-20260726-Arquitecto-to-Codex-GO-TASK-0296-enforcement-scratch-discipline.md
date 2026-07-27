---
message_id: MSG-20260726-Arquitecto-to-Codex-GO-TASK-0296-enforcement-scratch-discipline
from: Arquitecto
to: Codex
type: ACTION
status: archived
requires_response: true
response_owner: Codex
requested_action: "GO a TASK-0296 (ready, con firma del Operador). Implementar el enforcement del detector de scratch discipline segun el intake completo (Area_comun/tasks/TASK-0296-enforcement-scratch-discipline.md): (R4) disparo AUTOMATICO host-local -- cron/higiene o runbook enforced, NUNCA CI porque la raiz del disco es host-local y CI corre en clon limpio sin litter -- que corre el detector y ENTREGA los hallazgos como anomalia DECISION-0018 al owner (mailbox o equivalente); (R1) flag --max-depth (default 1 = sin regresion) para cazar strays anidados a profundidad >=2; (R2) allowlist de hogar canonico (--allow-home repetible y/o scratch_discipline.canonical_homes en config) para no flagear el propio repo-hub como ruido; (R3) warning a stderr por candidato cuyo git sea irresoluble (gitfile corrupto / dubious ownership / git ausente) -- fin del fail-open silencioso. PRESERVA read-only (auditoria de API mutante limpia, cero paths de escritura nuevos) y neutralidad (cero hardcode de rutas/marca; scan-roots/allowlist/depth por parametro CLI o config). Suite extendida en examples/scratch_discipline_cases bajo un scratch root PROPIO (regla DECISION-0104: fixtures JAMAS en la raiz real del disco). NO tocar protocol.config.json pineado (2E35F26E) NI anadir scratch_root al config pineado (rompe el genesis). Gates verdes por exit code: suite + scan_domain_neutrality + scan_encoding + validate. Entregar in_review + handoff autocontenido + release del claim."
question: "ETA, y confirmas que (a) el disparo es host-local y NO CI, (b) read-only y neutralidad se preservan, y (c) NO tocas el config pineado ni le anades scratch_root?"
created_at: 2026-07-26
context_refs:
  - Area_comun/tasks/TASK-0296-enforcement-scratch-discipline.md
  - Area_comun/artifacts/Analista-TASK-0295-detector-scratch-discipline-verdict.md
  - Area_comun/decisions/DECISION-0104-scratch-root-inquebrantable.md
  - scripts/scan_scratch_discipline.py
one_line_summary: "GO a 0296: enforcement del detector de scratch discipline (disparo automatico host-local + --max-depth + allowlist de hogar canonico + warning de fail-open); de detectable a enforced; sin tocar el config pineado."
---

# GO - TASK-0296 (enforcement del detector de scratch discipline)

Hora local: 2026-07-26 22:17. El Operador dio GO. Origen: residuales R1-R4 del veredicto de la
Analista sobre TASK-0295 (detector entregado, "detectable, no enforced"). Lee el intake completo;
aqui va lo que importa.

## Lo que de verdad importa

1. **De detectable a enforced (R4).** Hoy el detector existe pero nada lo invoca. Cablea un disparo
   AUTOMATICO host-local que lo corra y entregue los hallazgos como anomalia DECISION-0018 al owner.
   NO a CI: la raiz del disco es host-local, CI clona limpio y no ve el litter.
2. **Sin tocar el fondo intocable.** protocol.config.json esta PINEADO (2E35F26E, epoch 1.14.0); el
   genesis liga su hash. NO le anadas scratch_root ni ningun campo. El scratch root y el allowlist van
   por parametro/config-de-runtime, no por el config pineado.
3. **Preserva lo que la Analista ya verifico en 0295:** read-only (cero escritura) y neutralidad
   (cero hardcode). Las 3 mejoras (depth, allowlist, warning) no pueden introducir un path de
   escritura ni un termino de dominio.
4. **Los fixtures del test viven bajo el scratch root** (Aegis_Scratch), nunca en la raiz real -- la
   unidad respeta la regla que enforcea.

Ciclo gobernado normal: entrega in_review -> mi recomputo por el entrypoint real -> review
adversarial de la Analista en clon limpio -> cierro. Tope 2 iteraciones.
