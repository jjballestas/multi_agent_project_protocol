---
spec_id: SPEC-0057-fase7-release-engineering
task_id: TASK-0071
type: implementation
status: accepted
created_at: 2026-06-07
author: Claude (arquitecto)
linked_decisions: [DECISION-0001, DECISION-0019, DECISION-0021]
relates_to: [PACKAGE_VERSIONING, SPEC-0043]
---

> Fase 7 (release engineering) aprobada por el operador 2026-06-07. Decomposicion en rebanadas aditivas;
> la primera (F7.1 SBOM) es la de menor riesgo. Aditivo al proceso de release (DECISION-0001), neutral, sin
> secretos. Promover de a una (DECISION-0020).

# SPEC-0057 - Fase 7: Release engineering (cadena de suministro del paquete)

## 1. Objetivo

Endurecer COMO se publica y COMO se verifica el paquete-metodologia: que un adoptante pueda confirmar
criptograficamente que recibe exactamente lo publicado (procedencia + integridad), sin manipulacion. Hoy el
release es tag + CHANGELOG + reporte humano (DECISION-0001); Fase 7 agrega SBOM, provenance, firma y
verificacion automatizable, de forma aditiva.

## 2. Decomposicion en rebanadas (aditivas, gateadas, neutral, sin secretos)

- **F7.1 (TASK-0071, esta): SBOM determinista.** Script que genera un inventario verificable del paquete
  para un release: archivos del nucleo/runtime/scripts/plantillas/perfiles + los 4 ejes de version
  (protocol/runtime/schema/profile, ver PACKAGE_VERSIONING) + hash canonico por archivo. Determinista
  (sin reloj/red; timestamp/commit provistos), salida estable (orden canonico). Golden + CI. Sin firma aun.
- **F7.2 (gateada): manifiesto de release + verificacion de integridad.** Un manifiesto (SBOM + version axes
  + hash global) y un comando `verify` que recomputa el SBOM y confirma integridad (hash) de un arbol/release.
  Sin claves externas todavia (integridad por contenido).
- **F7.3 (gateada): provenance / atestacion.** Registro estructurado y verificable de quien/que-commit/que-
  proceso construyo el release (estilo build attestation / SLSA-lite), enlazado al manifiesto.
- **F7.4 (gateada, probable DECISION nueva): firma.** Firmar el manifiesto/tag (material de clave local/CI,
  NUNCA commiteado; analogo a DECISION-0021); `verify` valida la firma. Politica de firma = DECISION.
- **F7.5 (gateada): docs + integracion al flujo de release.** Como producir un release endurecido
  (SBOM+provenance+firma) y como un adoptante lo verifica; integrar a PACKAGE_VERSIONING + CHANGELOG +
  reporte humano.

## 3. Alcance de F7.1 (TASK-0071) - SBOM determinista

1. `scripts/generate_sbom.py` (+ paridad o delegacion `.ps1`): genera un SBOM canonico del paquete.
   - Inventario: lista determinista de archivos del paquete (excluyendo estado/runs/efimeros: usar un
     conjunto explicito de globs de "fuente del paquete", NO instancia/estado).
   - Por archivo: ruta relativa (posix) + hash sha256 + tamano.
   - Cabecera: los 4 ejes de version leidos de protocol.config.json/turn_schema/profiles + commit + timestamp
     (ambos PROVISTOS como argumento para determinismo; sin reloj/red).
   - Salida JSON canonica (orden estable, ASCII/sin BOM) a stdout o a un path dado.
2. Determinismo: dos corridas con el mismo arbol + mismos commit/timestamp => salida byte-identica.
3. Neutralidad/sin secretos: el SBOM lista rutas + hashes (no contenido); no incrusta estado de dominio.
4. Golden `examples/sbom_cases` + CI.

## 4. Tests (F7.1, golden determinista, sin red)

1. SBOM de un arbol fijo => salida canonica esperada (rutas + sha256 + tamano + 4 ejes + commit/timestamp provistos).
2. Determinismo: dos corridas identicas => byte-identico.
3. Un archivo cambiado => su hash cambia en el SBOM (deteccion de cambio).
4. Excluye estado/efimeros (runtime/state, runtime/runs, .git, __pycache__): no aparecen en el SBOM.
5. Regresion: gates py/ps verdes; el SBOM en si no debe disparar neutralidad (lista rutas/hashes).

## 5. Fuera de alcance (F7.1)

- Firma y provenance (F7.3/F7.4). Verificacion de un release publicado (F7.2). Integracion al flujo de
  release (F7.5). Cualquier secreto/clave. Cambios al contrato de coordinacion o al turn schema.

## 6. SemVer

- MINOR (herramienta aditiva de release engineering; no cambia contrato ni nucleo). F7.4 (firma) evaluara
  DECISION + SemVer al llegar.

## 7. Secuencia

Promover TASK-0071 (F7.1) cuando la cola este libre (tras cerrar TASK-0070 y re-aplicar la activacion sombra;
o como siguiente tarea de Codex). Promover de a una (DECISION-0020). Las rebanadas F7.2-F7.5 se especifican/
encolan despues, una a una.
