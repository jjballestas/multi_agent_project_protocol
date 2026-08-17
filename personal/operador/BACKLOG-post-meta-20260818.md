# BACKLOG POST-META -- generado por el canal asesor, 2026-08-18 00:05 local

> META en curso (NO es parte de este backlog): veredicto 0414-r5 -> par
> reproducible -> tag v1.19.1 -> retransmision a NOVA -> retorno completo de
> NOVA. Este documento lista TODO lo que queda detras de esa meta, por bloques,
> con dueno, dependencias y senal-de-hecho.

## BLOQUE A -- Gobierno (firmas y permisos del operador humano)

A1. **Firmar o rechazar la DECISION camino-de-subida** (draft del Asesor,
    parado desde el 20-jul, RENUMERAR: 0104 ya es scratch-root en decisions/).
    Contenido al firmar: el generador de masters como mecanismo, el allowlist
    de exportacion como acto de promocion, R0 intacto (filtro, jamas
    disparador). Dueno: operador. Sin dependencias.
    Senal-de-hecho: DECISION-01XX en Area_comun/decisions/ con status accepted.

A2. **DECISION-lite por la clausula de poda borrada sin decision** (el vivo
    tumbo una clausula ratificada de TASK-0273 el 16-ago). Derogar o
    reformular CON la leccion que la falsifico (la ventana se abre sola; la
    barrera por mailbox quema un exec) -- NO reposicion ciega: TASK_PROTOCOL
    omite, no contradice. Dueno: Arquitecto redacta, operador firma.
    Es lo mas urgente del bloque y no depende de nada.
    Senal-de-hecho: DECISION-lite registrada + vivo y TASK_PROTOCOL coherentes.

A3. **DECISION-0119 (clave raiz offline, ceremonia fuera de banda)**. Sin
    reloj; solo el operador en persona. Senal-de-hecho: firma en decisions/.

A4. **Permiso de arnes para el taskkill del Arquitecto NOVA** (10 segundos en
    su ventana interactiva; la autorizacion de gobierno ya esta concedida y su
    RESP espera en su open/). Senal-de-hecho: los 10 PID zombis muertos y su
    RESP archivada.

## BLOQUE B -- Que la metodologia VIAJE (salida de la revision adversarial)

B1. **Master en el camino de entrega REAL** (D5, el techo de todo lo demas).
    upgrade_instance debe comparar el fichero que la instancia CONSUME
    (<gov>/.claude/skills/X/SKILL.md), no el staging del hub; classify() hoy
    solo casa rutas identicas. Dueno: tarea nueva, maker Codex.
    Depende de: nada tecnico; despues de la META por prioridad.
    Senal-de-hecho: el informe de upgrade de NOVA muestra fila comparando la
    skill consumida, con estado real (no "nuevo" espurio de staging).

B2. **Master = artefacto GENERADO** (sintesis de las dos revisiones; la unica
    forma de que la paridad de contenido tenga coordenada valida).
    build_skill_masters.py: lee vivos del ALLOWLIST, neutraliza (banner
    FRONTERA, placeholders de rutas/sha8), FALLA ante token de hub
    intraducible; CI corre --check como codigo generado. Incluye evaluar las
    5 skills vivas sin master (arquitecto-ledger-ops y cron-zombie-sweep son
    metodologia nuclear; pipeline-vision-nova y asesor-guarda-estado
    probablemente solo-hub: el allowlist lo decide).
    PROHIBICION transversal: nada toca protocol.config.json (genesis; medido
    dos veces). Depende de: A1 (el allowlist es el acto de promocion firmado)
    y B4. Senal-de-hecho: cp crudo del vivo al master -> CI exit 1.

