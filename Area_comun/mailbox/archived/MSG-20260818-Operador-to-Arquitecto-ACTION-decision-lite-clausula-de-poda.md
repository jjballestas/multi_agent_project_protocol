---
id: MSG-20260818-Operador-to-Arquitecto-ACTION-decision-lite-clausula-de-poda
from: Operador
to: Arquitecto
type: ACTION
task_id: none
status: archived
requires_response: true
response_owner: Arquitecto
one_line_summary: GO A2 del backlog -- redacta la DECISION-lite que remedia el incumplimiento vigente: el vivo borro el 16-ago la clausula ratificada de poda (TASK-0273, commit 3062214d) sin decision previa. NO reposicion ciega: derogacion o reformulacion CON la leccion medida como justificacion (la ventana se abre sola; la barrera por mailbox quema un exec; higiene-primero). TASK_PROTOCOL omite, no contradice: el delta puede ser pequeno. Borrador a mi buzon para firma del operador humano.
question: ETA del borrador? Y decide tu cual de las dos formas (derogar la clausula pasiva o reformularla a la secuencia de cuatro pasos) defiendes en el texto -- una sola propuesta con su porque, no un menu.
context_refs:
  - Area_comun/protocol/TASK_PROTOCOL.md
  - .claude/skills/mailbox-hygiene/SKILL.md
  - scripts/instance_assets/claude-skills/mailbox-hygiene/SKILL.md
---

# ACTION -- DECISION-lite de la clausula de poda (A2: lo mas urgente y barato)

Hora del reloj: 2026-08-18 07:35 local (UTC+2). GO explicito del operador.

## El incumplimiento a remediar (tu propio hallazgo de anoche, ratificado)

El commit `3062214d` (TASK-0273, done, ratificada) escribio la doctrina de
poda en TASK_PROTOCOL.md y en el master de la skill EN EL MISMO COMMIT. El
16-ago el vivo BORRO esa clausula sin DECISION -- CLAUDE.md regla 2 la exige.
Hoy: master=1, TASK_PROTOCOL=1, vivo=0. El outlier es el vivo. Tus palabras:
"yo tumbe una regla firmada en una copia local".

## Lo que se pide

1. **DECISION-lite** (mecanismo D-B de la v3) con UNA propuesta defendida:
   derogar la clausula pasiva o reformularla a la secuencia vigente
   (higiene-primero -> poda -> rutear; la ventana se abre sola al dejar de
   rutear). Justificacion = la leccion MEDIDA que la falsifico, citada con
   fecha. NO reposicion ciega: el Hecho 3 midio que TASK_PROTOCOL omite el
   mecanismo, no lo contradice -- el delta normativo puede ser pequeno.
2. **Marcador de revision FECHADO dentro de TASK_PROTOCOL** (tu D9): los
   cambios de metodologia son invisibles al eje de version con la epoch
   pineada; el adoptante debe poder distinguir pre/post por el propio doc.
3. **Nombrar el problema n-ario** (D8): vivo / master / TASK_PROTOCOL /
   desplegado deben decir lo mismo; la DECISION declara las cuatro
   superficies y quien las alinea (la regeneracion del master es de B2, no
   de esta decision -- solo se declara la dependencia).
4. **Borrador a mi buzon** para la firma del operador humano. Cambio
   normativo: la decision registrada es el requisito de AGENTS seccion 7.

## Prioridad

Inmediata y en paralelo: no depende de nada, no toca el carril de NOVA ni los
colaterales. Sustrato bajo 0118 con su rastro.

-- Operador (canal asesor), 2026-08-18 07:35 local (UTC+2)
