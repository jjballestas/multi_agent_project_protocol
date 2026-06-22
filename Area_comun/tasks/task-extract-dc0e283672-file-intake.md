---
task_id: "TASK-EXTRACT-DC0E283672"
title: "Extraction request from intake-ux-feedback.md"
type: "triage"
status: ready
owner: "Arquitecto"
phase: "P2"
priority: "normal"
project: "Zeus-protocol"
author: "Operador"
relayed_by: "Arquitecto"
endorsement: "none"
source_file_sha256: de1f1cb12e084606e373fd76c9ff253206d0515f54cf79f430f92ab14fd61434
source_extension: ".md"
source_store_locator: os-tmp/zeus-protocol-file-intake/de/de1f1cb12e084606e373fd76c9ff253206d0515f54cf79f430f92ab14fd61434/payload.bin
objective: "Prepare a bounded extraction request for an agent to derive candidate requirements from the uploaded file."
expected_output: "Candidate requirement drafts in a non-ledger store, with no candidate entering TASK_INDEX until human review and approval."
question_to_resolve: "Which candidate stories or use cases should be proposed from the uploaded file?"
closure_criterion: "All viable candidates are available for human review outside the ledger, or the extractor records a no-candidate/failed state."
---

# TASK-EXTRACT-DC0E283672 - Extraction request from intake-ux-feedback.md

## Source

- file_name: intake-ux-feedback.md
- sha256: de1f1cb12e084606e373fd76c9ff253206d0515f54cf79f430f92ab14fd61434
- bytes: 1158
- store_locator: os-tmp/zeus-protocol-file-intake/de/de1f1cb12e084606e373fd76c9ff253206d0515f54cf79f430f92ab14fd61434/payload.bin
- store_kind: os_tmp_outside_attested_dataset

## PII Screening

- mode: best_effort
- guaranteed: false
- channel: ascii
- detector_version: pii-screen-v1
- finding_count: 0
- findings: none

## Extraction Contract

- input_read_from: os-tmp/zeus-protocol-file-intake/de/de1f1cb12e084606e373fd76c9ff253206d0515f54cf79f430f92ab14fd61434/payload.bin
- input_verify_sha256: de1f1cb12e084606e373fd76c9ff253206d0515f54cf79f430f92ab14fd61434
- output_destination: external candidate store outside ledger
- output_format: json array of candidate requirement drafts with title, narrative, acceptance_intent, source_file_sha256 and candidate_hash
- done_when: candidates are written outside the ledger and each candidate still requires human PII review before governed intake

## Guardrails

- Server upload path does not call a model endpoint.
- Raw upload bytes stay outside the attested dataset.
- Candidate text must remain outside TASK_INDEX until a human PII review gate approves a governed intake.
