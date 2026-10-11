#!/usr/bin/env python3
"""Audit the submitted page-57 trace against the committed crop.

Writes a numbered overlay and point-by-point diagnostics. Does not alter trace data.
"""
from pathlib import Path
import csv, json, hashlib
import numpy as np
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data/raw/page57-spiral"
IMAGE = DATA / "page57_spiral_working.png"
CSV_PATH = DATA / "trace_points_working.csv"
META_PATH = DATA / "trace_points_working.json"
OVERLAY = DATA / "trace_audit_overlay.png"
REPORT = DATA / "trace_audit_working.json"

im = Image.open(IMAGE).convert("RGB")
image_hash = hashlib.sha256(IMAGE.read_bytes()).hexdigest()
meta = json.loads(META_PATH.read_text())
if image_hash != meta.get("image_sha256"):
    raise SystemExit(f"Trace/crop hash mismatch: crop={image_hash}, trace metadata={meta.get('image_sha256')}")

with CSV_PATH.open(newline="") as f:
    rows = list(csv.DictReader(f))
pts = np.array([[float(r["x_crop_px"]), float(r["y_crop_px"])] for r in rows])
if len(pts) < 3:
    raise SystemExit("Need at least 3 points for a trace audit")

# Use current free-fit center as a diagnostic reference only, not as ground truth.
center = np.array([189.72675681356674, 136.20090508108225])
delta = pts - center
r = np.hypot(delta[:, 0], delta[:, 1])
theta = np.arctan2(delta[:, 1], delta[:, 0])
inc = np.arctan2(np.sin(np.diff(theta)), np.cos(np.diff(theta)))
step = np.linalg.norm(np.diff(pts, axis=0), axis=1)

draw = ImageDraw.Draw(im)
try:
    font = ImageFont.truetype("DejaVuSans.ttf", 12)
except OSError:
    font = ImageFont.load_default()
for i in range(len(pts)-1):
    draw.line((tuple(pts[i]), tuple(pts[i+1])), fill=(255, 40, 40), width=1)
for i, (x, y) in enumerate(pts):
    rad = 3
    draw.ellipse((x-rad, y-rad, x+rad, y+rad), fill=(0, 220, 255), outline=(0,0,0), width=1)
    draw.text((x+4, y-10), str(i), fill=(255, 255, 0), font=font, stroke_width=1, stroke_fill=(0,0,0))
cx, cy = center
draw.ellipse((cx-4, cy-4, cx+4, cy+4), fill=(255, 0, 255), outline=(255,255,255), width=1)
draw.text((cx+5, cy+4), "reference center (not ground truth)", fill=(255,0,255), font=font, stroke_width=1, stroke_fill=(0,0,0))
im.save(OVERLAY)

records = []
for i, p in enumerate(pts):
    rec = {
        "point_index": i,
        "x_crop_px": float(p[0]), "y_crop_px": float(p[1]),
        "radius_from_reference_center_px": float(r[i]),
    }
    if i > 0:
        rec["segment_length_from_previous_px"] = float(step[i-1])
        rec["signed_shortest_angular_step_from_previous_deg"] = float(np.degrees(inc[i-1]))
        rec["radial_change_from_previous_px"] = float(r[i]-r[i-1])
    records.append(rec)

result = {
    "status": "trace audit only; no points modified",
    "crop": str(IMAGE.relative_to(ROOT)),
    "crop_sha256": image_hash,
    "trace_csv": str(CSV_PATH.relative_to(ROOT)),
    "trace_metadata_direction": meta.get("direction"),
    "point_count": len(pts),
    "reference_center_crop_px": center.tolist(),
    "reference_center_note": "Borrowed from prior exploratory fit only to expose suspicious jumps; not a validated spiral center.",
    "overlay": str(OVERLAY.relative_to(ROOT)),
    "points": records,
    "flags": [
        {"type": "near-180-degree angular step", "between_point_indices": [int(i), int(i+1)], "degrees": float(np.degrees(inc[i]))}
        for i in range(len(inc)) if abs(np.degrees(inc[i])) >= 150
    ],
    "limitations": [
        "Polar diagnostics depend on the reference center.",
        "A large angular step can be caused by a poor center when points are near it, not necessarily by a bad trace.",
        "The overlay is intended for visual review; no point is automatically removed or reordered."
    ]
}
REPORT.write_text(json.dumps(result, indent=2) + "\n")
print(json.dumps({"status": result["status"], "overlay": str(OVERLAY), "report": str(REPORT), "point_count": len(pts), "flags": result["flags"]}, indent=2))
