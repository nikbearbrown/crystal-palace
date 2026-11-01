"""Before/after pair JPGs for the 2026-11-01 envelope full-camera check (CANDIDATE only; no keep/revert)."""
import os, re, sys
from PIL import Image, ImageDraw
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = os.path.join(ROOT, "renders/candidates/envelope_check_20261101")
OUT = "/workspace/crystal-palace-survey/look/pairs_geo"
SHOT = {"CP023_into_nave_start": -2.2, "CP023_into_nave_end": -2.2}
H = 540; GAP = 10
for f in sorted(os.listdir(os.path.join(D, "candidate"))):
    cam = f[:-4]; a = os.path.join(D, "live", f); b = os.path.join(D, "candidate", f)
    if not os.path.exists(a): print("MISSING live", f); continue
    m = re.match(r"(CP\d{3})_", cam); cp = m.group(1) if m else "REVIEW"
    ims = [Image.open(p).convert("RGB") for p in (a, b)]
    ims = [im.resize((round(im.width * H / im.height), H), Image.LANCZOS) for im in ims]
    W = ims[0].width + GAP + ims[1].width
    sheet = Image.new("RGB", (W, H), (255, 255, 255)); sheet.paste(ims[0], (0, 0)); sheet.paste(ims[1], (ims[0].width + GAP, 0))
    d = ImageDraw.Draw(sheet)
    exp = f"exp {SHOT[cam]:+.1f} (per-shot)" if cam in SHOT else "look exp"
    for x, t in ((6, f"LIVE r11  {cam}"), (ims[0].width + GAP + 6, f"CANDIDATE r11_envelope  {exp}")):
        d.rectangle([x - 4, 4, x + 7 * len(t), 20], fill=(0, 0, 0)); d.text((x, 6), t, fill=(255, 255, 255))
    p = os.path.join(OUT, f"CANDIDATE_{cp}_transept_envelope_{cam}_pair.jpg"); sheet.save(p, quality=90); print(p)
