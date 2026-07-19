---
message_id: MSG-20260719-Operador-to-Arquitecto-ENMIENDA-E4-E5-adoptable-githooks
from: Operador
to: Arquitecto
type: DIRECTIVA
status: open
requires_response: true
response_owner: Arquitecto
requested_action: "Decidir el ruteo de las enmiendas E4 y E5 (conjunto adoptable de .githooks + cableado de core.hooksPath en new_instance.py): plegarlas al acceptance de TASK-0257 o abrirlas como unidad hermana. Confirmar la decision por mailbox; no hace falta parar el fix-loop en curso."
question: "Plegamos E4/E5 al acceptance de TASK-0257 o las abrimos como unidad hermana para no cargar el fix-loop que ya va por la iteracion 1 con tope de 2?"
created_at: 2026-07-19
context_refs:
  - Area_comun/decisions/DECISION-0103-visibilidad-plan-y-reportes-de-turno.md
  - Area_comun/mailbox/open/MSG-20260719-Arquitecto-to-Operador-REPORTE-fixloop-0257-iter1.md
one_line_summary: "ENMIENDA E4/E5 a la C5: .githooks NO esta en el conjunto adoptable de upgrade_instance.py y new_instance.py no cablea core.hooksPath, asi que la C5 seria la UNICA clausula de la 0103 que no viaja a instancias existentes (NOVA incluida). Ruteo a criterio del Arquitecto: plegar a 0257 o unidad hermana, para no cargar un fix-loop con tope de 2 iteraciones."
---

# ENMIENDA E4/E5 - la clausula C5 no viaja a las instancias

Hallazgo del Asesor, verificado en codigo el 19-jul.

## El hueco

`scripts/upgrade_instance.py` define `DEFAULT_ADOPTABLE_GLOBS`:

```
AGENTS.template.md, CLAUDE.template.md, protocol.config.template.json,
Area_comun/README.template.md, Area_comun/state/*.template.json,
Area_comun/protocol/*.md, Area_comun/specs/*_TEMPLATE.md,
profiles/PROFILE_TEMPLATE/**/*, scripts/*.py, scripts/*.ps1,
runtime/**, .github/workflows/validate.yml
```

**`.githooks/**` NO esta en la lista**, y `protocol.config.json` no tiene bloque
`upgrade` que lo anada (verificado: sin bloque upgrade).

Consecuencia: de las 9 unidades de la 0103, la C5 seria **la unica que no llega a las
instancias existentes**. El resto viaja solo -- `validate_collaboration_state.py` por
`scripts/*.py`, `turn_schema.json` y `turn_validate` por `runtime/**`, el CI por su ruta
explicita.

Y muerde de verdad: la instancia de NOVA (`D:/Agentes/NOVA-Suite/NOVA/Aegis`, protocol
1.14.0, con remoto propio) es instancia EXISTENTE, no nueva. Le llega la 0103 por
`upgrade_instance.py`, es decir por el camino donde falta `.githooks`.

## E4 - conjunto adoptable

`.githooks/**` entra al conjunto adoptable (via `DEFAULT_ADOPTABLE_GLOBS` o via
`upgrade.adoptable_globs` en `protocol.config.json`, lo que resulte mas limpio).
Verificacion: `upgrade_instance.py` contra una instancia real reporta el delta de
`.githooks/` como adoptable.

## E5 - cableado en la instanciacion

`new_instance.py` **cablea `core.hooksPath`** al instanciar. Copiar `.githooks/` sin
configurar el path deja el hook igual de muerto que hoy en el hub: el fichero no arma
nada por si solo. Verificacion: instancia nueva en sandbox -> `git config core.hooksPath`
devuelve la ruta y una prueba negativa aborta el commit.

Es el mismo error que motivo la propia C5, un nivel mas arriba: que exista no significa
que este armado.

## Ruteo - criterio tuyo, y con una preferencia declarada

TASK-0257 esta en fix-loop iteracion 1 con tope de 2 y dos defectos reales abiertos
(F-0257-01 juicio staged, F-0257-02 coste 11.5-12.9s sin modo acotado). E4/E5 son
concern distinto de esos dos defectos: no arreglan el hook, arreglan su PROPAGACION.

**Preferencia del Operador: unidad hermana**, para no cargar de alcance un fix-loop que
ya esta contra el tope. Si a tu juicio pesan menos plegadas que separadas, pliegalas y
lo dices. Lo que no quiero es que E4/E5 empujen a 0257 a agotar iteraciones y escalar por
alcance anadido en vez de por los defectos reales.

No hace falta parar nada en curso para responder esto.

-- Operador
