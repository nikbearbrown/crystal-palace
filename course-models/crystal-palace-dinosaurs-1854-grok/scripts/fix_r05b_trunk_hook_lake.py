"""Second-pass CP043b fixes on r05b-cand / live r05:
- Delete parkland tree trunk verts crowding Muse head (brown diagonal)
- Delete shore-rock verts that form the floating left-edge hook in CP043b
- Reframe: closer, waterline clearly behind body, less empty grass
"""
import bpy, math, bmesh
from mathutils import Vector
from bpy_extras.object_utils import world_to_camera_view

BASE = '/workspace/crystal-palace-dinosaurs/course-models/crystal-palace-dinosaurs-1854-grok'
for path in (
    f'{BASE}/rounds/dinosaurs-1854-r05b-cand.blend',
    f'{BASE}/rounds/dinosaurs-1854-r05.blend',
):
    bpy.ops.wm.open_mainfile(filepath=path)
    sc = bpy.context.scene
    cam = bpy.data.objects['CAM_CP043b_iguanodons_detail_50mm']
    ig = bpy.data.objects['iguanodon_recumbent']
    # Approx head world position (Muse nose toward +X after -25 heading)
    head = ig.matrix_world @ Vector((4.5, 0.0, 2.2))
    print('head approx', [round(v,2) for v in head])

    def delete_verts_near(obj_name, centre, radius, also_require_ndc_left=False, ndc_xmax=0.12):
        o = bpy.data.objects.get(obj_name)
        if not o: return 0
        bm = bmesh.new(); bm.from_mesh(o.data)
        bm.verts.ensure_lookup_table()
        kill = []
        for v in bm.verts:
            w = o.matrix_world @ v.co
            if (w - centre).length > radius:
                continue
            if also_require_ndc_left:
                ndc = world_to_camera_view(sc, cam, w)
                if ndc.z <= 0 or ndc.x > ndc_xmax:
                    continue
            kill.append(v)
        n = len(kill)
        if n:
            bmesh.ops.delete(bm, geom=kill, context='VERTS')
            bm.to_mesh(o.data); o.data.update()
        bm.free()
        print(f'  {obj_name}: deleted {n} verts near target')
        return n

    # Brown diagonal = parkland bark trunk behind head
    delete_verts_near('trees_parkland_and_young_island_planting', head, radius=3.2)
    # Also clear any megatherium_tree intrusion (far but check)
    delete_verts_near('megatherium_tree', head, radius=2.5)

    # Floating grey hook at far left: shore rocks that land in left strip of CP043b
    o = bpy.data.objects.get('shore_rocks_and_bases')
    if o:
        bm = bmesh.new(); bm.from_mesh(o.data)
        kill = []
        for v in bm.verts:
            w = o.matrix_world @ v.co
            ndc = world_to_camera_view(sc, cam, w)
            # left edge strip of current CP043b, mid height, not far water
            if ndc.z <= 0 or ndc.z > 55: continue
            if ndc.x < 0.10 and 0.25 < ndc.y < 0.65:
                kill.append(v)
        n = len(kill)
        if n:
            bmesh.ops.delete(bm, geom=kill, context='VERTS')
            bm.to_mesh(o.data); o.data.update()
        bm.free()
        print(f'  shore_rocks left-hook verts deleted: {n}')

    # Also push plesiosaur_3 further out of any left/centre contamination
    p3 = bpy.data.objects.get('plesiosaur_3')
    if p3:
        p3.location.x = min(p3.location.x, 24.0)  # keep away from 043b left
        # actually move further into -X water away from cam left
        p3.location = Vector((22.0, -22.0, -0.9))
        print('  plesiosaur_3 ->', list(p3.location))

    # Reframe for lake behind + filled frame, less grass
    tc = ig.location + Vector((0.0, 0.0, 1.15))
    # From N of animal, closer, looking S past body into lake (aim at water surface y~-8)
    cam.location = Vector((tc.x - 3.0, tc.y + 11.5, 1.55))
    aim = Vector((tc.x + 1.0, -8.0, 0.15))  # water beyond animal
    cam.rotation_euler = (aim - cam.location).to_track_quat('-Z', 'Y').to_euler()
    cam.data.lens = 50.0
    cam.data.shift_x = 0.0
    cam.data.shift_y = -0.05  # lift subject, crop empty grass
    print('CP043b', [round(v,2) for v in cam.location], 'aim', [round(v,2) for v in aim])

    # Verify lake in frustum behind
    lw = bpy.data.objects['lake_water']
    sample = lw.matrix_world @ Vector((18, -10, 0))
    ndc = world_to_camera_view(sc, cam, sample)
    print('  lake sample ndc', round(ndc.x,2), round(ndc.y,2), round(ndc.z,1))

    bpy.ops.wm.save_as_mainfile(filepath=path)
    print('saved', path)
