# PROPUESTA DE DISENO -- TASK-0178: Consola del Arquitecto en el front (canal vivo Operador<->Arquitecto)

> Autor: Arquitecto. Fecha: 2026-08-02. Estado: **PROPUESTA para que el operador ELIJA** (respeta la bandera
> DEBATE: nada construido/promovido). Cristaliza el DEBATE-front-agent-console-roster.md en opciones decision-ready.
> Ligada a REQ-ZEUS-001. Repo de producto: Zeus-protocol (panel del operador); gobernanza en el hub.

## 0. La decision en una frase
Hoy el front **MIRA** (read-only) y **ESCRIBE gobernado** (submit_intent), pero no tiene canal de conversacion
con los agentes ni control de sus runtimes. La pregunta es **hasta donde** convertirlo en un tablero que **OPERA**,
sabiendo que el eslabon fuerte (gobernanza atestada #4) ya esta, y el debil es la **capa de runtime** (los agentes
son crons de sesion que sondean; si la sesion muere, nadie sondea).

## 1. Las 4 piezas candidatas (de mayor a menor valor/menor a mayor riesgo)

| Pieza | Que da | Esfuerzo | Riesgo | Necesita supervisor? |
|---|---|---|---|---|
| **P1 - Consola de prompt (Q2)** | Combo agente + caja -> MSG gobernado al mailbox + vista de hilo con respuestas. Hablarles y ver respuestas SIN VS Code. | Bajo | Bajo | No |
| **P2 - Indicador + boton de empuje (Q1-barato)** | Estado vivo/dormido/ultimo latido de cada agente + boton "enviar/despertar" (escribe mailbox y, si esta muerto, lanza su cron). | Medio | Medio | No (usa lanzar puntual) |
| **P3 - Supervisor front-server (Q1-auto)** | El server (unico always-on) mantiene UNO-Y-SOLO-UNO cron por agente, vivo/dormido, reinicio, enruta el mailbox. "El sistema trabaja solo con el front abierto." | Alto | **Alto** | Es el supervisor |
| **P4 - Roster de agentes (Q3, dos niveles)** | (a) Alta de WORKER de producto + enlace a LLM (formulario, off-by-default, keypair). (b) Alta de agente de GOBERNANZA = inicia ceremonia re-genesis (no toggle). | (a) Medio / (b) Alto | (a) Bajo / (b) Alto | No |

## 2. Menu de alcance (ELIGE uno)

- **Alcance A -- "Hablar" (minimo viable, recomendado para empezar):** solo **P1**. Expone el mailbox (ya
  gobernado/atestable) como consola en la UI. Maximo valor, minimo riesgo, sin tocar el modelo de runtime. Te quita
  la dependencia de VS Code para conversar con los agentes.
- **Alcance B -- "Hablar + ver + empujar":** **P1 + P2**. Anade estado de agentes y boton de empuje/despertar
  puntual (ejercer DECISION-0057 desde el front, sandbox a crons CONOCIDOS). Sigue sin comprometerte al supervisor.
- **Alcance C -- "Operar de verdad":** **P1 + P2 + P3 (+ P4a)**. El front-server pasa a supervisor always-on. Es
  la version potente pero la de mayor implicacion de gobierno y **costo** (ver s.4). Solo con el modelo de
  costo/ciclo-de-vida resuelto.
- **Alcance D -- Roster:** anadir **P4** a cualquiera de los anteriores (worker+LLM = formulario ya; gobernanza =
  ceremonia).

## 3. Recomendacion del Arquitecto
**Incremental: Alcance A ya -> Alcance B despues -> P3 solo cuando decidamos el modelo de costo.** Razon: la parte
dificil (gobernanza atestable) ya funciona; lo que falta es ingenieria de runtime honesta. P1 es el hueco real de
tu dia a dia (hablarles sin VS Code) y es barato y sin riesgo. El **supervisor (P3) NO** por "suena bien": primero
hay que resolver el **polling ocioso** (ver s.4) o sale caro y no mas capaz. P4b (agente que firma #4) **nunca** es
un boton: es ceremonia de re-genesis con tu presencia; venderlo como toggle seria mentir sobre la seguridad de #4.

## 4. El punto duro del supervisor (P3) -- costo y ciclo de vida
Un server web que lanza procesos de IA tiene dos riesgos reales que hay que cerrar ANTES:
- **Gobernanza:** sandbox DURO -- solo lanza crons de agentes REGISTRADOS, nunca un comando arbitrario; el front no
  gana una shell. Activacion != autoridad de riesgo (extiende DECISION-0057).
- **Costo:** mantener agentes vivos quema tokens en polling ocioso (esta metodologia ya gasto muchas rondas en
  "heartbeat sin novedad"). Un supervisor DEBE dormir agresivamente y **despertar por evento, no por reloj**. Sin
  esa disciplina, es caro sin ser mas capaz. -> P3 depende de un diseno de "wake-on-event" primero.

## 5. Decisiones de gobernanza necesarias ANTES de construir (segun el alcance elegido)
- **DECISION A (para P2/P3):** "el front puede lanzar/detener runtimes de agentes CONOCIDOS" (extiende DECISION-0057
  al operador-via-front; sandbox a crons registrados; sin shell).
- **DECISION B (para P1):** "consola de prompt operador->agente = compose de mailbox gobernado" (ASCII/PII-redactado;
  marca `operator-directive`; NO es un segundo escritor; el agente sigue sus reglas SDD).
- **RF-9 roster de dos niveles (para P4):** formaliza worker-producto (front-form) vs gobernanza-#4 (ceremonia).

## 6. Como se construiria (tras tu eleccion) -- SDD, off-by-default
Cada pieza como RF/SPEC propio, maker=Codex, checker=Analista+Arquitecto, off-by-default, repo Zeus-protocol,
gobernanza en el hub. P1 primero (no depende de nadie). No se promueve ni construye NADA hasta tu GO explicito
sobre el alcance (la bandera DEBATE sigue vigente hasta entonces).

## 7. Lo que necesito de ti para desbloquear
1. **Alcance** (A / B / C / D-combo).
2. Si incluye P3: tu OK a abrir primero el diseno "wake-on-event + sandbox" antes del supervisor.
3. Si incluye P4b: confirmar que el alta de agente-que-firma es ceremonia (no boton).
Con eso levanto la bandera DEBATE del alcance elegido y redacto los SPEC + tareas para Codex (como hice con 0309).
