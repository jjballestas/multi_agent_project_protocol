# PROMPT para el Arquitecto de NOVA - insumos del sello Etapa 2 (BR-C4 + corpus + status 15-jul)
# Preparado por el hub-Arquitecto 2026-07-14 ~04:25 local. El Operador lo retransmite.
# NOTA AL OPERADOR: adjunta/retransmite tambien el encargo del DBA (personal/asesor/
# DRAFT-ENCARGO-DBA-BR-C4-hardening.md) -- el Arquitecto de NOVA no lee rutas del hub; los
# [PLACEHOLDER] de dominio (tabla de permisos, roles, procs) los completan tu + Julian.

---- PROMPT (paste-ready) ----

Eres el Arquitecto de la instancia NOVA (gobierno en Aegis/). Peticion del hub via Operador
(frontera dos-trios DECISION-0095 del hub: tu trio ejecuta en TU ledger; el hub solo necesita
EVIDENCIA verificable para citarla en su sello de Etapa 2, que firma el Operador antes del
29-jul). Tres encargos, en orden de dureza de fecha:

== 1. BR-C4: sembrado + verificacion de la matriz de autorizacion por operacion ==
DEADLINE DURO: entregado y VERIFICADO <= 29-jul (compromiso ya tomado por el Operador el
6-jul, opcion b del paquete P3.x del hub).

QUE ES: en la BD sandbox del producto (DbsFinanciero_SANDBOX), sembrar la matriz de
autorizacion POR OPERACION para los documentos de la familia P3: Availability/CDP (P3.2),
Commitment/RP (P3.3), Obligation/OBL (P3.4). Principio BR-C4: para cada (documento x
operacion: crear-borrador / aprobar-emitir / anular) se exige un permiso/rol DISTINTO --
emitir != aprobar != anular. Entregables (del encargo que te adjunta el Operador):
(a) filas de la matriz + roles creados; (b) guardas en los procs correspondientes (verifican
el permiso del llamante via SESSION_CONTEXT y hacen THROW con codigo si no lo tiene);
(c) set de codigos THROW nuevo documentado (sin colision con los rangos existentes);
(d) smoke FALSABLE con rollback: caso positivo (usuario con permiso pasa) + control NEGATIVO
(usuario sin permiso -> THROW esperado). El encargo trae los criterios de aceptacion; los
placeholders de dominio los completa el Operador + el DBA.

COMO (tu gobernanza, no la del hub): registra la TASK en TU ledger con intake completo;
owner/maker = jheredia (es trabajo de DBA; NO es dev medido: es HARDENING -- el dev gobernado
de Sprint 1 cableara la superficie C# despues y JAMAS crea los procs); checker = tu Analista
en modo ONE-SHOT (el mismo patron que cerro TASK-9391: contexto propio + clon limpio + firma
analista:v1); maker != checker; tus gates verdes en cada commit.

EVIDENCIA AL HUB: al cerrar VERDE, push a tu main + un FYI corto en tu mailbox con task_id,
commit del cierre, veredicto del checker y el rango de codigos THROW. El hub lo cita en su
sello (confirma pool Q4 n=10 con enmienda fechada). SI NO llega verificado al 29-jul: no hay
drama ni carrera de ultima hora -- el fallback esta PRE-DECLARADO (P3.2/P3.3/P3.4 caen del
pool, n=7); simplemente reportalo igual (el sello registra la caida como prevista, no como
sorpresa). NO comprometas la verificacion por llegar a la fecha: un sembrado sin control
negativo NO cuenta como entregado.

== 2. Corpus de Contabilidad ENUMERABLE ==
FECHA OBJETIVO: <= 25-jul (para que el sello no lo espere al limite).

QUE ES: la lista ENUMERADA de unidades candidatas de Contabilidad derivada del design-source
ya registrado (hito del 11-jul: base solida + WS1 + THROW). Por unidad: id estable, alcance
en 1 frase, y una verificacion de PARIDAD definible (mismo estandar que el pool Q4 del
estudio: que "hecho" sea falsable contra el sistema legado/fuente). NO es build -- solo la
enumeracion con sus criterios. Esto alimenta DOS cosas del sello: la poblacion del contraste
de peones (Q-PEON, que abre post-sello por completitud certificada) y las 6 unidades medidas
del pre-registro N=6 (post-30-jul).

EVIDENCIA AL HUB: artefacto versionado en tu repo (o entregado al Operador) con la lista; el
hub la cita en el sello.

== 3. Status del hardening del 15-jul (solo reporte) ==
El sello registra si el hardening comprometido para el 15-jul entrego los procs PAR-2 /
Annul_* (los items del pool que dependen de eso entran SOLO por enmienda fechada con entrega
comprometida). Manana 15-jul: reporta SI/NO + evidencia breve (commit/objeto BD). Un NO
tambien es informacion valida para el sello.

== Operativa ==
- Julian ya es firmante operativo (gate nominal cerrado) y tienes el harness generico en
  Aegis/scripts/harness/ si decides montar cron -- pero para estos encargos el ONE-SHOT basta.
- Prioridad: 1 > 2 > 3. Si algo bloquea, un mensaje concreto al Operador (no esperes en
  silencio).
- Reporta por push a tu main (el hub tiene watch read-only) + FYI en tu mailbox. Narracion
  minima: un reporte por encargo cerrado.

---- FIN PROMPT ----
