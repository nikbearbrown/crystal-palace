#!/usr/bin/env python3
"""Assemble CP002 CANDIDATE before/after pairs (matched exposure: same blend lighting + same render recipe both sides).
usage: make_cp002_pairs.py <before_dir> <after_dir> <out_dir>
Hero 'before' = the LIVE renders/ln02/CP002_lane_start.png (byte copy). Side-effect 'before' = ln02 re-rendered with the
identical recipe (the live factory/terrace PNGs predate the material pass, so they are not like-for-like)."""
import sys, shutil, json, hashlib
from pathlib import Path
from PIL import Image, ImageDraw, ImageStat, ImageChops
ROOT = Path(__file__).resolve().parent.parent
bdir, adir, out = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3]); out.mkdir(parents=True, exist_ok=True)
SHOTS = [("CP002_lane_start", "CANDIDATE_CP002_lane", "hero"),
         ("CP002_terrace_start", "CANDIDATE_CP002_sidefx_terrace", "side effect"),
         ("CP002_factory_start", "CANDIDATE_CP002_sidefx_factory", "side effect"),
         ("CP005_room_start", "CANDIDATE_CP002_sidefx_CP005_room", "side effect (check)"),
         ("CP005_table_start", "CANDIDATE_CP002_sidefx_CP005_table", "side effect (check)")]
def md5(p): return hashlib.md5(open(p, "rb").read()).hexdigest()
rows = []
for cam, stem, kind in SHOTS:
    b = ROOT / "renders/ln02" / f"{cam}.png" if kind == "hero" else bdir / f"{cam}.png"
    a = adir / f"{cam}.png"
    bo, ao = out / f"{stem}_before.png", out / f"{stem}_after.png"
    shutil.copy2(b, bo); shutil.copy2(a, ao)
    A, B = Image.open(bo).convert("RGB"), Image.open(ao).convert("RGB")
    lb, la = ImageStat.Stat(A.convert("L")).mean[0], ImageStat.Stat(B.convert("L")).mean[0]
    diff = sum(ImageStat.Stat(ImageChops.difference(A, B)).mean) / 3
    W, H = A.size; gap = 10; top = 34
    cv = Image.new("RGB", (W * 2 + gap, H + top), (24, 24, 24)); cv.paste(A, (0, top)); cv.paste(B, (W + gap, top))
    d = ImageDraw.Draw(cv)
    d.text((10, 10), f"BEFORE (live ln02) {cam}  luma {lb:.1f}", fill=(230, 230, 230))
    d.text((W + gap + 10, 10), f"AFTER CANDIDATE ln03_cp002 {cam}  luma {la:.1f}  exposure -0.10 both", fill=(255, 210, 120))
    pj = out / f"{stem}_pair.jpg"; cv.save(pj, quality=90)
    rows.append(dict(cam=cam, kind=kind, before=bo.name, after=ao.name, pair=pj.name, luma_before=round(lb, 2), luma_after=round(la, 2),
                     mean_abs_diff=round(diff, 2), before_src=str(b.relative_to(ROOT) if b.is_relative_to(ROOT) else b), md5_before=md5(bo), md5_after=md5(ao)))
json.dump(rows, open(out / "pairs.json", "w"), indent=1)
for r in rows: print(r)
