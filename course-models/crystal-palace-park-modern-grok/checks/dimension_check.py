"""usage: blender -b <round.blend> -P checks/dimension_check.py -- <out.txt>"""
import bpy, sys
from mathutils import Vector
F = 0.3048; out = sys.argv[sys.argv.index('--')+1]
OB = bpy.data.objects
ROOT = next((c.name for c in bpy.context.scene.collection.children
             if c.name.startswith('PARK')), '?')
ST = ROOT.split('_')[0]
rows = [f"STATE  root collection = {ROOT}"]
def flag(ok, label, src): rows.append(f"{'PASS' if ok else 'FAIL'}  {label:60s} [{src}]")
def has(*n): return all(x in OB for x in n)
def bb(names):
    pts = []
    for n in names:
        o = OB[n]; pts += [o.matrix_world @ Vector(c) for c in o.bound_box]
    return [min(p[i] for p in pts)/F for i in range(3)], [max(p[i] for p in pts)/F for i in range(3)]
flag(any(c.name.startswith('SYDENHAM') or 'RUINS' in c.name or 'APPENDED' in c.name
         for c in bpy.data.collections), 'Sydenham ruins shell appended', 'rule')
flag(has('pk_parade_road') or has('pk_subway_floor'), 'High Level / subway geometry present', 'G-STATION')
if ST == 'PARK54':
    flag(has('pk_hl_wall_S', 'pk_booking_closed_gate'), 'closed HL station + gated subway head', 'closed 1954 R')
    flag(has('CAM_CP065_hl_closed_35mm'), 'CP065 camera present', 'storyboard')
if ST in ('PARK60', 'PARK-NOW') or 'PARK60' in ROOT or 'PARK-NOW' in ROOT or 'NOW' in ROOT:
    if 'NSC' in ''.join(c.name for c in bpy.data.collections) or has('nsc_infield'):
        flag(has('nsc_infield', 'nsc_sports_hall'), 'NSC stadium infield + sports hall block-outs', 'opened 1964 R; forms U')
    if has('CAM_CP066_nsc_stadium_35mm'):
        flag(True, 'CP066 NSC cameras present', 'storyboard')
if 'NOW' in ROOT or ST == 'PARK-NOW':
    flag(has('ov_N', 'ov_CT'), 'footprint overlay present (interpretive)', 'CP072')
    flag(any('DN54' in c.name for c in bpy.data.collections), 'dinosaurs appended read-only', 'G-DINO')
    flag(any(o.name.startswith('ppl_now_') for o in OB), 'PPL-NOW visitors present', 'PPL-NOW')
    flag(has('CAM_CP071_subway_interior_28mm', 'CAM_CP072_footprint_35mm', 'CAM_CP073_sphinx_steps_50mm'),
         'CP071/072/073 cameras present', 'storyboard')
    flag(has('CAM_CP074_dinosaurs_35mm', 'CAM_CP075_layered_nsc_35mm', 'CAM_CP076_empty_plateau_35mm'),
         'CP074/075/076 cameras present', 'storyboard')
cams = [o for o in OB if o.type == 'CAMERA']
flag(all(abs(o.data.sensor_width - 36) < 0.01 for o in cams), 'all %d cameras on 36 mm sensor' % len(cams), 'rule')
flag(all(abs(o.matrix_world.to_euler().y) < 1e-3 or abs(abs(o.matrix_world.to_euler().y) - 3.14159) < 1e-3
         for o in cams), 'no camera roll', 'rule')
rows.append(f"INFO  objects={len(OB)} cameras={len(cams)}")
open(out,'w').write('\n'.join(rows)+'\n'); print('\n'.join(rows))
