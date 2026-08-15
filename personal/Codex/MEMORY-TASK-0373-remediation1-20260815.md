# TASK-0373 remediation r1

- Implementation commit: `4a9b6a12`.
- Cold task stubs require original source bytes and preserve the literal intake block.
- Stub rendering requires a caller-provided `requested_by`; the emitted retrieval command includes
  it and the F2 suite executes that command end to end.
- TASK-0350 is the permanent modern-corpus validator case; the rendered stub passes and a zero-byte
  replacement fails.
- Pack and manifest-index formats are bound by independent literal ASCII byte goldens.
- A `requires_stub: false` rule still forces a stub for an indexed task.
- Full memory suite passed 80/80. Encoding, fast drift, Python and PowerShell neutrality, canonical
  live validation, and canonical validation with TASK-0350 replaced by its stub all exited 0.
- TASK-0373 remains maker-owned until governed delivery moves it to `in_review`, releases all maker
  claims, and routes an independent checker. Codex did not review or ratify the work.
