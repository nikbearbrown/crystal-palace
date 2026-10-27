"""usage: blender -b <round.blend> -P checks/dimension_check.py -- <out.txt>
Measures world-space bounds of named objects and compares with guide (1856) figures, feet."""
import bpy, sys
from mathutils import Vector
F = 0.3048; out = sys.argv[sys.argv.index('--')+1]
def bb(names):
    pts = []
    for n in names:
        o = bpy.data.objects[n]; pts += [o.matrix_world @ Vector(c) for c in o.bound_box]
    return [min(p[i] for p in pts)/F for i in range(3)], [max(p[i] for p in pts)/F for i in range(3)]
rows = []
def chk(label, val, target, tol, src):
    ok = abs(val-target) <= tol; rows.append(f"{'PASS' if ok else 'FAIL'}  {label:46s} model {val:8.2f} ft  target {target:8.2f} ft  tol {tol}  [{src}]")
lo, hi = bb(['main_floor']); chk('main building length (end walls)', hi[0]-lo[0], 1608, 1, 'guide p.35 B')
chk('general width', hi[1]-lo[1], 312, 1, 'guide p.35 B')
lo, hi = bb(['central_transept_vault_glass']); chk('greatest width (central transept N-S extent)', hi[1]-lo[1], 384, 1, 'guide p.35 B')
chk('central transept crown above main floor', hi[2], 174.25, 0.5, "guide p.35 B 174'3\"")
chk('central transept span', hi[0]-lo[0], 120, 1, 'common figure; plan reads 104 inner lines (U)')
lo, hi = bb(['nave_vault_glass']); chk('nave crown above main floor', hi[2], 110.25, 0.5, "guide p.35 B 110'3\"")
chk('nave span', hi[1]-lo[1], 72, 0.5, 'section 0212 R')
lo, hi = bb(['basement_brick']); chk('basement depth below main floor', -lo[2], 23.58, 0.3, "guide p.35 B 197'10\"-174'3\"")
for w in ('south','north'):
    lo, hi = bb([f'{w}_transept_vault_glass']); chk(f'{w} transept centre x (plan 0205)', (lo[0]+hi[0])/2, -528 if w=='south' else 528, 8, 'plan 0205 R: -529/+523')
lo, hi = bb(['wings_glass']); chk('wing length (N-S direction, each)', hi[1]-lo[1], 574, 1, 'guide p.35 B')
lo, hi = bb(['colonnade_roof']); chk('railway colonnade length', hi[1]-lo[1], 720, 1, 'guide p.35 B')
gal = bpy.data.objects['gallery_floors']; 
area = sum(p.area for p in gal.data.polygons if p.normal.z > 0.9)/(F*F)
rows.append(f"INFO  gallery floor area modelled {area:,.0f} sq ft vs guide 261,568 sq ft (B) -> {area/261568:.0%}; remainder = galleries not yet modelled (outer tiers, transept galleries)")
open(out,'w').write('\n'.join(rows)+'\n'); print('\n'.join(rows))
