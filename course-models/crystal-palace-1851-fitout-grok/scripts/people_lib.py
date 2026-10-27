"""crystal-palace-people v3.1 — HBM base humans + period-correct modelled garments.

Drop-in API (compatible with v2 callers):
  person_mesh(name, kind, mats, FT=0.3048, style=None, pose=None, lod=None, seed=None)
  swap_scene_people(era="1851", camera=None, seed=0)

Bases: Blender Studio Human Base Meshes v1.4.1 (CC0), realistic male/female,
decimated LODs under people/vendor/bases/. Garments are modelled shells
(frock coat with tails, top hat, crinoline, bodice, bonnet, shawl, smock,
police tunic) — not lathe primitives. Proportions: head ~1/7.5 height;
1850s crowd height 5'0"–5'10". Matte period colours; no white hats.
Crowd mix: ~58% ladies (wide crinoline) so silhouettes read at mid-distance.
"""
from __future__ import annotations
import hashlib, math, os, random
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence, Tuple

import bpy
import bmesh
from mathutils import Matrix, Vector, Euler

PEOPLE_VERSION = "3.1"
PEOPLE_TAG = "cpl_people_v3"

_HERE = Path(__file__).resolve().parent
_SURVEY_PEOPLE = Path("/workspace/crystal-palace-survey/people")
# Prefer local vendor/ (canonical tree); fall back to survey people/ when vendored into grok scripts/
_BASES = _HERE / "vendor" / "bases"
if not _BASES.exists():
    _BASES = _SURVEY_PEOPLE / "vendor" / "bases"

# metres
INCH = 0.0254
FT = 0.3048
HEIGHT_MIN = 5.0 * FT          # 5'0"
HEIGHT_MAX = 5.0 * FT + 10*INCH  # 5'10"
HEAD_RATIO = 1.0 / 7.5
TOP_HAT_H = 7.0 * INCH         # ~7 in crown
HEAD_CIRC = 22.0 * INCH
HEAD_DIAM = HEAD_CIRC / math.pi

POSES = ("standing", "walking", "pointing", "seated", "working", "hauling")

ERA_ROLES = {
    "1850s": ("1850s_gentleman", "1850s_lady", "1850s_workman", "1850s_navvy",
              "1850s_police", "1850s_soldier", "1850s_boy", "1850s_girl"),
    "1851":  ("1850s_gentleman", "1850s_lady", "1850s_workman", "1850s_navvy",
              "1850s_police", "1850s_soldier", "1850s_boy", "1850s_girl"),
    "1890s": ("1890s_gentleman", "1890s_lady", "1890s_sailor", "1890s_uniform"),
    "1880s": ("1890s_gentleman", "1890s_lady", "1890s_sailor", "1890s_uniform"),
    "1910s": ("1890s_gentleman", "1890s_lady", "1890s_sailor", "1890s_uniform"),
    "1930s": ("1930s_man", "1930s_woman", "1930s_fireman"),
    "today": ("today_casual_m", "today_casual_f"),
}

_MESH_CACHE: Dict[Tuple, bpy.types.Mesh] = {}


# ---------------------------------------------------------------------------
# materials — matte period fabric; NO white hats
# ---------------------------------------------------------------------------

def _ensure_mat(name: str, color: Tuple[float, float, float], rough: float = 0.72) -> bpy.types.Material:
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
        if "Specular IOR Level" in bsdf.inputs:
            bsdf.inputs["Specular IOR Level"].default_value = 0.15
        elif "Specular" in bsdf.inputs:
            bsdf.inputs["Specular"].default_value = 0.15
    m.diffuse_color = (*color, 1.0)
    return m


# Dark coats dominant; skirts mid-tone but never chalk white; hats black/brown/navy
_COATS = [
    (0.05, 0.05, 0.06), (0.08, 0.06, 0.05), (0.04, 0.05, 0.045),
    (0.10, 0.08, 0.07), (0.06, 0.06, 0.08), (0.11, 0.05, 0.05),
    (0.07, 0.07, 0.06), (0.08, 0.08, 0.09),
]
_SKIRTS = [
    (0.28, 0.12, 0.14), (0.12, 0.18, 0.28), (0.34, 0.28, 0.20),
    (0.16, 0.20, 0.14), (0.26, 0.14, 0.22), (0.30, 0.24, 0.14),
    (0.14, 0.14, 0.18), (0.36, 0.30, 0.24),
]
_TROUS = [(0.08, 0.08, 0.10), (0.12, 0.11, 0.10), (0.06, 0.07, 0.10)]
_SKINS = [(0.62, 0.46, 0.38), (0.48, 0.34, 0.28), (0.70, 0.55, 0.44), (0.40, 0.28, 0.22)]
_HATS = [(0.04, 0.04, 0.05), (0.10, 0.08, 0.06), (0.06, 0.07, 0.10), (0.12, 0.09, 0.05)]  # never white
_BONNETS = [(0.18, 0.12, 0.08), (0.10, 0.10, 0.12), (0.22, 0.16, 0.10), (0.14, 0.08, 0.08)]
_SMOCKS = [(0.42, 0.40, 0.34), (0.35, 0.36, 0.32), (0.48, 0.44, 0.36)]  # drab linen, not chalk
_POLICE = (0.05, 0.08, 0.16)


def _mats_for(seed: int, role: str) -> Dict[str, bpy.types.Material]:
    rng = random.Random(seed)
    i = rng.randrange(8)
    skin = _ensure_mat(f"CPL3_skin_{seed % 4}", _SKINS[seed % 4], 0.55)
    if "lady" in role or "girl" in role or role.endswith("_f") or "woman" in role:
        main = _ensure_mat(f"CPL3_skirt_{i}", _SKIRTS[i], 0.75)
        sec = _ensure_mat(f"CPL3_bodice_{i}", _COATS[(i + 3) % 8], 0.7)
        hat = _ensure_mat(f"CPL3_bonnet_{i % 4}", _BONNETS[i % 4], 0.8)
    elif "police" in role:
        main = _ensure_mat("CPL3_police", _POLICE, 0.7)
        sec = _ensure_mat(f"CPL3_trou_{i % 3}", _TROUS[i % 3], 0.75)
        hat = _ensure_mat(f"CPL3_hat_{i % 4}", _HATS[i % 4], 0.7)
    elif "workman" in role or "navvy" in role or "fireman" in role:
        main = _ensure_mat(f"CPL3_smock_{i % 3}", _SMOCKS[i % 3], 0.85)
        sec = _ensure_mat(f"CPL3_trou_{i % 3}", _TROUS[i % 3], 0.8)
        hat = _ensure_mat(f"CPL3_hat_{i % 4}", _HATS[i % 4], 0.75)
    elif "sailor" in role:
        main = _ensure_mat("CPL3_navy", (0.06, 0.10, 0.18), 0.7)
        sec = _ensure_mat("CPL3_bell", (0.08, 0.08, 0.10), 0.7)
        hat = _ensure_mat("CPL3_sailorcap", (0.05, 0.05, 0.06), 0.7)
    else:
        main = _ensure_mat(f"CPL3_coat_{i}", _COATS[i], 0.7)
        sec = _ensure_mat(f"CPL3_trou_{i % 3}", _TROUS[i % 3], 0.75)
        hat = _ensure_mat(f"CPL3_hat_{i % 4}", _HATS[i % 4], 0.65)
    # waistcoat / cravat / shirt peek — mid tones, never chalk
    _WAIST = [(0.28, 0.22, 0.16), (0.18, 0.20, 0.24), (0.32, 0.18, 0.14),
              (0.22, 0.22, 0.20), (0.35, 0.30, 0.22)]
    trim = _ensure_mat(f"CPL3_waist_{i % 5}", _WAIST[i % 5], 0.65)
    return {"main": main, "sec": sec, "skin": skin, "hat": hat, "trim": trim}


