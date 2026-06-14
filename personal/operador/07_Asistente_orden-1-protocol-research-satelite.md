# 07_Asistente - Orden #1 / protocol_research (satelite: estructura + scaffolding)

> Insumo del operador (asistente Cowork) para el ARQUITECTO (Claude en VS Code).
> El asistente no redacta la DECISION ni muta estado: esto es el brief de requisitos.
> Fecha: 2026-06-14. Estado de partida: v1.7.0, en reposo. #3 ACTIVO, #4/chain-auth OFF, SA.4 OFF.
> Decision del operador: montar el satelite COMPLETO, acotado a "estructura + scaffolding"
> (NO corre experimentos, NO publica; lo gateado queda OFF/stub).

## 1. Objetivo
Montar `protocol_research/` como repo satelite READ-ONLY del Core, con:
- Acoplamiento UNIDIRECCIONAL: lee el eventlog + decisiones del Core como datos; NUNCA escribe al Core.
- #1: dataset MAST-sobre-historial-propio (reusa FAILURE_MODES.md), versionado, INTERNO.
- Scaffolding (stubs OFF) de: exporter #2 (PROV), feed #3 (cost-attribution -> research), harness de
  ablacion, espacio TFM.
- Todo lo gateado marcado OFF/stub con su gate nombrado. NO corre experimentos, NO publica.

## 2. Entra por el metodo (en el Core)
DECISION-00xx en `Area_comun/decisions/` que autoriza el satelite: documenta el acoplamiento unidireccional,
nombra los gates como hard-stops (GATE-DATASET legal, GATE-INST institucional, PRE-REG) y el alcance de #1.
Aditiva, neutral. SemVer MINOR + CHANGELOG (cambio visible: el Core referencia un satelite).
maker!=checker (TRES lentes que NO se solapan -- no es sobre-esfuerzo, es division de superficies):
- Arquitecto = maker (redacta DECISION + estructura).
- ANALISTA = honestidad/metodologia de #1 (comparabilidad como limite, sin overclaim) + gates + neutralidad.
- CODEX = invariante de codigo: acoplamiento DEMOSTRABLEMENTE read-only + stubs inertes + solidez estructural.
  Como el arquitecto construye la estructura, su checker de codigo es Codex (no se revisa a si mismo).
Flujo: drafts -> pasada del analista (honestidad) + pase de Codex (codigo) EN PARALELO -> ratificacion del
operador -> promover por submit_intent.

## 3. protocol_research/ (repo SEPARADO, no dentro del Core)
- Repo propio (hoja de ruta §2: UN SOLO REPO CORE sin forks; el satelite es separado y read-only). Sugerencia
  de ubicacion: hermano del Core (p. ej. D:\Agentes\protocol_research) -- el arquitecto/operador confirma.
- Acoplamiento: mecanismo que LEE el eventlog/decisiones del Core sin poder escribir (read-only por diseno).
  El arquitecto elige el mecanismo (submodulo / clone read-only / export programado), pero la propiedad
  INNEGOCIABLE es: protocol_research NUNCA muta el Core.
- README documentando: coupling unidireccional, los 3 gates, y que esta OFF/stub.

## 4. #1 - dataset MAST-sobre-historial (interno)
- Reusa FAILURE_MODES.md: exporta los modos + incidentes del protocolo a un formato de dataset versionado.
- Sobre el historial PROPIO del protocolo (handoffs fallidos, drift, colisiones) -- sin PII de produccion ->
  NO requiere GATE-DATASET para uso INTERNO.
- HONESTIDAD (lente analista, innegociable): la comparabilidad 1:1 con MAST-Data se REPORTA como limite, no se
  asume; NO afirmar "dataset citable" (queda condicionado a GATE-DATASET); cero numeros no medidos;
  severidad/frecuencia no se cuantifican. Coherente con la frontera ya fijada en FAILURE_MODES.md (v1.7.0).

## 5. Scaffolding gateado (stubs OFF, NO ejecutan)
- Exporter #2 (PROV-AGENT, eventlog -> W3C PROV): interfaz/stub documentado, OFF. Gate: GATE-DATASET (produccion).
- Feed #3 (cost-attribution -> research): interfaz/stub, OFF. Gate: GATE-DATASET.
- Harness de ablacion + TFM (H1/H2/H3, PRE-REG): esqueleto/stub, OFF. Gates: GATE-INST + PRE-REG + volumen real.
- Cada stub: placeholder NO ejecutable, con su interfaz + su gate nombrado. Sin captura de datos, sin corridas.

