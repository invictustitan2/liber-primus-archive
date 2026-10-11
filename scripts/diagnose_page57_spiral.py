#!/usr/bin/env python3
"""Comparable page-57 spiral diagnostic using pixel-radius residuals and winding checks.

This is an exploratory diagnostic, not a pixel-edge or orthogonal-distance fit.
It preserves the submitted manual trace and writes a separate result file.
"""
from pathlib import Path
import csv, json, math
import numpy as np
from scipy.optimize import minimize

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data/raw/page57-spiral"
CSV_PATH = DATA / "trace_points_working.csv"
META_PATH = DATA / "trace_points_working.json"
OUT_PATH = DATA / "fit_diagnostics_working.json"

rows = list(csv.DictReader(CSV_PATH.open(newline="")))
pts = np.array([[float(r["x_crop_px"]), float(r["y_crop_px"])] for r in rows])
meta = json.loads(META_PATH.read_text())
phi = (1 + math.sqrt(5)) / 2
b_golden = -math.log(phi) / (math.pi / 2)
# Explicitly penalize angular reversals so both models are assessed on a
# consistently wound trace. The penalty is reported and is not a likelihood.
REVERSAL_PENALTY_PX_PER_RAD = 30.0
MAX_ACCEPTABLE_STEP_DEG = 120.0

def evaluate(center, fixed_b=None, points=pts):
    d = points - np.asarray(center)
    r = np.hypot(d[:, 0], d[:, 1])
    if np.min(r) < 1e-5:
        return None
    raw = np.arctan2(d[:, 1], d[:, 0])
    # Signed shortest angular increments preserve observed point order.
    inc = np.arctan2(np.sin(np.diff(raw)), np.cos(np.diff(raw)))
    theta = np.r_[0.0, np.cumsum(inc)]
    log_r = np.log(r)
    if fixed_b is None:
        a, b = np.linalg.lstsq(np.c_[np.ones(len(theta)), theta], log_r, rcond=None)[0]
    else:
        b = float(fixed_b)
        a = float(np.mean(log_r - b * theta))
    predicted_r = np.exp(np.clip(a + b * theta, -30, 30))
    radial_resid = r - predicted_r
    rms_px = float(np.sqrt(np.mean(radial_resid**2)))
    reversal_amount = np.maximum(inc, 0.0)  # expected outward trace has decreasing theta
    reversal_rms_px = float(np.sqrt(np.mean((REVERSAL_PENALTY_PX_PER_RAD * reversal_amount)**2))) if len(inc) else 0.0
    score = rms_px**2 + reversal_rms_px**2
    return {
        "score": score, "center": np.asarray(center), "a": float(a), "b": float(b),
        "theta": theta, "inc": inc, "r": r, "predicted_r": predicted_r,
        "radial_residual": radial_resid, "rms_px": rms_px,
        "reversal_rms_px": reversal_rms_px,
    }

def fit(fixed_b=None, points=pts):
    seeds = [[185,130], [175,120], [190,140], [180,100], [200,150],
             [160,140], [200,100], [185,145], [170,130], [195,120]]
    candidates = []
    for seed in seeds:
        opt = minimize(
            lambda c: (evaluate(c, fixed_b, points)["score"]
                       if evaluate(c, fixed_b, points) is not None else 1e12),
            seed, method="Nelder-Mead",
            options={"maxiter": 4000, "xatol": 1e-7, "fatol": 1e-8},
        )
        candidate = evaluate(opt.x, fixed_b, points)
        if candidate is not None:
            candidates.append(candidate)
    return min(candidates, key=lambda x: x["score"])

models = {}
for name, fixed_b in [("free_log_spiral", None), ("golden_log_spiral", b_golden)]:
    m = fit(fixed_b)
    inc_deg = np.degrees(m["inc"])
    models[name] = {
        "center_crop_px": [float(x) for x in m["center"]],
        "log_radius_intercept_a": m["a"],
        "log_radius_slope_b": m["b"],
        "quarter_turn_growth_factor": float(np.exp(abs(m["b"]) * math.pi / 2)),
        "radial_pixel_rms": m["rms_px"],
        "radial_pixel_residuals": [float(x) for x in m["radial_residual"]],
        "theta_span_radians": float(m["theta"][-1] - m["theta"][0]),
        "theta_span_turns": float(abs(m["theta"][-1] - m["theta"][0]) / (2 * math.pi)),
        "angular_reversal_count": int(np.sum(m["inc"] > 1e-6)),
        "angular_steps_over_120_degrees": [
            {"between_point_indices": [int(i), int(i+1)], "degrees": float(v)}
            for i, v in enumerate(inc_deg) if abs(v) > MAX_ACCEPTABLE_STEP_DEG
        ],
        "reversal_penalty_rms_px": m["reversal_rms_px"],
        "optimization_score": m["score"],
    }

# Leave-one-point-out sensitivity: refit all points except one, using each
# model's full-fit center as the sole seed plus a deterministic local seed grid.
# This is diagnostic only; a manual trace is not a statistical sample.
sensitivity = {}
for name, fixed_b in [("free_log_spiral", None), ("golden_log_spiral", b_golden)]:
    full = fit(fixed_b)
    centers, errors = [], []
    for i in range(len(pts)):
        sub = np.delete(pts, i, axis=0)
        m = fit(fixed_b, sub)
        centers.append(m["center"].tolist())
        errors.append(m["rms_px"])
    centers = np.asarray(centers)
    sensitivity[name] = {
        "leave_one_out_center_x_range_px": [float(centers[:,0].min()), float(centers[:,0].max())],
        "leave_one_out_center_y_range_px": [float(centers[:,1].min()), float(centers[:,1].max())],
        "leave_one_out_rms_px_range": [float(min(errors)), float(max(errors))],
    }

result = {
    "status": "exploratory diagnostic; not a validated geometric conclusion",
    "trace_csv": str(CSV_PATH.relative_to(ROOT)),
    "trace_metadata": str(META_PATH.relative_to(ROOT)),
    "image_sha256": meta["image_sha256"],
    "point_count": len(pts),
    "method": "fit log(radius) versus cumulative signed shortest angular increments about a fitted center; compare radial residuals in pixels; penalize angular reversals",
    "reversal_penalty_px_per_rad": REVERSAL_PENALTY_PX_PER_RAD,
    "important_metric_caveat": "radial pixel residual is not orthogonal distance from points to the parametric curve",
    "golden_definition": {"phi": phi, "quarter_turn_growth_factor": phi, "signed_slope_for_outward_trace": b_golden},
    "models": models,
    "leave_one_point_out_sensitivity": sensitivity,
    "trace_order_diagnostics": {
        "point_order_as_submitted": "preserved unchanged",
        "direction_metadata": meta.get("direction"),
        "observed_coordinate_order": "points appear to proceed from inner region toward outer arc; metadata says outer toward inner",
        "warning": "Any angular step above 120 degrees is flagged; a near-180-degree step can indicate a trace-order, center, or point-placement problem.",
    },
    "limitations": [
        "Sparse manual points, not image-derived stroke centerline.",
        "Center and angle progression remain coupled; reversal penalty is an explicit heuristic.",
        "Radial pixel residual is not orthogonal point-to-curve distance.",
        "Leave-one-point-out ranges are sensitivity diagnostics, not confidence intervals.",
        "A good curve fit does not establish symbolic intent."
    ],
}
OUT_PATH.write_text(json.dumps(result, indent=2) + "\n")
print(json.dumps(result, indent=2))
