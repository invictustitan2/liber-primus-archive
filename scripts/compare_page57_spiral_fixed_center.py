#!/usr/bin/env python3
"""Compare free and golden logarithmic spirals at the user's fixed reference center.

This script does not modify the submitted trace or crop. It writes a new overlay
and JSON report locally. Distances are Euclidean point-to-parametric-curve
distances, approximated by bounded one-dimensional minimization for each point.
"""
from pathlib import Path
import csv
import hashlib
import json
import math

import numpy as np
from PIL import Image, ImageDraw, ImageFont
from scipy.optimize import minimize, minimize_scalar

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data/raw/page57-spiral"
IMAGE_PATH = DATA / "page57_spiral_working.png"
CSV_PATH = DATA / "trace_points_working.csv"
META_PATH = DATA / "trace_points_working.json"
OVERLAY_PATH = DATA / "fixed_center_orthogonal_comparison.png"
REPORT_PATH = DATA / "fixed_center_orthogonal_comparison.json"

EXPECTED_IMAGE_SHA256 = "5d7e7e667d55ed9a44f22e486c462bdea43cdd7fae6ecbddc7d26900649d1c4a"
PHI = (1 + math.sqrt(5)) / 2
B_GOLDEN = -math.log(PHI) / (math.pi / 2)

actual_hash = hashlib.sha256(IMAGE_PATH.read_bytes()).hexdigest()
if actual_hash != EXPECTED_IMAGE_SHA256:
    raise SystemExit(
        f"Crop hash mismatch: expected {EXPECTED_IMAGE_SHA256}, got {actual_hash}. "
        "No outputs written."
    )

meta = json.loads(META_PATH.read_text())
with CSV_PATH.open(newline="") as f:
    rows = list(csv.DictReader(f))
all_points = np.array(
    [[float(r["x_crop_px"]), float(r["y_crop_px"])] for r in rows],
    dtype=float,
)
if len(all_points) != 21:
    raise SystemExit(f"Expected 21 submitted rows; found {len(all_points)}.")

# Explicit role separation: row 0 is the fixed visual reference center, not a
# curve sample. Rows 1–20 are the submitted trace samples, unchanged.
center = all_points[0].copy()
points = all_points[1:].copy()
delta = points - center
raw_theta = np.arctan2(delta[:, 1], delta[:, 0])
theta_obs = np.unwrap(raw_theta)
if not np.all(np.diff(theta_obs) < 0):
    print("WARNING: observed point angles are not strictly decreasing; inspect the overlay.")
# Permit modest extension past the observed angular endpoints when finding the
# closest point on the fitted curve. Every model uses this same angular domain.
theta_min = float(theta_obs.min() - math.pi / 2)
theta_max = float(theta_obs.max() + math.pi / 2)

def curve_xy(theta, a, b):
    radius = np.exp(np.clip(a + b * theta, -20, 20))
    return np.column_stack((
        center[0] + radius * np.cos(theta),
        center[1] + radius * np.sin(theta),
    ))

def closest_for_point(point, a, b, grid_size=4097):
    """Approximate the global nearest point by bracketing every grid-local minimum.

    A single bounded minimization over the full interval is unsafe here because
    squared distance to a logarithmic spiral can be multimodal. This routine
    samples the full shared interval, refines every detected local-minimum
    bracket, and explicitly includes both interval endpoints. The finite grid
    makes this a convergence-checkable numerical approximation, not a formal
    global-minimum proof.
    """
    grid = np.linspace(theta_min, theta_max, grid_size)
    curve = curve_xy(grid, a, b)
    offsets = curve - point
    values = np.einsum("ij,ij->i", offsets, offsets)

    # Include both endpoints; the closest point may lie on a search boundary.
    candidates = [
        (float(values[0]), float(grid[0])),
        (float(values[-1]), float(grid[-1])),
    ]

    # Find all sampled local-minimum brackets, not just the best grid sample.
    local_minima = np.flatnonzero(
        (values[1:-1] <= values[:-2])
        & (values[1:-1] <= values[2:])
    ) + 1

    def squared_distance(theta):
        q = curve_xy(np.array([theta]), a, b)[0]
        return float(np.sum((q - point) ** 2))

    for i in local_minima:
        opt = minimize_scalar(
            squared_distance,
            bounds=(float(grid[i - 1]), float(grid[i + 1])),
            method="bounded",
            options={"xatol": 1e-10, "maxiter": 300},
        )
        candidates.append((squared_distance(opt.x), float(opt.x)))

    best_d2, best_theta = min(candidates, key=lambda item: item[0])
    q = curve_xy(np.array([best_theta]), a, b)[0]
    return math.sqrt(max(0.0, best_d2)), best_theta, q

