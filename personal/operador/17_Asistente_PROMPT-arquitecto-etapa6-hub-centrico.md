# 17_Asistente - GO/brief Etapa 6 (multi-proyecto + kickoff RF-10) - MODELO HUB-CENTRICO

> Insumo del operador (asistente Cowork) para el ARQUITECTO (Claude en VS Code).
> El asistente NO redacta la DECISION ni muta estado: esto es el brief de requisitos.
> Fecha: 2026-06-20. Canal ASCII. Supersede nada; cierra la pregunta de modelo multi-proyecto.
> Estado de partida (canonico): #4 ON epoca 1.14.0 INTACTA; Front etapas 1-4 + AC11 (TASK-0129)
> DONE; etapa 5 roster DEFERIDA; etapa 6 ENCOLADA (este GO la arranca).

## 0. Decision del operador (cierra la ambiguedad del selector)
MODELO **HUB-CENTRICO (DECISION-0050)**. El selector lista repos-PRODUCTO bajo D:\Agentes\Zeus\
read-only; la GOBERNANZA sigue siendo el HUB UNICO (tasks/claims/ledger/atestacion) = un solo dataset
de tesis. Multi-instancia (varias raices con su propio Area_comun) queda EXPLICITAMENTE FUERA DE ALCANCE
= posterior, su propia DECISION (cambia el modelo de confianza; ademas exigiria git-init de instancias
no-canonicas).

Contexto que motiva la decision: bajo Zeus hay Zeus-protocol (repo producto git, gobernado por el hub) y
NOVA (modernizacion del legacy Dbsfinanciero; instancia separada con su PROPIO Area_comun, hoy NO-git).
Budget vive DENTRO de NOVA y es trabajo POST-T0 (PII-gated). Por eso NO se resuelve multi-instancia ahora:
NOVA aparece en el selector como dir read-only y NO se lee su Area_comun (no-git = no canonico -> choca
con AC1/AC5 si se intentara).

## 1. Objetivo
Cerrar el front a "totalmente funcional" con la Etapa 6 (multi-proyecto MVP-light + kickoff RF-10), de a
UNA pieza, por SDD (maker=Codex / checker=Arquitecto / reproduccion desde clon limpio).

## 2. Entra por el metodo (en el hub)
1) **DECISION-0050** en Area_comun/decisions/ que fija el MODELO HUB-CENTRICO del selector multi-proyecto:
   - El selector lista repos-PRODUCTO bajo Zeus leyendo su estado CANONICO read-only (HEAD/branch/estado CI).
   - La gobernanza/atestacion permanece en el HUB UNICO (= dataset). Acoplamiento unidireccional: el front
     NUNCA escribe a los repos producto ni a instancias externas.
   - RF-10 kickoff = registrar el T0 gobernado del proyecto nuevo EN EL HUB via submit_intent (sin bypass).
   - Multi-instancia/multi-hub = FUERA DE ALCANCE (posterior, DECISION aparte; requeriria canonizar git la
     instancia). Aditiva, neutral. SemVer MINOR + CHANGELOG.
2) Task de etapa 6 (TASK-00xx) bajo SPEC-0086 (ya cubre RF-10 kickoff y RF-12 multi-proyecto MVP-light).

## 3. Alcance Etapa 6 (lo que entrega)
- **Selector/dashboard multi-proyecto (read-only):** lista los repos-PRODUCTO bajo D:\Agentes\Zeus\
  (este front; futuros). Por proyecto, vista read-only del estado: HEAD/branch, sucio vs limpio, estado de
  CI. Lee el CANONICO (objetos git / origin), NO el working tree volatil (AC1/AC5).
- **NOVA:** aparece como entrada read-only en el selector (dir bajo Zeus). NO se lee su Area_comun (no-git).
  Etiquetada como instancia externa / no gobernada por este hub (hasta que un kickoff la registre, si aplica).
- **RF-10 kickoff:** lanzar un proyecto nuevo DESDE LA UI -> su primer handoff gobernado = T0 del proyecto,
  emitido via submit_intent (atomico, idempotente, con actor/timestamp). 0 bypass de gates/#4/drift. El
  `git init` del repo producto lo hace el operador; el front NO crea ruta de escritura nueva fuera de
  submit_intent.

