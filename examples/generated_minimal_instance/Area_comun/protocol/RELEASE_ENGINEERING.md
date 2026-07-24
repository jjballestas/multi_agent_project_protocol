# RELEASE_ENGINEERING.md - Cadena de release verificable

Este documento explica como producir y verificar un release del paquete-metodologia con la cadena
implementada en Fase 7:

```text
SBOM -> manifiesto -> provenance -> firma
```

La cadena es aditiva al versionado existente. No cambia el contrato de coordinacion por si sola y no
activa ningun runtime. Su objetivo es que un adoptante pueda comprobar integridad, procedencia y, si el
emisor publica material de verificacion, autenticidad del release.

## Principios

- Determinismo: `commit` y `timestamp` los provee quien publica; los scripts no dependen del reloj ni de red.
- Neutralidad: los artefactos describen el paquete y sus hashes, no logica de dominio.
- Sin secretos: claves privadas, tokens o material real de firma pertenecen al emisor o CI y nunca se
  commitean. La clave fixture de golden es publica, etiquetada como fixture y no sirve para releases reales.
- Off-by-default: sin firma/material de verificacion, `verify_release` valida integridad de contenido, no
  afirma autenticidad.

## Artefactos

| Artefacto | Script | Contenido principal | Verificacion |
|---|---|---|---|
| SBOM | `scripts/generate_sbom.py` | Inventario canonico de archivos del paquete, hashes, tamanos y ejes de version. | Se embebe en el manifiesto. |
| Manifiesto | `scripts/generate_manifest.py` | SBOM + `sbom_hash` + `manifest_hash` + `commit` + `timestamp`. | `scripts/verify_release.py`. |
| Provenance | `scripts/generate_provenance.py` | Builder, commit, proceso declarado y `subject.digest.sha256 = manifest.sbom_hash`. | `generate_provenance.py --verify`. |
| Firma | `scripts/sign_release.py` | Firma de `manifest.sbom_hash` y metadatos del backend. | `verify_release.py --signature ... --pubkey ...`. |

Los wrappers `.ps1` delegan en los scripts Python para mantener paridad operativa.

## Generar un release

Ejemplo con rutas locales de salida. Ajusta `VERSION`, `COMMIT` y `TIMESTAMP` al release que estas
publicando.

```powershell
$VERSION = "v1.0.0"
$COMMIT = git rev-parse HEAD
$TIMESTAMP = "2026-06-07T00:00:00Z"
$OUT = "dist\$VERSION"
New-Item -ItemType Directory -Force $OUT | Out-Null
```

Genera el SBOM si quieres inspeccionarlo por separado:

```powershell
python scripts\generate_sbom.py `
  --root . `
  --commit $COMMIT `
  --timestamp $TIMESTAMP `
  --output "$OUT\sbom.json"
```

Genera el manifiesto. Este paso vuelve a construir el SBOM internamente y registra `sbom_hash`.

```powershell
python scripts\generate_manifest.py `
  --root . `
  --commit $COMMIT `
  --timestamp $TIMESTAMP `
  --output "$OUT\manifest.json"
```

Genera provenance enlazado al manifiesto. `--process` debe describir el proceso o receta usada para
construir el release; no debe contener secretos.

```powershell
python scripts\generate_provenance.py `
  --manifest "$OUT\manifest.json" `
  --builder-id "ci:release" `
  --commit $COMMIT `
  --process "python scripts\generate_manifest.py --root . --commit <commit> --timestamp <timestamp>" `
  --timestamp "2026-06-07T00:01:00Z" `
  --output "$OUT\provenance.json"
```

## Firmar

La politica aceptada en DECISION-0023 dice que se firma el digest del release, concretamente
`manifest.sbom_hash`. El backend real de firma es responsabilidad del emisor o de su CI. Puede ser un wrapper
local sobre cosign, minisign, gpg u otro mecanismo aprobado por la organizacion, pero el material de clave no
entra al repo.

El backend determinista incluido en los golden (`fixture-hmac-sha256`) es solo para pruebas. No lo uses para
publicar releases reales.

El core no commitea configuracion, comandos ni material de un backend real. Antes de un release autentico, el
emisor debe proveer en su entorno de publicacion un backend aprobado o wrapper externo equivalente y validar que
`verify_release` puede comprobar la firma con material publico. Si no hay backend/material publico, publica la
verificacion de integridad y no afirmes autenticidad.

Ejemplo de forma de invocacion con material local del emisor:

```powershell
python scripts\sign_release.py `
  --manifest "$OUT\manifest.json" `
  --backend "<backend-aprobado>" `
  --key "<referencia-local-o-CI>" `
  --key-id "<id-publico-del-emisor>" `
  --output "$OUT\signature.json"
```

Reglas de seguridad:

- No commitear `--key`, claves privadas, tokens, certificados privados ni dumps de CI.
- Publicar solo artefactos publicos: manifiesto, provenance, firma y, si aplica, clave publica o referencia de
  verificacion.
- Si el backend real requiere un comando externo, documentarlo en la instancia o pipeline del emisor, no en el
  core generico con credenciales reales.

## Verificar un release

Verificacion de integridad: recompone el SBOM del arbol y compara contra `manifest.sbom_hash`.

```powershell
python scripts\verify_release.py `
  --root . `
  --manifest "$OUT\manifest.json" `
  --output "$OUT\verify.integrity.json"
```

Verificacion de provenance: confirma que `subject.digest.sha256` coincide con el `sbom_hash` del manifiesto.

```powershell
python scripts\generate_provenance.py `
  --verify `
  --manifest "$OUT\manifest.json" `
  --provenance "$OUT\provenance.json" `
  --output "$OUT\verify.provenance.json"
```

Verificacion con firma: exige firma y material publico de verificacion. Si falta material, el verificador falla
cerrado para autenticidad.

```powershell
python scripts\verify_release.py `
  --root . `
  --manifest "$OUT\manifest.json" `
  --signature "$OUT\signature.json" `
  --backend "<backend-aprobado>" `
  --pubkey "<referencia-publica>" `
  --output "$OUT\verify.signed.json"
```

Interpretacion:

- `ok: true` sin bloque `signature` significa integridad de contenido verificada.
- `ok: true` con `signature.ok: true` significa integridad y autenticidad verificadas para el backend/material
  provisto.
- `ok: false` con diferencias en `diff` indica archivos cambiados, faltantes o extra.
- `ok: false` en `signature` indica que la firma no cubre el `sbom_hash`, no verifica con el material dado, o
  falta material publico.

## Checklist de publicacion

1. Fijar version, commit y timestamp provistos.
2. Generar `manifest.json`.
3. Generar `provenance.json` contra el manifiesto.
4. Verificar integridad y provenance localmente.
5. Firmar `manifest.sbom_hash` con backend/material del emisor fuera del repo.
6. Verificar la firma con material publico.
7. Publicar los artefactos publicos junto al tag/release.
8. Registrar en el reporte humano de release que la cadena SBOM/manifiesto/provenance/firma fue generada y
   verificada.

## Relacion con versionado

Los ejes de version (`protocol_version`, `runtime_version`, `schema_version`, `profile_version`) se registran
en el SBOM/manifiesto para que el adoptante sepa que contrato esta verificando. Ver
`Area_comun/protocol/PACKAGE_VERSIONING.md` para las reglas de adopcion y migracion.
