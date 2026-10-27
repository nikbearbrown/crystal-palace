"""crystal-palace-people v2 — procedural period figures (licence-clean, offline).

Drop-in API:
  person_mesh(name, kind, mats, FT=0.3048, style=None, pose=None, lod=None, seed=None)
  swap_scene_people(era="1851", camera=None, seed=0)  # replace baked lathe crowds in a .blend

Body: separate head / torso / arms+hands / legs+feet capsules and boxes (not a single lathe).
Clothing silhouettes by era/class. Poses. Seeded variation. Three LODs: hero / mid / crowd.
No third-party body meshes — built entirely in bmesh (MPFB/MakeHuman not available offline).
"""
from __future__ import annotations
import hashlib, math, random
from typing import Any, Dict, List, Optional, Sequence, Tuple

import bpy
import bmesh
from mathutils import Matrix, Vector

PEOPLE_VERSION = "2.0"
PEOPLE_TAG = "cpl_people_v2"

# ---------------------------------------------------------------------------
# materials helpers
# ---------------------------------------------------------------------------

def _ensure_mat(name: str, color: Tuple[float, float, float], rough: float = 0.55) -> bpy.types.Material:
    m = bpy.data.materials.get(name)
    if m is None:
        m = bpy.data.materials.new(name)
        m.use_nodes = True
    nt = m.node_tree
    bsdf = nt.nodes.get("Principled BSDF")
    if bsdf:
        bsdf.inputs["Base Color"].default_value = (*color, 1.0)
        if "Roughness" in bsdf.inputs:
            bsdf.inputs["Roughness"].default_value = rough
    m.diffuse_color = (*color, 1.0)
    return m


def _default_mats(seed: int = 0) -> List[bpy.types.Material]:
    """[main, second, skin, hat, trim] with seeded cloth variation."""
    rng = random.Random(seed)
    coats = [
        (0.12, 0.14, 0.22), (0.18, 0.12, 0.10), (0.08, 0.10, 0.08),
        (0.22, 0.18, 0.14), (0.10, 0.12, 0.18), (0.28, 0.08, 0.08),
        (0.14, 0.16, 0.12), (0.20, 0.20, 0.22),
    ]
    skirts = [
        (0.35, 0.12, 0.14), (0.12, 0.18, 0.28), (0.45, 0.40, 0.32),
        (0.18, 0.22, 0.16), (0.30, 0.20, 0.28), (0.40, 0.35, 0.20),
        (0.15, 0.15, 0.18), (0.50, 0.45, 0.40),
    ]
    trous = [(0.10, 0.10, 0.12), (0.18, 0.16, 0.14), (0.08, 0.10, 0.14)]
    skins = [(0.72, 0.55, 0.45), (0.55, 0.40, 0.32), (0.80, 0.65, 0.52)]
    hats = [(0.05, 0.05, 0.06), (0.12, 0.10, 0.08), (0.20, 0.18, 0.12), (0.08, 0.12, 0.08)]
    trims = [(0.55, 0.45, 0.20), (0.70, 0.70, 0.72), (0.40, 0.10, 0.10)]
    i = rng.randrange(8)
    return [
        _ensure_mat(f"CPL_PPL_main_{i}", coats[i] if rng.random() > 0.45 else skirts[i]),
        _ensure_mat(f"CPL_PPL_sec_{i % 3}", trous[i % 3]),
        _ensure_mat(f"CPL_PPL_skin_{i % 3}", skins[i % 3], 0.45),
        _ensure_mat(f"CPL_PPL_hat_{i % 4}", hats[i % 4], 0.65),
        _ensure_mat(f"CPL_PPL_trim_{i % 3}", trims[i % 3], 0.4),
    ]


# ---------------------------------------------------------------------------
# low-level solid builders (bmesh)
# ---------------------------------------------------------------------------

def _box(bm: bmesh.types.BMesh, x0, x1, y0, y1, z0, z1, mat=0):
    vs = [bm.verts.new(v) for v in [
        (x0, y0, z0), (x1, y0, z0), (x1, y1, z0), (x0, y1, z0),
        (x0, y0, z1), (x1, y0, z1), (x1, y1, z1), (x0, y1, z1),
    ]]
    for idx in ((0, 3, 2, 1), (4, 5, 6, 7), (0, 1, 5, 4), (1, 2, 6, 5), (2, 3, 7, 6), (3, 0, 4, 7)):
        f = bm.faces.new([vs[i] for i in idx])
        f.material_index = mat


def _capsule(bm: bmesh.types.BMesh, a: Vector, b: Vector, r: float, seg: int = 8, mat: int = 0):
    """Tapered cylinder between a and b with hemispheric end caps (low-poly)."""
    d = b - a
    length = d.length
    if length < 1e-8:
        return
    direction = d.normalized()
    # orthonormal basis
    up = Vector((0, 0, 1)) if abs(direction.z) < 0.9 else Vector((1, 0, 0))
    x_axis = direction.cross(up).normalized()
    y_axis = direction.cross(x_axis).normalized()
    rings = []
    # two end rings + mid if long
    zs = (0.0, 1.0)
    for t in zs:
        center = a.lerp(b, t)
        ring = []
        for k in range(seg):
            ang = 2 * math.pi * k / seg
            p = center + (math.cos(ang) * x_axis + math.sin(ang) * y_axis) * r
            ring.append(bm.verts.new(p))
        rings.append(ring)
    for A, B in zip(rings, rings[1:]):
        for k in range(seg):
            f = bm.faces.new([A[k], A[(k + 1) % seg], B[(k + 1) % seg], B[k]])
            f.material_index = mat
    # end caps (fan)
    for ring, tip in ((rings[0], a - direction * r * 0.35), (rings[-1], b + direction * r * 0.35)):
        tv = bm.verts.new(tip)
        for k in range(seg):
            f = bm.faces.new([ring[k], ring[(k + 1) % seg], tv])
            f.material_index = mat


