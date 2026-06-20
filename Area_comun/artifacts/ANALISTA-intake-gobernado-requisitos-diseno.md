# ANALISTA - Requisitos de diseno (lente honestidad/metodologia/neutralidad) - INTAKE GOBERNADO de historias

> Voz: Analista. Firma: Analista. Fecha: 2026-06-20. Insumo para Claude Design + para la SPEC del Arquitecto.
> NO disena la UI, NO muta estado, NO promueve. Entrega: REQUISITOS que el diseno DEBE honrar, falsables.
> Pull real: conducir nova.budget desde el front. Feature = el operador monta una historia/requisito en un
> wizard y la envia como artefacto de requisito GOBERNADO por submit_intent (execute + confirmacion); el
> Arquitecto la convierte en SPEC. El front es CLIENTE, no escritor.

## Anclajes verificados (no asumidos)
- GO en canonico: commit `98410ce` ("front intake gobernado de historias -> Arquitecto autora SPEC").
- `DECISION-0040` (GATE-DATASET / dos planos / cero PII de terceros): canonica.
- `TASK-0118` (DEF-PII = detector de PII real + exporter del plano publicable): **status `proposed`** ->
  el detector automatico de PII **NO existe aun**. La guarda de PII del diseno NO puede apoyarse en un
  scanner inexistente: debe ser estructural + advertencia.
- Front ya implementa `dry_run` (preview, HTTP 200) vs `execute` + `confirm:"SUBMIT_INTENT"` (else 409) en
  `Zeus-protocol/src/server.js`. El intake REUSA ese camino gobernado; NO crea un segundo escritor.

## Formato: por punto -> REQUISITO / MODO DE FALLA que descarta / como se ve HONESTO

### 1. Read vs Write visualmente distintos (montar/enviar una historia ES escribir)
- **REQUISITO:** la accion de montar/enviar se presenta como ESCRITURA gobernada, visualmente distinta del
  modo lectura (affordance/color de "operar", no de "observar"), con **paso de confirmacion explicito** que
  declara "esto encola un intent via submit_intent" y nombra el writer (`runtime/submit_intent.py`). "Enviar"
  no ejecuta hasta la confirmacion.
- **MODO DE FALLA (descartado):** un "Enviar" de un clic sin confirmacion; o un formulario tipo "Guardar
  historia" que sugiera editar/guardar directo (escritura directa al ledger).
- **HONESTO:** dos pasos visibles (Componer -> Confirmar y enviar); el confirm declara intent + writer +
  "el front no escribe el ledger, encola un intent".

### 2. Honestidad de estado + tercer estado (preview dry_run != envio execute)
- **REQUISITO:** el PREVIEW del intent (dry_run) se distingue inequivocamente del ENVIO real (execute
  confirmado): "PREVIEW (dry-run) - NO enviado" vs "ENVIADO - evento gobernado". Ningun feedback verde de
  "enviado/atestado" sin la respuesta real del submit_intent (execute ok). Estados cargando / indeterminado /
  error marcados; si el envio falla o no se confirma, NO verde. (Mapea al backend ya existente: dry_run=200
  vs execute+confirm; el diseno lo refleja, no lo inventa.)
- **MODO DE FALLA:** badge "enviado" verde tras el preview (sin execute); spinner que queda verde si la
  llamada falla; confundir dry-run con envio.
- **HONESTO:** preview en ambar/neutral "borrador, no enviado"; verde SOLO tras execute ok, mostrando el
  seq/id del evento; fallo en rojo con el motivo real.

### 3. Guarda PII innegociable (el diseno IMPIDE la fuga, no la deja pasar)
- **REQUISITO:** el texto libre de la historia (narrativa, intencion de aceptacion) puede traer PII de
  terceros de Budget (NIT, razon social, payloads SQL). El diseno DEBE: (a) **separar** la "intencion en
  lenguaje llano" (plano publicable, sin PII) de cualquier dato sensible (que NO va al evento); (b) en
  cualquier plano publicable/exportable, mostrar el texto libre **redactado/marcado**; (c) respetar **canal
  ASCII**; (d) **advertir al operador en compose y en confirm**: "no incluyas PII de terceros (NIT, razon
  social, datos SQL)". Como NO hay detector automatico (TASK-0118/DEF-PII proposed), la guarda es
  estructural + advertencia, no "el scanner lo atrapa".
