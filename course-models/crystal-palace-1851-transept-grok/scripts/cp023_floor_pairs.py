"""Before/after pairs for the 2026-11-02 CP023 START floor-detail CANDIDATE (CANDIDATE only; no keep/revert call).
Before = live CP023 start (renders/candidates/cp023_boots_20261101: r11_envelope_v2, exp -0.9, dressing, --cp023-boots).
After  = renders/candidates/cp023_floor_20261102/full (r11_envelope_v2_cp023floor.blend, same settings).
Alt    = renders/candidates/cp023_floor_20261102/full_shift (same + --shift-y 0.035 reframe), if present.
Lower-detail pairs crop the bottom 30% (where the empty floor was)."""
import os
from PIL import Image, ImageDraw, ImageStat
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
A = os.path.join(ROOT, "renders/candidates/cp023_boots_20261101/CP023_into_nave_start.png")
B = os.path.join(ROOT, "renders/candidates/cp023_floor_20261102/full/CP023_into_nave_start.png")
C = os.path.join(ROOT, "renders/candidates/cp023_floor_20261102/full_shift/CP023_into_nave_start.png")
OUT = "/workspace/crystal-palace-survey/look/pairs_geo"
H = 720; GAP = 10

def sheet(ims, labels, path, scale=None):
    hh = H if scale is None else round(ims[0].height * scale)
    ims = [im.resize((round(im.width * hh / im.height), hh), Image.LANCZOS) for im in ims]
    s = Image.new("RGB", (ims[0].width + GAP + ims[1].width, hh), (255, 255, 255))
    s.paste(ims[0], (0, 0)); s.paste(ims[1], (ims[0].width + GAP, 0))
    d = ImageDraw.Draw(s)
    for x, t in ((6, labels[0]), (ims[0].width + GAP + 6, labels[1])):
        d.rectangle([x - 4, 4, x + 7 * len(t), 20], fill=(0, 0, 0)); d.text((x, 6), t, fill=(255, 255, 255))
    s.save(path); print(path)

def lum(im): return ImageStat.Stat(im.convert("L")).mean[0]
a = Image.open(A).convert("RGB")
for path, tag, name in ((B, "floor detail", "CANDIDATE_CP023_floor_start"), (C, "floor detail + shift_y 0.035", "CANDIDATE_CP023_floor_shift_start")):
    if not os.path.exists(path): print("missing", path); continue
    b = Image.open(path).convert("RGB")
    sheet([a, b], (f"LIVE CP023_into_nave_start (boots-only)  exp -0.9  luma {lum(a):.1f}",
                   f"CANDIDATE {tag}  exp -0.9  luma {lum(b):.1f}"), os.path.join(OUT, name + "_pair.png"))
    w, h = a.size
    crops = [im.crop((0, int(h * 0.70), w, h)) for im in (a, b)]
    sheet(crops, ("LIVE start lower 30%", f"CANDIDATE {tag} lower 30%"), os.path.join(OUT, name + "_lowerdetail_pair.png"), scale=1.0)
    print(name, "luma", round(lum(a), 1), "->", round(lum(b), 1))