## 4. Acceptance criteria (ademas de los ya verdes del SPEC)
- **AC11 (PERMANENTE, propiedad-tesis):** todo badge/indicador nuevo del selector (estado por proyecto, CI,
  canonico-vs-sucio) lleva TEST DE COMPORTAMIENTO: verificacion-runtime controlada -> render real; verif que
  falla / no-canonico / no verificable -> NO-verde (warn/danger/indeterminate); todo valido -> verde; texto
  libre SIEMPRE redactado. Nunca verde hardcodeado.
- validate_collaboration_state --root . exit 0 CON y SIN secretos (DECISION-0046); drift 0.
- **#4 epoca 1.14.0 INTACTA** (sin re-genesis; sin tocar config pinned).
- Neutralidad/acoplamiento (AC6): codigo SOLO en Zeus-protocol; cero producto en el core neutral; el front no
  escribe el protocolo salvo por submit_intent. scan_domain_neutrality limpio.
- CI de Zeus-protocol VERDE como gate de la etapa (AC7). Al cerrar, front ejecutable (`npm start`, :4173).

## 5. Proceso
Drafts/SDD primero -> pasada del Analista si aplica (honestidad de los indicadores nuevos) + pase de Codex
(codigo) -> ratificacion del operador -> promover por submit_intent. De a una pieza. Reproduccion del checker
(Arquitecto) desde clon limpio. Reportar en canonico.

## 6. Orden corta para pegar al Arquitecto
"Arquitecto: arranca la Etapa 6 del front (multi-proyecto MVP-light + kickoff RF-10) por el metodo, MODELO
HUB-CENTRICO. (1) Autora DECISION-0050 en Area_comun/decisions/ que fija el modelo: el selector lista repos-
PRODUCTO bajo D:\Agentes\Zeus\ leyendo su estado CANONICO read-only; la gobernanza/atestacion permanece en el
HUB UNICO (= dataset); RF-10 kickoff registra el T0 gobernado del proyecto nuevo EN EL HUB via submit_intent
sin bypass; acoplamiento unidireccional; MULTI-INSTANCIA/multi-hub EXPLICITAMENTE FUERA DE ALCANCE (posterior,
DECISION aparte, requeriria git-init de la instancia). Aditiva, neutral, SemVer MINOR + CHANGELOG. (2) Task de
etapa 6 bajo SPEC-0086: selector/dashboard read-only de proyectos bajo Zeus (HEAD/branch/sucio/CI por
proyecto, leyendo canonico no working tree) + RF-10 kickoff desde la UI (primer handoff gobernado = T0 via
submit_intent; el git init del repo lo hace el operador). NOVA (modernizacion legacy Dbsfinanciero; instancia
separada con su propio Area_comun, no-git; contiene Budget post-T0 PII-gated) aparece SOLO como dir read-only
y NO se lee su Area_comun. AC: AC11 badge-honesto/test-de-COMPORTAMIENTO PERMANENTE en todo indicador nuevo;
validate con/sin secretos exit 0; drift 0; #4 epoca 1.14.0 intacta; CI de Zeus-protocol verde; neutralidad
limpia; al cerrar `npm start` ejecutable. maker=Codex / checker=Arquitecto, de a una pieza, reproduccion desde
clon limpio. Drafts primero para mi ratificacion. Reporta en canonico."

## 7. Notas de cierre del MVP (alcance "front completo")
- Con etapa 6 cerrada, el front queda feature-complete para el operador (observar + operar + atestacion +
  multi-proyecto + kickoff). **Etapa 5 roster (RF-9) queda DEFERIDA** por 3.4 (sin agente que agregar):
  registrar esa deferral como recorte explicito del MVP-T0 en el cierre (no como pendiente abierto).
- Pendiente operacional aparte (no bloquea etapa 6): verificar que el push del remote de Zeus-protocol
  aterrizo (origin + HEAD 4d9f1b3; ojo rama local = `master`, no `main`).
