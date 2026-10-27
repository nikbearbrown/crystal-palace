# r11: later Sydenham states, exec'd at the end of build.py (shares its namespace: MB, mat, f, C, coll, root, M, STATE,
# HALF, BD, UT, LT, yU, yL, BANK, TX, ST_X, CT_SPAN, CT_Y0, TOWER_H, gz, zs, cam, EYE, sc, ...). Evidence grades in
# DEPARTURES.md r11. Feet throughout.
import random
rs = random.Random(1936)
LATE = STATE in ('1936', 'FIRE', 'AFTER', 'RUINS', 'RUINS41')
SHELL_GONE = STATE in ('AFTER', 'RUINS', 'RUINS41')

def emis_mat(name, temp_lo=1300, temp_hi=2100, strength=30.0, alpha_noise=True, scale=0.25):
    """flame emitter: blackbody colour from noise, cut by a noise alpha so cones don't read as solids (I)."""
    m = bpy.data.materials.new(name); m.use_nodes = True; nt = m.node_tree; n = nt.nodes; l = nt.links
    for x in list(n): n.remove(x)
    out = n.new('ShaderNodeOutputMaterial'); em = n.new('ShaderNodeEmission'); tr = n.new('ShaderNodeBsdfTransparent')
    mix = n.new('ShaderNodeMixShader'); tc = n.new('ShaderNodeTexCoord'); nz = n.new('ShaderNodeTexNoise')
    nz.inputs['Scale'].default_value = scale; nz.inputs['Detail'].default_value = 6.0
    l.new(tc.outputs['Object'], nz.inputs['Vector'])
    mr = n.new('ShaderNodeMapRange'); mr.inputs['To Min'].default_value = temp_lo; mr.inputs['To Max'].default_value = temp_hi
    l.new(nz.outputs['Fac'], mr.inputs['Value']); bb = n.new('ShaderNodeBlackbody'); l.new(mr.outputs['Result'], bb.inputs['Temperature'])
    l.new(bb.outputs['Color'], em.inputs['Color']); em.inputs['Strength'].default_value = strength
    if alpha_noise:
        ramp = n.new('ShaderNodeValToRGB'); ramp.color_ramp.elements[0].position = 0.42; ramp.color_ramp.elements[1].position = 0.62
        l.new(nz.outputs['Fac'], ramp.inputs[0]); l.new(ramp.outputs['Color'], mix.inputs[0])
    else: mix.inputs[0].default_value = 1.0
    l.new(tr.outputs[0], mix.inputs[1]); l.new(em.outputs[0], mix.inputs[2]); l.new(mix.outputs[0], out.inputs['Surface'])
    return m

def flame_surf_mat(name, strength=12.0):
    """r11b flames: emissive *surface* tongues whose opacity falls off toward the silhouette (Layer Weight facing) and is
    broken up by vertically stretched world-space noise, so cones read as soft licking tongues, not solids. Much cheaper
    than per-object volumes (tested: 600 volume objects did not finish in 24 min). Blackbody from noise (I)."""
    m = bpy.data.materials.new(name); m.use_nodes = True; nt = m.node_tree; n = nt.nodes; l = nt.links
    for x in list(n): n.remove(x)
    out = n.new('ShaderNodeOutputMaterial'); em = n.new('ShaderNodeEmission'); tr = n.new('ShaderNodeBsdfTransparent')
    mix = n.new('ShaderNodeMixShader'); geo = n.new('ShaderNodeNewGeometry'); lw = n.new('ShaderNodeLayerWeight')
    lw.inputs['Blend'].default_value = 0.5
    def M(op, a, b=None):
        k = n.new('ShaderNodeMath'); k.operation = op; k.use_clamp = True
        for i, v in enumerate((a, b)):
            if v is None: continue
            if isinstance(v, (int, float)): k.inputs[i].default_value = v
            else: l.new(v, k.inputs[i])
        return k.outputs[0]
    core = M('POWER', M('SUBTRACT', 1.0, lw.outputs['Facing']), 2.2)          # 1 facing camera -> 0 at silhouette
    mp = n.new('ShaderNodeMapping'); mp.inputs['Scale'].default_value = (1.0, 1.0, 0.3); l.new(geo.outputs['Position'], mp.inputs['Vector'])
    nz = n.new('ShaderNodeTexNoise'); nz.inputs['Scale'].default_value = 0.9; nz.inputs['Detail'].default_value = 8.0; nz.inputs['Roughness'].default_value = 0.62
    l.new(mp.outputs[0], nz.inputs['Vector'])
    ramp = n.new('ShaderNodeValToRGB'); ramp.color_ramp.elements[0].position = 0.42; ramp.color_ramp.elements[1].position = 0.68
    l.new(nz.outputs['Fac'], ramp.inputs[0])
    at = n.new('ShaderNodeAttribute'); at.attribute_name = 'hfac'              # 0 at tongue base -> 1 at tip (per vertex)
    tip = M('POWER', M('SUBTRACT', 1.0, at.outputs['Fac']), 1.1)
    fac = M('MULTIPLY', M('MULTIPLY', core, ramp.outputs['Color']), tip)
    mr = n.new('ShaderNodeMapRange'); mr.inputs['To Min'].default_value = 1150; mr.inputs['To Max'].default_value = 2300
    l.new(fac, mr.inputs['Value']); bb = n.new('ShaderNodeBlackbody'); l.new(mr.outputs['Result'], bb.inputs['Temperature'])
    l.new(bb.outputs['Color'], em.inputs['Color']); em.inputs['Strength'].default_value = strength
    l.new(fac, mix.inputs[0]); l.new(tr.outputs[0], mix.inputs[1]); l.new(em.outputs[0], mix.inputs[2]); l.new(mix.outputs[0], out.inputs['Surface'])
    return m

