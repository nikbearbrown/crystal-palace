# Coverage audit cams (CP037/044 for EARLY; CP051/052/054 for LATE11). Exec'd from build or standalone -P.
# Units feet via f(); cam()/MB/coll/people/public/face_rot/EYE/GALLERY_FLOOR expected in namespace.
import math, random, bmesh
from mathutils import Vector, Matrix

def fmat(name, rgb, rough=0.75, metal=0.0):
    """Local mat helper (EARLY has no eras.fmat; LATE11 eras.fmat has different signature)."""
    m = bpy.data.materials.get(name) or mat(name, rgb, rough, metal)
    try: m.use_backface_culling = False
    except Exception: pass
    return m

def _cov_box(bm, x0, x1, y0, y1, z0, z1, mi=0):
    r = bmesh.ops.create_cube(bm, size=1.0)
    bmesh.ops.transform(bm, matrix=Matrix.Translation(Vector(((x0+x1)/2, (y0+y1)/2, (z0+z1)/2)) * F) @ Matrix.Diagonal(Vector((f(x1-x0), f(y1-y0), f(z1-z0), 1))), verts=r['verts'])
    for fc in {fc for v in r['verts'] for fc in v.link_faces}: fc.material_index = mi

if STATE == 'EARLY':
    # CP037 — taller Sydenham nave interior (different programme from Hyde Park)
    cam('CAM_CP037_taller_nave_28mm', (-120, 18, EYE + 2), (40, -8, 95), 28)
    # CP044 — education operating costs: pay desks, guidebook sellers, refreshment
    C44 = coll('SY56_education_costs__dated')
    wood = fmat('cov_desk_oak', (0.35, 0.22, 0.12), 0.75)
    cloth = fmat('cov_refresh_cloth', (0.55, 0.12, 0.08), 0.7)
    D = MB('cov_pay_desks', C44, wood); RF = MB('cov_refreshment', C44, cloth)
    # pay desks along south nave aisle (I placement)
    for i, x in enumerate([-420, -360, -300, -240]):
        D.box(x - 6, x + 6, -28, -22, 0, 3.2)
        D.box(x - 5.5, x + 5.5, -27.5, -22.5, 3.2, 3.4)  # desk top
    # guidebook stall
    D.box(-180, -150, -30, -24, 0, 4.0)
    D.box(-178, -152, -29, -25, 4.0, 7.5)  # shelf back
    # refreshment room counter near south end (I)
    RF.box(200, 280, -40, -28, 0, 3.5)
    RF.box(205, 275, -39, -29, 3.5, 3.7)
    D.done(); RF.done()
    pts44 = []
    R44 = random.Random(1856044)
    for x in (-420, -360, -300, -240, -165):
        pts44.append((x, -20, 0, public(R44), face_rot(0, 1), 1.0))  # clerk/seller
        for k in range(3):
            pts44.append((x + R44.uniform(-8, 8), -16 + R44.uniform(0, 6), 0, public(R44), face_rot(0, -1), R44.uniform(0.95, 1.03)))
    for k in range(18):
        pts44.append((220 + R44.uniform(-30, 40), -24 + R44.uniform(-4, 8), 0, public(R44), face_rot(0, 1), 1.0))
    people('ppl56_education_costs', C44, pts44)
    cam('CAM_CP044_pay_desks_35mm', (-380, -8, EYE + 1), (-360, -25, 4), 35)
    cam('CAM_CP044_refreshment_35mm', (160, -5, EYE + 1), (240, -32, 5), 35)
    print('COVERAGE EARLY CP037 CP044')

