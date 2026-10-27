"""usage: blender -b <round.blend> -P checks/dimension_check.py -- <out.txt>
D-checks for the Hawkins sculptures (local mesh extents, feet) against published statue sizes; counts against the listing."""
import bpy, sys
F = 0.3048; out = sys.argv[sys.argv.index('--') + 1]; OB = bpy.data.objects; rows = []
def ext(n):
    o = OB[n]; vs = [v.co for v in o.data.vertices]; s = o.scale
    return [(max(v[i] for v in vs) - min(v[i] for v in vs)) * s[i] / F for i in range(3)], max(v.z for v in vs) * s[2] / F + o.location.z / F
def ground_under(n):
    o = OB[n]; t = OB['terrain_lake_islands_1854']; x, y = o.location.x, o.location.y
    near = [v.co.z for v in t.data.vertices if abs(v.co.x - x) < 1.3 and abs(v.co.y - y) < 1.3]
    return (sum(near) / len(near)) / F if near else 0.0
def chk(label, val, target, tol, src):
    rows.append(f"{'PASS' if abs(val - target) <= tol else 'FAIL'}  {label:52s} model {val:7.2f} ft  target {target:7.2f} ft  tol {tol}  [{src}]")
def flag(ok, label, src): rows.append(f"{'PASS' if ok else 'FAIL'}  {label:72s} [{src}]")
(L, W, H), top = ext('iguanodon_standing'); g = ground_under('iguanodon_standing')
chk('Iguanodon (standing) statue length', L, 32.8, 3.3, 'cpdinosaurs.org: 10 m R')
chk('Iguanodon (standing) height above ground', top - g, 8.86, 1.0, 'cpdinosaurs.org: 2.7 m R')
(L, W, H), top = ext('megalosaurus'); g = ground_under('megalosaurus')
chk('Megalosaurus statue length', L, 32.8, 3.3, 'Historic England: 10 m R')
chk('Megalosaurus height above ground', top - g, 11.48, 1.0, 'Historic England: 3.5 m R')
(L, W, H), top = ext('megatherium'); g = ground_under('megatherium')
flag(top - g <= 19.7, f'Megatherium upright height {top - g:.1f} ft <= 6 m (19.7 ft)', 'ArtUK/cpdinosaurs: up to 6 m R; statue height I')
flag('megatherium_tree' in OB, 'Megatherium clasps a tree', 'cpdinosaurs/ArtUK R')
(L, W, H), _ = ext('hylaeosaurus'); rows.append(f"INFO  Hylaeosaurus length {L:.1f} ft ({L*F:.1f} m); animal ~5 m (cpdinosaurs R), statue size I")
(L, W, H), _ = ext('irish_elk_stag'); rows.append(f"INFO  Irish elk stag antler span {W:.1f} ft ({W*F:.1f} m); Megaloceros spans to 3.6 m (R, animal)")
def n(prefix): return sum(1 for o in OB if o.type == 'MESH' and o.name.startswith(prefix) and 'mould' not in o.name and 'tree' not in o.name)
for p, k, src in [('iguanodon_', 2, 'NHM/cpdinosaurs: two Iguanodons R'), ('ichthyosaur_', 3, 'cpdinosaurs: three Ichthyosaurs R'), ('plesiosaur_', 3, 'cpdinosaurs: three Plesiosaurs R'),
                  ('irish_elk_', 4, 'Hawkins built four Megaloceros, 2 stags + 2 does (1854) R'), ('megalosaurus', 1, 'R'), ('hylaeosaurus', 1, 'R'), ('megatherium', 1, 'R')]:
    chk(f'count {p.rstrip("_")}', n(p), k, 0, src)
for nm, ref in [('iguanodon_standing', 'nose horn (Owen/Hawkins misplaced thumb spike) R')]:
    o = OB[nm]; flag(max(v.co.z for v in o.data.vertices) / F > 8.0, 'Iguanodon carries the 1854 nose horn / highest point near the snout', ref)
open(out, 'w').write('\n'.join(rows) + '\n'); print('\n'.join(rows))
