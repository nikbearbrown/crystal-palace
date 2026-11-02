#!/usr/bin/env bash
# CP032 arrival KEEP housekeeping (2026-11-02, MV16). After scripts/render_cp032_arrival_live.sh has written the live
# renders/m02/CP032_arrival_{start,end}.png from live rounds/m02.blend, this refreshes the derived files that still
# showed the boxy STAFF_07..11 stand-ins (pre-look 96-spp renders):
#   renders/m02/CP032_arrival_start.jpg, renders/m02/CP032_arrival_end.jpg   <- JPEG (q90) of the live PNGs
#   renders/m02_png/CP032_arrival_start.{png,jpg}                            <- copies of the live start frame
#   renders/m02/contact_sheet_m02.jpg   <- same layout as render_cp032_stale.sh (/workspace/tmp/sheet.py), JPEGs only
# No rendering here, so it is cheap and deterministic.   bash scripts/refresh_cp032_arrival_files.sh
set -euo pipefail
cd "$(dirname "$0")/.."
python3 - <<'PY'
import glob, os, shutil
from PIL import Image, ImageDraw
for t in ("start", "end"):
    im = Image.open("renders/m02/CP032_arrival_%s.png" % t).convert("RGB")
    im.save("renders/m02/CP032_arrival_%s.jpg" % t, quality=90)
shutil.copyfile("renders/m02/CP032_arrival_start.png", "renders/m02_png/CP032_arrival_start.png")
Image.open("renders/m02/CP032_arrival_start.png").convert("RGB").save("renders/m02_png/CP032_arrival_start.jpg", quality=90)
fs = sorted(f for f in glob.glob("renders/m02/*.jpg") if not os.path.basename(f).startswith("contact_sheet"))
W, H = 480, 270; c = 3; r = (len(fs) + c - 1) // c
s = Image.new("RGB", (c * W, r * (H + 18)), "white"); dr = ImageDraw.Draw(s)
for i, f in enumerate(fs):
    im = Image.open(f).convert("RGB"); im.thumbnail((W, H)); x, y = (i % c) * W, (i // c) * (H + 18)
    s.paste(im, (x, y + 18)); dr.text((x + 4, y + 3), os.path.basename(f), fill="black")
s.save("renders/m02/contact_sheet_m02.jpg", quality=85)
print("SHEET", len(fs), "frames")
PY
echo "done: CP032_arrival_{start,end}.jpg, m02_png arrival start, contact_sheet_m02.jpg"
