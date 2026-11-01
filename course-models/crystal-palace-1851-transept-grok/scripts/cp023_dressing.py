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
from mathutils import Vector, Matrix, Euler
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
def people_patch(PG, gate, cam, boots=False):
    """Install the CP023 pose rule and bonnet for one swap call, with a private mesh cache
    (so CP023 never reuses library-built meshes and nothing CP023-built leaks to other cams)."""
    orig = PG.get("_infer_pose")
    orig_bonnet = PG.get("build_bonnet")
    orig_cache = PG.get("_MESH_CACHE")
    orig_boots = PG.get("build_boots")
    orig_lm = PG.get("_landmarks")
    PG["build_bonnet"] = make_bonnet(PG)
    # boots=True (2026-11-01 boots+foreground CANDIDATE, PPL-C05): foot-fitted period boots.
    # Separate private cache so meshes built with/without the new boots never mix.
    PG["_MESH_CACHE"] = _CP023_CACHE_BOOTS if boots else _CP023_CACHE
    stats = {"pose_replaced": 0, "boots": 0}
    if boots:
        cap = {}
        def lm(obj):
            cap["body"] = obj
            return orig_lm(obj)
        PG["_landmarks"] = lm
        PG["build_boots"] = make_boots(PG, cap, orig_boots, stats)
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
        PG["build_boots"] = orig_boots
        PG["_landmarks"] = orig_lm


_CP023_CACHE = {}
_CP023_CACHE_BOOTS = {}
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


# ---------------------------------------------------------------------------
# 2026-11-01 boots + foreground CANDIDATE (DEPARTURES PPL-C05, PPL-C06)
# ---------------------------------------------------------------------------
# people_lib 3.4 build_boots: two axis-aligned shells at x = +-max(0.12, 0.38 * shoulder width)
# (+-0.20 m on the 1.76 m gentleman), toe at +Y, top at ankle + 0.14 m (0.21 m), wherever the
# HBM feet actually are. The HBM feet (24.8 cm long, splayed, trouser-coloured) poke out of
# the shell, so the union reads ~28 x 15 cm and 21 cm tall: the chunky stovepipe look, and
# on walking legs a second, detached shell. The CP023 boot below is fitted to each actual
# HBM foot (centroid + principal axis, toe = end away from the shin), squeezes the HBM foot
# inside it, and has a low ankle-boot shaft that ends under the trouser hem.
BOOT_LEN_MAX = 0.285   # m; adult man's boot ~27-29 cm (period ankle/Blucher boot)
BOOT_LEN_MIN = 0.22
BOOT_LEN_PAD = 0.025   # boot = measured HBM footprint + this, clamped to [MIN, MAX]
BOOT_W_MAX = 0.098     # m; ball-of-foot width of a man's boot ~9-10 cm
BOOT_SHAFT = 0.055     # m above the ankle landmark (top hidden under the trouser hem)
BOOT_SEG = 12


def _extent(pts):
    xs = [c.x for c in pts]; ys = [c.y for c in pts]
    return math.hypot(max(xs) - min(xs), max(ys) - min(ys))


