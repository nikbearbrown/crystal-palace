"""HP-EMPTY / HP-DISMANTLE (storyboard CP030-CP031, late 1851-1852). Grok Bot.
Stage 2 of scripts/build_round.sh: opens a transept base built with the transept's own scripts in a non-HP51 state
(build_transept.py -- --state empty: no crowd, banners, textiles, machinery, statues or planters) and adds the
after-exhibition dressing + the dismantling work zone, then saves dNN_<state>.blend. Everything new goes into
TRANSEPT_GROK/DISMANTLE_GROK so the exterior's combine() appends it with the transept at render time.
The exterior frame (x05) and Claude's west frame are never written: their per-state changes (roof glass off, stripped
bays, the girder being lowered) are applied at render time by zones.py.
  blender -b rounds/_base_empty.blend -P scripts/build_dismantle.py -- --state empty|dismantle --out rounds/d01_empty.blend
"""
import bpy, bmesh, math, random, sys, os, json
from mathutils import Vector, Matrix
argv = sys.argv[sys.argv.index("--") + 1:]
def arg(n, d=None): return argv[argv.index(n) + 1] if n in argv else d
STATE = arg("--state", "empty"); OUT = arg("--out")
assert STATE in ("empty", "dismantle"), STATE
HERE = os.path.dirname(os.path.abspath(__file__)); ROOTDIR = os.path.dirname(HERE)
TRS = os.path.join(ROOTDIR, "..", "crystal-palace-1851-transept-grok", "scripts")
sys.path.insert(0, TRS); sys.path.insert(0, HERE)
import figures            # transept r09 stand-ins (Grok), base=False for live horses
import zones as Z
FT = 0.3048
def ft(f): return f * FT
def inch(i): return i / 12.0 * FT
rnd = random.Random(1852)
scene = bpy.context.scene
ROOT = bpy.data.collections["TRANSEPT_GROK"]
D = bpy.data.collections.new("DISMANTLE_GROK"); ROOT.children.link(D)
SUB = {}
def sub(n):
    if n not in SUB: c = bpy.data.collections.new("D_" + n); D.children.link(c); SUB[n] = c
    return SUB[n]
def mat(name, rgb, rough=0.8, metal=0.0):
    m = bpy.data.materials.get(name)
    if m: return m
    m = bpy.data.materials.new(name); m.use_nodes = True
    b = m.node_tree.nodes["Principled BSDF"]; b.inputs["Base Color"].default_value = (*rgb, 1)
    b.inputs["Roughness"].default_value = rough; b.inputs["Metallic"].default_value = metal
    m.diffuse_color = (*rgb, 1); return m
def finish(bm, name, m0, extra=()):
    me = bpy.data.meshes.new(name); bm.to_mesh(me); bm.free()
    me.materials.append(m0)
    for m in extra: me.materials.append(m)
    return me
def obj(name, me, c, loc=(0, 0, 0), rz=0.0, **props):
    o = bpy.data.objects.new(name, me); o.location = [ft(v) for v in loc]; o.rotation_euler = (0, 0, rz)
    sub(c).objects.link(o)
    for k, v in props.items(): o[k] = v
    return o
def mark(bm, n0, idx):
    bm.faces.ensure_lookup_table()
    for f in bm.faces[n0:]: f.material_index = idx
def box(bm, x0, x1, y0, y1, z0, z1):   # feet
    vs = [bm.verts.new((ft(a), ft(b), ft(c))) for a, b, c in
          [(x0, y0, z0), (x1, y0, z0), (x1, y1, z0), (x0, y1, z0), (x0, y0, z1), (x1, y0, z1), (x1, y1, z1), (x0, y1, z1)]]
    for f in [(0, 3, 2, 1), (4, 5, 6, 7), (0, 1, 5, 4), (1, 2, 6, 5), (2, 3, 7, 6), (3, 0, 4, 7)]: bm.faces.new([vs[i] for i in f])
def rod(bm, a, b, r, seg=8):   # feet
    a = Vector([ft(v) for v in a]); b = Vector([ft(v) for v in b]); d = b - a
    M = Matrix.Translation((a + b) / 2) @ d.to_track_quat('Z', 'Y').to_matrix().to_4x4()
    bmesh.ops.create_cone(bm, cap_ends=True, segments=seg, radius1=ft(r), radius2=ft(r), depth=d.length, matrix=M)
def beam(bm, a, b, w, t):      # square timber from a to b (feet), w x t feet
    a = Vector(a); b = Vector(b); d = (b - a); L = d.length
    q = d.to_track_quat('Z', 'Y'); M = Matrix.Translation(Vector([ft(v) for v in (a + b) / 2])) @ q.to_matrix().to_4x4()
    bmesh.ops.create_cube(bm, size=1.0, matrix=M @ Matrix.Diagonal((ft(w), ft(t), ft(L), 1)))

