"""D-checks for HP-EMPTY / HP-DISMANTLE, run on the same combined scene the renders use (nothing saved).
blender -b <exterior>/rounds/x05.blend -P check_dismantle.py -- --dismantle rounds/d01_<state>.blend --state S --claude C --out checks/d01_<state>"""
import bpy, sys, os, json, math
from mathutils import Vector
from mathutils.bvhtree import BVHTree
argv = sys.argv[sys.argv.index("--") + 1:]
def arg(n, d=None): return argv[argv.index(n) + 1] if n in argv else d
HERE = os.path.dirname(os.path.abspath(__file__)); ROOTDIR = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(ROOTDIR, "..", "crystal-palace-1851-exterior-grok", "scripts")); sys.path.insert(0, HERE)
from combine import combine
import zones
FT = 0.3048; state = arg("--state"); DB = arg("--dismantle")
combine(arg("--claude"), DB, roof_override=True, furrow=True)
for o in bpy.data.objects:
    if o.get("part_kind") == "flag": o.hide_render = True
zinfo = zones.apply(state); nseam = zones.fix_floor_seam(); Z = zones.ZONE
rows = []
def chk(i, what, target, measured, ok): rows.append(dict(id=i, check=what, target=str(target), measured=str(measured), ok=bool(ok)))
route = json.load(open(os.path.join(ROOTDIR, "route", "camera_route.json")))
shots = [s for s in route["shots"] if state in s["states"]]
dg = bpy.context.evaluated_depsgraph_get()
vis = [o for o in bpy.data.objects if o.type == 'MESH' and not o.hide_render and o.visible_get() is not None]
def near_bvh(p, r):
    out = []
    for o in vis:
        if o.hide_render: continue
        bb = [o.matrix_world @ Vector(c) for c in o.bound_box]
        lo = Vector([min(v[i] for v in bb) for i in range(3)]); hi = Vector([max(v[i] for v in bb) for i in range(3)])
        d = Vector([max(lo[i] - p[i], 0, p[i] - hi[i]) for i in range(3)]).length
        if d < r:
            ev = o.evaluated_get(dg); me = ev.to_mesh()
            vs = [ev.matrix_world @ v.co for v in me.vertices]; ps = [list(pl.vertices) for pl in me.polygons]
            if ps: out.append((o.name, BVHTree.FromPolygons(vs, ps)))
            ev.to_mesh_clear()
    return out
for s in shots:
    for k in ("start", "end"):
        if k not in s: continue
        name = f"{s['id']}_{k}"; cam = bpy.data.objects.get(name)
        if not cam: chk("K00", f"{name} exists", "camera", "missing", False); continue
        rev = s["id"].startswith("REV")
        chk("K01", f"{name} lens", s["lens_mm"], round(cam.data.lens, 2), abs(cam.data.lens - s["lens_mm"]) < 0.01 and s["lens_mm"] in (28, 35, 50) and abs(cam.data.sensor_width - 36) < 0.01)
        xa = cam.matrix_world.to_3x3().col[0]
        chk("K02", f"{name} no roll (camera X axis z)", 0, round(xa.z, 5), abs(xa.z) < 1e-4)
        if not rev:
            base = s[k].get("eye_base_ft", 0.0)
            chk("K03", f"{name} eye height above standing surface (ft)", 5.25, round(cam.location.z / FT - base, 3), abs(cam.location.z / FT - base - 5.25) < 0.02)
            p = cam.location; md = 99.0; who = ""
            for n, t in near_bvh(p, 3.5 * FT * 3):
                r = t.find_nearest(p)
                if r[0] is not None and r[3] / FT < md: md, who = r[3] / FT, n
            chk("K04", f"{name} clearance to nearest visible mesh (ft)", ">= 3", f"{md:.2f} ({who})", md >= 3.0)
    if "end" in s and not s["id"].startswith("REV"):
        a = Vector(s["start"]["pos_ft"]); b = Vector(s["end"]["pos_ft"])
        chk("K05", f"{s['id']} move length (m)", "<= 10 m", round((b - a).length * FT, 2), (b - a).length * FT <= 10.0)
for f in os.listdir(os.path.join(ROOTDIR, "rounds")):
    if f.endswith(".blend"):
        mb = os.path.getsize(os.path.join(ROOTDIR, "rounds", f)) / 1e6
        chk("K06", f"rounds/{f} size (MB)", "< 90", round(mb, 1), mb < 90)
bad = [d.name for c in (bpy.data.objects, bpy.data.collections, bpy.data.materials, bpy.data.meshes) for d in c if "sydenham" in d.name.lower()]
chk("K07", "no Sydenham-named data (Hyde Park 1851 only)", 0, len(bad), not bad)
for kind in ("crowd", "banners", "sculpture", "textiles", "machinery", "planters"):
    n = sum(1 for o in bpy.data.objects if o.get("dress_kind") == kind and not o.hide_render)
    chk("K08", f"HP51 dressing '{kind}' visible", 0, n, n == 0)
