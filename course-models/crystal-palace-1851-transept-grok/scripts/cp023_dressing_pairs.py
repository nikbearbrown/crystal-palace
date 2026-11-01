"""Before/after pairs for the 2026-11-01 CP023 crowd dressing (CANDIDATE only; no keep/revert).
Before = live CP023 (renders/r11_envelope_v2/cp023_full, -0.9, gate off, no dressing).
After  = renders/candidates/cp023_dressing_20261101/full (same blend/settings, dressing on)."""
import os
from PIL import Image, ImageDraw, ImageStat
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
A = os.path.join(ROOT, "renders/r11_envelope_v2/cp023_full")
B = os.path.join(ROOT, "renders/candidates/cp023_dressing_20261101/full")
OUT = "/workspace/crystal-palace-survey/look/pairs_geo"
H = 720; GAP = 10
for cam in ("CP023_into_nave_start", "CP023_into_nave_end"):
    a, b = os.path.join(A, cam + ".png"), os.path.join(B, cam + ".png")
    ims = [Image.open(p).convert("RGB") for p in (a, b)]
    lum = [ImageStat.Stat(im.convert("L")).mean[0] for im in ims]
    ims = [im.resize((round(im.width * H / im.height), H), Image.LANCZOS) for im in ims]
    sheet = Image.new("RGB", (ims[0].width + GAP + ims[1].width, H), (255, 255, 255))
    sheet.paste(ims[0], (0, 0)); sheet.paste(ims[1], (ims[0].width + GAP, 0))
    d = ImageDraw.Draw(sheet)
    for x, t in ((6, f"LIVE r11_envelope_v2  {cam}  exp -0.9  no dressing  luma {lum[0]:.1f}"),
                 (ims[0].width + GAP + 6, f"CANDIDATE crowd dressing  exp -0.9  luma {lum[1]:.1f}")):
        d.rectangle([x - 4, 4, x + 7 * len(t), 20], fill=(0, 0, 0)); d.text((x, 6), t, fill=(255, 255, 255))
    p = os.path.join(OUT, f"CANDIDATE_CP023_crowd_dressing_{cam}_pair.jpg"); sheet.save(p, quality=90)
    print(p, "luma", round(lum[0], 1), "->", round(lum[1], 1))
