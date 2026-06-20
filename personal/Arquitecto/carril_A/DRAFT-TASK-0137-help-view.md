# DRAFT - TASK-0137: Vista Help (manual de metodologia + consola), read-only (SPEC-0086 ext4, AC23)

> DRAFT en personal/Arquitecto; NO promovido. Espera ratificacion (REQ-FB27AF72 -> SPEC-0086 ext4).
> maker=Codex / checker=Arquitecto. Codigo en Zeus-protocol. UX READ-ONLY (sin nueva superficie de escritura).

- spec: SPEC-0086 (ext4, AC23; carry AC11/AC12/AC13/AC17)
- origen: REQ-FB27AF72 (semilla del operador via intake; TITULO mangleado -> intent re-derivado de la narrativa)
- status propuesto al promover: ready (Codex)
- code_repo: D:/Agentes/Zeus/Zeus-protocol

## Alcance
1. Agregar el nav item **Help** y su panel; "help" entra en NAV_VIEWS (routing 1:1, hereda AC12). Activar
   Help muestra SOLO el panel Help; vista desconocida -> fallback.
2. Render de una guia DETALLADA y NAVEGABLE (secciones + indice/glosario) que cubre: consola; observar vs
   operar; submit_intent escritor-unico; dry_run vs execute/confirmacion; atestacion #4; las vistas; el intake
   RF-14; el pipeline SDD; glosario.
3. **Fuente unica = docs/MANUAL-operador.md** (reusar, no duplicar). Implementacion a eleccion de Codex
   (servir el manual read-only y renderizarlo, o incluirlo en build desde ese unico archivo); NO crear una
   segunda copia divergente del texto.
4. Honestidad (AC11): refleja lo que la app HACE hoy incl. limitaciones; lo no implementado se marca
   pendiente/fuera-de-alcance, no se afirma como activo.
5. Read-only: sin botones de accion, sin llamadas a submit; conforme al design-system (AC13).

## DoD
- AC23 verde con tests de COMPORTAMIENTO permanentes: routing de "help" (solo su panel; fallback); contenido
  derivado de docs/MANUAL-operador.md (no placeholder; cubre secciones clave/glosario); no-bypass (sin
  superficie de escritura en el panel). Carry AC11/AC12/AC13/AC17 verdes.
- node --test/CI verde; npm start ejecutable; Help navegable en vivo.
- validate exit 0 con/sin secretos (clon limpio, DECISION-0046); drift 0; #4 epoca 1.14.0 BYTE-IDENTICA;
  neutralidad/encoding limpio.
- Reproducido por el checker (Arquitecto) desde clon limpio; maker!=checker. Commit como Arquitecto +
  Co-Authored-By: Codex.

## Fuera de alcance
- Cualquier cambio de superficie de escritura (vista 100% read-only).
- Editar/duplicar el contenido del manual (la fuente es docs/MANUAL-operador.md; documentar features
  inexistentes esta PROHIBIDO por AC11).
