# Page 57 trace audit — 2026-10-11

## Observed in diagnostic output

The winding-aware diagnostic ran successfully on the committed 21-point trace. Its output is exploratory only. A nearly 180° angular step occurs between submitted points 0 and 1 for the free-model center, and the golden-constrained model has two angular reversals. The free and golden fits infer about 2.07 versus 1.08 turns, so their current radial residuals are not a sufficient basis for model selection.

The first two points are near the free-model fitted center, making polar angle unstable there. This could be point placement, trace ordering, or center/model mismatch; the diagnostic alone cannot distinguish these explanations. Do not reorder or delete points without reviewing the trace overlay.

## Next audit

Run:

`.wf-venv/bin/python scripts/audit_page57_trace.py`

This writes:
- `data/raw/page57-spiral/trace_audit_overlay.png`: crop with numbered points and connecting segments;
- `data/raw/page57-spiral/trace_audit_working.json`: point-by-point segment length, radial change, angular step, and flags.

The script verifies the crop SHA-256 against the trace metadata before creating outputs. It does not alter the submitted trace. Inspect the overlay visually to determine whether points 0–2 lie on the same centerline and whether the stated trace direction is accurate. Only after that audit should we re-trace or perform orthogonal pixel-space curve fitting.

## Current conclusion

No validated golden-spiral conclusion. The current free model has lower radial pixel RMS, but the model comparison is confounded by center/angle coupling and inconsistent inferred winding. The correct next task is trace validation, not further interpretation.
