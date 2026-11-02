"""CP031 candidate (2026-11-02, Grok): the key-strike smith as a people_lib v3.4 1850s workman.

Replaces the r09 stand-in D_STAFF_STRIKER and the bolt-on arm rods inside D_MAUL with
  * D_STAFF_STRIKER_CPL3 : canonical people_lib v3.4 `1850s_workman` (hero LOD: cap, smock,
    trousers, boots), arms posed by a scripted two-bone IK so both hands close on the helve;
  * D_MAUL_CPL3          : ash helve from behind his rear hand to a cast-iron head whose barrel is
    square to the helve in the swing plane, striking face on the half-driven key.
The people_lib module is imported read-only from the survey repo (the vendored copies in the
course folders carry someone else's uncommitted edits and are not touched).
"""
import math, sys
import bpy, bmesh
from mathutils import Vector, Matrix, Quaternion

FT = 0.3048
SURVEY_PEOPLE = "/workspace/crystal-palace-survey/people"


def ft(v):
    return Vector(v) * FT


def _arm_rig(me, side):
    """Shoulder / elbow / wrist / hand-centre (local metres) for the A-pose base, side=+1 (x>0) or -1."""
    vs = [v.co for v in me.vertices]
    zs = [c.z for c in vs]; h = max(zs) - min(zs); z0 = min(zs)
    sh_z = z0 + 0.80 * h
    # hand: the outermost verts on this side below the waist
    low = [c for c in vs if side * c.x > 0.30 and c.z < z0 + 0.52 * h]
    tip = min(low, key=lambda c: c.z)
    hand_c = sum(low, Vector()) / len(low)
    S = Vector((side * 0.19, 0.0, sh_z))
    axis = hand_c - S
    L = (tip - S).length
    return S, axis.normalized(), L, h


def _two_bone(S, T, l1, l2, pole):
    """Elbow position for shoulder S reaching target T with bone lengths l1, l2; elbow bends toward pole."""
    d = T - S; dist = min(d.length, (l1 + l2) * 0.999); dn = d.normalized()
    a = (l1 * l1 - l2 * l2 + dist * dist) / (2 * dist)
    r = math.sqrt(max(l1 * l1 - a * a, 0.0))
    p = (pole - dn * pole.dot(dn)).normalized()
    return S + dn * a + p * r, S + dn * dist


def _seg_dist(p, a, b):
    ab = b - a; t = max(0.0, min(1.0, (p - a).dot(ab) / ab.length_squared))
    return (p - (a + ab * t)).length


