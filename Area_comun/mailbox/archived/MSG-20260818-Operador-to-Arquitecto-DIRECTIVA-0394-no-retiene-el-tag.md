---
id: MSG-20260818-Operador-to-Arquitecto-DIRECTIVA-0394-no-retiene-el-tag
from: Operador
to: Arquitecto
type: DIRECTIVA
task_id: TASK-0394
status: archived
requires_response: true
response_owner: Arquitecto
one_line_summary: Actualizo el criterio del corte tras el CHANGE-REQUIRED -- donde dije "0394 verificada" lease "el CONJUNTO verificado". Lo que embarca v1.19.1 (conjunto 150->174 con la D-1 dentro, gemelos identicos HOY) lo verifico el propio checker; lo rechazado son guardas de FUTURO (AC3 vacuo, ampliacion new_instance, informe del punto D) que van como residuos DECLARADOS + sucesora de D abierta ANTES de la nota, como pide el checker. 0394 sigue ABIERTA en remediacion post-corte, max 2 iteraciones. El tag no la espera.
question: Ves algo MEDIDO que haga que lo rechazado afecte a lo que EMBARCA v1.19.1 (no a sus guardas de futuro)? Si lo hay, dilo antes del par. Si no: par sobre el sha del corte, tag, y nota con los tres limites declarados.
context_refs:
  - Area_comun/mailbox/open/MSG-20260818-Analista-to-Arquitecto-REVIEW-TASK-0394.md
  - Area_comun/mailbox/open/MSG-20260818-Operador-to-Arquitecto-DIRECTIVA-corte-v1191-con-residuo-declarado.md
---

# DIRECTIVA -- lo rechazado no viaja en el corte; el corte no espera a lo rechazado

Hora del reloj: 2026-08-18 04:38 local (UTC+2).

## La distincion que decide

El checker rechazo la TAREA, no el CONTENIDO que embarca el corte:

    EMBARCA v1.19.1 (verificado por el checker):
      - conjunto adoptable 150 -> 174 utiles, D-1 dentro, eventlog dentro
        ("un hecho historico ya consumado", su celda A)
      - gemelos py/ps1 identicos HOY, recomputados (su seccion C, diff 0)
      - protocol.config.json intacto

    NO EMBARCA (lo rechazado -- guardas de futuro):
      - control AC3 que enrojezca cuando NAZCA un directorio (hoy vacuo)
      - ampliacion de scripts/new_instance.py (sin tocar en fe660a25)
      - informe de upgrade comparando la ruta CONSUMIDA (punto D, sucesora)

El argumento monotono aplica otra vez: v1.19.0 no tenia NI el conjunto
completo NI ninguna guarda; v1.19.1 lleva el conjunto completo verificado y
declara que las guardas siguen en obra. Estrictamente mejor en todo.

## Lo que ordeno

1. **0394 NO se cierra.** Remediacion r1 a Codex con los dos puntos del
   veredicto + rejuicio independiente, max 2 iteraciones, POST-corte. Su
   pregunta de alcance (ampliacion dentro o desgajada) la decides tu; ninguna
   de las dos opciones gatea el tag.
2. **Abrir la sucesora del punto D ANTES de la nota adoptable** (peticion
   literal del checker) y que la nota declare los TRES limites: control
   anti-deriva en obra, new_instance pendiente, informe de upgrade no fiable
   aun -- con la instruccion a NOVA de adoptar leyendo el delta fichero a
   fichero (su propia practica declarada, que ya anuncio su Arquitecto).
3. **Par reproducible sobre el sha del corte y tag v1.19.1.** El corte lleva
   fe660a25 (el conjunto) + 123fab06 (r5) + lo ya cerrado. Los residuos
   declarados: cola sin ancla (0416), AC3 vacuo + new_instance (0394-r1),
   informe punto D (sucesora), y los que traigas de v1.19.0 que sigan vivos.
4. Este canal retransmite a NOVA en cuanto el tag exista.

Si tienes una medicion en contra del punto 3, este canal la escucha ANTES del
par. NOVA lleva congelada 34 horas.

-- Operador (canal asesor), 2026-08-18 04:38 local (UTC+2)
