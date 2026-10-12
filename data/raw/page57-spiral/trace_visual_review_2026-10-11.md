# Page 57 trace visual review — 2026-10-11

> **Superseded for current fixed-center analysis by user clarification (2026-10-11):** point 0 `(176.048, 124.437)` is the manually placed fixed center/reference, not a spiral sample. Points 1–20 are the 20 spiral samples. The earlier assessment below that point 0 is a bad tracing click applies to the prior mistaken interpretation of all 21 coordinates as curve samples and must not be used to recommend deleting or replacing point 0. The original trace remains unchanged. The direction-label discrepancy for points 1–20 remains a separate metadata issue.

## Scope and evidence

This is a first visual review of the committed tight crop (`page57_spiral_working.png`) alongside the unchanged `trace_points_working.csv` point coordinates. The remote archive does **not** contain `trace_audit_overlay.png` or `trace_audit_working.json`; therefore this review does not claim to have inspected those generated artifacts. The source crop itself and all 21 coordinate rows were inspected.

## Findings

1. **Trace direction label is inconsistent with point order.** Points 1–20 run from the inner terminal outward around the loop. That is the reverse of metadata's stated “outer loop toward inner terminal.” This is a recorded inconsistency, not a reason to rewrite the source files silently.
2. **Superseded interpretation:** the earlier review called point 0 a likely tracing error because it treated all 21 coordinates as curve samples. Under the user's clarified geometry, point 0 is the fixed center/reference, so that visual claim and the 0→1 segment-as-curve-step inference do not apply to the current fitting problem. The sequence of samples to assess is points 1–20.
3. **Do not infer that point 0 should simply be deleted and the fit rerun.** The visual mismatch strongly suggests a bad click, but the appropriate replacement coordinate, and whether the trace should begin at the terminal or at a separately traced outer endpoint, should be established with a deliberate re-trace. Keep the submitted CSV/JSON immutable.
4. The current trace excludes the stem by definition. The crop retains the spiral-to-stem junction; the trace should follow the spiral centerline only, not continue down the stem.

## Current action status

Do not create a new trace based on the superseded point-0 assessment. The user has fixed the center at point 0 and designated points 1–20 as curve samples. The fixed-center radial-log baseline is already recorded in `WORKING_CONTEXT.md`; the intended next geometric comparison is orthogonal or consistently sampled pixel-space distance for those 20 samples, with the center held fixed. Local overlay generation and inspection remain the user's responsibility. The direction metadata mismatch is separate and should be addressed only through a documented amendment or versioned metadata if/when authorized.

## Status

- Crop/source pixel association: **verified**.
- Point 0 off-centerline / likely bad click: **visual assessment; high confidence but not a pixel-mask measurement**.
- Direction metadata mismatch: **verified from coordinate sequence**.
- Correct replacement point and geometric model conclusion: **unresolved**.
