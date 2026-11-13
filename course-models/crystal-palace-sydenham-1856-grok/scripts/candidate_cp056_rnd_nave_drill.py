"""CP056 CANDIDATE (2026-11-13): SY-WAR 1915 — the nave as the Royal Naval Division depot's wet-weather drill floor.

usage: blender -b rounds/sydenham-war-r14.blend -P scripts/candidate_cp056_rnd_nave_drill.py [-- out.blend]
       (env CP056_NOSAVE=1: build in memory only)
Opens the live WAR round (never writes it), adds dated collection SY15_rnd_depot_nave_drill_mess__1915 and hides
(never deletes) the nave planting/statuary placeholders. Removes only the 160 r14 nave cone-squad points from
ppl15_rnd_ratings (terrace/lower-terrace points untouched). Cameras are NOT moved.
Sources (DEPARTURES D-SY-CP056-01..):
  * 'Hygienic Conditions at the Crystal Palace', The Hospital, 1915 (PMC5229154): 'The ground floor, cleared of its
    statuary, goods stalls, and other impedimenta, is used for drill, instruction classes, etc. ... other chambers for
    taking meals are provided by screening off wide spaces on the outskirts of the vast nave'.
  * The Southern Reporter, 25 Nov 1915 (quoted royalnavaldivision.info/crystalpalace.htm): 'In wet weather 10,000 men can
    be drilled and physically trained on the main floor'; RND men formed into squads of twenty to thirty, each under a
    Petty Officer assisted by a Leading Seaman.
  * Rev. John Carter, 'H.M.S. Crystal Palace', Wesleyan Magazine 1916: 'all the men begin their service in blue-jacket
    uniform'; 'take their meals in mess decks'.
  * Plan/params: nave 72 ft between column lines y = +-36, bays 24 ft (params.py, R); main floor z = 0.
No rifles, drill equipment or totals are shown (storyboard CP056 flag). Units: feet (F converts).
"""
import bpy, bmesh, math, sys, os, random
from mathutils import Vector, Matrix

F = 0.3048
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import params as P
from cpl_people import person_mesh

argv = sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else []
OUT = '--nosave' if os.environ.get('CP056_NOSAVE') else (argv[0] if argv and argv[0].endswith('.blend') else 'rounds/candidates/sydenham-war-r14_cp056rnd.blend')
STATE = 'SY-WAR_1915'
RNG = random.Random(1915)
BAY = P.BAY                                  # 24 ft (R)
NY = P.NAVE_SPAN / 2                         # nave column lines y = +-36 (R)

COLL = 'SY15_rnd_depot_nave_drill_mess__1915'
col = bpy.data.collections.get(COLL) or bpy.data.collections.new(COLL)
if col.name not in [c.name for c in bpy.context.scene.collection.children]:
    bpy.context.scene.collection.children.link(col)
col['cp_state'] = STATE
col['evidence'] = 'The Hospital 1915 (floor cleared, drill, screened mess spaces) R; Southern Reporter 25 Nov 1915 (wet-weather drill on main floor, squads 20-30 + PO + LS) R; layout/sizes I'

def mat(name, rgb, rough=0.7, metal=0.0):
    m = bpy.data.materials.get(name)
    if m: return m
    m = bpy.data.materials.new(name); m.use_nodes = True
    b = m.node_tree.nodes.get('Principled BSDF')
    b.inputs['Base Color'].default_value = (*rgb, 1); b.inputs['Roughness'].default_value = rough; b.inputs['Metallic'].default_value = metal
    return m
M = dict(
    canvas=mat('cp056_screen_canvas', (0.50, 0.46, 0.37), 0.9),      # unbleached canvas on the screens (I)
    frame=mat('cp056_screen_deal_frame', (0.30, 0.22, 0.13), 0.8),    # stained deal framing (I)
    table=mat('cp056_mess_deal_scrubbed', (0.55, 0.47, 0.34), 0.85),  # scrubbed deal mess tables / forms (I)
    trestle=mat('cp056_mess_trestle', (0.26, 0.19, 0.11), 0.85),
    enamel=mat('cp056_mess_enamel_white', (0.78, 0.78, 0.74), 0.35),
)

