# TASK-0359 remediation 4 memory

- Implementation commit `e08d9e54` makes the real-loop outcome probe execute the production
  sampling seed through the end of the production supervision loop; the former three hand-fed
  seed assignments are removed from the probe.
- The permanent negative executes three production mutants: unreachable sampling guard,
  `DateTime::MaxValue` seed, and the one-character seed sign change. The healthy outcome keeps
  silent CPU work alive; every mutant reports hung and calls the process-tree stop once.
- The exec-lease suite passed 31/31. Falsification inventory 74/74, mailbox retry, collaboration,
  encoding, Python neutrality, and diff gates exited 0. No production file changed.
- TASK-0359 remains `in_progress` under the remediation-4 maker claim pending governed delivery
  to `in_review` and independent checker re-judgment. Codex did not review or ratify the work.
