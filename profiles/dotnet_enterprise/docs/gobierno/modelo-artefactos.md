# Modelo de artefactos — Desarrollo_DotNet

## Objetivo

Definir qué artefacto produce el pipeline, cómo se versiona y cómo se distribuye a los entornos de despliegue.

---

## Tipo de artefacto

Las aplicaciones .NET del entorno se publican como **carpeta publicada** (`dotnet publish`) empaquetada en un archivo `.zip`, almacenada en Azure Artifacts.

Este modelo es compatible con el despliegue en máquinas virtuales mediante copia directa o script de despliegue.

---

## Convención de versionado

Se usa **versionado semántico**: `MAJOR.MINOR.PATCH`

| Componente | Cuándo cambia |
|---|---|
| `MAJOR` | Cambios incompatibles con versiones anteriores |
| `MINOR` | Funcionalidad nueva compatible |
| `PATCH` | Correcciones de bugs o hotfixes |

El número de versión se gestiona en el archivo `.csproj` de la aplicación:

```xml
<PropertyGroup>
  <Version>1.2.0</Version>
  <AssemblyVersion>1.2.0.0</AssemblyVersion>
</PropertyGroup>
```

El pipeline lee esta versión y la usa para nombrar el artefacto.

---

## Nombre del artefacto

Formato: `[NombreApp]-[Version]-[Entorno].zip`

Ejemplos:
```
AppFacturacion-1.2.0-DEV.zip
AppFacturacion-1.2.0-QA.zip
AppFacturacion-1.2.0-PROD.zip
```

---

## Pasos de generación en el pipeline

Añadir estos pasos al `azure-pipelines.yml` de cada aplicación después del step de tests:

```yaml
- script: dotnet publish --configuration $(buildConfiguration) --output $(Build.ArtifactStagingDirectory)/publish --no-build
  displayName: 'Publish application'

- task: ArchiveFiles@2
  inputs:
    rootFolderOrFile: '$(Build.ArtifactStagingDirectory)/publish'
    includeRootFolder: false
    archiveType: 'zip'
    archiveFile: '$(Build.ArtifactStagingDirectory)/$(Build.Repository.Name)-$(Build.BuildNumber).zip'
    replaceExistingArchive: true
  displayName: 'Package artifact'

- task: PublishBuildArtifacts@1
  inputs:
    PathtoPublish: '$(Build.ArtifactStagingDirectory)'
    ArtifactName: 'drop'
    publishLocation: 'Container'
  displayName: 'Publish artifact to Azure DevOps'
```

---

## Almacenamiento

Los artefactos se almacenan en **Azure Artifacts** dentro del mismo proyecto de Azure DevOps.

Retención recomendada:
- Artefactos de `feature/*`: 7 días
- Artefactos de `develop`: 30 días
- Artefactos de `release/*` y `main`: indefinido (hasta decisión de limpieza)

---

## Promoción entre entornos

El mismo artefacto generado para DEV se promueve a QA y luego a PROD **sin recompilación**. El artefacto no cambia entre entornos; solo cambia la configuración de despliegue.

```
Artefacto v1.2.0
  └─ desplegado en DEV  →  validado
  └─ promovido a QA     →  validado
  └─ promovido a PROD   →  en producción
```

La configuración por entorno (cadenas de conexión, variables) se gestiona en el servidor de destino, no en el artefacto.

---

## Despliegue en máquinas virtuales

El despliegue consiste en:

1. Detener el servicio o proceso de la aplicación en la VM.
2. Descomprimir el nuevo artefacto en el directorio de la aplicación.
3. Restaurar la configuración del entorno (`appsettings.Production.json` o variables del sistema).
4. Reiniciar el servicio.

Este proceso puede automatizarse con un pipeline de release en Azure DevOps o ejecutarse manualmente con validación humana obligatoria para producción.
