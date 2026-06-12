DRAFT (NO commitear hasta que el operador confirme el tag v1.1.0 sobre 703ed93).
Insertar en README_INSTANCIACION.md justo despues del bloque "### Firma externa de releases"
(tras el parrafo que termina en "...no afirma autenticidad de un release real."), como subseccion
nueva. POST-TAG: queda en main, fuera del release firmado (README esta en el SBOM; por eso NO se
commitea bajo el tag). ASCII puro.

------------------------------------------------------------------------------------------------

#### Receta de verificacion publicada para v1.1.0 (cosign keyless)

> **Fuente firmada autoritativa:** la receta de verificacion AUTORITATIVA (cubierta por la firma del
> release) vive en
> [`Area_comun/reports/REPORT-20260610-release-v1.1.0.md`](Area_comun/reports/REPORT-20260610-release-v1.1.0.md).
> Esta copia en el README es solo para descubrabilidad y **NO esta cubierta por la firma** (este archivo
> esta dentro del SBOM, por lo que se publica en un commit posterior al tag). Ante cualquier duda de
> manipulacion de este README, la fuente firmada es el REPORT.

El release `v1.1.0` esta firmado con cosign keyless (sigstore). Identidad publica del firmante
`john.ballestas@gmail.com`, issuer OIDC `https://accounts.google.com`, transparencia en Rekor
(`logIndex 1777945271`, `https://search.sigstore.dev/?logIndex=1777945271`). Un tercero verifica la
autenticidad con cualquiera de estos dos comandos (cosign requerido en el PATH; la verificacion keyless
consulta Rekor y por tanto requiere red, o un bundle offline):

```text
# cosign directo (autenticidad):
cosign verify-blob --bundle dist/v1.1.0/cosign.bundle.json \
  --certificate-identity john.ballestas@gmail.com \
  --certificate-oidc-issuer https://accounts.google.com \
  dist/v1.1.0/manifest.json

# cadena del protocolo (integridad + procedencia + autenticidad, ok:true global):
python scripts/verify_release.py --root . --manifest dist/v1.1.0/manifest.json \
  --signature dist/v1.1.0/signature.json --backend external-command \
  --verify-command "cosign verify-blob --bundle dist/v1.1.0/cosign.bundle.json \
    --certificate-identity john.ballestas@gmail.com \
    --certificate-oidc-issuer https://accounts.google.com {manifest}"
```
