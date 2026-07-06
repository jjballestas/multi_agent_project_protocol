# Nota de diseno - Contraste "mono vs peones" medido en costo de tokens (paquete sello Etapa 2)

> Insumo del paquete de diseno del sello de Etapa 2, ordenado por la DIRECTIVA del Operador
> 2026-07-06 (commit 30a4252, seccion 4). Estado: PROPUESTA lista para el pre-registro de
> Etapa 2; NO ejecuta nada en Etapa 1. El brazo gobernado del contraste central de Etapa 1 se
> mantiene MONO-orquestado (linea roja del sello, intacta). Redactado por el Arquitecto;
> la adjudicacion final del contraste es del sello de Etapa 2 firmado por el Operador.

## 1. Pregunta candidata (pre-registrable)

**Q-PEON:** bajo gobierno COMPLETO (mismo gate adversarial, mismos SLA, mismo aparato de
medicion), delegar el drafting mecanico a peones (modelos no-frontera, keyless, fuera del
ledger como makers-borrador) REDUCE el costo de tokens de los modelos frontera por unidad
equivalente, sin degradar la calidad (defectos D1-D4 y reworks estables)?

- Metrica primaria: `tokens_total_atribuibles` por unidad (la moneda confirmatoria ya probada
  en el baseline de Etapa 1), desglosada con las cubetas Q1 ya instrumentadas
  (regimen / arranque / overhead separados via `tag_incidente_maquinaria`).
- Metrica de guardia (no-inferioridad): defectos por taxonomia D1-D4, `reworks_n`,
  `secuencia_veredictos` del gate. Un ahorro de tokens con degradacion de calidad NO es exito.
- El schema de medicion v1.0 (52 cols) YA incluye los 5 campos de peones -- la instrumentacion
  existe desde F3.3; no se requiere aparato nuevo.

## 2. Poblacion y asignacion

- **Corpus:** unidades de Contabilidad que salgan del analisis de migracion (DIRECTIVA seccion 3).
  Ese analisis debe entregarlas ENUMERABLES y con verificacion de paridad definible (mismo
  estandar que el pool Q4 de Etapa 1) -- es el prerequisito duro de este contraste.
- **Brazos:** A = mono-orquestado gobernado (identico al tratamiento de Etapa 1); B = peones
  bajo gobierno completo (peon draftea, firmante frontera revisa/firma; maker != checker se
  preserva; el peon JAMAS firma ledger).
- **Asignacion:** sorteo sellado sobre pares/estratos isomorfos (mismo procedimiento NIST +
  sha256 del sello de Etapa 1; las lecciones s.21/s.23 de isomorfismo aplican de origen).
- **Tratamiento declarado:** la memoria hibrida (REQ-MEMORIA-HIBRIDA v0.3.0, decision en cola)
  forma parte del tratamiento de AMBOS brazos si su DECISION esta aprobada antes del sello de
  Etapa 2; es prerequisito declarado de que los peones revivan con contexto (sinergia
  DIRECTIVA seccion 2.3). Si no llega a tiempo, el contraste corre sin ella EN AMBOS brazos
  (simetria primero; nunca un brazo con memoria y otro sin).

## 3. REGLA ESTRUCTURAL del sello Etapa 2 (ordenada por el Operador, no negociable en el diseno)

Las ventanas y aperturas del sello de Etapa 2 se definen POR COMPLETITUD CERTIFICADA --
certificacion READ-ONLY de un tercero (checker que no fue maker de lo certificado) de que el
trabajo previo esta completo y reconciliado -- NUNCA por fecha de calendario. Es la correccion
del punto debil identificado en Etapa 1 (tiempo muerto endogeno de ventanas por fecha) y queda
sellada de origen como regla del diseno. Consecuencia operativa: el contraste peones NO abre
hasta que se certifique (a) reconciliacion de Etapa 1 completa, (b) analisis de Contabilidad
entregado con unidades enumerables, (c) sello de Etapa 2 firmado.

## 4. Amenazas declaradas (para el anexo de riesgos del sello Etapa 2)

1. **Confusion arranque/regimen:** los peones agregan overhead de arranque propio; separar con
   las cubetas Q1 (leccion del piloto GOAL-P1: el desglose se captura donde el runtime lo
   permita, degradacion ex-ante si no).
2. **Curva de aprendizaje asimetrica:** el brazo B estrena tooling; declarar las primeras
   unidades como teething tagueado (`tag_incidente_maquinaria=arranque`), igual que hizo el
   baseline de Etapa 1.
3. **Fuga de trabajo entre brazos:** el peon no puede tocar unidades del brazo A; misma regla
   de aislamiento de par que Etapa 1, con verificacion mecanica.
4. **Atribucion de tokens del peon:** los tokens del peon NO son tokens de frontera; se
   registran en sus campos propios (5 campos peones del schema) y JAMAS se restan de
   `tokens_total_atribuibles` del firmante -- el ahorro se lee comparando el costo frontera
   entre brazos, no editando la moneda.

## 4b. Pre-registro de PARTICIPANTES en el sello Etapa 2 (hueco 6 del onboarding remoto)

Requisito estructural adicional (DIRECTIVA addendum onboarding-remoto, 2026-07-06): el sello
de Etapa 2 DEBE NOMBRAR, antes de sellar, a los participantes, sus maquinas/clones y sus roles
(maker/checker por unidad). Razon de study-integrity: un SEGUNDO humano operando Contabilidad
(empleado remoto) es una VARIABLE del estudio -- los exception events (`assist`/
`manual_intervention`) y el journal ya registran quien hizo que, pero la COMPOSICION del equipo
debe estar pre-registrada, no descubierta a mitad de ventana. Decidirlo antes de sellar es
gratis; a mitad de ventana seria enmienda. Incluye: id de cada participante, su identidad
firmante (y si opera bajo identidad existente u propia -- ver bifurcacion del runbook s.8.4),
su maquina/huso, y el reparto maker!=checker (separado fisicamente por posesion de llave).

## 5. Traza de re-alcance de TASK-0231 (F6.1)

Por decision del Operador (DIRECTIVA 30a4252 seccion 4, update 2026-07-06): F6.1/peones NO se
corre como F6 sobre Presupuesto post-Sprint-1; se REDISENA dentro del sello de Etapa 2 como este
contraste. Criterio de asiento del Arquitecto: el DISENO/pre-registro es capa ESTUDIO/meta ->
vive en el HUB (DECISION-0088 punto 1; DECISION-0093 punto 1); la EJECUCION del brazo B sobre
unidades de Contabilidad se gobierna desde Aegis como el resto de la suite. TASK-0231 queda
`proposed` en el hub con nota de re-alcance apuntando a esta nota; no se activa antes del sello
de Etapa 2.
