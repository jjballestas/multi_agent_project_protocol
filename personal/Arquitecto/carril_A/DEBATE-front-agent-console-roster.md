# DEBATE - Front como panel de operacion de agentes (Q1 auto/launch, Q2 consola de prompts, Q3 alta de agentes + LLM)

> Estado: DEBATE (no desarrollar aun, orden del operador 2026-06-23). Drafts/propuesta; nada promovido ni construido.
> Autor: Arquitecto. Contexto: el front (Zeus-protocol) hoy OBSERVA (read-only) y ESCRIBE gobernado (submit_intent),
> pero NO tiene canal de conversacion con los agentes ni control de sus runtimes.

## Verdad arquitectonica de base (clave para las 3 respuestas)

Los agentes (Arquitecto/Codex/Analista) NO son un servicio always-on: corren como **crons de sesion** en este
entorno (PowerShell .ps1 que lanzan `codex exec` / la sesion de Claude). Mientras la sesion vive, un heartbeat
sondea el mailbox/estado y toma trabajo. Si la sesion se cierra, **nadie** sondea. El UNICO proceso que esta
always-on mientras el operador trabaja es **el server del front (Node)**. Esto es la palanca de diseno.

## Q1 - Cuando monto un requisito, el Arquitecto lo toma AUTOMATICO o lo lanzo yo?

**Hoy: semi-automatico y fragil.** El requisito que montas por el front entra al ledger (submit_intent) y con AC58
llega a origin. El Arquitecto lo recoge en el siguiente tick de su heartbeat (~30 min idle) **si su sesion esta
viva**. No hay (a) garantia de que el Arquitecto este despierto, ni (b) feedback en el front de si lo tomo, ni (c)
forma de "empujarlo" ya.

**Lo que falta (lo que tu instinto pide):**
- Un boton **"Enviar al Arquitecto"** en el intake que, ademas de registrar (submit_intent), NOTIFIQUE/DESPIERTE al
  Arquitecto (no esperar 30 min).
- Un **indicador de estado** del Arquitecto en el front: vivo / dormido / ultimo latido + ETA.
- El paso de fondo: **el server del front actua de SUPERVISOR** -- mantiene vivo el cron del Arquitecto y enruta el
  requisito. Eso convierte "polled+fragil" en "automatico+visible" y es lo que de verdad te quita la dependencia de
  tener una sesion VS Code/terminal abierta a mano.

**Respuesta corta:** hoy lo toma solo SOLO SI el Arquitecto esta vivo y dentro de ~30 min; deberia haber boton de
empuje + indicador + (mejor) el front-server supervisando. Las dos cosas (auto y boton) conviven: auto cuando esta
vivo, boton para empujar/despertar.

## Q2 - Hablarle a los agentes desde el front (combo de agente + prompt + respuesta)

**Es el hueco mas importante para que el front sea tu panel diario.** Hoy no hay canal de conversacion. PERO el
canal agente-agente YA EXISTE y es gobernado: **el mailbox** (MSG-*.md, ASCII, atestables). La solucion es exponerlo
en UI, no inventar un canal nuevo:

- **Combo de agente** (Arquitecto/Codex/Analista/worker) + **caja de prompt** -> compone un **MSG gobernado** a
  `mailbox/open` (`to:` ese agente), ASCII + PII-redactado (mismas guardas AC16).
- **Vista de hilo/conversacion**: lee el mailbox (open + archived) filtrado por ese agente y muestra tu prompt + las
  respuestas del agente. Asi ves las respuestas EN el front (como me hablas ahora, pero desde la UI).
- **Despertar el runtime** del agente destino si esta dormido (al enviar el prompt), para que lo procese ya.

Es exactamente lo que ya hacemos por mailbox, con cara de UI. **No es bypass** del gobierno: sigue siendo el canal
gobernado/atestable. Caveat de disciplina: un prompt libre a Codex podria saltarse el flujo SDD; para un panel
single-operator esta bien (eres el dueno humano), pero conviene marcar esos mensajes como `operator-directive` y que
el agente siga sus reglas de protocolo igual.

## Q3 - Registrar un agente desde el front + enlazarlo a un LLM

**Dos niveles (leccion del Extractor):**

1. **Worker de PRODUCTO que NO escribe el ledger** (como el Extractor; DECISION-0058 Opcion 2): se registra FUERA del
   config #4 (un roster de workers tipo `extractors.config.json`), con su keypair propio, off-by-default. -> **SI se
   puede dar de alta desde el front** + **enlazarlo a un LLM** (provider/endpoint/modelo: otro local-vlm, otro
   modelo de Ollama, etc.). Esto es un formulario del front perfectamente viable.
2. **Agente de GOBERNANZA #4 que FIRMA el ledger** (Arquitecto/Codex/Analista): el `agent_registry` esta **PINNED**
   bajo #4 (epoca 1.14.0). Dar de alta uno cambia el genesis -> **ceremonia de re-genesis-boundary GOBERNADA**
   (operador presente, provisioning de keypair), NO un toggle del front. El front puede **iniciar/preparar** la
   ceremonia, pero el flip es la ceremonia. (Esto es justo por lo que RF-9 roster quedo diferido.)

"Enlazar a un LLM" significa cosas distintas por nivel: worker = provider config (endpoint+modelo); agente de
gobernanza = wrapper de runtime (preset claude/codex). 

**Respuesta corta:** workers de producto + LLM = si, desde el front. Agentes que firman el ledger = ceremonia
gobernada, no boton.

