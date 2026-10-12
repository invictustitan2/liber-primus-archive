# Page 57 trace audit — visual review of committed crop and point sequence

Date: 2026-10-11

## Scope and evidence

Reviewed the committed tight crop `data/raw/page57-spiral/page57_spiral_working.png` (301 × 236 px) and the unchanged 21-point sequence in `trace_points_working.csv`. The crop is source-pixel verified; its SHA-256 is `5d7e7e667d55ed9a44f22e486c462bdea43cdd7fae6ecbddc7d26900649d1c4a`.

This is a qualitative review of the displayed crop against the recorded coordinates, not a pixel-segmentation or centerline ground-truth audit. No trace points were changed.

## Findings

1. **Trace direction metadata is reversed or otherwise mislabeled.** Point indices run from the inner region toward the long outer continuation: points 8–20 move around the large loop and then along the outward tail toward the left. This conflicts with JSON metadata saying “outer loop toward inner terminal.” The coordinate order itself should be preserved; correct the metadata only in a versioned follow-up after confirming the intended definition.
2. **Points 0–2 require re-tracing before fitting.** Their coordinates are (176.048, 124.437), (193.321, 139.292), and (195.048, 110.273). The 0→1 segment cuts diagonally across the tight inner region, then 1→2 reverses sharply upward. These points do not form a smooth, credible continuation of the spiral centerline as a sequence. This agrees with the diagnostic's near-180° angular-step flag for points 0 and 1.
3. **Do not treat the current fit comparison as model-selection evidence.** A local trace defect near the inner terminal can strongly perturb the fitted center and polar angle, and the competing fits already infer different winding spans.
4. **No point-level correction is made here.** The correct centerline location at the inner terminal should be determined from the visible stroke, with an explicit tracing convention (center of stroke, not either edge). The original 21-point CSV and JSON remain immutable.

## Next action

Create a separate candidate trace, leaving `trace_points_working.csv` unchanged. Re-digitize the inner terminal and first few turns with closer sampling, then plot the candidate and the original points over the crop. Compare the candidate visually before rerunning fits. Record which points were changed and why. Do not infer a golden-ratio construction from the current trace.

## Status

- Source scan and tight crop association: verified.
- Broad contextual crop rectangle/path: unresolved.
- Current trace direction label: inconsistent with point order.
- Inner-region point placement: suspect; requires a candidate re-trace.
- Golden-spiral hypothesis: unresolved.
