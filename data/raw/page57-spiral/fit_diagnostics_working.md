# Page 57 spiral — winding-aware diagnostic plan

Status: diagnostic code added; output has not yet been executed or reviewed. No new fit result is claimed in this note.

## Why this follow-up exists

The first exploratory script independently optimized the spiral center for each model and unwrapped polar angles. Its reported angular spans differ substantially between the free-slope and golden-constrained fits (about 12.86 and 6.71 radians). Since the center affects polar angles, those fits may not represent the same winding of the trace. The residual comparison is therefore not yet a robust model-selection result.

## New diagnostic

Run:

`.wf-venv/bin/python scripts/diagnose_page57_spiral.py`

The script preserves the submitted CSV and original fit output. It writes a separate `fit_diagnostics_working.json` with:

- free-slope and golden-slope logarithmic models;
- fitted center and radius-growth factor;
- radial residuals expressed in pixels (not log-radius units);
- signed angular progression and flags for unusually large angular steps;
- leave-one-point-out parameter/error ranges as sensitivity diagnostics.

To make the trace direction explicit, the script computes signed shortest angular increments in submitted point order and penalizes positive angular reversals for the outward trace. The penalty scale is an exposed heuristic, not a statistically calibrated quantity. Large angular steps are flagged, not silently corrected.

## Interpretation guardrails

- A radial pixel residual is still not the orthogonal Euclidean distance from a point to a parametric curve.
- Leave-one-point-out ranges are diagnostics, not confidence intervals.
- Sparse manually clicked points are not independent statistical observations.
- A curve fit cannot by itself establish golden-ratio intent or symbolic meaning.
- Do not overwrite `trace_points_working.csv`, its metadata, or the original `fit_results_working.json`.
- Before using a model comparison as evidence, inspect the trace overlay against the committed crop, resolve the direction-label discrepancy, and ensure both candidate models describe the same observed loop and winding.

## Next required validation

1. Run the diagnostic and review the angular-step flags.
2. Plot the raw points and both fitted curves over the crop.
3. Replace the radial-only objective with orthogonal point-to-curve distance or a consistently sampled parametric pixel-space distance.
4. Test reasonable centerline perturbations / redigitization and compare fit stability.
5. Only then interpret whether a golden constraint is supported, rejected, or unresolved.