B3. **TASK-0394 (GO ya dado a Codex esta noche)** -- conjunto adoptable por
    criterio, no por lista. Anadidos que salieron de la revision: comparar la
    ruta consumida (cruza con B1), prohibicion de tocar protocol.config.json,
    y el gemelo ps1 sin .githooks/** (residuo de TASK-0266, ya en su scope).
    Senal-de-hecho: crear fichero exportable en directorio no cubierto -> el
    control enrojece (su AC3).

B4. **Cerrar TASK-0410 ANTES de construir paridad nueva** (el gate de gemelos
    esta rojo y su cardinal ==91 fue desmentido como 92 por el Analista).
    Dueno: cola del maker. Senal-de-hecho: NEG-NEUTRALITY-IDENTITY-INVENTORY-
    PARITY verde en CI dos corridas.

B5. **Limpiar .agents/skills/** (4 skills, 0 versionadas, ~6 semanas rancias,
    invisibles a git). Borrar o .gitignore con decision explicita.
    Senal-de-hecho: git status sin ese espejo o regla que lo declare.

## BLOQUE C -- Higiene del arbol (plan aprobado 00:05, RESP en open/)

C1. **Lote unico de Codex**: reglas .gitignore de recibos (3 patrones) +
    MUESTRA verificada que INCLUYA recibos de intents RECHAZADOS (el
    subconjunto con mas papeletas de no reconstruirse desde events.jsonl; si
    alguno no se reconstruye, esa familia va a commit historico) + commitear
    los 7 .md de evidencia + mover task0294_attested/ (CLAVES dentro) a
    D:/Aegis_Scratch/protocol/fixtures/ SIN commitear.
    Senal-de-hecho: personal/Codex sin untracked salvo ignorados.

C2. **Pre-commit deny-pattern para material de firma** (*.key, *.pem, patron
    real de claves eventauth) en rutas commiteables. El "ni por descuido" se
    cablea, no se promete. Senal-de-hecho: intento de commit de un .key de
    prueba -> pre-commit lo rechaza.

C3. **Drenajes restantes**: Arquitecto 53 (su checkpoint), canal operador 46
    (lo drena el Asesor en ventana quieta), Analista 5.
    Senal-de-hecho: censo por dueno ~0 untracked no ignorado.

C4. **Poda PRUNE DUE** (cold_start >= 20000 avisado por el hook) + limpiar
    entradas exhausted consumidas de los retry.json (Analista: ADENDA2 y
    REVIEW-0378 del 14-ago; Codex: GO-0337, r4b, r5, y la de r5b si quedo
    huerfana tras el archivado -- archivar no desencola).
    Senal-de-hecho: prune verde + retry.json sin entradas de mensajes
    archivados.

## BLOQUE D -- NOVA post-retorno

D1. **Reemitir GO-28-9432-SONDA con ID NUEVO** tras la adopcion del corte (su
    retry esta agotado y no se reprocesa; ya autorizado). Dueno: Arquitecto
    NOVA. Senal-de-hecho: 9432 en curso con mensaje nuevo consumido.

D2. **Espejo v3 de metodologia a NOVA** (DECISION-0117 prioridad sustrato +
    0118 trailer de actor, como decisiones SUYAS) UN DIA despues de su retorno
    completo. Dueno: canal asesor + Arquitecto NOVA.

D3. **Watchdog de ausencia en NOVA al relanzar peers** (15min/3 + alerta
    exhausted; alli hoy solo hay vigias de eventos). Dueno: Arquitecto NOVA.

D4. **Post-incidente causa raiz del borrado de claves eventauth v1** (sin
    prisa, declarado por su Arquitecto).

D5. **9441 (shell del front)**: el operador lo trata directamente con el
    Arquitecto NOVA (fuera del canal asesor salvo orden).

## BLOQUE E -- Colaterales del hub en vuelo esta noche

E1. **Veredictos pendientes del Analista**: 0378-r5 (en curso), 0397, 0408,
    0414-r5 (camino critico). Cada veredicto -> cierre o remediacion por el
    Arquitecto. Senal-de-hecho: tareas a done con veredicto independiente.

E2. **TASK-0408 (alertas durables de encargos muertos)**: cuando su review
    pase, verificar POR CONDUCTA que cubre el hueco entre-sesiones del canal
    asesor (la leccion de las 5 horas: el vacio entre sesiones no tiene
    instrumento). Senal-de-hecho: alerta persistida visible en frio tras un
    RETRY_EXHAUSTED simulado.

## BLOQUE F -- V3 del debate de metodologia (aprobada 16-ago; estado real en ledger)

Verificado 2026-08-18 00:12: D-B YA SELLADA -- DECISION-0117 (trailer de actor)
y DECISION-0118 (prioridad de sustrato auditada) con status accepted. La
semana 0 YA REGISTRADA con dos tareas en ready, owner Codex.

F1. **TASK-0412 -- preflight de intake con dientes** (ready). Primera de la
    semana 0. Encolar tras 0394/0410 en la cola del maker.
    Senal-de-hecho: veredicto independiente + preflight enrojeciendo ante un
    intake defectuoso real.

F2. **TASK-0413 -- panel de metricas M7/M8** (ready). Segunda de la semana 0.
    Senal-de-hecho: panel poblado con datos reales de la instancia.

F3. **Cableado de DECISION-0117**: verificar si el trailer de actor ya tiene
    dientes (un gate que lo LEA) o si esta decidido pero no cableado -- la
    leccion que la motivo es "identidad de git no es identidad de gobierno"
    (user.name = Codex para los tres). Si no hay gate, es tarea nueva.
    Senal-de-hecho: commit sin trailer de actor valido -> gate rojo.

F4. **P6 condicionada / P7 diferida / P5 retirada**: P6 solo se activa si se
    cumple su condicion registrada (verificar contra la DIRECTIVA 48bf524c
    antes de activar); P7 no se toca salvo orden del operador; P5 muerta.

F5. **DECISION-0118 gobierna el ORDEN de este backlog**: la prioridad de
    sustrato es auditada -- los bloques B y F (sustrato) reclaman prioridad
    sobre colaterales de producto al encolar al maker. Aplicarla al secuenciar
    y dejar el rastro de auditoria que la decision exige.

## Notas de orden

- A2 es lo mas urgente de todo el documento y no depende de nada.
- B1 va antes que B2 (arreglar paridad sin arreglar entrega = el verde caro).
- B4 es precondicion dura de B2.
- C1/C2 caben en cualquier ventana quieta; no compiten con la META.
- Cola del maker post-META, con la prioridad de sustrato de DECISION-0118:
  0394 (ya GO, entro en la META) -> 0410 (B4) -> 0412 -> 0413 -> B1 -> B2.
- ACTUALIZACION 00:12: TASK-0394 SALIO de este backlog -- el Arquitecto midio
  que el conjunto adoptable no transporta la D-1 de NOVA y la metio como
  bloqueante del tag (GO 69eaffde). Queda reflejada solo como B3 historico.
- Los IDs de tarea del harness (sesion asesor): 9-14 cubren E/C4/B/A parcial;
  este documento es la vista detallada y canonica.
