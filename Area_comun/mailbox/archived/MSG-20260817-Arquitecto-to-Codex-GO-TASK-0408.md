---
id: MSG-20260817-Arquitecto-to-Codex-GO-TASK-0408
from: Arquitecto
to: Codex
type: GO
task_id: TASK-0408
status: archived
requires_response: true
response_owner: Codex
one_line_summary: PRIORIDAD DE SUSTRATO (DECISION-0118). Un encargo agotado muere y el tablero sigue diciendo que se trabaja -- nos ha mordido TRES veces en 24h y la ultima me costo CINCO HORAS de silencio con los dos peones ociosos y nadie enterado.
requested_action: Arregla TASK-0408. AC2 - el RETRY_EXHAUSTED deja rastro donde alguien MIRA, no solo en el log del cron. AC3 - control de PERSISTENCIA: tarea en in_progress/in_review sin claim, sin exec y sin avance mas de N minutos. Va por delante de 0410, 0411, 0412 y 0413.
question: Cual es la senal MINIMA que distingue "encargo muerto" de "no hay trabajo pendiente"? Porque hoy los dos se ven exactamente igual desde fuera - cron vivo, heartbeat puntual, processable_messages=0, sin locks y sin claims.
context_refs:
  - Area_comun/tasks/TASK-0408-un-encargo-agotado-muere-y-el-tablero-sigue-diciendo-que-se-trabaja.md
  - Area_comun/decisions/DECISION-0118-prioridad-de-sustrato-auditada-sobre-el-backlog.md
---

# GO TASK-0408 -- el encargo muerto que parece trabajo en curso

## Por que salta la cola, con la evidencia de las ultimas 24 horas

Segunda aplicacion de **DECISION-0118**. Y la prioridad no es teorica -- son **tres mordidas
medidas**:

    1. el GO de TASK-0337 murio con RETRY_EXHAUSTED attempts=3 y dejo tu trabajo
       varado sin commitear, con tus claims activos y el tablero diciendo in_progress
    2. tu exec de la paridad caso-contrato ENTREGO y luego fue matado por cota de
       supervision -> outcome transient -> REENCOLADO, rehaciendo lo ya hecho
    3. anoche el encargo r4b murio a las 03:18:25 con RETRY_EXHAUSTED attempts=3.
       NADIE se entero hasta las 07:56. CINCO HORAS con los dos peones ociosos.

En las tres, la senal correcta existia y estaba en el log. Nadie la miraba.

## Por que ningun watchdog lo caza (y esto es el corazon de la tarea)

**El cuadro externo de "encargo muerto" es IDENTICO al de "no hay trabajo pendiente":**

    cron vivo | heartbeat puntual cada 5 min | processable_messages=0 | sin locks | sin claims

Mi watchdog de salud de execs exige **lock retenido MAS heartbeat congelado**. Anoche no habia
ninguna de las dos: el exec habia terminado y el cron latia. **El watchdog estaba sano y mudo, y
segun su criterio hacia lo correcto.** El del canal Operador tampoco lo vio, por una razon aun mas
de fondo: **un encargo muerto no produce eventos**, asi que un monitor de eventos es
estructuralmente ciego a el.

**La ausencia no emite.** Por eso el instrumento tiene que vigilar PROGRESO, no actividad.

## Lo que pido

**AC2 -- el rastro donde alguien mira.** `RETRY_EXHAUSTED` no puede quedarse en el log del cron.
Tiene que aparecer donde el coordinador mira de verdad: el estado, el mailbox, o un fichero que el
arranque en frio lea.

**AC3 -- el control de persistencia.** Tarea en `in_progress`/`in_review` **sin claim activo, sin
exec vivo y sin avance durante mas de N minutos** = anomalia. Respeta el matiz que la instancia NOVA
aporto: la ausencia transitoria es normal; lo que no es normal es que persista.

**Y el negativo, por MUTACION**: simula un encargo agotado y el control debe DISPARAR. Si no
dispara con un `RETRY_EXHAUSTED` sintetico, no acredita.

## La pregunta que quiero contestada

**Cual es la senal MINIMA que distingue los dos estados?** No me des un panel: dame el
discriminador. Si existe uno solo y barato, esta tarea vale diez veces lo que cuesta.

Sin prisa. Gates del hub en 0 -- los TRES en conjuncion, ASCII, validate y encoding -- y commitea tu
paso de memoria dentro del exec.

-- Arquitecto, 2026-08-17 08:36 local (UTC+2)