# ---------------- materials ----------------
CRATEW = mat("GT_PackingCase", (0.36, 0.28, 0.19), 0.85)
CRATEW_D = mat("GT_PackingCaseDark", (0.22, 0.17, 0.12), 0.85)
STRAW = mat("GT_Straw", (0.62, 0.52, 0.30), 0.95)
SHEET = mat("GT_DustSheet", (0.80, 0.78, 0.72), 0.95)
OAK = mat("GT_ShoreTimber", (0.34, 0.27, 0.19), 0.85)
ROPE = mat("GT_Rope", (0.45, 0.40, 0.30), 0.9)
POLE = mat("GT_ScaffoldPole", (0.32, 0.27, 0.20), 0.85)
PLANK = mat("GT_ScaffoldPlank", (0.40, 0.34, 0.26), 0.85)
IRON = bpy.data.materials.get("GT_Iron") or mat("GT_Iron", (0.30, 0.42, 0.60), 0.5, 0.2)
CAST = mat("GT_CastIronBare", (0.13, 0.13, 0.14), 0.55, 0.4)
TIMBERP = mat("GT_SashBarBundle", (0.70, 0.66, 0.58), 0.8)
REDLEAD = mat("GT_RedLeadPrimer", (0.40, 0.10, 0.05), 0.7)       # d03 DM13
STENCIL = mat("GT_CaseStencil", (0.05, 0.04, 0.03), 0.9)
SK = [mat("GT_Skin_a", (0.72, 0.53, 0.42), 0.6), mat("GT_Skin_b", (0.60, 0.43, 0.33), 0.6)]
WCOAT = [mat("GT_WorkCoat_dk", (0.05, 0.05, 0.06), 0.85), mat("GT_WorkCoat_brn", (0.14, 0.10, 0.07), 0.85),
         mat("GT_WorkSmock", (0.62, 0.60, 0.52), 0.9), mat("GT_WorkShirt", (0.74, 0.72, 0.66), 0.85)]
WTROU = [mat("GT_WorkTrou_fawn", (0.36, 0.31, 0.23), 0.85), mat("GT_WorkTrou_dk", (0.10, 0.09, 0.08), 0.85)]
HATS = [mat("GT_WorkCap", (0.08, 0.07, 0.06), 0.85), mat("hat_black_D", (0.02, 0.02, 0.02), 0.8)]
TRIM = mat("GT_WorkTrim", (0.70, 0.68, 0.62), 0.85)   # d04: r10-style cravat/belt slot
POLICE = mat("GT_PoliceBlue", (0.03, 0.04, 0.08), 0.8)
info = {"state": STATE, "credits": []}

# ---------------- the transept's own HP51 leftovers ----------------
cases = sorted([o for o in [_o for _o in ROOT.all_objects if _o is not None] if o.get("part_kind") == "exhibit_case"], key=lambda o: o.name)
plinths = [o for o in [_o for _o in ROOT.all_objects if _o is not None] if o.get("part_kind") == "exhibit_plinth"]
benches = [o for o in [_o for _o in ROOT.all_objects if _o is not None] if o.get("part_kind") == "bench"]
def hide(o): o.hide_render = True; o.hide_viewport = True; o["hidden_by_state"] = STATE
kept_cases = []
for i, o in enumerate(cases):
    if STATE == "dismantle" or i % 2 == 1: hide(o)                 # half the Muse cases already gone in HP-EMPTY
    else: kept_cases.append(o)
for o in plinths + benches: hide(o)
for o in [_o for _o in ROOT.all_objects if _o is not None]:
    if o.get("part_kind") == "fountain_water" or o.name in ("FOUNTAIN_WATER", "FOUNTAIN_JET"): hide(o)     # water off
    if STATE == "dismantle" and o.get("part_kind") in ("fountain", "fountain_water"): hide(o)   # fountain removed (DM05)
info["cases_kept"] = len(kept_cases); info["cases_hidden"] = len(cases) - len(kept_cases)

# ---------------- Muse crate (models/hp-crate-and-display-case), read-only append, closed variant ----------------
MUSE = "/workspace/models-main-ro/models/hp-crate-and-display-case/hp-crate-and-display-case.blend"
with bpy.data.libraries.load(MUSE, link=False) as (src, dst):
    dst.objects = [n for n in src.objects if n.startswith("Crate")]
MC = bpy.data.collections.new("MUSE_Crate_by_Muse_D"); MC.instance_offset = (-1.4, 0.0, 0.0)
MC["credit"] = "Muse, models/hp-crate-and-display-case (origin/main), appended read-only; closed sheathing Grok (construction c04 recipe)"
for o in dst.objects:
    if o: MC.objects.link(o)
bm = bmesh.new()                       # sheathing boards + lid over Muse's frame (same recipe as construction c04, CN30)
def mbox(bm, x0, x1, y0, y1, z0, z1):
    vs = [bm.verts.new(v) for v in [(x0, y0, z0), (x1, y0, z0), (x1, y1, z0), (x0, y1, z0), (x0, y0, z1), (x1, y0, z1), (x1, y1, z1), (x0, y1, z1)]]
    for f in [(0, 3, 2, 1), (4, 5, 6, 7), (0, 1, 5, 4), (1, 2, 6, 5), (2, 3, 7, 6), (3, 0, 4, 7)]: bm.faces.new([vs[i] for i in f])
for k in range(5):
    z0 = 0.03 + k * 0.152; z1 = z0 + 0.146
    mbox(bm, -1.905, -0.895, -0.405, -0.395, z0, z1); mbox(bm, -1.905, -0.895, 0.395, 0.405, z0, z1)
    mbox(bm, -1.905, -1.895, -0.395, 0.395, z0, z1); mbox(bm, -0.905, -0.895, -0.395, 0.395, z0, z1)
