---
message_id: MSG-20260706-Operador-to-Arquitecto-ACTION-corte-aegis-cola-reqs-contabilidad
from: Operador
to: Arquitecto
type: ACTION
status: open
requires_response: true
response_owner: Arquitecto
created_at: 2026-07-06
context_refs:
  - Area_comun/decisions/DECISION-0088-asiento-escalonado-instancia-aegis.md
  - Area_comun/decisions/DECISION-0091-sello-etapa1-nova-budget.md
  - personal/operador/vision-nova/SELLO-ETAPA-1-nova-budget-DRAFT.md
  - personal/operador/requerimientos-futuros/software-engineering-ia-no-vibecoding/REQ-ZEUS-AEGIS-SOFTWARE-ENGINEERING-CON-IA-NO-VIBECODING.md
  - personal/operador/requerimientos-futuros/intake-profesional-requerimientos/REQ-ZEUS-AEGIS-INTAKE-PROFESIONAL-REQUERIMIENTOS.md
  - personal/operador/requerimientos-futuros/memoria-hibrida-db-archivo-frio/REQ-MEMORIA-HIBRIDA-DB-ARCHIVO-FRIO.md
  - personal/operador/requerimientos-futuros/aprendizajes-agentes-externos/ANALISIS-TRANSCRIPCION-c5Gwx0RcxNE-REGLAS-METODOLOGIA.md
  - Area_comun/tasks/TASK-0231-vision-nova-f6-1-fase-peones.md
one_line_summary: "Decisiones del Operador tras revision del alcance total (Ingenas ~13 modulos/452 forms): SIN enmienda al sello (calendario Etapa 1 intacto); corte de gobernanza hub->Aegis YA (DECISION-0088); cola pre-30-jul = DECISIONes+implementacion de los 4 REQs futuros en ambito instancia/producto; analisis de migracion de Contabilidad arranca de inmediato; peones/tokens se disena dentro del sello Etapa 2. Proceder de inmediato."
requested_action: "Ejecutar en este orden y confirmar pickup con plan + ETAs por mailbox: (1) formalizar el corte de gobernanza hub->Aegis segun DECISION-0088 y verificar los 3 firmantes operativos en la instancia Aegis con un ciclo e2e de humo; (2) preparar y rutear las DECISIONes de los 4 REQs (orden: anti-vibecoding -> intake -> memoria-hibrida; aprendizajes-externos se absorbe como reglas) y lanzar su implementacion en ambito Aegis/Zeus-Aegis, nunca el core pineado del hub; (3) abrir el analisis de migracion de Contabilidad (fuentes Ingenas) gobernado desde Aegis; (4) incluir la pregunta peones-vs-tokens como contraste candidato del paquete de diseno del sello Etapa 2; (5) registrar la declaracion de trabajo paralelo en el reporte de Etapa 1. La cola PREP vigente (MSG DIRECTIVA cola-prep-sprint1-no-idle) sigue viva; esta directiva la AMPLIA y fija prioridades relativas."
question: "Confirmas pickup, orden y ETAs? Marca explicitamente cualquier item que a tu juicio roce el sello de Etapa 1 (linea roja Q4 / unidades gobernadas / aparato de medicion) y difierelo con nota, sin frenar el resto de la cola."
---

# ACTION - Corte hub->Aegis + cola pre-30-jul (4 REQs) + Contabilidad + peones/Etapa 2

Directiva del Operador tras sesion de debate con agente independiente (2026-07-06). Se reviso el
alcance total del legado Ingenas (~13 modulos, ~452 formularios, 278 tablas; Nova-Budget cubre ~25%),
se verifico que el brazo BASELINE esta completo (TASK-0250/0251/0253/0254/0255 done, PAR-2 confirmado,
cero claims activos de desarrollo baseline), y se tomaron las decisiones de abajo. Orden: proceder de
inmediato.

## 0. Decisiones marco del Operador (contexto vinculante)

- **SIN enmienda al sello de Etapa 1.** El calendario sellado queda INTACTO: reconciliacion 26-29-jul,
  Sprint 1 gobernado abre 2026-07-30, orden de arranque y brazos tal como estan. El tiempo de ventana
  se aprovecha con la cola de abajo, no adelantando unidades selladas.
- **Prioridad de negocio de la suite (orden fijado por el Operador):** 1 Presupuesto, 2 Contabilidad,
  3 Control de Pagos, 4 Tesoreria, 5 Nomina, 6 Almacen, 7 Impuesto Predial, 8 Impuesto de Industria y
  Comercio, 9 Sobretasa a la gasolina, 10 Rentas varias, 11 Facturacion (Acueducto).
