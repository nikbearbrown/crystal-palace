"""CP009 v2 figures (2026-11-09, DEPARTURES SD32): period-dressed 1850 site figures for the contract shot.
Replaces the rejected people_lib v3.4 swap (bald heads, A-pose torsos, floating hats, bare feet).
Head = CC0 HBM realistic head from the survey people_lib vendor bases (cut at the neck, hair shell added);
everything below the collar is modelled dress: lathe-ellipse coat/jacket, waistcoat, collar + neckerchief/cravat,
sleeved arms posed per role, mitten hands, trousers, laced ankle boots; hats SIT on the head (band at the brow line).
Faces -y in local space (same convention as the s01/s02 lathe figures it replaces). Subdivided once, smooth shaded."""
import bpy, bmesh, math, sys, random, zlib
from mathutils import Vector, Matrix
sys.path.insert(0, "/workspace/crystal-palace-survey/people")
import people_lib as PL

def _mat(name, c, rough=0.85, sheen=0.0, noise_s=0.0):
    m = bpy.data.materials.get(name)
    if m: return m
    m = bpy.data.materials.new(name); m.use_nodes = True; nt = m.node_tree
    b = nt.nodes["Principled BSDF"]; b.inputs["Base Color"].default_value = (*c, 1); b.inputs["Roughness"].default_value = rough
    if "Specular IOR Level" in b.inputs: b.inputs["Specular IOR Level"].default_value = 0.15
    if sheen and "Sheen Weight" in b.inputs: b.inputs["Sheen Weight"].default_value = sheen
    if noise_s:
        tc = nt.nodes.new("ShaderNodeTexCoord"); n = nt.nodes.new("ShaderNodeTexNoise"); n.inputs["Scale"].default_value = noise_s
        n.inputs["Detail"].default_value = 6; nt.links.new(tc.outputs["Object"], n.inputs["Vector"])
        r = nt.nodes.new("ShaderNodeValToRGB"); e = r.color_ramp
        e.elements[0].position = 0.3; e.elements[0].color = (*[x * 0.78 for x in c], 1)
        e.elements[1].position = 0.75; e.elements[1].color = (*[min(1, x * 1.2) for x in c], 1)
        nt.links.new(n.outputs["Fac"], r.inputs[0]); nt.links.new(r.outputs[0], b.inputs["Base Color"])
        bp = nt.nodes.new("ShaderNodeBump"); bp.inputs["Strength"].default_value = 0.08
        n2 = nt.nodes.new("ShaderNodeTexNoise"); n2.inputs["Scale"].default_value = noise_s * 12
        nt.links.new(tc.outputs["Object"], n2.inputs["Vector"]); nt.links.new(n2.outputs["Fac"], bp.inputs["Height"])
        nt.links.new(bp.outputs[0], b.inputs["Normal"])
    m.diffuse_color = (*c, 1); return m

def _frame(d):
    d = d.normalized(); up = Vector((0, 0, 1)) if abs(d.z) < 0.95 else Vector((0, 1, 0))
    u = d.cross(up).normalized(); v = d.cross(u).normalized(); return u, v

def tube(bm, pts, mat, seg=12, cap0=True, cap1=True):
    """pts: list of (Vector centre, rx, ry[, yaw_dir]) -> ring sweep perpendicular to the path."""
    rings = []
    for i, (c, rx, ry) in enumerate(pts):
        a = pts[max(0, i - 1)][0]; b = pts[min(len(pts) - 1, i + 1)][0]; d = b - a
        if d.length < 1e-6: d = Vector((0, 0, 1))
        if abs(d.normalized().z) > 0.7:   # vertical: x = across, y = depth (front -y)
            u, v = Vector((1, 0, 0)), Vector((0, 1, 0))
        else:
            u, v = _frame(d)
        rings.append([bm.verts.new(c + u * (math.cos(2 * math.pi * k / seg) * rx) + v * (math.sin(2 * math.pi * k / seg) * ry)) for k in range(seg)])
    for A, B in zip(rings, rings[1:]):
        for k in range(seg):
            f = bm.faces.new([A[k], A[(k + 1) % seg], B[(k + 1) % seg], B[k]]); f.material_index = mat
    for ring, c, on in ((rings[0], pts[0][0], cap0), (rings[-1], pts[-1][0], cap1)):
        if on:
            t = bm.verts.new(c)
            for k in range(seg):
                f = bm.faces.new([ring[k], ring[(k + 1) % seg], t]); f.material_index = mat
    return rings

