# PAQUETE - Decisiones de dominio P3.x pendientes para el Sello Etapa 2

> Preparado por el Arquitecto (DIRECTIVA operador 2026-07-06, item 3 de la cola PREP Sprint 1). Enumera
> las decisiones de dominio REALMENTE abiertas que bloquean el sello Etapa 2 (F3.2), con opciones y
> recomendacion, listas para que el Operador resuelva. Verificado contra `personal/operador/vision-nova/
> DECISIONES-DOMINIO-PENDIENTES-nova.md` (DD-01/02/03 YA RESUELTAS 2026-07-03 y horneadas en las SPECs,
> confirmado: cero marcadores "PENDIENTE/decidir/TBD" en `Area_comun/specs/nova/SPEC-NOVA-P3-*.md`) y
> contra `SELLO-ETAPA-1-nova-budget-DRAFT.md` s.3.

## Item unico genuinamente abierto: cierre de BR-C4 (autorizacion por operacion)

### Contexto
DD-01 (ya RESUELTA 2026-07-03) acepto para Sprint 1 el supuesto temporal "cualquier usuario
AUTENTICADO con rol presupuesto captura/aprueba/emite", difiriendo la matriz FINA por-operacion
(BR-C4: emitir != aprobar != anular) a POST-Sprint-1. Eso ya esta horneado en las 5 SPECs de la familia
P3 (P3-001..005).

Lo que sigue abierto NO es "que dice DD-01" (ya resuelto), sino: **la clasificacion de criticidad y
pertenencia al pool Q4 de P3.2/P3.3/P3.4 depende de si BR-C4 se cierra ANTES del sello Etapa 2
(29-jul)** (SELLO-ETAPA-1-nova-budget-DRAFT.md s.3: "P3.2/P3.3/P3.4 Drafts, elegibles al pool Q4 SI su
DEC cerrada al sello Etapa 2"). Si BR-C4 no cierra a tiempo, estas 3 unidades CAEN del pool Q4 (bajan
de "media condicional" a fuera de contraste) segun la regla ya sellada -- no es una decision nueva de
dominio, es la EJECUCION de una condicion ya declarada.

### La pregunta real para el Operador
No es "que politica de autorizacion adoptar" (eso ya se resolvio, DD-01). Es: **?BR-C4 (la matriz de
autorizacion por operacion, hoy sin sembrar en BD) es realista cerrarla antes del 29-jul, o se acepta
desde ya que P3.2/P3.3/P3.4 caen del pool Q4 por la condicion ya sellada?**

| Opcion | Consecuencia | Esfuerzo |
|---|---|---|
| (a) Confirmar AHORA que BR-C4 NO cierra antes del 29-jul (no hay trabajo de dominio/BD comprometido para sembrarla en esa ventana) | P3.2/P3.3/P3.4 caen del pool Q4 de forma PREVISIBLE (no sorpresiva) en el sello Etapa 2; el pool Q4 baja de n=10 a n=7, ya declarado como riesgo de subpotenciacion en el draft F3.2 del Asesor (s.2.2) | Ninguno -- es una confirmacion, no trabajo nuevo |
| (b) Comprometer el sembrado de BR-C4 en BD (DBA) antes del 29-jul, como trabajo de HARDENING (no de dominio) | P3.2/P3.3/P3.4 MANTIENEN su elegibilidad al pool Q4 con criticidad "media" (ya no condicional); n=10 se preserva | Depende del DBA -- requiere estimar el trabajo real de sembrar la matriz por-operacion (fuera de mi carril estimarlo, es trabajo de BD/dominio) |
| (c) Diferir la decision hasta mas cerca del 29-jul (dejar la condicion tal como esta sellada, sin adelantar el veredicto) | Riesgo de sorpresa tardia si BR-C4 no cierra a tiempo y el pool Q4 se reduce a ultima hora, sin margen para ajustar el plan de Sprint 1 | Ninguno ahora, pero mayor riesgo de proceso |

### Recomendacion del Arquitecto
**(a) o (b), NO (c).** El draft F3.2 del Asesor ya declara honestamente la subpotenciacion del pool Q4
como una limitacion aceptada del estudio (no invalida Q1/Q2, que son las confirmatorias fuertes); saber
AHORA si BR-C4 cierra o no permite planificar Sprint 1 con el n real desde ya, en vez de descubrirlo el
29-jul. Si el sembrado de BR-C4 no esta ya en marcha con el DBA, mi lectura es que **(a) es la opcion
realista** (no hay margen para comprometer trabajo de BD nuevo sin conocerlo hoy), pero la decision de
si intentar (b) es del Operador, que conoce la disponibilidad real del DBA para esa ventana.

## Verificacion negativa (no hay otros items de dominio P3.x abiertos)

Revise las 5 SPECs de la familia P3 (`P3-001` a `P3-005`) buscando marcadores de decision pendiente
(`PENDIENTE`, `decidir`, `TBD`, `por resolver`): **cero coincidencias**. DD-02 (minimo de caracteres del
objeto del RP) y DD-03 (default de referencia SECOP) tambien estan RESUELTAS y horneadas. Los items de
`DECISIONES-DOMINIO-PENDIENTES-nova.md` seccion 3 (brechas B-01/B-02/etc.) son HARDENING de BD, no
decisiones de dominio (ya clasificados asi por el Asesor, confirmado correcto en esta revision).

## Conclusion

El paquete de "DEC de dominio P3.x" se reduce a UN item real (BR-C4 timing), ya enmarcado arriba con
opciones + recomendacion. No hay decisiones de dominio nuevas escondidas en las SPECs ya escritas.

task_id: TASK-0246
status: prep-completo
executive_summary: Paquete de decisiones de dominio P3.x preparado para el Operador. Un solo item genuinamente abierto (timing de cierre de BR-C4, con efecto directo en la pertenencia de P3.2/P3.3/P3.4 al pool Q4 segun regla ya sellada); DD-01/02/03 confirmadas resueltas y horneadas, sin marcadores pendientes en las SPECs.
artifacts: Area_comun/artifacts/PAQUETE-DEC-DOMINIO-P3x-sello-etapa2.md
gates: N/A (documento de preparacion).
next_recommended: El Operador elige (a)/(b)/(c) sobre BR-C4; el Arquitecto registra la resolucion como enmienda fechada del sello si aplica.
risks: Ninguno -- solo lectura, no cambia ninguna SPEC ni el sello.
