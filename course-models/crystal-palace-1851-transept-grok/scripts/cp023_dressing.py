"""CP023-only crowd dressing (2026-11-01, DEPARTURES PPL-C01..C04).

Used by render_views.py for CP023_into_nave_start/end only. The shared people_lib is
not modified: the pose rule is a temporary wrapper around the library's _infer_pose,
installed for the CP023 swap call and removed straight after, like the gate-off swap.

  people_patch(PG, gate, cam) context manager (render_views.py calls this; pose_patch is
                             an old alias): figures above the library close-up gate
                             (projected height > 8% of frame) get "standing" only (walking
                             dropped, see OK_POSES); seated/working/hauling/pointing/walking
                             are replaced deterministically by name hash. Also installs the
                             CP023 bonnet (make_bonnet) and a private mesh cache.
  dress(cam)                 after the swap: any figure whose world bbox is cut by the
                             frame edge (or crosses behind the camera), or that stands
                             within NEAR_M of the camera, is moved to a free in-frame spot
                             on the same floor level (same yaw); if no spot is found it is
                             hidden. Stray hat/bonnet parts (non-figure meshes whose
                             materials are all hat/bonnet) in view are hidden.
                             Returns (stats, undo) - call undo() after the render so the
                             next camera starts from the blend's own placement.
"""
import bpy, hashlib, random, math
from contextlib import contextmanager
from mathutils import Vector
from bpy_extras.object_utils import world_to_camera_view as w2c

CP023_CAMS = {"CP023_into_nave_start", "CP023_into_nave_end"}
OK_POSES = ("standing",)   # "walking" (strolling) dropped: people_lib 3.4 builds boots at the
                           # unposed ankle, so walking legs leave detached boots (the stray
                           # "hat"/block objects at figures' feet in the lean test). Standing only.
NEAR_M = 3.0          # "within about 3 m of the camera"
MIN_NEW_DIST = 7.0    # relocated figures go to the mid-ground (no new foreground close-ups)
MAX_NEW_DIST = 30.0
EDGE = 0.01           # relocated bbox must sit this far inside the frame
SPACING = 1.1         # min centre spacing to any other figure on the same level
FOOT_R = 0.45


def _h(name):
    return int(hashlib.md5(name.encode()).hexdigest()[:8], 16)


def make_bonnet(PG):
    """CP023-only bonnet. people_lib 3.4's build_bonnet puts its hood at -Y, which is the
    FACE side of the HBM base (turnaround check 2026-11-01), with radii half the head's, so
    the hood sits over the face and every lady seen from behind reads bald. This version
    is a hood over the back/top of the head, open at the face, sized just outside the skull."""
    _ring_unused = PG.get("_ring")
    def build_bonnet(bm, chin_z, crown_z, head_r, mat=0, seg=10):
        n = max(10, seg)
        cy = -0.20 * head_r          # skull centre sits slightly forward of the origin
        rows = []
        # (height t between chin and crown, radius scale, half-angle of the open face sector)
        for t, s, open_deg in ((0.30, 1.02, 72), (0.55, 1.10, 66), (0.80, 1.06, 56),
                               (0.98, 0.86, 40), (1.10, 0.55, 0)):
            z = chin_z + t * (crown_z + 0.025 - chin_z)
            rx, ry = head_r * 1.10 * s, head_r * 1.16 * s
            a0 = math.radians(open_deg); a1 = 2 * math.pi - a0
            full = open_deg == 0
            m = n if full else n + 1
            ring = []
            for i in range(m):
                a = (a0 + (a1 - a0) * i / (m - 1)) if not full else 2 * math.pi * i / n
                ring.append(bm.verts.new((math.sin(a) * rx, cy - math.cos(a) * ry + 0.0, z)))
            rows.append((ring, full))
        for (A, fa), (B, fb) in zip(rows, rows[1:]):
            if fa == fb:
                k = len(A) - (0 if fa else 1)
                for i in range(k):
                    j = (i + 1) % len(A)
                    try:
                        f = bm.faces.new((A[i], A[j], B[j], B[i])); f.material_index = mat
                    except ValueError:
                        pass
            else:   # open arc (A) to closed top ring (B): map arc verts onto ring
                for i in range(len(A) - 1):
                    bi = min(len(B) - 1, round(i * len(B) / (len(A) - 1)))
                    bj = min(len(B) - 1, round((i + 1) * len(B) / (len(A) - 1))) % len(B)
                    vs = [A[i], A[i + 1], B[bj]] if bi == bj else [A[i], A[i + 1], B[bj], B[bi]]
                    try:
                        f = bm.faces.new(vs); f.material_index = mat
                    except ValueError:
                        pass
        top, _ = rows[-1]
        c = bm.verts.new((0, cy + 0.1 * head_r, crown_z + 0.04))
        for i in range(len(top)):
            try:
                f = bm.faces.new((top[i], top[(i + 1) % len(top)], c)); f.material_index = mat
            except ValueError:
                pass
    return build_bonnet


