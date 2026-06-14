# v1.1.0 known limitations

`v1.1.0` is a historical release created before the repository had a root
`.gitattributes` policy that forces LF checkouts for text files. Its signed
manifest is preserved unchanged.

The release manifest at `dist/v1.1.0/manifest.json` is authentic, but it is not
LF-reproducible from a clean checkout by third parties. Exhaustive byte
classification of the 757 SBOM-included files against the recorded commit
`04436c3c93f9aaddd7167cf2f7d4a4529e7ebe4d` found:

- 616 files match under LF.
- 127 files were CRLF in the recorded commit, so LF-normalizing those blobs
  changes their hashes.
- 14 files do not match the manifest under raw, LF-normalized, or
  CRLF-normalized bytes.

The 14 non-EOL mismatches mean the manifest was generated from a dirty working
tree, not from a clean checkout of the recorded commit. Thirteen of those files
match a later working tree observed during analysis; `runtime/protocol_replay.py`
does not match any available ref or observed working tree, so that original
content is irreproducible from repository refs.

`dist/v1.1.0/verify.integrity.json` reports `ok:true` for the emitter's local
tree at release time. It is not evidence that an independent clean checkout can
reproduce the manifest. A `scripts/verify_release.py` run for `v1.1.0` that
fails under a clean LF checkout is expected and is not a regression in the
future-release LF policy.

The false premise in `SPEC-0075` was that no SBOM-included blob would change
under renormalization for `v1.1.0`. That premise is true for current `HEAD`, but
it was false for the recorded `v1.1.0` source commit because 127 SBOM-included
blobs were CRLF. TASK-0100 is therefore scoped to releases `v1.2.0+`: the root
`.gitattributes` policy protects future release checkouts, while the `v1.1.0`
signature and manifest remain intact.
