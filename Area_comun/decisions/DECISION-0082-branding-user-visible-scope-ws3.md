---
decision_id: DECISION-0082
title: "Definicion precisa de 'branding user-visible' para el gate de WS3 (TASK-0229): el gate cubre SOLO la superficie renderizada al usuario final del app shipped; el resto va a allowlist etiquetada verificada por el checker (no cero-grep)"
status: accepted
date: 2026-07-02
deciders: [operador humano (eleccion explicita 2026-07-02 via pregunta del Arquitecto), Arquitecto]
supersedes: []
superseded_by: []
relates_to: [DECISION-0076, DECISION-0077, DECISION-0079, REQ-ZEUS-001]
phase: P2
scope: product (Zeus-Aegis, TASK-0229 WS3)
approval_ref: "Operador eligio la opcion 'Redefinir user-visible + acotar AC' ante 4 NO-GO consecutivos de TASK-0229"
---

# DECISION-0082 - Alcance de 'branding user-visible' para el gate de WS3

> Contexto: TASK-0229 (WS3 branding white-label, DECISION-0076) acumulo 4 NO-GO en whack-a-mole. En cada ronda
> npm test / shim ZEUS_* / build / gates de protocolo pasaban; el bloqueo era que `git grep -i hermes` sobre
> `vendor/hermes-2.3.0/src/**` + `electron/server-bundle.cjs` seguia hallando cadenas Hermes. Causa: `vendor/src`
> es el producto upstream completo, pervasivamente marcado "Hermes"; rebrandear string-por-string a mano (a) no
> converge y (b) choca con preservar el merge upstream (DoD punto 4). El operador eligio acotar la definicion de
> "user-visible" en vez de seguir el barrido ciego o un transform de build-time. Mismo patron que DECISION-0079
> (acotar una frontera en disputa a algo verificable). Scope de producto; no toca el core neutral ni los templates.

## Decision

1. **Frontera del gate (AC de TASK-0229).** Una cadena `hermes` es una **fuga de marca** (gatea NO-GO) si y solo si
   se **RENDERIZA/MUESTRA al usuario final** en el app **distribuido (shipped)**, en alguna de estas superficies:
   - Texto visible de la UI (JSX renderizado, labels, titulos, botones, i18n/copy mostrado en pantalla).
   - Onboarding / setup mostrado en pantalla.
   - Ayuda / uso / salida de CLI impresa al usuario al correr el app shipped.
   - Mensajes de error / toast / notificacion MOSTRADOS en la UI.
   - URLs / enlaces / paths user-facing mostrados o navegados en la UI (p.ej. `~/.hermes` si se muestra).

2. **Fuera del gate (allowlist).** NO es fuga (no gatea) y va a la allowlist etiquetada:
   - Identificadores de codigo (nombres de funciones/variables/tipos), imports, nombres de paquete/modulo.
   - Comentarios del source.
   - Logs de debug/dev **no surfaceados** al usuario final en el build shipped.
   - Fixtures de test no distribuidos.
   - NOTICE / LICENSE MIT y atribucion / provenance a NousResearch exigida por licencia.
   - Nombres de env `HERMES_*` del shim de compatibilidad.

3. **Metodo del gate (checker).** El AC deja de ser `git grep -i hermes == 0`. Pasa a: el maker (Codex) entrega
   una **ALLOWLIST ETIQUETADA** -- por cada hit `hermes` que quede, una etiqueta del conjunto {identificador |
   import | comentario | dev-log-no-surfaceado | test-fixture | licencia-provenance | env-shim}. El checker
   (Analista) declara **CERRABLE** si (a) NINGUN hit user-**renderizado** (superficie del punto 1) queda sin
   rebrandear a Zeus, y (b) NINGUNA etiqueta de la allowlist es falsa (un string que SI se muestra al usuario
   etiquetado como interno). La **carga de la prueba** de "no se renderiza" es del maker: debe poder trazar el hit
   a que no llega a una superficie del punto 1. Ambiguedad genuina se resuelve a favor de rebrandear.

4. **Sin cambio del resto del DoD de TASK-0229.** Se mantienen: shim ZEUS/HERMES funcionando, `npm test` verde por
   EXIT en clon limpio, binarios/appId/paquetes NO renombrados (merge upstream), NOTICE MIT intacto, bundle
   regenerado desde el src (no editado suelto).

## Consecuencias

- El objetivo se vuelve **finito y convergente**: la superficie renderizada es acotada; el maker la rebrandea y
  etiqueta el resto; el checker verifica etiquetas (spot-check de que ningun string mostrado quede mal etiquetado),
  en vez de perseguir cada hit del grep sobre codigo interno vendorizado.
- Preserva el merge upstream: los strings internos no-renderizados de `vendor/src` no se tocan.
- Si en el futuro se quisiera cero-Hermes TOTAL (incluido interno), seria un rebrand de build-time (transform al
  generar el bundle) como decision aparte; queda FUERA de TASK-0229 por esta decision.

## Aprobacion

Operador humano (John Ballestas), 2026-07-02, eligio explicitamente "Redefinir user-visible + acotar AC" entre las
opciones que el Arquitecto planteo ante los 4 NO-GO. El Arquitecto formaliza y ejecuta.