# ---------------------------------------------------------------------------
# base body load
# ---------------------------------------------------------------------------

def _sex_for(role: str) -> str:
    if any(k in role for k in ("lady", "girl", "woman", "_f")):
        return "female"
    return "male"


def _height_for(role: str, seed: int) -> float:
    rng = random.Random(seed + 17)
    if "boy" in role or "girl" in role:
        return rng.uniform(1.15, 1.40)
    if _sex_for(role) == "female":
        # 1850s women often ~5'0"–5'4"
        return rng.uniform(HEIGHT_MIN, 5.0 * FT + 4 * INCH)
    return rng.uniform(5.0 * FT + 4 * INCH, HEIGHT_MAX)


def _lod_suffix(lod: str) -> str:
    return {"hero": "_hero", "mid": "_mid", "crowd": "_crowd"}.get(lod, "_mid")


def _import_base(sex: str, lod: str) -> bpy.types.Object:
    """Import realistic HBM body OBJ (CC0); falls back to stylized if missing."""
    suf = _lod_suffix(lod)
    path = _BASES / f"{sex}_realistic{suf}.obj"
    if not path.exists():
        path = _BASES / f"{sex}_realistic_mid.obj"
    if not path.exists():
        path = _BASES / f"{sex}_stylized{suf}.obj"
    if not path.exists():
        path = _BASES / f"{sex}_stylized_mid.obj"
    if not path.exists():
        raise FileNotFoundError(f"missing base mesh {path}")
    before = set(bpy.data.objects)
    # Blender 4+/5
    try:
        bpy.ops.wm.obj_import(filepath=str(path))
    except Exception:
        bpy.ops.import_scene.obj(filepath=str(path))
    new = [o for o in bpy.data.objects if o not in before]
    if not new:
        raise RuntimeError(f"OBJ import produced nothing: {path}")
    obj = new[0]
    for extra in new[1:]:
        bpy.data.objects.remove(extra, do_unlink=True)
    # center XY on origin, feet at z=0
    bbox = [obj.matrix_world @ Vector(c) for c in obj.bound_box]
    xs = [v.x for v in bbox]; ys = [v.y for v in bbox]; zs = [v.z for v in bbox]
    cx = 0.5 * (min(xs) + max(xs))
    cy = 0.5 * (min(ys) + max(ys))
    zmin = min(zs)
    obj.location -= Vector((cx, cy, zmin))
    bpy.context.view_layer.objects.active = obj
    obj.select_set(True)
    bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
    return obj


def _scale_to_height(obj: bpy.types.Object, target_h: float) -> float:
    zs = [(obj.matrix_world @ Vector(c)).z for c in obj.bound_box]
    h = max(zs) - min(zs)
    if h < 1e-6:
        return 1.0
    s = target_h / h
    obj.scale = (s, s, s)
    bpy.context.view_layer.objects.active = obj
    obj.select_set(True)
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    # re-ground
    zs = [(obj.matrix_world @ Vector(c)).z for c in obj.bound_box]
    obj.location.z -= min(zs)
    bpy.ops.object.transform_apply(location=True, rotation=False, scale=False)
    return s



def _enforce_head_ratio(obj: bpy.types.Object, target_ratio: float = HEAD_RATIO):
    """Scale head verts about the neck so head height ~= target_ratio * body height.
    Neck is detected as the narrowest XY ring between 78–88% of height."""
    me = obj.data
    zs = [v.co.z for v in me.vertices]
    z0, z1 = min(zs), max(zs)
    h = z1 - z0
    if h < 1e-6:
        return
    # find neck: sample bands, pick min mean radius
    best_z, best_r = z0 + 0.82 * h, 1e9
    for i in range(12):
        zc = z0 + (0.78 + 0.01 * i) * h
        ring = [v for v in me.vertices if abs(v.co.z - zc) < 0.012]
        if len(ring) < 6:
            continue
        rs = [((v.co.x) ** 2 + (v.co.y) ** 2) ** 0.5 for v in ring]
        r = sum(rs) / len(rs)
        if r < best_r:
            best_r, best_z = r, zc
    neck_z = best_z
    head_h = z1 - neck_z
    want = target_ratio * h
    if head_h < 1e-6:
        return
    s = want / head_h
    # shrink oversized heads; mild enlarge if head is tiny
    if 0.92 <= s <= 1.05:
        return
    s = max(0.55, min(1.15, s))
    # keep neck XY centroid
    neck_ring = [v for v in me.vertices if abs(v.co.z - neck_z) < 0.02]
    cx = sum(v.co.x for v in neck_ring) / max(1, len(neck_ring))
    cy = sum(v.co.y for v in neck_ring) / max(1, len(neck_ring))
    neck = Vector((cx, cy, neck_z))
    for v in me.vertices:
        if v.co.z >= neck_z - 0.005:
            delta = v.co - neck
            v.co = neck + Vector((delta.x * s, delta.y * s, delta.z * s))
    me.update()


def _landmarks(obj: bpy.types.Object) -> Dict[str, float]:
    """Z landmarks as fractions of height (feet=0)."""
    zs = [v.co.z for v in obj.data.vertices]
    z0, z1 = min(zs), max(zs)
    h = z1 - z0
    return {
        "z0": z0, "z1": z1, "h": h,
        "ankle": z0 + 0.04 * h,
        "knee": z0 + 0.28 * h,
        "hip": z0 + 0.50 * h,
        "waist": z0 + 0.58 * h,
        "chest": z0 + 0.72 * h,
        "shoulder": z0 + 0.80 * h,
        "chin": z0 + 0.86 * h,
        "crown": z1,
        "head_h": h * HEAD_RATIO,
    }


# ---------------------------------------------------------------------------
# garment builders (modelled shells, not lathe pegs)
# ---------------------------------------------------------------------------

def _new_bm():
    return bmesh.new()


def _finish_mesh(bm: bmesh.types.BMesh, name: str) -> bpy.types.Mesh:
    me = bpy.data.meshes.new(name)
    bm.to_mesh(me)
    bm.free()
    me.update()
    return me


def _ring(bm, cx, cy, z, rx, ry, seg, mat=0):
    vs = []
    for k in range(seg):
        a = 2 * math.pi * k / seg
        vs.append(bm.verts.new((cx + math.cos(a) * rx, cy + math.sin(a) * ry, z)))
    return vs


def _bridge(bm, A, B, mat=0):
    n = len(A)
    for k in range(n):
        f = bm.faces.new([A[k], A[(k + 1) % n], B[(k + 1) % n], B[k]])
        f.material_index = mat


def _cap(bm, ring, tip, mat=0):
    tv = tip if isinstance(tip, bmesh.types.BMVert) else bm.verts.new(tip)
    n = len(ring)
    for k in range(n):
        f = bm.faces.new([ring[k], ring[(k + 1) % n], tv])
        f.material_index = mat
    return tv


def _lathed_shell(bm, profile, seg=12, mat=0, cx=0.0, cy=0.0):
    """profile: list of (radius_x, radius_y, z)."""
    rings = [_ring(bm, cx, cy, z, rx, ry, seg) for rx, ry, z in profile]
    for A, B in zip(rings, rings[1:]):
        _bridge(bm, A, B, mat)
    return rings