## Propuesta (para construir DESPUES del debate) -- panel "Operar Agentes"

Un RF nuevo, en 4 piezas SDD, cada una off-by-default, maker=Codex/checker=Arquitecto+Analista:

1. **Consola de prompt** (Q2): combo agente + caja -> MSG gobernado al mailbox + vista de hilo (respuestas). PII/ASCII.
2. **Control de runtime** (Q1-launch): activar/detener + indicador vivo/dormido (DECISION-0057 ejercida por el
   operador via el front).
3. **Enviar requisito al Arquitecto** (Q1-auto): boton en el intake que registra (submit_intent) + notifica/despierta;
   y el **front-server como supervisor** que mantiene vivos los crons y enruta el mailbox.
4. **Roster RF-9 de dos niveles** (Q3): (a) alta de worker de producto + enlace a LLM desde un formulario
   (off-by-default, keypair); (b) alta de agente de gobernanza = inicia ceremonia re-genesis (no toggle).

## Decisiones de gobernanza necesarias ANTES de construir

- **DECISION nueva A:** "el front puede lanzar/detener runtimes de agentes CONOCIDOS" (extiende DECISION-0057 al
  operador-via-front). Sandbox duro: solo crons de agentes registrados, nunca un comando arbitrario; el front no gana
  una shell. Activacion != autoridad de riesgo.
- **DECISION nueva B:** "consola de prompt operador->agente = compose de mailbox gobernado" (ASCII/PII-redactado;
  marca `operator-directive`; no es un segundo escritor; el agente sigue sus reglas).
- **RF-9 roster de dos niveles** formalizado (worker-producto vs gobernanza-#4) -- ya estaba diferido; aqui se separa
  explicitamente lo que SI es front-form de lo que es ceremonia.

## El gran punto a decidir contigo

Que **el server del front pase a ser el SUPERVISOR always-on** (mantiene vivos los crons de los agentes y enruta el
mailbox). Hoy los agentes dependen de una sesion viva; si el front-server los supervisa, basta con tener el front
abierto para que el sistema "trabaje solo". Es la diferencia entre un tablero que MIRA y un tablero que OPERA. Es
tambien la pieza con mas implicacion de gobierno (un proceso que lanza runtimes), por eso es decision tuya primero.

## Opinion realista del Arquitecto (para discusion, 2026-06-23)

**Lo que esta solido hoy:** la capa de GOBERNANZA (ledger atestado #4, submit_intent single-writer, maker!=checker,
verificacion adversarial). El loop de 4 ciclos de TASK-0158 lo demostro: el Analista re-ejecuto el s9 en vivo y
atrapo dos pruebas falsas (259 catalogo, 208 tabla inexistente) que habrian dejado pasar un connector "read-only"
sin evidencia real. Eso es el corazon de la tesis y funciona.

**El eslabon DEBIL (y es el que tu intuicion toco):** la capa de RUNTIME. Los agentes no son un servicio; son
crons de PowerShell que sondean. Es fragil y se nota: esta sesion acumulo 8 instancias de cron duplicadas porque yo
reactivaba sin verificar; el lock las salvo, pero eso es suerte, no diseno. Para una tesis/demo alcanza; para una
"herramienta diaria" NO. Mi opinion: el front no sera un panel de operacion de verdad hasta que exista un
SUPERVISOR real (un proceso que tenga el ciclo de vida de los agentes: uno-y-solo-uno por agente, vivo/dormido,
reinicio, costo). El server-front es el candidato natural porque ya esta always-on.

**Prioridad honesta (lo que vale la pena vs lo que no, ya):**
1. **Q2 consola de prompts -- HAZLO PRIMERO.** Es lo de mayor valor, menor riesgo y menor esfuerzo: solo expone el
   mailbox (que ya es gobernado/atestado) en la UI. Te da "hablarle a los agentes y ver respuestas" sin VS Code, que
   es exactamente lo que te falta. No necesita supervisor.
2. **Q1 indicador vivo/dormido + boton de empuje -- SEGUNDO, en su version barata:** mostrar estado y un boton que
   escribe al mailbox y (si esta muerto) lanza el cron. Util ya, sin comprometerte al supervisor completo.
3. **El SUPERVISOR (front-server mantiene vivos los crons) -- es la decision grande y la dejaria para DESPUES de
   pensarla bien.** Es poderosa pero es la de mayor implicacion: un servidor web que lanza procesos de IA. Riesgos
   reales: (a) gobernanza -- hay que sandboxearlo a crons CONOCIDOS, nunca shell; (b) COSTO -- mantener agentes vivos
   quema tokens en polling ocioso (esta sesion gasto muchas rondas en "heartbeat sin novedad"); un supervisor debe
   dormir agresivamente y despertar por evento, no por reloj. Sin esa disciplina, te sale caro y no mas capaz.
4. **Q3 alta de agente + LLM -- separa los dos niveles y se honesto:** worker de producto (tipo Extractor) = SI, un
   formulario del front, factible y barato. Agente de gobernanza que firma el ledger = ceremonia de re-genesis con
   tu presencia, NO un boton; venderlo como boton seria mentir sobre la seguridad de #4.

**Mi veredicto:** la direccion es correcta y la parte dificil (gobernanza atestable) ya esta. Lo que falta es
ingenieria de runtime honesta. Yo iria incremental: Q2 ya, Q1-barato despues, y el supervisor solo cuando decidamos
el modelo de costo/ciclo-de-vida. No construir el supervisor "porque suena bien" sin resolver el polling-ocioso
primero.