def score(a, b, include_details=False):
    details = [closest_for_point(p, a, b) for p in points]
    distances = np.array([d[0] for d in details])
    mse = float(np.mean(distances ** 2))
    if include_details:
        return mse, distances, details
    return mse

# Use the observed polar coordinates for a deterministic initial estimate of a
# and b. The final objective is orthogonal Euclidean distance, not radial error.
radii = np.hypot(delta[:, 0], delta[:, 1])
a0, b0 = np.linalg.lstsq(
    np.column_stack([np.ones(len(theta_obs)), theta_obs]),
    np.log(radii), rcond=None,
)[0]

free_opt = minimize(
    lambda z: score(float(z[0]), float(z[1])),
    x0=np.array([float(a0), float(b0)]),
    method="Nelder-Mead",
    options={"maxiter": 2500, "xatol": 1e-7, "fatol": 1e-8},
)
if not free_opt.success and not np.isfinite(free_opt.fun):
    raise SystemExit(f"Free-slope optimization failed: {free_opt.message}")
a_free, b_free = map(float, free_opt.x)

# For the golden model, only scale/intercept is fitted; the reference center
# and theoretical quarter-turn growth are fixed.
golden_opt = minimize_scalar(
    lambda a: score(float(a), B_GOLDEN),
    bounds=(-5.0, 8.0), method="bounded",
    options={"xatol": 1e-9, "maxiter": 500},
)
a_golden = float(golden_opt.x)

def summarize(name, a, b):
    mse, distances, details = score(a, b, include_details=True)
    return {
        "model": name,
        "fixed_center_crop_px": [float(center[0]), float(center[1])],
        "log_radius_intercept_a": float(a),
        "log_radius_slope_b": float(b),
        "quarter_turn_growth_factor": float(math.exp(abs(b) * math.pi / 2)),
        "orthogonal_distance_rms_px": float(math.sqrt(mse)),
        "orthogonal_distance_mean_px": float(np.mean(distances)),
        "orthogonal_distance_max_px": float(np.max(distances)),
        "per_point_distances_px": [
            {"trace_point_index": int(i + 1), "distance_px": float(d)}
            for i, d in enumerate(distances)
        ],
        "closest_curve_parameters_theta_rad": [float(d[1]) for d in details],
    }

models = {
    "free_log_spiral": summarize("free_log_spiral", a_free, b_free),
    "golden_log_spiral": summarize("golden_log_spiral", a_golden, B_GOLDEN),
}

# Draw both model curves over the unmodified source crop. This is an overlay
# artifact only; it does not edit the source image or the trace CSV/JSON.
im = Image.open(IMAGE_PATH).convert("RGB")
draw = ImageDraw.Draw(im)
try:
    font = ImageFont.truetype("DejaVuSans.ttf", 10)
except OSError:
    font = ImageFont.load_default()

# Trace polyline and point markers.
for i in range(len(points) - 1):
    draw.line((tuple(points[i]), tuple(points[i + 1])), fill=(235, 55, 55), width=1)
for i, (x, y) in enumerate(points, start=1):
    rr = 2
    draw.ellipse((x-rr, y-rr, x+rr, y+rr), fill=(255, 235, 0), outline=(0, 0, 0), width=1)
    draw.text((x+3, y-8), str(i), fill=(255, 255, 0), font=font, stroke_width=1, stroke_fill=(0, 0, 0))
cx, cy = center
draw.ellipse((cx-4, cy-4, cx+4, cy+4), fill=(255, 0, 255), outline=(255, 255, 255), width=1)
draw.text((cx+5, cy+4), "fixed center", fill=(255, 0, 255), font=font, stroke_width=1, stroke_fill=(0, 0, 0))