def flame_vol_mat(name, strength=2.0):
    """r11 (kept for reference/SY_FLAMEVOL=1): emissive volume flames in one mesh (hard cone silhouettes)."""
    m = bpy.data.materials.new(name); m.use_nodes = True; nt = m.node_tree; n = nt.nodes; l = nt.links
    for x in list(n): n.remove(x)
    out = n.new('ShaderNodeOutputMaterial'); pv = n.new('ShaderNodeVolumePrincipled'); tc = n.new('ShaderNodeTexCoord')
    mp = n.new('ShaderNodeMapping'); mp.inputs['Scale'].default_value = (1.0, 1.0, 0.3); l.new(tc.outputs['Object'], mp.inputs['Vector'])
    nz = n.new('ShaderNodeTexNoise'); nz.inputs['Scale'].default_value = 0.6; nz.inputs['Detail'].default_value = 8.0; nz.inputs['Roughness'].default_value = 0.6
    l.new(mp.outputs[0], nz.inputs['Vector'])
    ramp = n.new('ShaderNodeValToRGB'); ramp.color_ramp.elements[0].position = 0.40; ramp.color_ramp.elements[1].position = 0.75
    l.new(nz.outputs['Fac'], ramp.inputs[0])
    mr = n.new('ShaderNodeMapRange'); mr.inputs['To Min'].default_value = 1200; mr.inputs['To Max'].default_value = 2300
    l.new(ramp.outputs['Color'], mr.inputs['Value']); bb = n.new('ShaderNodeBlackbody'); l.new(mr.outputs['Result'], bb.inputs['Temperature'])
    mul = n.new('ShaderNodeMath'); mul.operation = 'MULTIPLY'; mul.inputs[1].default_value = strength; l.new(ramp.outputs['Color'], mul.inputs[0])
    l.new(bb.outputs['Color'], pv.inputs['Emission Color']); l.new(mul.outputs[0], pv.inputs['Emission Strength'])
    pv.inputs['Density'].default_value = 0.02; pv.inputs['Color'].default_value = (0.05, 0.04, 0.03, 1)
    l.new(pv.outputs[0], out.inputs['Volume']); return m

