# LOG DE DECISIONES - Experimento QC-barato 3 condiciones (Asesor, autoridad delegada)

Directiva madre: b5d4401 (GO 3 condiciones). Autoridad delegada del Operador al Asesor para
resolver dudas de diseno durante la corrida. Demo privada, NO citable.

Baseline objetivo del cruce: 129921 tokens frontier (TASK-0014, lote-100 directo).
Lecturas: efecto sanitizador = arm3 vs 139195 (el +7.1 pct original); efecto checker =
arm2 vs arm3; cruce = total < 129921, SIEMPRE junto a calidad (defectos que el sello 0101
caza y el checker dejo pasar) + tasa de escalacion.

---

## DECISION 1 - Aval del diseno ex-ante del Arquitecto (2026-07-18 ~06:32)
Contexto: el Arquitecto pre-registro el diseno ANTES de ejecutar (d31e9a0: DISENO-QCBARATO-3cond
+ SPEC-SANITIZADOR-pregate + SPEC-CHECKER-LOCAL-pii) y pidio objecion de parametros por mailbox.
Decision: AVALADOS los 5 parametros sin objecion.
Razon: familia lote-100 PII + qwen7b B0-reuse = comparable al +7.1 pct; checker arm2 deepseek6.7b
familia distinta con contrato fijado ex-ante (no ajustable post-arm3) = aplica fit T3 con firewall
limpio; tope-2 + triaje validado; sanitizador mecanico 0-LLM como setup amortizable aparte = no
contamina el per-unit. Pre-registro ex-ante = disciplina anti-HARKing correcta.

## DECISION 2 - APRUEBO reuso del baseline 129921 (2026-07-18 ~06:32)
Contexto: el Arquitecto declaro reutilizar el punto medido 129921 (TASK-0014) como baseline
directo en vez de re-medirlo, declarado ex-ante en el diseno.
Decision: APROBADO (autoridad delegada).
Razon: protocolo identico (misma familia, lote, instrumento), meseta verificada (131340@50 ->
129921@100), calidad de referencia = sello 0101 de TASK-0014. Re-medir reproduce un punto ya
conocido a ~130k tokens frontier sin cambiar ninguna decision. Reuso economico Y honesto por ir
DECLARADO ex-ante (no post-hoc); respeta la regla de no gastar frontier reproduciendo lo ya medido.

## DECISION 3 - Guarda de consistencia de contabilidad (2026-07-18 ~06:32)
Contexto: el cruce total<129921 solo es valido si la frontera de tokens frontier es simetrica.
Decision: fijada guarda (no objecion): sello 0101 contado de forma uniforme en las 3 condiciones
(o delta antes del sello); el total del arm se reporta en la MISMA base que el 129921.
Razon: el sello es aditivo constante en las 3; si se cuenta igual, no sesga cual cruza. Evita
un falso cruce por asimetria de contabilidad.

Commit del ACK: 0b818b5 (Ops-Reason 110c, ASCII 0, push OK).

## ARM3 CERRADO (2026-07-18 ~07:12) - senal + confounding
Resultado: sanitizador ELIMINO los bounces (0 vs 5 en TASK-0014), QC acepto 10/10 a la primera,
gate 100 tests + regresion verdes, sello 0101 GO-CON-HALLAZGOS (0 defectos en 100 tests; 1 MENOR
latente en el tool, no ejercido). Bruto exec = 283024 pero NO comparable al 139195: confounding
declarado (autoria one-time del sanitizador + 1 artefacto extra + manejo de anomalia DECISION-0020).

## DECISION 4 - GO a la celda MARGINAL arm3 (2026-07-18 ~07:15)
Pregunta 1 del Arquitecto. Decision: GO (re-run con sanitizador ya existente, ~140k frontier,
comparable al protocolo 139195/129921), como celda aparte etiquetada, post-arm2.
Razon: el cruce en coste TOTAL es una de las 3 metricas comprometidas y el 283024 confundido no
puede darlo; la marginal (setup hundido) es el steady-state relevante para NOVA (sanitizador ya
construido, coste amortizado); lava los 3 confounds con instrumento limpio en vez de particion
post-hoc (HARKing-adyacente); aplica la regla del operador (medir el punto limpio cuando el
estudio es revelador). Reportar per-unit vs 129921 (cruce) y vs 139195 (efecto sanitizador).