- **Sede de gobernanza:** el hub (este repo) cierra la Etapa 1 y sigue siendo el nucleo neutral del
  protocolo. TODA gobernanza nueva de la suite Nova (Contabilidad en adelante) nace en el ledger de la
  instancia Aegis (`D:/Agentes/Zeus/NOVA/Aegis`, pin v1.18.0, perfil governed-instance). Los repos de
  producto siguen bajo `D:/Agentes/Zeus/`.
- **Desde el 30-jul, el Sprint 1 gobernado tiene PRIORIDAD DURA** sobre Contabilidad y sobre los REQs,
  por el SLA del sello (adversarial 48h, veredicto 48h, una gracia 72h/ventana, STOP total por
  reincidencia). Ninguna otra cola justifica incumplir ese SLA.

## 1. Corte de gobernanza hub->Aegis (DECISION-0088) - INMEDIATO

1. Formaliza el corte como complemento FORMAL de DECISION-0088 -- es formalizacion NECESARIA, no
   opcional: el texto vigente de 0088 dice "migracion post-sello", y hacer el corte AHORA (lo medido
   sigue en el hub, lo nuevo nace en Aegis) es un refinamiento que ese texto no autoriza explicito.
   Sin el complemento quedaria drift "el corte contradijo 0088". Regla del Operador: hub = Etapa 1
   completa (sello, sorteo, journal, Sprint 1, reconciliacion, reporte) + evolucion del protocolo
   neutral; Aegis = todo lo nuevo de la suite Nova (tareas, claims, mailbox, atestacion de
   Contabilidad en adelante, y las DECISIONes de los REQs de la seccion 2 cuando su ambito sea
   instancia/producto).
2. El corte CABLEA la cross-atestacion dual desde el arranque, no solo levanta un segundo ledger:
   DECISION-0088 exige que el ledger #4 del hub registre el sha256 de las atestaciones de Aegis por
   gate. Si Aegis arranca como cadena #4 independiente sin ese enlace, los dos ledgers pueden
   divergir sin traza. Verifica ademas que los 3 firmantes esten operativos en Aegis: llaves
   (event_auth/actor_auth), capabilities maker/checker cruzado equivalentes al hub, y un ciclo e2e
   de humo (task_upsert -> claim -> flip -> release) verde en el ledger de Aegis antes de la primera
   tarea real, INCLUYENDO la verificacion del enlace de cross-atestacion hub->Aegis.
3. Ninguna tarea de Contabilidad queda huerfana entre dos ledgers: si algo ya se encolo en el hub que
   pertenezca al ambito Aegis, migra el asiento de forma gobernada y deja la traza.

## 2. Cola pre-30-jul: los 4 REQs futuros (DECISION primero, implementacion despues)

