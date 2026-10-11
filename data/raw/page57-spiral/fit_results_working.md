# Page 57 spiral — first trace/model comparison

Status: exploratory result from the manually clicked working-crop trace. Not a validated geometric conclusion.

## Inputs
- Working crop: `data/raw/page57-spiral/page57_spiral_working.png` (301 × 236 px).
- Trace: `data/raw/page57-spiral/trace_points_working.csv` (21 points).
- Trace metadata: `data/raw/page57-spiral/trace_points_working.json`.
- The metadata says the trace proceeds outer-to-inner, but the coordinate sequence appears to proceed inner-to-outer. The submitted CSV is preserved unchanged; this direction discrepancy must be resolved in the record before treating results as final.

## Exploratory fit method
For each candidate center, calculate polar angle and radius for each clicked point, unwrap angle in trace order, then fit
`log(r) = a + b·theta`.
The center is optimized to minimize RMS residual in log-radius. This is a radial log-space comparison, not an orthogonal-distance fit in image pixels.

For a golden logarithmic spiral, the magnitude of the slope is `ln(phi)/(pi/2) ≈ 0.30635`, corresponding to a radius growth factor of `phi ≈ 1.618` per quarter-turn. The trace's outward direction yields a negative signed slope under the coordinate ordering used here.

## Preliminary result
- Free logarithmic spiral: fitted center approximately (184.62, 129.56) crop pixels; slope `b ≈ -0.19793`; RMS log-radius residual ≈ 0.1732; implied radius growth ≈ 1.365 per quarter-turn.
- Golden logarithmic spiral: best center found in the deterministic multi-start search approximately (187.77, 134.52) crop pixels; fixed slope `b ≈ -0.30635`; RMS log-radius residual ≈ 0.3222.
- Under this particular objective and trace, the free-slope logarithmic spiral has materially lower residual than the golden-constrained spiral. The free-slope residual corresponds to a multiplicative scale of roughly 1.19, while the golden-constrained residual corresponds to roughly 1.38.

## Interpretation and limits
This first comparison does **not** support treating the trace as a precise golden logarithmic spiral. It does not establish that the motif is or is not intentionally based on the golden ratio: the trace is sparse and manually clicked, the curve center is estimated, and the objective is not an orthogonal pixel-distance measure. Trace-direction metadata should be corrected in a follow-up annotation, not by silently changing the submitted data. Next validation should inspect point placement against the source pixels, test trace sensitivity, and compare alternative curve models using a consistent pixel-space metric.

## Reproduction
Run `.wf-venv/bin/python scripts/fit_page57_spiral.py` from the repository root. It writes `data/raw/page57-spiral/fit_results_working.json` locally.
