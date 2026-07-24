# CARVE_OUTS.md - Catalogo de exclusiones deliberadas por lente (gate-scope auditable)

> Version: 1.0 (DECISION-0092). Dominio-neutral. ASCII puro.
> Fuente: patron "Do not flag when..." de review-*.md (framework 4R, gentle-ai/gentle-pi, licencia
> MIT), adoptado como practica de documentacion (DECISION-0092 seccion A.3).

## 1. Proposito

Un gate/checker que revisa una lente (ver `REVIEW_CONTRACT.md`) tiene, por diseno, un alcance
limitado: hay cosas que DELIBERADAMENTE no marca. Si esa exclusion queda implicita, el punto ciego
del gate no es auditable (nadie puede saber si "no hay hallazgo" significa "se reviso y esta bien" o
"nunca se reviso eso"). Este documento exige que cada checker/lente DECLARE sus carve-outs
explicitamente, en vez de dejarlos como conocimiento tacito del revisor.

Regla dura: un carve-out no declarado no es un carve-out, es un punto ciego oculto. Declarar el
carve-out no lo elimina, lo hace auditable.

## 2. Formato de un carve-out

```
- lente: R1 | R2 | R3 | R4
  regla: "condicion exacta bajo la cual el checker NO marca, aunque el patron general aplicaria"
  justificacion: "por que esta exclusion es legitima y no un hueco"
  instancia: "core (aplica a toda instancia) | <nombre-instancia> (solo aplica ahi)"
```

## 3. Carve-outs de nivel CORE (aplican a cualquier instancia de este protocolo)

- **R1 (Risk):** no marcar terminos de dominio dentro de directorios `profiles/` de la instancia (el
  vocabulario de dominio ahi es intencional, DECISION-0002); si marcarlo, marcarlo en el CORE
  (archivos genericos y `*.template.*`), nunca en `profiles/`.
- **R1 (Risk):** no marcar secretos de ejemplo declarados explicitamente como tales en archivos
  `*.template.*` o de documentacion de onboarding (son placeholders, no credenciales reales).
- **R2 (Readability):** no marcar un helper local claro, autoexplicativo y usado en un solo punto
  (evita ruido de "extraer funcion" sin beneficio real).
- **R3 (Reliability):** no marcar ausencia de test de integracion donde el contrato de la unidad es
  `spec_prepagado` (unidad que reusa una especificacion/evidencia ya versionada de otra unidad,
  declarado explicitamente en su DoR).
- **R4 (Resilience):** no marcar latencia de tareas reconocidas como pesadas por diseno (harnesses
  end-to-end largos, migraciones, cargas de datos) cuando el tiempo esperado ya esta documentado; el
  umbral de alarma es el tiempo SIN progreso, no el tiempo total.

## 4. Carve-outs de nivel INSTANCIA (declarados por cada instancia en su propio documento)

Cada instancia que adopte este contrato mantiene su propia lista de carve-outs especificos de su
dominio (nombres de procedimientos, columnas, endpoints, umbrales numericos de su negocio). Esa lista
NO vive en este archivo (violaria la neutralidad de dominio del core); vive en el `profile/` o en la
documentacion de gobierno de esa instancia, y se referencia desde ahi.

## 5. Disciplina de mantenimiento

- Un carve-out se agrega SOLO cuando un revisor real lo necesito para no generar un falso positivo
  documentado (no especulativamente).
- Un carve-out que empieza a ocultar defectos reales (el "uso normal" empieza a disparar el patron
  excluido) se retira o se acota; el patron de deteccion es el mismo criterio del checker (DEFECT_
  TAXONOMY.md: "si el uso normal lo dispara, es real").
- Cambiar un carve-out de CORE requiere el mismo proceso que cualquier cambio del nucleo neutral
  (revision + registro); cambiar uno de INSTANCIA es autonomia de esa instancia.

## 6. Relacion con otros documentos del core

- `REVIEW_CONTRACT.md`: el contrato de salida que estos carve-outs acotan.
- `DEFECT_TAXONOMY.md`: la regla "uso normal dispara -> WARNING-real" es el limite que evita que un
  carve-out se use para esconder un defecto genuino.