def lathe(bm, prof, mat, seg=16, cx=0.0, cy=0.0, close_top=True, close_bot=False):
    """prof: (z, rx, ry[, dy]) bottom -> top; front is -y."""
    pts = [(Vector((cx, cy + (p[3] if len(p) > 3 else 0.0), p[0])), p[1], p[2]) for p in prof]
    return tube(bm, pts, mat, seg, cap0=close_bot, cap1=close_top)

def ellipsoid(bm, c, r, mat, seg=10, rot=None):
    m = Matrix.Diagonal((*r, 1.0))
    if rot: m = rot.to_4x4() @ m
    res = bmesh.ops.create_uvsphere(bm, u_segments=seg, v_segments=max(6, seg // 2 + 1), radius=1.0, matrix=Matrix.Translation(c) @ m)
    for f in {f for v in res["verts"] for f in v.link_faces}: f.material_index = mat

def boxv(bm, c, s, mat):
    res = bmesh.ops.create_cube(bm, size=1.0, matrix=Matrix.Translation(c) @ Matrix.Diagonal((*s, 1.0)))
    for f in {f for v in res["verts"] for f in v.link_faces}: f.material_index = mat

# --------------------------------------------------------------------------------------------------------------
_HEAD_CACHE = {}
def _hbm_head(H):
    """CC0 HBM realistic male head + neck stump, scaled to a body of height H. Returns (mesh verts/faces, info)."""
    o = PL._import_base("male", "hero"); PL._scale_to_height(o, H); PL._enforce_head_ratio(o, PL.HEAD_RATIO)
    me = o.data; zs = [v.co.z for v in me.vertices]; z0, z1 = min(zs), max(zs); h = z1 - z0
    cut = z0 + 0.852 * h
    bm = bmesh.new(); bm.from_mesh(me); bpy.data.objects.remove(o, do_unlink=True)
    bmesh.ops.delete(bm, geom=[v for v in bm.verts if v.co.z < cut], context="VERTS")
    hv = [v.co for v in bm.verts if v.co.z > z1 - 0.13]
    cx = sum(c.x for c in hv) / len(hv); cy = sum(c.y for c in hv) / len(hv)
    for v in bm.verts: v.co.x -= cx; v.co.y -= cy
    ear = [v.co for v in bm.verts if abs(v.co.z - (z1 - 0.11)) < 0.012]
    info = dict(crown=z1, cut=cut, head_rx=max(abs(c.x) for c in ear), head_ry=max(abs(c.y) for c in ear),
                front=min(c.y for c in ear), back=max(c.y for c in ear))
    return bm, info

def _add_head(bm, H, skin, hair, hair_style):
    hb, I = _hbm_head(H)
    # hair shell: scalp verts above the ears and behind the brow, pushed out along the normal
    hb.normal_update()
    hair_bm = bmesh.new()
    vmap = {}
    brow_z = I["crown"] - 0.075
    for v in hb.verts:
        c = v.co
        back_ok = c.y > I["front"] + 0.035 or c.z > I["crown"] - 0.045      # not the face
        if (c.z > brow_z - (0.06 if c.y > 0.0 else 0.0)) and back_ok:
            vmap[v] = hair_bm.verts.new(c + v.normal * 0.007)
    for f in hb.faces:
        if all(v in vmap for v in f.verts):
            try: hair_bm.faces.new([vmap[v] for v in f.verts])
            except ValueError: pass
    me_h = bpy.data.meshes.new("tmp_hair"); hair_bm.to_mesh(me_h); hair_bm.free()
    me_k = bpy.data.meshes.new("tmp_head"); hb.to_mesh(me_k); hb.free()
    off = len(bm.verts)
    for me, mi in ((me_k, skin), (me_h, hair)):
        tmp = bmesh.new(); tmp.from_mesh(me)
        for f in tmp.faces: f.material_index = mi
        tmp.to_mesh(me); tmp.free(); bm.from_mesh(me); bpy.data.meshes.remove(me)
    return I

def _hat(bm, I, kind, mat, band):
    hr = I["head_rx"] * 1.06; hd = I["head_ry"] * 1.04; cy = (I["front"] + I["back"]) / 2
    z = I["crown"] - (0.062 if kind != "cap" else 0.05)          # hat band sits at the brow / top of the ears
    if kind == "top":   # silk top hat, ~6.5 in crown, slight bell, curled brim
        lathe(bm, [(z - 0.004, hr * 1.70, hd * 1.62), (z + 0.006, hr * 1.66, hd * 1.58), (z + 0.010, hr * 1.02, hd * 1.0)], mat, 20, cy=cy, close_top=False, close_bot=True)
        lathe(bm, [(z + 0.004, hr * 1.02, hd * 1.0), (z + 0.03, hr * 0.99, hd * 0.97), (z + 0.12, hr * 1.0, hd * 0.98), (z + 0.168, hr * 1.06, hd * 1.03), (z + 0.172, hr * 0.6, hd * 0.6)], mat, 20, cy=cy)
        lathe(bm, [(z + 0.012, hr * 1.025, hd * 1.005), (z + 0.035, hr * 1.005, hd * 0.985)], band, 20, cy=cy, close_top=False)
    elif kind == "wide":  # low-crowned felt 'wideawake', soft brim drooping slightly
        lathe(bm, [(z - 0.018, hr * 2.0, hd * 1.95), (z - 0.006, hr * 1.85, hd * 1.8), (z + 0.004, hr * 1.03, hd * 1.01)], mat, 20, cy=cy, close_top=False, close_bot=True)
        lathe(bm, [(z, hr * 1.03, hd * 1.01), (z + 0.05, hr * 1.0, hd * 0.98), (z + 0.085, hr * 0.85, hd * 0.83), (z + 0.095, hr * 0.4, hd * 0.4)], mat, 20, cy=cy)
        lathe(bm, [(z + 0.005, hr * 1.045, hd * 1.025), (z + 0.022, hr * 1.04, hd * 1.02)], band, 20, cy=cy, close_top=False)
    else:               # cloth cap: soft crown, puffed, short peak at the front (-y)
        lathe(bm, [(z, hr * 1.05, hd * 1.04), (z + 0.03, hr * 1.12, hd * 1.14, -0.005), (z + 0.06, hr * 1.0, hd * 1.05, -0.01), (z + 0.075, hr * 0.45, hd * 0.5, -0.008)], mat, 18, cy=cy, close_bot=False)
        ellipsoid(bm, Vector((0, cy - hd * 1.05, z + 0.004)), (hr * 0.85, hd * 0.42, 0.008), mat, 12)

def build_figure(name, role, H=1.75, pose="standing", seed=1, mats=None, hat=None):
    """role: 'engineer' (frock coat, top hat) | 'foreman' (jacket + waistcoat, wideawake) | 'workman' (fustian jacket,
    moleskin trousers, cap or wideawake) | 'carter' (smock-frock, wideawake). pose: standing | hauling | working | table."""
    rng = random.Random(seed); M = mats
    names = ["skin", "hair", "coat", "trou", "waist", "shirt", "neck", "boot", "hat", "band"]
    idx = {n: i for i, n in enumerate(names)}
    bm = bmesh.new()
    I = _add_head(bm, H, idx["skin"], idx["hair"], None)
    k = H / 1.75
    Z = lambda f: f * H
    neckz = I["cut"]
    # ---- legs (trousers) + boots ----
    stance = 0.095 * k
    for s in (-1, 1):
        x = s * stance
        tube(bm, [(Vector((x * 0.9, 0.0, Z(0.505))), 0.082 * k, 0.085 * k), (Vector((x, -0.005, Z(0.30))), 0.066 * k, 0.07 * k),
                  (Vector((x, 0.0, Z(0.14))), 0.058 * k, 0.06 * k), (Vector((x * 1.02, 0.005, Z(0.06))), 0.060 * k, 0.062 * k)], idx["trou"], 12, cap0=False)
        # laced ankle boot: ankle shaft + vamp + toe, sole slightly proud
        tube(bm, [(Vector((x * 1.02, 0.01, Z(0.075))), 0.05 * k, 0.055 * k), (Vector((x * 1.02, 0.0, Z(0.035))), 0.052 * k, 0.07 * k)], idx["boot"], 12, cap0=False, cap1=False)
        boxv(bm, Vector((x * 1.02, -0.045 * k, 0.03 * k)), (0.095 * k, 0.26 * k, 0.06 * k), idx["boot"])
        ellipsoid(bm, Vector((x * 1.02, -0.15 * k, 0.03 * k)), (0.048 * k, 0.06 * k, 0.03 * k), idx["boot"], 10)
    # ---- shirt collar / neckwear ----
    lathe(bm, [(neckz - 0.03, 0.068 * k, 0.064 * k), (neckz + 0.035, 0.06 * k, 0.058 * k)], idx["shirt"], 14, close_top=False)
    lathe(bm, [(neckz - 0.02, 0.072 * k, 0.07 * k), (neckz + 0.012, 0.066 * k, 0.064 * k)], idx["neck"], 14, close_top=False)
    if role == "engineer":
        ellipsoid(bm, Vector((0, -0.07 * k, neckz - 0.03)), (0.035 * k, 0.02 * k, 0.03 * k), idx["neck"], 10)  # cravat knot
    else:
        ellipsoid(bm, Vector((0.01, -0.068 * k, neckz - 0.035)), (0.03 * k, 0.018 * k, 0.04 * k), idx["neck"], 8)  # neckerchief knot
    # ---- coat body ----
    if role == "engineer":    # frock coat to the knee, fitted waist, flared skirts
        prof = [(0.29, .205, .175), (0.38, .19, .155), (0.48, .17, .135), (0.56, .155, .118), (0.62, .158, .12), (0.70, .175, .125), (0.765, .182, .12), (0.80, .17, .108), (0.825, .125, .088), (0.845, .08, .07)]
    elif role == "carter":    # smock-frock, full, to mid thigh
        prof = [(0.40, .215, .18), (0.50, .20, .165), (0.60, .19, .15), (0.70, .185, .135), (0.77, .185, .125), (0.80, .172, .11), (0.825, .125, .09), (0.845, .08, .07)]
    else:                     # short jacket to the hip
        prof = [(0.455, .175, .135), (0.52, .168, .128), (0.60, .162, .122), (0.70, .175, .126), (0.765, .182, .12), (0.80, .17, .108), (0.825, .125, .088), (0.845, .08, .07)]
    lathe(bm, [(Z(p[0]), p[1] * k, p[2] * k) for p in prof[:-1]] + [(max(neckz - 0.005, Z(prof[-2][0]) + 0.01), prof[-1][1] * k, prof[-1][2] * k)], idx["coat"], 18, close_top=False, close_bot=True)
    # open-fronted coat: a V of waistcoat (and shirt-front) conformed to the coat surface, buttons down the waistcoat
    def front_y(zf, x):
        for (za, rxa, rya), (zb, rxb, ryb) in zip(prof, prof[1:]):
            if za <= zf <= zb:
                t = (zf - za) / (zb - za); rx = (rxa + t * (rxb - rxa)) * k; ry = (rya + t * (ryb - rya)) * k
                return -ry * math.sqrt(max(0.0, 1 - (x / rx) ** 2)) - 0.004
        return -prof[-1][2] * k
    def vpanel(z_lo, z_hi, w_hi, mi, lift=0.0, nz=8, nx=6):
        rows = []
        for i in range(nz + 1):
            zf = z_lo + (z_hi - z_lo) * i / nz; w = max(0.004, w_hi * (zf - z_lo) / (z_hi - z_lo)) * k
            rows.append([bm.verts.new((x, front_y(zf, x) - lift, Z(zf))) for x in [-w + 2 * w * j / nx for j in range(nx + 1)]])
        for A, B in zip(rows, rows[1:]):
            for j in range(nx):
                f = bm.faces.new([A[j], A[j + 1], B[j + 1], B[j]]); f.material_index = mi
    if role != "carter":
        vz = 0.70 if role == "engineer" else 0.64
        vpanel(vz, 0.825, 0.065, idx["waist"])
        vpanel(0.765, 0.835, 0.03, idx["shirt"], lift=0.001)
        for i in range(4):   # waistcoat buttons
            zf = vz + 0.02 + 0.026 * i
            if zf < 0.77: ellipsoid(bm, Vector((0, front_y(zf, 0) - 0.003, Z(zf))), (0.007 * k, 0.004 * k, 0.007 * k), idx["boot"], 6)
        for i in range(3):   # coat buttons below the V
            zf = vz - 0.035 - 0.04 * i
            if zf > prof[0][0] + 0.03: ellipsoid(bm, Vector((0.035 * k, front_y(zf, 0.035 * k) - 0.003, Z(zf))), (0.009 * k, 0.005 * k, 0.009 * k), idx["boot"], 6)
    else:   # smock-frock: gathered smocking panel on the chest
        vpanel(0.68, 0.80, 0.10, idx["waist"], nx=10)
    # ---- arms ----
    sh = 0.172 * k; shz = Z(0.79)
    for s_ in (-1, 1):   # deltoid / sleeve-head, blends the sleeve into the coat shoulder
        ellipsoid(bm, Vector((s_ * 0.158 * k, 0.0, Z(0.792))), (0.062 * k, 0.064 * k, 0.055 * k), idx["coat"], 12)
    POSES = {   # (elbow, wrist) per side in units of k, z in H-fraction; s = side sign
        "standing": lambda s: ((s * 0.215, 0.02, 0.625), (s * 0.215, -0.02, 0.475)),
        "table":    lambda s: ((s * 0.21, -0.06, 0.63), (s * 0.17, -0.27, 0.565)) if s < 0 else ((s * 0.215, 0.02, 0.625), (s * 0.205, -0.03, 0.48)),
        "hauling":  lambda s: ((s * 0.2, -0.18, 0.69), (s * 0.13, -0.40, 0.66)),
        "working":  lambda s: ((s * 0.2, -0.16, 0.62), (s * 0.12, -0.33, 0.52)),
        "hips":     lambda s: ((s * 0.33, 0.02, 0.64), (s * 0.19, -0.03, 0.56)),
    }
    for s in (-1, 1):
        e, w = POSES[pose](s)
        S = Vector((s * sh, 0.0, shz)); E = Vector((e[0] * k, e[1] * k, Z(e[2]))); W = Vector((w[0] * k, w[1] * k, Z(w[2])))
        tube(bm, [(S, 0.058 * k, 0.06 * k), (S.lerp(E, 0.5), 0.056 * k, 0.058 * k), (E, 0.052 * k, 0.054 * k),
                  (E.lerp(W, 0.55), 0.048 * k, 0.05 * k), (W, 0.047 * k, 0.049 * k)], idx["coat"], 12, cap0=True, cap1=False)
        tube(bm, [(W - (W - E).normalized() * 0.01, 0.042 * k, 0.044 * k), (W + (W - E).normalized() * 0.012, 0.038 * k, 0.04 * k)], idx["shirt"], 10, cap0=False, cap1=False)
        d = (W - E).normalized(); hc = W + d * 0.06 * k
        xl = d.cross(Vector((0, 0, 1))); xl = xl.normalized() if xl.length > 1e-4 else Vector((1, 0, 0))
        yl = d.cross(xl).normalized(); rot = Matrix((xl, yl, d)).transposed()   # local x = palm width (horizontal), z = along forearm
        ellipsoid(bm, hc, (0.041 * k, 0.021 * k, 0.068 * k), idx["skin"], 10, rot=rot)   # flat hand, fingers together
        ellipsoid(bm, hc + rot @ Vector((-s * 0.038 * k, 0.0, -0.02 * k)), (0.011 * k, 0.011 * k, 0.03 * k), idx["skin"], 8, rot=rot)  # thumb
    # ---- hat ----
    hat_kind = hat or {"engineer": "top", "foreman": "wide", "carter": "wide"}.get(role, "cap" if seed % 2 else "wide")
    _hat(bm, I, hat_kind, idx["hat"], idx["band"])
    me = bpy.data.meshes.new(name)
    bm.to_mesh(me); bm.free()
    for n in names: me.materials.append(M[n])
    o = bpy.data.objects.new(name, me)
    # one Catmull-Clark level on the modelled dress; the HBM head is already dense, so subdivide via modifier, render 1
    sub = o.modifiers.new("sub", "SUBSURF"); sub.levels = 1; sub.render_levels = 1
    for p in me.polygons: p.use_smooth = True
    o["c9_role"] = role; o["c9_pose"] = pose; o["c9_hat"] = hat_kind; o["c9_height_m"] = round(H, 3)
    return o

def palette(tag, kind):
    """kind: engineer / foreman / workman_a / workman_b / carter"""
    P = {
        "skin": [(0.36, 0.22, 0.15), (0.31, 0.19, 0.13), (0.40, 0.25, 0.17)],
        "hair": (0.05, 0.035, 0.025),
        "shirt": (0.62, 0.60, 0.55), "boot": (0.028, 0.022, 0.018),
    }
    D = {
        "engineer":  dict(coat=(0.025, 0.025, 0.03), trou=(0.11, 0.10, 0.09), waist=(0.20, 0.17, 0.12), neck=(0.015, 0.015, 0.018), hat=(0.015, 0.015, 0.018), band=(0.005, 0.005, 0.006)),
        "foreman":   dict(coat=(0.10, 0.075, 0.05), trou=(0.13, 0.115, 0.09), waist=(0.16, 0.06, 0.04), neck=(0.05, 0.06, 0.12), hat=(0.06, 0.05, 0.04), band=(0.02, 0.018, 0.015)),
        "workman_a": dict(coat=(0.12, 0.11, 0.075), trou=(0.27, 0.24, 0.185), waist=(0.08, 0.07, 0.06), neck=(0.30, 0.06, 0.04), hat=(0.05, 0.045, 0.04), band=(0.03, 0.028, 0.025)),
        "workman_b": dict(coat=(0.08, 0.085, 0.09), trou=(0.25, 0.225, 0.175), waist=(0.14, 0.10, 0.06), neck=(0.06, 0.09, 0.20), hat=(0.07, 0.06, 0.05), band=(0.03, 0.028, 0.025)),
        "carter":    dict(coat=(0.40, 0.38, 0.30), trou=(0.16, 0.14, 0.10), waist=(0.36, 0.34, 0.27), neck=(0.25, 0.07, 0.05), hat=(0.08, 0.07, 0.055), band=(0.03, 0.028, 0.025)),
    }[kind]
    out = {}
    # skin tone index: was hash(tag) % 3 (Python string hashing is salted per process, so rebuilds drifted). Pinned on
    # 2026-11-09 to the tones of the reviewed KEEP candidate (rounds/candidates/s02_cp009contract_v2.blend, site 7ee5d75);
    # other tags fall back to a stable crc32.
    SKIN_PIN = {"c9_0": 2, "c9_1": 2, "c9_2": 0, "c9_3": 2, "c9_4": 1, "c9_5": 0}
    out["skin"] = _mat(f"C9V2_skin_{tag}", P["skin"][SKIN_PIN.get(tag, zlib.crc32(tag.encode()) % 3)], 0.55)
    out["hair"] = _mat("C9V2_hair", P["hair"], 0.6)
    out["shirt"] = _mat("C9V2_shirt_linen", P["shirt"], 0.8, noise_s=6)
    out["boot"] = _mat("C9V2_boot_leather", P["boot"], 0.45)
    for kk, v in D.items():
        out[kk] = _mat(f"C9V2_{kk}_{kind}", v, 0.92 if kk not in ("hat", "band") else 0.6 if kind == "engineer" else 0.9,
                       sheen=0.3 if kk == "coat" else 0.0, noise_s=4.0 if kk in ("coat", "trou") else 0.0)
    return out
