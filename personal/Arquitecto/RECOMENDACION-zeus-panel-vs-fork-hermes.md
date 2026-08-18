# RECOMENDACION (brutalmente honesta): panel Zeus -- seguir Zeus-protocol; congelar el fork Hermes (Zeus-Aegis)
# 2026-07-14 ~03:55 local. Pedida por el operador en chat. La decision es del operador; esto es mi recomendacion
# con la evidencia delante. NO es una DECISION de ledger.

## Recomendacion

**Seguir con Zeus-protocol como linea del panel/producto. Congelar Zeus-Aegis (el fork de Hermes)
como referencia de UI y cumplimiento MIT ya hecho -- no borrarlo, no desarrollarlo.**

## La evidencia (verificada hoy sobre los repos y tus propios documentos)

| Hecho | Zeus-protocol | Zeus-Aegis (fork Hermes) |
|---|---|---|
| Commits | 102 | 73 |
| Ultima actividad | 2026-07-07 (TASK-1109, deteccion de ambiguedad) | 2026-07-02 (remediacion de branding) |
| Que contiene | src/ + tests/ + design/ + docs/; architect-bridge (consola DECISION-0062/0063), extractors, file-ingestion, registro de excepciones, matriz de ambiguedad (el trabajo anti-vibecoding TASK-11xx) | vendor/ (app Hermes rebrandeada), LICENSE/NOTICE MIT, DECISION-0082 allowlist de marca, logs de smoke en la raiz |
| Dependencias | 0 (vanilla) | stack Next.js/React vendored (el analisis del 26-jun: Hermes es ~99% UI JS/TS) |
| Historia operativa | gates estables | npm test colgante = causa raiz documentada de los cron-jams (memoria: cron-jam-root-cause) |

Tu propio analisis (26-jun, personal/operador/analisis_protocolo_vs_hermes.html) ya lo dijo con
precision: "tu activo defendible NO es la UI; es el protocolo de gobernanza + runtime atestiguado
que Hermes no tiene". Hermes = cabina madura (chat, terminal, memoria, skills, PWA; 5.7k stars,
MIT, de Nous Research); nuestro foso = control-plane. No compiten: encajan.

## Por que NO seguir el fork (las 5 razones, en orden de peso)

1. **El foso es el control-plane y es 100% in-house en AMBAS rutas.** El fork solo compra chrome
   (chat/terminal/PWA/layout). El PANEL que la metodologia necesita (DECISION-0050 p.4: operar y
   observar -- mailbox, estado, ledger/atestacion, GOs, lanzar agentes, multi-proyecto) es
   dashboards + acciones gobernadas via submit_intent. Nada de eso viene en Hermes; TODO eso hay
   que construirlo igual en las dos rutas. El fork no acorta el camino de lo que importa.

2. **Doble cerebro: la MISMA clase de conflicto que ya mataste con Engram.** Hermes trae SU
   memoria, SUS skills (2000+), SU orquestador (Conductor/Swarm). Nosotros tenemos ruta UNICA de
   memoria (DECISION-0081, sellada hace 12 dias), skills gobernadas (DECISION-0061) y orquestacion
   con capabilities + ledger. Mantener el fork vivo = arbitrar permanentemente que capa manda en
   cada feature, o desactivar la mitad de Hermes (y entonces que compraste?). Ya decidiste una vez
   que doble-backend con drift no se paga (DECISION-0081); esto es el mismo patron con mas
   superficie.

3. **El impuesto del fork es permanente y ya lo pagaste 3 veces en 2 semanas.** Upstream Hermes
   se mueve rapido (v2.3.0 may-2026, origen hackathon, release cada pocas semanas). Cada feature
   futura que quieras de upstream = re-merge contra tu rebranding (ya costo 3+ commits de
   remediacion "clear Hermes copy") + tus parches de gobernanza. Y el arbol node del fork ya
   causo dano operativo real (cron-jams por npm test colgante, 4 huecos de harness documentados).
   Con el equipo actual (tu + el trio, con NOVA/TFM hasta el 30-jul y las 6 unidades despues),
   ese impuesto sale directo del camino critico.

4. **Velocidad revelada.** En las mismas 2 semanas: Zeus-protocol recibio el trabajo REAL del
   producto (ambiguedad, excepciones, consola) hasta el 7-jul; el fork quedo parado en branding
   el 2-jul. El equipo vota con los commits: la linea productiva es Zeus-protocol.

5. **Coherencia de identidad.** El producto (DECISION-0084) es anti-vibecoding para
   desarrolladores profesionales: interrogacion de requisitos, quality panel, excepciones
   auditadas. Un artefacto de esa identidad se audita facil: deps minimas, superficie conocida.
   Un megafork vendored de un workspace de hackathon es exactamente lo contrario del pitch.

## El contra-lado honesto (que pierdes y cuando el fork ganaria)

- Pierdes MESES de chrome ya pulido: PWA/movil, chat multi-modelo, terminal en browser, layout
  bonito. Si el objetivo CERCANO fuera un demo vendible de "workspace de agentes" para terceros,
  el fork llega antes a la primera impresion. Ese no es el objetivo declarado del panel hoy.
- Tu plan de integracion del 26-jun ("su UI sobre tu metodologia", puerto de vistas de gobernanza
  al fork con /api/governance/*) era SANO en el papel y sigue siendo la arquitectura correcta SI
  algun dia se retoma el fork: la conclusion de hoy no invalida ese diseno, invalida su COSTO DE
  OPORTUNIDAD con este equipo y esta ventana.
- Si mas adelante el panel necesita chat/terminal/movil, la opcion barata NO es revivir el fork
  entero: es tomar componentes puntuales (MIT lo permite, con sus avisos) o re-evaluar entonces.

## Que hacer con Zeus-Aegis (si aceptas la recomendacion)

1. CONGELAR: README de una linea declarando estado (referencia de UI + cumplimiento MIT hecho +
   DECISION-0082 allowlist), sin builds ni crons apuntandole.
2. Limpiar los logs de smoke de la raiz (higiene, 1 commit).
3. Las lecciones/UX que gusten de Hermes se toman como REFERENCIA de diseno para las vistas de
   Zeus-protocol (mirar, no mergear).
4. La gobernanza sigue donde esta: Zeus-protocol-Aegis gobierna Zeus-protocol; el fork congelado
   no necesita instancia viva.

## Nota de alcance

Esto NO entra al ledger como decision mia: es insumo. Si decides, la DECISION del producto la
sella su instancia (Zeus-protocol-Aegis) o el hub segun donde corresponda, con tu GO.
