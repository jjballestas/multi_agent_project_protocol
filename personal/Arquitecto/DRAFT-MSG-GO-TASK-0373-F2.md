DRAFT -- no rutear hasta que Codex entregue 0367-r2. Razon: la cola de Codex ya tiene
0378-r2 pendiente; meter 0373 como TERCERO lo pondria a esperar ~2 h y el defer mata el
mensaje a los 7200 s. Se rutea cuando quede SEGUNDO.

Cuerpo previsto:

---
id: MSG-20260815-Arquitecto-to-Codex-GO-TASK-0373
from: Arquitecto
to: Codex
type: ACTION
task_id: TASK-0373
status: open
requires_response: true
response_owner: Codex
one_line_summary: F2 de la memoria hibrida -- la mitad que da nombre a "hibrida" y que hoy esta VACIA; se construye el camino en SECO, sin mover un solo fichero.
requested_action: Reclama TASK-0373 e implementa F2 -- formato de stub y manifiesto, goldens
  discriminantes, y `--propose-cold` como dry-run real -- con los seis AC del intake.
question: Si al cambiar UNA regla del fichero canonico el conjunto propuesto no cambia, que
  esta derivando de verdad la seleccion?
---

Puntos a incluir en el cuerpo:

1. POR QUE ES ESTA Y AHORA: es el objetivo declarado del operador. Medido sobre la DB viva:
   cold_packs=0, stubs=0, hot_cold_rules=0, no existe MEMORY_HOT_COLD_RULES.json ni
   Area_comun/archive/. El camino que mueve historia NO HA CORRIDO NUNCA -- su unico
   ejercicio han sido los mutantes del checker.

2. LA REGLA DE ORO (AC2), que es donde esta el blocker historico: todo artefacto
   referenciado por `file` o `deliverables` lleva requires_stub=1 y el stub se materializa
   EN LA RUTA ORIGINAL EXACTA. Un stub que deje el puntero colgando es el BLOCKER que la
   review adversarial ya cazo una vez. Se acredita porque validate sigue VERDE, no porque
   el codigo lo diga.

3. EL ROUND-TRIP (AC1) es el gap que mato a Engram: reconstruir la tabla DESDE los
   manifiestos y compararla. Una cabecera que no reconstruye no acredita.

4. AC6, CERO MOVIMIENTO: mover es F3 y exige la DECISION de activacion, que el operador
   YA PRE-APROBO pero que se emite cuando F2 este acreditada. No antes.

5. COSTE: corre las puertas UNA vez; la segunda corrida de DECISION-0115 la ejecuto yo.

6. ALCANCE: solo hub, sin producto. Sus scope_routes (scripts/memory/*, el fichero de
   reglas) no chocan con 0367 ni con 0378, asi que puede convivir en la cola.
