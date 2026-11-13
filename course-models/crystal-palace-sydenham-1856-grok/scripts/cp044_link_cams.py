"""Before-side helper (CP044 candidate, 2026-11-13): link the candidate's CP044 cameras into the open LIVE round
under a temporary name (in memory only, never saved), so the live geometry can be rendered from the new viewpoints.
usage: blender -b rounds/sydenham-1856-r16.blend -P scripts/cp044_link_cams.py -P scripts/render.py -- ..."""
import bpy, os
CAND = os.path.abspath('rounds/candidates/sydenham-1856-r16_cp044gate.blend')
names = ['CAM_CP044_pay_desks_35mm', 'CAM_CP044_maintenance_50mm']
for n in names:
    o = bpy.data.objects.get(n)
    if o: o.name = n + '__live'
with bpy.data.libraries.load(CAND, link=False) as (src, dst):
    dst.objects = [n for n in names]
for o in dst.objects:
    bpy.context.scene.collection.objects.link(o)
    print('CP044_LINKED_CAM', o.name, tuple(round(v / 0.3048, 2) for v in o.location))
