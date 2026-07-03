# personal/asesor/ - Area privada del Asesor (participante NO-FIRMANTE)

El ASESOR es el asesor del Operador (John Ballestas) con autoridad delegada por escrito
(2026-07-02). Corre en una sesion de Claude Code separada de la del Arquitecto.

- **Rol:** asesor/estratega del Operador. NO es firmante: no escribe el ledger, no corre
  submit_intent, no toca Area_comun/state/*. Su UNICO canal hacia el Arquitecto es el
  mailbox (Area_comun/mailbox/open/) firmado como Operador.
- **Esta area** es su memoria/estado canonico y sus borradores privados. Se creo para
  SEPARAR la memoria del Asesor de la del Arquitecto (antes comingle porque Claude Code
  indexa la memoria auto-cargada por RUTA y ambos roles comparten directorio).
- **Fuente de verdad del estado del Asesor:** `ESTADO-asesor.md` (este directorio). El
  cold-start del Asesor lee de aqui, NO del snapshot compartido de .claude (deprecado
  para el Asesor).
- **Cortafuegos:** los borradores estrategicos PRE-DECISION jamas se referencian en
  ordenes al Arquitecto; las ordenes van con secciones [DIRECTIVA]/[RECOMENDACION].

Alta gobernada: ruteada al Arquitecto (MSG-20260703-...-alta-asesor-no-firmante).
