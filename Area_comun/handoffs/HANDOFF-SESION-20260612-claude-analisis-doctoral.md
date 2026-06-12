# HANDOFF - Sesion 2026-06-12 (Claude/Cowork) - Analisis doctoral, correcciones y DECISION-0029

> **De:** Claude (architect, sesion Cowork 2026-06-12) - **Para:** cualquier sesion futura (VS Code u
> otra) de Claude o del operador. **Tipo:** handoff de continuidad autocontenido: leer este archivo +
> los enlazados basta para retomar; no se asume memoria de la sesion anterior.

## 1. Que paso en esta sesion (orden cronologico)

1. **Investigacion SOTA** (6 pilares: event-sourcing/integridad, seguridad por capacidad, release
   engineering verificable, economia de tokens, coordinacion N-agente, autonomia supervisada), ~85
   referencias con URLs verificadas y gaps G1-G6. Informe:
   `personal/Claude/research/SOTA_sistemas_multiagente_2026-06.md` (copia tambien en el caso de estudio,
   ver seccion 3).
2. **Veredicto critico** sobre la viabilidad doctoral de la metodologia: como artefacto de ingenieria es
   solido; como diseno de investigacion tenia 3 defectos fatales: (a) hipotesis circular, (b) adversario
   indefinido para G3.1 (auto-atestacion: runtime escritor unico firma con HMAC lo que el mismo escribe),
   (c) publicabilidad del dataset sin examinar (RGPD ScanPay + Ley 1581 Galapa).
3. **Paquete de correcciones** (5 documentos, en el caso de estudio loops_agenticos, seccion 3):
   hipotesis falsables H1 (solidez: deteccion >=95%, FPR <=1%), H2 (coste: <=5% tokens / <=10% latencia),
   H3 (verificabilidad externa >=90%); modelo de amenaza A1/A2/A3r/A4 con propiedades P1-P6; esquema de
   dataset en dos planos con gates GATE-DATASET / GATE-INST / GATE-SOTA.
4. **El operador APROBO los firmantes cruzados** (literal: "yo apruebo los firmantes cruzados") y se
   implemento en el ledger de ESTE repo via runtime (eventos 322-330, sin drift):
   - **DECISION-0029** (`Area_comun/decisions/DECISION-0029-firmantes-cruzados.md`): firma por agente +
     prev_hash + anclaje externo; BFT sigue prohibido; off-by-default.
   - **TASK-0101** (prev_hash, base), **TASK-0102** (firma por agente, central), **TASK-0103** (anclaje
     externo): `proposed`, owner Codex, `sdd_required`, specs PENDIENTES.
   - Mailbox: `Area_comun/mailbox/open/MSG-20260612-Claude-to-Codex-decision0029-tareas.md`.

## 2. Estado exacto al cierre de sesion

- Repo: protocol v1.1.0, runtime v0.11.0, `event_state` enabled/materialize/enforce/authoritative = true
  (NO editar `Area_comun/state/*.json` a mano; usar `runtime/submit_intent.py`).
- Tareas vivas nuevas: TASK-0101..0103 en `proposed`. NADA mas del pipeline esta encolado (ni Fase 0, ni
  GATE-DATASET, ni `protocol_research/`). Las SPECs de 0101-0103 NO existen (`spec_id: pending`).
- Gates de calidad: encoding y neutralidad de dominio verdes al cierre.
- `RESUME.md` esta DESACTUALIZADO (foto de 2026-06-05, v0.5.0); no se actualizo en esta sesion.

## 3. Artefactos fuera de este repo (caso de estudio)

Carpeta: `D:\Agentes\Estudio\Case_Studies\loops_agenticos\`
- `01_Sources/Documents/01_Hipotesis_Reformulada.md` (H1-H3, pre-registro)
- `01_Sources/Documents/02_Modelo_de_Amenaza_G3.1.md` (adversarios, propiedades, revision de la regla 3.5)
- `01_Sources/Documents/03_Publicabilidad_Dataset.md` (dos planos, T1/T2/T3, GATE-DATASET)
- `01_Sources/Documents/04_Integracion_en_Fase_6.md` (Fase 6 revisada, gates, enmiendas R1-R8)
- `01_Sources/Documents/05_Resumen_Ejecutivo_Correcciones.md` (mapa veredicto->correccion)
- `01_Sources/Documents/SOTA_sistemas_multiagente_2026-06.md` (informe SOTA)
- `04_Learning_Output/Final_Deliverables/sintesis_hoja_de_ruta.md|.html` (hoja de ruta REVISADA
  2026-06-12 con las correcciones integradas; secciones marcadas [rev. 2026-06-12])

## 4. Proximos pasos acordados (en orden)

1. **Claude redacta las SPECs de TASK-0101..0103** (acceptance_criteria + test_plan + golden cases);
   empezar por 0101. El operador da GO de promocion a `ready` tarea por tarea.
2. **Encolar Fase 0 del pipeline** (E5 catalogo de modos de fallo MAST, E6 test "merece un loop?", #1
   anotacion MAST del historial propio) - barata, sin runtime.
3. **GATE-DATASET** (consulta juridica RGPD + Ley 1581, doc. 03 seccion 6) - mayor latencia del camino
   critico; bloquea la ACTIVACION de la Fase 3 en produccion, no su construccion.
4. NO encolar Fases 1-2 y 4-5 todavia (regla 3.4 del pipeline: solo cuando un proyecto real lo exija con
   fecha).

## 5. Decisiones de criterio que la proxima sesion debe respetar

- Toda afirmacion de seguridad cita clase de adversario (A1/A2/A3r/A4); sin clase, no se afirma.
- "Capability" del registry = habilidad (RBAC), NO object-capability; no citar como "alineado con CaMeL".
- Los umbrales de H1-H3 se congelan en pre-registro ANTES de medir; no ajustar a posteriori.
- "Aborda" un gap, nunca "resuelve" (enmienda R1).
- Canal entre agentes en ASCII (DECISION-0012): sin tildes ni caracteres no-ASCII en archivos compartidos.
