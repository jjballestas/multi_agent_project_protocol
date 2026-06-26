# Pre-registro H1–H3 — Atestación de autoría en un protocolo multi-agente (TFM)

> Estado: **FROZEN v1.0 — 2026-06-27.** Umbrales de §5 confirmados (el operador delegó la fijación en el
> Arquitecto; justificación por principio/requisito en §5, no por inspección de resultados). El freeze es el
> commit de git que introduce este estado (fecha+hash inmutables = la marca de pre-registro). **Tras el freeze NO
> se cambian** hipótesis, métricas ni umbrales antes de medir (regla anti-post-hoc; corazón de un trabajo
> audit-first). Si el operador discrepa de un umbral, se emite una **v2.0 nueva** (con su fecha), nunca se edita
> esta v1.0 — pero solo es válido cambiarlos ANTES de mirar cualquier resultado.
> Referencias de fondo: DECISION-0029 (firmantes cruzados), DECISION-0039 (activación gateada + A1–A4 + AC2/AC3),
> DECISION-0046 (replay secret-independiente), DECISION-0040 (GATE-DATASET / sin PII).

## 0. Por qué existe este documento (y qué NO es)

Construir el sistema instrumentado (#4 + banco de pruebas golden) es el **instrumento**. Este pre-registro fija,
**antes de mirar resultados**, qué se va a medir, cómo, y qué umbrales separan "confirmado" de "refutado". Sin
esto, cualquier número posterior es post-hoc — justo lo que un trabajo sobre integridad no puede permitirse.

## 1. Objeto y sistema congelado bajo medición

- **Objeto:** el mecanismo de atestación #4 = cadena `prev_hash` (A1) + **firma de autoría por agente Ed25519**
  (A2, contribución nueva) + anclaje externo (A3), sobre el event-log de un protocolo multi-agente gobernado
  (single-writer `submit_intent`).
- **Sistema congelado:** `multi_agent_project_protocol` en el commit de freeze (a registrar al congelar) con
  `protocol_version` (época) **1.14.0**. La medición corre sobre ESTE estado; ningún cambio del core/umbrales
  entre el freeze y la medición.
- **Precondición conocida (no es resultado, es estado de partida):** hoy los turnos vivos llevan integridad
  **HMAC** (`event_auth`, simétrica) pero **cero firmas Ed25519 por agente** (`actor_auth:"not_enforced_phase2"`,
  1448 eventos). La capa **A2 asimétrica** (la contribución) está construida+probada en golden pero **no opera
  sobre el dataset vivo**. → El **cutover A2** (encender la auto-firma Ed25519 en turnos reales) ocurre
  DESPUÉS de este freeze y ANTES de medir (ver §6); es prerequisito de H1 sobre A2.

## 2. Modelo de amenaza (clases de adversario; DECISION-0039 §3)

- **A1 — Manipulación post-hoc del log** (alterar/borrar/insertar/reordenar eventos ya escritos). Cubierto por
  `prev_hash`. — **Vivo hoy.**
- **A2 — Suplantación de autoría entre agentes** (un agente o el runtime atribuye a otro un turno que no produjo).
  Cubierto por firma Ed25519 con privada fuera del repo que el runtime encadena pero no puede producir. — **La
  contribución; pendiente de cutover.**
- **A3 (restringido) — Reescritura por el runtime de historia ya anclada.** Cubierto por anclaje externo del
  digest de cabeza. Riesgo residual declarado: omisión de eventos aún no anclados (ventana).
- **A4 — Operador humano malicioso / bizantino / identidad criptográfica del MODELO: FUERA DE ALCANCE.** Sin
  clase asignada no se afirma nada.

## 3. Hipótesis (operacionalizadas)

- **H1 (Detección / seguridad).** El validador/replay **rechaza** toda atestación forjada o alterada de los
  vectores en alcance (A1, A2, A3) — propiedad **binaria por vector** (AC3 de DECISION-0039) — **sin** rechazar
  eventos legítimos (salud AC2). Operacional: TPR de detección = 100 % sobre ataques inyectados; FPR sobre el
  dataset legítimo ≤ umbral (§5).
- **H2 (Sobrecoste acotado).** El coste incremental de #4 (latencia y bytes por evento, y sobrecoste de
  tokens/coordinación con #3 cost-attribution) frente a un baseline **sin #4** está **acotado** por los umbrales
  de §5. Operacional: Δlatencia (mediana y p95) ms/evento, Δalmacenamiento bytes/evento, Δtokens %.
- **H3 (Verificabilidad independiente).** Un verificador **externo** con solo las claves **públicas** (sin
  secretos de firma) reproduce el **mismo veredicto** desde un **clon limpio** — replay secret-independiente
  (DECISION-0046): mismo hash canónico con y sin secretos, y firmas Ed25519 verificables con la pública.
  Operacional: acuerdo verificador-externo = 100 % (veredicto idéntico) + match de hash canónico clon-limpio.

## 4. Métricas y variables

| Métrica | Definición | Hipótesis |
|---|---|---|
| Detección (TPR) por vector | ataques inyectados rechazados / ataques inyectados | H1 |
| FPR | eventos legítimos rechazados / eventos legítimos | H1 |
| Salud del instrumento (AC2) | atestaciones bien formadas y verificables / eventos autoría-relevantes (denominador **independiente del firmante**) | H1 |
| Δlatencia | ms/evento con #4 − sin #4 (mediana, p95) | H2 |
| Δalmacenamiento | bytes/evento con #4 − sin #4 | H2 |
| Δtokens | % sobrecoste de tokens/coordinación (vía #3) | H2 |
| Acuerdo externo | veredictos idénticos verificador-externo / total | H3 |
| Match clon-limpio | hash canónico (con secretos) == (sin secretos) | H3 |

## 5. Umbrales PRE-COMPROMETIDOS (CONFIRMADOS — FROZEN v1.0)

> Fijados por el Arquitecto por delegación del operador. **Justificados por principio/requisito, no por inspección
> de resultados** (no se ha medido nada). Congelados: no se mueven antes de medir.

- **H1 — CONFIRMADA si:**
  - **Detección = 100 %** en TODOS los vectores (A1, A2, A3). *Justificación:* AC3 es **binario** (DECISION-0039);
    un mecanismo de seguridad que deja pasar UNA sola falsificación está roto. No negociable.
  - **Salud AC2 ≥ 99 %** (instrumento bien formado en runs legítimos). *Justificación:* umbral ya fijado en
    DECISION-0039 §3.
  - **FPR = 0 %** sobre el dataset legítimo (ningún evento legítimo rechazado). *Justificación:* el verificador es
    **determinista** (cripto); una firma/cadena correcta SIEMPRE verifica (DECISION-0046 lo hizo
    secret-independiente), así que cualquier rechazo falso es un **defecto**, no ruido — la barra honesta es 0.
  - **Refutada si:** algún vector evade detección, **o** FPR > 0, **o** salud < 99 %.
- **H2 — CONFIRMADA si** (cotas por requisito de uso, no por peek):
  - **Δlatencia: mediana ≤ 50 ms/evento y p95 ≤ 200 ms/evento.** *Justificación:* un turno de agente dura
    **segundos**; el firmado/encadenado es una op cripto local que debe ser <1 % del turno → imperceptible en el
    lazo interactivo.
  - **Δalmacenamiento ≤ 4 KB/evento.** *Justificación:* lo que #4 añade por evento es firma Ed25519 (64 B) +
    hashes (32 B c/u) + envoltura JSON; 4 KB es holgado y mantiene un dataset de miles de eventos en orden de MB.
  - **Δtokens ≤ 5 %.** *Justificación:* #4 firma **hashes, no texto** (DECISION-0033/0040: cero payload nuevo),
    así que el sobrecoste de tokens por la atestación es ≈ 0; 5 % es un techo generoso para el plumbing de medición.
  - **Refutada si:** se excede cualquiera de las tres cotas.
- **H3 — CONFIRMADA si:** **acuerdo externo = 100 %** (verdicto idéntico del verificador externo con solo claves
  públicas) **Y** **match clon-limpio = sí** (hash canónico con secretos == sin secretos, DECISION-0046).
  *Justificación:* binario/principal — si un tercero no llega al mismo veredicto, la atestación no es externamente
  verificable. **Refutada si:** difiere algún veredicto **o** el hash no casa.

## 6. Procedimiento de medición (qué se EJECUTA, en orden)

1. **Cutover A2 (prerequisito):** encender la auto-firma Ed25519 por agente en turnos vivos (provisioning de
   `signature_config.public_keys` ya hecho; falta que cada agente firme sus turnos en operación, no solo en
   golden). Ventana de riesgo única, operador presente, rollback armado (DECISION-0039 §5). **Tras el freeze.**
2. **Generación del dataset:** correr el protocolo multi-agente por una ventana/volumen definidos (**N ≥ [OPERADOR:
   p.ej. 500] turnos gobernados por ≥ 2 agentes**) → corpus = event-log cruzado-firmado. Sin PII (DECISION-0040).
3. **Inyección de ataques (experimento negativo):** por cada vector A1/A2/A3, generar **K ataques** (alteración
   puntual, borrado, inserción, reordenamiento, llave no registrada, atribución cruzada, rollback de ancla),
   pasarlos al validador/replay, registrar detectado/evadido. (Los `attestation_negative_cases` son el esqueleto;
   se escalan a una corrida con conteos.)
4. **FPR:** correr el validador sobre el dataset legítimo (sin ataques) → contar rechazos falsos (esperado 0).
5. **Sobrecoste:** medir latencia y bytes por evento **con #4** vs un **baseline sin #4** sobre la misma carga;
   sobrecoste de tokens vía #3.
6. **Verificación independiente:** un verificador externo (clon limpio, solo claves públicas, sin secretos)
   re-corre la verificación → comparar veredictos + hash (DECISION-0046).
7. **Comparar contra §5** → aceptar/refutar cada H → §7.

## 7. Análisis y reporte

Reportar por hipótesis: número observado vs umbral pre-comprometido, veredicto (confirmada/refutada), y
limitaciones. **Reportar también los fallos** (vectores no detectados, FPR>0, sobrecoste excedido) sin maquillaje.

## 8. Independencia y limitaciones declaradas (honestidad audit-first)

- **A2 independencia DÉBIL:** todas las llaves se acuñaron en una ceremonia (no hay separación física de
  custodios). Declarado; acota la fuerza de no-repudio frente a un orquestador que tuvo acceso a la ceremonia.
- **A3 independencia DÉBIL:** ancla en el mismo disco (`D:\Agentes\audit-anchor`). Declarado.
- **Sujeto = medidor:** los agentes (incl. el Arquitecto) son sujetos de la atestación; por eso H3 (verificador
  externo) y este pre-registro son los que dan credibilidad. La inyección de ataques debe ser **programática y
  reproducible** (no juicio de un agente).
- **A4 fuera de alcance.** No se afirma seguridad contra operador malicioso / bizantino / identidad del modelo.

## 9. Freeze — EJECUTADO

**FROZEN v1.0 el 2026-06-27.** La marca de pre-registro es el **commit de git** que introduce este estado
(fecha + hash de commit inmutables, en el repo empujado a origin). El `sha256` del contenido congelado se registra
en el mensaje de ese commit como auto-certificación. Refuerzo audit-first opcional pendiente: atestar ese `sha256`
en el ledger #4 como parte del setup de medición (antes de generar el dataset), para anclar la fecha de freeze en
la cadena. Tras este freeze, cualquier cambio = documento NUEVO (v2.0) con su fecha; jamás se edita esta v1.0, y
solo es legítimo cambiar umbrales ANTES de mirar resultados.