def smoke_mat(name, density=0.025, emit=0.0, col=(0.06, 0.055, 0.05)):
    """volume-only smoke: noise density masked by a spherical falloff in the object's generated (bbox) coords."""
    m = bpy.data.materials.new(name); m.use_nodes = True; nt = m.node_tree; n = nt.nodes; l = nt.links
    for x in list(n): n.remove(x)
    out = n.new('ShaderNodeOutputMaterial'); pv = n.new('ShaderNodeVolumePrincipled'); tc = n.new('ShaderNodeTexCoord')
    sub = n.new('ShaderNodeVectorMath'); sub.operation = 'SUBTRACT'; sub.inputs[1].default_value = (0.5, 0.5, 0.5)
    sc2 = n.new('ShaderNodeVectorMath'); sc2.operation = 'SCALE'; sc2.inputs['Scale'].default_value = 2.0
    gr = n.new('ShaderNodeTexGradient'); gr.gradient_type = 'QUADRATIC_SPHERE'
    l.new(tc.outputs['Generated'], sub.inputs[0]); l.new(sub.outputs[0], sc2.inputs[0]); l.new(sc2.outputs[0], gr.inputs['Vector'])
    nz = n.new('ShaderNodeTexNoise'); nz.inputs['Scale'].default_value = 0.035; nz.inputs['Detail'].default_value = 9.0; nz.inputs['Roughness'].default_value = 0.62
    l.new(tc.outputs['Object'], nz.inputs['Vector'])
    ramp = n.new('ShaderNodeValToRGB'); ramp.color_ramp.elements[0].position = 0.46; ramp.color_ramp.elements[1].position = 0.64
    l.new(nz.outputs['Fac'], ramp.inputs[0])
    pw = n.new('ShaderNodeMath'); pw.operation = 'POWER'; pw.inputs[1].default_value = 1.8; l.new(gr.outputs['Fac'], pw.inputs[0])
    mul = n.new('ShaderNodeMath'); mul.operation = 'MULTIPLY'; l.new(pw.outputs[0], mul.inputs[0]); l.new(ramp.outputs['Color'], mul.inputs[1])
    mul2 = n.new('ShaderNodeMath'); mul2.operation = 'MULTIPLY'; mul2.inputs[1].default_value = density; l.new(mul.outputs[0], mul2.inputs[0])
    l.new(mul2.outputs[0], pv.inputs['Density']); pv.inputs['Color'].default_value = (*col, 1)
    if emit > 0:
        me = n.new('ShaderNodeMath'); me.operation = 'MULTIPLY'; me.inputs[1].default_value = emit / max(density, 1e-6) * 4.0
        l.new(mul2.outputs[0], me.inputs[0]); l.new(me.outputs[0], pv.inputs['Emission Strength'])   # glow only where smoke is
        pv.inputs['Emission Color'].default_value = (1.0, 0.32, 0.06, 1)
    l.new(pv.outputs[0], out.inputs['Volume']); return m

def ell(mb, cx, cy, cz, rx, ry, rz, us=20, vs=12):
    bmesh.ops.create_uvsphere(mb.bm, u_segments=us, v_segments=vs, radius=1.0,
        matrix=Matrix.Translation(Vector((f(cx), f(cy), f(cz)))) @ Matrix.Diagonal((f(rx), f(ry), f(rz), 1)))

def remove_obj(o): bpy.data.objects.remove(o, do_unlink=True)
def colls_of(o): return {c.name for c in o.users_collection}

# ---------------- terrace side flights + the six sphinxes (all states) ----------------
# Park Trust / Marsh award: "a set of six sphinxes, set in pairs at the head of three great granite steps" between the
# upper and lower terraces (R count/arrangement). ArtUK SE19_JK_S106: H 180 x D 480 cm, 1854, brick core + concrete,
# repainted terracotta red in 2016 "as they had been until the end of the 19th century" (Park Trust). Side-flight
# positions at the side transepts I; sphinx form procedural (Tanis type) I.
SPH = coll('SY54_terrace_sphinxes_and_side_flights__1854_extant')
sphm = mat('sphinx_red_painted_c1856', (0.42, 0.13, 0.07), 0.75) if not LATE else mat('sphinx_weathered_concrete', (0.47, 0.44, 0.39), 0.9)
add_bump(sphm, 6.0, 0.3) if 'add_bump' in globals() else None
SF = MB('terrace_side_flights', SPH, M['stone'])
RUN_ = (BANK - 2.5) / 10
for xc_ in (-ST_X, ST_X):
    for i in range(10):
        SF.box(xc_-14, xc_+14, yU-2.5-(i+1)*RUN_, yU-2.5-i*RUN_, LT, UT - i*(LOWER_TERRACE_DROP/10) + 0.01)
    for sx_ in (-1, 1):   # cheek walls
        SF.box(xc_+sx_*14, xc_+sx_*16.5, yU-BANK, yU-2.5, LT, UT+1.0)
