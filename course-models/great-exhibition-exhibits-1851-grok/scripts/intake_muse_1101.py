"""CANDIDATES from 2026-11-01 reference intake (BUILD-PLAN 'Reference intake 2026-11-01').
Appends Muse packages from origin/main a62ba2e (read-only extract at
/workspace/tmp/muse-main-a62ba2e/models; Muse's folders are never edited).
Opens live rounds/e02.blend, never saves it; writes a candidate .blend only.

  blender -b rounds/e02.blend -P scripts/intake_muse_1101.py -- --mode hammer   --out rounds/candidates/e02_muse_hammer.blend
  blender -b rounds/e02.blend -P scripts/intake_muse_1101.py -- --mode dressing --out rounds/candidates/e02_muse_dressing.blend
"""
import bpy, os, sys, math

HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
MUSE = "/workspace/tmp/muse-main-a62ba2e/models"
argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
def arg(n, d=None): return argv[argv.index(n) + 1] if n in argv else d
MODE = arg("--mode", "hammer"); OUT = arg("--out")
out = OUT if os.path.isabs(OUT) else os.path.join(ROOT, OUT)
os.makedirs(os.path.dirname(out), exist_ok=True)
bpy.ops.wm.open_mainfile(filepath=os.path.join(ROOT, "rounds/e02.blend"))
SKIP = ("GroundPlane", "Ground", "Floor", "Backdrop", "RenderCam", "Camera", "Sun", "Light")

def append_pkg(pkg, coll_name, loc, rot_z=0.0, tag=None):
    path = os.path.join(MUSE, pkg, pkg + ".blend")
    with bpy.data.libraries.load(path, link=False) as (src, dst):
        dst.objects = [n for n in src.objects if not n.startswith(SKIP)]
    coll = bpy.data.collections.new(coll_name); bpy.context.scene.collection.children.link(coll)
    root = bpy.data.objects.new(coll_name + "_ROOT", None); coll.objects.link(root)
    root.location = loc; root.rotation_euler = (0, 0, rot_z)
    n = 0
    for o in dst.objects:
        if o is None or o.type in ("CAMERA", "LIGHT"): continue
        coll.objects.link(o); n += 1
        if o.parent is None:
            o.parent = root
        o["cp_era"] = "HP1851"; o["cp_source"] = f"Muse models/{pkg} @ origin/main a62ba2e"; o["candidate"] = tag
    root["cp_era"] = "HP1851"; root["candidate"] = tag
    print("APPENDED", pkg, n, "objs at", loc, flush=True)
    return coll

credit = bpy.data.texts.new("CREDIT_MUSE_INTAKE_1101")
if MODE == "hammer":
    hc = bpy.data.collections["EXH_NASMYTH_HAMMER"]; hidden = []
    for o in hc.objects:
        if o.name in ("HAM_barrier", "HAM_label"): continue
        o.hide_render = True; o.hide_viewport = True; hidden.append(o.name)
    print("HID_GROK_HAMMER", hidden, flush=True)
    append_pkg("hp-working-machine-exhibit", "EXH_MUSE_NASMYTH_HAMMER", (29.261, 0.0, 0.0), 0.0, "e02_muse_hammer")
    credit.write(
        "CANDIDATE e02_muse_hammer (2026-11-01)\n"
        "Nasmyth steam hammer: Muse, models/hp-working-machine-exhibit (origin/main a62ba2e),\n"
        "appended unmodified (form from Ferrier photo RCIN 2800024; H=5.00 m ASSUMED +-30%).\n"
        "Grok HAM_* hammer hidden (barrier + label kept). Muse Tup static at mid-stroke (no blow cycle).\n"
        "Known: Muse standards built leaning OUTWARD at the top (V) though notes say A-form;\n"
        "rotation sign in build script line ~146. Not corrected here (their package is read-only).\n")
elif MODE == "dressing":
    # Replace grey neighbour block-outs with Muse 1851 machines; press block-out stays.
    for n in ("HPE_nbr_boiler", "HPE_nbr_engine", "HPE_nbr_lathe"):
        o = bpy.data.objects[n]; o.hide_render = True; o.hide_viewport = True
    append_pkg("vacuum-sugar-apparatus", "MC_MUSE_VACUUM_SUGAR", (19.51, -2.44, 0.0), 0.0, "e02_muse_dressing")
    append_pkg("portable-steam-engine", "MC_MUSE_PORTABLE_ENGINE", (37.19, -4.27, 0.0), math.radians(200), "e02_muse_dressing")
    append_pkg("seed-drill", "MC_MUSE_SEED_DRILL", (38.4, 3.05, 0.0), math.radians(90), "e02_muse_dressing")
    credit.write(
        "CANDIDATE e02_muse_dressing (2026-11-01)\n"
        "Machinery Court dressing, all by Muse (origin/main a62ba2e), appended unmodified:\n"
        " vacuum-sugar-apparatus (Talbot 1851 photo) at old boiler block-out (19.51,-2.44)\n"
        " portable-steam-engine (Garrett) at old engine block-out (37.19,-4.27)\n"
        " seed-drill (Talbot plates) at old lathe block-out (38.4,3.05)\n"
        "HPE_nbr_boiler/engine/lathe hidden; HPE_nbr_press kept.\n"
        "Departure: 1851 portable engines + seed drills stood in the agricultural implements\n"
        "area (Class IX), not the machinery-in-motion court; placed here as dressing only.\n")
else:
    raise SystemExit("bad mode")
bpy.ops.wm.save_as_mainfile(filepath=out)
print("SAVED", out, flush=True)
