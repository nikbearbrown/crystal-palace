"""CANDIDATE: replace crude FOUNTAIN_* lathe with Muse osler-crystal-fountain
(append-with-credit, Muse folders read-only). Sibling only — live o01 untouched.

Uses models-main-ro copy of origin/main models/osler-crystal-fountain
(Wellcome-governed; arcade/pinnacles/water sheets) — beats both our lathe
and the earlier hp-osler-crystal-fountain Ferrier build for hero detail.

  blender -b rounds/o01.blend -P scripts/polish_osler_cand.py -- \
      --out rounds/candidates/o01_osler.blend
"""
import bpy, os, sys
from mathutils import Vector

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
# Read-only extract from origin/main (never edit Muse folders)
MUSE = "/workspace/models-main-ro/models/osler-crystal-fountain/osler-crystal-fountain.blend"

argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
OUT = argv[argv.index("--out") + 1] if "--out" in argv else "rounds/candidates/o01_osler.blend"
out = OUT if os.path.isabs(OUT) else os.path.join(ROOT, OUT)
os.makedirs(os.path.dirname(out), exist_ok=True)

if not bpy.data.filepath:
    bpy.ops.wm.open_mainfile(filepath=os.path.join(ROOT, "rounds/o01.blend"))

# Hide crude lathe fountain body — keep scenic railing
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

# Also clear any prior MUSE_OSLER_* from a previous candidate pass
for o in list(bpy.data.objects):
    if o.name.startswith("MUSE_OSLER_"):
        bpy.data.objects.remove(o, do_unlink=True)
for c in list(bpy.data.collections):
    if c.name.startswith("MUSE_OSLER"):
        bpy.data.collections.remove(c)

before = set(bpy.data.objects.keys())
before_mats = set(bpy.data.materials.keys())

# New Muse blend has objects on the scene root (no Model collection).
# Append all mesh objects by name.
with bpy.data.libraries.load(MUSE, link=False) as (data_from, data_to):
    data_to.objects = list(data_from.objects)

muse_col = bpy.data.collections.get("MUSE_OSLER_FOUNTAIN") or bpy.data.collections.new("MUSE_OSLER_FOUNTAIN")
if muse_col.name not in bpy.context.scene.collection.children:
    bpy.context.scene.collection.children.link(muse_col)

new_objs = [o for o in bpy.data.objects if o.name not in before]
n_tagged = 0
for o in new_objs:
    if o.name.startswith("Softbox") or "Backdrop" in o.name or o.name.startswith("Camera") or o.name.startswith("Light"):
        # skip studio setup if any
        for col in list(o.users_collection):
            col.objects.unlink(o)
        continue
    # link into our credit collection; unlink from scene root duplicates
    for col in list(o.users_collection):
        col.objects.unlink(o)
    muse_col.objects.link(o)
    if not o.name.startswith("MUSE_OSLER_"):
        o.name = "MUSE_OSLER_" + o.name
    o["credit"] = "Muse — osler-crystal-fountain (Wellcome plate; cat. 27 ft)"
    o["source_blend"] = MUSE
    o["part_kind"] = "fountain_muse"
    o["candidate"] = "CP022_osler"
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
    "CANDIDATE CP022 — Osler Crystal Fountain\n"
    "Appended (read-only) from Muse model:\n"
    "  models/osler-crystal-fountain/ (origin/main via models-main-ro)\n"
    "Credit: Muse. Wellcome engraving governs; Official Catalogue 27 ft.\n"
    "Chosen over hp-osler-crystal-fountain for arcade/pinnacles/water sheets.\n"
    "Live FOUNTAIN_* lathe hidden, not deleted. Live o01 untouched.\n"
)

bpy.ops.wm.save_as_mainfile(filepath=out)
print("SAVED", out, "muse_objs", n_tagged, flush=True)