def pose_strike(me, grips):
    """Deform `me` (local, facing -Y, feet z=0) so the hands land on grips[+1] / grips[-1] (local metres).
    Smooth linear-blend skinning over five capsules (body, two upper arms, two forearms); weights fall off
    with the distance to each capsule surface, so garment shells (smock, sleeves) bend with the arm without
    tearing. Elbows are solved with an analytic two-bone IK, bending out and down."""
    coords = [v.co.copy() for v in me.vertices]
    zs = [c.z for c in coords]; h = max(zs) - min(zs)
    caps = [(Vector((0, 0, 0.0)), Vector((0, 0, 0.80 * h + 0.06)), 0.125, None)]   # body: static
    report = {}; rigs = {}
    for side in (1, -1):
        S, ax, L, _ = _arm_rig(me, side)
        l1 = 0.47 * L; l2 = L - l1
        hand_off = 0.09
        E0 = S + ax * l1; T0 = S + ax * L
        E1, Tr = _two_bone(S, grips[side], l1, l2 - hand_off, Vector((side * 1.0, 0.25, -0.9)))
        q1 = ax.rotation_difference((E1 - S).normalized())
        q2 = ax.rotation_difference((Tr - E1).normalized())
        rigs[side] = (S, ax, L)
        caps.append((S, E0, 0.050, ("up", S, q1)))
        caps.append((E0, T0, 0.040, ("fore", E0, E1, q2)))
        report[side] = dict(S=tuple(round(x, 3) for x in S), L=round(L, 3), elbow=tuple(round(x, 3) for x in E1),
                            hand=tuple(round(x, 3) for x in Tr))
    out = []; armw = []
    for c in coords:
        ws = []
        for (a, b, r, xf) in caps:
            d = max(_seg_dist(c, a, b) - r, 0.004)
            ws.append(1.0 / d ** 6)
        tot = sum(ws); p = Vector(); aw = 0.0
        for w, (a, b, r, xf) in zip(ws, caps):
            w /= tot
            if xf is None:
                q = c
            elif xf[0] == "up":
                q = xf[1] + (xf[2] @ (c - xf[1]))
            else:
                q = xf[2] + (xf[3] @ (c - xf[1]))
            if xf is not None:
                aw += w
            p += q * w
        out.append(p); armw.append(aw)
    for v, c in zip(me.vertices, out):
        v.co = c
    me.update()
    # the trouser shell of the base dressing also wraps the hanging A-pose hands/forearms (z < waist):
    # on a raised arm that reads as a dark mitten, so drop trouser faces that ride on the arms
    bm = bmesh.new(); bm.from_mesh(me); bm.verts.ensure_lookup_table()
    trou = [k for k, m in enumerate(me.materials) if m and "trou" in m.name]
    kill = [f for f in bm.faces if f.material_index in trou and min(armw[v.index] for v in f.verts) > 0.5]
    # ...and the smock shell, which in the A-pose also wraps the hands: cut it back to the wrist so the bare
    # hands close on the helve (cuff 17 cm short of the finger tips)
    smock = [k for k, m in enumerate(me.materials) if m and "smock" in m.name]
    def beyond_wrist(i):
        c = coords[i]; side = 1 if c.x > 0 else -1
        S, ax, L = rigs[side]
        return (c - S).dot(ax) > L - 0.17
    kill += [f for f in bm.faces if f.material_index in smock and min(armw[v.index] for v in f.verts) > 0.5
             and all(beyond_wrist(v.index) for v in f.verts)]
    bmesh.ops.delete(bm, geom=kill, context="FACES")
    bm.to_mesh(me); bm.free(); me.update()
    report["trouser_faces_removed_from_arms"] = len(kill)
    return report


def narrow_stance(me, foot_half=0.15):
    """The live trestle deck is only 1.6 x 1.8 ft; the HBM base stands with its feet 0.54 m apart. Draw the legs
    in (x scaled about the centre line, 1.0 at the hip -> foot_half/|x_foot| at the soles) so both boots stand on
    the planks. Torso and arms are untouched."""
    vs = me.vertices
    zs = [v.co.z for v in vs]; h = max(zs) - min(zs); z0 = min(zs); hip = z0 + 0.50 * h
    xf = max(abs(v.co.x) for v in vs if v.co.z < z0 + 0.03)
    k = min(1.0, foot_half / xf)
    for v in vs:
        if v.co.z < hip and abs(v.co.x) < 0.30:
            t = (hip - v.co.z) / (hip - z0)
            v.co.x *= 1.0 + (k - 1.0) * t
    me.update()
    return dict(feet_half_before=round(xf, 3), feet_half_after=round(xf * k, 3))


def _mat(name, rgb, rough=0.85):
    m = bpy.data.materials.get(name)
    if m is None:
        m = bpy.data.materials.new(name); m.use_nodes = True
        b = m.node_tree.nodes.get("Principled BSDF")
        b.inputs["Base Color"].default_value = (*rgb, 1.0); b.inputs["Roughness"].default_value = rough
        m.diffuse_color = (*rgb, 1.0)
    return m


