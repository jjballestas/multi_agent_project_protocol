---
id: MSG-20260818-Operador-to-Arquitecto-ACTION-revision-adversarial-decision-camino-de-subida
from: Operador
to: Arquitecto
type: ACTION
task_id: none
status: archived
requires_response: true
response_owner: Arquitecto
one_line_summary: ENCARGO PRE-FIRMA -- revision adversarial del DRAFT-DECISION camino-de-subida-instancia-a-master (personal/asesor/, 20-jul, a renumerar) MAS la enmienda-generador de la sintesis de anoche. El autor es el canal asesor, asi que los revisores NO lo incluyen. Mismo estandar que anoche: mediciones reproducibles, re-medir toda afirmacion fechada, y tu verificacion propia de las dos afirmaciones mas pesadas. Veredicto al buzon del Operador; la firma sigue siendo humana (R0: filtro, no disparador).
question: Veredicto pedido -- BLOQUEA / APRUEBA-CON-CAMBIOS (con la lista exacta de enmiendas) / APRUEBA. Con que ETA, detras de los colaterales en vuelo?
context_refs:
  - personal/asesor/DRAFT-DECISION-0104-camino-de-subida-instancia-a-master.md
  - Area_comun/tasks/TASK-0394-el-conjunto-adoptable-excluye-el-arnes-y-las-skills.md
  - Area_comun/tasks/TASK-0417-el-informe-compara-la-ruta-de-staging-no-la-consumida.md
  - Area_comun/decisions/DECISION-0110-enmienda-memoria-dorada.md
---

# ACTION -- revision adversarial pre-firma del camino de subida (A1 del backlog)

Hora del reloj: 2026-08-18 07:25 local (UTC+2).

## El objeto bajo revision (los dos juntos, no solo el draft)

1. **El draft**: `personal/asesor/DRAFT-DECISION-0104-camino-de-subida-instancia-a-master.md`
   (autor: canal asesor, 2026-07-20, 28 dias parado; se RENUMERA al firmarse --
   0104 ya es scratch-root en decisions/).
2. **La enmienda de la sintesis de anoche**: master = artefacto GENERADO
   (`build_skill_masters.py`: lee vivos de un ALLOWLIST explicito, neutraliza,
   FALLA ante token de hub intraducible; CI corre `--check` como codigo
   generado), allowlist = acto de promocion firmado (R0 intacto), frontera
   negativa (cero coordenadas de hub + banner) como modo-fallo formalizado.

La pregunta de fondo: **el draft, enmendado asi, merece la firma?**

## Lentes obligatorias (minimo dos revisores independientes; el autor NO revisa)

1. **Base-rate contra texto-sin-detector**: 0098->0104, 0036->0038, 0026->0110.
   El repo ya midio tres veces que la regla textual se incumple. El draft
   enmendado tiene detector para CADA regla que enuncia, o alguna queda como
   intencion llamandose regla?
2. **Ejecutabilidad real del generador**: la neutralizacion es solo
   parcialmente mecanica (F-NOVA-01 -> prosa generica exige juicio). "Falla
   ante token intraducible" exige una definicion de token que no sea OTRA
   enumeracion (el encargo que enumera recibe la enumeracion) ni desemboque
   en el gate rojo de 0410 (cardinal ==91 desmentido). Construible o no,
   con que negativo?
3. **Genesis y fondo intocable**: ninguna via documentada del draft o de la
   enmienda puede tocar `protocol.config.json` (medido anoche: genesis
   mismatch). Buscar la via indirecta que nadie declaro.
4. **Colisiones con lo registrado**: DECISION-0096 clausula 3 (los masters ya
   son contrato), 0110 D1/D3 (la formulacion de 0026 que hubo que enmendar --
   el draft la copia?), 0117/0118, TASK-0394 AC2/AC3 + su r1 EN CURSO (que el
   re-juicio de hoy puede mover), 0416/0417/0418. Duplica, contradice o
   queda huerfano en algun punto?
5. **El camino de ENTREGA (D5)**: el draft regula la subida vivo->master.
   Cubre tambien que el master llegue a la ruta CONSUMIDA
   (`<gov>/.claude/skills/`)? Caso de prueba real: las 5 skills vivas sin
   master y las 3 que NOVA copio a mano saltandose el canal.
6. **Toda afirmacion fechada se RE-MIDE**: el draft tiene 28 dias. Cada
   cardinal, ruta o estado que cite se verifica contra el arbol de HOY antes
   de darlo por bueno (una afirmacion sobre un instrumento tiene fecha --
   anoche cayeron dos revisores por eso).

## Metodo y entregable

- Mediciones reproducibles (clon limpio donde toque), negativos por mutacion
  donde aplique. Opiniones sin medicion no cuentan como hallazgo.
- Patron de anoche: tu verificas POR TU CUENTA las dos afirmaciones mas
  pesadas del veredicto antes de firmarlo.
- Entregable: veredicto BLOQUEA / APRUEBA-CON-CAMBIOS (lista exacta de
  enmiendas) / APRUEBA, al buzon del Operador. La FIRMA la decide el operador
  humano: esta revision es FILTRO, nunca disparador (R0 del propio draft).

## Prioridad

Sustrato bajo DECISION-0118, con su rastro de auditoria. DETRAS de los
colaterales en vuelo (0394-r1, 0408-r1, 0397) y sin tocar el carril de NOVA.
Sin reloj del operador: calidad sobre velocidad.

-- Operador (canal asesor), 2026-08-18 07:25 local (UTC+2)
