# LISTA de candidatos a limpieza en la raiz D:\  (SOLO LISTA -- NO se elimina nada)

> Generada por el Arquitecto a peticion del Operador (directiva 3: "listar ... NO ELIMINARLAS,
> solo listarlas para que yo decida"). Fecha: 2026-07-26. NINGUNA carpeta fue borrada.
> Metodo: `Get-ChildItem D:\ -Directory` + `git remote get-url origin` por dir + suma de tamano.
> El operador decide que se borra. Al aprobar, el barrido se hara con verificacion 1x1 (que cada
> candidato tenga `.git` con remote al original vivo, o sea output regenerable) y `rm -rf` explicito.

## Resumen
- Candidatos "seguros" (clones/probes/outputs regenerables): **75 dirs, ~81.5 GB**.
- Categoria E (FLAG, requiere tu confirmacion 1x1): **14 dirs, ~24 MB**.
- El grueso del coste son 42 clones del hub a ~2 GB c/u (cada clon arrastra el `.git` completo:
  miles de eventos del ledger + dataset N=500).

## NO CANDIDATOS -- NUNCA tocar (excluidos)
`Aegis_Scratch` (scratch designado, tiene instancias reales: Nova-Payroll, NOVA-Prototype, NOVA-Suite),
`Agentes` (padre del repo real y de los productos), `Jball`, `Ing`, `ZaraLumis`, `Escritorio`, `v1`,
`.pnpm-store`, `System Volume Information`, `$RECYCLE.BIN`.
Ademas dejo FUERA por precaucion (no son metodologia-obvio, no los toco sin tu palabra): `temp`, `tmp`, `Backups`.

---

## Categoria A -- clones del HUB (clean-clone-validate)  [42 dirs, ~81.4 GB]
Remote -> `multi_agent_project_protocol` (o clon-de-clon). Son CLONES; el hub original en
`D:\Agentes\multi_agent_project_protocol` queda intacto. Seguro borrar.
```
ccv0268 ccv0268b ccv0258 ccv0258p ccv0269 ccv0258f ccv0272 ccv0273 ccv0272r1 ccv0272r2
ccv0277 ccv0280p ccvAp ccvB ccvBp ccvC ccvCp ccvQ ccv0280m ccv0280c ccv0280
ccv0281b ccv0281c ccv0281m ccv0281p ccv0281f ccv0284 ccvA ccv0274b c283 c283i3 c283i4
ccv0276b ccv0276m ccv0285 ccv-0261 ccv-0261-parent ccv266r1 ccv0290 ccv0256 ccv256r1 ccv293
```

## Categoria B -- repos-probe de test (git init, sin remote)  [17 dirs, ~3 MB]
Fixtures throwaway de probes de hook/bench (cadena DECISION-0103 + bench peones TASK-0280). Sin remote =
commits solo locales, pero son fixtures de prueba, no data real. Seguro borrar.
```
bench0280-mj9j5la4 bench0280-re8jsle3 bench0280-b8rwas15 bench0280-9l1h6d_f bench0280-8g1wlp_q
bench0280-w07g_ro1 bench0280-_vcsrnvk bench0280-xbo89m11 bench0280-9zj_sscd bench0280-h3zw4evg
rt_probe lsprobe gs0284 del_staged_del del_unstaged_del broken0284 ccv266r1inst
```

## Categoria C -- outputs / instancias generadas (sin git)  [13 dirs, ~16 MB]
Instancias born-operational generadas, sandboxes y salidas de probe (regenerables). Seguro borrar.
```
ccv0268inst ccv0268inst2 sb0272r1 sb0272r2 u0272r2-oxhgn7pv lhtest ccv0280_probe
bo0280 aws0284 ci0285 inst256 i293 d
```

## Categoria D -- clones del PRODUCTO Nova-Payroll  [3 dirs, ~18 MB]
Remote -> `D:\Agentes\NOVA-Suite\Nova-Payroll`. Clones del producto; el producto original intacto. Seguro borrar.
```
t5a t5j t6b-946779
```

## Categoria E -- dirs sueltos que REPLICAN el arbol del repo en la raiz  [14 dirs, ~24 MB]  (FLAG)
TODOS creados 2026-07-19 19:54 (una sola operacion: extraccion / checkout-index fallido a `D:\` raiz;
`D:\` NO es un repo git). Parecen copias del arbol del repo, pero NO lo presumo: los reviso 1x1 antes de
tocar por si alguno tiene contenido que no sea copia. **Requiere tu confirmacion explicita.**
```
Area_comun connectors scripts skills examples .claude personal pre_t0_ledger_seal
.githooks .github runtime dist research profiles
```

---

## Como procederia (SOLO si autorizas)
1. Barrido de A+B+C+D (seguros): por cada dir, verificar `.git`+remote-al-original (o output), luego `rm -rf` explicito por nombre (nunca glob ciego), reportando cuanto se recupero.
2. Categoria E: revisar 1x1, mostrarte que contiene cada uno, y borrar solo lo que confirmes.
3. Nada de esto toca el fondo #4 ni ningun repo vivo (son copias/outputs en la raiz).
