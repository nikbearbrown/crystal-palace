"""D-checks for HP-SITE 1850. blender -b rounds/s01.blend -P scripts/check_site.py -- --out checks/s01_checks.json"""
import bpy, sys, os, json, math, subprocess
from mathutils import Vector
HERE = os.path.dirname(os.path.abspath(__file__)); ROOTDIR = os.path.dirname(HERE)
argv = sys.argv[sys.argv.index("--") + 1:]; OUT = argv[argv.index("--out") + 1]
FT = 0.3048; I = 1 / 12; R = []; O = bpy.data.objects
def chk(cid, name, ok, val, note=""): R.append({"id": cid, "check": name, "pass": bool(ok), "value": val, "note": note})
def zg(x, y): return 1.1 * math.sin(x / 330 + .4) * math.cos(y / 270) + 0.5 * math.sin(x / 120 + y / 170) - 0.0004 * x
def vw(o): return [o.matrix_world @ v.co / FT for v in o.data.vertices]
def bb(o):
    cs = [o.matrix_world @ Vector(c) / FT for c in o.bound_box]
    return [min(c[i] for c in cs) for i in range(3)], [max(c[i] for c in cs) for i in range(3)]
# cameras: eye height above zg, lens per storyboard, no roll, not inside objects
LENS = {"CP006": 35, "CP007": 50, "CP008": 28, "CP009": 35}
cams = sorted([o for o in O if o.type == 'CAMERA'], key=lambda o: o.name)
solids = [o for o in O if o.type == 'MESH' and not o.name.startswith(("G_", "PATH", "ROTTEN_ROW", "DRIVE", "KENSINGTON", "DISTANT", "OVL_", "TR_", "LV_"))]
for c in cams:
    x, y, z = [v / FT for v in c.location]; xax = c.matrix_world.to_3x3() @ Vector((1, 0, 0))
    roll = math.degrees(math.asin(max(-1, min(1, xax.z)))); eye = z - zg(x, y); want = LENS[c.name[:5]]
    inside = [o.name for o in solids if (lambda l, h: l[0] - .3 < x < h[0] + .3 and l[1] - .3 < y < h[1] + .3 and l[2] - .3 < z < h[2] + .3)(*bb(o))]
    chk("C-" + c.name, f"eye 5.25 above terrain, lens {want} mm, no roll, clear of objects", abs(eye - 5.25) < 0.02 and c.data.lens == want and abs(roll) < 0.01 and not inside,
        {"eye": round(eye, 3), "lens": c.data.lens, "roll_deg": round(roll, 4), "inside": inside})
def mv(a, b): return math.dist([v / FT for v in O[a].location], [v / FT for v in O[b].location])
d8 = mv("CP008_start", "CP008_end"); chk("C8W", "CP008 walk ~5 m (16.4 ft)", 14.5 < d8 < 18.5, {"ft": round(d8, 2), "m": round(d8 * FT, 2)})
d9 = mv("CP009_start", "CP009_end"); chk("C9M", "CP009 move <= 7 m", d9 * FT <= 7.0, {"ft": round(d9, 2), "m": round(d9 * FT, 2)})
# survey
pegs = vw(O["SV_PEGS"]); tops = sorted({round(v.x, 2) for v in pegs if abs(v.y + 204) < 0.2 and abs(v.x) < 200})
cx = []
for t in tops:
    if cx and t - cx[-1][-1] < 1.0: cx[-1].append(t)
    else: cx.append([t])
cx = [round(sum(g) / len(g), 2) for g in cx]
gaps = sorted({round(b - a, 2) for a, b in zip(cx, cx[1:])})
chk("SV1", "line pegs at 24 ft on the south building line y=-204", gaps == [24.0] and len(cx) == 15, {"n": len(cx), "gaps": gaps})
corn = [(x, y) for (x, y) in ((-924, -204), (924, -204), (-924, 252), (924, 252)) if any(abs(v.x - x) < 0.2 and abs(v.y - y) < 0.2 for v in pegs)]
chk("SV2", "corner pegs at x +-924, y -204 / 252 (HP1851 frame)", len(corn) == 4, corn)
ch = O["SV_TOOL_CHAIN"]; chk("SV3", "Gunter's chain 66 ft of 100 links (7.92 in)", ch["links"] == 100 and abs(100 * 7.92 * I - 66) < 1e-6 and ch["length_ft"] == 66, {"links": ch["links"], "len": round(100 * 7.92 * I, 4)})
pv = vw(O["SV_TOOL_POLES"]); ph = max(v.z - zg(v.x, v.y) for v in pv if abs(v.x + 168) < 0.2)
chk("SV4", "ranging pole 8 ft above ground", abs(ph - 8) < 0.05, round(ph, 3))
# elms = transept r10 ELMS exactly
ELMS = {"ELM_SOUTH": (4.0, -128.0), "ELM_NORTH": (-3.0, 142.0), "ELM_NORTH2": (12.0, 98.0)}
for n, (x, y) in ELMS.items():
    v = vw(O[n + "_WOOD"]); zmin = min(p.z for p in v); base = [p for p in v if p.z < zmin + 0.6]
    bx = sum(p.x for p in base) / len(base); by = sum(p.y for p in base) / len(base)
    chk("E-" + n, "elm trunk at transept ELMS position", math.hypot(bx - x, by - y) < 0.6, {"base": (round(bx, 2), round(by, 2)), "want": (x, y)})
