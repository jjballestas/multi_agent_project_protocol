# DRAFT (parqueado) - 5to brazo: peon local MAYOR (14b/32b) - medir si un maker mas capaz ahorra

> Estado: DRAFT parqueado por el Operador (18-jul). RECORDATORIO PROGRAMADO: 10-ago-2026 09:07
> (tarea agendada durable "recordatorio-5to-brazo-peon-14b-32b", one-shot, sobrevive cierre de
> sesion). NO rutear hasta el recordatorio + GO del operador. Demo privada, NO citable.

## Pregunta
Un maker local MAS CAPAZ (14b/32b coder), que NO cometa los errores de tipos/float ni el
techo-de-reparacion del 7b, produce AHORRO real de tokens frontier (delegado < directo)?

## Prediccion estructural (falsable, ex-ante)
Llega a ~EMPATE (baja del +43pct del 7b hacia el suelo del envelope ~135k), NO cruza. Razon:
el peon solo descarga la GENERACION, que ya es barata en el frontier; la spec y el sello siguen
siendo frontier (el suelo del envelope). Un peon perfecto ahorra a lo sumo la fraccion de
generacion (~1.5-20pct). Solo cruzaria en unidades de GENERACION CARA (logica profunda), que es
la frontera de la clase delegable.

## Diseno propuesto (cuando se active)
- Misma unidad del 4to brazo (motor nomina 50fn/250asserts) o familia QC-barato, MISMO protocolo
  (comparabilidad). Swap del maker: qwen2.5-coder:7b -> 14b o 32b via Ollama con offload a RAM.
- Metricas: escalacion (baja a 0?), bounces-noop (desaparecen?), velocidad (tok/s con offload),
  y CRUCE (delegado total vs directo 137042). Sello 0101 en ambos.
- Hardware: RTX 5060 8GB VRAM + 63.7GB RAM. 14b ~8-9GB (offload ligero, ~10-20 tok/s); 32b
  ~18-20GB (offload fuerte CPU, ~2-5 tok/s, lento pero corre). deepseek-coder-v2:16b MoE opcion
  velocidad/capacidad.

## Lectura que cerraria
Si llega a empate y no cruza -> confirma que la capacidad del peon NO es la palanca del ahorro
(lo es la estructura: spec+sello frontier). Si cruza en unidad de generacion cara -> abre la
unica via real, a cuantificar. Barato de responder con dato en vez de teoria.

## Gancho al recordatorio
Este draft conecta con la DECISION del operador (18-jul): NO adoptar peones hasta revisar+
replicar un metodo que preserve calidad. El 5to brazo es una de las mediciones que informaria
esa reapertura (junto a la revision bibliografica de metodos quality-preserving).