theta_plot = np.linspace(theta_min, theta_max, 2400)
for name, a, b, color, label in [
    ("free_log_spiral", a_free, b_free, (30, 130, 255), "free"),
    ("golden_log_spiral", a_golden, B_GOLDEN, (30, 220, 100), "golden"),
]:
    xy = curve_xy(theta_plot, a, b)
    # Clip drawing to the image; PIL handles out-of-bounds coordinates.
    draw.line([tuple(p) for p in xy], fill=color, width=2)
    first = xy[0]
    draw.text((float(first[0]), float(first[1])), label, fill=color, font=font, stroke_width=1, stroke_fill=(0,0,0))

im.save(OVERLAY_PATH)

result = {
    "status": "exploratory; fixed-center orthogonal-distance comparison",
    "crop": str(IMAGE_PATH.relative_to(ROOT)),
    "crop_sha256": actual_hash,
    "trace_csv": str(CSV_PATH.relative_to(ROOT)),
    "trace_metadata": str(META_PATH.relative_to(ROOT)),
    "trace_metadata_sha256_not_checked": True,
    "all_21_submitted_rows_preserved": True,
    "center_role": "CSV row 0 is the fixed visual reference center, excluded from curve samples.",
    "curve_sample_rows": "CSV rows 1–20, used without modification.",
    "fixed_center_crop_px": [float(center[0]), float(center[1])],
    "curve_parameterization": "x=cx+exp(a+b*theta)*cos(theta); y=cy+exp(a+b*theta)*sin(theta), with crop y increasing downward",
    "golden_definition": {
        "phi": PHI,
        "quarter_turn_growth_factor": PHI,
        "signed_slope_for_decreasing_unwrapped_angle": B_GOLDEN,
    },
    "metric": "For each trace sample, sample the shared bounded theta interval, refine every detected grid-local minimum of squared Euclidean distance, include both interval endpoints, and report RMS nearest-point distance in crop pixels.",
    "nearest_point_search": {
        "method": "dense uniform grid plus bounded refinement of every detected sampled local-minimum bracket; both interval endpoints included",
        "grid_size": 4097,
        "refinement_xatol_rad": 1e-10,
        "globality_note": "Numerical approximation, not a formal global-minimum guarantee; repeat at higher grid resolution to check convergence."
    },
    "theta_search_interval_rad": [theta_min, theta_max],
    "initial_log_polar_estimate": {"a": float(a0), "b": float(b0)},
    "optimizer": {
        "free_model": {"method": "Nelder-Mead", "success": bool(free_opt.success), "message": str(free_opt.message)},
        "golden_model": {"method": "bounded scalar minimization for a, b fixed", "success": bool(golden_opt.success)},
    },
    "models": models,
    "overlay": str(OVERLAY_PATH.relative_to(ROOT)),
    "report": str(REPORT_PATH.relative_to(ROOT)),
    "limitations": [
        "The manual trace is sparse and its points are not re-digitized or automatically adjusted.",
        "The center is fixed to the user's visual reference estimate, not fitted or independently validated as the mathematical center.",
        "Nearest-point distances use a finite-grid search with local-minimum refinement; this is not a formal global-minimum proof. Check convergence at higher grid resolutions and inspect per-point distances for endpoint effects.",
        "Only logarithmic spirals are compared; other curve families and trace perturbations remain untested.",
        "Fit quality does not establish symbolic intent.",
    ],
}
REPORT_PATH.write_text(json.dumps(result, indent=2) + "\n")
print(json.dumps({
    "status": result["status"],
    "overlay": str(OVERLAY_PATH),
    "report": str(REPORT_PATH),
    "fixed_center_crop_px": result["fixed_center_crop_px"],
    "models": {
        key: {
            "slope": value["log_radius_slope_b"],
            "quarter_turn_growth_factor": value["quarter_turn_growth_factor"],
            "orthogonal_distance_rms_px": value["orthogonal_distance_rms_px"],
            "orthogonal_distance_max_px": value["orthogonal_distance_max_px"],
        }
        for key, value in models.items()
    },
}, indent=2))
