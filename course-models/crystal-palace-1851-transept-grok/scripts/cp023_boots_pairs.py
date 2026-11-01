"""Before/after pair for the 2026-11-01 CP023 boots-only START candidate (CANDIDATE only; no keep/revert).
Before = live CP023 start (renders/candidates/cp023_dressing_20261101/full: r11_envelope_v2, exp -0.9, crowd dressing).
After  = renders/candidates/cp023_boots_20261101 (same blend/settings + --cp023-boots, no --cp023-foreground).
Also writes a lower-45% detail pair for judging boots."""
import os
from PIL import Image, ImageDraw, ImageStat
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
A = os.path.join(ROOT, "renders/candidates/cp023_dressing_20261101/full/CP023_into_nave_start.png")
B = os.path.join(ROOT, "renders/candidates/cp023_boots_20261101/CP023_into_nave_start.png")
OUT = "/workspace/crystal-palace-survey/look/pairs_geo"
H = 720; GAP = 10

def sheet(ims, labels, path):
    ims = [im.resize((round(im.width * H / im.height), H), Image.LANCZOS) for im in ims]
    s = Image.new("RGB", (ims[0].width + GAP + ims[1].width, H), (255, 255, 255))
    s.paste(ims[0], (0, 0)); s.paste(ims[1], (ims[0].width + GAP, 0))
    d = ImageDraw.Draw(s)
    for x, t in ((6, labels[0]), (ims[0].width + GAP + 6, labels[1])):
        d.rectangle([x - 4, 4, x + 7 * len(t), 20], fill=(0, 0, 0)); d.text((x, 6), t, fill=(255, 255, 255))
    s.save(path); print(path)

ims = [Image.open(p).convert("RGB") for p in (A, B)]
lum = [ImageStat.Stat(im.convert("L")).mean[0] for im in ims]
sheet(ims, (f"LIVE CP023_into_nave_start  exp -0.9  luma {lum[0]:.1f}",
            f"CANDIDATE boots only  exp -0.9  luma {lum[1]:.1f}"),
      os.path.join(OUT, "CANDIDATE_CP023_bootsonly_start_pair.png"))
w, h = ims[0].size
crops = [im.crop((0, int(h * 0.55), w, h)) for im in ims]
sheet(crops, ("LIVE start lower 45%", "CANDIDATE boots only lower 45%"),
      os.path.join(OUT, "CANDIDATE_CP023_bootsonly_start_lowerdetail_pair.png"))
print("luma", round(lum[0], 1), "->", round(lum[1], 1))
