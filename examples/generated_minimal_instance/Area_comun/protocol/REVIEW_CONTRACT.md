# REVIEW_CONTRACT.md - Contrato de salida uniforme para revisores (lentes R1-R4)

> Version: 1.0 (DECISION-0092). Dominio-neutral. ASCII puro.
> Fuente: adopcion selectiva del framework 4R (gentle-ai/gentle-pi de Alan Buscaglia, licencia MIT)
> y de la skill judgment-day (licencia Apache-2.0), citadas como trabajo relacionado. Esta version es
> presentacion/documentacion (DECISION-0092 seccion A): no cambia el comportamiento de ningun gate,
> solo etiqueta y uniforma lo que un revisor YA emite.

## 1. Proposito y alcance

Formato uniforme, parseable por maquina, para el reporte de cualquier revisor (adversarial informal,
checker formal, maker auto-declarando cobertura, juez) sobre una unidad de trabajo. No define QUE
revisar (eso lo fija cada instancia/dominio en su propio checklist); define COMO se reporta lo que
se reviso, para que el resultado sea comparable entre revisores y verificable por un tercero.

Es opcional y aditivo: una instancia puede seguir reportando en su formato actual sin violar el
protocolo; adoptar este contrato mejora el parseo y la trazabilidad.

## 2. Lentes R1-R4 (vocabulario neutral, no un checker nuevo)

Etiqueta ortogonal sobre hallazgos que un revisor YA produce. No prescribe reglas de dominio; cada
instancia mapea sus propios checks a la lente que corresponda.

| Lente | Nombre | Eje de la revision |
|-------|--------|---------------------|
| R1 | Risk | Seguridad, secretos, superficies de riesgo, guardas de procedencia de evidencia |
| R2 | Readability | Claridad de artefactos/handoffs, acoplamiento estructural, duplicacion, componentes compartidos entre unidades |
| R3 | Reliability | Cobertura de contrato/comportamiento, determinismo, tests de regresion |
| R4 | Resilience | Rutas de fallo/recuperacion, observabilidad, rollback, umbrales operativos |

Un revisor puede cubrir una, varias o todas las lentes en una pasada; el contrato exige DECLARAR
cuales corrieron (`lenses_run`), no fingir cobertura total.

## 3. Formato del veredicto

### 3.1 Cabecera (una por revision)

```
## REVIEW -- {target} -- round {n}
reviewer_role: maker | adversarial_informal | checker_formal | judge
provider_family: <familia de modelo del revisor>      # traza para el principio de s.5
maker_family: <familia de modelo de quien construyo>  # familia de lo revisado
lenses_run: [R1, R3]                                  # cobertura EXPLICITA; el resto = no evaluado
verdict: GO | NOGO | ESCALATE
```

### 3.2 Por hallazgo

```
- id: "#N"                            # numeracion del backlog de hallazgos de la instancia
  lens: R1 | R2 | R3 | R4
  severity: BLOCKER | CRITICAL | WARNING | SUGGESTION
  blocking: true | false              # eje bloqueante vs quality-data
  files: ["path:line", ...]           # evidencia exacta, obligatoria
  evidence: "que se observo y CONTRA QUE FUENTE se verifico"
  why: "por que importa"
  corrective_criterion: "criterio correctivo horneable (fix-forward, no parche retroactivo)"
  attestation: "referencia de proveniencia: sha256 | id de evento del ledger | NA"
```

Los campos `corrective_criterion` y `attestation` son extension propia de este protocolo (el 4R
original no los lleva): convierten un "finding" en un hallazgo gobernado con proveniencia y ruta de
correccion, no solo una observacion.

### 3.3 Cadena limpia canonica

- Por lente: `R{n}: No findings.`
- Global: `REVIEW CLEAN -- no findings across [R1,R2,R3,R4].`

Cadena EXACTA y deterministica, parseable por runtime file-based.

### 3.4 Mapa de severidad sugerido (cada instancia puede ajustar el umbral, no el vocabulario)

| Severidad | Significado | blocking tipico |
|-----------|-------------|------------------|
| BLOCKER | Rompe el gate, veredicto NOGO obligatorio | true |
| CRITICAL | Correctness con impacto, condicionado al contexto | true/false |
| WARNING | No bloqueante, se registra como quality-data | false |
| SUGGESTION | Mejora opcional | false |

## 4. Gate de cobertura (DIFERIDO, ver DECISION-0092 seccion B)

El computo automatico de `lenses_required` (derivado de senales del diff/cambio) y el gate que exige
`lenses_run` cubra `lenses_required` es un CAMBIO DE COMPORTAMIENTO del proceso de revision -- no se
activa por la sola existencia de este documento. Cada instancia decide y registra por su cuenta
(via su propia DECISION) cuando pasa de "contrato de reporte" a "gate de cobertura obligatorio".

## 5. Principio de disjuncion-del-maker (registrado; ver CARVE_OUTS.md y DECISION-0092 seccion A.4)

Independencia operacionalizada: la familia de modelo del revisor (`provider_family`) debe ser
DISTINTA de la familia de modelo de quien construyo (`maker_family`) mientras esa relacion
maker/checker este vigente. Es una extension sobre "diversificar modelo" (judgment-day): no basta con
que los revisores sean diversos entre si, el revisor tampoco puede compartir familia con el maker (un
revisor de la misma familia hereda los puntos ciegos de esa familia y tiende a validar sus propios
errores de clase). Este documento REGISTRA el principio como diseno; su ENFORCEMENT (bloquear en el
gate una configuracion prohibida) es decision de cada instancia.

## 6. Ejemplo de uso

```
## REVIEW -- unidad-ejemplo -- round 2
reviewer_role: adversarial_informal ; provider_family: familia-B ; maker_family: familia-A
lenses_run: [R1, R3] ; verdict: GO (con quality-data no-bloqueante)

- id: "#7" ; lens: R3 ; severity: WARNING ; blocking: false
  files: ["src/modulo.ext:120"]
  evidence: "camino de lectura de produccion difiere del camino ejercitado por el harness de evidencia"
  why: "el camino real nunca fue verificado contra la fuente desplegada"
  corrective_criterion: "unificar el camino de lectura entre produccion y harness de evidencia"
  attestation: "hallazgo #7 registrado, veredicto formal pendiente"

# R2 y R4 no corrieron sobre esta unidad -- lenses_run declara la cobertura, no se finge.
R2: not run. R4: not run.
```

## 7. Relacion con otros documentos del core

- `DEFECT_TAXONOMY.md`: clasifica defectos por canal de deteccion (D1-D4) y naturaleza (S1-S7); este
  documento clasifica hallazgos por LENTE (que eje de revision lo produjo). Son ejes ortogonales,
  compatibles: un mismo hallazgo puede llevar clase D/S y lente R.
- `CARVE_OUTS.md`: catalogo de "do not flag" por lente, referenciado desde aqui.
- `HANDOFF_TEMPLATE.md`: un handoff puede incluir un bloque REVIEW en este formato cuando reporta el
  resultado de una revision.