class MB:
    def __init__(self, name, m):
        self.name, self.bm, self.m = name, bmesh.new(), m
    def box(self, x0, x1, y0, y1, z0, z1):
        r = bmesh.ops.create_cube(self.bm, size=1.0)
        T = Matrix.Translation(Vector(((x0+x1)/2, (y0+y1)/2, (z0+z1)/2)) * F) @ Matrix.Diagonal(Vector((abs(x1-x0)*F, abs(y1-y0)*F, abs(z1-z0)*F, 1)))
        bmesh.ops.transform(self.bm, matrix=T, verts=r['verts'])
    def cyl(self, x, y, z0, z1, r, seg=8):
        res = bmesh.ops.create_cone(self.bm, cap_ends=True, segments=seg, radius1=r*F, radius2=r*F, depth=(z1-z0)*F)
        bmesh.ops.transform(self.bm, matrix=Matrix.Translation(Vector((x, y, (z0+z1)/2)) * F), verts=res['verts'])
    def done(self):
        me = bpy.data.meshes.new(self.name); self.bm.to_mesh(me); self.bm.free()
        me.materials.append(self.m)
        o = bpy.data.objects.new(self.name, me); col.objects.link(o); o['cp_state'] = STATE; return o

# ------------------------------------------------------------------ 0. floor cleared: hide nave planting + statuary placeholders (kept in file)
HIDDEN = []
for o in bpy.data.objects:
    if o.name.startswith(('PLACEHOLDER_nave_tree_', 'PLACEHOLDER_nave_palm_')) or o.name in ('PLACEHOLDER_nave_statues', 'PLACEHOLDER_nave_tubs'):
        o.hide_render = True; o.hide_viewport = True; o['cp056_hidden_by_candidate'] = True; HIDDEN.append(o.name)
print('CP056 hidden', len(HIDDEN))

# ------------------------------------------------------------------ 1. remove the r14 nave cone squads (z = 0 points inside the nave) from ppl15_rnd_ratings
pp = bpy.data.objects['ppl15_rnd_ratings']
me = pp.data.copy(); me.name = 'ppl15_rnd_ratings_cp056'; pp.data = me
bm = bmesh.new(); bm.from_mesh(me)
mw = pp.matrix_world
dead = [v for v in bm.verts if abs((mw @ v.co).z / F) < 0.5 and abs((mw @ v.co).y / F) < NY and -480 < (mw @ v.co).x / F < -40]
bmesh.ops.delete(bm, geom=dead, context='VERTS'); bm.to_mesh(me); bm.free(); me.update()
pp['cp056_removed_nave_points'] = len(dead)
print('CP056 removed nave cone points', len(dead), 'left', len(me.vertices))

# ------------------------------------------------------------------ 2. squads: people_lib v3.4 1890s_sailor baked meshes (blue-jacket rig, Carter 1916)
NPEOPLE = [0]
def put(name, pose, x, y, face, seed, z=0.0):
    person_mesh(name, '1890s_sailor', style={'role': '1890s_sailor', 'pose': pose, 'lod': 'mid', 'era': '1910s'}, seed=seed)
    o = bpy.data.objects[name]
    for c in list(o.users_collection): c.objects.unlink(o)
    col.objects.link(o)
    o.location = (x * F, y * F, z * F)
    o.rotation_euler = (0, 0, math.atan2(face[0], -face[1]))   # base meshes face local -Y
    o['cp_state'] = STATE; o['cpl_people'] = 'cpl_people_v3'; NPEOPLE[0] += 1
    return o

FILE_W, RANK_D = 2.25, 3.5   # I: ~27 in frontage per man, ranks ~3.5 ft centre to centre (close order)
def squad_line(tag, cx, cy, face, files=12, ranks=2, seed=0):
    """halted squad in line (2 ranks x 12 files = 24, within the 20-30 R), PO 9 ft out front facing it, LS on the right flank"""
    fx, fy = face; rx, ry = -fy, fx          # rank direction (perpendicular to facing)
    for r in range(ranks):
        for k in range(files):
            s = (k - (files - 1) / 2) * FILE_W; b = -r * RANK_D
            put(f'cp056_{tag}_r{r}f{k:02d}', 'standing', cx + rx*s + fx*b + RNG.uniform(-0.12, 0.12), cy + ry*s + fy*b + RNG.uniform(-0.12, 0.12), face, seed + r*files + k)
    put(f'cp056_{tag}_PO', 'pointing', cx + fx*9, cy + fy*9, (-fx, -fy), seed + 90)
    s = ((files - 1) / 2 + 1.3) * FILE_W
    put(f'cp056_{tag}_LS', 'standing', cx + rx*s, cy + ry*s, face, seed + 91)