SF.done()
SX = MB('terrace_sphinxes', SPH, sphm); SP = MB('terrace_sphinx_plinths', SPH, M['stone'])
import sys as _sys, os as _os
_sd = _os.path.dirname(_os.path.abspath(__file__)) if '__file__' in globals() else _os.path.join(_os.getcwd(), 'scripts')
if _sd not in _sys.path: _sys.path.insert(0, _sd)
import sculpt as _sculpt
_SPH_T = _sculpt.sphinx_mesh('sphinx_template_r12')   # r12: metaball lion body + hull nemes (scripts/sculpt.py), metres
def sphinx(x, y, z, face=-1):
    """Tanis-type sphinx, long axis on Y, head toward `face` (-1 = garden/-Y). Body 15.6 ft long, 5.95 ft high (ArtUK
    H 180 x D 480 cm, R) on a 3 ft plinth with a cornice (plinth I). r12: sculpted stand-in replaces the r11 ellipsoids."""
    SP.box(x-3.4, x+3.4, y-9.0, y+9.0, z, z+2.4); SP.box(x-3.8, x+3.8, y-9.4, y+9.4, z+2.4, z+3.0)   # plinth + cornice
    SP.box(x-3.45, x+3.45, y-9.05, y+9.05, z+0.9, z+1.5)                                              # hieroglyph band (blank) I
    rot = Matrix.Identity(4) if face < 0 else Matrix.Rotation(math.pi, 4, 'Z')
    _sculpt.append_mesh(SX.bm, _SPH_T, Matrix.Translation(Vector((f(x), f(y + 0.2), f(z + 3.0)))) @ rot)
for xc_, half in ((0, 48), (-ST_X, 14), (ST_X, 14)):
    for sx_ in (-1, 1):
        sphinx(xc_ + sx_*(half + 6.5), yU + 12, UT)   # at the head of each flight, on the upper terrace, facing the garden
SX.done(); SP.done(); bpy.data.meshes.remove(_SPH_T)

# ---------------- cameras for the later states (built in every state so pairs match) ----------------
# 36 mm sensor, 1.6 m eye, no roll; 35 mm exteriors, 28 mm interiors, 50 mm details (storyboard grammar). Positions I.
cam('CAM_CP057_1936_lower_terrace_35mm', (330, yL + 30, LT + EYE), (-120, -120, 85), 35)       # CP057/CP058/CP062 matched
cam('CAM_CP001_prologue_distant_35mm', (-260, -2150, zs(-2150) + EYE), (0, 0, 110), 35)        # CP001: glow from the park
cam('CAM_CP059_nave_fire_28mm', (-430, 10, EYE), (0, -5, 40), 28)                              # CP059: inside the nave
cam('CAM_CP061_transept_collapse_35mm', (-170, yU + 25, UT + EYE), (0, -60, 105), 35)          # CP061: CT from the upper terrace
cam('CAM_CP062_morning_between_towers_35mm', (0, -1950, zs(-1950) + EYE), (0, 30, 95), 35)    # CP062: both towers
cam('CAM_CP064_skyline_50mm', (260, -3150, zs(-3150) + EYE), (0, 30, 150), 50)                # CP064: tower skyline
cam('CAM_CP072_footprint_35mm', (-336, 0, gz(0) + EYE), (450, -10, gz(-10) + 4), 35)                    # CP072: empty plateau
cam('CAM_CP073_sphinx_steps_50mm', (-80, yU + 1, UT + EYE + 1), (-54.5, yU + 13, UT + 5.0), 50)   # CP073: sphinx detail
cam('CAM_CP073_steps_35mm', (-90, yU - 70, LT + EYE), (0, yU + 10, UT + 6), 35)                 # CP073: steps + sphinxes

# ---------------- 1936 and later dressing ----------------
TOWER_OBJS = [o for o in C['SY56_water_towers__dated'].objects]
if LATE:
    # fountains out of use long before 1936 (HE listing via Inside Croydon): jets removed, basins dry (I which ones)
    dry = mat('dry_basin_silt', (0.22, 0.20, 0.16), 0.95)
    for o in list(bpy.data.objects):
        if o.type == 'MESH' and o.data.materials and o.data.materials[0] == M['jet']: remove_obj(o)
        elif o.type == 'MESH' and o.data.materials and o.data.materials[0] == M['water']: o.data.materials[0] = dry