def _foot_frame(me, side, L):
    """Per-foot frame from the HBM mesh: centre, forward axis (toe), lateral axis,
    length/width of the sole footprint, shin centre and radii just above the ankle."""
    z0, ank = L["z0"], L["ankle"]
    low = [v.co for v in me.vertices if v.co.z < ank + 0.10 and v.co.x * side > 0.02]
    if len(low) < 6:
        return None
    zb = min(c.z for c in low)            # this foot's lowest point (lifted heel/toe on walking legs)
    sole = [c for c in low if c.z < zb + 0.03]
    if len(sole) < 6 or _extent(sole) < 0.18:   # tilted foot: use the whole foot below the ankle
        sole = [c for c in low if c.z < zb + 0.085]
    shin = [v.co for v in me.vertices if zb + ank - z0 + 0.03 < v.co.z < zb + ank - z0 + 0.08 and v.co.x * side > 0.02]
    if len(sole) < 6 or len(shin) < 4:
        return None
    cx = sum(c.x for c in sole) / len(sole); cy = sum(c.y for c in sole) / len(sole)
    sx = sum(c.x for c in shin) / len(shin); sy = sum(c.y for c in shin) / len(shin)
    xx = sum((c.x - cx) ** 2 for c in sole); yy = sum((c.y - cy) ** 2 for c in sole)
    xy = sum((c.x - cx) * (c.y - cy) for c in sole)
    ang = 0.5 * math.atan2(2 * xy, xx - yy)
    ax, ay = math.cos(ang), math.sin(ang)
    # toe = end of the principal axis farther from the shin
    proj = [((c.x - cx) * ax + (c.y - cy) * ay) for c in sole]
    smin, smax = min(proj), max(proj)
    shin_s = (sx - cx) * ax + (sy - cy) * ay
    if abs(shin_s - smax) < abs(shin_s - smin):
        ax, ay = -ax, -ay; smin, smax = -smax, -smin
    lat = [(-(c.x - cx) * ay + (c.y - cy) * ax) for c in sole]
    sr = [((c.x - sx) * ax + (c.y - sy) * ay) for c in shin]
    tr = [(-(c.x - sx) * ay + (c.y - sy) * ax) for c in shin]
    return {"zb": zb, "c": (cx, cy), "a": (ax, ay), "len": smax - smin, "s0": smin, "s1": smax,
            "wid": max(lat) - min(lat), "shin": (sx, sy),
            "shin_rs": (max(sr) - min(sr)) / 2, "shin_rt": (max(tr) - min(tr)) / 2}


def make_boots(PG, cap, orig, stats):
    def build_boots(bm, L, hip_w, mat=0, seg=8):
        body = cap.get("body")
        if body is None or body.type != 'MESH':
            return orig(bm, L, hip_w, mat=mat, seg=seg)
        me = body.data; z0, ank = L["z0"], L["ankle"]
        frames = [f for f in (_foot_frame(me, sd, L) for sd in (-1.0, 1.0)) if f]
        if len(frames) < 2:
            return orig(bm, L, hip_w, mat=mat, seg=seg)
        n = BOOT_SEG
        for F in frames:
            (cx, cy), (ax, ay) = F["c"], F["a"]
            blen = min(BOOT_LEN_MAX, max(BOOT_LEN_MIN, F["len"] + BOOT_LEN_PAD))
            bw = min(BOOT_W_MAX, max(0.08, F["wid"] * 0.92))
            mid_s = 0.5 * (F["s0"] + F["s1"])   # sole midpoint along the axis
            # squeeze the HBM foot (and the bottom of the ankle) inside the boot
            # (tucked well inside the shell so no HBM toe lumps poke through; z flattened too)
            ks = min(0.85, (blen - 0.07) / max(F["len"], 1e-3))
            kt = min(0.75, (bw - 0.035) / max(F["wid"], 1e-3))
            side = 1.0 if cx > 0 else -1.0
            zb = F["zb"]; fa = zb + (ank - z0)        # this foot's ankle height
            for v in me.vertices:
                z = v.co.z
                if z > fa + 0.07 or v.co.x * side <= 0.0:
                    continue
                w = 1.0 if z <= fa + 0.01 else (fa + 0.07 - z) / 0.06
                ds, dt = (v.co.x - cx) * ax + (v.co.y - cy) * ay, -(v.co.x - cx) * ay + (v.co.y - cy) * ax
                ds = mid_s + (ds - mid_s) * (1 - w * (1 - ks)); dt *= (1 - w * (1 - kt))
                v.co.z = zb + 0.006 + (z - zb - 0.006) * (1 - w * 0.25) if z > zb + 0.006 else z
                v.co.x = cx + ds * ax - dt * ay; v.co.y = cy + ds * ay + dt * ax
            me.update()
            # boot rings in the foot frame: (z, centre_s, half_len, half_wid, heel_narrow)
            sx, sy = F["shin"]; shin_s = (sx - cx) * ax + (sy - cy) * ay
            shin_t = -(sx - cx) * ay + (sy - cy) * ax
            rs = min(F["shin_rs"], 0.06) + 0.012; rt = min(F["shin_rt"], 0.055) + 0.012
            hl, hw = blen / 2, bw / 2
            rings_def = (
                (zb + 0.002, mid_s, 0.0, hl, hw, 0.78),
                (zb + 0.022, mid_s, 0.0, hl * 1.0, hw * 1.0, 0.80),
                (zb + 0.050, mid_s - 0.015, 0.0, hl * 0.86, hw * 0.92, 0.85),
                (fa + 0.015, shin_s + 0.012, shin_t, rs + 0.03, rt * 1.05, 1.0),
                (fa + BOOT_SHAFT, shin_s, shin_t, rs, rt, 1.0),
            )
            rings = []
            for z, cs, ct, a, b, heel in rings_def:
                r = []
                for k in range(n):
                    t = 2 * math.pi * k / n
                    s_, t_ = math.cos(t) * a, math.sin(t) * b * (heel if math.cos(t) < 0 else 1.0)
                    if math.cos(t) > 0.3:   # rounded, slightly squared toe
                        t_ *= 1.0 - 0.15 * (math.cos(t) - 0.3)
                    s_ += cs; t_ += ct
                    r.append(bm.verts.new((cx + s_ * ax - t_ * ay, cy + s_ * ay + t_ * ax, z)))
                rings.append(r)
            for A, B in zip(rings, rings[1:]):
                PG["_bridge"](bm, A, B, mat)
            try:
                bm.faces.new(list(reversed(rings[0]))).material_index = mat
            except ValueError:
                pass
            stats["boots"] = stats.get("boots", 0) + 1
            stats.setdefault("boot_dims", set()).add((round(blen, 3), round(bw, 3)))
    return build_boots


