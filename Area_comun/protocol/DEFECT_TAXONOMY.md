# DEFECT_TAXONOMY.md - Taxonomia de defectos D1-D4 ampliada + severidad del checker

> Version: 1.0 (TASK-0241, [VISION-NOVA][F1.4]). Dominio-neutral. ASCII puro.
> Fuente de las clases D1-D4: convenciones del pre-registro (seccion 7.0). Los 6 huecos: veredicto
> adversarial del pivote v2 (Area_comun/artifacts/ANALISTA-pivote-v2-veredicto.md).

## 1. Proposito y alcance

Taxonomia CERRADA de defectos para instancias del protocolo que midan calidad (pre-registro,
metricas de escape, evaluacion de checkers). Cierra los 6 huecos senalados por la revision
adversarial del pivote v2 (requisito mal entendido, deuda de arquitectura, performance no
testeada, UX/soporte, integracion externa, conciliacion tardia) via SUBCATEGORIAS, y declara
explicitamente el SUBCONTEO ESPERADO (que defectos el estudio NO capta). Adopta la escala de
severidad del checker con la regla del uso normal.

Regla de cierre: todo defecto observable cae en exactamente UNA clase D1-D4 (canal de
deteccion) y UNA subcategoria S1-S7 (naturaleza). Ambiguedades -> `arbitrated:true` y se
reportan aparte; si una conclusion depende de arbitrados, se declara.

## 2. Clases D1-D4 (canal de deteccion; taxonomia cerrada)

| Clase | Definicion | Evidencia requerida |
|-------|------------|---------------------|
| D1 | Gate/test ROJO antes del GO del checker (validador, tests, scans, CI) | Log del gate con exit code != 0 ligado a la tarea |
| D2 | Hallazgo del checker en un NO-GO, con test/repro adjunto | Veredicto NO-GO + repro/test que lo demuestra |
| D3 | Escape post-GO: tarea `type:fix` con trailer `Fixes-Task:` obligatorio, o revert/hotfix que referencia el commit aceptado | Trailer `Fixes-Task:` o referencia explicita al commit aceptado |
| D4 | Reporte de usuario/operador sobre comportamiento ya aceptado | Mensaje/mailbox del reporte ligado a la tarea de origen |

Solo D3/D4 cuentan como "escape". D1/D2 son defectos CONTENIDOS por el proceso (el gate o el
checker los detuvo antes de la aceptacion).

## 3. Subcategorias S1-S7 (naturaleza del defecto; cierran los 6 huecos)

| Sub | Nombre | Definicion | Hueco del veredicto que cierra |
|-----|--------|------------|--------------------------------|
| S1 | Implementacion | Logica/estado/borde incorrecto respecto a un requisito bien entendido | (base, ya cubierto) |
| S2 | Requisito mal entendido | La entrega cumple lo construido pero NO lo pedido; AC ambiguo o interpretado mal | hueco 1 |
| S3 | Deuda de arquitectura | Decision estructural que degrada mantenibilidad/extensibilidad y obliga rework posterior | hueco 2 |
| S4 | Performance no testeada | Degradacion de latencia/consumo/escala sin test que la cubriera al aceptar | hueco 3 |
| S5 | UX/soporte | Friccion de uso u operacion: mensajes confusos, flujo inoperable, coste de soporte | hueco 4 |
| S6 | Integracion externa | Fallo en el borde con dependencias/herramientas/entornos de terceros | hueco 5 |
| S7 | Conciliacion tardia | Discrepancia de datos/estado detectada por verificacion diferida contra una fuente de referencia, sin hotfix inmediato | hueco 6 |

Toda instancia de defecto se etiqueta `D<x>/S<y>`. Si ninguna S aplica sin forzar -> S1 por
defecto NO se permite: se marca `arbitrated:true` con nota (evita el cajon de sastre).

## 4. Severidad del checker (escala adoptada; regla del uso normal)

