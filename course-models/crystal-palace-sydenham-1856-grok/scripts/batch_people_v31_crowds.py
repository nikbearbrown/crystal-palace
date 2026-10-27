#!/usr/bin/env python3
"""Adopt people v3.1 into Sydenham (+football) crowd shots; keep-better before/after."""
from __future__ import annotations
import json, os, shutil, subprocess, sys
from pathlib import Path
from collections import OrderedDict

BLENDER = "/workspace/blender5/blender"
SY = Path("/workspace/crystal-palace-sydenham/course-models/crystal-palace-sydenham-1856-grok")
FB = Path("/workspace/crystal-palace-football/course-models/crystal-palace-football-1895-grok")
OUT_SY = SY / "people_v31"
OUT_FB = FB / "people_v31"
for d in (OUT_SY / "before", OUT_SY / "after", OUT_SY / "previews",
          OUT_FB / "before", OUT_FB / "after", OUT_FB / "previews"):
    d.mkdir(parents=True, exist_ok=True)

# (cp, era, root, blend, cam, before_png, tag, hero_dest_rel)
SHOTS = [
    ("CP035", "1850s", SY, "rounds/sydenham-open54-r16.blend",
     "CAM_CP035_transept_gallery_28mm",
     "renders/r16/r16_CAM_CP035_transept_gallery_28mm.png",
     "v31", "renders/r16/r16_CAM_CP035_transept_gallery_28mm.png"),
    ("CP036", "1850s", SY, "rounds/sydenham-open54-r16.blend",
     "CAM_CP036_covered_way_28mm",
     "renders/r14_open54_CAM_CP036_covered_way_28mm.png",
     "v31", "renders/r14_open54_CAM_CP036_covered_way_28mm.png"),
    ("CP037", "1850s", SY, "rounds/sydenham-1856-r16.blend",
     "CAM_CP037_taller_nave_28mm",
     "renders/r16/r16_CAM_CP037_taller_nave_28mm.png",
     "v31", "renders/r16/r16_CAM_CP037_taller_nave_28mm.png"),
    ("CP044", "1850s", SY, "rounds/sydenham-1856-r16.blend",
     "CAM_CP044_pay_desks_35mm",
     "renders/r16/r16_CAM_CP044_pay_desks_35mm.png",
     "v31", "renders/r16/r16_CAM_CP044_pay_desks_35mm.png"),
    ("CP045", "1850s", SY, "rounds/sydenham-concert57-r14.blend",
     "CAM_CP045_gallery_wide_b_28mm",
     "renders/r13_concert57_CAM_CP045_gallery_wide_b_28mm.png",
     "v31", "renders/r13_concert57_CAM_CP045_gallery_wide_b_28mm.png"),
    ("CP049", "1910s", SY, "rounds/sydenham-late11-r16.blend",
     "CAM_CP049_worn_garden_front_35mm",
     "renders/r16/r16_CAM_CP049_worn_garden_front_35mm.png",
     "v31", "renders/r16/r16_CAM_CP049_worn_garden_front_35mm.png"),
    ("CP051", "1910s", SY, "rounds/sydenham-late11-r16.blend",
     "CAM_CP051_electric_nave_28mm",
     "renders/r16/r16_CAM_CP051_electric_nave_28mm.png",
     "v31", "renders/r16/r16_CAM_CP051_electric_nave_28mm.png"),
    ("CP054", "1910s", SY, "rounds/sydenham-late11-r16.blend",
     "CAM_CP054_plymouth_rescue_35mm",
     "renders/r16/r16_CAM_CP054_plymouth_rescue_35mm.png",
     "v31", "renders/r16/r16_CAM_CP054_plymouth_rescue_35mm.png"),
    ("CP058", "1930s", SY, "rounds/sydenham-1936after-r17.blend",
     "CAM_CP058_parade_appliances_35mm",
     "renders/r17i_after_CAM_CP058_parade_appliances_35mm.png",
     "v31", "renders/r17i_after_CAM_CP058_parade_appliances_35mm.png"),
    ("CP060", "1930s", SY, "rounds/sydenham-1936after-r17.blend",
     "CAM_CP060_crowd_watching_35mm",
     "renders/r12_1936_CAM_CP060_crowd_watching_35mm.png",
     "v31", "renders/r12_1936_CAM_CP060_crowd_watching_35mm.png"),
    ("CP050", "1890s", FB, "rounds/fb02_1895.blend",
     "CP050_bank_1895_start",
     "renders/fb02_1895/CP050_bank_1895_start.png",
     "v31", "renders/fb02_1895/CP050_bank_1895_start.png"),
    ("CP055", "1910s", FB, "rounds/fb02.blend",
     "CP055_bank_1913_start",
     "renders/fb02/CP055_bank_1913_start.png",
     "v31", "renders/fb02/CP055_bank_1913_start.png"),
]

