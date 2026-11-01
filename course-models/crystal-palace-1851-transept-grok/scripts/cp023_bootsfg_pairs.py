"""Before/after pairs for the 2026-11-01 CP023 boots + foreground pass (CANDIDATE only; no keep/revert).
Before = live CP023 (renders/candidates/cp023_dressing_20261101/full: r11_envelope_v2, exp -0.9, crowd dressing).
After  = renders/candidates/cp023_bootsfg_20261101/full (same blend/settings + --cp023-boots --cp023-foreground).
Also writes a lower-half detail pair per camera (bottom 45% of frame, for judging boots/floor)."""
import os
from PIL import Image, ImageDraw, ImageStat
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
A = os.path.join(ROOT, "renders/candidates/cp023_dressing_20261101/full")
B = os.path.join(ROOT, "renders/candidates/cp023_bootsfg_20261101/full")
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

for cam in ("CP023_into_nave_start", "CP023_into_nave_end"):
    ims = [Image.open(os.path.join(p, cam + ".png")).convert("RGB") for p in (A, B)]
    lum = [ImageStat.Stat(im.convert("L")).mean[0] for im in ims]
    sheet(ims, (f"LIVE {cam}  exp -0.9  luma {lum[0]:.1f}",
                f"CANDIDATE boots+foreground  exp -0.9  luma {lum[1]:.1f}"),
          os.path.join(OUT, f"CANDIDATE_CP023_boots_foreground_{cam}_pair.png"))
    w, h = ims[0].size
    crops = [im.crop((0, int(h * 0.55), w, h)) for im in ims]
    sheet(crops, (f"LIVE {cam} lower 45%", "CANDIDATE lower 45%"),
          os.path.join(OUT, f"CANDIDATE_CP023_boots_foreground_{cam}_lowerdetail_pair.png"))
    print(cam, "luma", round(lum[0], 1), "->", round(lum[1], 1))
