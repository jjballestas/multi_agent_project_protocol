---
decision_id: DECISION-0001
title: Adopt dotnet_enterprise profile
status: accepted
date: 2026-06-05
deciders: [Claude, Codex, operador humano]
relates_to: [TASK-0006]
---

# DECISION-0001 - Adopt `dotnet_enterprise`

## Context

This controlled example validates that a protocol instance can compose the neutral core with an
optional professional profile.

## Decision

Adopt `profiles/dotnet_enterprise` version `0.1.0` on top of protocol version `0.2.0`.

## Consequences

- The instance remains valid as a core protocol instance.
- .NET, SQL Server, Azure DevOps and Docker-specific practices live only in the adopted profile.
- Real secrets remain outside the repository; committed files may contain placeholders only.
