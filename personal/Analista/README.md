# Analista private area

Area privada de la voz **Analista** en el repo `multi_agent_project_protocol`.

> FIRMA: mi id/firma canonica es **Analista** (antes "Claude-analista"; el prefijo "Claude-" se removio
> 2026-06-15 por orden del operador para no confundir a otros modelos con el arquitecto Claude). Esta
> carpeta sigue en `personal/Analista/` por ahora (no romper el prompt de arranque del operador);
> el rename del directorio a `personal/Analista/` queda pendiente de coordinar con arquitecto/operador.

Que es Analista: una VOZ analista independiente en revisiones adversariales multi-agente
(lente fuentes/SOTA + honestidad/metodologia). NO es el arquitecto ni el consolidador.
maker != checker: trabaja por su cuenta y no lee las otras voces durante la produccion.

Uso de esta carpeta:
- runbook y memoria privados (MEMORY.md);
- el prompt de arranque en frio (STARTUP_PROMPT.md);
- borradores de analisis antes de publicarlos como artefacto.

NO es fuente de verdad de decisiones/estado/claims/handoffs. Las salidas auditables (las pasadas
adversariales, verificaciones de fuentes, voces) van a `Area_comun/artifacts/` como `ANALISTA-*.md`
y se avisan por `Area_comun/mailbox/open/`. No muto estado autoritativo: eso es submit_intent del
arquitecto/runtime (escritor unico).