- **MODO DE FALLA:** mostrar/exportar el texto libre crudo en un plano publicable; asumir un scanner de PII
  que no existe; permitir no-ASCII al canal; un solo campo que mezcle intencion publicable con payload
  sensible.
- **HONESTO:** aviso PII visible en compose y confirm; preview del plano publicable con el texto libre
  redactado/marcado; coherente con DECISION-0040 (dos planos: el evento lleva plano de protocolo, no PII).

### 4. Roles/SDD visibles (el wizard captura SEMILLA, no SPEC)
- **REQUISITO:** el wizard captura la SEMILLA (titulo, narrativa, intencion de aceptacion en lenguaje llano,
  proyecto destino) = un REQUISITO, NO una SPEC. El diseno deja claro que **el Arquitecto autora la SPEC
  (AC + test_plan) DESPUES**; el operador NO firma AC ni cierra DoD aqui.
- **MODO DE FALLA:** campos "acceptance criteria"/"test plan" que hagan creer que el operador escribe la
  SPEC; lenguaje "crear SPEC"/"definir AC".
- **HONESTO:** rotulo "Historia / requisito (semilla para SDD)"; nota "El Arquitecto la convertira en SPEC
  con AC y test_plan"; se pide intencion en lenguaje llano, no AC formales.

### 5. Trazabilidad (evento gobernado atribuido al operador, con huella)
- **REQUISITO:** el intake queda como evento gobernado **atribuido al operador**; el diseno muestra que cada
  envio deja huella (id del requisito + seq del evento, idempotente, con confirmacion). Tras enviar, se ve el
  identificador y su estado.
- **MODO DE FALLA:** envio sin recibo/huella; reenvio que duplica (idempotencia no visible); autoria difusa.
- **HONESTO:** tras execute, "Requisito REQ-xxxx encolado - evento seq N, actor: operador"; el boton se
  deshabilita tras enviar (idempotencia), reintento explicito y marcado.

### 6. Neutralidad (el dominio vive en el producto, no en el nucleo)
- **REQUISITO:** el diseno NO mete dominio/negocio (reglas fiscales, terminos de trading/presupuesto) en el
  NUCLEO neutral del protocolo; la feature vive en el PRODUCTO (Zeus-protocol). "Proyecto destino" es un
  selector de entidad, no logica de dominio embebida. Reusa el design-system neutral
  (governed-action/badges) sin terminos de dominio.
- **MODO DE FALLA:** labels/campos de dominio (fiscal, NIT como concepto de primera clase) presentados como
  parte del protocolo/core; copiar reglas de negocio al design-system neutral.
- **HONESTO:** el dominio (nova.budget) aparece solo como DATO (nombre de proyecto/entidad); los componentes
  reutilizados siguen neutrales.

### 7. Modos de falla a EVITAR (consolidado - el diseno debe poder demostrar que NINGUNO ocurre)
- Pantalla que parezca **escribir directo el ledger** -> viola P1 (front cliente).
- **Verde falso** (enviado/atestado sin verificacion real) -> viola P2.
- **Texto libre crudo expuesto** en plano publicable -> viola P3 / DECISION-0040.
- Un **"enviar" sin confirmacion** (un clic muta) -> viola P1.
Criterio de cierre del diseno: para cada uno, existe en la maqueta la evidencia de que NO pasa (paso de
confirmacion presente, badge derivado, texto redactado, dos pasos compose->confirm).

## Nota transversal (metodologia)
El intake es una NUEVA accion gobernada, no un nuevo camino de escritura: debe colgar del patron existente
`governed-action` / pantalla "Acciones gobernadas" (dry_run preview + execute confirmado), para no introducir
un segundo escritor ni una superficie de bypass. Esto reduce el riesgo y mantiene un solo writer.

## Que NO hice (a proposito)
- No disene la UI (eso es Claude Design); entregue requisitos falsables desde mi lente.
- No promovi, no mute estado, no autore la SPEC (eso es del Arquitecto).
- No asumi un detector de PII inexistente (TASK-0118 proposed): la guarda de diseno es estructural.