if STATE in ('1936', 'FIRE', 'AFTER'):
    # Baird's experimental TV transmitting mast on the South Tower from 1933 (HE listing via Inside Croydon, R);
    # form/height U (lattice mast 50 ft on the lantern).
    mm = MB('south_tower_baird_mast_1933', C['SY56_water_towers__dated'], M['iron_ext'])
    xc, yc, z0 = -(HALF + 120), 60, TOWER_H
    for sx_, sy_ in ((-1, -1), (1, -1), (1, 1), (-1, 1)):
        mm.strut((xc + sx_*1.6, yc + sy_*1.6, z0 - 6), (xc + sx_*0.6, yc + sy_*0.6, z0 + 50), 0.35, 0.35)
    for k in range(9):
        zz = z0 - 4 + k*6; r_ = 1.6 - 1.0*(k*6+2)/56
        mm.strut((xc - r_, yc - r_, zz), (xc + r_, yc + r_, zz + 6), 0.18, 0.18); mm.strut((xc + r_, yc - r_, zz), (xc - r_, yc + r_, zz + 6), 0.18, 0.18)
    mm.done()

def charred_iron(name):
    """r12: fire-blackened cast/wrought iron - near-black scale with sparse dull rust bloom and soot roughness (I;
    the 1936 aftermath photographs, refs 0587/0588, show the wreckage reading black against pale ash)."""
    m = mat(name, (0.028, 0.026, 0.024), 0.82, 0.45); nt = m.node_tree; b = nt.nodes['Principled BSDF']
    tc = nt.nodes.new('ShaderNodeTexCoord'); nz = nt.nodes.new('ShaderNodeTexNoise'); nz.inputs['Scale'].default_value = 1.6
    nz.inputs['Detail'].default_value = 8.0; nt.links.new(tc.outputs['Object'], nz.inputs['Vector'])
    cr = nt.nodes.new('ShaderNodeValToRGB'); cr.color_ramp.elements[0].position = 0.58; cr.color_ramp.elements[1].position = 0.72
    cr.color_ramp.elements[0].color = (0.026, 0.024, 0.022, 1); cr.color_ramp.elements[1].color = (0.11, 0.05, 0.025, 1)
    nt.links.new(nz.outputs['Fac'], cr.inputs['Fac']); nt.links.new(cr.outputs['Color'], b.inputs['Base Color'])
    bp = nt.nodes.new('ShaderNodeBump'); bp.inputs['Strength'].default_value = 0.35
    n2 = nt.nodes.new('ShaderNodeTexNoise'); n2.inputs['Scale'].default_value = 40.0; nt.links.new(tc.outputs['Object'], n2.inputs['Vector'])
    nt.links.new(n2.outputs['Fac'], bp.inputs['Height']); nt.links.new(bp.outputs['Normal'], b.inputs['Normal'])
    return m
burnt = charred_iron('iron_charred_black_1936')
def twisted(mb, x, y, z, L, rng, kink=True, w=0.9, flat=False):
    """a fallen girder/column length with an optional kink (I: generic ruin, never an intact component)."""
    a = rng.uniform(0, 2*math.pi); el = rng.uniform(-0.15, 0.25) if not flat else rng.uniform(-0.12, 0.12)
    d = Vector((math.cos(a)*math.cos(el), math.sin(a)*math.cos(el), math.sin(el)))
    p0 = Vector((x, y, z)); 
    if kink:
        t = rng.uniform(0.3, 0.7); p1 = p0 + d*L*t
        a2 = a + rng.uniform(-1.0, 1.0); el2 = rng.uniform(-0.2, 0.6) if not flat else rng.uniform(-0.25, 0.35)
        d2 = Vector((math.cos(a2)*math.cos(el2), math.sin(a2)*math.cos(el2), math.sin(el2)))
        mb.strut(tuple(p0), tuple(p1), w, w*1.6); mb.strut(tuple(p1), tuple(p1 + d2*L*(1-t)), w, w*1.6)
    else: mb.strut(tuple(p0), tuple(p0 + d*L), w, w*1.6)

