# DRAFT (personal, NO publicado) - Endurecimiento badge-honesto: test de comportamiento

> Preparado en ventana de espera (DECISION-0020 #1). NO publicar a Area_comun hasta GO del operador
> sobre la secuencia (mensaje GO-front-completo-disenador, mi respuesta confirma-front, rr=true pendiente).
> Origen: recomendacion del Analista (MSG-20260620-Analista-to-Arquitecto-TASK-0128-recomendacion).

## Por que (problema)
El `staticContract.test.js` de Zeus-protocol prueba PRESENCIA (string-match: que el codigo contiene
`validate_chain`, `signature verified`, `[redacted - PII de tercero]`, etc.), NO COMPORTAMIENTO. Un refactor
que conserve los strings pero rompa el cableado (p.ej. un badge que se repinte verde pese a una verificacion
fallida) pasaria el test igual. El badge-honesto es ahora AC DURO de todo el front -> la propiedad debe quedar
regresion-proof, no descansar en revision de codigo.

## Que (alcance, pieza chica, producto Zeus-protocol)
Test de COMPORTAMIENTO que inyecta un runner/llamada-runtime controlado y asevera el render:
- chain.valid=false  -> badge cadena NO-verde (warn/danger), `attested` = false.
- event_auth con un item invalido -> badge event-auth NO-verde, `attested` = false.
- anchor invalido / drift has_drift=true / validator no-ok -> `attested` = false (no verde).
- source.state != "canonical" (working_tree) -> chip canonico NO-verde (warn), aunque todo lo demas verifique.
- TODO valido (chain/sig/anchor/event_auth ok + drift false + validator ok + source canonical) -> atestado VERDE.
- runtime no verificable (sin secretos / sin entries) -> badge "indeterminate" (warn), NUNCA verde.
- PII: payload con texto -> preview SIEMPRE "[redacted - PII de tercero]" (positivo y negativo).

Las funciones ya son inyectables: `loadRuntimeVerification` acepta runner (execFile) inyectable; la derivacion
de `app.js` (`attested = validatorOk && driftOk && chainOk && agentSignaturesOk && anchorOk && eventAuthOk`,
`sourceClean = state==='canonical'`, `variant = valid===true?ok:valid===false?danger:warn`) es testeable con un
modelo fake. Extraer la logica de derivacion de badge a una funcion pura testeable si hace falta (sin cambiar
comportamiento) - refactor minimo, cubierto por el propio test.

## AC (criterios de aceptacion)
1. Test de comportamiento agregado (node --test) que cubre los casos arriba (falla->no-verde; valido->verde;
   indeterminado->warn; PII siempre redactado). Falla si se repinta verde una verificacion fallida.
2. La logica de derivacion del badge NO cambia su comportamiento observable (mismo render que hoy en el caso
   canonico vivo). Refactor a funcion pura permitido si queda cubierto.
3. node --test verde (>= los 11 actuales + nuevos), gateado por EXIT REAL.
4. Read-only intacto: ninguna ruta de escritura nueva.
5. Gates protocolo: validate con/sin secretos exit 0; drift 0; scans exit 0. Epoca 1.14.0 pinned.
6. maker=Codex / checker=Arquitecto (o Analista); reproduccion desde clon limpio.

## Gobernanza
- SPEC: delta a SPEC-0086 (AC PERMANENTE "test de comportamiento del badge" para etapas con badges) +
  task de producto (no reabre TASK-0128). Codigo en Zeus-protocol; cita en Area_comun (dataset).
- AC PERMANENTE para etapa5/6: toda pieza nueva con badges trae su test de comportamiento, no solo string-match.

## Pendiente del operador (antes de publicar)
- (b) secuencia: esta pieza PRIMERO (recomendado) o plegada como primer sub-AC de etapa5.
- Si va como pieza propia: asignar TASK-id siguiente y GO a Codex.
