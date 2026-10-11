#!/usr/bin/env python3
"""Manually trace the page-57 spiral centerline without modifying the source crop.

Run from the archive root:
  .wf-venv/bin/python scripts/trace_page57_spiral.py

Click points along the centerline of the dominant loop in order, from the outer
loop near the stem junction toward the inner terminal. Do not trace the stem.
Press Enter to save; Backspace removes the last point; Escape cancels.
Coordinates are crop-local pixel coordinates with origin at top-left.
"""
from pathlib import Path
import csv
import json
import hashlib
import sys

import matplotlib.pyplot as plt
import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
IMAGE = ROOT / "data/raw/page57-spiral/page57_spiral_working.png"
OUT_CSV = ROOT / "data/raw/page57-spiral/trace_points_working.csv"
OUT_JSON = ROOT / "data/raw/page57-spiral/trace_points_working.json"

if not IMAGE.exists():
    sys.exit(f"Missing crop: {IMAGE}")

raw = IMAGE.read_bytes()
img = Image.open(IMAGE).convert("RGB")
arr = np.asarray(img)
fig, ax = plt.subplots(figsize=(11, 8))
ax.imshow(arr, origin="upper", interpolation="nearest")
ax.set_title(
    "Click loop centerline in order: outer loop → inner terminal\n"
    "Enter=save | Backspace=undo | Esc=cancel"
)
ax.set_xlabel("crop x (pixels)")
ax.set_ylabel("crop y (pixels)")
points = []
line, = ax.plot([], [], "r.-", linewidth=1.2, markersize=4)
status = ax.text(
    0.02, 0.02, "0 points",
    transform=ax.transAxes, color="red",
    bbox={"facecolor": "white", "alpha": 0.8, "edgecolor": "none"}
)
finished = {"save": False}

def redraw():
    if points:
        xs, ys = zip(*points)
        line.set_data(xs, ys)
    else:
        line.set_data([], [])
    status.set_text(f"{len(points)} points")
    fig.canvas.draw_idle()

def on_click(event):
    if event.inaxes != ax or event.xdata is None or event.ydata is None:
        return
    points.append((float(event.xdata), float(event.ydata)))
    redraw()

def on_key(event):
    if event.key in ("backspace", "delete"):
        if points:
            points.pop()
        redraw()
    elif event.key in ("enter", "return"):
        if len(points) < 8:
            status.set_text(f"{len(points)} points — add at least 8 before saving")
            fig.canvas.draw_idle()
            return
        finished["save"] = True
        plt.close(fig)
    elif event.key == "escape":
        plt.close(fig)

fig.canvas.mpl_connect("button_press_event", on_click)
fig.canvas.mpl_connect("key_press_event", on_key)
plt.tight_layout()
plt.show()

if not finished["save"]:
    print("Cancelled; no output written.")
    sys.exit(0)

with OUT_CSV.open("w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["point_index", "x_crop_px", "y_crop_px"])
    for i, (x, y) in enumerate(points):
        writer.writerow([i, f"{x:.3f}", f"{y:.3f}"])

metadata = {
    "image": str(IMAGE.relative_to(ROOT)),
    "image_sha256": hashlib.sha256(raw).hexdigest(),
    "image_size_px": list(img.size),
    "coordinate_system": "crop-local pixels; origin top-left; x rightward; y downward",
    "trace_definition": "manual centerline trace of dominant spiral loop only; stem excluded",
    "direction": "outer loop toward inner terminal",
    "point_count": len(points),
    "points_csv": str(OUT_CSV.relative_to(ROOT)),
    "method": "interactive manual clicks; no smoothing or interpolation applied",
}
OUT_JSON.write_text(json.dumps(metadata, indent=2) + "\n")
print(f"Saved {len(points)} points to {OUT_CSV}")
print(f"Saved trace metadata to {OUT_JSON}")
