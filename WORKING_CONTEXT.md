# Working Context and Session Handoff — Liber Primus Research

**Last consolidated:** 2026-10-11  
**Purpose:** Preserve the actual project state and reasoning across sessions. This is an operational handoff, not a short summary. Read this and the linked primary notes before asking the user to repeat work, rerunning checks, or proposing edits.

## 1. Rules for continuing work

1. **Read today's work first.** Inspect this handoff, the cumulative research ledger, and the dated page-57 notes listed below. The sequence matters; don't reconstruct the project from filenames alone.
2. **Do not make the user repeat known work.** If a result is recorded, treat it as done unless there is a concrete reason to question its validity.
3. **Do not infer missing provenance.** Distinguish source evidence, metadata claims, visual observations, and hypotheses.
4. **Preserve primary artifacts.** Do not silently change the submitted trace, original crop files, original reports, or existing research notes. Put corrections in versioned/new artifacts or explicitly documented amendments.
5. **Do not confuse local and remote state.** The GitHub connector exposes the remote repository, not the user's local filesystem or local annotation database. Never claim to have inspected local-only files unless their contents were actually provided.
6. **Make progress without needless instructions.** Inspect repository docs/history first. Ask the user for local-only evidence only when remote records cannot answer the specific question.
7. **State confidence precisely.** Label claims verified, recorded, exploratory, or unresolved. An earlier assistant statement is not evidence by itself.
8. **Do not infer symbolic intent from geometric resemblance.** Any claim about golden-ratio construction needs reproducible measurements, a defensible comparison method, sensitivity analysis, and appropriate alternatives.

## 2. Repositories and state

- Research archive: `invictustitan2/liber-primus-archive`, default branch `main`.
- Annotation app: `invictustitan2/lp-annotation`, branch `master`, version/tag `v3.12.3`.
- Local archive checkout: `~/archives/liber-primus-archive`.
- Local annotation app source: `/home/dreamboat/projects/lp-annotation/app`.
- Local annotation database and source-image bytes are under `~/.local/share/lp-annotation/`; they are not mirrored in the app source repository.
- The archive checkout was fast-forwarded to `e983cb97c5b7d708199f8a6de73940c5980f464c`. At the last reported local status, multiple analysis outputs and `research/` and `toolkits/` were untracked. Do not assume the local status remains unchanged.
- `toolkits/liber-primus/` is a nested Git repository. Do not modify or stage it incidentally.
- This handoff was first created as `WORKING_CONTEXT.md`, commit `1979e8b19771a7f59aa40bb9bc3d80c0dc731c7b`; it was too narrow and is now being expanded based on the full set of today's page-57 work.

## 3. What happened today, in order

The Git history on 2026-10-11 records this progression:

1. `22:21Z` — initialize research archive.
2. `22:38Z` — add page-57 spiral evidence and source manifest.
3. `23:12Z` — add an improved tight working crop and document its provenance/visual framing.
4. `23:14Z` — add a reproducible manual centerline-tracing tool.
5. `23:28Z` — commit the 21-point centerline trace.
6. `23:30Z` — add the first exploratory logarithmic-spiral fit and document the free-slope vs golden-constrained comparison.
7. `23:37Z` — add a winding-aware diagnostic because the first model comparison implied substantially different angular spans; run/record radial pixel-space diagnostics and leave-one-point-out sensitivity ranges.
8. `23:40Z` — add the visual trace-audit tool and record the winding anomaly.
9. `23:41Z` — inventory existing visual evidence and establish the cumulative research ledger.
10. `23:50Z` — review crop-provenance implementation in the annotation app.
11. `23:52Z` — check the local annotation DB and establish that no saved region row exists for this source.
12. `23:55Z` — independently verify the tight crop by re-extracting it from the canonical source and comparing decoded pixels.

This order matters: the geometry work began with a manually traced tight crop; the later provenance check strengthened the crop's source association, while the trace/model validity question remains open. The context crop is a separate earlier/broader view, not a duplicate of the analysis crop.

## 4. The two page-57 crops — different roles

Both depict the same motif on the canonical page-57 scan, but intentionally retain different context.

### A. Broader contextual crop: `data/raw/page57-spiral/page57_spiral_left.png`

- Visual contents: dominant spiral plus connected stem and lower branching/root-like lines.
- Intended question: preserve the motif's larger connected structure for visual/contextual interpretation, while asking whether the curve could fit a logarithmic golden spiral better than alternatives.
- Sidecar: `data/raw/page57-spiral/page57_spiral_left.txt`.
- Sidecar records source `data/pages/57.jpg`, source SHA-256 `3f5af995b39f94f268d4aa94825a10f2429f4a3affa1921a7f627e6d1bfcfb69`, source size 746,355 bytes, rectangular crop only, no resizing/rotation/retouching, and selection rationale “spiral and connected stem/branch retained.”
- Image Git blob SHA: `89b348b81ff738abfc7cf801162b8e9a6179fafc`.
- **Still unresolved:** the sidecar leaves the crop rectangle as `[record x, y, width, height in source pixels]` and names `research/visual-evidence/page57_spiral_left.png`, not the archive path above. The exact rectangle and historical path need to be recovered from repository history or original local artifacts. Do not invent them or treat this as the same crop as the tight working crop.

