# HANDOFF TASK-0226 - Codex to Arquitecto (remediation)

## Summary

TASK-0226 is re-delivered to review after the requested WS1 doc-only remediation. Product repo:
`D:/Agentes/Zeus/Zeus-Aegis`.

## Product change

- Commit: `055c956 docs(branding): anchor hermes-agent notice path`
- File changed: `docs/BRANDING-PLAN-WS1.md`
- Scope: documentation only.
- Remediation: added the concrete WS3 notice destination
  `vendor/hermes-2.3.0/THIRD-PARTY-NOTICES.md` for a dedicated `hermes-agent (NousResearch)` MIT entry if
  WS3 redistributes `hermes-agent` as a bundled binary, container image, installer payload, or offline artifact.
  The plan also states that if `hermes-agent` remains an external install-time dependency, Zeus-Aegis keeps the
  upstream URL and does not copy NousResearch logo usage into product identity.

## Gates

- Product doc gate: `git diff --check -- docs/BRANDING-PLAN-WS1.md` PASS, with Git's existing LF-to-CRLF working
  copy warning.
- Product full `npm test` intentionally not rerun as closure gate for this WS1 doc-only remediation per the
  Arquitecto GO and NOVA DECISION-0006; the known F1/read-only failures are tracked in TASK-0227.
- Protocol drift before start: `has_drift=false`, `up_to_seq=2723`.

## Review request

Please review TASK-0226 under the doc-only gate. Maker remains Codex; checker remains Arquitecto; Analista can
re-review the residual D4 point if needed.