def build_top_hat(bm, crown_z, head_r, mat=0, seg=12):
    """Period silk top hat: ~7 in crown, clear flat brim (not a fez/cap)."""
    head_r = max(0.078, min(head_r, 0.105))
    crown_r = head_r * 0.98
    brim_r = head_r * 1.75          # wide readable brim
    h = TOP_HAT_H
    scalp = crown_z - 0.018
    # thick brim slab (top + bottom faces) so it reads at crowd distance
    brim_z_lo = scalp - 0.012
    brim_z_hi = scalp - 0.002
    outer_lo = _ring(bm, 0, 0, brim_z_lo, brim_r, brim_r, seg)
    outer_hi = _ring(bm, 0, 0, brim_z_hi, brim_r, brim_r, seg)
    inner_lo = _ring(bm, 0, 0, brim_z_lo, crown_r, crown_r, seg)
    inner_hi = _ring(bm, 0, 0, brim_z_hi, crown_r, crown_r, seg)
    n = seg
    for k in range(n):
        # top of brim
        f = bm.faces.new([outer_hi[k], outer_hi[(k + 1) % n], inner_hi[(k + 1) % n], inner_hi[k]])
        f.material_index = mat
        # bottom of brim
        f = bm.faces.new([outer_lo[(k + 1) % n], outer_lo[k], inner_lo[k], inner_lo[(k + 1) % n]])
        f.material_index = mat
        # outer rim
        f = bm.faces.new([outer_lo[k], outer_lo[(k + 1) % n], outer_hi[(k + 1) % n], outer_hi[k]])
        f.material_index = mat
    # crown cylinder — slightly tapered
    bot = _ring(bm, 0, 0, scalp, crown_r, crown_r, seg)
    top = _ring(bm, 0, 0, scalp + h, crown_r * 0.92, crown_r * 0.92, seg)
    _bridge(bm, bot, top, mat)
    _bridge(bm, inner_hi, bot, mat)
    _cap(bm, top, (0, 0, scalp + h + 0.008), mat)


def build_boater(bm, crown_z, head_r, mat=0, seg=12):
    crown_r = head_r * 0.95
    brim_r = head_r * 1.55
    h = 0.055
    brim_z = crown_z - 0.005
    outer = _ring(bm, 0, 0, brim_z, brim_r, brim_r, seg)
    inner = _ring(bm, 0, 0, brim_z, crown_r, crown_r, seg)
    n = seg
    for k in range(n):
        f = bm.faces.new([outer[k], outer[(k + 1) % n], inner[(k + 1) % n], inner[k]])
        f.material_index = mat
    top = _ring(bm, 0, 0, crown_z + h, crown_r, crown_r, seg)
    bot = _ring(bm, 0, 0, crown_z, crown_r, crown_r, seg)
    _bridge(bm, bot, top, mat)
    _cap(bm, top, (0, 0, crown_z + h + 0.002), mat)


def build_trilby(bm, crown_z, head_r, mat=0, seg=12):
    crown_r = head_r * 0.95
    brim_r = head_r * 1.4
    h = 0.10
    # pinched crown: oval
    brim_z = crown_z - 0.008
    outer = _ring(bm, 0, 0, brim_z, brim_r * 1.05, brim_r * 0.9, seg)
    inner = _ring(bm, 0, 0, brim_z, crown_r, crown_r * 0.9, seg)
    n = seg
    for k in range(n):
        f = bm.faces.new([outer[k], outer[(k + 1) % n], inner[(k + 1) % n], inner[k]])
        f.material_index = mat
    top = _ring(bm, 0, 0, crown_z + h, crown_r * 0.85, crown_r * 0.7, seg)
    bot = _ring(bm, 0, 0, crown_z, crown_r, crown_r * 0.9, seg)
    _bridge(bm, bot, top, mat)
    _cap(bm, top, (0, 0, crown_z + h + 0.01), mat)


def build_cap(bm, crown_z, head_r, mat=0, seg=10):
    """Cloth / peaked workman's cap — low profile, dark."""
    r = head_r * 1.05
    h = 0.045
    scalp = crown_z - 0.02
    bot = _ring(bm, 0, 0, scalp, r, r, seg)
    top = _ring(bm, 0, 0.01, scalp + h, r * 0.7, r * 0.7, seg)
    _bridge(bm, bot, top, mat)
    _cap(bm, top, (0, 0.02, scalp + h + 0.01), mat)
    # small peak
    peak = [
        bm.verts.new((0, r * 0.2, scalp)),
        bm.verts.new((-r * 0.35, r * 1.15, scalp - 0.005)),
        bm.verts.new((r * 0.35, r * 1.15, scalp - 0.005)),
    ]
    f = bm.faces.new(peak); f.material_index = mat


def build_bonnet(bm, chin_z, crown_z, head_r, mat=0, seg=10):
    """1850s bonnet: rear hood + cheek sides; face fully open."""
    r = head_r * 1.0
    cy = -head_r * 0.40
    rings = []
    for t, sc, yoff in ((0.20, 0.80, 0.0), (0.55, 1.0, -0.02), (0.90, 0.85, -0.03), (1.12, 0.40, -0.02)):
        z = chin_z + t * (crown_z + 0.03 - chin_z)
        rings.append(_ring(bm, 0, cy + yoff, z, r * sc * 0.50, r * sc * 0.45, seg))
    for A, B in zip(rings, rings[1:]):
        _bridge(bm, A, B, mat)
    _cap(bm, rings[-1], (0, cy - 0.02, crown_z + 0.04), mat)
    # cheek ties / side panels (left & right), not over the face
    for sign in (-1.0, 1.0):
        vs = [
            bm.verts.new((sign * head_r * 0.55, -head_r * 0.1, chin_z + 0.04)),
            bm.verts.new((sign * head_r * 0.70, head_r * 0.15, chin_z + 0.08)),
            bm.verts.new((sign * head_r * 0.55, head_r * 0.05, crown_z - 0.02)),
            bm.verts.new((sign * head_r * 0.35, -head_r * 0.25, crown_z - 0.04)),
        ]
        try:
            f = bm.faces.new(vs); f.material_index = mat
        except ValueError:
            pass