def dress_head(me):
    """people_lib v3.4 hero rule: no bald close-ups. Replace the perched disc cap with a cloth cap shrink-fitted
    to the skull (down to 7 cm below the crown, peak to the front) and a short-cropped hair shell on the back and
    sides of the head (down to the nape). Both are offset copies of the head skin, so they sit ON the head."""
    bm = bmesh.new(); bm.from_mesh(me); bm.verts.ensure_lookup_table(); bm.normal_update()
    mats = list(me.materials)
    hat = [k for k, m in enumerate(mats) if m and "hat" in m.name]
    skin = [k for k, m in enumerate(mats) if m and "skin" in m.name]
    bmesh.ops.delete(bm, geom=[f for f in bm.faces if f.material_index in hat], context="FACES")
    crown = max(v.co.z for v in bm.verts)
    headv = [v for v in bm.verts if v.co.z > crown - 0.12 and abs(v.co.x) < 0.12]
    hc = sum((v.co for v in headv), Vector()) / len(headv)
    hc.y = 0.5 * (min(v.co.y for v in headv) + max(v.co.y for v in headv))
    me.materials.append(_mat("CP031_hair_dkbrown", (0.035, 0.022, 0.014), 0.75)); i_hair = len(me.materials) - 1
    me.materials.append(_mat("CP031_cap_cloth_slate", (0.045, 0.05, 0.058), 0.9)); i_cap = len(me.materials) - 1
    cap_lo, hair_lo_back, hair_lo_front = crown - 0.075, crown - 0.185, crown - 0.075

    def region(pred):
        return [f for f in bm.faces if f.material_index in skin and all(pred(v.co) for v in f.verts)]

    def shell(faces, off, mi):
        d = bmesh.ops.duplicate(bm, geom=faces)
        nv = [g for g in d["geom"] if isinstance(g, bmesh.types.BMVert)]
        nf = [g for g in d["geom"] if isinstance(g, bmesh.types.BMFace)]
        for v in nv:
            r = (v.co - hc); r.z *= 0.6
            v.co += r.normalized() * off
        for f in nf:
            f.material_index = mi
        return nf

    back = lambda c: (c.y - hc.y) > -0.035          # facing -Y: back of head is +Y
    hair = region(lambda c: (c.z > hair_lo_back and back(c) and abs(c.x) < (0.10 if c.z > crown - 0.10 else 0.068)) or c.z > hair_lo_front)
    shell(hair, 0.006, i_hair)
    capf = region(lambda c: c.z > cap_lo - 0.004 * (1 if back(c) else 0))
    shell(capf, 0.014, i_cap)
    # peak: a shallow curved visor on the front edge of the cap
    r = 0.105; zc = cap_lo + 0.006
    ring = []
    for k in range(9):
        a = math.radians(-60 + 15 * k)
        inner = Vector((hc.x + math.sin(a) * 0.085, hc.y - math.cos(a) * 0.098, zc))
        outer = Vector((hc.x + math.sin(a) * 0.125, hc.y - math.cos(a) * 0.150, zc - 0.012))
        ring.append((bm.verts.new(inner), bm.verts.new(outer)))
    for (a0, b0), (a1, b1) in zip(ring, ring[1:]):
        f = bm.faces.new((a0, a1, b1, b0)); f.material_index = i_cap
    bm.to_mesh(me); bm.free(); me.update()
    return dict(crown=round(crown, 3), head_centre=tuple(round(x, 3) for x in hc), hair_faces=len(hair), cap_faces=len(capf))


