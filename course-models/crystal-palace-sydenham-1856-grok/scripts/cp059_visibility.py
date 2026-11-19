"""CP059 candidate side-effect finder: ray-cast visibility of the new dated collection from every camera in the round.
usage: blender -b rounds/candidates/sydenham-1936fire-r11b_cp059planting.blend -P scripts/cp059_visibility.py   (prints VIS lines)"""
import bpy
STATE = "SY36_nave_planting_burning__30Nov1936"
sc = bpy.context.scene; dg = bpy.context.evaluated_depsgraph_get()
new = {o.name for o in bpy.data.collections[STATE].all_objects}
NX, NY = 96, 54
for cam in sorted((o for o in bpy.data.objects if o.type == 'CAMERA'), key=lambda o: o.name):
    sc.camera = cam; fr = cam.data.view_frame(scene=sc); M = cam.matrix_world; R = M.to_3x3(); hits = 0
    for j in range(NY):
        for i in range(NX):
            p = fr[2] + (fr[1] - fr[2]) * ((i + 0.5) / NX) + (fr[3] - fr[2]) * ((j + 0.5) / NY)
            if cam.data.type == 'ORTHO':
                o = M @ p; d = R @ __import__('mathutils').Vector((0, 0, -1))
            else:
                o = M.translation; d = (R @ p).normalized()
            ok, loc, n, idx, ob, mx = sc.ray_cast(dg, o, d)
            if ok and ob.name in new: hits += 1
    print(f'VIS {cam.name} {100 * hits / (NX * NY):.2f}')