for k in range(6): mbox(bm, -1.905 + k * 0.1683, -1.905 + k * 0.1683 + 0.162, -0.41, 0.41, 0.80, 0.82)
sheath = bpy.data.objects.new("CRATE_closed_sheathing_Grok_D", finish(bm, "crate_closed_sheathing_D", CRATEW)); MC.objects.link(sheath)
info["credits"].append("Muse crate frame appended read-only (models/hp-crate-and-display-case)")
CRATE_W, CRATE_D_, CRATE_H = 1.01 / FT, 0.82 / FT, 0.845 / FT          # ~3.3 x 2.7 x 2.8 ft
crates = []
def muse_crate(x, y, z=0.0, rz=0.0, tag=""):
    e = bpy.data.objects.new(f"D_CRATE_{len(crates):03d}{tag}", None); e.instance_type = 'COLLECTION'; e.instance_collection = MC
    e.location = (ft(x), ft(y), ft(z)); e.rotation_euler = (0, 0, rz); sub("CRATES").objects.link(e)
    e["part_kind"] = "crate"; e["credit"] = "Muse"; crates.append(e); return e
# exhibitors' own packing cases for machinery (Grok): boarded box with battens and a stencilled band
case_meshes = {}
def case_mesh(L, W, H):
    k = (L, W, H)
    if k in case_meshes: return case_meshes[k]
    bm = bmesh.new(); box(bm, -L / 2, L / 2, -W / 2, W / 2, 0.25, H)
    for x in [(-L / 2) + i * L / max(2, int(L / 3)) for i in range(int(L / 3) + 1)]:
        box(bm, x - 0.2, x + 0.2, -W / 2 - 0.08, W / 2 + 0.08, 0.25, H + 0.05)          # battens
    n0 = len(bm.faces)
    for sx in (-L / 2 + 0.6, L / 2 - 0.6): box(bm, sx - 0.25, sx + 0.25, -W / 2 + 0.3, W / 2 - 0.3, 0.0, 0.25)   # skids
    mark(bm, n0, 1); n0 = len(bm.faces)
    box(bm, -L / 4, L / 4, -W / 2 - 0.1, -W / 2 - 0.09, H * 0.55, H * 0.7); mark(bm, n0, 2)  # stencil band
    case_meshes[k] = finish(bm, f"packing_case_{L}x{W}x{H}", CRATEW, [CRATEW_D, STENCIL]); return case_meshes[k]
pcases = []
def pcase(x, y, L, W, H, rz=0.0, z=0.0):
    o = obj(f"D_PCASE_{len(pcases):02d}", case_mesh(L, W, H), "CRATES", (x, y, z), rz, part_kind="packing_case", credit="Grok")
    pcases.append(o); return o
STRAWM = None
def straw_mesh():
    bm = bmesh.new()
    for i in range(14):
        a = rnd.uniform(0, 6.283); r = rnd.uniform(0.3, 2.2); x, y = r * math.cos(a), r * math.sin(a)
        box(bm, x - 0.45, x + 0.45, y - 0.3, y + 0.3, 0.0, 0.05 + rnd.uniform(0, 0.08))
    return finish(bm, "straw_litter", STRAW)
STRAWM = straw_mesh()
def straw(x, y, rz=0.0): return obj(f"D_STRAW_{x:+.0f}_{y:+.0f}", STRAWM, "LITTER", (x, y, 0.005), rz, part_kind="litter")

# ---------------- people: workmen and an attendant (figures.person_mesh, Grok r09) ----------------
# d04: r10 figure styles for workmen (caps, frock coats, cravats, belts)
PM = []
_STYLES = [
    {"hat": "cap", "frock": True, "cravat": True},
    {"hat": "low", "frock": True, "cravat": False},
    {"hat": "cap", "frock": False, "belt": True},
    {"hat": "top", "frock": True, "cravat": True},
    {"hat": "cap", "frock": True, "cane": False},
    {"hat": "low", "frock": False, "cravat": True},
]
for j in range(6):
    PM.append(figures.person_mesh(f"PERSON_workman_{j}", "man",
              [WCOAT[j % 4], WTROU[j % 2], SK[j % 2], HATS[0 if _STYLES[j]["hat"] == "cap" else 1], TRIM],
              style=_STYLES[j]))
PM_POLICE = figures.person_mesh("PERSON_policeman", "man", [POLICE, POLICE, SK[0], HATS[1], TRIM],
                                style={"hat": "top", "frock": True})
staff = []
def man(x, y, face_deg, role="workman", z=0.0, k=None):
    me = PM_POLICE if role == "police" else PM[(len(staff) if k is None else k) % len(PM)]
    # figures.person_mesh faces -Y at rz 0 (r09 bonnet convention), so facing direction face_deg needs rz = face_deg + 90 (d03 fix, DM18)
    o = obj(f"D_STAFF_{len(staff):02d}_{role}", me, "STAFF", (x, y, z), math.radians(face_deg + 90), part_kind="figure", role=role, face_deg=face_deg)
    staff.append(o); return o
# a two-man crate carry on poles and a sack truck
def carry(x, y, face_deg):
    a = math.radians(face_deg); dx, dy = math.cos(a), math.sin(a); nx, ny = -dy, dx
    man(x + 3.6 * dx, y + 3.6 * dy, face_deg); man(x - 3.6 * dx, y - 3.6 * dy, face_deg)
    bm = bmesh.new()
    for s in (-0.9, 0.9):
        rod(bm, (x - 4.6 * dx + s * nx, y - 4.6 * dy + s * ny, 3.1), (x + 4.6 * dx + s * nx, y + 4.6 * dy + s * ny, 3.1), 0.12, 8)
    n0 = len(bm.faces); box(bm, x - 1.4, x + 1.4, y - 1.1, y + 1.1, 2.3, 4.4); mark(bm, n0, 1)
    obj(f"D_CARRY_{len(staff):02d}", finish(bm, "carry_poles", POLE, [CRATEW]), "STAFF", (0, 0, 0), 0.0, part_kind="handling")