def build_frock_coat(bm, L, shoulder_w, mat=0, seg=12):
    """Fitted torso + flared skirted tails to mid-thigh."""
    sw = shoulder_w * 0.55
    chest_r = sw * 0.95
    waist_r = sw * 0.78
    hip_r = sw * 0.88
    # torso shell
    profile = [
        (chest_r * 0.55, chest_r * 0.4, L["shoulder"] + 0.02),  # collar base
        (chest_r, chest_r * 0.7, L["chest"]),
        (waist_r, waist_r * 0.7, L["waist"]),
        (hip_r, hip_r * 0.65, L["hip"] + 0.02),
    ]
    rings = _lathed_shell(bm, profile, seg=seg, mat=mat)
    # collar
    collar_bot = rings[0]
    collar_top = _ring(bm, 0, 0, L["shoulder"] + 0.06, chest_r * 0.5, chest_r * 0.38, seg)
    _bridge(bm, collar_bot, collar_top, mat)
    # tails: rear half panels from waist to mid-thigh, flared back
    tail_z0 = L["waist"]
    tail_z1 = L["hip"] - 0.12 * L["h"]
    # left and right rear tails as extruded quads (simplified solid)
    for sign in (-1, 1):
        x0 = sign * waist_r * 0.15
        x1 = sign * hip_r * 0.95
        # outer rear
        vs = [
            bm.verts.new((x0, -waist_r * 0.5, tail_z0)),
            bm.verts.new((x1, -hip_r * 1.05, tail_z0)),
            bm.verts.new((x1 * 1.05, -hip_r * 1.25, tail_z1)),
            bm.verts.new((sign * 0.02, -hip_r * 0.7, tail_z1)),
        ]
        # thicken slightly in Y
        vs2 = [
            bm.verts.new((v.co.x, v.co.y + 0.025, v.co.z)) for v in vs
        ]
        try:
            f = bm.faces.new(vs); f.material_index = mat
            f = bm.faces.new(list(reversed(vs2))); f.material_index = mat
            for i in range(4):
                f = bm.faces.new([vs[i], vs[(i + 1) % 4], vs2[(i + 1) % 4], vs2[i]])
                f.material_index = mat
        except ValueError:
            pass
    # sleeves (upper arm cylinders)
    for sign in (-1.0, 1.0):
        sx = sign * (shoulder_w * 0.5)
        a = Vector((sx, 0.0, L["shoulder"] - 0.02))
        b = Vector((sx + sign * 0.22, 0.05, L["waist"] + 0.08))
        _sleeve(bm, a, b, 0.045, seg=max(6, seg // 2), mat=mat)


def _sleeve(bm, a: Vector, b: Vector, r: float, seg=6, mat=0):
    d = b - a
    if d.length < 1e-6:
        return
    direction = d.normalized()
    up = Vector((0, 0, 1)) if abs(direction.z) < 0.9 else Vector((1, 0, 0))
    x_axis = direction.cross(up).normalized()
    y_axis = direction.cross(x_axis).normalized()
    rings = []
    for t in (0.0, 1.0):
        c = a.lerp(b, t)
        ring = []
        for k in range(seg):
            ang = 2 * math.pi * k / seg
            ring.append(bm.verts.new(c + (math.cos(ang) * x_axis + math.sin(ang) * y_axis) * r))
        rings.append(ring)
    _bridge(bm, rings[0], rings[1], mat)



def build_frock_tails_and_sleeves(bm, L, shoulder_w, mat=0, seg=12):
    """Extras for frock coat: standing collar, long sleeves to wrist, rear tails.
    Fitted torso comes from _body_shell_mesh in _build_person."""
    sw = shoulder_w * 0.52
    # standing collar
    collar_bot = _ring(bm, 0, 0.01, L["chin"] - 0.02, sw * 0.38, sw * 0.32, seg)
    collar_top = _ring(bm, 0, 0.015, L["chin"] + 0.02, sw * 0.36, sw * 0.30, seg)
    _bridge(bm, collar_bot, collar_top, mat)
    # long sleeves shoulder → near wrist (two segments)
    for sign in (-1.0, 1.0):
        sx = sign * (shoulder_w * 0.48)
        shoulder = Vector((sx, 0.02, L["shoulder"] - 0.01))
        elbow = Vector((sx + sign * 0.14, 0.04, L["waist"] + 0.12))
        wrist = Vector((sx + sign * 0.20, 0.02, L["hip"] + 0.15))
        _sleeve(bm, shoulder, elbow, 0.050, seg=max(6, seg // 2), mat=mat)
        _sleeve(bm, elbow, wrist, 0.040, seg=max(6, seg // 2), mat=mat)
    # rear tails — flared panels to mid-thigh
    waist_r = sw * 0.85
    hip_r = sw * 1.0
    tail_z0 = L["waist"]
    tail_z1 = max(L["knee"] + 0.04, L["hip"] - 0.15 * L["h"])
    y_back0 = -max(0.12, waist_r * 0.75)
    y_back1 = -max(0.18, hip_r * 1.2)
    for sign in (-1, 1):
        x0 = sign * waist_r * 0.1
        x1 = sign * hip_r * 0.95
        vs = [
            bm.verts.new((x0, y_back0, tail_z0)),
            bm.verts.new((x1, y_back1, tail_z0)),
            bm.verts.new((x1 * 1.12, y_back1 - 0.07, tail_z1)),
            bm.verts.new((sign * 0.015, y_back0 - 0.05, tail_z1)),
        ]
        vs2 = [bm.verts.new((v.co.x, v.co.y + 0.04, v.co.z)) for v in vs]
        try:
            f = bm.faces.new(vs); f.material_index = mat
            f = bm.faces.new(list(reversed(vs2))); f.material_index = mat
            for i in range(4):
                f = bm.faces.new([vs[i], vs[(i + 1) % 4], vs2[(i + 1) % 4], vs2[i]])
                f.material_index = mat
        except ValueError:
            pass


def build_waistcoat(bm, L, shoulder_w, mat=0, seg=10):
    """Fitted waistcoat under the frock — V-front, ends at waist."""
    sw = shoulder_w * 0.48
    profile = [
        (sw * 0.42, sw * 0.34, L["shoulder"] - 0.01),
        (sw * 0.88, sw * 0.62, L["chest"]),
        (sw * 0.70, sw * 0.52, L["waist"] + 0.01),
    ]
    _lathed_shell(bm, profile, seg=seg, mat=mat)


def build_cravat(bm, L, shoulder_w, mat=0, seg=8):
    """Necktie / cravat knot at the throat."""
    sw = shoulder_w * 0.42
    z = L["chin"] - 0.04
    # small torus-like band
    outer = _ring(bm, 0, 0.02, z, sw * 0.38, sw * 0.30, seg)
    inner = _ring(bm, 0, 0.02, z + 0.025, sw * 0.32, sw * 0.26, seg)
    _bridge(bm, outer, inner, mat)
    # knot blob at front
    try:
        knot = [
            bm.verts.new((-0.025, 0.06, z - 0.01)),
            bm.verts.new((0.025, 0.06, z - 0.01)),
            bm.verts.new((0.02, 0.09, z + 0.02)),
            bm.verts.new((-0.02, 0.09, z + 0.02)),
        ]
        f = bm.faces.new(knot); f.material_index = mat
    except ValueError:
        pass


def build_police_tunic(bm, L, shoulder_w, mat=0, seg=12):
    """Dark fitted tunic, shorter than frock, standing collar."""
    sw = shoulder_w * 0.55
    profile = [
        (sw * 0.5, sw * 0.38, L["shoulder"] + 0.04),
        (sw * 0.95, sw * 0.7, L["chest"]),
        (sw * 0.8, sw * 0.65, L["waist"]),
        (sw * 0.85, sw * 0.6, L["hip"] + 0.05),
    ]
    _lathed_shell(bm, profile, seg=seg, mat=mat)
    for sign in (-1.0, 1.0):
        sx = sign * (shoulder_w * 0.5)
        _sleeve(bm, Vector((sx, 0, L["shoulder"] - 0.02)),
                Vector((sx + sign * 0.2, 0.04, L["waist"] + 0.1)), 0.042, seg=6, mat=mat)


def build_smock(bm, L, shoulder_w, mat=0, seg=12):
    """Workmen's smock — loose A-line over torso to mid-thigh."""
    sw = shoulder_w * 0.55
    profile = [
        (sw * 0.55, sw * 0.45, L["shoulder"] + 0.02),
        (sw * 1.05, sw * 0.85, L["chest"]),
        (sw * 1.15, sw * 0.95, L["waist"]),
        (sw * 1.25, sw * 1.05, L["hip"] - 0.05 * L["h"]),
    ]
    _lathed_shell(bm, profile, seg=seg, mat=mat)
    for sign in (-1.0, 1.0):
        sx = sign * (shoulder_w * 0.48)
        _sleeve(bm, Vector((sx, 0, L["shoulder"])),
                Vector((sx + sign * 0.18, 0.03, L["waist"] + 0.12)), 0.055, seg=6, mat=mat)


def build_bodice(bm, L, shoulder_w, mat=0, seg=12):
    """Fitted women's bodice — shoulder to waist, not a bell."""
    sw = shoulder_w * 0.52
    profile = [
        (sw * 0.5, sw * 0.4, L["shoulder"] + 0.01),
        (sw * 0.95, sw * 0.7, L["chest"]),
        (sw * 0.72, sw * 0.58, L["waist"] + 0.02),
    ]
    _lathed_shell(bm, profile, seg=seg, mat=mat)
    for sign in (-1.0, 1.0):
        sx = sign * (shoulder_w * 0.48)
        _sleeve(bm, Vector((sx, 0, L["shoulder"])),
                Vector((sx + sign * 0.16, 0.02, L["chest"] - 0.05)), 0.038, seg=6, mat=mat)



def build_sleeves_only(bm, L, shoulder_w, mat=0, seg=6, length=0.85):
    """Upper-arm sleeves without a lathed torso (torso from body shell)."""
    r = 0.032 if length < 0.9 else 0.036
    for sign in (-1.0, 1.0):
        sx = sign * (shoulder_w * 0.50)
        a = Vector((sx, 0.02, L["shoulder"] - 0.015))
        if length > 0.9:
            b = Vector((sx + sign * 0.16, 0.04, L["waist"] + 0.12))
        else:
            b = Vector((sx + sign * 0.14, 0.03, L["chest"] - 0.04))
        _sleeve(bm, a, b, r, seg=seg, mat=mat)


def build_crinoline(bm, L, mat=0, seg=16):
    """Full 1850s bell crinoline: waist to floor, wide elliptical hem."""
    z0 = L["waist"]
    z1 = max(L["z0"] + 0.01, L["ankle"] - 0.01)  # floor-length
    waist_rx, waist_ry = 0.14, 0.12
    # Full bell ~1.2–1.3 m across at hem (reads at mid-distance)
    hem_rx, hem_ry = 0.58, 0.50
    mid_z = z0 + 0.45 * (z1 - z0)
    profile = [
        (waist_rx, waist_ry, z0),
        (waist_rx * 1.8, waist_ry * 1.6, z0 + 0.18 * (z1 - z0)),
        (hem_rx * 0.88, hem_ry * 0.88, mid_z),
        (hem_rx, hem_ry, z1),
    ]
    rings = _lathed_shell(bm, profile, seg=seg, mat=mat)
    # close hem underside partially (prevents see-through) — small inset
    inset = _ring(bm, 0, 0, z1 + 0.01, hem_rx * 0.4, hem_ry * 0.4, seg)
    _bridge(bm, rings[-1], inset, mat)
    try:
        bm.faces.new(list(reversed(inset))).material_index = mat
    except ValueError:
        pass


def build_bustle_skirt(bm, L, mat=0, seg=14):
    """1880s–1910s bustle: fuller at rear."""
    z0 = L["waist"]
    z1 = L["ankle"] + 0.02
    # build asymmetric by shifting ring centres backward at mid
    rings = []
    steps = [
        (0.15, 0.13, z0, 0.0),
        (0.32, 0.30, z0 + 0.35 * (z1 - z0), -0.08),
        (0.42, 0.45, z1, -0.06),
    ]
    for rx, ry, z, cy in steps:
        rings.append(_ring(bm, 0, cy, z, rx, ry, seg))
    for A, B in zip(rings, rings[1:]):
        _bridge(bm, A, B, mat)


def build_shawl(bm, L, shoulder_w, mat=0):
    """Thin draped triangle across shoulders — not blocky pads."""
    z = L["shoulder"]
    w = shoulder_w * 0.55
    # front drape tip + shoulder ends; slight thickness via dual sheet
    front = [
        bm.verts.new((-w, 0.04, z + 0.01)),
        bm.verts.new((w, 0.04, z + 0.01)),
        bm.verts.new((0.0, 0.10, z - 0.22)),
    ]
    back = [
        bm.verts.new((-w * 0.85, -0.06, z + 0.01)),
        bm.verts.new((w * 0.85, -0.06, z + 0.01)),
        bm.verts.new((0.0, -0.12, z - 0.18)),
    ]
    try:
        f = bm.faces.new(front); f.material_index = mat
        f = bm.faces.new(list(reversed(back))); f.material_index = mat
        # side connectors
        f = bm.faces.new([front[0], front[2], back[2], back[0]]); f.material_index = mat
        f = bm.faces.new([front[1], back[1], back[2], front[2]]); f.material_index = mat
    except ValueError:
        pass


def build_trousers(bm, L, hip_w, mat=0, seg=8):
    """Separate legs — not a skirt. Radii scale with hip width."""
    hip_r = max(0.07, hip_w * 0.14)
    for sign in (-1.0, 1.0):
        cx = sign * hip_w * 0.20
        profile = [
            (hip_r, hip_r * 1.05, L["hip"] + 0.02),
            (hip_r * 0.85, hip_r * 0.95, L["knee"]),
            (hip_r * 0.65, hip_r * 0.72, L["ankle"] + 0.03),
        ]
        rings = []
        for rx, ry, z in profile:
            rings.append(_ring(bm, cx, 0.01, z, rx, ry, seg))
        for A, B in zip(rings, rings[1:]):
            _bridge(bm, A, B, mat)



def build_boots(bm, L, hip_w, mat=0, seg=8):
    """Period ankle boots covering foot + ankle (~ankle+0.14 m)."""
    foot_x = max(0.12, hip_w * 0.38)
    for sign in (-1.0, 1.0):
        cx = sign * foot_x
        z0 = max(0.0, L["z0"])
        z1 = L["ankle"] + 0.14
        top = _ring(bm, cx, 0.01, z1, 0.055, 0.062, seg)
        mid = _ring(bm, cx, 0.03, z0 + 0.04, 0.058, 0.070, seg)
        _bridge(bm, top, mid, mat)
        toe = _ring(bm, cx, 0.09, z0 + 0.005, 0.050, 0.095, seg)
        _bridge(bm, mid, toe, mat)
        try:
            bm.faces.new(list(reversed(toe))).material_index = mat
        except ValueError:
            pass


def build_fire_helmet(bm, crown_z, head_r, mat=0, seg=10):
    r = head_r * 1.1
    h = 0.12
    bot = _ring(bm, 0, 0, crown_z, r, r, seg)
    top = _ring(bm, 0, 0, crown_z + h, r * 0.5, r * 0.5, seg)
    _bridge(bm, bot, top, mat)
    _cap(bm, top, (0, 0, crown_z + h + 0.04), mat)
    # rear brim
    brim = _ring(bm, 0, -0.05, crown_z - 0.01, r * 1.2, r * 1.3, seg)
    _bridge(bm, bot, brim, mat)


# ---------------------------------------------------------------------------
# body material paint (skin head/hands; hide torso under clothes via dark)
# ---------------------------------------------------------------------------

def _paint_body_materials(obj, L, mats, role):
    """Paint HBM body under modelled garments.
    Gentlemen: waistcoat (sec) on torso, trousers on legs, skin head/hands —
    frock coat is a separate modelled shell (not a painted T-shirt).
    Ladies: bodice (sec) torso, skirt (main) below waist.
    Workmen: smock (main) torso+arms."""
    me = obj.data
    while len(me.materials) < 4:
        me.materials.append(None)
    me.materials[0] = mats["skin"]
    me.materials[1] = mats["main"]
    me.materials[2] = mats["sec"]
    me.materials[3] = mats.get("trim") or mats["sec"]
    sh_xs = [abs(v.co.x) for v in me.vertices if abs(v.co.z - L["shoulder"]) < 0.06]
    shoulder_w = max(sh_xs) if sh_xs else 0.22
    hand_x = shoulder_w * 0.72
    is_lady = any(k in role for k in ("lady", "girl", "woman")) or role.endswith("_f")
    is_worker = any(k in role for k in ("workman", "navvy", "fireman"))
    is_gent = (not is_lady) and (not is_worker) and ("police" not in role) and ("sailor" not in role)
    for p in me.polygons:
        zs = [me.vertices[i].co.z for i in p.vertices]
        xs = [me.vertices[i].co.x for i in p.vertices]
        zc = sum(zs) / len(zs)
        xc = sum(abs(x) for x in xs) / len(xs)
        if zc >= L["chin"] - 0.01:
            p.material_index = 0
            continue
        # hands only: hanging-arm band (hip..chest), far from centreline — never legs
        if L["hip"] + 0.02 < zc < L["chest"] - 0.05 and xc > hand_x:
            p.material_index = 0
            continue
        if is_lady:
            if zc < L["waist"]:
                p.material_index = 1  # skirt
            else:
                p.material_index = 2  # bodice
            continue
        if is_gent:
            # torso = waistcoat (trim/slot3); legs = trousers (sec); arms under coat
            if zc >= L["waist"] - 0.02 and xc < hand_x * 0.85:
                p.material_index = 3  # waistcoat
            elif zc >= L["waist"] - 0.02:
                p.material_index = 0  # shirt cuff / skin peek under sleeve
            else:
                p.material_index = 2  # trousers
            continue
        # worker / police / default: main on torso+arms, sec trousers
        if zc >= L["waist"] - 0.02:
            p.material_index = 1
        else:
            p.material_index = 2


# ---------------------------------------------------------------------------
# simple pose via armature-free limb bend
# ---------------------------------------------------------------------------

def _apply_pose(obj: bpy.types.Object, L: Dict[str, float], pose: str, seed: int):
    if pose in (None, "standing"):
        return
    rng = random.Random(seed + 99)
    me = obj.data
    # approximate shoulder / hip centres
    sh_z = L["shoulder"]
    hip_z = L["hip"]
    # collect verts
    coords = [v.co.copy() for v in me.vertices]

    def rot_around(origin, axis, angle, co):
        M = Matrix.Rotation(angle, 4, axis)
        return origin + M @ (co - origin)

    for i, co in enumerate(coords):
        # left/right arm: x sign, z above waist
        if co.z > L["waist"] + 0.02 and abs(co.x) > 0.12:
            sign = 1.0 if co.x > 0 else -1.0
            origin = Vector((sign * 0.12, 0.0, sh_z))
            if pose == "walking":
                ang = sign * 0.35 * (1 if sign > 0 else -1) * (0.8 + 0.4 * rng.random())
                # swing forward/back around X-ish via Y rotation alternate
                swing = 0.4 if (sign > 0) == (seed % 2 == 0) else -0.35
                co = rot_around(origin, Vector((1, 0, 0)), swing, co)
            elif pose == "pointing":
                if sign > 0:
                    co = rot_around(origin, Vector((0, 1, 0)), -0.9, co)
                    co = rot_around(origin, Vector((1, 0, 0)), -0.5, co)
            elif pose == "working":
                swing = -0.7 if sign > 0 else 0.2
                co = rot_around(origin, Vector((1, 0, 0)), swing, co)
            elif pose == "hauling":
                co = rot_around(origin, Vector((1, 0, 0)), -0.9, co)
            elif pose == "seated":
                pass
            coords[i] = co
        # legs for walking / seated
        if co.z < L["hip"] and abs(co.x) > 0.03:
            sign = 1.0 if co.x > 0 else -1.0
            origin = Vector((sign * 0.08, 0.0, hip_z))
            if pose == "walking":
                swing = -0.35 if (sign > 0) == (seed % 2 == 0) else 0.3
                coords[i] = rot_around(origin, Vector((1, 0, 0)), swing, co)
            elif pose == "seated":
                coords[i] = rot_around(origin, Vector((1, 0, 0)), -1.2, co)
            elif pose == "hauling":
                coords[i] = rot_around(origin, Vector((1, 0, 0)), -0.15, co)

    for v, co in zip(me.vertices, coords):
        v.co = co
    me.update()
    # re-ground after pose
    zs = [v.co.z for v in me.vertices]
    dz = -min(zs)
    if abs(dz) > 1e-5:
        for v in me.vertices:
            v.co.z += dz



def _body_shell_mesh(body: bpy.types.Object, z_lo: float, z_hi: float,
                     inflate: float = 0.025, name: str = "shell",
                     xy_scale: float = 1.06) -> bpy.types.Mesh:
    """Duplicate body verts in a Z band, scale XY from centre, inflate along normals.
    Produces a fitted garment shell that follows the HBM body — not a lathe bell."""
    src = body.data
    bm = bmesh.new()
    bm.from_mesh(src)
    # delete verts outside band (and their faces)
    doomed = [v for v in bm.verts if v.co.z < z_lo - 0.01 or v.co.z > z_hi + 0.01]
    bmesh.ops.delete(bm, geom=doomed, context="VERTS")
    if not bm.verts:
        bm.free()
        return bpy.data.meshes.new(name)
    # centre XY
    xs = [v.co.x for v in bm.verts]; ys = [v.co.y for v in bm.verts]
    cx = 0.5 * (min(xs) + max(xs)); cy = 0.5 * (min(ys) + max(ys))
    for v in bm.verts:
        v.co.x = cx + (v.co.x - cx) * xy_scale
        v.co.y = cy + (v.co.y - cy) * xy_scale
    bmesh.ops.recalc_face_normals(bm, faces=list(bm.faces))
    if inflate > 0 and bm.faces:
        for v in bm.verts:
            v.normal_update()
        for v in bm.verts:
            v.co += v.normal * inflate
    me = bpy.data.meshes.new(name)
    bm.to_mesh(me)
    bm.free()
    me.update()
    return me


def _append_mesh(bm_dst: bmesh.types.BMesh, me: bpy.types.Mesh, mat: int = 0):
    """Append mesh geometry into bmesh with material index."""
    tmp = bmesh.new()
    tmp.from_mesh(me)
    vmap = {}
    for v in tmp.verts:
        vmap[v.index] = bm_dst.verts.new(v.co.copy())
    bm_dst.verts.ensure_lookup_table()
    for f in tmp.faces:
        try:
            nf = bm_dst.faces.new([vmap[v.index] for v in f.verts])
            nf.material_index = mat
        except ValueError:
            pass
    tmp.free()



# ---------------------------------------------------------------------------
# assemble person
# ---------------------------------------------------------------------------

def _shoulder_width(obj) -> float:
    Lapprox_z = None
    zs = [v.co.z for v in obj.data.vertices]
    z0, z1 = min(zs), max(zs)
    sh = z0 + 0.80 * (z1 - z0)
    xs = [v.co.x for v in obj.data.vertices if abs(v.co.z - sh) < 0.06]
    if not xs:
        xs = [v.co.x for v in obj.data.vertices]
    return max(xs) - min(xs)


def _join_garment(body: bpy.types.Object, gme: bpy.types.Mesh, mats_list):
    gob = bpy.data.objects.new(gme.name + "_ob", gme)
    bpy.context.collection.objects.link(gob)
    # materials already on mesh slots via caller
    bpy.ops.object.select_all(action="DESELECT")
    body.select_set(True)
    gob.select_set(True)
    bpy.context.view_layer.objects.active = body
    bpy.ops.object.join()
    return body


def _build_person(role: str, pose: str, lod: str, seed: int) -> bpy.types.Mesh:
    sex = _sex_for(role)
    height = _height_for(role, seed)
    mats = _mats_for(seed, role)
    seg = {"hero": 14, "mid": 10, "crowd": 8}[lod if lod in ("hero", "mid", "crowd") else "mid"]

    body = _import_base(sex, lod)
    _scale_to_height(body, height)
    _enforce_head_ratio(body, HEAD_RATIO)
    L = _landmarks(body)
    # enforce head ratio softly: if crown-chin >> head_ratio, we still trust HBM
    sw = _shoulder_width(body)
    # measure actual head radius from mesh (chin..crown band)
    hs = [abs(v.co.x) for v in body.data.vertices if v.co.z >= L["chin"] - 0.02]
    head_r = max(hs) * 1.05 if hs else (HEAD_DIAM * 0.5 * (height / (5.5 * FT)))

    _paint_body_materials(body, L, mats, role)
    _apply_pose(body, L, pose, seed)
    L = _landmarks(body)  # refresh after pose/ground

    # garment bmesh — fitted body shells + modelled hats/skirts/tails
    bm = _new_bm()
    is_lady = any(k in role for k in ("lady", "girl", "woman")) or role.endswith("_f")
    is_worker = any(k in role for k in ("workman", "navvy"))
    is_police = "police" in role
    is_sailor = "sailor" in role
    is_fire = "fireman" in role
    is_1890 = role.startswith("1890")
    is_1930 = role.startswith("1930")
    is_today = role.startswith("today")

    def add_shell(z_lo, z_hi, inflate, xy, mat):
        sm = _body_shell_mesh(body, z_lo, z_hi, inflate=inflate, xy_scale=xy,
                              name=f"sh_{mat}_{seed}")
        if sm.vertices:
            _append_mesh(bm, sm, mat=mat)
        if sm.users == 0:
            bpy.data.meshes.remove(sm)

    # Fitted shells from the HBM body (shrinkwrap-style) + modelled volume extras.
    # garment mat slots: 0=main, 1=sec, 2=hat, 3=trim
    if is_lady:
        if is_1890:
            build_bustle_skirt(bm, L, mat=0, seg=seg)
            build_boater(bm, L["crown"] - 0.002, head_r, mat=2, seg=seg)
        else:
            build_crinoline(bm, L, mat=0, seg=max(seg, 16))
            build_bonnet(bm, L["chin"], L["crown"], head_r, mat=2, seg=seg)
        # fitted bodice shell following the female HBM torso
        add_shell(L["waist"] - 0.005, L["shoulder"] + 0.03, 0.016, 1.05, 1)
        build_sleeves_only(bm, L, sw, mat=1, seg=max(6, seg // 2), length=0.7)
        if seed % 5 != 1:
            build_shawl(bm, L, sw, mat=3)
        build_boots(bm, L, sw * 0.7, mat=1, seg=max(6, seg // 2))
    elif is_police:
        add_shell(L["hip"] + 0.02, L["shoulder"] + 0.04, 0.022, 1.08, 0)
        build_frock_tails_and_sleeves(bm, L, sw * 0.9, mat=0, seg=seg)
        build_top_hat(bm, L["crown"] - 0.002, head_r, mat=2, seg=seg)
        build_boots(bm, L, sw, mat=1, seg=max(6, seg // 2))
    elif is_worker or is_fire:
        add_shell(L["ankle"] + 0.02, L["waist"] + 0.02, 0.014, 1.06, 1)  # trousers
        add_shell(L["hip"] - 0.04 * L["h"], L["shoulder"] + 0.03, 0.030, 1.12, 0)  # smock
        build_sleeves_only(bm, L, sw, mat=0, seg=max(6, seg // 2), length=0.75)
        if is_fire:
            build_fire_helmet(bm, L["crown"] - 0.002, head_r, mat=2, seg=seg)
        else:
            build_cap(bm, L["crown"] - 0.002, head_r, mat=2, seg=seg)
        build_boots(bm, L, sw, mat=1, seg=max(6, seg // 2))
    elif is_sailor:
        add_shell(L["waist"] - 0.02, L["shoulder"] + 0.03, 0.022, 1.06, 0)
        build_cap(bm, L["crown"] - 0.002, head_r, mat=2, seg=seg)
        build_boots(bm, L, sw, mat=1, seg=max(6, seg // 2))
    elif is_1930:
        add_shell(L["hip"] + 0.02, L["shoulder"] + 0.03, 0.020, 1.06, 0)
        build_trilby(bm, L["crown"] - 0.002, head_r, mat=2, seg=seg)
        build_boots(bm, L, sw, mat=1, seg=max(6, seg // 2))
    elif is_today:
        if not is_lady:
            build_boots(bm, L, sw, mat=1, seg=max(6, seg // 2))
    else:
        # gentleman: waistcoat + frock + trousers shells + cravat + tails/sleeves + top hat
        add_shell(L["ankle"] + 0.02, L["waist"] + 0.02, 0.014, 1.06, 1)  # trousers
        add_shell(L["waist"] - 0.01, L["shoulder"] + 0.02, 0.012, 1.03, 3)  # waistcoat
        add_shell(L["hip"] - 0.06 * L["h"], L["shoulder"] + 0.04, 0.024, 1.08, 0)  # frock
        build_cravat(bm, L, sw, mat=3, seg=max(6, seg // 2))
        build_frock_tails_and_sleeves(bm, L, sw, mat=0, seg=seg)
        if is_1890:
            build_boater(bm, L["crown"] - 0.002, head_r, mat=2, seg=seg)
        else:
            build_top_hat(bm, L["crown"] - 0.002, head_r, mat=2, seg=seg)
        build_boots(bm, L, sw, mat=1, seg=max(6, seg // 2))

    gme = _finish_mesh(bm, f"CPL3_gar_{role}_{seed}")
    # assign materials to garment slots
    gme.materials.append(mats["main"])
    gme.materials.append(mats["sec"])
    gme.materials.append(mats["hat"])
    gme.materials.append(mats["trim"])
    gme.materials.append(mats["skin"])

    body = _join_garment(body, gme, mats)
    # smooth shading helps garments read as cloth not facets
    for p in body.data.polygons:
        p.use_smooth = True
    if hasattr(body.data, "use_auto_smooth"):
        body.data.use_auto_smooth = True
    me = body.data
    me.name = f"CPL3_{role}_{pose}_{lod}_{seed % 24}"
    body["cpl_people"] = PEOPLE_TAG
    body["cpl_role"] = role
    body["cpl_pose"] = pose
    body["cpl_lod"] = lod
    # return mesh; leave object — caller may keep or remove object
    return body


def clear_mesh_cache():
    _MESH_CACHE.clear()


def resolve_role(kind: str, style: Optional[dict], era: str = "1850s") -> str:
    style = style or {}
    if "role" in style:
        return style["role"]
    k = (kind or "").lower()
    era_key = "1850s"
    if era:
        e = str(era).lower()
        for key in ERA_ROLES:
            if key in e or e in key:
                era_key = key
                break
        if e.isdigit():
            y = int(e)
            if y >= 1930: era_key = "1930s"
            elif y >= 1880: era_key = "1890s"
            else: era_key = "1850s"
    roles = ERA_ROLES.get(era_key, ERA_ROLES["1850s"])
    if any(x in k for x in ("woman", "lady", "female", "girl")):
        for r in roles:
            if any(x in r for x in ("lady", "woman", "girl", "_f")):
                return r
    if "police" in k: return "1850s_police" if "1850" in era_key or era_key == "1851" else roles[0]
    if any(x in k for x in ("work", "navvy", "labour", "labor")): 
        return "1850s_workman" if era_key in ("1850s", "1851") else roles[0]
    if "sailor" in k or "rnd" in k: return "1890s_sailor"
    if "fire" in k: return "1930s_fireman"
    if "soldier" in k or "uniform" in k:
        return "1850s_soldier" if era_key in ("1850s", "1851") else "1890s_uniform"
    # default first male-ish
    for r in roles:
        if not any(x in r for x in ("lady", "woman", "girl", "_f")):
            return r
    return roles[0]


def person_mesh(name, kind, mats=None, FT=0.3048, style=None, pose=None,
                lod=None, seed=None, era="1850s"):
    """Build or cache a dressed person mesh; return mesh datablock.
    Places a temporary object named `name` (replacing any existing)."""
    style = style or {}
    role = resolve_role(kind, style, era=style.get("era", era))
    pose = pose or style.get("pose") or "standing"
    if pose not in POSES:
        pose = "standing"
    lod = lod or style.get("lod") or "mid"
    if lod not in ("hero", "mid", "crowd"):
        lod = "mid"
    if seed is None:
        seed = int(hashlib.md5(name.encode()).hexdigest()[:8], 16)
    key = (role, pose, lod, seed % 24)
    me = _MESH_CACHE.get(key)
    if me is None or me.users < 0:
        # remove old object if present
        old = bpy.data.objects.get(name)
        if old:
            bpy.data.objects.remove(old, do_unlink=True)
        body_ob = _build_person(role, pose, lod, seed)
        body_ob.name = name
        me = body_ob.data
        _MESH_CACHE[key] = me
        return me
    # instance cached mesh on object
    old = bpy.data.objects.get(name)
    if old:
        old.data = me
        return me
    ob = bpy.data.objects.new(name, me)
    bpy.context.collection.objects.link(ob)
    return me


def catalogue():
    return {
        "version": PEOPLE_VERSION,
        "bases": "Blender Studio Human Base Meshes v1.4.1 realistic (CC0)",
        "roles": {k: list(v) for k, v in ERA_ROLES.items()},
        "poses": list(POSES),
        "lods": ["hero", "mid", "crowd"],
        "height_m": (HEIGHT_MIN, HEIGHT_MAX),
        "head_ratio": HEAD_RATIO,
        "top_hat_m": TOP_HAT_H,
    }


# ---------------------------------------------------------------------------
# scene swap
# ---------------------------------------------------------------------------

_FIGURE_PREFIXES = (
    "CROWD", "VIS_", "PERSON", "FIG_", "FIGURE", "PEOPLE", "GENT", "LADY",
    "MAN_", "WOMAN", "CHILD", "BOY_", "GIRL", "POLICE", "SAILOR", "SOLDIER",
    "KWORKER", "WORKER", "NAVY", "FIRE", "GUEST", "STAFF",
)
_FIGURE_KINDS = {"figure", "worker", "crowd", "person", "human", "visitor"}


def _is_figure(ob: bpy.types.Object) -> bool:
    if ob.type != "MESH":
        return False
    if ob.get("cpl_people") in (PEOPLE_TAG, "cpl_people_v2", "cpl_people_v1"):
        return True
    pk = (ob.get("part_kind") or ob.get("kind") or "").lower()
    if pk in _FIGURE_KINDS:
        return True
    name = ob.name.upper()
    return any(name.startswith(p) or f"_{p}" in name for p in _FIGURE_PREFIXES)


def _infer_kind(ob) -> str:
    n = ob.name.lower()
    pk = (ob.get("part_kind") or "").lower()
    if pk == "worker" or "worker" in n or "kworker" in n or "navvy" in n:
        return "workman"
    if "police" in n: return "police"
    if "lady" in n or "woman" in n or "girl" in n: return "lady"
    if "sailor" in n: return "sailor"
    if "fire" in n: return "fireman"
    if "soldier" in n: return "soldier"
    if "boy" in n: return "boy"
    return "man"


def _infer_pose(ob, seed: int) -> str:
    n = ob.name.lower()
    for p in POSES:
        if p in n:
            return p
    return POSES[seed % len(POSES)]


def swap_scene_people(era: str = "1851", camera=None, seed: int = 0,
                      max_hero: int = 10, max_mid: int = 60) -> Dict[str, Any]:
    """Replace baked lathe/v2 figures with v3 HBM+garment people. Does not save."""
    figs = [o for o in bpy.data.objects if _is_figure(o)]
    if not figs:
        return {"swapped": 0, "version": PEOPLE_VERSION}

    cam = camera or bpy.context.scene.camera
    cam_loc = cam.matrix_world.translation if cam else Vector((0, 0, 1.6))

    # distance sort for LOD
    dists = []
    for ob in figs:
        d = (ob.matrix_world.translation - cam_loc).length
        dists.append((d, ob))
    dists.sort(key=lambda x: x[0])

    swapped = 0
    for i, (d, ob) in enumerate(dists):
        if i < max_hero:
            lod = "hero"
        elif i < max_hero + max_mid:
            lod = "mid"
        else:
            lod = "crowd"
        rng_seed = seed + int(hashlib.md5(ob.name.encode()).hexdigest()[:6], 16)
        kind = _infer_kind(ob)
        # 1850s Victorian crowd: force ≥40% ladies when figure is anonymous "man"
        era_l = (era or "").lower()
        if kind == "man" and ("1850" in era_l or era_l in ("1851", "1850s")):
            # deterministic: ~58% ladies so crinolines read at mid-distance
            if (rng_seed % 100) < 58:
                kind = "lady"
            elif (rng_seed % 100) >= 88:
                kind = "workman"  # ~12% workmen in anonymous crowd
        pose = _infer_pose(ob, rng_seed)
        role = resolve_role(kind, {}, era=era)
        # preserve transform
        mw = ob.matrix_world.copy()
        # uniform XY scale from original (height encoded in scale often)
        sx = ob.scale.x
        # build
        key = (role, pose, lod, rng_seed % 24)
        me = _MESH_CACHE.get(key)
        if me is None:
            body_ob = _build_person(role, pose, lod, rng_seed)
            me = body_ob.data
            _MESH_CACHE[key] = me
            # remove temp object (we'll reuse mesh on original)
            bpy.data.objects.remove(body_ob, do_unlink=True)
        ob.data = me
        ob.matrix_world = mw
        # keep original footprint scale roughly: our mesh is already real-world height;
        # if old figure was ~1.7 unit tall via scale, reset scale to 1
        # Detect peg scale: if scale.z wildly off, normalize
        if max(ob.scale) > 2.5 or min(ob.scale) < 0.3:
            ob.scale = (1, 1, 1)
        else:
            # keep horizontal facing; height from mesh
            ob.scale = (1, 1, 1)
        ob["cpl_people"] = PEOPLE_TAG
        ob["cpl_role"] = role
        ob["cpl_lod"] = lod
        swapped += 1

    return {"swapped": swapped, "version": PEOPLE_VERSION, "cache": len(_MESH_CACHE),
            "era": era}