### B. Tight spiral-analysis crop: `data/raw/page57-spiral/page57_spiral_working.png`

- Visual contents: dominant loop and inner terminal, with the spiral-to-stem junction retained; the long stem is clipped at top and bottom.
- Intended question: isolate the loop for centerline tracing and geometric model comparison.
- Sidecar: `data/raw/page57-spiral/page57_spiral_working.txt`.
- Source rectangle in zero-based half-open coordinates: `[160,461) × [2246,2482)`; equivalently x=160..460, y=2246..2481.
- Dimensions 301×236 px. Git blob SHA `876a7788fb5ef7dfd597a4e31577c09b15812280`.
- Canonical source scan: page 57 / `57.jpg`, 2400×3600, 746,355 bytes, SHA-256 `3f5af995b39f94f268d4aa94825a10f2429f4a3affa1921a7f627e6d1bfcfb69`.
- Annotation DB source ID: `3f167f8e-8aae-48ce-85a7-4e4f2e6b0794`.
- Verified crop SHA-256: `5d7e7e667d55ed9a44f22e486c462bdea43cdd7fae6ecbddc7d26900649d1c4a`.
- User ran the source verification locally with the actual app implementation: source hash matched; source dimensions matched; re-extracted crop dimensions matched; decoded pixel arrays were an exact match.
- No saved `regions` row exists for this source in the queried DB. This is an absence of contemporaneous annotation metadata, not a failure of the retrospective pixel-level crop verification.
- Transformation: rectangular crop only; no resizing, rotation, sharpening, or retouching.

**Do not interchange these crops.** Use the broad crop for motif connectivity/context; use the tight crop for the current 21-point trace and geometric analysis. If the analysis target changes, record that change explicitly.

## 5. Primary documents created/updated today — read in this order

- `research/research-ledger-and-visual-motif-inventory.md`: archive inventory, discipline, page workstream, current page-57 status, app implementation review, database check, and pixel verification. It also explicitly warns that no consolidated ledger of the user's separate tree/root theories was found in the tracked parent archive at the time; do not infer those theories do not exist.
- `data/raw/page57-spiral/page57_spiral_left.txt`: broad crop's source claim, selection rationale, and missing rectangle/path inconsistency.
- `data/raw/page57-spiral/page57_spiral_working.txt`: tight crop coordinates and framing rationale.
- `data/raw/page57-spiral/trace_points_working.json`: trace metadata, 21-point count, crop hash, coordinate system, and stated direction.
- `data/raw/page57-spiral/trace_points_working.csv`: immutable submitted point sequence.
- `data/raw/page57-spiral/fit_results_working.md`: first fit comparison and its limitations.
- `data/raw/page57-spiral/fit_diagnostics_working.md`: why the second diagnostic was added and the further validation it requires.
- `data/raw/page57-spiral/trace_audit_working.md`: winding anomaly and visual audit plan.
- `data/raw/page57-spiral/fit_results_working.json`, `fit_diagnostics_working.json`, `trace_audit_working.json`: machine-readable result artifacts where present; local working outputs may not all be committed.
- Scripts: `scripts/trace_page57_spiral.py`, `scripts/fit_page57_spiral.py`, `scripts/diagnose_page57_spiral.py`, `scripts/audit_page57_trace.py`.

## 6. Trace and model comparison — current state

### Submitted trace

- File: `data/raw/page57-spiral/trace_points_working.csv`.
- 21 manually clicked centerline points, crop-local coordinates, origin top-left, x right, y down.
- Definition says dominant spiral loop only; stem excluded.
- Metadata states “outer loop toward inner terminal,” but the ordered coordinates appear to run from near the inner terminal outward. This direction-label mismatch is recorded; do not silently rewrite the CSV or metadata.
- Method: interactive manual clicks; no smoothing or interpolation.

### First fit

The first script fitted `log(r)=a+b·theta`, optimizing center to minimize RMS log-radius residual. It is radial log-space fitting, not orthogonal distance in image pixels.

- Free-slope result: center about (184.62,129.56) crop px; slope about -0.19793; RMS log-radius residual about 0.1732; implied growth factor about 1.365 per quarter-turn.
- Golden-constrained result: center about (187.77,134.52) crop px; slope about -0.30635; RMS log-radius residual about 0.3222.
- Under this objective and this trace, free slope fits better. This is not a final rejection of golden-ratio intent.

### Winding-aware diagnostic

The later diagnostic jointly optimized center and logarithmic spiral parameters against radial pixel residuals and penalized angular reversals for the presumed outward trace. The reversal penalty is a heuristic, not statistically calibrated. Radial pixel residual is still not orthogonal point-to-curve distance.