FLAME_K = float(os.environ.get('SY_FLAME', '1.5'))
if STATE == 'FIRE':
    # Night of 30 Nov 1936. Fire began near the centre (LFB: women's cloakroom or Egyptian Court; Wikipedia), spread by
    # high wind through timber floors; iron frames buckled as glass failed and collapsed "creating a domino effect" (LFB).
    # The central transept collapse is the storyboard beat (CP061). Flame placement/extent at this instant I.
    for o in list(C['SY_central_transept'].objects): remove_obj(o)
    FC = coll('SY36_fire_30Nov1936__effects')
    glow = emis_mat('iron_glowing_debris', 900, 1300, 1.2, alpha_noise=False, scale=0.6)
    DB = MB('ct_collapse_debris_glowing', FC, glow); DB2 = MB('ct_collapse_debris', FC, burnt)
    for i in range(520):                                    # transept collapse pile (|x| < 60)
        x_ = rs.uniform(-62, 62); y_ = rs.uniform(-150, 150 if rs.random() < 0.8 else 175)
        twisted(DB if rs.random() < 0.35 else DB2, x_, y_, rs.uniform(0, 14), rs.uniform(8, 38), rs)
    for k in range(7):                                      # surviving / falling CT rib stubs, leaning (I)
        xr = rs.choice((-1, 1)) * rs.uniform(55, 62); yr = rs.uniform(-130, 130); R_ = CT_SPAN/2; lean = rs.uniform(0.15, 0.6)*(1 if xr < 0 else -1)
        pts = []
        for j in range(9):
            t = j/8*rs.uniform(0.6, 1.1); pts.append((xr - (R_ - R_*math.cos(t))*math.copysign(1, xr) + lean*R_*math.sin(t)*0.5, yr, CT_SPRING*0.7 + R_*math.sin(t)*0.9))
        DB2.strut((xr, yr, 0), pts[0], 1.6, 1.6)
        for p, q in zip(pts[:-1], pts[1:]): DB2.strut(p, q, 1.3, 2.2)
    VOLF = os.environ.get('SY_FLAMEVOL') == '1'
    fm = flame_vol_mat('fire_flames_volume', FLAME_K) if VOLF else flame_surf_mat('fire_flames_surface', 4.0 * FLAME_K)
    FL = MB('fire_flames', FC, fm)
    HL = FL.bm.verts.layers.float.new('hfac')
    def flame(x, y, z, r, h):
        n0 = len(FL.bm.verts); FL.cyl(x, y, z, z + h, r, r*0.12, seg=10); FL.bm.verts.ensure_lookup_table()
        for v in FL.bm.verts[n0:]: v[HL] = min(1.0, max(0.0, (v.co.z - f(z)) / f(h)))
    for i in range(70): flame(rs.uniform(-60, 60), rs.uniform(-150, 160), rs.uniform(0, 12), rs.uniform(7, 16), rs.uniform(35, 120))   # pile burning
    for i in range(420):                                    # nave and aisles: strongest south of centre, spreading (I)
        x_ = rs.gauss(-120, 360)
        if abs(x_) > HALF - 8: continue
        w_ = math.exp(-((x_ + 120)/520)**2)
        if rs.random() > w_: continue
        y_ = rs.uniform(-150, 150); zb = 0 if rs.random() < 0.8 else GALLERY_FLOOR
        if (x_ + 430)**2 + (y_ - 10)**2 < 110**2: continue   # keep the CP059 eye clear of flames
        flame(x_, y_, zb, rs.uniform(4, 11), rs.uniform(14, 45) * (0.6 + w_))
    FL.done(); DB.done(); DB2.done()
    if not VOLF: bpy.data.objects['fire_flames'].visible_shadow = False
    # smoke: separate puff objects (Generated coords are per-object) rising and leaning north-east downwind (wind U)
    smk = smoke_mat('smoke_volume_lit', 0.016, 0.0012, (0.2, 0.18, 0.16))
    smg = smoke_mat('smoke_volume_lowglow', 0.010, 0.003, (0.3, 0.24, 0.2))
    for k in range(16):
        t = k / 15
        cx = rs.uniform(-260, 120) + 650*t**1.4; cy = rs.uniform(-40, 60) + 260*t**1.4; cz = 110 + 640*t + rs.uniform(-30, 30)
        r = 130 + 260*t; P = MB(f'smoke_puff_{k:02d}', FC, smg if t < 0.25 else smk)
        ell(P, cx, cy, cz, r*rs.uniform(0.9, 1.4), r*rs.uniform(0.7, 1.0), r*rs.uniform(0.5, 0.8), 14, 9); P.done()
        bpy.data.objects[f'smoke_puff_{k:02d}'].visible_shadow = False
    for k, (cx, cy) in enumerate(((-40, 0), (-260, 20), (180, -10))):   # low puffs joining flames to the column
        P = MB(f'smoke_low_{k}', FC, smg); ell(P, cx, cy, 75, 170, 120, 70, 14, 9); P.done()
        bpy.data.objects[f'smoke_low_{k}'].visible_shadow = False