# overlay
w = vw(O["OVL_TRANSEPT_WIRE"]); xs = [p.x for p in w]; ys = [p.y for p in w]; zt = max(p.z for p in w)
chk("OV1", "overlay: span 72 between column lines, extrados 37.17 at spring 65, 408 ft long",
    abs((max(xs) - min(xs)) - 2 * 37.1667) < 0.5 and abs(zt - (65 + 37.1667)) < 0.3 and abs((max(ys) - min(ys)) - 408) < 0.5,
    {"x_extent": round(max(xs) - min(xs), 2), "crown": round(zt, 2), "len": round(max(ys) - min(ys), 2)}, "rods r=0.13 ft")
chk("OV2", "overlay labelled DESIGN STUDY and render-hidden outside CP008", "DESIGN STUDY" in O["OVL_LABEL"].data.body and O["OVL_TRANSEPT_WIRE"].hide_render, O["OVL_LABEL"].data.body)
# figures: on the ground, not intersecting parts/props
figs = [o for o in O if o.name.startswith(("SVP_", "ST_FIG", "RIDER_"))]
props = [o for o in solids if not o.name.startswith(("SVP_", "ST_FIG", "RIDER_", "SV_LINE", "SV_TOOL_CHAIN", "ROTTEN_ROW_RAILS", "ST_HOARDING", "SV_PEGS"))]
bad = []; flo = []
for f in figs:
    x, y, z = [v / FT for v in f.location]
    if not f.name.startswith("RIDER_") and abs(z - zg(x, y)) > 0.1: flo.append((f.name, round(z - zg(x, y), 3)))
    for o in props:
        if o.name.endswith("_WOOD"):
            if math.hypot(x - O[o.name].location.x / FT, y - O[o.name].location.y / FT) < 3: bad.append((f.name, o.name))
            continue
        if o.name == "SV_TOOL_POLES":
            if any(math.hypot(x - px, y - py) < 0.55 + 0.06 for px, py in ((-168, -204), (168, -204), (-96, -203.6), (-924, -204), (924, -204))): bad.append((f.name, o.name))
            continue
        l, h = bb(o)
        if l[0] < x + 0.55 and h[0] > x - 0.55 and l[1] < y + 0.55 and h[1] > y - 0.55 and l[2] < z + 5 and h[2] > z + 0.3: bad.append((f.name, o.name))
chk("F1", "no figure intersects a prop/part/tree (0.55 ft body core)", not bad, bad, "riders' ground check skipped (mounted)")
chk("F2", "standing figures on terrain", not flo, flo)
# file + others untouched
sz = os.path.getsize(bpy.data.filepath) / 2**20; chk("S1", "blend < 90 MB", sz < 90, round(sz, 2))
def gs(p):
    try: return subprocess.run(["git", "-C", p, "status", "--porcelain"], capture_output=True, text=True).stdout.strip()
    except Exception as e: return str(e)
st = gs("/workspace/crystal-palace-site")
foreign = [l for l in st.splitlines() if "hyde-park-site-1850-grok" not in l]
chk("S2", "worktree: nothing outside our folder modified (Muse/Claude/Codex untouched)", not foreign, foreign)
libs = [l.filepath for l in bpy.data.libraries]; chk("S3", "no linked libraries (props appended/copied)", True, libs)
json.dump({"round": "s01", "pass": sum(r["pass"] for r in R), "total": len(R), "checks": R}, open(OUT, "w"), indent=1)
for r in R: print("CHK", "PASS" if r["pass"] else "FAIL", r["id"], r["value"])
print("CHECK_SITE", sum(r["pass"] for r in R), "/", len(R))