## 6. Restricciones (innegociables)
- Acoplamiento unidireccional: protocol_research NUNCA escribe al Core.
- Nada de GATE-DATASET / GATE-INST / experimentos / publicacion en esta tarea (solo estructura + stubs).
- El Core sigue neutral; #3 ACTIVO, #4/chain-auth OFF, SA.4 OFF -- intactos.
- DECISION en el Core por submit_intent (escritor unico); SemVer MINOR + CHANGELOG. El repo satelite lleva su
  propio versionado.

## 7. Orden corta para pegar al arquitecto
"Arquitecto: monta el satelite #1/protocol_research acotado a ESTRUCTURA + SCAFFOLDING (no corre nada, no
publica). Por el metodo: DECISION en el Core (Area_comun/decisions/) que autoriza el satelite read-only,
documenta el acoplamiento UNIDIRECCIONAL (lee Core, NUNCA escribe), nombra los gates como hard-stops
(GATE-DATASET / GATE-INST / PRE-REG) y el alcance de #1; aditiva, neutral, MINOR + CHANGELOG. Crea
protocol_research/ como repo SEPARADO read-only (ubicacion hermana del Core, confirma conmigo): (a) #1 =
dataset MAST-sobre-historial-propio reusando FAILURE_MODES.md, versionado, INTERNO, con comparabilidad a
MAST-Data REPORTADA como limite y SIN afirmar 'citable' (eso depende de GATE-DATASET); (b) stubs OFF y NO
ejecutables de exporter #2 (PROV), feed #3 (cost-attribution) y harness de ablacion/TFM, cada uno con su gate
nombrado; (c) README del coupling + gates. Drafts primero para la pasada del analista (honestidad de #1 +
gates) y mi ratificacion. NO toques #3/#4/SA.4; neutralidad estricta; protocol_research NUNCA muta el Core.
Reporta los drafts."

## 8. Pase del ANALISTA (honestidad/metodologia, cuando existan drafts, antes de ratificar)
"Analista: UNA pasada adversarial acotada sobre los drafts de #1/protocol_research, ANTES de ratificar. Lente
honestidad/metodologia, no ingenieria. Falsable, vuelve como artefacto. Proporcional (es estructura+stubs).
Responde por punto PASA / CAMBIO REQUERIDO (falsable) / RIESGO DECLARADO:
1) Honestidad de #1: comparabilidad con MAST-Data reportada como LIMITE (no asumida) y sin 'citable'/empirico.
2) Acoplamiento: ¿el diseno garantiza que protocol_research NO puede escribir al Core?
3) Gates: cada stub (#2/#3/ablacion) OFF, no ejecutable, citando su gate (GATE-DATASET/GATE-INST/PRE-REG).
4) Neutralidad: ¿el satelite, al leer datos del Core, arrastra dominio o rompe la neutralidad del Core?
FUERA DE ALCANCE: estilo, mecanica fina. Entrega: veredicto breve por punto."

## 9. Pase de CODEX (invariante de codigo, EN PARALELO al analista, antes de ratificar)
"Codex: revision de codigo acotada sobre los drafts de #1/protocol_research, antes de la ratificacion del
operador. Solo el invariante estructural, no estilo ni metodologia. Responde PASA / FALLA (con repro) por punto:
1) Acoplamiento UNIDIRECCIONAL: ¿el mecanismo (submodulo/clone/export) garantiza que protocol_research NO puede
   escribir al Core? Busca UNA ruta de escritura al Core; si existe, reportala con repro.
2) Stubs inertes: ¿los stubs de #2 (PROV), #3 (cost-feed) y el harness de ablacion estan OFF y NO ejecutables?
   ¿Alguno puede correr o capturar datos sin pasar su gate? Nombra cual, o confirma que ninguno.
3) Solidez estructural: ¿la lectura del eventlog/decisiones del Core es robusta (no rompe si el Core avanza)?
FUERA DE ALCANCE: honestidad de #1 (eso lo ve el analista), redaccion. Entrega: veredicto por punto + repro de
cualquier FALLA."
