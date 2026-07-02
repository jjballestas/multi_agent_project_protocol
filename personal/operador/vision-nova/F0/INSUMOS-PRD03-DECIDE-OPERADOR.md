# INSUMOS PRD-03 - Decisiones que solo el Operador puede tomar (paquete F0, parte d)

## RESUELTO (respuestas del Operador, 2026-07-02, sesion Asesor)

- Insumo 1 (dataset publico): **COMPLETO SEUDONIMIZADO** (opcion ii). El Operador
  elige maxima reproducibilidad sobre la recomendacion de agregado. Implicaciones
  aplicadas: el consentimiento (punto 6) incluye ADVERTENCIA EXPRESA de riesgo de
  re-identificacion en equipo pequeno que el empleado acepta al firmar; la revision
  legal de 30 min pasa de recomendada a IMPRESCINDIBLE; el pre-registro (F3.4)
  declara "eventos por tarea con etiqueta de rol" como nivel de publicacion; la
  redaccion PII pre-publicacion (CB.1) gana peso.
- Insumo 2a (no-consentimiento): **exclusion solo del dataset publicado**; el
  empleado trabaja exactamente igual (punto 9 resuelto).
- Insumo 2b (retencion de crudos atribuibles): **24 meses** post-estudio, luego
  eliminacion o anonimizacion irreversible (punto 7 resuelto).

PRD-03 queda DESBLOQUEADO: F3.1 (politica de medicion) puede redactarse con estas
elecciones cuando toque F3.

---

Contexto original de la peticion (conservado como provenance):

Estas 2 entradas BLOQUEAN PRD-03 (estudio pre-registrado): sin ellas no se puede
redactar la politica de medicion (F3.1) ni sellar el pre-registro (F3.4).

## Insumo 1 - Dataset publico: agregado vs completo

Que saldria al publico en el Carril B (y que se le promete al empleado en el punto 6
del consentimiento). Opciones:

- (i) AGREGADO -- RECOMENDADA: metricas agregadas por tarea/fase/brazo, sin ids de
  persona ni rol individual. Publicable sin friccion legal; pierde granularidad
  para terceros que quieran re-analizar.
  Razon de la recomendacion: con 2-6 personas la seudonimizacion es ficcion
  (hallazgo ClaudeAI ronda 2); el agregado elimina la re-identificacion de raiz y
  hace el consentimiento mas facil de firmar de verdad (consentimiento laboral =
  juridicamente debil; hay que compensar con garantias reales).
- (ii) COMPLETO SEUDONIMIZADO: eventos crudos con rol (dev-1, dev-2). Maximo valor
  de reproducibilidad; riesgo de re-identificacion alto en equipo pequeno.
- (iii) DUAL: agregado publico + corpus completo privado retenido para auditoria
  (un auditor externo puede verificarlo bajo acuerdo). Balance razonable si la
  reproducibilidad importa.

## Insumo 2 - Texto de consentimiento: 3 decisiones dentro del borrador

Borrador completo listo en CONSENTIMIENTO-EMPLEADOS-BORRADOR.md con las marcas:

1. Punto 6 (publicacion): la misma eleccion del Insumo 1 -- el empleado debe saber
   si sus eventos salen y como.
2. Punto 9 (no-consentimiento): (i) exclusion solo del dataset PUBLICADO, trabaja
   normal -- RECOMENDADA; o (ii) exclusion total del estudio (reduce muestra;
   declararlo en el pre-registro).
3. Punto 7 (retencion de datos crudos atribuibles): 12 o 24 meses post-estudio --
   RECOMENDADA 24 (cubre auditoria del estudio ago-dic + margen).

## Paso legal (IMPRESCINDIBLE)

Revision de ~30 minutos del borrador con abogado laboral/de datos ANTES de la
primera firma. JURISDICCION DUAL (anadido 2026-07-02, operador en Espana +
empleado en Colombia): la revision debe cubrir Ley 1581 de 2012 (Colombia,
habeas data) Y RGPD (UE 2016/679, responsable del tratamiento en Espana),
incluida la transferencia internacional de datos Colombia-Espana. Barato, y es
la diferencia entre estudio publicable y demanda evitable.

## Que pasa cuando el Operador decida

- Las 3 marcas [DECIDE EL OPERADOR] se resuelven en el borrador -> texto final.
- La politica de medicion F3.1 se redacta coherente con esas elecciones.
- El pre-registro (F3.4) declara: nivel de publicacion, regla de exclusion por
  no-consentimiento y retencion -- y se sella con hash + seq + ancla externa.
