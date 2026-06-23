---
task_id: "TASK-EXTRACT-1F5C13A7B5"
title: "Extraction request from historias_panel_operar_agentes.md"
type: "triage"
status: ready
owner: "Arquitecto"
phase: "P2"
priority: "normal"
project: "Zeus-protocol"
author: "Operador"
relayed_by: "Arquitecto"
endorsement: "none"
source_file_sha256: 4eb704a9a9ad3344226cc8bdc1c9b2ec215385416abe8aa792a44a384507c2d2
source_extension: ".md"
source_store_locator: os-tmp/zeus-protocol-file-intake/4e/4eb704a9a9ad3344226cc8bdc1c9b2ec215385416abe8aa792a44a384507c2d2/payload.bin
objective: "Prepare a bounded extraction request for an agent to derive candidate requirements from the uploaded file."
expected_output: "Candidate requirement drafts in a non-ledger store, with no candidate entering TASK_INDEX until human review and approval."
question_to_resolve: "Which candidate stories or use cases should be proposed from the uploaded file?"
closure_criterion: "All viable candidates are available for human review outside the ledger, or the extractor records a no-candidate/failed state."
---

# TASK-EXTRACT-1F5C13A7B5 - Extraction request from historias_panel_operar_agentes.md

## Source

- file_name: historias_panel_operar_agentes.md
- sha256: 4eb704a9a9ad3344226cc8bdc1c9b2ec215385416abe8aa792a44a384507c2d2
- bytes: 3993
- store_locator: os-tmp/zeus-protocol-file-intake/4e/4eb704a9a9ad3344226cc8bdc1c9b2ec215385416abe8aa792a44a384507c2d2/payload.bin
- store_kind: os_tmp_outside_attested_dataset

## PII Screening

- mode: best_effort
- guaranteed: false
- channel: ascii
- detector_version: pii-screen-v1
- finding_count: 3
- proper_name: 3

## Extraction Contract

- input_read_from: os-tmp/zeus-protocol-file-intake/4e/4eb704a9a9ad3344226cc8bdc1c9b2ec215385416abe8aa792a44a384507c2d2/payload.bin
- input_verify_sha256: 4eb704a9a9ad3344226cc8bdc1c9b2ec215385416abe8aa792a44a384507c2d2
- output_destination: external candidate store outside ledger
- output_format: json array of candidate requirement drafts with title, narrative, acceptance_intent, source_file_sha256 and candidate_hash
- done_when: candidates are written outside the ledger and each candidate still requires human PII review before governed intake

## Guardrails

- Server upload path does not call a model endpoint.
- Raw upload bytes stay outside the attested dataset.
- Candidate text must remain outside TASK_INDEX until a human PII review gate approves a governed intake.