def sack_truck(x, y, face_deg, loaded=True):
    bm = bmesh.new()
    for s in (-0.9, 0.9): rod(bm, (0, s, 0.6), (-1.6, s, 4.6), 0.07, 6)
    for s in (-1.0, 1.0): rod(bm, (0.05, s - 0.1, 0.6), (0.05, s + 0.1, 0.6), 0.6, 14)
    box(bm, 0.0, 0.9, -0.9, 0.9, 0.0, 0.1)
    if loaded:
        n0 = len(bm.faces); box(bm, -0.2, 2.0, -1.1, 1.1, 0.1, 2.4); mark(bm, n0, 1)
    obj(f"D_SACKTRUCK_{x:+.0f}_{y:+.0f}", finish(bm, "sack_truck", CAST, [CRATEW]), "STAFF", (x, y, 0), math.radians(face_deg), part_kind="handling")

def trolley(tx, ty, trz, load="columns", tag=""):
    """four-wheeled timber trolley (pole wagon) 16 ft with a draught horse and carter (Grok)"""
    HORSE = mat("GT_DraughtHorse", (0.13, 0.08, 0.05), 0.7)
    hm = bpy.data.meshes.get("horse_draught_bay_D") or figures.horse_group_mesh("horse_draught_bay_D", 2.35, HORSE, rearing=False, rider=False, base=False)
    bm = bmesh.new()
    for sx in (-6.0, 6.0):
        for sy in (-2.6, 2.6): rod(bm, (sx, sy - 0.2, 1.8), (sx, sy + 0.2, 1.8), 1.8, 18)
    box(bm, -8, 8, -2.2, 2.2, 2.6, 3.0); beam(bm, (8, 0, 2.6), (14, 0, 3.2), 0.3, 0.3)
    n0 = len(bm.faces)
    if load == "columns":
        for k in range(2): box(bm, -7.5, 7.5, -0.6 + k * 1.2 - 0.35, -0.6 + k * 1.2 + 0.35, 3.0, 5.6)
        mark(bm, n0, 1)
    else:                                                    # packing cases, roped
        box(bm, -7.5, -1.0, -2.0, 2.0, 3.0, 7.2); box(bm, -0.5, 4.5, -1.8, 1.8, 3.0, 6.0); box(bm, 5.0, 7.6, -1.5, 1.5, 3.0, 5.4)
        mark(bm, n0, 2); n0 = len(bm.faces)
        for x in (-5.5, -3.0, 2.0): box(bm, x - 0.06, x + 0.06, -2.08, 2.08, 3.0, 7.25)
        mark(bm, n0, 3)
    obj(f"D_TROLLEY{tag}", finish(bm, "trolley_D" + tag, CRATEW_D, [CAST, CRATEW, ROPE]), "STACKS", (tx, ty, 0), math.radians(trz), part_kind="cart", load=load)
    a = math.radians(trz)
    obj(f"D_HORSE{tag}", hm, "STACKS", (tx + 16.5 * math.cos(a), ty + 16.5 * math.sin(a), 0), a, part_kind="horse")
    man(tx + 19 * math.cos(a) + 2.5 * math.sin(a), ty + 19 * math.sin(a) - 2.5 * math.cos(a), trz - 90, k=0)

# ---------------- HP-EMPTY: crates at former exhibit positions, dust sheets, straw, staff ----------------
# east nave machinery footprints from transept dressing.py (r09): the exhibitors' cases now stand where the machines did
MACH = {"LOCOMOTIVE": (84, -28.5, 30, 8, 9), "STEAM_ENGINE": (72, -48, 16, 9, 8), "HYDRAULIC_PRESS": (96, -48, 12, 8, 9),
        "MARINE_ENGINE": (120, -48, 12, 8, 8), "BEAM_ENGINE": (72, 48, 14, 9, 10), "POWER_LOOMS": (96, 48, 16, 6, 6),
        "REAPER": (92, 20, 14, 7, 6), "PRINTING_MACHINE": (120, 48, 9, 9, 9)}