def build(scene_root_coll, coll_staff, coll_support, mats, man_xy_ft, deck_ft, key_box_ft, seed=1852031):
    """Create the workman + maul. Returns (striker_obj, maul_obj, info dict)."""
    if SURVEY_PEOPLE not in sys.path:
        sys.path.insert(0, SURVEY_PEOPLE)
    import people_lib as P
    me0 = P.person_mesh("CP031_TMP", "workman", style={"role": "1850s_workman"}, pose="standing",
                        lod="hero", seed=seed)
    tmp = bpy.data.objects.get("CP031_TMP")
    me = me0.copy(); me.name = "cp031_striker_cpl3"
    if tmp is not None:
        bpy.data.objects.remove(tmp, do_unlink=True)

    # --- strike geometry (feet) -------------------------------------------------------------
    kx0, kx1, ky0, ky1, kz0, kz1 = key_box_ft
    man = Vector((man_xy_ft[0], man_xy_ft[1], deck_ft))
    C = Vector(((kx0 + kx1) / 2, ky1, 22.45))      # contact: N face of the key, 3.4 in above the girder top (22 ft 2 in)
    g = Vector((C.x - man.x, C.y - man.y, 0)).normalized()          # facing (horizontal)
    rz = math.atan2(g.x, -g.y)                                        # local -Y -> g
    Rw = Matrix.Rotation(rz, 4, 'Z')
    to_local = lambda p: Rw.inverted() @ ((p - man) * FT)            # world ft -> local m
    to_world = lambda p: man + (Rw @ p) / FT

    face_half = 5.25 / 12        # barrel 10.5 in long: striking face 5.25 in from the helve eye
    peen_len = 2.0 / 12
    rear_l = Vector((0.0, -0.52, 1.33))                               # rear (left) hand, local m
    Hc = None; d = None
    for _ in range(8):                                                # helve dir <-> head position
        Rw_rear = to_world(rear_l)
        if Hc is None:
            Hc = C
        d = (Hc - Rw_rear).normalized()
        # striking face normal: perpendicular to the helve in the vertical swing plane, toward the key
        side = d.cross(Vector((0, 0, 1))).normalized()
        nface = side.cross(d).normalized() * -1                       # forward-down
        if nface.dot(Vector((g.x, g.y, 0))) < 0:
            nface = -nface
        Hc = C - nface * face_half
    helve_back = 0.18   # ft behind the rear hand
    grip_gap = 0.40     # ft between hands
    hend = Rw_rear - d * helve_back
    front = Rw_rear + d * grip_gap
    grips = {-1: to_local(Rw_rear), 1: to_local(front)}
    # local x: +x is the figure's left (it faces -Y); put the rear hand on the left side of the helve
    grips[-1] = grips[-1] + Vector((0.035, 0, 0)); grips[1] = grips[1] + Vector((-0.035, 0, 0))
    stance = narrow_stance(me)
    rep = pose_strike(me, {1: grips[-1], -1: grips[1]})
    rep["stance"] = stance
    rep["head"] = dress_head(me)

    st = bpy.data.objects.new("D_STAFF_STRIKER_CPL3", me)
    coll_staff.objects.link(st)
    st.location = man * FT; st.rotation_euler = (0, 0, rz)
    st["role"] = "striker"; st["people_lib"] = P.PEOPLE_VERSION; st["style_role"] = "1850s_workman"
    st["pose"] = "strike_contact (scripted IK, cp031_striker.py)"; st["candidate"] = "CP031_strike 2026-11-02"

    # --- maul -----------------------------------------------------------------------------------
    bm = bmesh.new()
    def rod(a, b, r, seg):
        a = Vector(a) * FT; b = Vector(b) * FT; r = r * FT
        v = b - a; Ln = v.length
        m = bmesh.ops.create_cone(bm, cap_ends=True, segments=seg, radius1=r, radius2=r, depth=Ln)
        q = Vector((0, 0, 1)).rotation_difference(v.normalized())
        bmesh.ops.rotate(bm, verts=m["verts"], cent=Vector(), matrix=q.to_matrix())
        bmesh.ops.translate(bm, verts=m["verts"], vec=(a + b) / 2)
    hz = nface
    rod(hend, Hc, 0.62 / 12, 8)                                       # ash helve, 1.25 in dia at the grip
    rod(Hc - hz * (face_half - 0.02), Hc + hz * face_half, 2.4 / 12, 14)   # barrel, 4.8 in dia
    rod(Hc - hz * (face_half + peen_len), Hc - hz * (face_half - 0.05), 1.3 / 12, 10)   # peen
    me2 = bpy.data.meshes.new("maul_cp031")
    bm.to_mesh(me2); bm.free()
    for m in mats:
        me2.materials.append(m)
    # helve faces -> material 1 (ash), head -> 0 (cast iron)
    nh = 8 * 3  # cone with caps: 8 side faces + 2 caps -> first 10 faces
    for i, f in enumerate(me2.polygons):
        f.material_index = 1 if i < 10 else 0
    ma = bpy.data.objects.new("D_MAUL_CPL3", me2)
    coll_support.objects.link(ma)
    ma["part_kind"] = "tool"; ma["pose"] = "striking"; ma["head_dia_in"] = 4.8
    ma["helve_len_in"] = round((Hc - hend).length * 12, 1); ma["candidate"] = "CP031_strike 2026-11-02"
    info = dict(rz_deg=round(math.degrees(rz), 1), man_ft=tuple(round(x, 2) for x in man),
                contact_ft=tuple(round(x, 2) for x in C), head_ft=tuple(round(x, 2) for x in Hc),
                helve_in=ma["helve_len_in"], helve_elev_deg=round(math.degrees(math.asin(d.z)), 1),
                grips_local=[tuple(round(x, 3) for x in grips[-1]), tuple(round(x, 3) for x in grips[1])],
                arms=rep, height_m=round(max(v.co.z for v in me.vertices) - min(v.co.z for v in me.vertices), 3))
    return st, ma, info