@contextmanager
def people_patch(PG, gate, cam):
    """Install the CP023 pose rule and bonnet for one swap call, with a private mesh cache
    (so CP023 never reuses library-built meshes and nothing CP023-built leaks to other cams)."""
    orig = PG.get("_infer_pose")
    orig_bonnet = PG.get("build_bonnet")
    orig_cache = PG.get("_MESH_CACHE")
    PG["build_bonnet"] = make_bonnet(PG)
    PG["_MESH_CACHE"] = _CP023_CACHE
    stats = {"pose_replaced": 0}
    def wrapped(ob, seed):
        p = orig(ob, seed)
        if p not in OK_POSES and gate is not None and gate(ob, cam):
            p = OK_POSES[_h(ob.name) % len(OK_POSES)]
            stats["pose_replaced"] += 1
        return p
    PG["_infer_pose"] = wrapped
    try:
        yield stats
    finally:
        PG["_infer_pose"] = orig
        PG["build_bonnet"] = orig_bonnet
        PG["_MESH_CACHE"] = orig_cache


_CP023_CACHE = {}
pose_patch = people_patch   # old name


def _corners(ob):
    return [ob.matrix_world @ Vector(c) for c in ob.bound_box]


def _proj(sc, cam, pts):
    return [w2c(sc, cam, p) for p in pts]


def _in_view(ps):
    """Any part of the bbox in front of the camera and overlapping the frame (corners only)."""
    front = [p for p in ps if p.z > 0]
    if not front:
        return False
    xs = [p.x for p in front]; ys = [p.y for p in front]
    return max(xs) > 0 and min(xs) < 1 and max(ys) > 0 and min(ys) < 1


def _bbox_in_view(sc, cam, cs, n=6):
    """Robust test for boxes that straddle the camera plane: sample a grid through the bbox."""
    if _in_view(_proj(sc, cam, cs)) and all(p.z > 0 for p in _proj(sc, cam, cs)):
        return True
    lo = Vector((min(c.x for c in cs), min(c.y for c in cs), min(c.z for c in cs)))
    hi = Vector((max(c.x for c in cs), max(c.y for c in cs), max(c.z for c in cs)))
    for i in range(n):
        for j in range(n):
            for k in range(n):
                q = Vector((lo.x + (hi.x - lo.x) * i / (n - 1), lo.y + (hi.y - lo.y) * j / (n - 1),
                            lo.z + (hi.z - lo.z) * k / (n - 1)))
                p = w2c(sc, cam, q)
                if p.z > 0 and 0 < p.x < 1 and 0 < p.y < 1:
                    return True
    return False


def _cut(ps, m=0.0):
    if any(p.z <= 0 for p in ps):
        return True
    return any(p.x < m or p.x > 1 - m or p.y < m or p.y > 1 - m for p in ps)


def _hdist(a, b):
    return math.hypot(a.x - b.x, a.y - b.y)