if STATE == "empty":
    for n, (x, y, L, W, H) in MACH.items():
        if n == "LOCOMOTIVE":       # the engine itself still on its display rails, half boxed: case sections either side
            pcase(x - 10, y, 9, W, H); pcase(x + 9, y, 11, W, H - 1); pcase(x - 1, y + 0.3, 6, W - 1.5, H - 2.5)
        else:
            pcase(x, y, L * 0.6, W * 0.8, H * 0.8, rz=rnd.uniform(-0.05, 0.05))
            pcase(x + L * 0.35, y + (W * 0.6 if y > 0 else -W * 0.6) * 0.0, 4, 3.5, 3.5, rz=0.3)
        straw(x - L * 0.45, y + 3.5, rnd.uniform(0, 3)); straw(x + 2, y - 4, rnd.uniform(0, 3))
    # Muse crates where the hidden cases were (transept aisles); every kept case gets a dust sheet
    for o in cases:
        if o in kept_cases: continue
        x, y = o.location.x / FT, o.location.y / FT
        for k in range(rnd.choice([1, 2, 3])):
            muse_crate(x + rnd.uniform(-0.6, 0.6), y + (k - 1) * 3.2, 0, rnd.uniform(-0.1, 0.1) + (math.pi / 2 if k % 2 else 0))
        if rnd.random() < 0.5: muse_crate(x, y, CRATE_H, 0.2)
        straw(x + 3.5, y, rnd.uniform(0, 3))
    bm = bmesh.new()
    for o in kept_cases:
        x, y = o.location.x / FT, o.location.y / FT
        box(bm, x - 2.3, x + 2.3, y - 4.3, y + 4.3, 0.4, 7.4)          # sheet thrown over the case (Muse case ~4 x 8 x 7 ft)
        box(bm, x - 2.45, x + 2.45, y - 4.45, y + 4.45, 0.0, 0.4)
    obj("D_DUST_SHEETS", finish(bm, "dust_sheets", SHEET), "LITTER", part_kind="dust_sheet", n=len(kept_cases))
    # staff: CP030 walk (x 40 -> 64, y -6 -> -23) passes porters carrying cases toward the east doors
    carry(78, -12, 0); sack_truck(100, -6, 180); man(102.5, -6, 180, k=3)
    man(70, 4, 200, k=1); man(73, 6, 250, k=4)                    # two talking by the reaper's case
    man(110, -30, 90, k=2); man(118, 24, 270, k=5); man(126, -10, 180, "police")
    man(88, -44, 0, k=0); man(92, -45, 20, k=3)                  # nailing the press case
    man(-10, 60, 270, k=2); man(12, -70, 90, k=4); man(-40, -100, 0, k=1)
    carry(20, 120, 270); sack_truck(42, 96, 90, loaded=False)
    # d03: more porters and a mid-distance cart (CP030 walk looks east down the nave; aisle looks south)
    trolley(112, -21, 0, load="cases", tag="_E")                     # loading for the east doors, horse to the east
    man(106, -26.2, 90, k=1); man(110, -26.4, 100, k=4); man(116, -25.8, 80, k=2)   # lifting a case up on the off side
    pcase(109, -29.5, 4, 3.5, 3.5, rz=0.1)
    carry(94, -18, 10); carry(124, -8, 180)
    man(132, -38, 160, k=5); man(134, -36, 200, k=3)
    carry(50, -84, 270); man(45, -104, 80, k=2); sack_truck(52, -118, 90); man(54.6, -118, 270, k=1)
    carry(44, -136, 90); man(40, -60, 300, k=4)

