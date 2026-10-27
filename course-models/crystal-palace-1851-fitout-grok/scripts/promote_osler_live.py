"""KEEP: promote Muse osler-crystal-fountain into a live blend (fitout o01 / transept).
Hides FOUNTAIN_GLASS/PRISMS/JET/CURB/WATER; appends Muse with credit. Never edits Muse folders.
  blender -b rounds/o01.blend -P scripts/promote_osler_live.py
  blender -b /path/to/r11.blend -P /path/to/promote_osler_live.py -- --in-place
"""
import bpy, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
MUSE = "/workspace/models-main-ro/models/osler-crystal-fountain/osler-crystal-fountain.blend"

argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
# default: overwrite the opened file in place
OUT = None
if "--out" in argv:
    OUT = argv[argv.index("--out") + 1]
    if not os.path.isabs(OUT):
        OUT = os.path.join(ROOT, OUT)

if not bpy.data.filepath and "--out" not in argv:
    bpy.ops.wm.open_mainfile(filepath=os.path.join(ROOT, "rounds/o01.blend"))

HIDE = ("FOUNTAIN_GLASS", "FOUNTAIN_PRISMS", "FOUNTAIN_JET",
        "FOUNTAIN_CURB", "FOUNTAIN_WATER")
for n in HIDE:
    o = bpy.data.objects.get(n)
    if o:
        o.hide_render = True
        o.hide_viewport = True
        try:
            o.hide_set(True)
        except Exception:
            pass

for o in list(bpy.data.objects):
    if o.name.startswith("MUSE_OSLER_"):
        bpy.data.objects.remove(o, do_unlink=True)
for c in list(bpy.data.collections):
    if c.name.startswith("MUSE_OSLER"):
        bpy.data.collections.remove(c)

before = set(bpy.data.objects.keys())
before_mats = set(bpy.data.materials.keys())
with bpy.data.libraries.load(MUSE, link=False) as (data_from, data_to):
    data_to.objects = list(data_from.objects)

muse_col = bpy.data.collections.get("MUSE_OSLER_FOUNTAIN") or bpy.data.collections.new("MUSE_OSLER_FOUNTAIN")
if muse_col.name not in bpy.context.scene.collection.children:
    bpy.context.scene.collection.children.link(muse_col)

n_tagged = 0
for o in [o for o in bpy.data.objects if o.name not in before]:
    if o.name.startswith("Softbox") or "Backdrop" in o.name or o.name.startswith("Camera") or o.name.startswith("Light"):
        for col in list(o.users_collection):
            col.objects.unlink(o)
        continue
    for col in list(o.users_collection):
        col.objects.unlink(o)
    muse_col.objects.link(o)
    if not o.name.startswith("MUSE_OSLER_"):
        o.name = "MUSE_OSLER_" + o.name
    o["credit"] = "Muse — osler-crystal-fountain (Wellcome plate; cat. 27 ft)"
    o["source_blend"] = MUSE
    o["part_kind"] = "fountain_muse"
    o["keep"] = "CP022_osler"
    if "candidate" in o:
        del o["candidate"]
    o.hide_render = False
    o.hide_viewport = False
    try:
        o.hide_set(False)
    except Exception:
        pass
    n_tagged += 1

for m in list(bpy.data.materials):
    if m.name in before_mats:
        continue
    if not m.name.startswith("MUSE_OSLER_"):
        m.name = "MUSE_OSLER_" + m.name

txt = bpy.data.texts.get("CREDIT_MUSE_OSLER") or bpy.data.texts.new("CREDIT_MUSE_OSLER")
txt.clear()
txt.write(
    "KEEP CP021/CP022/CP023 — Osler Crystal Fountain (live)\n"
    "Appended (read-only) from Muse model:\n"
    "  models/osler-crystal-fountain/ (origin/main via models-main-ro)\n"
    "Credit: Muse. Wellcome engraving governs; Official Catalogue 27 ft.\n"
    "Chosen over hp-osler-crystal-fountain for arcade/pinnacles/water sheets.\n"
    "Live FOUNTAIN_* lathe hidden, not deleted.\n"
)

dest = OUT or bpy.data.filepath
bpy.ops.wm.save_as_mainfile(filepath=dest)
print("PROMOTED", dest, "muse_objs", n_tagged, flush=True)
