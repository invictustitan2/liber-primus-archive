#!/usr/bin/env python3
"""Exploratory page-57 spiral comparison with pixel-radius objective and winding diagnostics.

This minimizes radial distance in pixels, not orthogonal Euclidean distance to the
parametric curve. The manual trace and original fit files are never modified.
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

with CSV_PATH.open(newline="") as f:
    rows = list(csv.DictReader(f))
pts = np.array([[float(r["x_crop_px"]), float(r["y_crop_px"])] for r in rows])
meta = json.loads(META_PATH.read_text())
phi = (1 + math.sqrt(5)) / 2
b_golden = -math.log(phi) / (math.pi / 2)
REVERSAL_PENALTY_PX_PER_RAD = 30.0
MAX_ANGULAR_STEP_DEG = 120.0
SEEDS = [[185,130], [175,120], [190,140], [180,100], [200,150],
         [160,140], [200,100], [185,145], [170,130], [195,120]]

def geometry(center, points):
    d = points - np.asarray(center)
    r = np.hypot(d[:, 0], d[:, 1])
    if np.min(r) < 1e-5:
        return None
    raw = np.arctan2(d[:, 1], d[:, 0])
    inc = np.arctan2(np.sin(np.diff(raw)), np.cos(np.diff(raw)))
    theta = np.r_[0.0, np.cumsum(inc)]
    return r, theta, inc

def unpack_and_score(params, fixed_b, points):
    center = np.asarray(params[:2])
    a = float(params[2])
    b = float(fixed_b if fixed_b is not None else params[3])
    geom = geometry(center, points)
    if geom is None:
        return None
    r, theta, inc = geom
    pred = np.exp(np.clip(a + b * theta, -20, 20))
    residual = r - pred
    rms = float(np.sqrt(np.mean(residual**2)))
    # Submitted order is expected to move outward with decreasing polar angle.
    reversal = np.maximum(inc, 0.0)
    reversal_rms = float(np.sqrt(np.mean((REVERSAL_PENALTY_PX_PER_RAD * reversal)**2))) if len(inc) else 0.0
    return {
        "score": rms**2 + reversal_rms**2, "center": center, "a": a, "b": b,
        "r": r, "theta": theta, "inc": inc, "pred": pred,
        "residual": residual, "rms_px": rms, "reversal_rms_px": reversal_rms,
    }

def fit(fixed_b=None, points=pts):
    # For each starting center, initialize a and (if free) b by a log-radius regression,
    # then optimize the actual radial-pixel residual objective.
    candidates = []
    for seed in SEEDS:
        g = geometry(seed, points)
        if g is None:
            continue
        r, theta, _ = g
        ab = np.linalg.lstsq(np.c_[np.ones(len(theta)), theta], np.log(r), rcond=None)[0]
        a0 = float(ab[0])
        x0 = [float(seed[0]), float(seed[1]), a0]
        if fixed_b is None:
            x0.append(float(ab[1]))
        def objective(p):
            out = unpack_and_score(p, fixed_b, points)
            return out["score"] if out is not None else 1e12
        opt = minimize(objective, x0, method="Nelder-Mead",
                       options={"maxiter": 5000, "xatol": 1e-7, "fatol": 1e-8})
        out = unpack_and_score(opt.x, fixed_b, points)
        if out is not None:
            candidates.append(out)
    return min(candidates, key=lambda x: x["score"])

models = {}
fits = {}
for name, fixed_b in [("free_log_spiral", None), ("golden_log_spiral", b_golden)]:
    m = fit(fixed_b)
    fits[name] = m
    inc_deg = np.degrees(m["inc"])
    models[name] = {
        "center_crop_px": [float(x) for x in m["center"]],
        "log_radius_intercept_a": m["a"],
        "log_radius_slope_b": m["b"],
        "quarter_turn_growth_factor": float(np.exp(abs(m["b"]) * math.pi / 2)),
        "radial_pixel_rms": m["rms_px"],
        "radial_pixel_residuals": [float(x) for x in m["residual"]],
        "theta_span_radians": float(m["theta"][-1] - m["theta"][0]),
        "theta_span_turns": float(abs(m["theta"][-1] - m["theta"][0]) / (2 * math.pi)),
        "angular_reversal_count": int(np.sum(m["inc"] > 1e-6)),
        "angular_steps_over_120_degrees": [
            {"between_point_indices": [int(i), int(i+1)], "degrees": float(v)}
            for i, v in enumerate(inc_deg) if abs(v) > MAX_ANGULAR_STEP_DEG
        ],
        "reversal_penalty_rms_px": m["reversal_rms_px"],
        "optimization_score": m["score"],
    }

# Leave-one-point-out sensitivity. These ranges are diagnostics, not confidence intervals.
sensitivity = {}
for name, fixed_b in [("free_log_spiral", None), ("golden_log_spiral", b_golden)]:
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
    "method": "jointly optimize center and logarithmic-spiral parameters against radial pixel residuals; signed shortest angular increments preserve submitted point order; positive angular reversals receive an explicit heuristic penalty",
    "reversal_penalty_px_per_rad": REVERSAL_PENALTY_PX_PER_RAD,
    "metric_caveat": "radial distance error is measured in pixels but is not orthogonal Euclidean distance to the parametric curve",
    "golden_definition": {"phi": phi, "quarter_turn_growth_factor": phi, "signed_slope_for_outward_trace": b_golden},
    "models": models,
    "leave_one_point_out_sensitivity": sensitivity,
    "trace_order_diagnostics": {
        "point_order": "submitted order preserved unchanged",
        "direction_metadata": meta.get("direction"),
        "coordinate_order_assessment": "initial inspection suggests the points may proceed inner-to-outer, contrary to the metadata; verify against the crop",
        "warning": "angular steps above 120 degrees are flagged as possible trace-order, center, or point-placement problems"
    },
    "limitations": [
        "Sparse manual clicks, not image-derived stroke centerline.",
        "Center and angle progression remain coupled; reversal penalty is a heuristic.",
        "Radial pixel residual is not orthogonal point-to-curve distance.",
        "Leave-one-point-out ranges are sensitivity diagnostics, not confidence intervals.",
        "A good curve fit does not establish symbolic intent."
    ],
}
OUT_PATH.write_text(json.dumps(result, indent=2) + "\n")
print(json.dumps(result, indent=2))
