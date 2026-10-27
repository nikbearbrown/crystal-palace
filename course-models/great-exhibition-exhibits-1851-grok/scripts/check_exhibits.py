"""D-checks for the hero-exhibit assets. blender -b rounds/eNN.blend -P scripts/check_exhibits.py -- --out checks/eNN/checks.md"""
import bpy, sys, os, json, math
from mathutils import Vector
argv = sys.argv[sys.argv.index("--") + 1:]; OUT = argv[argv.index("--out") + 1]
FT = 0.3048; f = lambda m: m / FT; res = []
def chk(cid, ok, what, detail=""): res.append((cid, bool(ok), what, detail))
obs = bpy.data.objects; C = bpy.data.collections; sc = bpy.context.scene
def bb(objs):
    cs = [o.matrix_world @ Vector(c) for o in objs for c in o.bound_box]
    return [f(min(c[i] for c in cs)) for i in range(3)], [f(max(c[i] for c in cs)) for i in range(3)]
A = ["EXH_KOHINOOR", "EXH_OSLER_CANDELABRUM", "EXH_NASMYTH_HAMMER"]
miss = [n for n in A if n not in C]
chk("E01", not miss, "three asset collections present", f"missing {miss}")
bad = [n for n in A if n in C and not all(k in C[n] for k in ("credit", "sources", "status", "title"))]
chk("E02", not bad, "each asset carries title, status, credit and sources", f"{bad}")
org = {}
for n in A:
    lo, hi = bb(C[n].objects); org[n] = (round(lo[2], 3), round((lo[0] + hi[0]) / 2, 2), round((lo[1] + hi[1]) / 2, 2))
okorg = all(abs(v[0]) < 0.08 and abs(v[1]) < 0.6 and abs(v[2]) < 0.8 for v in org.values()) and all(tuple(C[n].instance_offset) == (0, 0, 0) for n in A)
chk("E03", okorg, "instance-ready: origin at floor centre (min z ~0, footprint centred), instance offset 0", json.dumps(org))
inst = [o for o in obs if o.instance_type == 'COLLECTION' and o.instance_collection and o.instance_collection.name in A]
chk("E04", len(inst) == 3, "preview stand uses collection instances (same path as placement elsewhere)", f"{len(inst)} instances")
lay = bpy.context.view_layer.layer_collection.children.get("EXH_ASSETS")
chk("E05", all(C[n].asset_data for n in A), "collections marked as Blender assets", f"{[bool(C[n].asset_data) for n in A]}")
d = obs["KOH_diamond"]; L, W, D = d["L_in"], d["W_in"], d["D_in"]
vol_in3 = 4 / 3 * math.pi * (L / 2) * (W / 2) * (D / 2) * 0.9; ct = vol_in3 * 16.387 * 3.52 * 5
chk("E06", 160 <= ct <= 210, "Koh-i-Noor sized for ~186 ct (pre-1852 cut) at diamond density 3.52 g/cm3", f"{L} x {W} x {D} in -> ~{ct:.0f} ct")
cage = obs["KOH_cage"]; crown = obs["KOH_crown"]; lo, hi = bb([cage]); clo, chi = bb([crown]); slo, shi = bb([obs["KOH_dome"]])
dlo, dhi = bb([d])
inside = all(lo[i] < dlo[i] and dhi[i] < hi[i] for i in range(2)) and dlo[2] > lo[2] and dhi[2] < shi[2] and slo[2] >= lo[2] - 0.01
chk("E07", inside and clo[2] >= hi[2] - 0.1, "stone under the glass dome, inside the gilded bars, crown on the apex", f"cage z {lo[2]:.2f}-{hi[2]:.2f}, crown top {chi[2]:.2f} ft")
rail = obs["KOH_rail"]; vis = [o for o in obs if o.get("role") == "visitor" and (o.location.xy.length / FT) < 20]
near = [o.name for o in vis if f(o.location.xy.length) < rail["radius_ft"] + 0.4]
chk("E08", not near, "Koh-i-Noor visitors stay outside the rail", f"{len(vis)} visitors near, {near}")
OC = C["EXH_OSLER_CANDELABRUM"]; olo, ohi = bb(OC.objects)
chk("E09", abs(ohi[2] - 8.0) < 0.15 and OC["lights_built"] == 15 and obs["OSL_shaft_prisms"]["length_ft"] > 3.0,
    "Osler candelabrum: 8 ft high, 15 lights, prism shaft over 3 ft (Official Catalogue)", f"h {ohi[2]:.2f} ft, {OC['lights_built']} lights, shaft {obs['OSL_shaft_prisms']['length_ft']:.2f} ft")