| Severidad | Definicion | Efecto en el veredicto |
|-----------|------------|------------------------|
| CRITICAL | Rompe la funcion principal, corrompe estado o viola un boundary del proyecto | NO-GO obligatorio |
| WARNING-real | Defecto que el USO NORMAL dispara (regla: "si el uso normal lo dispara, es real") | NO-GO salvo excepcion registrada |
| WARNING-theoretical | Defecto real pero solo alcanzable en condiciones fuera del uso normal declarado | No bloquea; se registra y se encola |
| SUGGESTION | Mejora de calidad sin defecto observable | No bloquea |

El checker DEBE etiquetar cada hallazgo con una severidad; los NO-GO citan al menos un
CRITICAL o WARNING-real con repro. Un patron repetido de WARNING-theoretical elevado a NO-GO
es anomalia de proceso (sobre-bloqueo) y se senala.

## 5. SUBCONTEO ESPERADO (lo que este esquema declara que NO capta)

1. Defectos NUNCA detectados: sin gate rojo, sin NO-GO, sin fix, sin reporte -> invisibles
   por construccion (cota inferior, no censo).
2. D3 sin trailer: un fix que omite `Fixes-Task:` y elude el validador de trailers no linkea
   (mitigado cuando el gate de trailers esta ACTIVO; ver ventana de arranque declarada).
3. D4 no reportados: usuarios/operadores que toleran el defecto sin reportarlo.
4. Defectos latentes de S3/S4 que solo se manifiestan a escalas o plazos posteriores a la
   ventana de medicion.
5. Defectos en rutas exentas por el arranque declarado (commits/tareas historicos previos al
   `start` de cada gate: intake_start, trailer_start_seq).
6. Auto-fixes silenciosos dentro del mismo turno del owner (corregidos antes del primer gate;
   no dejan rastro D1).
Toda conclusion cuantitativa sobre "defectos totales" se reporta como COTA INFERIOR con esta
lista citada.

## 6. Prueba de mesa: 10 defectos historicos re-clasificados (sin residuo)

| # | Defecto historico (evidencia) | Clase | Sub | Severidad en su momento |
|---|-------------------------------|-------|-----|--------------------------|
| 1 | F-0238-01: R5 intake_exempt no fail-closed, aceptaba exception_ref falso (NO-GO Analista, repro) | D2 | S1 | CRITICAL |
| 2 | F-0239-01: payload actor != caller firmante -> mis-atribucion (NO-GO Analista, repro) | D2 | S1 | WARNING-real |
| 3 | F-0240-01: parser contaba Task-Id fuera de la seccion final de trailers (NO-GO Analista, repro) | D2 | S1 | WARNING-real |
| 4 | npm test colgante (arbol node/esbuild) que jameaba los crons; fix TASK-0236/0237 | D3 | S6 | CRITICAL |
| 5 | exec-death: exec del checker muere ~10min y deja lock huerfano; fix TASK-0235 | D3 | S6 | CRITICAL |
| 6 | Footgun stop-order: regex de corte disparaba con "para" preposicion; fix harness 0236 (affe347) | D3 | S2 | WARNING-real |
| 7 | Whack-a-mole branding 0229: AC "cero grep" inalcanzable, 4 NO-GO; cierre por DECISION-0082 | D2 | S2 | WARNING-real |
| 8 | Em-dashes/no-ASCII en MSG rompieron scan_encoding (gate rojo pre-commit/pre-GO) | D1 | S5 | WARNING-real |
| 9 | Claim wildcard scope ["*"] bloqueo toda edicion ~1h; detectado por el Arquitecto en operacion | D4 | S5 | WARNING-real |
| 10 | Monitor async no despierta la sesion idle; entrega 03:17 sin reaccion, lo noto el operador | D4 | S5 | WARNING-real |

Residuo: 0/10 (todas las instancias reciben exactamente una D y una S sin forzar).

## 7. Integracion con el protocolo

- El intake block (`risk`) y esta taxonomia son ortogonales: `risk` es prospectivo, D/S es
  retrospectivo sobre defectos observados.
- Los trailers (`Task-Id:` / `Fixes-Task:`) son el mecanismo de linkage v1 de D3 (bisect/blame
  = v2, fuera de alcance).
- El checker referencia esta escala en su prompt de review; los veredictos citan `D/S` +
  severidad por hallazgo cuando la instancia mide calidad.
