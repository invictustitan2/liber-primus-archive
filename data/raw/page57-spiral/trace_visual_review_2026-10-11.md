# Page 57 trace visual review — 2026-10-11

## Scope and evidence

This is a first visual review of the committed tight crop (`page57_spiral_working.png`) alongside the unchanged `trace_points_working.csv` point coordinates. The remote archive does **not** contain `trace_audit_overlay.png` or `trace_audit_working.json`; therefore this review does not claim to have inspected those generated artifacts. The source crop itself and all 21 coordinate rows were inspected.

## Findings

1. **Trace direction label is inconsistent with point order.** Points 1–20 run from the inner terminal outward around the loop. That is the reverse of metadata's stated “outer loop toward inner terminal.” This is a recorded inconsistency, not a reason to rewrite the source files silently.
2. **Point 0 is a likely tracing error.** Its coordinate is (176.048, 124.437). On the displayed crop it lies inside the white interior of the curl rather than on the black centerline. The segment from point 0 to point 1 (193.321, 139.292) cuts diagonally across the curl's interior; the subsequent sequence 1→2→3→… follows the visible inner curl and then progresses around the larger loop. This agrees with the previously reported near-180° angular step between points 0 and 1.
3. **Do not infer that point 0 should simply be deleted and the fit rerun.** The visual mismatch strongly suggests a bad click, but the appropriate replacement coordinate, and whether the trace should begin at the terminal or at a separately traced outer endpoint, should be established with a deliberate re-trace. Keep the submitted CSV/JSON immutable.
4. The current trace excludes the stem by definition. The crop retains the spiral-to-stem junction; the trace should follow the spiral centerline only, not continue down the stem.

## Recommended next action

Create a separate, versioned trace after re-clicking the spiral centerline on the verified tight crop. Preserve all original points and compare old/new traces overlaid on the source pixels. At minimum, explicitly verify the inner terminal and points around the first turn; do not let model-fit residuals choose points. Correct the direction metadata in the new trace to match its actual point order. Only then rerun geometric model comparison.

## Status

- Crop/source pixel association: **verified**.
- Point 0 off-centerline / likely bad click: **visual assessment; high confidence but not a pixel-mask measurement**.
- Direction metadata mismatch: **verified from coordinate sequence**.
- Correct replacement point and geometric model conclusion: **unresolved**.
