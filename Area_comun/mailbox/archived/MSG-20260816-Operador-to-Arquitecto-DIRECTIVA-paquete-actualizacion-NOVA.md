---
message_id: MSG-20260816-Operador-to-Arquitecto-DIRECTIVA-paquete-actualizacion-NOVA
task_id: none
type: DIRECTIVA
from: Operador
to: Arquitecto
status: archived
requires_response: true
response_owner: Arquitecto
one_line_summary: "DIRECTIVA con deadline: NOVA debe tener su instancia actualizada MANANA 2026-08-17. El operador te encomienda terminar lo que NOVA necesita para el upgrade. La ruta ya la acordamos en el debate (secuencia urgente corregida por tu C0/V6): pin de 0378, contrato residual de 0397, re-GO de 0337 con nombre nuevo, re-review de r2, corte en release etiquetada sobre verde reproducible con conteo de pasos. El Asesor coordina en paralelo la recepcion con el Arquitecto de NOVA."
requested_action: "Ejecuta en este orden y responde por mailbox con PLAN + ETA del corte + contenido exacto del paquete: (1) rechazo formal de 0378 por el pin; Codex remedia gancho + pin EN EL MISMO COMMIT sobre a5c5ad57, sin revertir r2. (2) Neutralizar el contrato residual de TASK-0397 que esta matando gates ajenos (mato el GO de 0337 esta noche). (3) Re-emitir el GO de TASK-0337 con NOMBRE DE MENSAJE NUEVO (el actual consta exhausted attempts=3 en el retry de Codex; la firma es Name|Length|Ticks, un nombre nuevo es una entrada nueva). (4) Rutear la re-review de r2 ampliada al pin, una sola pasada, con cero claims activos sobre esas rutas. (5) Corte del paquete: release etiquetada sobre verde REPRODUCIBLE (dos corridas, DECISION-0115) verificando CONTEO DE PASOS EJECUTADOS del job, no solo color (el rojo absorbe rojos; leccion F3). (6) Nota de version adoptable por upgrade_instance.py declarando que entra. Alcance minimo del paquete: fix del pin (la verificacion CI vuelve a operar) + 0337 verificada. 0408 entra SOLO si llega verificada manana; si no llega, NOVA recibe como interim la vigilancia manual de su retry.json y 0408 va en el siguiente corte -- no bloquea este. Registrar D-6 como tarea si el presupuesto de manana lo permite; tampoco bloquea."
question: "Que entra en el paquete de manana y a que hora estimas el corte (release tag)? Si ves imposible el deadline con 0337 verificada, dilo YA con el minimo viable que si llega."
context_refs:
  - personal/Analista/drafts/PROPUESTA-20260816-eficiencia-coordinacion-v2.md
  - personal/Arquitecto/REVISION-ADVERSARIAL-2-20260816-propuesta-v2-multivector.md
  - Area_comun/mailbox/archived/MSG-20260815-Codex-to-Arquitecto-HANDOFF-TASK-0378-remediation-2.md
  - .github/workflows/validate.yml
  - scripts/upgrade_instance.py
deadline_or_blocking_level: high
---

# DIRECTIVA - paquete de actualizacion para la instancia NOVA, corte MANANA 2026-08-17

Contexto operativo, verificado esta madrugada:

- El pin sha256 de `.githooks/pre-commit` en `validate.yml:117` NO coincide con el hook
  actual desde `6f0feb3b` (entrega 0378): el job muere en el paso 4 y salta 78 pasos.
  Dos dias con ~77% de la verificacion apagada. El corte NO puede certificarse hasta
  remediar esto; por eso es el paso (1).
- El GO de TASK-0337 esta MUERTO: `attempts: 3, exhausted: true` en el retry de Codex,
  con un error de contrato heredado de TASK-0397 (ya entregada). Pasos (2) y (3).
- El handoff r2 de 0378 (`a5c5ad57`) lleva desde el 15-ago 02:05Z esperando el ruteo de
  su review. Paso (4). El maker ya nombro el SHA: clonad ESE sha.

La prioridad del operador es inequivoca: manana NOVA actualiza su instancia. Todo lo
que no sirva a ese corte se difiere. El Asesor esta coordinando en paralelo con el
Arquitecto de NOVA la ventana de recepcion (freeze de crons, backup, upgrade, validate
en clon limpio, relanzamiento); cuando confirmes ETA del corte, se la traslado.

Responde por mailbox (este canal). El Asesor monitoriza open/ y origin/main.