if SHELL_GONE:
    KEEP = {'SY_basement_garden_front', 'SY54_railway_colonnade', 'SY56_water_towers__dated', 'SY56_fountains_basins__dated',
            'SY_terraces_terrain', 'SY56_park_fountains_cascades__dated', 'SY56_park_paths_beds__dated',
            'SY_park_trees__placeholders', 'CAMERAS', 'REF_plan_0205', SPH.name}
    for o in list(bpy.data.objects):
        if o.type in ('CAMERA', 'LIGHT'): continue
        if not (colls_of(o) & KEEP) or o.name in ('basement_windows',): remove_obj(o)
    for c in list(bpy.data.collections):
        if c.name in ('SY_north_transept__lost1866',) or (not c.objects and not c.children and c != root and c.name not in KEEP and c.name.startswith('SY')):
            bpy.data.collections.remove(c)
    # ash / scorched ground over the footprint (I)
    ashm = mat('ash_scorched_ground' if STATE == 'AFTER' else 'cleared_plateau_rubble_grass', (0.07, 0.065, 0.06) if STATE == 'AFTER' else (0.24, 0.24, 0.17), 0.95)
    add_bump(ashm, 4.0, 0.4) if 'add_bump' in globals() else None
    AG = coll('SY36_aftermath_debris__Dec1936' if STATE == 'AFTER' else 'SY-RUINS_cleared_plateau_foundations__1937-40')
    AS = MB('footprint_ground', AG, ashm)
    ny = 24
    for j in range(ny):
        ya_ = -156 + 312*j/ny; yb_ = -156 + 312*(j+1)/ny
        AS.poly([(-HALF, ya_, gz(ya_) + 0.25), (HALF, ya_, gz(ya_) + 0.25), (HALF, yb_, gz(yb_) + 0.25), (-HALF, yb_, gz(yb_) + 0.25)])
    AS.poly([(-CT_SPAN/2, CT_Y0, -BD + 0.25), (CT_SPAN/2, CT_Y0, -BD + 0.25), (CT_SPAN/2, -156, -BD + 0.25), (-CT_SPAN/2, -156, -BD + 0.25)])
    AS.done()

if STATE == 'AFTER':
    # Aerial "a few days after" (refs 0587/0588, R): a field of collapsed ironwork across the whole plateau, the brick
    # basement front arcade standing, towers standing, the railway colonnade intact. Wikipedia: "all that was left
    # standing ... were the two water towers and a section of the north end of the main nave which was too badly damaged
    # to be saved" (R that it stood; its extent I). Density/heights of wreckage I.
    DF = MB('collapsed_ironwork_field', AG, burnt); FR = MB('north_end_standing_fragment', AG, burnt)
    for i in range(2600):
        x_ = rs.uniform(-HALF + 4, HALF - 4); y_ = rs.uniform(-154, 154)
        if (x_ + 336)**2 + y_**2 < 45**2: continue          # keep the CP072 eye clear
        twisted(DF, x_, y_, gz(y_) + rs.uniform(0.3, 4 if rs.random() < 0.8 else 9), rs.uniform(6, 30), rs, w=rs.uniform(0.35, 0.75), flat=True)
    for i in range(170):                                    # standing / leaning column stumps on the grid
        k = rs.randint(0, 66); x_ = -HALF + 24*k; y_ = rs.choice(COL_Y)
        h = rs.uniform(4, 30) if rs.random() < 0.85 else rs.uniform(35, 62)
        if (x_ + 336)**2 + y_**2 < 45**2: continue
        lx, ly = rs.uniform(-0.25, 0.25)*h, rs.uniform(-0.25, 0.25)*h
        DF.strut((x_, y_, gz(y_)), (x_ + lx, y_ + ly, gz(y_) + h), 0.8, 0.8)   # r12: 8-10 in columns, not 14 in (I)
    for x_ in [HALF - 24*k for k in range(4)]:              # north-end fragment: 3 bays of frame to the tiers, buckling
        for y_ in COL_Y:
            if abs(y_) < 37: continue
            top = (TIERS[1] if abs(y_) < 109 else TIERS[0]) * rs.uniform(0.75, 1.0)
            FR.strut((x_, y_, gz(y_)), (x_ + rs.uniform(-2, 2), y_ + rs.uniform(-2, 2), top), 1.2, 1.2)
            if x_ > HALF - 70: FR.strut((x_, y_, top - 2), (x_ - 24, y_ + rs.uniform(-3, 3), top - rs.uniform(2, 14)), 0.9, 2.2)
    for k in range(13):                                     # north gable rib, partly standing (I)
        t0, t1 = math.pi*k/13, math.pi*(k+1)/13
        if k > 8: break
        FR.strut((HALF, -36*math.cos(t0), NAVE_SPRING*0.92 + 36*math.sin(t0)), (HALF, -36*math.cos(t1), NAVE_SPRING*0.92 + 36*math.sin(t1)), 1.2, 2.4)
    FR.strut((HALF, -36, 0), (HALF, -36, NAVE_SPRING*0.92), 1.4, 1.4)
    DF.done(); FR.done()
    SW = MB('smouldering_smoke', AG, smoke_mat('smoke_volume_thin', 0.006, 0.0, (0.35, 0.34, 0.33)))
    ell(SW, -80, 20, 120, 300, 160, 120, 16, 10); ell(SW, 250, 60, 260, 360, 200, 150, 16, 10)
    SW.done(); bpy.data.objects['smouldering_smoke'].visible_shadow = False

