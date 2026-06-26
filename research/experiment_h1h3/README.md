# H1-H3 Experiment Harness

Tooling de investigacion para medir H1-H3 sobre fixtures y copias desechables. El runner nunca muta el ledger vivo:
crea un directorio temporal root-local, inyecta vectores A1/A2/A3 sobre fixtures, calcula deteccion/FPR/salud,
estima sobrecoste con y sin #4, y ejecuta verificacion externa solo con publicas.

Uso:

```powershell
python research/experiment_h1h3/harness.py --seed 104 --k 9 --run-id local-check
```

Salidas:

- `research/experiment_h1h3/results/<run>.json`
- `research/experiment_h1h3/results/<run>.md`

La corrida real de medicion queda fuera de este tooling. Este aparato esta pensado para CI y revision en clon limpio.
