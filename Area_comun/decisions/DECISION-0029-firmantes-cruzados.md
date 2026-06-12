---
decision_id: DECISION-0029
title: Firmantes cruzados sin consenso - firma por agente + prev_hash + anclaje externo (atestacion de autoria con adversario explicito)
status: accepted
date: 2026-06-12
ratified_at: 2026-06-12
deciders: [operador humano, Claude (architect)]
supersedes: []
superseded_by: []
relates_to: [DECISION-0015, DECISION-0017, DECISION-0022, DECISION-0023, DECISION-0028]
phase: P2
---

# DECISION-0029 - Firmantes cruzados sin consenso (politica; implementacion off-by-default)

> ACCEPTED por el operador (2026-06-12, "yo apruebo los firmantes cruzados") y promovida al ledger por
> Claude el mismo dia. Aprueba la POLITICA y habilita encolar TASK-0101..0103. La ACTIVACION en la
> instancia viva sigue el patron DECISION-0022/0024: cada pieza se construye apagada (off-by-default,
> opt-in por instancia) y su encendido exige SPEC cerrada + golden cases verdes + aprobacion explicita
> posterior del operador. SemVer: MINOR cuando se libere. Nucleo neutral de dominio: sin cambios de
> frontera de dominio.

## Contexto

El eventlog actual autentica con HMAC simetrico cuya clave posee el runtime, sin encadenado prev_hash
(runtime v0.11.0). El runtime es ademas el escritor unico del estado (DECISION-0022/0028). Consecuencia:
quien produce el registro es quien lo autentica (auto-atestacion). Para que la atestacion de autoria por
agente (linea de investigacion G3.1 del caso de estudio loops_agenticos; analisis externo en
`01_Sources/Documents/02_Modelo_de_Amenaza_G3.1.md` de ese caso) tenga una propiedad de seguridad
verificable, debe existir al menos un actor capaz de mentir cuya mentira el mecanismo detecte. La revision
critica de 2026-06-12 detecto ademas una contradiccion: la lista de NO-hacer del plan excluia los
mecanismos multipartitos en bloque, eliminando de raiz a los adversarios que dan valor a la atestacion.

## Decision

1. **Distincion normativa.** Queda PROHIBIDO (sin cambio): consenso BFT/SMR/CRDTs, replicacion multi-nodo,
   modelo trustless, tokenomics. Queda ADOPTADO (nuevo): **multiples firmantes independientes SIN
   consenso** - cada firmante atesta unilateralmente; el orden lo sigue fijando el escritor unico. La
   distincion es entre "decidir juntos" (prohibido, innecesario) y "no poder falsificarse mutuamente"
   (necesario). Esta decision NO cambia el modelo operativo single-writer.
2. **Tres piezas tecnicas** (cada una off-by-default, flag propio, opt-in por instancia):
   a. **prev_hash encadenado** en el eventlog: `hash_n = SHA256(evento_n || hash_{n-1})`, manteniendo el
      HMAC actual como capa de compatibilidad. Hace detectables borrado y reordenamiento, no solo
      alteracion puntual. (TASK-0101)
   b. **Firma por agente**: cada agente del `agent_registry` posee material de firma propio (Ed25519
      local o identidad keyless; backend configurable, vendor-neutral como en DECISION-0023). Los turnos
      y handoffs relevantes para autoria llevan atestacion firmada por el agente productor (sujeto: hash
      del artefacto; predicado: agente, modelo-version, tarea, decision habilitante, trust_boundary de
      insumos; formato compatible in-toto). El runtime almacena y encadena las atestaciones pero NO puede
      producirlas. La revision maker!=checker existente se registra como atestacion firmada del revisor.
      (TASK-0102)
   c. **Anclaje externo periodico**: el digest de cabeza de la cadena se publica con frecuencia
      configurable en al menos un medio fuera del control de escritura del runtime (remoto git
      independiente, log de transparencia, o sellado RFC 3161; backend configurable). (TASK-0103)
3. **Propiedades objetivo y limites declarados.** Con 2a+2b+2c el ledger es tamper-evident frente a:
   manipulacion post-hoc (A1), suplantacion de autoria entre agentes (A2) y fabricacion/reescritura por el
   runtime de historia anclada (A3-restringido). RIESGO RESIDUAL DECLARADO: omision de eventos aun no
   anclados por el runtime (mitigacion parcial: ventanas cortas + atestaciones huerfanas del revisor).
   NO-OBJETIVOS: integridad bizantina, disponibilidad, demostracion criptografica de identidad de modelo,
   operador humano malicioso. Toda afirmacion de seguridad en docs/specs debe citar la clase de adversario
   que cubre; sin clase asignada, no se afirma.
4. **Regla de entrada.** Cada TASK exige SPEC con acceptance_criteria + test_plan + golden cases antes de
   GO (sdd_required). Orden: TASK-0101 primero (base de encadenado); 0102 y 0103 dependen de 0101.
5. **Sin secretos en el repo** (sin cambio de boundary): claves privadas de agente viven fuera del repo
   (wrapper de cada agente); al repo solo entran claves publicas/identidades y atestaciones.

## Consecuencias

- G3.1 pasa de "logging firmado" a "atestacion con adversario explicito" - prerrequisito de la via de
  investigacion del caso loops_agenticos, y feature de auditoria valiosa por si misma para instancias.
- El coste (tokens/latencia/bytes) entra en el presupuesto medible; el caso de estudio lo evaluara como
  hipotesis H2 con umbrales pre-registrados.
- DECISION-0023 (firma de release) queda complementada: la firma del release atesta el artefacto final;
  esta decision atesta la autoria de los cambios que llegan a el.

## Alternativas consideradas

- Mantener HMAC unico (status quo): conserva la auto-atestacion; descartada por valor probatorio nulo.
- Consenso BFT: resuelve un problema (acuerdo distribuido trustless) que el modelo single-operator no
  tiene; coste y complejidad injustificados; sigue prohibido.
- Solo prev_hash sin firma por agente: protege contra A1 pero no contra A2/A3; insuficiente para G3.1.
