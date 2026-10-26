"""Shared helpers for the Crystal Palace plate measurements.

All scripts read the working JPEGs of Downes's 1852 plates (see PLATE-INDEX.md) and print what
they measured, in pixels and in feet, next to the figure the text or the plate states. Nothing here
touches a model. Run each script with `python3 -I`.

Honest limits: windows and seeds (where on the sheet to look) were chosen by looking at the plate,
so they are specific to this scan. The scripts report every candidate they find inside a window, not
just the one they pick, so a reader can see where the choice is ambiguous.
"""
from pathlib import Path

import numpy as np
from PIL import Image

Image.MAX_IMAGE_PIXELS = None

PLATES = Path(__file__).resolve().parents[2] / "source-scans" / "plates"


def load_gray(name):
    """Load plates/<name> as a float grayscale array. `name` is e.g. 'plate-006.jpg'."""
    return np.asarray(Image.open(PLATES / name).convert("L"), dtype=float)


def groups(idx, gap):
    """Group sorted integer positions into runs whose neighbours are at most `gap` apart.
    Returns a list of lists."""
    idx = list(idx)
    if not idx:
        return []
    out, cur = [], [idx[0]]
    for v in idx[1:]:
        if v - cur[-1] <= gap:
            cur.append(v)
        else:
            out.append(cur)
            cur = [v]
    out.append(cur)
    return out


def centres(idx, gap):
    """Centre and width of each run of positions. Returns [(centre, width), ...]."""
    return [(float(np.mean(g)), len(g)) for g in groups(idx, gap)]


def dark_cols(a, y0, y1, x0, x1, thr, frac, gap=6):
    """Vertical dark lines: columns whose dark-pixel fraction over rows y0:y1 exceeds `frac`.
    Dark means below (median of the window - thr)."""
    b = a[y0:y1, x0:x1]
    c = (b < np.median(b) - thr).sum(axis=0) / b.shape[0]
    xs = np.where(c > frac)[0] + x0
    return centres(xs, gap)


def dark_rows(a, y0, y1, x0, x1, thr, frac, gap=3):
    """Horizontal dark lines: rows whose dark-pixel fraction over columns x0:x1 exceeds `frac`."""
    b = a[y0:y1, x0:x1]
    r = (b < np.median(b) - thr).sum(axis=1) / b.shape[1]
    ys = np.where(r > frac)[0] + y0
    return centres(ys, gap)


def ticks(a, y0, y1, x0, x1, thr=25, minc=6, gap=3):
    """Scale-bar tick marks: narrow dark columns in a short band just above a bar."""
    b = a[y0:y1, x0:x1]
    c = (b < np.median(b) - thr).sum(axis=0)
    xs = np.where(c >= minc)[0] + x0
    return [m for m, _ in centres(xs, gap)]


def fit_scale(tick_x, step_ft, first_ft):
    """Least-squares px/ft from evenly spaced ticks; also the per-step spread.
    Returns (px_per_ft, (min, max) of the individual per-step px/ft)."""
    tick_x = np.asarray(tick_x, float)
    ft = first_ft + step_ft * np.arange(len(tick_x))
    slope = np.polyfit(ft, tick_x, 1)[0]
    gaps = np.diff(tick_x) / step_ft
    return float(slope), (float(gaps.min()), float(gaps.max()))


def pct(measured, stated):
    return 100.0 * (measured - stated) / stated
