# INSUMOS PRD-03 - Decisiones que solo el Operador puede tomar (paquete F0, parte d)

Estas 2 entradas BLOQUEAN PRD-03 (estudio pre-registrado): sin ellas no se puede
redactar la politica de medicion (F3.1) ni sellar el pre-registro (F3.4).

## Insumo 1 - Dataset publico: agregado vs completo

Que saldria al publico en el Carril B (y que se le promete al empleado en el punto 6
del consentimiento). Opciones:

- (i) AGREGADO — RECOMENDADA: metricas agregadas por tarea/fase/brazo, sin ids de
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

1. Punto 6 (publicacion): la misma eleccion del Insumo 1 — el empleado debe saber
   si sus eventos salen y como.
2. Punto 9 (no-consentimiento): (i) exclusion solo del dataset PUBLICADO, trabaja
   normal — RECOMENDADA; o (ii) exclusion total del estudio (reduce muestra;
   declararlo en el pre-registro).
3. Punto 7 (retencion de datos crudos atribuibles): 12 o 24 meses post-estudio —
   RECOMENDADA 24 (cubre auditoria del estudio ago-dic + margen).

## Paso legal (recomendacion firme, no opcional en la practica)

Revision de ~30 minutos del borrador con abogado laboral/de datos local (Ley 1581
de 2012, habeas data; relacion laboral + datos personales) ANTES de la primera
firma. Barato, y es la diferencia entre estudio publicable y demanda evitable.

## Que pasa cuando el Operador decida

- Las 3 marcas [DECIDE EL OPERADOR] se resuelven en el borrador -> texto final.
- La politica de medicion F3.1 se redacta coherente con esas elecciones.
- El pre-registro (F3.4) declara: nivel de publicacion, regla de exclusion por
  no-consentimiento y retencion — y se sella con hash + seq + ancla externa.