if STATE == 'LATE11':
    C51 = coll('SY-LATE_modernity_electric__dated')
    C52 = coll('SY-LATE_repair_scaffold__dated')
    C54 = coll('SY-LATE_plymouth_rescue_1913__dated')
    brass = fmat('cov_electric_brass', (0.55, 0.4, 0.15), 0.35, 0.8)
    glass = fmat('cov_bulb_glass', (0.85, 0.9, 0.95), 0.2)
    timber = fmat('cov_scaffold_timber', (0.32, 0.22, 0.12), 0.85)
    # CP051 — late electric / technology exhibit in nave
    EL = MB('cov_electric_fittings', C51, brass); BL = MB('cov_electric_bulbs', C51, glass)
    for x in range(-500, 200, 80):
        EL.cyl(x, 0, 42, 48, 0.35, 0.35, 8)          # pendant drop
        BL.cyl(x, 0, 40.5, 42.2, 1.1, 0.6, 10)        # bulb cluster
        # warm point lights
        ld = bpy.data.lights.new(f'cov_elec_{x}', 'POINT'); ld.energy = 1200; ld.color = (1.0, 0.85, 0.55); ld.shadow_soft_size = f(2)
        lo = bpy.data.objects.new(f'cov_elec_{x}', ld); C51.objects.link(lo); lo.location = (f(x), 0, f(41))
    # tech exhibit cabinets along aisle
    for i, x in enumerate([-200, -120, -40, 40]):
        EL.box(x - 8, x + 8, 30, 36, 0, 8)
        EL.box(x - 7, x + 7, 30.2, 35.8, 8, 8.3)
    EL.done(); BL.done()
    cam('CAM_CP051_electric_nave_28mm', (-280, -20, EYE + 2), (-40, 8, 45), 28)
    # CP052 — scaffolding + reglazing gang on garden front / nave glazing
    SC = MB('cov_repair_scaffold', C52, timber)
    # scaffold tower against south nave glazing bay
    for bay in (-100, 0, 100):
        for lx in (bay - 12, bay + 12):
            SC.strut((lx, -158, 0), (lx, -158, 55), 0.7, 0.7)
            SC.strut((lx, -148, 0), (lx, -148, 55), 0.7, 0.7)
        for z in (12, 24, 36, 48):
            SC.strut((bay - 12, -158, z), (bay + 12, -148, z), 0.5, 0.4)
            SC.box(bay - 14, bay + 14, -160, -146, z - 0.4, z)  # platform
    SC.done()
    pts52 = []
    R52 = random.Random(1911052)
    for bay in (-100, 0, 100):
        for k in range(5):
            pts52.append((bay + R52.uniform(-8, 8), -152 + R52.uniform(-2, 4), 12 + (k % 3) * 12, public(R52), face_rot(0, 1), 1.0))
    people('ppl11_reglazing_gang', C52, pts52)
    cam('CAM_CP052_scaffold_reglaze_35mm', (-72, -269, 18), (0, -153, 31), 35)  # dud-fix: pull back + raise; scaffold+gang fill
    # CP054 — 1913 public rescue: Lord Plymouth purchase celebration (crowd + bunting on terrace)
    FL54 = {k: MB(f'cov_plymouth_flag_{k}', C54, fmat(f'cov_ply_{k}', c)) for k, c in
            (('red', (0.5, 0.05, 0.05)), ('white', (0.85, 0.85, 0.8)), ('blue', (0.05, 0.08, 0.3)))}
    PO = MB('cov_plymouth_poles', C54, fmat('cov_ply_pole', (0.7, 0.7, 0.65), 0.6))
    for i, x in enumerate(range(-400, 401, 50)):
        flag(PO, [FL54['red'], FL54['white'], FL54['blue']], x, yU + 2, UT, 28, 10, 7, seed=i + 54)
    for m_ in (PO, *FL54.values()): m_.done()
    pts54 = crowd_pts(R_, (-500, 500, yU + 4, yU + 40), 2200, lambda x, y: UT, lambda r: public11(r), lambda x, y: face_rot(0, -1))
    people('ppl13_plymouth_rescue_crowd', C54, pts54)
    cam('CAM_CP054_plymouth_rescue_35mm', (-200, yU + 50, UT + EYE + 2), (40, yU - 10, UT + 20), 35)
    print('COVERAGE LATE11 CP051 CP052 CP054')
