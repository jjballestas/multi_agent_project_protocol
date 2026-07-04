# BRIEF para revision legal -- consentimiento y manejo de datos del estudio Nova

> Autor: Asesor (Vision Nova). Carril: study-integrity + cumplimiento. Estado: BRIEF para que el Operador
> lo revise y lo reenvie a su area legal. NO es dictamen legal; enmarca las preguntas para que legal
> responda eficiente. Fecha: 2026-07-04.
> Marco normativo objetivo: Ley 1581 de 2012 (Colombia, habeas data) + RGPD (referencia comparada,
> Considerando 26 sobre seudonimizacion). Anclas tecnicas: SPEC-0079 C3 (subject_hash = SEUDONIMO, no
> anonimo, re-identificable) + schema_medicion v1.0 (que se mide) + delimitacion sellada del sello Etapa 1.

## 1. Que es el estudio (para que legal entienda el objeto)
Un estudio de metodologia de desarrollo de software asistido por IA: contrasta un brazo BASELINE (agente
+ gate informal) contra un brazo GOBERNADO (agente + checker formal atestado + maquinaria) construyendo
el modulo Nova-Budget. Se mide COSTO (tokens), TIEMPO, y CALIDAD (defectos post-entrega). Fases:
- AHORA (3-30 jul): el desarrollo lo ejecutan AGENTES de IA (Codex/Claude), no empleados humanos.
- FUTURO (diferido, pre-registrado): una REPLICA "employee-run" en Nova Accounting, donde EMPLEADOS de la
  empresa corren la metodologia -> ahi entran datos de personas (empleados). ESTE es el disparador legal.

## 2. Los DOS focos que legal debe separar

### Foco A -- Datos de PERSONAS (empleados) en la replica employee-run
- Cuando empleados participen, se registrara su trabajo (tareas, tiempos, posiblemente identidad del
  autor por tarea via `actor`/correlation-id). Preguntas para legal:
  1. Bajo Ley 1581, participar en la medicion de su propio trabajo, es tratamiento de dato personal
     laboral que requiere AUTORIZACION PREVIA, EXPRESA E INFORMADA del titular (empleado)?
  2. La medicion (costo/tiempo/defectos por tarea) se distingue de una EVALUACION DE DESEMPENO? El
     estudio afirma que mide el PROCESO/metodologia, NO el rendimiento del empleado -- legal debe validar
     que esa delimitacion se sostiene y como redactarla en la autorizacion para que no derive en monitoreo
     laboral encubierto.
  3. Finalidad, retencion y supresion: por cuanto se guardan las filas atribuibles a un empleado; derecho
     de acceso/rectificacion/supresion (habeas data); base de legitimacion (consentimiento vs relacion
     laboral vs interes legitimo).
  4. Voluntariedad y no-represalia: puede un empleado NEGARSE a participar sin consecuencia laboral?

### Foco B -- Datos FINANCIEROS reales de la empresa (DbsFinanciero) tocados en el dev/medicion
- El desarrollo y la verificacion de paridad tocan la BD real (presupuesto publico, terceros con
  identificacion CC/CE/NIT). Preguntas para legal:
  1. Los terceros (Core.Terceros: personas naturales/juridicas con identificacion) son titulares bajo Ley
     1581 -> el acceso de desarrollo/verificacion a esos datos requiere que politica/finalidad? El acceso
     de verificacion es READONLY y por procs autorizados (no exfiltra), pero legal debe validar la base.
  2. Datos financieros de entidad publica: hay regimen especial (reserva, CUIPO/SIA/CHIP regulatorio) que
     limite su uso en un estudio, aun interno?
  3. Si el estudio se PUBLICA (Carril B, dataset/preprint): que puede salir? La postura tecnica es que solo
     sale el PLANO DE PROTOCOLO (metricas + `subject_hash`), SIN texto libre ni datos de negocio. PERO
     (SPEC-0079 C3) `subject_hash` es SEUDONIMO re-identificable, NO anonimo -> legal debe decir si es
     publicable y bajo que condiciones (anonimizacion adicional? agregacion? no publicar per-tarea?).

## 3. Postura tecnica ya construida (para que legal no parta de cero)
- SEUDONIMIZACION, no anonimizacion: el plano de protocolo referencia contenido por hash, sin prosa; el
  `actor` se restringe a un vocabulario de ids de agente. Bajo RGPD Cons.26 / Ley 1581, un hash con la
  carga util retenida es dato SEUDONIMIZADO (re-identificable) -> NO es "publicable como anonimo" sin mas.
- SEPARACION DE PLANOS: metricas (costo/tiempo/defectos) viven separadas del contenido del trabajo; no se
  registra texto libre del trabajo en el plano medible.
- MINIMIZACION: el schema mide lo necesario para las preguntas Q1-Q5; no captura contenido de negocio.

## 4. Lo que necesito de legal (entregable concreto)
1. Un formato de AUTORIZACION/consentimiento para empleados de la replica (Foco A) conforme a Ley 1581
   (finalidad, voluntariedad, no-represalia, derechos del titular, retencion).
2. Dictamen sobre el acceso de dev/verificacion a datos de terceros de DbsFinanciero (Foco B.1/B.2).
3. Dictamen de PUBLICABILIDAD del dataset seudonimizado (Foco B.3): que sale, en que granularidad, con que
   salvaguarda; o veredicto de "no publicar per-tarea / solo agregado".

## 5. Urgencia (por que arrancar hoy)
La replica employee-run es el ENTREGABLE de mayor valor (veredicto de compra) y esta DIFERIDA -- pero su
consentimiento legal tiene lead time largo. Meterlo a la cola de legal HOY evita que sea el cuello de
botella cuando llegue la replica. El estudio actual (agentes, sin personas) no lo requiere para AHORA,
pero el Foco B (datos reales tocados en dev) si aplica ya en menor grado.

## 6. Nota de carril (Asesor)
Esto enmarca preguntas; el dictamen es de legal. Yo aporto la postura tecnica (seudonimizacion, separacion
de planos, minimizacion) y la delimitacion del estudio. No sustituye asesoria juridica.