Recorded results:
- Free center approx (189.7268,136.2009), slope -0.1795197, quarter-turn growth 1.32576, radial pixel RMS 7.439 px, angular span -12.985 rad (~2.067 turns), no angular reversals, but near-180° step between points 0 and 1.
- Golden center approx (194.7956,146.6002), slope -0.306349, quarter-turn growth 1.61803, radial pixel RMS 13.934 px, angular span -6.7963 rad (~1.082 turns), two reversals, reversal-penalty RMS 3.646 px.
- Leave-one-out ranges: free center x 187.59–190.62, y 135.27–144.48; RMS 6.80–7.62. Golden center x 192.11–195.50, y 144.38–149.91; RMS 11.46–14.28. These are sensitivity diagnostics, not confidence intervals.

### Interpretation limits

- The model centers imply different angular spans/winding, so their residuals are not yet a fair model-selection comparison.
- Points 0 and 1 are near the free-model center, where polar angle is unstable; this could reflect point placement, order, or center/model mismatch. Diagnostic alone cannot distinguish.
- Trace is sparse and manual. Neither radial residuals nor leave-one-out results validate a golden spiral.
- No conclusion about geometric construction, Fibonacci derivation, or symbolic intent is validated yet.

## 7. Annotation app provenance mechanics

Reviewed implementation files in `invictustitan2/lp-annotation`: `app/images.py`, `app/geometry.py`, `app/static/viewer.js`, `app/static/viewer.html`, `app/annotations.py`, `app/database.py`, `app/library.py`, `app/exports.py`.

- Source inspection hashes original bytes and records dimensions.
- Rectangle geometry uses integer, half-open source-pixel coordinates.
- Viewer maps displayed pointer coordinates to natural/source coordinates, rounds and clamps them, then canvas-renders a crop and exports PNG.
- Exporting a crop does not automatically save an annotation region in SQLite. The PNG does not itself carry the source ID/hash/rectangle metadata.
- Saving a region separately records source ID, rectangle, observation/interpretation/status, and revision history.
- Therefore the absence of a saved region row was real, but the exact tight crop association was subsequently recovered through source hash + rectangle extraction + exact pixel comparison.
- Do not retroactively pretend a region was saved at crop time.

## 8. Broader research scope

The existing ledger identifies these visual-motif workstream candidates:
1. Page 57 / scan 57 / book page 40: spiral and connected stem, current geometry target.
2. Page 20 / book page 3: index label “sprouts.”
3. Page 25 / book page 8: index label “roots.”
4. Page 74 / book page 57: index label “parable”; prior note reports a plain-Gematria solve, potential text/image cross-check only.
5. Pages 66 and 68: include because repeat-check crops already exist, not because a tree connection is established.

The index labels are search handles, not proof of shared iconography or a common mechanism. The ledger also lists existing comparison crops, guide-marked page images, transcription files, and statistical/prior-art notes; inspect those before duplicating evidence. No dedicated consolidated ledger of separate user tree/root theories was found among tracked files during today's inventory; they may exist in local workbench, nested toolkit, or prior conversation. Do not erase that uncertainty.

## 9. Next actions — strict order

1. **First: inspect the trace audit overlay against the tight crop.** The audit script is intended to create `data/raw/page57-spiral/trace_audit_overlay.png` and `trace_audit_working.json` while verifying the crop hash. Local outputs were reported as untracked. Do not ask the user to rerun it if those outputs are already available; inspect the existing overlay/artifact first.
2. Determine whether points 0–2 follow the visible centerline and whether the trace direction metadata is reversed. Record findings before changing anything.
3. Preserve the submitted CSV and JSON unchanged. If correction is needed, create a new version or a clearly named correction note with reason and audit trail.
4. Resolve the broader crop's exact rectangle and path mismatch using repository history or original local artifacts. If not recoverable, leave the rectangle explicitly unknown.
5. Plot both candidate curves over the source pixels and compare models using orthogonal point-to-curve distance or a consistent sampled parametric pixel-space metric.
6. Test reasonable centerline perturbations/redigitization and model sensitivity before interpreting fit quality.
7. Update both this handoff and the cumulative research ledger after each material finding. Keep a dated history of what changed and why.

## 10. Evidence labels

- **Verified:** directly checked against source pixels, hashes, repository records, or reproducible computation.
- **Recorded:** stated in a source sidecar/report but not independently reverified.
- **Exploratory:** depends on manual points, provisional method, or preliminary model.
- **Unresolved:** evidence is absent, inconsistent, or insufficient.

Current top-level status: source scan and tight crop association are verified; contextual crop rectangle is unresolved; submitted trace has a likely bad point 0 and reversed direction metadata (see `trace_visual_review_2026-10-11.md`); golden-spiral claim is unresolved. The immediate next task is a new, versioned manual trace, not more fit interpretation.