def _ellipsoid(bm: bmesh.types.BMesh, c: Vector, rx, ry, rz, seg: int = 8, mat: int = 0):
    """UV-sphere scaled to ellipsoid."""
    stacks = max(4, seg // 2)
    sectors = seg
    grid = []
    for i in range(stacks + 1):
        phi = math.pi * i / stacks
        row = []
        for j in range(sectors):
            th = 2 * math.pi * j / sectors
            x = c.x + rx * math.sin(phi) * math.cos(th)
            y = c.y + ry * math.sin(phi) * math.sin(th)
            z = c.z + rz * math.cos(phi)
            row.append(bm.verts.new((x, y, z)))
        grid.append(row)
    for i in range(stacks):
        for j in range(sectors):
            v1 = grid[i][j]
            v2 = grid[i][(j + 1) % sectors]
            v3 = grid[i + 1][(j + 1) % sectors]
            v4 = grid[i + 1][j]
            if i == 0:
                f = bm.faces.new([v1, v3, v4]); f.material_index = mat
            elif i == stacks - 1:
                f = bm.faces.new([v1, v2, v4]); f.material_index = mat
            else:
                f = bm.faces.new([v1, v2, v3, v4]); f.material_index = mat


def _lathe(bm: bmesh.types.BMesh, prof: Sequence[Tuple[float, float]], seg: int, cx=0.0, cy=0.0, ox=0.0, mat=0):
    rings = []
    for r, z in prof:
        ring = [bm.verts.new((cx + r * math.cos(2 * math.pi * k / seg) + ox,
                              cy + r * math.sin(2 * math.pi * k / seg), z)) for k in range(seg)]
        rings.append(ring)
    for A, B in zip(rings, rings[1:]):
        for k in range(seg):
            f = bm.faces.new([A[k], A[(k + 1) % seg], B[(k + 1) % seg], B[k]])
            f.material_index = mat
    if prof[-1][0] > 1e-6:
        f = bm.faces.new(rings[-1]); f.material_index = mat
    if prof[0][0] > 1e-6:
        f = bm.faces.new(list(reversed(rings[0]))); f.material_index = mat


# ---------------------------------------------------------------------------
# proportions (metres, adult male ~1.70 m crown; facing -Y like legacy figures)
# ---------------------------------------------------------------------------

# Landmark heights as fraction of body height H (feet at z=0, crown at H)
PROP = {
    "male": dict(H=1.70, shoulder_w=0.42, hip_w=0.34, chest_d=0.24, head_r=0.11,
                 upper_arm=0.30, forearm=0.27, hand=0.095, thigh=0.42, shin=0.42, foot=0.24),
    "female": dict(H=1.62, shoulder_w=0.36, hip_w=0.36, chest_d=0.22, head_r=0.105,
                   upper_arm=0.28, forearm=0.25, hand=0.085, thigh=0.40, shin=0.40, foot=0.22),
    "child": dict(H=1.20, shoulder_w=0.28, hip_w=0.26, chest_d=0.18, head_r=0.10,
                  upper_arm=0.22, forearm=0.20, hand=0.07, thigh=0.30, shin=0.30, foot=0.16),
}


def _seed_of(name: str, seed: Optional[int] = None) -> int:
    if seed is not None:
        return int(seed)
    return int(hashlib.md5(name.encode()).hexdigest()[:8], 16)


def _sex_for_kind(kind: str) -> str:
    k = (kind or "man").lower()
    if k in ("woman", "girl", "lady", "bustle"):
        return "female" if k != "girl" else "child"
    if k in ("boy",):
        return "child"
    return "male"


# ---------------------------------------------------------------------------
# era / role / clothing presets
# ---------------------------------------------------------------------------

ERA_ROLES = {
    # 1850s Hyde Park / Great Exhibition
    "1850s_gentleman": dict(era="1850s", sex="male", hat="top", coat="frock", trousers=True, cravat=True),
    "1850s_lady": dict(era="1850s", sex="female", hat="bonnet", skirt="crinoline", shawl=True),
    "1850s_workman": dict(era="1850s", sex="male", hat="cap", coat="smock", trousers=True, tool=False),
    "1850s_navvy": dict(era="1850s", sex="male", hat="cap", coat="waistcoat", trousers=True, tool=True),
    "1850s_police": dict(era="1850s", sex="male", hat="top", coat="frock", trousers=True, trim="police"),
    "1850s_soldier": dict(era="1850s", sex="male", hat="shako", coat="redcoat", trousers=True),
    "1850s_girl": dict(era="1850s", sex="child", hat="bonnet", skirt="crinoline", female_child=True),
    "1850s_boy": dict(era="1850s", sex="child", hat="cap", coat="frock", trousers=True),
    # 1880s–1910s Sydenham / naval
    "1890s_gentleman": dict(era="1890s", sex="male", hat="boater", coat="lounge", trousers=True),
    "1890s_lady": dict(era="1890s", sex="female", hat="boater", skirt="bustle", shawl=False),
    "1890s_sailor": dict(era="1890s", sex="male", hat="sailor", coat="sailor", trousers=True, bellbottoms=True),
    "1890s_uniform": dict(era="1890s", sex="male", hat="peak", coat="uniform", trousers=True),
    # 1930s
    "1930s_man": dict(era="1930s", sex="male", hat="trilby", coat="overcoat", trousers=True),
    "1930s_woman": dict(era="1930s", sex="female", hat="beret", skirt="straight", coat="overcoat"),
    "1930s_fireman": dict(era="1930s", sex="male", hat="helmet", coat="fire", trousers=True),
    # today
    "today_casual_m": dict(era="today", sex="male", hat="none", coat="tee", trousers=True),
    "today_casual_f": dict(era="today", sex="female", hat="none", coat="tee", skirt="straight"),
}


def resolve_role(kind: str, style: Optional[dict], era_hint: str = "1850s") -> dict:
    st = dict(style or {})
    if st.get("role") and st["role"] in ERA_ROLES:
        base = dict(ERA_ROLES[st["role"]])
        base.update({k: v for k, v in st.items() if k != "role"})
        return base
    k = (kind or "man").lower()
    era = st.get("era", era_hint)
    # map legacy style flags
    if era.startswith("185") or era in ("1851", "1850", "1850s"):
        if k in ("woman", "lady"):
            role = "1850s_lady"
        elif k == "girl":
            role = "1850s_girl"
        elif k == "boy":
            role = "1850s_boy"
        elif k in ("soldier",):
            role = "1850s_soldier"
        elif k in ("police", "policeman"):
            role = "1850s_police"
        elif k in ("worker", "workman", "navvy"):
            role = "1850s_navvy" if st.get("tool") or st.get("hat") == "cap" else "1850s_workman"
        elif st.get("hat") == "cap" or st.get("smock"):
            role = "1850s_workman"
        else:
            role = "1850s_gentleman"
    elif era.startswith("188") or era.startswith("189") or era.startswith("190") or era.startswith("191"):
        if k in ("woman", "lady"):
            role = "1890s_lady"
        elif "sail" in k or st.get("sailor"):
            role = "1890s_sailor"
        else:
            role = "1890s_gentleman"
    elif era.startswith("193"):
        if "fire" in k:
            role = "1930s_fireman"
        elif k in ("woman", "lady"):
            role = "1930s_woman"
        else:
            role = "1930s_man"
    else:
        role = "today_casual_f" if k in ("woman", "lady", "girl") else "today_casual_m"
    base = dict(ERA_ROLES[role])
    # honour explicit style overrides from legacy dressing
    if "hat" in st:
        base["hat"] = st["hat"]
    if st.get("frock"):
        base["coat"] = "frock"
    if "skirt_w" in st:
        base["skirt_w"] = st["skirt_w"]
    if st.get("shawl"):
        base["shawl"] = True
    if st.get("cane"):
        base["cane"] = True
    if st.get("tool"):
        base["tool"] = True
    base["role_name"] = role
    return base


# ---------------------------------------------------------------------------
# poses — limb joint angles (radians); arms hang by default facing -Y
# ---------------------------------------------------------------------------

POSES = {
    "standing": dict(L_hip=0.05, R_hip=-0.05, L_knee=0.05, R_knee=0.02,
                     L_shoulder=0.12, R_shoulder=0.12, L_elbow=0.15, R_elbow=0.15,
                     spine=0.0, head=0.0),
    "walking": dict(L_hip=0.35, R_hip=-0.30, L_knee=0.45, R_knee=0.10,
                    L_shoulder=-0.35, R_shoulder=0.40, L_elbow=0.40, R_elbow=0.35,
                    spine=0.04, head=0.0),
    "pointing": dict(L_hip=0.05, R_hip=-0.05, L_knee=0.05, R_knee=0.02,
                     L_shoulder=0.15, R_shoulder=-1.15, L_elbow=0.2, R_elbow=0.15,
                     spine=0.05, head=-0.15),
    "seated": dict(L_hip=1.15, R_hip=1.15, L_knee=1.35, R_knee=1.35,
                   L_shoulder=0.25, R_shoulder=0.25, L_elbow=0.9, R_elbow=0.9,
                   spine=0.12, head=0.05, seat_z=0.48),
    "working": dict(L_hip=0.15, R_hip=-0.10, L_knee=0.25, R_knee=0.15,
                    L_shoulder=-0.7, R_shoulder=-0.85, L_elbow=0.7, R_elbow=0.55,
                    spine=0.18, head=0.2),
    "hauling": dict(L_hip=0.25, R_hip=-0.2, L_knee=0.3, R_knee=0.2,
                    L_shoulder=-1.0, R_shoulder=-1.0, L_elbow=0.35, R_elbow=0.35,
                    spine=0.22, head=0.1),
}


def _lod_seg(lod: str) -> int:
    return {"hero": 12, "mid": 8, "crowd": 6}.get(lod, 8)


# ---------------------------------------------------------------------------
# core builder
# ---------------------------------------------------------------------------

def build_person_bmesh(
    role: dict,
    pose_name: str = "standing",
    lod: str = "mid",
    seed: int = 0,
    height_scale: float = 1.0,
) -> bmesh.types.BMesh:
    """Build an articulated figure into a new BMesh. Material indices:
    0=main(coat/skirt), 1=second(trousers/bodice), 2=skin, 3=hat, 4=trim.
    """
    rng = random.Random(seed)
    sex = role.get("sex", "male")
    if role.get("female_child"):
        sex = "child"
    prop = dict(PROP["female" if sex == "female" else ("child" if sex == "child" else "male")])
    # seeded variation
    hs = height_scale * (0.94 + 0.12 * rng.random())
    for k in ("shoulder_w", "hip_w", "chest_d"):
        prop[k] *= 0.94 + 0.12 * rng.random()
    H = prop["H"] * hs
    seg = _lod_seg(lod)
    pose = dict(POSES.get(pose_name, POSES["standing"]))
    # slight pose jitter
    for k in list(pose.keys()):
        if isinstance(pose[k], float):
            pose[k] += rng.uniform(-0.04, 0.04)

    bm = bmesh.new()

    # ---- landmarks ----
    ankle_z = 0.04 * H
    knee_z = ankle_z + prop["shin"] * hs * 0.55
    hip_z = knee_z + prop["thigh"] * hs * 0.55
    if pose_name == "seated":
        hip_z = pose.get("seat_z", 0.48) * H
        knee_z = hip_z - 0.05 * H
        ankle_z = 0.02 * H
    waist_z = hip_z + 0.08 * H
    chest_z = waist_z + 0.22 * H
    shoulder_z = chest_z + 0.10 * H
    neck_z = shoulder_z + 0.04 * H
    chin_z = neck_z + 0.03 * H
    crown_z = chin_z + prop["head_r"] * 2.1

    sw = prop["shoulder_w"] * 0.5
    hw = prop["hip_w"] * 0.5

    # ---- legs (separate L/R) ----
    def leg(side: float, hip_a: float, knee_a: float, mat_leg: int):
        # hip flare forward(-Y) by hip_a
        hip = Vector((side * hw * 0.85, 0.0, hip_z))
        knee = Vector((side * hw * 0.7, -math.sin(hip_a) * prop["thigh"] * hs * 0.5, knee_z))
        ankle = Vector((side * hw * 0.55,
                        knee.y - math.sin(knee_a) * prop["shin"] * hs * 0.35,
                        ankle_z))
        thigh_r = 0.065 * H if lod != "crowd" else 0.07 * H
        shin_r = 0.048 * H
        _capsule(bm, hip, knee, thigh_r, seg=seg, mat=mat_leg)
        _capsule(bm, knee, ankle, shin_r, seg=max(6, seg - 2), mat=mat_leg)
        # foot
        toe = ankle + Vector((0, -prop["foot"] * hs * 0.55, -0.01 * H))
        if lod == "crowd":
            _box(bm, ankle.x - 0.03 * H, ankle.x + 0.03 * H,
                 toe.y, ankle.y + 0.02 * H, 0.0, 0.035 * H, mat=3)
        else:
            _ellipsoid(bm, Vector((ankle.x, (ankle.y + toe.y) * 0.5, 0.02 * H)),
                       0.04 * H, prop["foot"] * hs * 0.28, 0.025 * H, seg=max(6, seg - 2), mat=3)
        return hip, ankle

    mat_leg = 1 if role.get("trousers") or role.get("skirt") is None else 0
    if role.get("skirt"):
        mat_leg = 0  # skirt covers; still build legs underneath for hero/mid
    if lod == "crowd" and role.get("skirt"):
        # skip individual legs under full skirt for crowd LOD
        pass
    else:
        leg(-1.0, pose["L_hip"], pose["L_knee"], mat_leg)
        leg(1.0, pose["R_hip"], pose["R_knee"], mat_leg)

    # ---- skirt / crinoline / bustle / straight ----
    skirt = role.get("skirt")
    if skirt:
        sw_factor = float(role.get("skirt_w", 1.0))
        if skirt == "crinoline":
            hem_r = 0.38 * H * sw_factor
            mid_r = 0.32 * H * sw_factor
            waist_r = 0.12 * H
            _lathe(bm, [
                (0.0, 0.02 * H), (hem_r, 0.02 * H), (hem_r * 0.98, 0.12 * H),
                (mid_r, hip_z * 0.55), (waist_r * 1.5, hip_z), (waist_r * 1.15, waist_z), (waist_r * 0.95, chest_z - 0.06 * H),
                (0.0, chest_z - 0.05 * H),
            ], seg=seg + 2, mat=0)
        elif skirt == "bustle":
            hem_r = 0.22 * H * sw_factor
            _lathe(bm, [
                (0.0, 0.02 * H), (hem_r, 0.02 * H), (hem_r * 0.9, hip_z * 0.5),
                (0.14 * H, hip_z), (0.12 * H, waist_z), (0.11 * H, chest_z - 0.05 * H), (0.0, chest_z - 0.04 * H),
            ], seg=seg, mat=0)
            # bustle puff rear (+Y historically? our figures face -Y so rear is +Y)
            _ellipsoid(bm, Vector((0, 0.12 * H, hip_z * 0.7)),
                       0.10 * H, 0.12 * H, 0.12 * H, seg=seg, mat=0)
        else:  # straight / today
            hem_r = 0.14 * H * sw_factor
            _lathe(bm, [
                (0.0, 0.02 * H), (hem_r, 0.02 * H), (hem_r * 0.95, hip_z * 0.6),
                (0.11 * H, hip_z), (0.10 * H, waist_z), (0.10 * H, chest_z - 0.05 * H), (0.0, chest_z - 0.04 * H),
            ], seg=seg, mat=0)

    # ---- continuous pelvis → torso (no waist gap) ----
    _ellipsoid(bm, Vector((0, 0.01 * H, (hip_z + waist_z) * 0.5)),
               prop["hip_w"] * 0.48, prop["chest_d"] * 0.50, 0.10 * H, seg=seg, mat=0)
    _capsule(bm, Vector((0, 0.012 * H, hip_z + 0.02 * H)), Vector((0, 0.015 * H, shoulder_z - 0.02 * H)),
             prop["chest_d"] * 0.42, seg=seg, mat=0)
    _ellipsoid(bm, Vector((0, 0.015 * H, chest_z)),
               prop["shoulder_w"] * 0.40, prop["chest_d"] * 0.50, 0.12 * H, seg=seg, mat=0)
    # shoulders bar
    _capsule(bm, Vector((-sw, 0.01 * H, shoulder_z)), Vector((sw, 0.01 * H, shoulder_z)),
             0.045 * H, seg=max(6, seg - 2), mat=0)

    coat = role.get("coat", "frock")
    if coat == "frock":
        # knee-length frock skirts
        _lathe(bm, [
            (0.0, hip_z * 0.55), (0.16 * H, hip_z * 0.55), (0.17 * H, hip_z),
            (0.15 * H, waist_z), (0.0, waist_z + 0.01 * H),
        ], seg=seg, mat=0)
    elif coat == "smock":
        _lathe(bm, [
            (0.0, hip_z * 0.4), (0.18 * H, hip_z * 0.4), (0.20 * H, waist_z),
            (0.16 * H, chest_z), (0.0, chest_z + 0.02 * H),
        ], seg=seg, mat=0)
    elif coat == "waistcoat":
        _lathe(bm, [
            (0.0, waist_z - 0.02 * H), (0.13 * H, waist_z - 0.02 * H),
            (0.14 * H, chest_z), (0.12 * H, shoulder_z - 0.02 * H), (0.0, shoulder_z),
        ], seg=seg, mat=0)
        # shirt sleeves already from arms; add shirt collar hint
    elif coat == "overcoat":
        _lathe(bm, [
            (0.0, 0.08 * H), (0.18 * H, 0.08 * H), (0.20 * H, hip_z),
            (0.18 * H, chest_z), (0.14 * H, shoulder_z), (0.0, shoulder_z + 0.02 * H),
        ], seg=seg, mat=0)
    elif coat == "sailor":
        # jumper + sailor collar (flared rear flap)
        _lathe(bm, [
            (0.0, hip_z * 0.7), (0.14 * H, hip_z * 0.7), (0.15 * H, chest_z),
            (0.13 * H, shoulder_z), (0.0, shoulder_z),
        ], seg=seg, mat=0)
        _box(bm, -0.10 * H, 0.10 * H, 0.02 * H, 0.14 * H, neck_z - 0.02 * H, neck_z + 0.04 * H, mat=1)
    elif coat == "redcoat":
        _lathe(bm, [
            (0.0, hip_z * 0.5), (0.15 * H, hip_z * 0.5), (0.16 * H, waist_z),
            (0.15 * H, chest_z), (0.13 * H, shoulder_z), (0.0, shoulder_z),
        ], seg=seg, mat=0)
    elif coat == "fire":
        _lathe(bm, [
            (0.0, hip_z * 0.45), (0.17 * H, hip_z * 0.45), (0.18 * H, chest_z),
            (0.15 * H, shoulder_z), (0.0, shoulder_z),
        ], seg=seg, mat=0)
    elif coat == "uniform":
        _lathe(bm, [
            (0.0, hip_z * 0.55), (0.14 * H, hip_z * 0.55), (0.15 * H, chest_z),
            (0.13 * H, shoulder_z), (0.0, shoulder_z),
        ], seg=seg, mat=0)
    elif coat == "lounge":
        _lathe(bm, [
            (0.0, hip_z * 0.65), (0.15 * H, hip_z * 0.65), (0.16 * H, chest_z),
            (0.14 * H, shoulder_z), (0.0, shoulder_z),
        ], seg=seg, mat=0)
    elif coat == "tee":
        _lathe(bm, [
            (0.0, waist_z), (0.13 * H, waist_z), (0.14 * H, chest_z),
            (0.12 * H, shoulder_z), (0.0, shoulder_z),
        ], seg=seg, mat=0)

    if role.get("bellbottoms"):
        for s in (-1, 1):
            _lathe(bm, [
                (0.06 * H, 0.0), (0.08 * H, 0.0), (0.05 * H, knee_z * 0.5),
                (0.04 * H, knee_z), (0.0, knee_z),
            ], seg=max(6, seg - 2), ox=s * hw * 0.7, mat=1)

    if role.get("shawl") and lod != "crowd":
        _ellipsoid(bm, Vector((0, -0.02 * H, chest_z)),
                   0.16 * H, 0.08 * H, 0.10 * H, seg=seg, mat=4)

    if role.get("cravat") and lod != "crowd":
        _box(bm, -0.03 * H, 0.03 * H, -0.06 * H, -0.02 * H, neck_z - 0.02 * H, neck_z + 0.03 * H, mat=4)

    if role.get("trim") == "police" and lod != "crowd":
        # belt + buttons strip
        _lathe(bm, [(0.0, waist_z - 0.01 * H), (0.145 * H, waist_z - 0.01 * H),
                    (0.145 * H, waist_z + 0.02 * H), (0.0, waist_z + 0.02 * H)], seg=seg, mat=4)

    # ---- neck + head (separate) ----
    _capsule(bm, Vector((0, 0.01 * H, shoulder_z - 0.01 * H)), Vector((0, 0.015 * H, chin_z + 0.01 * H)),
             0.042 * H, seg=max(6, seg - 2), mat=2)
    head_c = Vector((0, 0.015 * H + pose.get("head", 0) * 0.02, (chin_z + crown_z) * 0.5))
    _ellipsoid(bm, head_c, prop["head_r"] * 0.85, prop["head_r"] * 0.95, prop["head_r"] * 1.05,
               seg=seg, mat=2)
    # simple nose for hero
    if lod == "hero":
        _ellipsoid(bm, head_c + Vector((0, -prop["head_r"] * 0.9, -0.01 * H)),
                   0.015 * H, 0.025 * H, 0.015 * H, seg=6, mat=2)

    # ---- arms + hands (separate) ----
    def arm(side: float, sh_a: float, el_a: float):
        shoulder = Vector((side * sw, 0.01 * H, shoulder_z))
        # sh_a: negative = raise forward (-Y)
        upper_len = prop["upper_arm"] * hs
        fore_len = prop["forearm"] * hs
        elbow = shoulder + Vector((side * 0.04 * H,
                                   -math.sin(-sh_a) * upper_len,
                                   -math.cos(sh_a) * upper_len * 0.85))
        # elbow bend
        hand = elbow + Vector((side * 0.02 * H,
                               -math.sin(-sh_a + el_a) * fore_len,
                               -math.cos(sh_a - el_a * 0.5) * fore_len * 0.7))
        arm_mat = 0 if coat not in ("tee", "smock", "waistcoat") else 2
        if coat in ("smock", "tee", "waistcoat"):
            arm_mat = 2  # sleeves short / skin
        _capsule(bm, shoulder, elbow, 0.045 * H, seg=max(6, seg - 2), mat=arm_mat)
        _capsule(bm, elbow, hand, 0.036 * H, seg=max(6, seg - 2), mat=2)
        # hand
        if lod == "crowd":
            _ellipsoid(bm, hand, 0.025 * H, 0.035 * H, 0.02 * H, seg=6, mat=2)
        else:
            # palm box + thumb stub
            hx, hy, hz = hand.x, hand.y, hand.z
            _box(bm, hx - 0.028 * H, hx + 0.028 * H,
                 hy - 0.045 * H, hy + 0.01 * H,
                 hz - 0.015 * H, hz + 0.015 * H, mat=2)
            if lod == "hero":
                _capsule(bm, hand, hand + Vector((side * 0.03 * H, -0.03 * H, 0.01 * H)),
                         0.012 * H, seg=6, mat=2)
        return hand

    hand_L = arm(-1.0, pose["L_shoulder"], pose["L_elbow"])
    hand_R = arm(1.0, pose["R_shoulder"], pose["R_elbow"])

    # ---- hat ----
    hat = role.get("hat", "top")
    hat_z = crown_z - 0.01 * H
    if hat == "top":
        _lathe(bm, [
            (0.0, hat_z - 0.01 * H), (0.12 * H, hat_z - 0.01 * H), (0.12 * H, hat_z),
            (0.075 * H, hat_z), (0.078 * H, hat_z + 0.16 * H), (0.0, hat_z + 0.16 * H),
        ], seg=seg, mat=3)
    elif hat == "low":
        _lathe(bm, [
            (0.0, hat_z - 0.01 * H), (0.13 * H, hat_z - 0.01 * H), (0.13 * H, hat_z),
            (0.08 * H, hat_z), (0.075 * H, hat_z + 0.09 * H), (0.0, hat_z + 0.09 * H),
        ], seg=seg, mat=3)
    elif hat == "cap":
        _lathe(bm, [
            (0.0, hat_z - 0.005 * H), (0.10 * H, hat_z - 0.005 * H),
            (0.11 * H, hat_z + 0.04 * H), (0.0, hat_z + 0.055 * H),
        ], seg=seg, mat=3)
        _box(bm, -0.06 * H, 0.06 * H, -0.14 * H, -0.08 * H, hat_z - 0.01 * H, hat_z + 0.01 * H, mat=3)
    elif hat == "bonnet":
        _ellipsoid(bm, Vector((0, -0.02 * H, hat_z + 0.02 * H)),
                   0.12 * H, 0.14 * H, 0.08 * H, seg=seg, mat=3)
        if lod != "crowd":
            # brim ribbon
            _box(bm, -0.04 * H, 0.04 * H, -0.12 * H, -0.05 * H, chin_z, chin_z + 0.08 * H, mat=4)
    elif hat == "boater":
        _lathe(bm, [
            (0.0, hat_z - 0.005 * H), (0.14 * H, hat_z - 0.005 * H), (0.14 * H, hat_z),
            (0.09 * H, hat_z), (0.09 * H, hat_z + 0.055 * H), (0.0, hat_z + 0.055 * H),
        ], seg=seg, mat=3)
        if lod != "crowd":
            _lathe(bm, [(0.085 * H, hat_z + 0.02 * H), (0.092 * H, hat_z + 0.02 * H),
                        (0.092 * H, hat_z + 0.04 * H), (0.085 * H, hat_z + 0.04 * H)], seg=seg, mat=4)
    elif hat == "sailor":
        _lathe(bm, [
            (0.0, hat_z - 0.005 * H), (0.11 * H, hat_z - 0.005 * H),
            (0.10 * H, hat_z + 0.05 * H), (0.0, hat_z + 0.055 * H),
        ], seg=seg, mat=3)
    elif hat == "trilby":
        _lathe(bm, [
            (0.0, hat_z - 0.008 * H), (0.13 * H, hat_z - 0.008 * H), (0.12 * H, hat_z),
            (0.08 * H, hat_z), (0.07 * H, hat_z + 0.08 * H), (0.0, hat_z + 0.09 * H),
        ], seg=seg, mat=3)
    elif hat == "shako":
        _lathe(bm, [
            (0.0, hat_z - 0.005 * H), (0.09 * H, hat_z - 0.005 * H),
            (0.095 * H, hat_z + 0.18 * H), (0.0, hat_z + 0.18 * H),
        ], seg=seg, mat=3)
        if lod != "crowd":
            _box(bm, -0.02 * H, 0.02 * H, -0.10 * H, -0.08 * H, hat_z + 0.05 * H, hat_z + 0.18 * H, mat=4)
    elif hat == "helmet":
        _ellipsoid(bm, Vector((0, 0, hat_z + 0.06 * H)), 0.11 * H, 0.13 * H, 0.09 * H, seg=seg, mat=3)
        _box(bm, -0.015 * H, 0.015 * H, -0.02 * H, 0.02 * H, hat_z + 0.12 * H, hat_z + 0.22 * H, mat=3)
    elif hat == "beret":
        _ellipsoid(bm, Vector((0.02 * H, 0, hat_z + 0.02 * H)), 0.11 * H, 0.11 * H, 0.04 * H, seg=seg, mat=3)
    elif hat == "peak":
        _lathe(bm, [
            (0.0, hat_z - 0.005 * H), (0.10 * H, hat_z - 0.005 * H),
            (0.10 * H, hat_z + 0.06 * H), (0.0, hat_z + 0.07 * H),
        ], seg=seg, mat=3)
        _box(bm, -0.07 * H, 0.07 * H, -0.14 * H, -0.08 * H, hat_z - 0.01 * H, hat_z + 0.01 * H, mat=3)
    # else none

    # ---- props: cane / tool ----
    if role.get("cane") and lod != "crowd":
        _capsule(bm, hand_R + Vector((0.02 * H, 0, 0)), Vector((hand_R.x + 0.02 * H, hand_R.y, 0.02 * H)),
                 0.012 * H, seg=6, mat=3)
    if role.get("tool") and pose_name in ("working", "hauling", "standing") and lod != "crowd":
        # simple hammer / bar in right hand
        tip = hand_R + Vector((0.02 * H, -0.25 * H, 0.05 * H))
        _capsule(bm, hand_R, tip, 0.015 * H, seg=6, mat=3)
        if lod == "hero":
            _box(bm, tip.x - 0.04 * H, tip.x + 0.04 * H,
                 tip.y - 0.03 * H, tip.y + 0.03 * H,
                 tip.z - 0.02 * H, tip.z + 0.05 * H, mat=4)

    # smooth
    for f in bm.faces:
        f.smooth = True
    try:
        bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    except Exception:
        pass
    return bm


def person_mesh(
    name: str,
    kind: str = "man",
    mats: Optional[Sequence] = None,
    FT: float = 0.3048,  # noqa: ARG001 — kept for drop-in compat with legacy callers
    style: Optional[dict] = None,
    pose: Optional[str] = None,
    lod: Optional[str] = None,
    seed: Optional[int] = None,
    era: str = "1850s",
) -> bpy.types.Mesh:
    """Drop-in replacement for figures.person_mesh. Returns a Mesh with up to 5 material slots."""
    sid = _seed_of(name, seed)
    role = resolve_role(kind, style, era_hint=era)
    pose_name = pose or (style or {}).get("pose") or "standing"
    lod_name = lod or (style or {}).get("lod") or "mid"
    bm = build_person_bmesh(role, pose_name=pose_name, lod=lod_name, seed=sid)
    me = bpy.data.meshes.new(name)
    bm.to_mesh(me)
    bm.free()
    # materials
    use_mats = list(mats) if mats else _default_mats(sid)
    while len(use_mats) < 5:
        use_mats.append(use_mats[-1] if use_mats else _default_mats(sid)[0])
    # Ensure workman/navvy main cloth is earthy (not washed linen white)
    rn = role.get("role_name", "")
    if rn in ("1850s_workman", "1850s_navvy", "1850s_police") and (mats is None or len([m for m in use_mats if m]) < 2):
        use_mats[0] = _ensure_mat(f"CPL_PPL_work_{sid % 5}", [
            (0.22, 0.20, 0.16), (0.18, 0.16, 0.14), (0.28, 0.24, 0.18),
            (0.16, 0.18, 0.20), (0.24, 0.18, 0.12)][sid % 5], 0.7)
        use_mats[1] = _ensure_mat(f"CPL_PPL_trou_{sid % 3}", [
            (0.12, 0.12, 0.14), (0.16, 0.14, 0.12), (0.10, 0.10, 0.12)][sid % 3], 0.65)
    for m in use_mats[:5]:
        if m is not None:
            me.materials.append(m)
    me["cpl_people"] = PEOPLE_VERSION
    me["cpl_role"] = role.get("role_name", "")
    me["cpl_pose"] = pose_name
    me["cpl_lod"] = lod_name
    return me


# ---------------------------------------------------------------------------
# scene swap — replace lathe crowds with v2 meshes (render-time, not saved)
# ---------------------------------------------------------------------------

_MESH_CACHE: Dict[Tuple, bpy.types.Mesh] = {}


def _infer_kind_role(ob: bpy.types.Object) -> Tuple[str, dict]:
    n = ob.name.upper()
    style: dict = {}
    if any(k in n for k in ("WOMAN", "CROWD_F", "CROWD_CL_F", "LADY", "QUEUE_F", "GIRL")):
        kind = "girl" if "GIRL" in n else "woman"
    elif "BOY" in n:
        kind = "boy"
    elif "POLICE" in n:
        kind = "police"; style["role"] = "1850s_police"
    elif any(k in n for k in ("SOLDIER", "GUARD")):
        kind = "soldier"; style["role"] = "1850s_soldier"
    elif any(k in n for k in ("SAILOR", "RND")):
        kind = "man"; style["role"] = "1890s_sailor"
    elif "FIRE" in n:
        kind = "man"; style["role"] = "1930s_fireman"
    elif any(k in n for k in (
        "WORK", "KWORKER", "NAVVY", "ATTEND", "MONEY", "BUILDER", "CARPENTER",
        "CARRY", "CARTER", "ENGINE", "PAINT", "LAYER", "FOOT_", "EXHIBITOR", "HAMMER",
    )):
        kind = "workman"; style["role"] = "1850s_navvy"; style["tool"] = True; style["hat"] = "cap"
    elif any(k in n for k in ("ENTERING", "CROWD_M", "QUEUE_M", "MAN", "STAIR", "CROWD_CL")):
        # CROWD_CL_* closing crowd: seed sex
        if "CROWD_CL" in n:
            kind = "woman" if (_seed_of(ob.name) % 2) else "man"
        else:
            kind = "man"
    elif n.startswith("VIS_"):
        kind = "woman" if (_seed_of(ob.name) % 3 == 0) else "man"
    else:
        kind = "woman" if (_seed_of(ob.name) % 2) else "man"
    return kind, style


def _infer_pose(ob: bpy.types.Object) -> str:
    n = ob.name.upper()
    if any(k in n for k in ("SIT", "SEAT", "BENCH")):
        return "seated"
    if any(k in n for k in ("POINT", "GESTURE", "ATTEND")):
        return "pointing"
    if any(k in n for k in ("WORK", "HAMMER", "TOOL", "NAVVY", "PAINT", "LAYER", "ENGINE", "KWORKER")):
        return "working"
    if any(k in n for k in ("CARRY", "CARTER")):
        return "hauling"
    if any(k in n for k in ("HAUL", "CARRY", "LIFT")):
        return "hauling"
    if any(k in n for k in ("WALK", "ENTER", "QUEUE")):
        return "walking"
    # seeded standing/walking mix for crowds
    return "walking" if (_seed_of(ob.name) % 5 == 0) else "standing"


def _lod_for_distance(dist: float, hero_n: int, mid_n: int, idx: int) -> str:
    if idx < hero_n and dist < 12.0:
        return "hero"
    if idx < hero_n + mid_n and dist < 35.0:
        return "mid"
    return "crowd"


def swap_scene_people(
    era: str = "1851",
    camera: Optional[bpy.types.Object] = None,
    seed: int = 0,
    max_hero: int = 10,
    max_mid: int = 60,
    kinds: Sequence[str] = ("figure", "worker", "person", "crowd"),
) -> dict:
    """Replace mesh datablocks on figure objects with people v2. Does not save the .blend.
    Hides legacy figure_arm extras (arms are built into v2). Returns stats dict.
    """
    cam = camera or bpy.context.scene.camera
    cam_loc = cam.matrix_world.translation if cam else Vector((0, 0, 1.6))
    era_hint = "1850s"
    if str(era).startswith("193"):
        era_hint = "1930s"
    elif str(era).startswith(("188", "189", "190", "191")):
        era_hint = "1890s"
    elif str(era) in ("today", "2020", "modern", "2010"):
        era_hint = "today"

    NAME_PREFIXES = (
        "CROWD", "QUEUE", "VIS", "FIG_", "PERSON", "WORKER", "KWORKER", "POLICE",
        "ATTEND", "CARRY", "CARTER", "ENGINE", "PAINTER", "PAINT_", "EXHIBITOR",
        "LAYER", "FOOT_", "MONEY", "ENTERING", "STAIR", "NAVVY", "SAILOR",
    )
    figs = [o for o in bpy.data.objects
            if o.type == "MESH" and not o.hide_render
            and (o.get("part_kind") in kinds
                 or any(o.name.upper().startswith(p) for p in NAME_PREFIXES))]

    # sort by distance to camera — nearest get hero LOD
    def dist(o):
        return (o.matrix_world.translation - cam_loc).length
    figs.sort(key=dist)

    # hide separate arms
    n_arms = 0
    for o in bpy.data.objects:
        if o.get("part_kind") == "figure_arm" or o.name.upper().endswith("_ARM"):
            if any(o.name.upper().startswith(p) or (o.parent and o.parent in figs)
                   for p in ("ATTEND", "CROWD", "QUEUE", "WORK")):
                o.hide_render = True
                o.hide_viewport = True
                n_arms += 1

    stats = dict(version=PEOPLE_VERSION, n=0, hero=0, mid=0, crowd=0, cache=0, arms_hidden=n_arms)
    # reuse materials from first figure when possible
    for idx, ob in enumerate(figs):
        d = dist(ob)
        lod = _lod_for_distance(d, max_hero, max_mid, idx)
        kind, style = _infer_kind_role(ob)
        # era override for modern park etc.
        if era_hint == "today":
            style["era"] = "today"
        elif era_hint != "1850s" and "role" not in style:
            style["era"] = era_hint
        pose = _infer_pose(ob)
        style["pose"] = pose
        sid = _seed_of(ob.name, seed + idx)
        role = resolve_role(kind, style, era_hint=era_hint)
        cache_key = (role.get("role_name"), pose, lod, sid % 24)  # 24 body variants
        me = _MESH_CACHE.get(cache_key)
        if me is None:
            # build with materials from object if present
            mats = [s.material for s in ob.material_slots] if ob.material_slots else None
            # Drop blown-out pale mains (common on smock lathes) so v2 uses earthy cloth
            if mats:
                def _too_pale(m):
                    if m is None: return True
                    try:
                        c = m.diffuse_color
                        return (c[0] + c[1] + c[2]) / 3.0 > 0.55
                    except Exception:
                        return False
                if _too_pale(mats[0] if mats else None):
                    mats = None  # fall back to role-aware defaults
            me = person_mesh(f"CPL_PPL_{cache_key[0]}_{pose}_{lod}_{sid % 24}",
                             kind=kind, mats=mats, style=style, pose=pose, lod=lod,
                             seed=sid, era=era_hint)
            _MESH_CACHE[cache_key] = me
        else:
            stats["cache"] += 1
        old = ob.data
        ob.data = me
        # Prefer mesh (DATA) materials from the new figure — object overrides
        # often left pale linen on the wrong slots after a lathe→v2 swap.
        for slot in ob.material_slots:
            try:
                slot.link = "DATA"
            except Exception:
                pass
        ob[PEOPLE_TAG] = PEOPLE_VERSION
        ob["cpl_lod"] = lod
        stats["n"] += 1
        stats[lod] = stats.get(lod, 0) + 1
        # old mesh may become orphan — leave for Blender; don't delete shared
        _ = old
    return stats


def clear_mesh_cache():
    _MESH_CACHE.clear()


# ---------------------------------------------------------------------------
# catalogue helpers for README / previews
# ---------------------------------------------------------------------------

def catalogue() -> List[dict]:
    rows = []
    for role_name, role in ERA_ROLES.items():
        for pose in POSES:
            for lod in ("hero", "mid", "crowd"):
                rows.append({"role": role_name, "pose": pose, "lod": lod, **{k: role[k] for k in ("era", "sex")}})
    return rows
