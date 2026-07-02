# DRAFT - Politica interna de medicion de empleados (F3.1, bloqueante 1 del Sprint 1)

- fecha: 2026-07-02 (borrador adelantado por el Asesor, directiva de proactividad;
  F3.1 formalmente corre en sem 3-4 pero ya esta desbloqueado por los insumos)
- estado: DRAFT. GATES antes de vigencia: (1) revision legal dual Ley 1581 + RGPD
  (IMPRESCINDIBLE, ver consentimiento v0.2); (2) gate adversarial del Analista en
  F3; (3) firma del Operador.
- pareja: CONSENTIMIENTO-EMPLEADOS-BORRADOR.md v0.2 (cara del empleado); este doc
  es la cara empresa/proceso. Deben permanecer coherentes.

## 1. Ambito y base

Aplica al estudio pre-registrado de la metodologia sobre Nova Budget (y futuras
instancias Nova que lo adopten explicitamente). Decisiones del Operador 2026-07-02
incorporadas: dataset publico COMPLETO SEUDONIMIZADO (roles, no nombres, con
advertencia expresa de re-identificacion); no-consentimiento = exclusion SOLO del
dataset publicado; retencion de crudos atribuibles = 24 meses post-estudio.

## 2. Que se mide y que no (limites duros)

Se mide SOLO lo derivado de ledger/git/CI a nivel de tarea: costo (tokens),
ciclos de review y veredictos, defectos ligados (taxonomia D1-D4 ampliada),
tiempos de ciclo, eventos exception.recorded. NO se mide: pantalla, teclado,
contenido de comunicaciones privadas, ubicacion, horarios mas alla de metadatos
git/CI. Herramientas de vigilancia = PROHIBIDAS por esta politica.

## 3. No-punitivo (compromiso central)

Las metricas del estudio NO se usan para evaluacion de desempeno individual,
compensacion ni decisiones disciplinarias. Incondicional durante el estudio y
sobre sus datos. Violacion de este punto = violacion de politica reportable como
anomalia (DECISION-0018) y anula el consentimiento otorgado.

## 4. Redaccion y minimizacion

Eventos del ledger: cero PII estructural (leccion DECISION-0071/B: enums y refs,
no prosa libre); personas referidas por id de agente/rol (dev-1, dev-2), jamas
nombre/correo. Los summary de exception.recorded en ASCII y sin datos personales.
Antes de CUALQUIER publicacion (CB.1): pasada de redaccion PII sobre el corpus.

## 5. Acceso y retencion

Datos crudos atribuibles: acceso SOLO operador del estudio + auditor tecnico
designado. Retencion 24 meses post-cierre; despues, borrado o anonimizacion
irreversible. Cada participante consulta SUS datos cuando quiera y puede pedir
correccion de atribucion. Lo publicado (dataset seudonimizado) no es retirable;
la retencion aplica al corpus crudo interno.

## 6. Ayudas, excepciones y disputa

Toda ayuda/des-atasco/arbitraje/suspension se registra como exception.recorded
(F1-B); las del periodo se listan en el reporte del estudio. Disputa de
atribucion: canal interno -> se registra evento firmado con arbitrated:true ->
resolucion auditable. Disputar no tiene consecuencia negativa.

## 7. Acuse y vigencia

Consentimiento firmado ANTES del onboarding al estudio (F4.1); acuse registrable
como evento consent.acknowledged (id de agente + hash del documento, sin datos
personales). Retiro del consentimiento: efecto hacia adelante, exclusion del
dataset publicado, sin efecto laboral. Cambios materiales a esta politica o al
nivel de publicacion => nuevo consentimiento.

## 8. Jurisdiccion

Dual: Ley 1581 de 2012 (Colombia, participante) + RGPD UE 2016/679 (Espana,
responsable del tratamiento), incluida la transferencia internacional CO-ES.
[GATE ABIERTO: revision de abogado laboral/datos en ambas normativas antes de la
primera firma.]