HC = C["EXH_NASMYTH_HAMMER"]; mach = [o for o in HC.objects if o.get("part_kind") not in ("rail", "label")]
sc.frame_set(1); hlo, hhi = bb(mach)
chk("E10", 13.0 <= hhi[0] - hlo[0] <= 14.6 and 5.5 <= hhi[1] - hlo[1] <= 6.6 and 18.0 <= hhi[2] <= 19.5,
    "Nasmyth hammer at the NMAH proportions: base ~14 x 6 ft, ~19 ft high", f"{hhi[0]-hlo[0]:.1f} x {hhi[1]-hlo[1]:.1f} x {hhi[2]:.1f} ft")
ram = obs["HAM_ram"]; zs = []
for fr in range(1, 97): sc.frame_set(fr); zs.append(f(ram.matrix_world.translation.z))
die = 2.95
chk("E11", abs(min(zs) - die) < 0.02 and 3.0 < max(zs) - min(zs) < 4.0 and sum(1 for a, b in zip(zs, zs[1:]) if a > die + 0.05 and b <= die + 0.02) >= 3,
    "ram animated: strikes the lower die (never through it), 3.5 ft stroke, repeated blows", f"z {min(zs):.2f}-{max(zs):.2f} ft")
rodtop = max(zs) + 2.55 + 8.9; rodbot = min(zs) + 2.55 + 8.9
chk("E12", 13.85 < rodbot and rodtop < 18.0, "piston rod stays inside the cylinder through the stroke", f"rod top {rodbot:.2f}-{rodtop:.2f} ft vs cylinder 13.85-18.0")
alo, ahi = bb([obs["HAM_anvil"]]); flo, fhi = bb([obs["HAM_frame"]])
chk("E13", obs["HAM_anvil"].get("independent_foundation") and ahi[0] < 2.2, "anvil block separate from the standards (own foundation)", f"anvil x {alo[0]:.1f}..{ahi[0]:.1f}")
sc.frame_set(48)
cams = [o for o in obs if o.type == 'CAMERA']
badeye = [c.name for c in cams if abs(f(c.location.z) - 5.25) > 0.01]
chk("E14", cams and not badeye, "cameras at 5.25 ft eye height", f"{len(cams)} cams, bad {badeye}")
roll = [c.name for c in cams if abs((c.matrix_world.to_3x3() @ Vector((1, 0, 0))).z) > 1e-4]
chk("E15", not roll, "no roll", f"{roll}")
lens = {c.name: c.data.lens for c in cams}; badl = [n for n, l in lens.items() if l not in (28, 35, 50)]
chk("E16", not badl, "lenses 28/35/50 only", json.dumps(lens))
dg = bpy.context.evaluated_depsgraph_get(); tight = []
dirs = [Vector((x, y, z)).normalized() for x in (-1, 0, 1) for y in (-1, 0, 1) for z in (-1, 0, 1) if (x, y, z) != (0, 0, 0)]
for c in cams:
    for dv in dirs:
        hit, loc, *_ = sc.ray_cast(dg, c.location, dv, distance=FT)
        if hit: tight.append(c.name); break
chk("E17", not tight, "cameras at least 1 ft from any mesh", f"{tight}")
syd = [o.name for o in obs if "sydenham" in o.name.lower()]
chk("E18", not syd, "Hyde Park 1851 only, no Sydenham content")
fsz = os.path.getsize(bpy.data.filepath) / 1e6
chk("E19", fsz < 90, "file under 90 MB", f"{fsz:.1f} MB")
os.makedirs(os.path.dirname(OUT), exist_ok=True)
with open(OUT, "w") as fh:
    fh.write(f"# exhibit checks {os.path.basename(bpy.data.filepath)}\n\n| id | result | check | detail |\n|---|---|---|---|\n")
    for cid, ok, w, dd in res: fh.write(f"| {cid} | {'PASS' if ok else 'FAIL'} | {w} | {dd} |\n")
    fh.write(f"\n{sum(r[1] for r in res)}/{len(res)} pass\n")
print(open(OUT).read())