## DECISION 5 - CONFIRMO arm2 con sanitizador VERBATIM (2026-07-18 ~07:15)
Pregunta 2 del Arquitecto. Decision: CONFIRMADO, no endurecer el sanitizador antes del arm2.
Razon: disciplina de factor unico -- arm2-vs-arm3 aisla el CHECKER (Codex vs deepseek local);
endurecer el sanitizador ahora mete un segundo factor y confunde esa lectura. El MENOR es latente
(no ejercido, 0 defectos sellados), telemetria lo vigila; el endurecimiento va como recomendacion
al protocolo NOVA. Misma regla firewall: fijar ex-ante, no ajustar tras ver resultados.

## NOTA 6 - DECISION-0020 (write concurrente) acusada
Mi ACK 0b818b5 fue mailbox-only con pathspec explicito (solo Area_comun/mailbox/open/), no toco
el workspace reclamado. Leccion que tomo: vigilar la ventana de claim de la instancia al pushear
coordinacion durante un exec activo. El manejo de esa anomalia es uno de los confounds que la
celda marginal (D4) lava. Cerrado sin ping-pong de culpa.

Commit de la RESP: fb88610 (Ops-Reason 99c, ASCII 0, push OK).

## ARM2 CERRADO (2026-07-18 ~08:20) - HALLAZGO CENTRAL negativo (dato, no decision)
Veredicto: el checker local deepseek NO aporto filtrado util en esta familia. Sello 0101: 13 de
sus 18 GO precedieron gate rojo; sus 4 NO-GO con rationale espurio; el check de nombres es vacuo
POST-sanitizador (su espacio util era vacio); 0 true-positives. Ademas dio GO a un bloque cuya
evidencia CRUDA tenia un IBAN mod-97 valido (ejemplo de doc); las 100 unidades finales limpias.
Convergencia sostenida por SANITIZADOR + GATE DURO + ESCALACION frontier 50pct (5/10 bloques,
todas por gate rojo tras GO local con tope agotado; V9 se recupero en bounce2 sin escalar).
- bounces arm2 = 12 | escalacion = 5/10 | coste local checker = 84914 prompt_eval + 367 eval (0
  frontier) | gate 100+42 exit 0 | calidad final = 0 defectos (2 MENORES en evidencia cruda).
- frontier bruto 160535 (confounding: setup orquestador + run abortado en el mismo exec; la
  comparacion de coste TOTAL limpia queda para la marginal; la de PIPELINE ya es valida).
IMPLICACION provisional para el envelope NOVA: si el pre-filtro local no discrimina, su papel
util queda en el SANITIZADOR mecanico (gratis) + gate duro, con QC frontier solo en escalacion
-- que es lo que arm2 termino haciendo. (A confirmar con la marginal.) Sin decision mia pendiente:
el Arquitecto procede a TASK-0017 marginal arm3 (mi GO ya dado). Commit reporte: eab353a.

## CIERRE (2026-07-18 ~08:56) - VEREDICTO FINAL
Marginal arm3 steady-state = 135171 = +4.0 pct vs directo 129921. NINGUNA condicion cruza.
- Efecto SANITIZADOR: baja el premium de +7.1 a +4.0 (-3.1pp), robusto (la marginal tuvo MAS
  friccion: 5 bounces + 2 techos vs 5+0 de la referencia) + mata la clase de deslices de formato.
- Efecto CHECKER local: 0 valor de filtrado (0 true-positives; 13/18 GO precedieron gate rojo;
  NO-GO espurios; nombres ya resueltos por el sanitizador). Convergencia por gate + escalacion
  frontier 50pct, NO por el checker. Fuera del envelope NOVA.
- Bonus (sello): con decode determinista, bounce-2 sobre prompt identico = respuesta byte-identica
  -> inutil. Tope efectivo recomendado: 1 bounce + triaje.
- Calidad: 0 defectos en 300 unidades (3 sellos 0101); 0 fugas PII (IBANs mod-97-invalidos en las
  3). 1 MAYOR declarativo (lote no-nuevo en marginal) enmendado sin re-run (peon stateless, ~135k
  no cambiaria decision); anomalia 0018 a Codex con fix de proceso.
- Coste total variante ~579k frontier (283024+160535+135171).
CONCLUSION: delegar compra CAPACIDAD, no ahorro neto (confirma y refina el piloto). El sanitizador
mecanico SI vale adoptar; el checker LLM local NO. ADOPCION = decision del operador (no la tomo yo).
Commit reporte final Arquitecto: b26f1cd.

EXPERIMENTO CERRADO. Entregado REPORTE FINAL al operador en chat + closing ACK al Arquitecto.
---