def dress(cam, is_figure):
    sc = bpy.context.scene
    bpy.context.view_layer.update()
    dg = bpy.context.evaluated_depsgraph_get()
    cl = cam.matrix_world.translation.copy()
    figs = [o for o in bpy.data.objects if o.type == 'MESH' and not o.hide_render and is_figure(o)]
    saved = [(o, o.matrix_world.copy(), o.hide_render) for o in figs]
    info = {}
    for o in figs:
        cs = _corners(o); ps = _proj(sc, cam, cs)
        near = min((c - cl).length for c in cs) < NEAR_M or _hdist(o.matrix_world.translation, cl) < NEAR_M
        info[o] = (cs, ps, _bbox_in_view(sc, cam, cs), near)
    visible_before = sum(1 for o in figs if info[o][2])
    bad = [o for o in figs if info[o][2] and (info[o][3] or _cut(info[o][1]))]
    # near-camera figures fully out of frame can still shadow / pop in; hide them too
    near_hidden = [o for o in figs if info[o][3] and not info[o][2]]
    keep = [o for o in figs if o not in bad and o not in near_hidden]
    pos = {}   # level -> list of xy of kept figures
    for o in keep:
        t = o.matrix_world.translation
        pos.setdefault(round(t.z, 1), []).append(t.copy())
    moved, hidden, log = 0, 0, []
    for o in near_hidden:
        o.hide_render = True
    for o in bad:
        t0 = o.matrix_world.translation.copy(); lvl = t0.z; key = round(lvl, 1)
        rng = random.Random(_h(o.name) ^ _h(cam.name))
        cs0 = info[o][0]
        done = False
        for _ in range(600):
            u, v = rng.uniform(0.06, 0.94), rng.uniform(0.02, 0.6)
            # camera ray through (u, v) -> plane z = lvl
            frame = cam.data.view_frame(scene=sc)   # tr, br, bl, tl (camera space)
            tr, br, bl, tl = frame
            pc = bl + (br - bl) * u + (tl - bl) * v
            d = (cam.matrix_world.to_3x3() @ pc).normalized()
            if abs(d.z) < 1e-4: continue
            s = (lvl - cl.z) / d.z
            if s <= 0: continue
            p = cl + d * s
            hd = _hdist(p, cl)
            if hd < MIN_NEW_DIST or hd > MAX_NEW_DIST: continue
            delta = Vector((p.x - t0.x, p.y - t0.y, 0.0))
            ps = _proj(sc, cam, [c + delta for c in cs0])
            if _cut(ps, EDGE): continue
            if any(_hdist(p, q) < SPACING for q in pos.get(key, [])): continue
            okfoot = True
            gal = lvl > 1.0   # gallery figures: narrower footprint, railings may block the sight line
            fr = 0.3 if gal else FOOT_R
            for dx, dy in ((0, 0), (fr, 0), (-fr, 0), (0, fr), (0, -fr)):
                hit, loc, nor, idx, hob, mw = sc.ray_cast(dg, Vector((p.x + dx, p.y + dy, lvl + 1.95)), Vector((0, 0, -1)), distance=2.5)
                if not hit or abs(loc.z - lvl) > 0.06 or (hob is not None and is_figure(hob)):
                    okfoot = False; break
            if not okfoot: continue
            chest = Vector((p.x, p.y, lvl + 1.3)); dv = chest - cl
            if not gal:
                hit, loc, *_ = sc.ray_cast(dg, cl, dv.normalized(), distance=dv.length - 0.4)
                if hit: continue
            mw = o.matrix_world.copy(); mw.translation = Vector((p.x, p.y, lvl))
            o.matrix_world = mw
            pos.setdefault(key, []).append(Vector((p.x, p.y, lvl)))
            moved += 1; done = True
            log.append(f"MOVE {o.name} {tuple(round(x, 2) for x in t0)} -> {tuple(round(x, 2) for x in (p.x, p.y, lvl))}")
            break
        if not done:
            o.hide_render = True; hidden += 1
            log.append(f"HIDE {o.name} {tuple(round(x, 2) for x in t0)} (no free spot)")
    # stray hat / bonnet parts: visible non-figure meshes made only of hat materials
    orphans = []
    for o in bpy.data.objects:
        if o.type != 'MESH' or o.hide_render or is_figure(o) or not o.data.materials: continue
        names = [(m.name if m else "").lower() for m in o.data.materials]
        if names and all(("hat" in n or "bonnet" in n) for n in names):
            if _in_view(_proj(sc, cam, _corners(o))):
                saved.append((o, o.matrix_world.copy(), o.hide_render))
                o.hide_render = True; orphans.append(o.name)
    bpy.context.view_layer.update()
    visible_after = 0
    for o in figs:
        if o.hide_render: continue
        if _bbox_in_view(sc, cam, _corners(o)): visible_after += 1
    def undo():
        for o, mw, hr in saved:
            o.matrix_world = mw; o.hide_render = hr
    stats = {"figs": len(figs), "visible_before": visible_before, "flagged": len(bad),
             "moved": moved, "hidden_no_spot": hidden, "near_offframe_hidden": len(near_hidden),
             "orphans_hidden": orphans, "visible_after": visible_after}
    return stats, log, undo
