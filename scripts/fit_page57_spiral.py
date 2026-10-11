#!/usr/bin/env python3
"""Exploratory radial-log fit for the page 57 manual spiral trace.

This is not a pixel-edge detector or an orthogonal-distance fit. It fits
log(r) = a + b*theta around a candidate center, using the manually clicked
centerline points. See the accompanying note for limitations.
"""
from pathlib import Path
import csv, json, math
import numpy as np
from scipy.optimize import minimize

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data/raw/page57-spiral"
CSV_PATH = DATA / "trace_points_working.csv"
JSON_PATH = DATA / "trace_points_working.json"
OUT_PATH = DATA / "fit_results_working.json"

with CSV_PATH.open(newline="") as f:
    rows = list(csv.DictReader(f))
pts = np.array([[float(r["x_crop_px"]), float(r["y_crop_px"])] for r in rows])
trace_meta = json.loads(JSON_PATH.read_text())
phi = (1 + math.sqrt(5)) / 2
b_golden_magnitude = math.log(phi) / (math.pi / 2)

def evaluate(center, fixed_b=None):
    d = pts - np.asarray(center)
    r = np.hypot(d[:, 0], d[:, 1])
    if np.min(r) < 1e-6:
        return None
    theta = np.unwrap(np.arctan2(d[:, 1], d[:, 0]))
    log_r = np.log(r)
    if fixed_b is None:
        design = np.column_stack([np.ones(len(theta)), theta])
        a, b = np.linalg.lstsq(design, log_r, rcond=None)[0]
    else:
        b = fixed_b
        a = float(np.mean(log_r - b * theta))
    residual = log_r - (a + b * theta)
    return {
        "center_crop_px": [float(center[0]), float(center[1])],
        "log_radius_intercept_a": float(a),
        "log_radius_slope_b": float(b),
        "rms_log_radial_residual": float(np.sqrt(np.mean(residual**2))),
        "multiplicative_rms_factor": float(np.exp(np.sqrt(np.mean(residual**2)))),
        "theta_span_radians": float(theta[-1] - theta[0]),
        "radius_first_px": float(r[0]),
        "radius_last_px": float(r[-1]),
        "quarter_turn_growth_factor": float(np.exp(abs(b) * math.pi / 2)),
    }

def objective(center, fixed_b=None):
    out = evaluate(center, fixed_b)
    if out is None:
        return 1e6
    return out["rms_log_radial_residual"] ** 2

# Multiple deterministic starting centers reduce dependence on one initial guess.
seeds = [[185,130], [175,120], [190,140], [180,100], [200,150],
         [160,140], [200,100], [185,145], [170,130], [195,120]]
fits = {}
for label, fixed_b in [
    ("free_log_spiral", None),
    ("golden_log_spiral", -b_golden_magnitude),
]:
    candidates = []
    for seed in seeds:
        opt = minimize(lambda c: objective(c, fixed_b), seed,
                       method="Nelder-Mead",
                       options={"maxiter": 3000, "xatol": 1e-7, "fatol": 1e-10})
        candidates.append(evaluate(opt.x, fixed_b))
    fits[label] = min(candidates, key=lambda item: item["rms_log_radial_residual"])

result = {
    "status": "exploratory; not a validated geometric conclusion",
    "trace_csv": str(CSV_PATH.relative_to(ROOT)),
    "trace_metadata": str(JSON_PATH.relative_to(ROOT)),
    "trace_image_sha256": trace_meta["image_sha256"],
    "point_count": len(pts),
    "method": "minimize RMS residual in log-radius about a fitted center; angle is unwrapped in trace order; center search uses deterministic multi-start Nelder-Mead",
    "golden_spiral_definition": {
        "phi": phi,
        "quarter_turn_growth_factor": phi,
        "absolute_log_radius_slope": b_golden_magnitude,
        "trace_direction_signed_slope": -b_golden_magnitude,
    },
    "models": fits,
    "limitations": [
        "Input is a manually clicked, sparse centerline trace, not a stroke segmentation.",
        "Residuals are radial log-space residuals, not orthogonal pixel distances.",
        "The fitted center and result may be affected by trace placement, curve segmentation, and angle unwrapping.",
        "This comparison tests a golden logarithmic spiral against a free logarithmic spiral only; it does not establish symbolic intent or exclude other curve families."
    ],
}
OUT_PATH.write_text(json.dumps(result, indent=2) + "\n")
print(json.dumps(result, indent=2))