if STATE in ('RUINS', 'RUINS41'):
    # Cleared by Thos. W. Ward Ltd (Wikipedia, R that the site was dismantled); state of the plateau c.1937-40 U.
    # Kept: basement garden-front arcade and garden stairs (survive today as the upper-terrace wall: refs CPupperterraces
    # 01-04, R), basement walls/tunnel as foundations, terraces, sphinxes, dry basins. Column footings as low pads (I).
    FP = MB('column_footing_pads', AG, M['brick'])
    for k in range(67):
        x_ = -HALF + 24*k
        for y_ in COL_Y:
            if rs.random() < 0.7: FP.box(x_ - 2, x_ + 2, y_ - 2, y_ + 2, gz(y_), gz(y_) + rs.uniform(0.6, 1.6))
    FP.done()
    if STATE == 'RUINS':
        # towers into dated sub-collections; the dates conflict between sources (DEPARTURES r11)
        for nm, label in (('south', 'SY-RUINS_south_water_tower__dismantled_autumn1940-1941'), ('north', 'SY-RUINS_north_water_tower__demolished_16Apr1941')):
            tc_ = coll(label, parent=C['SY56_water_towers__dated'])
            for o in TOWER_OBJS:
                if o.name.endswith('_'+nm) and o.name in bpy.data.objects:
                    for c in list(o.users_collection): c.objects.unlink(o)
                    tc_.objects.link(o)
    else:
        for o in TOWER_OBJS:   # 1941: both towers gone; the brick bases stay (south base excavated 1985, R)
            if o.name in bpy.data.objects and not o.name.startswith('water_tower_base_'): remove_obj(o)

# ---------------- lighting per state ----------------
def set_sky(elev, rot, strength, sun_e, sun_rot_z, sun_el):
    try: sky.sun_elevation = math.radians(elev); sky.sun_rotation = math.radians(rot)
    except Exception: pass
    bg.inputs[1].default_value = strength; sun.energy = sun_e
    so.rotation_euler = (math.radians(90 - sun_el), 0, math.radians(sun_rot_z))
if STATE == 'FIRE':
    for lk in list(nt.links):
        if lk.to_node == bg: nt.links.remove(lk)
    bg.inputs[0].default_value = (0.010, 0.011, 0.020, 1); bg.inputs[1].default_value = 1.0
    sun.energy = 0.04; sun.color = (0.6, 0.7, 1.0)                    # faint moonlight (U)
    sc.view_settings.exposure = -0.5
    sc.cycles.volume_step_rate = 6.0; sc.cycles.volume_max_steps = 256
elif STATE == 'AFTER':
    set_sky(9, 0, 0.30, 1.5, 0, 9)                                       # low December morning sun from the east (-Y) (I time)
    for a_, v_ in (('dust_density', 6.0), ('aerosol_density', 6.0), ('air_density', 1.6)):
        try: setattr(sky, a_, v_)
        except Exception: pass
    hz = nt.nodes.new('ShaderNodeMix'); hz.data_type = 'RGBA'; socket(hz, 'Factor_Float').default_value = 0.5
    socket(hz, 'B_Color').default_value = (0.42, 0.42, 0.44, 1)          # smoke haze over the site (I)
    nt.links.new(sky.outputs[0], socket(hz, 'A_Color')); nt.links.new(socket(hz, 'Result_Color', True), bg.inputs[0])
    sun.color = (1.0, 0.82, 0.62)
    sc.cycles.volume_step_rate = 6.0
print('STATE', STATE, 'root', root.name)

# ---------------- r12: PPL-20C 1936 dressing (appliances, hoses, crowds, police) ----------------
exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'dress36.py')).read())
