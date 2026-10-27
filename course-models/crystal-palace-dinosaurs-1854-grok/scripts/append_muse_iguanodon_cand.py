"""Append Muse models/iguanodon (read-only) as recumbent; Muse mould for studio.
Never edits Muse folders. Credits in object custom props + NOTES.
Updates rounds/dinosaurs-1854-r04-cand.blend in place.
"""
import bpy, math, os
from mathutils import Vector, Matrix

CAND = '/workspace/crystal-palace-dinosaurs/course-models/crystal-palace-dinosaurs-1854-grok/rounds/dinosaurs-1854-r04-cand.blend'
MUSE_IG = '/workspace/models-main-ro/models/iguanodon/iguanodon.blend'
MUSE_MOULD = '/workspace/models-main-ro/models/hawkins-mould-and-table/hawkins-mould-and-table.blend'

SKIP_IG = {'GroundBase', 'Camera', 'Light', 'Sun', 'Floor'}  # keep Trunk — pose needs it
# RenderSetup ground from mould package
SKIP_MOULD = {'RS_Ground'}

def credit(ob, src):
    ob['credit'] = src
    ob['candidate'] = 'r04_cand'
    if ob.data and hasattr(ob.data, 'materials'):
        pass

def append_objects(blend, names=None, skip=None):
    skip = skip or set()
    with bpy.data.libraries.load(blend, link=False) as (df, dt):
        if names is None:
            dt.objects = [n for n in df.objects if n not in skip]
        else:
            dt.objects = [n for n in names if n in df.objects]
    out = []
    for o in dt.objects:
        if o is None: continue
        bpy.context.collection.objects.link(o)
        out.append(o)
    return out

def join_named(name, objs, mat_fallback=None):
    bpy.ops.object.select_all(action='DESELECT')
    keep = [o for o in objs if o.type == 'MESH']
    if not keep: return None
    for o in keep:
        o.select_set(True)
    bpy.context.view_layer.objects.active = keep[0]
    bpy.ops.object.join()
    ob = bpy.context.view_layer.objects.active
    ob.name = name
    if ob.data: ob.data.name = name
    return ob

def replace_scene_obj(scene_name, new_ob, scale_to_old=True, z_mode='preserve'):
    old = bpy.data.objects.get(scene_name)
    if not old:
        print('no scene obj', scene_name); return
    old_loc = old.location.copy()
    old_rot = old.rotation_euler.copy()
    old_dim = old.dimensions.copy()
    col = old.users_collection[0] if old.users_collection else bpy.context.collection
    # unlink old
    for c in list(old.users_collection):
        c.objects.unlink(old)
    bpy.data.objects.remove(old, do_unlink=True)
    # place new
    for c in list(new_ob.users_collection):
        c.objects.unlink(new_ob)
    col.objects.link(new_ob)
    new_ob.name = scene_name
    if new_ob.data: new_ob.data.name = scene_name + '_muse'
    new_ob.location = old_loc
    new_ob.rotation_euler = old_rot
    new_ob.scale = (1, 1, 1)
    bpy.context.view_layer.update()
    if scale_to_old and new_ob.dimensions.x > 1e-3:
        # match plan length primarily
        s = old_dim.x / new_ob.dimensions.x
        # Muse recumbent is ~9.3m; old was ~10.9 — slight scale OK
        new_ob.scale = (s, s, s)
        bpy.ops.object.select_all(action='DESELECT')
        new_ob.select_set(True); bpy.context.view_layer.objects.active = new_ob
        bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    bpy.context.view_layer.update()
    print(f'replaced {scene_name} with Muse append dim={[round(v,2) for v in new_ob.dimensions]} loc={[round(v,2) for v in new_ob.location]}')

def main():
    bpy.ops.wm.open_mainfile(filepath=CAND)
    # --- Muse Iguanodon (recumbent / foreground sprawled) ---
    ig_parts = append_objects(MUSE_IG, skip=SKIP_IG | {'GroundBase'})
    # drop cameras/lights if any slipped in
    ig_parts = [o for o in ig_parts if o.type == 'MESH']
    for o in ig_parts:
        credit(o, 'models/iguanodon (Muse, main) — CC BY-SA photo ref; append-only')
    # Exclude GroundBase already; Trunk stays
    joined = join_named('_muse_iguanodon_tmp', ig_parts)
    if joined:
        credit(joined, 'models/iguanodon (Muse, main) — append-only, not edited')
        replace_scene_obj('iguanodon_recumbent', joined, scale_to_old=True)
    # --- Muse mould for studio (replace crude mould) ---
    mould_parts = append_objects(MUSE_MOULD, skip=SKIP_MOULD)
    mould_parts = [o for o in mould_parts if o.type == 'MESH' and (
        o.name.startswith('Mould_') or o.name.startswith('Table_'))]
    # Prefer just the mould body for iguanodon_mould_open (dinner set already has table/guests)
    mould_only = [o for o in mould_parts if o.name.startswith('Mould_')]
    # unlink table extras we don't need for mould_open stand-in
    for o in mould_parts:
        if o not in mould_only:
            bpy.data.objects.remove(o, do_unlink=True)
    for o in mould_only:
        credit(o, 'models/hawkins-mould-and-table (Muse, main) — append-only')
    if mould_only:
        mjoin = join_named('_muse_mould_tmp', mould_only)
        if mjoin:
            credit(mjoin, 'models/hawkins-mould-and-table (Muse, main) — append-only')
            # studio mould sits at ~914,0,1.22 — replace
            replace_scene_obj('iguanodon_mould_open', mjoin, scale_to_old=True)
    # ensure res
    sc = bpy.context.scene
    sc.render.resolution_x = 1920
    sc.render.resolution_y = 1080
    sc.render.resolution_percentage = 100
    bpy.ops.wm.save_as_mainfile(filepath=CAND)
    print('updated CANDIDATE', CAND)

if __name__ == '__main__':
    main()
