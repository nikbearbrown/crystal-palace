#!/usr/bin/env bash
# CP032 housekeeping (2026-11-02): refresh the m02 files that still showed the boxy STAFF_* stand-ins after the
# departure-hands KEEP (MV15, move 8bfed03). Everything comes from live rounds/m02.blend, same settings as the live
# start frame (render_shots.py, 1920x1080, 24 spp, look exposure):
#   renders/m02/CP032_departure_end.jpg      <- fresh render of camera CP032_departure_end (own Blender session)
#   renders/m02/CP032_departure_start.jpg    <- JPEG of the live renders/m02/CP032_departure_start.png
#   renders/m02_png/CP032_departure_start.{png,jpg} <- copies of the live start frame
#   renders/m02/contact_sheet_m02.jpg        <- /workspace/tmp/sheet.py layout over the m02 JPEGs only (the live .png is
#                                               skipped so the start frame isn't shown twice)
# Note: render CP032_departure_end in its OWN session. Rendering it after CP032_departure_start in one session gives a
# different (still valid) people swap; the single-camera session is deterministic (checked twice, pixel-identical).
#   bash scripts/render_cp032_stale.sh
set -euo pipefail
cd "$(dirname "$0")/.."
B=/workspace/blender5/blender
TMP=$(mktemp -d)
"$B" -b rounds/m02.blend -P scripts/render_shots.py -- --out "$TMP" --cams CP032_departure_end --samples 24 --pct 100 \
  2>&1 | grep -E "PEOPLE|RENDERED|Error" || true
python3 - "$TMP" <<'PY'
import sys, glob, os, shutil
from PIL import Image, ImageDraw
tmp = sys.argv[1]
Image.open(os.path.join(tmp, "CP032_departure_end.png")).convert("RGB").save("renders/m02/CP032_departure_end.jpg", quality=90)
live = Image.open("renders/m02/CP032_departure_start.png").convert("RGB")
live.save("renders/m02/CP032_departure_start.jpg", quality=90)
shutil.copyfile("renders/m02/CP032_departure_start.png", "renders/m02_png/CP032_departure_start.png")
live.save("renders/m02_png/CP032_departure_start.jpg", quality=90)
# contact sheet: same layout as /workspace/tmp/sheet.py, JPEGs only
fs = sorted(f for f in glob.glob("renders/m02/*.jpg") if not os.path.basename(f).startswith("contact_sheet"))
W, H = 480, 270; c = 3; r = (len(fs) + c - 1) // c
s = Image.new("RGB", (c * W, r * (H + 18)), "white"); dr = ImageDraw.Draw(s)
for i, f in enumerate(fs):
    im = Image.open(f).convert("RGB"); im.thumbnail((W, H)); x, y = (i % c) * W, (i // c) * (H + 18)
    s.paste(im, (x, y + 18)); dr.text((x + 4, y + 3), os.path.basename(f), fill="black")
s.save("renders/m02/contact_sheet_m02.jpg", quality=85)
print("SHEET", len(fs), "frames")
PY
rm -rf "$TMP"
echo "done: CP032_departure_end.jpg, CP032_departure_start.jpg, m02_png start, contact_sheet_m02.jpg"