n = sum(1 for o in bpy.data.objects if o.get("part_kind") in ("exhibit_plinth", "bench") and not o.hide_render)
chk("K09", "Muse plinths and benches cleared", 0, n, n == 0)
crates = [o for o in bpy.data.objects if o.get("part_kind") == "crate"]
cred = all("Muse" in str(o.get("credit", "")) or "Muse" in str(o.users_collection[0].get("credit", "")) for o in crates)
chk("K10", "Muse crates present and credited", "> 0, credited", f"{len(crates)}, credited={cred}", crates and cred)
cases = [o for o in bpy.data.objects if o.get("part_kind") == "exhibit_case" and not o.hide_render]
if state == "empty":
    chk("K11", "EMPTY: half the vitrines kept (dust-sheeted)", 24, len(cases), len(cases) == 24)
    ds = bpy.data.objects.get("D_DUST_SHEETS"); chk("K12", "EMPTY: dust sheets", "present", bool(ds), ds is not None)
    pc = [o for o in bpy.data.objects if o.get("part_kind") == "packing_case"]
    chk("K13", "EMPTY: packing cases at the machinery footprints", ">= 8", len(pc), len(pc) >= 8)
else:
    chk("K11", "DISMANTLE: all vitrines gone", 0, len(cases), len(cases) == 0)
    home = [o for o in bpy.data.objects if o.name.split(".")[0] == Z["lift_girder_name"]]
    chk("K14", "home girder hidden while lowered", "all hidden", [o.hide_render for o in home], home and all(o.hide_render for o in home))
    g = bpy.data.objects["D_GIRDER_LOWERING"]; bb = [g.matrix_world @ Vector(c) for c in g.bound_box]
    zlo, zhi = min(v.z for v in bb) / FT, max(v.z for v in bb) / FT; xlo, xhi = min(v.x for v in bb) / FT, max(v.x for v in bb) / FT
    chk("K15", "lowered girder between floor and its seat (ft)", "0 < z < 19.17", f"{zlo:.2f}-{zhi:.2f}", 0 < zlo and zhi < 19.17)
    chk("K16", "lowered girder clear of its columns (x, ft)", "156.4 < x < 179.6 (column faces)", f"{xlo:.2f}-{xhi:.2f}", xlo > 156.4 and xhi < 179.6)
    sh = bpy.data.objects["D_SHORES"]; bb = [sh.matrix_world @ Vector(c) for c in sh.bound_box]
    top = max(v.z for v in bb) / FT; nb = [o for o in bpy.data.objects if o.name.split(".")[0] == Z["shored_girder_name"]]
    gb = min((o.matrix_world @ Vector(c)).z for o in nb for c in o.bound_box) / FT if nb else -1
    chk("K17", "shores bear on the neighbour girder (top vs girder soffit, ft)", f"{gb:.2f} +/- 0.15", f"{top:.2f}", nb and abs(top - gb) < 0.15 and not nb[0].hide_render)
    sl = bpy.data.objects["D_SHEERLEGS"]; ap = max((sl.matrix_world @ Vector(c)).z for c in sl.bound_box) / FT
    chk("K18", "sheer-leg head above the girder line (ft)", "> 22.17 + 10", round(ap, 2), ap > 32.17)
    chk("K19", "zone R stripped / zone G glass-off units", "> 0 / > 0", f"{zinfo['R']} / {zinfo['G']}", zinfo["R"] > 0 and zinfo["G"] > 0)
    keys = bpy.data.objects.get("D_JOINT_KEYS"); jx, jy = Z["joint_xy"]
    kp = keys and min(((keys.matrix_world @ Vector(c)).xy - Vector((jx * FT, jy * FT))).length for c in keys.bound_box) / FT
    chk("K20", "joint keys at the column head (ft from joint)", "< 3", round(kp or 99, 2), keys and kp < 3)
fb = [o for o in bpy.data.objects if o.name.split(".")[0] == "FLOOR_BOARDS"]; eb = [o for o in bpy.data.objects if o.name.split(".")[0] == "EFLOOR_BOARDS"]
if fb and eb:
    dz = (max((eb[0].matrix_world @ Vector(c)).z for c in eb[0].bound_box) - max((fb[0].matrix_world @ Vector(c)).z for c in fb[0].bound_box)) / FT
    chk("K21", "floor seam: exterior boards above transept boards where they overlap (ft)", "0.01-0.05", round(dz, 3), 0.01 <= dz <= 0.05)
if state == "dismantle":
    g = bpy.data.objects["D_GIRDER_LOWERING"]; mn = {s.material.name for s in g.material_slots if s.material}
    chk("K22", "lowered + stacked girders in red-lead primer", "GT_RedLeadPrimer", sorted(mn), mn == {"GT_RedLeadPrimer"})
    st = bpy.data.objects.get("D_STAFF_STRIKER"); keys = bpy.data.objects.get("D_JOINT_KEYS")
    if st:
        d = ((st.matrix_world.translation.xy - Vector((Z["joint_xy"][0] * FT, Z["joint_xy"][1] * FT))).length) / FT
        chk("K23", "key striker within maul reach of the joint (ft, horizontal)", "< 4", round(d, 2), d < 4)
out = arg("--out"); os.makedirs(os.path.dirname(os.path.join(ROOTDIR, out)), exist_ok=True)
P = sum(r["ok"] for r in rows)
with open(os.path.join(ROOTDIR, out + ".json"), "w") as f: json.dump(dict(state=state, zones=zinfo, rows=rows, passed=P, total=len(rows)), f, indent=1)
with open(os.path.join(ROOTDIR, out + ".md"), "w") as f:
    f.write(f"# {os.path.basename(out)} checks: {P}/{len(rows)}\n\n| id | check | target | measured | pass |\n|---|---|---|---|---|\n")
    for r in rows: f.write(f"| {r['id']} | {r['check']} | {r['target']} | {r['measured']} | {'PASS' if r['ok'] else 'FAIL'} |\n")
print("CHECKS", P, "/", len(rows)); [print("FAIL", r) for r in rows if not r["ok"]]
