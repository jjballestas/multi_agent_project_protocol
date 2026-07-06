---
message_id: MSG-20260706-Operador-to-Arquitecto-ACTION-nota-isomorfismo-s23-s21
from: Operador
to: Arquitecto
type: ACTION
status: archived
requires_response: true
response_owner: Arquitecto
created_at: 2026-07-06
context_refs:
  - personal/operador/vision-nova/SELLO-ETAPA-1-nova-budget-DRAFT.md
one_line_summary: "DIRECTIVA operador: anadir NOTA DE ISOMORFISMO al sorteo del miembro baseline de PAR-2 (s.23) y por simetria a PAR-1 (s.21) -- blinda el desempate alfabetico (aplicado post-empate con semilla ya publica) declarando que es INTRASCENDENTE porque los miembros del par son isomorfos: el desempate no puede sesgar el contraste."
requested_action: "Anadir una NOTA DE ISOMORFISMO a la enmienda s.23 (y espejo en s.21) del SELLO-ETAPA-1. Es documentacion/blindaje: NO reabre el sello, NO cambia ninguna asignacion baseline/gobernado ya fijada, NO toca datos medidos ni la cadena #4 (cero re-genesis). Solo hornea el razonamiento que vuelve defendible el desempate. Texto recomendado abajo (ajusta la forma a tu estilo de enmienda fechada). Atesta el sha256 como en las demas enmiendas."
question: "Aplicas la NOTA DE ISOMORFISMO en s.23 + s.21 con este contenido? Si tu lectura del isomorfismo difiere (p.ej. algun matiz que rompa la simetria), dimelo antes de sellarla."
---

# ACTION - Nota de isomorfismo para blindar el desempate del sorteo (s.23 / s.21)

## Por que
El sorteo del miembro baseline de PAR-2 (s.23) dio EMPATE (ambos `h[0]` pares) y se resolvio con un
desempate alfabetico fijado por el Operador DESPUES de ver el empate, con la semilla NIST 1844242 ya
publica desde el sello Etapa 1. En abstracto, una regla post-resultado con semilla publica es un punto
debil de defensibilidad (atacable como "moldeable" en revision/publicacion). Lo que lo vuelve INOFENSIVO
-- y hay que dejarlo ESCRITO -- es que los dos miembros del par son ISOMORFOS: si son isomorfos, da igual
cual quede baseline vs gobernado, el desempate no tiene grado de libertad para sesgar el contraste.

## Texto recomendado (NOTA DE ISOMORFISMO, para s.23)
> NOTA DE ISOMORFISMO (blindaje del desempate): los dos miembros de PAR-2
> (`Annul_Availability_Certificate` / `Annul_Commitment`) son ISOMORFOS -- mismo estrato M/M, mismo patron
> "solo superficie API", procs espejo (anulacion de CDP vs anulacion de RP) con sets de THROW paralelos
> (50100 + 50280-50287 vs 50100 + 50290-50297), ambos construidos y verificados por el DBA con el mismo
> preflight ampliado (s.24). En consecuencia, el desempate alfabetico -- aunque se aplico DESPUES de conocer
> el empate y con la semilla ya publica -- es INTRASCENDENTE para el contraste: cualquiera que fuese el
> miembro baseline vs gobernado, la comparacion pareada no se sesga (no hay grado de libertad que la
> eleccion pueda explotar para favorecer un resultado). La regla la fijo el Operador (autoridad de dominio),
> no una discrecion del Arquitecto.

## Espejo en s.21 (PAR-1)
Anadir la misma nota, adaptada: P4.2 / P4.3 (`Apply_Availability_Adjustment` / `Apply_Commitment_Adjustment`)
son S/S ISOMORFAS (ya declarado asi en s.4, tabla de pares), procs de ajuste existentes espejo; el desempate
de s.21 es igualmente intrascendente por el mismo argumento.

## Alcance / limite
Documentacion de rigor, no cambia resultados: las asignaciones (Annul_Availability_Certificate = baseline
PAR-2; P4.2 = baseline PAR-1) SE MANTIENEN. Es cosmetico-de-defensibilidad, no bloqueante; se pidio ahora
para cerrarlo antes del cierre duro (25-jul) y dejar el sello a prueba de la objecion en publicacion.
