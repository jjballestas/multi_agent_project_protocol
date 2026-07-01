---
decision_id: DECISION-0075
title: "REQ-ZEUS D4 - hermes-agent bajo MIT (verificado); vendorizar el binario PERMITIDO conservando el aviso MIT; caveat de marca (logo NousResearch = purga aparte)"
status: accepted
ratified_at: 2026-06-30
date: 2026-06-30
deciders: [operador humano, Arquitecto]
supersedes: []
superseded_by: []
relates_to: [REQ-ZEUS-001, DECISION-0050, DECISION-0076]
scope: product
phase: P2
---

# DECISION-0075 (REQ-ZEUS D4) - hermes-agent MIT; vendorizar permitido

> ACCEPTED, licencia VERIFICADA 2026-06-30 (operador endoso OPS-115242Z + registro en hub). Canonicaliza la D4 de NOVA
> (`.../NOVA/Area_comun/decisions/DECISION-0004-D4-hermes-agent-desde-fuente.md`).

## Hallazgo (verificado)
El binario **hermes-agent (NousResearch) esta bajo MIT License, Copyright (c) 2025 Nous Research.** Verificado en
tres fuentes (2026-06-30): repo GitHub `NousResearch/hermes-agent` (LICENSE MIT integro + badge), y el footer de
`hermes-agent.nousresearch.com/docs` ("MIT License"). MIT permite usar/copiar/modificar/distribuir/vender, incluido
uso comercial, con UNA condicion: conservar el aviso de copyright + el texto de la licencia.

## Decision
- **Vendorizar el binario hermes-agent ESTA PERMITIDO** (MIT). El bloqueante legal de un release turnkey-con-binario
  queda LEVANTADO, siempre que se incluya el **LICENSE/aviso MIT de hermes-agent** en la distribucion.
- **Recomendacion de empaquetado (R1):** vendorizar para un instalador turnkey de un solo paso (mejor UX). Instalar
  desde fuente queda como alternativa valida (bundle menor). Eleccion final de empaquetado = operador.

## Caveat de MARCA (separado de la licencia del codigo)
MIT cubre el CODIGO, no la **marca/logo NousResearch**. Aunque podamos redistribuir el binario: NO shippear el
logo/marca NousResearch ni implicar endoso (retirar assets `nous*` del build; ver D5 / gate de purga). En el release
publico, THIRD-PARTY-NOTICES incluye **DOS** avisos MIT: Hermes Workspace (fork base) + hermes-agent (gateway).

## Consecuencias
- D4 deja de ser bloqueante de release; el unico residual de marca es el logo (gate de purga de assets).
- Accion de release: incluir ambos LICENSE MIT en THIRD-PARTY-NOTICES; CI gate que verifique su presencia y la
  ausencia de assets de marca de terceros en `dist/`.
