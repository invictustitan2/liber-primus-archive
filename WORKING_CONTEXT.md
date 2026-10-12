# Working Context — Liber Primus Page 57 Spiral Research

**Purpose:** Durable handoff notes for ongoing work. Read this before proposing next steps or asking for checks that may already have been completed. Update it when decisions, provenance, or verified results change.

## Operating rules

- Treat this document and the research ledger as the current project memory; consult them before asking the user to repeat prior work.
- Distinguish verified facts, exploratory results, and unresolved questions. Do not turn a hypothesis into a fact.
- Do not ask the user to rerun a check whose result is already recorded here or in the ledger.
- Do not modify, stage, or overwrite research artifacts until their roles and provenance are understood.
- When repository state is relevant, inspect the available remote files/history first. Do not imply access to the user's local filesystem.
- Keep source evidence, crop provenance, traces, diagnostics, and interpretation distinct.
- Preserve existing artifacts. Correct documentation explicitly rather than silently replacing or conflating files.

## Repositories and locations

- Research archive: `invictustitan2/liber-primus-archive`, default branch `main`.
- Annotation app: `invictustitan2/lp-annotation`, branch `master`, version/tag `v3.12.3`.
- The annotation app's original scans and SQLite database are local data under `~/.local/share/lp-annotation/`; they are not included in the app source repository.
- Local archive checkout: `~/archives/liber-primus-archive`.
- Local annotation app source: `/home/dreamboat/projects/lp-annotation/app`.
- The archive checkout was fast-forwarded to commit `e983cb97c5b7d708199f8a6de73940c5980f464c`. At the last recorded status, analysis outputs and `research/` and `toolkits/` were untracked. Do not assume that status remains current without evidence.
- `toolkits/liber-primus/` is a nested Git repository. Do not treat it as ordinary archive content or modify it incidentally.

## Page 57 source scan — verified

- Source ID in annotation database: `3f167f8e-8aae-48ce-85a7-4e4f2e6b0794`.
- Original name: `57.jpg`; stored as `sources/3f/3f167f8e-8aae-48ce-85a7-4e4f2e6b0794.original`.
- Dimensions: 2400 × 3600 pixels.
- Byte size: 746,355.
- SHA-256: `3f5af995b39f94f268d4aa94825a10f2429f4a3affa1921a7f627e6d1bfcfb69`.
- The database query found no saved `regions` row for this source. This means there is no persisted region record to cite; it does not invalidate a crop that can be independently verified against the source.

## Why there are two crops

These files are intentionally different framings of the same page-57 motif, not duplicate artifacts.

### 1. Context crop — `page57_spiral_left.png`

- Archive path: `data/raw/page57-spiral/page57_spiral_left.png`.
- Git blob SHA recorded in the archive: `89b348b81ff738abfc7cf801162b8e9a6179fafc`.
- Visual scope: the spiral plus the connected stem and lower branching/root-like structure.
- Purpose: preserve the motif's surrounding visual context and connectivity for interpretation.
- Its sidecar `data/raw/page57-spiral/page57_spiral_left.txt` identifies source `data/pages/57.jpg`, records the source SHA-256 above, says the operation was a rectangular crop with no resizing, rotation, or retouching, and gives the selection rationale as retaining the spiral and connected stem/branch.
- **Provenance gap:** that sidecar does not record the crop rectangle. It names `research/visual-evidence/page57_spiral_left.png` as the crop file, whereas the archived image lives at `data/raw/page57-spiral/page57_spiral_left.png`. This is a path inconsistency to resolve/document, not grounds to conflate the two crops.

### 2. Tight analysis crop — `page57_spiral_working.png`

- Archive path: `data/raw/page57-spiral/page57_spiral_working.png`.
- Git blob SHA: `876a7788fb5ef7dfd597a4e31577c09b15812280`.
- Dimensions: 301 × 236 pixels.
- Source rectangle, zero-based half-open bounds: `[160, 461) × [2246, 2482)`, i.e. x = 160..460 and y = 2246..2481.
- Purpose: isolate the dominant spiral loop and inner terminal for tracing and curve fitting, while retaining the spiral-to-stem junction. The long connected stem is clipped at the crop's top and bottom edges.
- Sidecar: `data/raw/page57-spiral/page57_spiral_working.txt`.
- A crop was re-extracted from the canonical source using the annotation app's `extract_crop` and `Rectangle` implementation. Source hash matched, dimensions matched, crop SHA-256 matched, and pixel arrays matched.
- Verified extracted/working-crop SHA-256: `5d7e7e667d55ed9a44f22e486c462bdea43cdd7fae6ecbddc7d26900649d1c4a`.
- The crop operation was rectangular only: no resizing, rotation, sharpening, or retouching.

**Use rule:** use the context crop when discussing the motif's relationship to the connected stem/branches; use the tight working crop for the current spiral trace and geometric model comparison. Never substitute one for the other without explicitly stating the change of framing.

## Current analysis state

- A manually clicked 21-point trace is stored as `data/raw/page57-spiral/trace_points_working.csv` and `trace_points_working.json`.
- The trace metadata says outer-to-inner, but the coordinate sequence appears inner-to-outer. Preserve the submitted trace and document this direction mismatch; do not silently reverse or rewrite it.
- The initial fit comparison is exploratory, not a validated geometric conclusion. The free-slope logarithmic fit had a lower residual than the golden-constrained fit under the recorded log-radius objective. The trace is sparse/manual, the center is estimated, and the objective is not an orthogonal pixel-distance fit. This does not establish intent or definitively rule out a golden-ratio relationship.
- A winding-aware pixel-space diagnostic was also run. It found a near-180-degree step between trace points 0 and 1 for the free-center fit; the golden-constrained fit had angular reversals. Treat trace quality and point placement as unresolved.
- Existing remote analysis scripts include `scripts/trace_page57_spiral.py`, `scripts/fit_page57_spiral.py`, `scripts/diagnose_page57_spiral.py`, and `scripts/audit_page57_trace.py`.
- Existing remote reports include `fit_results_working.md`, `fit_diagnostics_working.md`, and `trace_audit_working.md` under `data/raw/page57-spiral/`.
- The research ledger is `research/research-ledger-and-visual-motif-inventory.md`.

## Next work, in order

1. Resolve the context crop's missing rectangle/path discrepancy from repository history or available original records. If the rectangle cannot be recovered, leave it explicitly unknown; do not infer it from appearance alone.
2. Inspect the trace overlay against the tight crop and source pixels before changing any trace points.
3. Reconcile the trace direction metadata with the coordinate sequence in a new, explicitly versioned annotation or correction note; preserve the original files unchanged.
4. Only then rerun or extend model comparisons with a consistent pixel-space metric and sensitivity analysis.
5. Record each new finding here and in the research ledger so future sessions do not restart from assumptions.

## Evidence discipline

For each new claim, label it as one of:
- **Verified:** directly checked against source pixels, hashes, repository records, or reproducible computation.
- **Recorded:** stated in an existing sidecar/report but not independently reverified.
- **Exploratory:** dependent on manual points, an initial model, or a provisional method.
- **Unresolved:** evidence is absent, inconsistent, or insufficient.

Do not describe a result as verified solely because it appears in a prior assistant response.
