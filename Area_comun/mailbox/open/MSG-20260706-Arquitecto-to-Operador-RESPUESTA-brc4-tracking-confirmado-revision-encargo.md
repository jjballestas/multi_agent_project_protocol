---
message_id: MSG-20260706-Arquitecto-to-Operador-RESPUESTA-brc4-tracking-confirmado-revision-encargo
from: Arquitecto
to: Operador
type: HANDOFF
status: open
requires_response: false
created_at: 2026-07-06
context_refs:
  - Area_comun/mailbox/archived/MSG-20260706-Operador-to-Arquitecto-ACTION-brc4-opcion-b-dba-encargo.md
  - Area_comun/artifacts/PAQUETE-DEC-DOMINIO-P3x-sello-etapa2.md
  - personal/asesor/DRAFT-ENCARGO-DBA-BR-C4-hardening.md
one_line_summary: "BR-C4 opcion (b) CONFIRMADO y trackeado (deadline duro 29-jul, auto-fallback n=7 sin accion; traza en el paquete DEC). Revision adversarial del encargo del DBA: solido, con 4 endurecimientos concretos propuestos antes de entregarlo. LOTE-PENDIENTE-OPERADOR = 4/4 DRENADO."
requested_action: "Ninguna obligatoria. Si acoges los 4 endurecimientos, que el Asesor los hornee en el encargo antes de entregarlo al DBA (son adiciones a s.4, no cambian el alcance)."
---

# RESPUESTA - BR-C4 tracking confirmado + revision del encargo (06:20 local, 2026-07-06)

## 1. Tracking CONFIRMADO (tu parte queda ejecutada de mi lado)

- **P3.2/P3.3/P3.4 = elegibilidad Q4 CONDICIONAL, deadline duro <= 29-jul, auto-fallback a n=7**
  sin decision nueva (es la condicion YA sellada, s.3). Traza registrada en el paquete DEC
  (RESOLUCION DEL OPERADOR) -- el paquete P3.x queda CERRADO.
- La enmienda fechada del sello se registra AL ENTREGAR el DBA verificado (formato s.24/s.25),
  no antes -- tal como ordenaste. Punto de verificacion natural: ventana de reconciliacion
  26..29-jul (ya en mi prompt de arranque y memoria persistente).

## 2. Revision adversarial del encargo del Asesor: SOLIDO, 4 endurecimientos propuestos

El encargo espeja bien s.24 (OBJECT_DEFINITION, 3 identidades, guard de entorno, verificador
no-sysadmin, rango THROW anti-colision). Cuatro huecos que valdria cerrar en s.4 (lecciones
pagadas de F-NOVA-01 y del baseline):

1. **Cruce lista-vs-lista del set THROW (leccion P3-005):** exigir que el set THROW DOCUMENTADO
   en la entrega se re-verifique contra el set REAL de los procs desplegados via
   OBJECT_DEFINITION (lista contra lista, no spot-check). El set documentado casi siempre
   difiere del real; s.4 hoy pide "la guarda visible" pero no el cruce completo del set.
2. **Separacion ENTRE DOCUMENTOS, no solo entre operaciones:** el smoke de 3 identidades prueba
   emitir != aprobar != anular DENTRO de un documento. Falta la prueba negativa cruzada: el
   aprobador de CDP debe ser BLOQUEADO al aprobar RP y OBL (permiso por celda documento x
   operacion, no rol grueso "aprobador"). Sin esto, un rol coarse pasa el smoke y la matriz no
   es realmente por-celda. Sugerencia: 1 identidad extra o reusar las 3 cruzandolas (9 casos
   negativos minimos).
3. **Fail-closed sin SESSION_CONTEXT:** llamada SIN SESSION_CONTEXT de usuario -> THROW (familia
   50100, mismo patron ya desplegado en P4.x). Si el contexto ausente cae en default-permitir,
   la guarda es bypasseable y el smoke de identidades no lo detecta.
4. **Preflight AMPLIADO del grant (leccion s.24):** el grant de verificacion debe enumerarse
   desde el CODIGO REAL de las guardas nuevas (todas las tablas/vistas que consulten: matriz,
   roles, usuarios), concedido de una vez -- no descubrir permisos uno-por-uno via SQL 229
   durante la verificacion.

Extra menor (transparencia, patron hallazgo #10): registrar el rango 50300-50319 tambien en el
diccionario/log de cambios del producto al cablearse en Sprint 1.

## 3. Estado del LOTE: 4/4 DRENADO

Con BR-C4 adjudicado, el LOTE-PENDIENTE-OPERADOR queda completamente drenado (firmantes + humo
e2e verde, DECISION-1001/1002 registradas, remoto GitHub con branch model resuelto, BR-C4
trackeado). Queda vivo de fondo: gate 2-clones pre-Contabilidad, promocion de las primeras
tareas 1001/1002 cuando fijes orden, veredictos del Analista #10/#11-13, y tu preferencia
opcional repo-separado vs rama aegis/main.

-- Arquitecto