def make_pair(before: Path, after: Path, dest: Path):
    from PIL import Image, ImageDraw
    if not before.exists() or not after.exists():
        return False
    a = Image.open(before).convert("RGB")
    b = Image.open(after).convert("RGB")
    h = max(a.height, b.height)
    def fit(im):
        r = h / im.height
        return im.resize((int(im.width * r), h), Image.Resampling.LANCZOS)
    a, b = fit(a), fit(b)
    gap = 8
    canvas = Image.new("RGB", (a.width + b.width + gap, h + 28), (30, 30, 30))
    canvas.paste(a, (0, 28)); canvas.paste(b, (a.width + gap, 28))
    dr = ImageDraw.Draw(canvas)
    dr.text((8, 6), "BEFORE (lathe)", fill=(220, 220, 220))
    dr.text((a.width + gap + 8, 6), "AFTER (people v3.1)", fill=(220, 220, 220))
    dest.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(dest, quality=90)
    return True

def main():
    only = set(sys.argv[1:]) if len(sys.argv) > 1 else None
    shots = [s for s in SHOTS if (not only or s[0] in only)]
    # freeze befores
    meta = {}
    for cp, era, root, blend_rel, cam, before_rel, tag, dest_rel in shots:
        out_root = OUT_SY if root == SY else OUT_FB
        before_src = root / before_rel
        bdest = out_root / "before" / f"{cp}__{Path(before_rel).name}"
        if before_src.exists():
            shutil.copy2(before_src, bdest)
        meta[cp] = dict(era=era, root=root, blend=root/blend_rel, cam=cam,
                        before=bdest, dest_rel=dest_rel, tag=tag,
                        after=out_root/"after"/f"{cp}__{Path(dest_rel).name}",
                        pair=out_root/"previews"/f"{cp}_v31_before_after.jpg",
                        hero=root/dest_rel)

    # group by (root, blend, era)
    groups = OrderedDict()
    for s in shots:
        cp, era, root, blend_rel, cam, *_ = s
        key = (str(root), blend_rel, era)
        groups.setdefault(key, []).append(cp)

    log = []
    for (root_s, blend_rel, era), cps in groups.items():
        root = Path(root_s)
        blend = root / blend_rel
        cams = [meta[cp]["cam"] for cp in cps]
        render_dir = (OUT_SY if root == SY else OUT_FB) / "after" / f"_grp_{cps[0]}"
        render_dir.mkdir(parents=True, exist_ok=True)
        seed = sum(int(cp[2:]) for cp in cps)
        print(f"\n=== GROUP {cps} era={era} blend={blend.name} ===", flush=True)
        if root == SY:
            env = os.environ.copy()
            env["PEOPLE_ERA"] = era
            env["PEOPLE_SEED"] = str(seed)
            env["RES"] = "1280x720"
            env["THREADS"] = "8"
            cmd = [BLENDER, "-b", str(blend), "-P", str(SY / "scripts/render.py"), "--",
                   str(render_dir), "v31", "100", "28", *cams]
            print("CMD", " ".join(cmd), flush=True)
            rc = subprocess.run(cmd, cwd=str(SY), env=env).returncode
            for cp in cps:
                wrote = render_dir / f"v31_{meta[cp]['cam']}.png"
                ok = rc == 0 and wrote.exists()
                if ok:
                    shutil.copy2(wrote, meta[cp]["after"])
                    shutil.copy2(wrote, meta[cp]["hero"])
                    make_pair(meta[cp]["before"], meta[cp]["after"], meta[cp]["pair"])
                log.append({"cp": cp, "era": era, "ok": ok,
                            "verdict": "pending_visual" if ok else "fail",
                            "before": str(meta[cp]["before"]),
                            "after": str(meta[cp]["after"]),
                            "pair": str(meta[cp]["pair"]),
                            "hero": str(meta[cp]["hero"]),
                            "cam": meta[cp]["cam"], "blend": blend_rel})
                print("RESULT", cp, ok, flush=True)
        else:
            cmd = [BLENDER, "-b", str(blend), "-P", str(FB / "scripts/render_views.py"), "--",
                   "--cams", ",".join(cams), "--outdir", str(render_dir),
                   "--res", "1280x720", "--samples", "28", "--threads", "8",
                   "--era", era, "--seed", str(seed)]
            print("CMD", " ".join(cmd), flush=True)
            rc = subprocess.run(cmd, cwd=str(FB)).returncode
            for cp in cps:
                wrote = render_dir / f"{meta[cp]['cam']}.png"
                ok = rc == 0 and wrote.exists()
                if ok:
                    shutil.copy2(wrote, meta[cp]["after"])
                    shutil.copy2(wrote, meta[cp]["hero"])
                    make_pair(meta[cp]["before"], meta[cp]["after"], meta[cp]["pair"])
                log.append({"cp": cp, "era": era, "ok": ok,
                            "verdict": "pending_visual" if ok else "fail",
                            "before": str(meta[cp]["before"]),
                            "after": str(meta[cp]["after"]),
                            "pair": str(meta[cp]["pair"]),
                            "hero": str(meta[cp]["hero"]),
                            "cam": meta[cp]["cam"], "blend": blend_rel})
                print("RESULT", cp, ok, flush=True)

    (OUT_SY / "verdicts_v31_crowds.json").write_text(json.dumps(log, indent=2))
    print("DONE groups", len(groups), "shots", len(log), flush=True)

if __name__ == "__main__":
    main()