Los 4 documentos estan en `personal/operador/requerimientos-futuros/` con `decision_required: true` e
`implementation_allowed_before_decision: false`. Su `target_phase` ("despues del cierre de la cola
pesada actual") YA se cumplio: el baseline esta completo. Orden de dependencia fijado:

1. **REQ-ZEUS-AEGIS-SOFTWARE-ENGINEERING-CON-IA-NO-VIBECODING (v0.2.0, priority critical).** Es el
   principio rector; los demas lo citan. Preparar la DECISION corta que fija la identidad y el
   destino de gobierno (los REQs son requisitos, no texto verbatim de la decision).
2. **REQ-ZEUS-AEGIS-INTAKE-PROFESIONAL-REQUERIMIENTOS (v0.2.0).** Ya viene fusionado con el anterior
   segun su update_note; una sola iniciativa, decision y descomposicion en tareas implementables.
3. **REQ-MEMORIA-HIBRIDA-DB-ARCHIVO-FRIO (v0.3.0).** Ruta UNICA de memoria ya fijada por el Operador;
   su decision formal debe SUPERSEDER DECISION-0071 explicitamente. Notar la sinergia con peones
   (seccion 4): la memoria hibrida es prerequisito de que los peones revivan con contexto.
4. **ANALISIS-TRANSCRIPCION-c5Gwx0RcxNE (aprendizajes agentes externos).** NO es entregable propio:
   sus reglas extraibles se absorben como requisitos dentro de las decisiones 1-3 donde apliquen,
   con cita. Nada se copia literal.

Reglas de frontera de esta cola:
- Ambito de implementacion = instancia Aegis y producto Zeus-Aegis. PROHIBIDO tocar el core pineado
  del hub (epoch 1.14.0, protocol.config.json, eventlog/validator pineados por sha256).
- Estas implementaciones NO son unidades medidas de ningun brazo. Si algun paso amenaza la linea roja
  Q4 o el aparato de Etapa 1, se marca, se difiere con nota y el resto sigue.
- La cola PREP ya ruteada (SPECs DECISION-0092 B, hardening SPECs Sprint 1, paquete DEC P3.x) sigue
  vigente; tu decides el interleaving, con el paquete DEC P3.x en alta prioridad porque desbloquea el
  sello de Etapa 2.

## 3. Analisis de migracion de Contabilidad - ARRANCA DE INMEDIATO

- Fuente de verdad: `D:/Agentes/Ingenas/Budget/` (mismo patron del analisis de Presupuesto:
  `01_Sources/code/DbsFinanciero/` VB6 + `01_Sources/Database/dbsystem.mdb` +
  `02_Analysis/Database_Migration/`). Alcance legado estimado: ~57 formularios de Contabilidad y
  ~34 tablas (prefijos maco/Maco/Cont), hoy en estado EN_ESPERA en el indice de migracion.
- Entregable: analisis de migracion equivalente al que tuvo Presupuesto (mapa formularios -> casos de
  uso, tablas Access -> esquema SQL Server `Accounting`, reglas de comprobantes y frontera con
  Budget/Treasury/PayControl ya migrados) + propuesta de descomposicion en unidades implementables
  con estimates S/M/L.
- Gobernanza: desde Aegis (seccion 1). Este analisis es ademas el insumo del corpus candidato del
  sello de Etapa 2 -- las unidades que salgan deben quedar enumerables y con verificacion de
  paridad definible, igual que hizo el sello de Etapa 1 con el pool Q4.

## 4. Peones y costo de tokens - se disena dentro del sello Etapa 2, NO en Sprint 1

- El interes del Operador: medir si el uso de peones reduce el costo de tokens de los modelos
  frontera, con la instrumentacion de cubetas Q1 ya probada (regimen/arranque/overhead separados).
- Restriccion vigente que se RESPETA: el brazo gobernado del contraste central de Etapa 1 se mantiene
  MONO-orquestado; mezclar peones ahi confunde Q1/Q4 y esta prohibido por el sello. TASK-0231 (F6.1)
  NO se activa en el hub por ahora.
- Orden: incluye en el paquete de diseno del sello de Etapa 2 la pregunta "mono vs peones bajo
  gobierno completo, medida en costo de tokens" como contraste candidato pre-registrado sobre
  unidades de Contabilidad, y con la memoria hibrida (seccion 2.3) ya decidida como parte del
  tratamiento declarado.
- **REGLA DE DISENO del sello Etapa 2 (no nota al margen):** las ventanas y aperturas del sello de
  Etapa 2 se definen POR COMPLETITUD CERTIFICADA (certificacion read-only de un tercero de que el
  trabajo previo esta completo y reconciliado), NO por fecha de calendario. Es la correccion del
  punto debil identificado en Etapa 1 (tiempo muerto endogeno de las ventanas por fecha) y queda
  sellada de origen como regla estructural del diseno de Etapa 2.
- **DECIDIDO por el Operador (update 2026-07-06, mismo dia):** F6.1/peones se REDISENA dentro del
  sello de Etapa 2. NO se corre como F6 sobre Presupuesto post-Sprint-1. TASK-0231 se re-alcanza o se
  supersede hacia el diseno de Etapa 2 segun tu criterio de asiento (hub vs Aegis), dejando traza.

## 5. Declaracion de trabajo paralelo (blindaje del reporte de Etapa 1)

Registra desde ya, donde corresponda del aparato de Etapa 1 (nota en el sello o en el material del
reporte), que durante la ventana 06-jul a 30-jul corre en instancia separada: implementacion de los
REQs (seccion 2) y analisis de Contabilidad (seccion 3). La declaracion debe ser ARM-ORTOGONAL, no
solo "existe trabajo paralelo": el trabajo paralelo es de fondo y NO esta correlacionado con la
asignacion ligero/completo de Q4 (ortogonal a la aleatorizacion del sorteo) -- esa no-correlacion es
lo que sostiene la simetria entre brazos y lo que el reporte debe afirmar textualmente. Se declara
como limitacion honesta, no se oculta.

## Higiene de canal

Los mensajes a mi nombre `MSG-20260706-Arquitecto-to-Operador-FYI-cola-prep-sprint1-progreso` y
`MSG-20260706-Arquitecto-to-Operador-RESPUESTA-cola-refill-4items` quedan LEIDOS y consumidos por esta
directiva: puedes archivarlos en tu proximo checkpoint de higiene.

-- Operador