# ---------------- HP-DISMANTLE: the work zone (DM03-DM08) ----------------
if STATE == "dismantle":
    # transept leftovers: a few crates by the fountain site, straw
    for k in range(6): muse_crate(-6 + 3.4 * k, -20 - (k % 2) * 3.0, 0, 0.05 * k)
    for (x, y) in ((0, 0), (40, 20), (-30, -60), (90, -10)): straw(x, y, rnd.uniform(0, 3))
    zinfo = Z.ZONE
    # 1. the girder being lowered: a copy of the 24 ft girder (transept mesh) hanging between the columns
    gm = None
    for o in [_o for _o in ROOT.all_objects if _o is not None]:
        if o.get("part_kind") == "girder" and o.type == 'MESH' and 23.0 < o.dimensions.x / FT < 24.0 and o.dimensions.z / FT > 2.5:
            gm = o.data; break
    gx, gy = zinfo["lift_girder_xy"]; gz0 = zinfo["lift_bottom_ft"]
    if gm is None:
        bm = bmesh.new(); box(bm, -11.76, 11.76, -0.17, 0.17, -3.0, 0.0); gm = finish(bm, "girder24_D", IRON)
    zl = gm.vertices[0].co.z
    zmin = min(v.co.z for v in gm.vertices) / FT
    GR = math.radians(zinfo.get("lift_cant_deg", 15.0))        # canted by the tag lines to clear the column shafts
    gmr = bpy.data.meshes.get("girder24_redlead_D")
    if gmr is None:
        gmr = gm.copy(); gmr.name = "girder24_redlead_D"
        for i in range(len(gmr.materials)): gmr.materials[i] = REDLEAD
    gm = gmr          # DM13: lowered + stacked girders shown in red-lead primer (paint scraped at the bearings; reads off the white)
    G = obj("D_GIRDER_LOWERING", gm, "LIFT", (gx, gy, gz0 - zmin), GR, part_kind="girder", state="lowering",
            home=zinfo["lift_girder_name"], credit="Grok (girder mesh from the transept)")
    APEX = zinfo["apex_ft"]
    bm = bmesh.new()
    for fx, fy in zinfo["leg_feet"]: rod(bm, (fx, fy, 0), APEX, 5 / 12, 10)
    for fx, fy in zinfo["leg_feet"]: box(bm, fx - 1.2, fx + 1.2, fy - 1.2, fy + 1.2, 0, 0.5)          # sole pieces
    obj("D_SHEERLEGS", finish(bm, "sheerlegs_D", POLE), "LIFT", part_kind="sheer_legs", apex_ft=list(APEX),
        credit="Grok (construction c04 sheer-legs recipe)")
    gtop = gz0 + 3.0
    bm = bmesh.new()
    rod(bm, APEX, (APEX[0], APEX[1], gtop + 3.6), 0.06, 6)                               # fall (apex is over the girder)
    box(bm, APEX[0] - 0.5, APEX[0] + 0.5, APEX[1] - 0.35, APEX[1] + 0.35, gtop + 2.2, gtop + 3.6)   # lower block
    for sx in (-7.0, 7.0): rod(bm, (gx + sx * math.cos(GR), gy + sx * math.sin(GR), gtop), (gx, gy, gtop + 2.4), 0.05, 6)  # sling
    foot = tuple(zinfo["leg_feet"][1]) + (0.6,)
    rod(bm, APEX, foot, 0.05, 6); rod(bm, foot, tuple(zinfo["winch_xy"]) + (2.0,), 0.05, 6)     # lead via snatch block to the crab
    for a in zinfo["guy_anchors"]: rod(bm, APEX, tuple(a) + (0.0,), 0.05, 6)                    # guys
    for (tx, ty), sx in zip(zinfo["tag_men"], (-11.0, 11.0)):
        rod(bm, (gx + sx * math.cos(GR), gy + sx * math.sin(GR), gz0 + 1.5), (tx, ty, 3.6), 0.04, 6)                         # tag lines
    obj("D_ROPES", finish(bm, "ropes_D", ROPE), "LIFT", part_kind="rope")
    wx, wy = zinfo["winch_xy"]
    bm = bmesh.new(); box(bm, -1.5, 1.5, -1.2, 1.2, 0, 2.4); rod(bm, (-1.7, 0, 2.0), (1.7, 0, 2.0), 0.6, 14)
    for s in (-1.75, 1.75): rod(bm, (s, 0, 2.0), (s, 0.9, 3.3), 0.08, 6)                   # crank handles
    obj("D_CRAB_WINCH", finish(bm, "crab_D", PLANK), "LIFT", (wx, wy, 0), 0.0, part_kind="winch", credit="Grok (construction c04 recipe)")
    man(wx - 2.4, wy + 1.0, 180, k=0); man(wx + 2.4, wy + 1.0, 180, k=3)
    for (tx, ty), fd in zip(zinfo["tag_men"], (90, 270)): man(tx, ty, fd, k=1 if fd == 90 else 4)
    man(gx - 6, gy + 9, 250, k=2)                                     # ganger watching the load
    # 2. timber shores under the neighbouring girder BEFORE its joint is released (storyboard: show support first)
    sx0, sx1, sy = zinfo["shored_girder"]
    bm = bmesh.new(); n_sh = 0
    for x in (sx0 + 3.0, sx1 - 3.0):
        box(bm, x - 2.0, x + 2.0, sy - 2.5, sy + 2.5, 0.0, 0.5)                          # sole plate
        box(bm, x - 0.45, x + 0.45, sy - 0.45, sy + 0.45, 0.5, 18.25)                     # 10 x 10 in shore
        box(bm, x - 0.5, x + 0.5, sy - 2.0, sy + 2.0, 18.25, 18.9)                       # head tree
        box(bm, x - 0.3, x + 0.3, sy - 0.45, sy + 0.45, 18.9, 19.17)                     # folding wedges
        for s in (-1, 1): beam(bm, (x, sy + s * 2.0, 18.4), (x, sy + s * 9.0, 0.3), 0.5, 0.5)   # raking braces
        n_sh += 1
    obj("D_SHORES", finish(bm, "shores_D", OAK), "SUPPORT", part_kind="shore", n=n_sh, under=zinfo["shored_girder_name"])
    # 3. the released joint at the column head: scaffold tower, keys knocked out, men with mallet and bar
    jx, jy = zinfo["joint_xy"]; dk = zinfo["deck_ft"]; (dx0, dx1, dy0, dy1) = zinfo["deck_rect"]
    bm = bmesh.new()
    for x in (dx0, dx1):
        for y in (dy0, dy1): rod(bm, (x, y, -0.3), (x, y, dk + 3.6), 0.25, 8)
    for z in (6.0, 11.0):
        for y in (dy0, dy1): beam(bm, (dx0 - 0.5, y, z), (dx1 + 0.5, y, z), 0.33, 0.33)
        for x in (dx0, dx1): beam(bm, (x, dy0 - 0.5, z), (x, dy1 + 0.5, z), 0.33, 0.33)
    beam(bm, (dx0, dy1, dk + 3.4), (dx1, dy1, dk + 3.4), 0.25, 0.25); beam(bm, (dx1, dy0, dk + 3.4), (dx1, dy1, dk + 3.4), 0.25, 0.25)  # guard rail (back + side)
    beam(bm, (dx0, dy0, 0.3), (dx0, dy1, dk), 0.25, 0.25)                                   # brace
    n0 = len(bm.faces); box(bm, dx0 - 0.4, dx1 + 0.4, dy0 - 0.4, dy1 + 0.4, dk - 0.2, dk); mark(bm, n0, 1)
    for k in range(9): box(bm, dx1 + 0.2, dx1 + 1.2, dy0 + 0.6 * k * 0.0 + 0.2, dy0 + 1.4, k * dk / 9, k * dk / 9 + 0.15)  # ladder rungs
    for s in (0.2, 1.4): rod(bm, (dx1 + 0.7, dy0 + s, 0), (dx1 + 0.7, dy0 + s, dk + 3), 0.1, 6)
    obj("D_SCAFFOLD_JOINT", finish(bm, "scaffold_joint_D", POLE, [PLANK]), "SUPPORT", part_kind="scaffold", deck_ft=dk,
        rect=list(zinfo["deck_rect"]))
    bm = bmesh.new()                                           # iron keys: one half-driven out, two on the deck
    box(bm, jx + 0.55, jx + 0.72, jy - 0.07, jy + 0.07, 20.9, 23.0)
    box(bm, dx0 + 1.0, dx0 + 2.1, dy0 + 0.8, dy0 + 0.95, dk, dk + 0.12); box(bm, dx0 + 1.3, dx0 + 2.4, dy0 + 1.3, dy0 + 1.45, dk, dk + 0.12)
    obj("D_JOINT_KEYS", finish(bm, "joint_keys_D", CAST), "SUPPORT", part_kind="joint_key", state="released")
    # d03 (DM17): the key strike. A light trestle stage on the floor N of the girder line, west of the shore braces;
    # the smith stands on it at 16 ft and swings the maul at the half-driven key; mate holds a drift on the deck.
    TS = (180.75, 182.35, -153.9, -152.1, 16.0)
    tx0, tx1, ty0, ty1, tz = TS
    bm = bmesh.new()
    for x in (tx0 + 0.15, tx1 - 0.15):
        for y in (ty0 + 0.15, ty1 - 0.15): rod(bm, (x, y, 0), (x, y, tz), 0.13, 8)
    for z in (5.0, 10.5):
        for y in (ty0 + 0.15, ty1 - 0.15): beam(bm, (tx0, y, z), (tx1, y, z), 0.25, 0.25)
    beam(bm, (tx0 + 0.15, ty0 + 0.15, 0.3), (tx0 + 0.15, ty1 - 0.15, tz - 0.3), 0.2, 0.2)
    n0 = len(bm.faces); box(bm, tx0, tx1, ty0, ty1, tz - 0.2, tz); mark(bm, n0, 1)
    for k in range(13): box(bm, tx1 + 0.05, tx1 + 0.25, ty0 + 0.4, ty1 - 0.4, k * tz / 13 + 0.6, k * tz / 13 + 0.75)   # ladder on the E face
    obj("D_TRESTLE_STAGE", finish(bm, "trestle_stage_D", POLE, [PLANK]), "SUPPORT", part_kind="scaffold", deck_ft=tz)
    kx, ky, kz = jx + 0.64, jy, 21.9                          # key head
    sx_, sy_ = 181.65, -152.95
    # d04: maul with a distinct cast-iron head (barrel + peen) and raised two-handed strike pose
    hand = Vector((sx_ - 0.25, sy_ - 0.45, tz + 4.55)); head = Vector((kx + 0.35, ky + 0.4, kz + 0.15))
    bm = bmesh.new(); rod(bm, tuple(hand), tuple(head), 0.065, 8)             # ash helve
    dd = (head - hand).normalized(); hz = Vector((kx - head.x, ky - head.y, 0))
    if hz.length < 1e-6: hz = Vector((1, 0, 0))
    hz.normalize()
    # barrel head ~10 in long x 5 in dia, peen on the far side
    rod(bm, tuple(head - hz * 0.55), tuple(head + hz * 0.35), 0.28, 12)
    rod(bm, tuple(head + hz * 0.35), tuple(head + hz * 0.55), 0.14, 10)       # peen
    lat = Vector((-(ky - sy_), kx - sx_, 0))
    if lat.length < 1e-6: lat = Vector((0, 1, 0))
    lat.normalize()
    n0 = len(bm.faces)
    # raised arms: shoulders → elbows high → hands on the helve (pose reads as a swing)
    for sgn in (-1, 1):
        sh = Vector((sx_ + sgn * 0.6 * lat.x, sy_ + sgn * 0.6 * lat.y, tz + 4.55))
        el = Vector((sx_ + sgn * 0.35 * lat.x - 0.15 * dd.x, sy_ + sgn * 0.35 * lat.y - 0.15 * dd.y, tz + 5.35))
        rod(bm, tuple(sh), tuple(el), 0.16, 8)
        rod(bm, tuple(el), tuple(hand + dd * (0.15 if sgn < 0 else 0.55)), 0.14, 8)
    mark(bm, n0, 1)
    obj("D_MAUL", finish(bm, "maul_D", CAST, [WCOAT[0]]), "SUPPORT", part_kind="tool", pose="striking", head_dia_in=5.0)
    st = man(sx_, sy_, math.degrees(math.atan2(ky - sy_, kx - sx_)), z=tz, k=0, role="striker")
    st.name = "D_STAFF_STRIKER"
    man(dx0 + 1.0, dy1 - 1.0, 230, z=dk, k=1)                   # mate on the deck with the drift and bar, watching (behind the 50 mm camera)
    bm = bmesh.new(); rod(bm, (dx0 + 0.5, dy1 - 1.5, dk + 3.6), (dx0 - 0.4, dy1 - 2.3, dk + 4.6), 0.05, 6)
    obj("D_DRIFT_BAR", finish(bm, "drift_D", CAST), "SUPPORT", part_kind="tool")
    man(dx1 + 2.6, dy0 - 1.6, 135, k=5)                        # mate at the ladder foot
    # 4. component stack: columns, girders, sash-bar bundles, gutters, closed glass crates (DM07)
    (cx0, cx1, cy0, cy1) = zinfo["stack_rect"]
    bm = bmesh.new()
    for y in (cy0 + 1.0, cy1 - 1.0): box(bm, cx0, cx0 + 19.0, y - 0.4, y + 0.4, 0.0, 0.6)      # bearers
    n0 = len(bm.faces); rows = [5, 4, 3]; r = 4.0 / 12                                         # 8 in columns
    for li, n in enumerate(rows):
        for k in range(n):
            y = cy0 + 1.0 + r + (k + 0.5 * li) * 2 * r * 1.02 + 0.5; z = 0.6 + r + li * 2 * r * 0.88
            rod(bm, (cx0 + 0.5, y, z), (cx0 + 18.5, y, z), r, 12)
    mark(bm, n0, 1)
    obj("D_STACK_COLUMNS", finish(bm, "stack_columns_D", OAK, [CAST]), "STACKS", part_kind="component_stack", what="columns", n=sum(rows))
    bm = bmesh.new(); gy0 = cy1 - 3.5
    for y in (gy0 - 1.0, gy0 + 1.0): pass
    for x in (cx0 + 2, cx0 + 12, cx0 + 22): box(bm, x - 0.4, x + 0.4, gy0 - 2.5, gy0 + 2.5, 0.0, 0.6)
    gstack = []
    for k in range(3):
        o = obj(f"D_STACK_GIRDER_{k}", gm, "STACKS", (cx0 + 0.3 + 11.76, gy0 - 1.2 + 1.2 * k, 0.6 - zmin + (k == 1) * 3.05), 0.0,
                part_kind="component_stack", what="girder"); gstack.append(o)
    obj("D_STACK_BEARERS", finish(bm, "stack_bearers_D", OAK), "STACKS", part_kind="component_stack", what="bearers")
    bm = bmesh.new()                                          # sash-bar bundles (8 ft) tied in three places
    for b in range(4):
        bx = cx1 - 9.0 + (b % 2) * 0.0; by = cy0 + 1.0 + b * 1.6
        n0 = len(bm.faces); box(bm, bx, bx + 8.0, by - 0.55, by + 0.55, 0.0 + (b // 2) * 0.0, 1.0); mark(bm, n0, 0)
        n0 = len(bm.faces)
        for t in (0.8, 4.0, 7.2): box(bm, bx + t, bx + t + 0.12, by - 0.58, by + 0.58, -0.02, 1.03)
        mark(bm, n0, 1)
    for k in range(3):                                        # Paxton gutters, 24 ft, stacked
        n0 = len(bm.faces); box(bm, cx1 - 26.0, cx1 - 2.0, cy1 - 1.2 - k * 0.0, cy1 - 0.4, 0.6 + k * 0.6, 1.15 + k * 0.6); mark(bm, n0, 2)
    obj("D_STACK_BARS_GUTTERS", finish(bm, "stack_bars_D", TIMBERP, [ROPE, mat("GT_GutterTimber", (0.55, 0.52, 0.46), 0.8)]), "STACKS",
        part_kind="component_stack", what="sash_bars+gutters")
    for k in range(6): muse_crate(cx1 + 2.0, cy0 + 1.0 + k * 3.0 if k < 4 else cy0 + 2.0 + (k - 4) * 3.0, 0 if k < 4 else CRATE_H, math.pi / 2, "_glass")
    man(cx0 + 10, cy0 - 3.0, 90, k=1); man(cx1 + 5, cy0 + 4, 180, k=4)
    # 4b. glass first: a glazier on the gutter lowers a pane box on a line to a man on the floor (separate illustrative beat)
    px, py, pz = zinfo["pane_lower"]
    man(px, py, 180, z=pz, k=5)
    bm = bmesh.new(); box(bm, px - 1.3, px + 1.3, py - 0.5, py + 0.5, 11.0, 13.2)       # pane box (49 x 10 in sheets, edge-on)
    rod(bm, (px, py - 0.6, pz + 3.6), (px, py, 13.2), 0.035, 6)
    obj("D_PANE_BOX_LOWERING", finish(bm, "pane_box_D", CRATEW), "LIFT", part_kind="pane_box", state="lowering")
    man(px + 1.5, py + 2.6, 200, k=2)
    # 5. a timber-wheeled trolley at the stack with two horses' worth of girders goes to Sydenham? no: a cart, held (CP032 is separate)
    tx, ty, trz = zinfo["trolley"]
    # d04: pull the horse clear of the lowered girder in CP031_lateral_end (was half-hidden behind it)
    trolley(tx, ty - 12.0, trz, "columns")
    info["lift"] = {"girder": G.name, "bottom_ft": gz0, "apex_ft": list(APEX)}

# ---------------- cameras from route/camera_route.json (storyboard grammar; no roll) ----------------
CAMS = bpy.data.collections.new("CAMERAS_DISMANTLE"); ROOT.children.link(CAMS)
route = json.load(open(os.path.join(ROOTDIR, "route", "camera_route.json")))
for shot in route["shots"]:
    if STATE not in shot["states"]: continue
    for key in ("start", "end"):
        if key not in shot: continue
        cd = bpy.data.cameras.new(f"{shot['id']}_{key}"); cd.lens = shot["lens_mm"]; cd.sensor_width = 36.0
        cd.clip_start = 0.05; cd.clip_end = 3000
        ob = bpy.data.objects.new(f"{shot['id']}_{key}", cd); CAMS.objects.link(ob)
        ob.location = [ft(v) for v in shot[key]["pos_ft"]]
        d = Vector([ft(v) for v in shot[key]["look_ft"]]) - ob.location
        ob.rotation_euler = d.to_track_quat('-Z', 'Y').to_euler()
        ob["eye_base_ft"] = shot[key].get("eye_base_ft", 0.0); ob["shot"] = shot["id"]
info.update({"crates_muse": len(crates), "packing_cases": len(pcases), "staff": len(staff),
             "collections": {k: len(v.objects) for k, v in SUB.items()}})
scene["grok_dismantle"] = json.dumps(info)
print("DISMANTLE_INFO", json.dumps(info), flush=True)
bpy.ops.wm.save_as_mainfile(filepath=os.path.abspath(OUT), compress=True)
print("SAVED", OUT)
