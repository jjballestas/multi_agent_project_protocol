---
id: TASK-0340
title: El validador canonico lleva seis dias crashing en CI por una dependencia que CI no instala
status: ready
owner: Codex
type: implementation
file: Area_comun/tasks/TASK-0340-el-validador-canonico-lleva-seis-dias-crashing-en-CI.md
created: 2026-08-08
intake:
  type: fix
  goal: >
    El job `validate` de CI lleva rojo desde el 2026-08-02 como minimo -- 300 runs consecutivos sin
    un solo verde. Causa medida: `runtime/eventlog.py:401` importa `InvalidSignature` DENTRO de un
    bloque try, y la clausula `except InvalidSignature` de la linea 414 evalua ese nombre. Si el
    import falla, el propio except lanza UnboundLocalError y enmascara el ImportError original. CI
    instala `jsonschema pyyaml` y nunca `cryptography`, asi que el import falla siempre alli. El
    efecto es que la verificacion de firma de actor NO se ejercita en CI y el gate canonico se cae
    con exit 1 en vez de emitir un veredicto.
  acceptance:
    - "AC1 (falsacion previa): se reproduce el UnboundLocalError ejecutando el validador en un entorno SIN cryptography, y se demuestra que con la libreria presente el mismo codigo no lo lanza. Evidencia por comportamiento."
    - "AC2 (el except deja de depender del try): la clausula de excepcion no puede referenciar un nombre cuyo binding ocurre dentro del bloque protegido. Se corrige de forma que un import fallido produzca un veredicto declarado, nunca un UnboundLocalError."
    - "AC3 (que pasa sin la libreria, DECLARADO): se decide y se declara explicitamente el comportamiento cuando cryptography no esta disponible -- verificacion no disponible y gate rojo con motivo, o cualquier otra semantica -- y se escribe en el codigo. Lo que NO vale es degradar en silencio a 'firma invalida' o a 'firma omitida'."
    - "AC4 (CI ejercita la verificacion de VERDAD): CI instala la dependencia necesaria para que la verificacion de firma de actor se ejecute realmente, en TODOS los jobs que corren el validador. Se mide que la verificacion se ejercita, no solo que el job sale verde."
    - "AC5 (contrato): negativo permanente que caiga si el validador vuelve a poder crashear por una dependencia ausente, o si un job que corre el validador deja de instalar lo que necesita, verificado por MUTACION."
    - "AC6 (CI verde, medido en CI): el job `validate` sale success en un run REAL de GitHub Actions, y se cita el id del run. No basta el clon limpio local: es exactamente la verificacion que fallo durante seis dias."
  verification_cmd:
    - "python scripts/validate_collaboration_state.py --root ."
    - "python scripts/check_falsification_contracts.py --root ."
    - "python scripts/scan_encoding.py --root ."
  scope_routes:
    - runtime/eventlog.py
    - .github/workflows/validate.yml
    - Area_comun/protocol/FALSIFICATION_CONTRACTS.json
    - examples/
  out_of_scope:
    - "El rojo de `falsification-runners`, que es una regresion distinta y de hoy (contrato de subcadenas roto por TASK-0331)."
    - "Cualquier cambio en la semantica de firma mas alla de declarar el comportamiento sin la libreria."
    - "Codigo de producto."
  risk: high
  estimate: M
---

# TASK-0340 -- el gate canonico lleva 300 runs sin emitir veredicto

## Lo medido

    gh run list --limit 300   ->  0 verdes, 300 rojos
    ventana                   ->  2026-08-02T08:49 .. 2026-08-08T09:45

Traza de CI, identica en todos los inspeccionados:

    File "runtime/eventlog.py", line 414, in verify_actor_auth
        except InvalidSignature:
    UnboundLocalError: cannot access local variable 'InvalidSignature'
                       where it is not associated with a value

## El bug

    try:
        from cryptography.exceptions import InvalidSignature      # 401, DENTRO del try
        ...
        key.verify(raw_signature, actor_auth_message(event))
        return {"valid": True, "reason": "valid"}
    except InvalidSignature:                                      # 414
        return {"valid": False, "reason": "invalid_signature"}
    except Exception:
        return {"valid": False, "reason": "invalid_signature"}

Si el import de la 401 falla, Python evalua `except InvalidSignature` con el nombre sin ligar y
lanza `UnboundLocalError`. El `except Exception` de mas abajo **no llega a cubrirlo**, porque el
fallo ocurre al evaluar el tipo de la clausula anterior, no dentro del bloque.

`.github/workflows/validate.yml` instala `jsonschema pyyaml` (linea 26) y `jsonschema` (linea 281).
**Nunca `cryptography`.** Localmente si esta instalada, y por eso el gate sale verde en cada clon
limpio que hemos corrido.

## Por que es grave, y no solo ruidoso

1. **El gate canonico no ha emitido veredicto en seis dias.** No es que dijera "rojo por un motivo
   conocido": se caia antes de mirar nada. Todo lo que hemos declarado verde en esa ventana lo esta
   solo en local.
2. **La verificacion de firma de actor no se ejercita en CI.** Sin `cryptography` no hay ed25519, y
   la capa de atestacion que justifica el proyecto entero no se comprueba donde importa.
3. **El modo de fallo enmascara su propia causa.** El UnboundLocalError oculta el ImportError, asi
   que la traza no dice "falta cryptography" sino algo que parece un bug de logica.

## Nota de proceso, que va en el contrato a proposito

El AC6 exige un run REAL de GitHub Actions en verde, citando su id. Es deliberado: durante seis dias
hemos verificado en clon limpio local y llamado a eso "gates verdes". El clon limpio es necesario y
no basta. Esta tarea no se cierra con evidencia local.