FG_N = {"CP023_into_nave_start": 6, "CP023_into_nave_end": 5}
FG_MIN_DIST = 4.0     # m from the camera (dress() NEAR_M is 3.0)
FG_MAX_DIST = 9.0     # lower frame edge is ~5.5-6 m out on this eye-level lens; lower third ~6-9 m
FG_MAX_FRAC = 0.62    # projected proxy height <= this fraction of frame height (not filling the lens)
FG_MARGIN = 0.025     # proxy bbox this far inside every frame edge (never cut by the frame)
FG_SUBJECT_U = (0.40, 0.60)   # keep the nave vista / fountain axis clear: no foreground figure overlaps
FG_SPACING = 1.3
FG_PROXY_R, FG_PROXY_H = 0.55, 1.95   # crinoline radius / top-hat height (proxy before the swap)
FG_AWAY_SHARE = 0.7   # share walking into the nave (back to camera); the rest turn 3/4 towards it


def foreground(cam, is_figure, infer_kind):
    """Before the people swap (so the library's LOD ranking makes them hero figures): move a
    few floor-level figures that are NOT in this camera's view into the empty lower third,
    4-7 m out, fully inside the frame, clear of the central nave axis. Returns (stats, log, undo)."""
    sc = bpy.context.scene
    bpy.context.view_layer.update()
    dg = bpy.context.evaluated_depsgraph_get()
    cl = cam.matrix_world.translation.copy()
    n_want = FG_N.get(cam.name, 0)
    hit, loc, *_ = sc.ray_cast(dg, cl, Vector((0, 0, -1)), distance=10.0)
    lvl = loc.z if hit else 0.0
    figs = [o for o in bpy.data.objects if o.type == 'MESH' and not o.hide_render and is_figure(o)]
    floor = [o for o in figs if abs(o.matrix_world.translation.z - lvl) < 0.3]
    inview = set(o for o in floor if _bbox_in_view(sc, cam, _corners(o)))
    pool = [o for o in floor if o not in inview and _hdist(o.matrix_world.translation, cl) > 9.0]
    pool.sort(key=lambda o: _h(o.name + cam.name))
    def kind(o):
        k = infer_kind(o)
        if k == "man":
            r = int(hashlib.md5(o.name.encode()).hexdigest()[:6], 16) % 100
            k = "lady" if r < 42 else ("workman" if r >= 88 else "gentleman")
        return k
    # alternate gentleman / lady for a mixed group; skip workmen in the promenade foreground
    gents = [o for o in pool if kind(o) == "gentleman"]; ladies = [o for o in pool if kind(o) == "lady"]
    order = []
    for i in range(max(len(gents), len(ladies))):
        if i < len(gents): order.append(gents[i])
        if i < len(ladies): order.append(ladies[i])
    occupied = [o.matrix_world.translation.copy() for o in floor if o in inview]
    fwd = cam.matrix_world.to_3x3() @ Vector((0, 0, -1)); phi = math.atan2(fwd.y, fwd.x)
    frame = cam.data.view_frame(scene=sc); tr, br, bl, tl = frame
    rng = random.Random(_h(cam.name + "fg"))
    saved, log, placed = [], [], []
    for o in order:
        if len(placed) >= n_want: break
        for _ in range(1500):
            u = rng.choice((rng.uniform(0.06, 0.36), rng.uniform(0.64, 0.94)))
            v = rng.uniform(0.0, 0.34)          # foot point in the lower third
            pc = bl + (br - bl) * u + (tl - bl) * v
            d = (cam.matrix_world.to_3x3() @ pc).normalized()
            if d.z >= -1e-4: continue
            p = cl + d * ((lvl - cl.z) / d.z)
            hd = _hdist(p, cl)
            if not (FG_MIN_DIST <= hd <= FG_MAX_DIST): continue
            box = [Vector((p.x + dx, p.y + dy, lvl + dz)) for dx in (-FG_PROXY_R, FG_PROXY_R)
                   for dy in (-FG_PROXY_R, FG_PROXY_R) for dz in (0.0, FG_PROXY_H)]
            ps = _proj(sc, cam, box)
            if _cut(ps, FG_MARGIN): continue
            us = [q.x for q in ps]; vs = [q.y for q in ps]
            if max(vs) - min(vs) > FG_MAX_FRAC: continue
            if max(us) > FG_SUBJECT_U[0] and min(us) < FG_SUBJECT_U[1]: continue
            if any(_hdist(p, q) < FG_SPACING for q in occupied + placed): continue
            ok = True
            for dx, dy in ((0, 0), (FOOT_R, 0), (-FOOT_R, 0), (0, FOOT_R), (0, -FOOT_R)):
                h2, l2, n2, i2, hob, m2 = sc.ray_cast(dg, Vector((p.x + dx, p.y + dy, lvl + 2.2)), Vector((0, 0, -1)), distance=2.6)
                if not h2 or abs(l2.z - lvl) > 0.06 or (hob is not None and is_figure(hob)):
                    ok = False; break
            if not ok: continue
            chest = Vector((p.x, p.y, lvl + 1.3)); dv = chest - cl
            h3, *_ = sc.ray_cast(dg, cl, dv.normalized(), distance=dv.length - 0.4)
            if h3: continue
            away = rng.random() < FG_AWAY_SHARE
            yaw = phi + math.pi / 2 + (rng.uniform(-0.6, 0.6) if away else math.pi + rng.uniform(-0.9, 0.9))
            saved.append((o, o.matrix_world.copy()))
            loc0 = o.matrix_world.translation.copy()
            sca = o.matrix_world.to_scale()
            o.matrix_world = Matrix.LocRotScale(Vector((p.x, p.y, lvl)), Euler((0, 0, yaw)), sca)
            placed.append(Vector((p.x, p.y, lvl)))
            log.append(f"FG {o.name} {kind(o)} {tuple(round(x, 2) for x in loc0)} -> "
                       f"{tuple(round(x, 2) for x in (p.x, p.y, lvl))} d={hd:.2f} u={u:.2f} v={v:.2f} "
                       f"{'away' if away else 'toward'}")
            break
    bpy.context.view_layer.update()
    def undo():
        for o, mw in saved:
            o.matrix_world = mw
    return {"wanted": n_want, "placed": len(placed), "pool": len(pool), "floor_lvl": round(lvl, 3)}, log, undo