def squad_column(tag, cx, cy, face, rows=8, seed=0):
    """squad marching in column of threes (3 x 8 = 24 R range), PO alongside, LS at the rear"""
    fx, fy = face; rx, ry = -fy, fx
    for r in range(rows):
        for k in range(3):
            s = (k - 1) * FILE_W; b = -r * 3.0
            put(f'cp056_{tag}_r{r}f{k}', 'walking', cx + rx*s + fx*b + RNG.uniform(-0.15, 0.15), cy + ry*s + fy*b + RNG.uniform(-0.2, 0.2), face, seed + r*3 + k)
    put(f'cp056_{tag}_PO', 'walking', cx + rx*(-4.5) + fx*(-6), cy + ry*(-4.5) + fy*(-6), face, seed + 90)
    put(f'cp056_{tag}_LS', 'walking', cx + fx*(-rows*3.0 - 1), cy + fy*(-rows*3.0 - 1), face, seed + 91)

# west nave drill floor x -300..-70, y -30..30 (nearest man ~85 ft from the gallery camera at (-340, 38, 28); figures < ~10 % of frame height, none cut by the frame edge)
squad_line('sqA', -222, -22, (0, 1), seed=5600)
squad_line('sqB', -246, 14, (0, -1), seed=5630)
squad_line('sqC', -196, -14, (1, 0), files=10, seed=5660)
squad_line('sqD', -150, 12, (0, -1), seed=5690)
squad_column('sqE', -206, 22, (1, 0), seed=5720)
squad_column('sqF', -118, -18, (-1, 0), seed=5750)
squad_line('sqG', -96, 8, (0, -1), files=12, seed=5780)
squad_column('sqH', -150, -28, (1, 0), rows=7, seed=5810)
squad_line('sqJ', -262, -14, (1, 0), files=10, seed=5840)
print('CP056 squads people', NPEOPLE[0])

# ------------------------------------------------------------------ 3. mess spaces screened off on the outskirts of the nave (garden-side aisle, y -36..-60)
SC = MB('cp056_mess_screens_canvas', M['canvas']); SF = MB('cp056_mess_screens_frames', M['frame'])
TB = MB('cp056_mess_tables_forms', M['table']); TT = MB('cp056_mess_trestles', M['trestle']); EN = MB('cp056_mess_enamel_mugs', M['enamel'])
SY, SH = -NY - 1.0, 8.0                       # screen line 1 ft behind the column line; 8 ft high (I)
x = -330.0; nbay = 0
while x < -84:
    gap = (nbay % 3 == 2)                     # every third bay left open as the way in (I)
    if not gap:
        x0, x1 = x + 1.0, x + BAY - 1.0
        SC.box(x0, x1, SY - 0.05, SY + 0.05, 0.6, SH)
        for xp in (x0, (x0 + x1) / 2, x1): SF.box(xp - 0.2, xp + 0.2, SY - 0.2, SY + 0.2, 0, SH + 0.3)
        SF.box(x0, x1, SY - 0.2, SY + 0.2, SH, SH + 0.3)
    # mess tables behind the screen: 2 per bay, scrubbed deal 2.5 ft x 20 ft, 2.4 ft high, forms either side (I)
    for ty in (-44.0, -53.0):
        TB.box(x + 2, x + 22, ty - 1.25, ty + 1.25, 2.3, 2.45)
        for tx in (x + 4, x + 20): TT.box(tx - 0.15, tx + 0.15, ty - 1.0, ty + 1.0, 0, 2.3)
        for fy in (ty - 2.4, ty + 2.4):
            TB.box(x + 2, x + 22, fy - 0.45, fy + 0.45, 1.45, 1.55)
            for tx in (x + 4, x + 20): TT.box(tx - 0.12, tx + 0.12, fy - 0.35, fy + 0.35, 0, 1.45)
        for k in range(10): EN.cyl(x + 3.5 + k * 1.8, ty + (0.6 if k % 2 else -0.6), 2.45, 2.75, 0.18, 8)
    x += BAY; nbay += 1
for o in (SC, SF, TB, TT, EN): o.done()
# a mess party laying up a table behind an open bay (backs/profiles; seated pose at the forms)
for k, (px, py, pose, face) in enumerate([(-201, -46.4, 'seated', (0, 1)), (-197, -46.4, 'seated', (0, 1)), (-193, -46.4, 'seated', (0, 1)),
                                          (-199, -41.6, 'seated', (0, -1)), (-195, -41.6, 'seated', (0, -1)), (-190, -39.5, 'walking', (1, 0))]):
    put(f'cp056_mess_{k}', pose, px, py, face, 5900 + k)
print('CP056 BUILT screens bays', nbay, 'people', NPEOPLE[0])

if OUT != '--nosave':
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    bpy.ops.wm.save_as_mainfile(filepath=os.path.abspath(OUT), copy=True)
    print('CP056 SAVED', OUT)
