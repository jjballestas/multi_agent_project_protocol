---
id: TASK-0369
title: La seccion normativa de la SPEC contradice al motor en tres puntos, y una allowlist cuya lista publicada difiere de la efectiva deja de ser allowlist
status: proposed
owner: Arquitecto
type: doc
file: Area_comun/tasks/TASK-0369-la-seccion-normativa-de-la-spec-contradice-al-motor.md
created: 2026-08-12
reviewer: Analista
intake:
  type: doc
  goal: >
    Bloqueante B2 del veredicto formal de TASK-0365, y es del lado del TEXTO: mio. La s.7 de
    SPEC-MEMORIA-HIBRIDA -- la seccion normativa a la que remite el invariante I3 -- contradice al
    motor en tres puntos. Dos de ellos los AUTORIZO el hallazgo P7 del port y la s.7 nunca se
    transcribio: `title` acepta UTF-8 y la s.7 dice ASCII, y el tope real es 500 mientras la s.7 dice
    200. Esos dos son contradicciones internas de la SPEC contra si misma. El tercero no lo autorizo
    nadie: `applies_to` se INDEXA (esta en la allowlist efectiva de `build_memory_db.py`) y no figura
    en la lista de 20 claves que la s.7 publica -- aunque la propia s.7 la usa como columna de
    `policy_status`. Una allowlist cuya lista publicada difiere de la efectiva deja de ser allowlist:
    quien la lee para saber que se indexa obtiene una respuesta falsa, y es precisamente la lista que
    I3 usa para prometer que el indice no lleva texto libre.
  acceptance:
    - "AC1 (las tres divergencias cerradas, cada una por su via correcta): para cada uno de los tres
      puntos se declara si el TEXTO se alinea al motor o el MOTOR al texto, y por que. Los dos de P7
      se transcriben al texto porque el cambio ya estaba autorizado y solo falto escribirlo. El de
      `applies_to` se resuelve declarando su autorizacion con motivo -- la propia s.7 lo exige como
      columna de `policy_status`, asi que indexarlo era necesario y lo que falto fue publicarlo."
    - "AC2 (la lista publicada se DERIVA de la efectiva, no se copia): tras el cambio existe una
      comprobacion que falla si la allowlist publicada en la s.7 y la que el motor aplica vuelven a
      divergir. Copiarlas a mano no acredita: hoy divergen precisamente porque alguien las copio una
      vez. La comprobacion se acredita por conducta, anadiendo una clave en un lado y viendo el rojo."
    - "AC3 (el negativo de I3 sigue vivo): tras el cambio, el indice sigue sin admitir texto libre.
      Se acredita midiendo sobre la DB construida que la unica fuente de `search_terms` sigue siendo
      `metadata_allowlist` y que los excerpts y las banderas de PII siguen a cero, como midio el
      checker en el veredicto (4797 filas, 0 excerpts, 0 `public_plane_allowed`, 0 `is_pii_safe`)."
    - "AC4 (P4 cerrado de paso, que es del texto): `build_memory_db.py:9` conserva una mencion de
      producto que el hallazgo P4 mandaba quitar y que `scan_domain_neutrality` no caza. Se quita y
      se declara por que el escaner no la vio -- si el escaner deberia haberla visto, eso es un
      hallazgo aparte y se dice, no se arregla de paso."
    - "AC5 (la SPEC no sale de draft con esta tarea): esta tarea cierra el bloqueante del TEXTO. La
      SPEC no puede dejar `draft-reviewed-informal` hasta que TASK-0368 cierre tambien; se declara
      explicitamente para que el cierre de esta no se lea como el cierre de la review."
  verification_cmd:
    - "python scripts/memory/test_memory_db.py"
    - "python scripts/scan_domain_neutrality.py --root ."
    - "python scripts/validate_collaboration_state.py --root ."
  scope_routes:
    - Area_comun/specs/SPEC-MEMORIA-HIBRIDA.md
    - scripts/memory/build_memory_db.py
  out_of_scope:
    - "El mapeo de `status` a estado de politica: es TASK-0368, del lado del MOTOR, y es el otro
      bloqueante del mismo veredicto."
    - "Los nueve residuales censados en el artefacto del veredicto que no bloquean (aristas
      `implements` inertes, alcance de la deteccion agrupada de IBAN, siglas de id fiscal por lista,
      cardinales sin poblacion nombrada): cada uno con su tarea si se decide abrirlas."
    - "Reescribir la SPEC mas alla de las divergencias medidas: se transcribe lo que el motor hace,
      no se aprovecha para rediseniar."
  risk: low
  estimate: S
---

# TASK-0369 -- la seccion normativa contra el motor

## Las tres divergencias, medidas por el checker

    applies_to   el motor lo INDEXA; la s.7 no lo lista entre sus 20 claves
                 (y la propia s.7 lo usa como columna de policy_status)
    title        el motor acepta UTF-8; la s.7 dice ASCII          <- P7 lo autorizo
    tope         el motor usa 500; la s.7 dice 200                 <- P7 lo autorizo

## Por que el tercero es distinto de los dos primeros

Los dos primeros son transcripcion pendiente: el port los autorizo y nadie bajo el cambio al texto
normativo. El tercero es una allowlist que no dice la verdad sobre si misma. El invariante I3 se
apoya en esa lista para prometer que el indice no lleva texto libre; si la lista publicada no es la
efectiva, la promesa se verifica contra el documento equivocado.

La correccion no es copiar la lista buena encima de la mala -- hoy divergen justamente porque alguien
las copio una vez y despues el motor siguio andando. AC2 pide que una vuelva a DERIVARSE de la otra,
o que exista una puerta que las ate.
