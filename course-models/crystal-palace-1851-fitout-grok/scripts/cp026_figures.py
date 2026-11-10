"""CP026 shilling-day figures (2026-11-10, DEPARTURES FT55). Working-class excursionists of summer 1851 in the
c9_figures_v2 style (copied as c26_figures_base.py): HBM CC0 head + modelled dress.
Men: base.build_figure (jacket / smock-frock / best frock coat, caps, wideawakes, a few top hats) with shilling-day palettes.
Women (new here): HBM female head, fitted bodice, full skirt over petticoats to the ground (pre-crinoline 1851, ~0.75 m
hem), shawl over the shoulders, hands clasped at the waist, open-fronted bonnet (straw / black) or a white cap.
Children: the same builders at 1.15-1.38 m. Local -y is the front (same as state_common.heading_rz)."""
import bpy, bmesh, math, random, zlib, os, sys
from mathutils import Vector
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import c26_figures_base as B

def _m(name, c, rough=0.9, sheen=0.0, noise=0.0):
    return B._mat("C26_" + name, c, rough, sheen, noise)

SKIN = [(0.40, 0.25, 0.17), (0.36, 0.22, 0.15), (0.31, 0.19, 0.13), (0.44, 0.28, 0.20)]
HAIR = [(0.05, 0.035, 0.025), (0.10, 0.07, 0.04), (0.16, 0.11, 0.06)]

# men's shilling-day dress: (coat, trousers, waistcoat, neck, hat, role, hat kind)
MEN = [
    ("fustian",  (0.17, 0.13, 0.08), (0.26, 0.23, 0.18), (0.10, 0.08, 0.06), (0.32, 0.07, 0.05), (0.05, 0.045, 0.04), "workman", "cap"),
    ("cord",     (0.22, 0.17, 0.10), (0.12, 0.11, 0.09), (0.16, 0.06, 0.04), (0.06, 0.09, 0.20), (0.07, 0.06, 0.05), "workman", "wide"),
    ("smock",    (0.46, 0.43, 0.34), (0.16, 0.14, 0.10), (0.42, 0.39, 0.31), (0.25, 0.07, 0.05), (0.09, 0.075, 0.055), "carter", "wide"),
    ("bestblack",(0.03, 0.03, 0.035),(0.10, 0.09, 0.08), (0.18, 0.15, 0.10), (0.015, 0.015, 0.018), (0.015, 0.015, 0.018), "engineer", "top"),
    ("bluecloth",(0.07, 0.08, 0.13), (0.24, 0.21, 0.16), (0.12, 0.09, 0.06), (0.30, 0.28, 0.25), (0.05, 0.045, 0.04), "workman", "cap"),
    ("velveteen",(0.13, 0.09, 0.05), (0.27, 0.24, 0.19), (0.20, 0.08, 0.05), (0.05, 0.05, 0.06), (0.06, 0.05, 0.04), "foreman", "wide"),
    ("greycoat", (0.14, 0.14, 0.13), (0.09, 0.085, 0.08), (0.22, 0.18, 0.12), (0.02, 0.02, 0.025), (0.02, 0.02, 0.022), "engineer", "top"),
    ("moleskin", (0.24, 0.22, 0.18), (0.11, 0.10, 0.085),(0.09, 0.08, 0.07), (0.28, 0.05, 0.05), (0.05, 0.045, 0.04), "workman", "cap"),
]
# women: (dress, shawl, bonnet kind, bonnet colour)
WOMEN = [   # albedos x0.66 (dress/shawl), x0.82 straw: 2026-11-10 preview read pastel under the exterior_midday sun
    ("print_lilac", (0.238, 0.191, 0.251), (0.198, 0.046, 0.033), "straw", (0.325, 0.258, 0.137)),
    ("print_blue",  (0.112, 0.145, 0.224), (0.172, 0.112, 0.059), "black", (0.040, 0.035, 0.035)),
    ("stuff_black", (0.030, 0.026, 0.026), (0.185, 0.172, 0.132), "straw", (0.295, 0.235, 0.127)),
    ("print_brown", (0.198, 0.139, 0.086), (0.066, 0.079, 0.145), "straw", (0.277, 0.218, 0.117)),
    ("print_pink",  (0.317, 0.198, 0.185), (0.046, 0.046, 0.050),"straw", (0.343, 0.276, 0.153)),
    ("plaid_green", (0.106, 0.145, 0.092), (0.238, 0.198, 0.132), "black", (0.050, 0.045, 0.040)),
    ("print_grey",  (0.224, 0.218, 0.198), (0.224, 0.059, 0.040), "black", (0.045, 0.040, 0.040)),
    ("merino_plum", (0.145, 0.059, 0.092), (0.132, 0.119, 0.092), "black", (0.040, 0.035, 0.035)),
]

def man(name, v, H, seed, pose="standing"):
    tag, coat, trou, waist, neck, hat, role, hk = MEN[v % len(MEN)]
    M = {"skin": _m(f"skin{seed % 4}", SKIN[seed % 4], 0.55), "hair": _m(f"hair{seed % 3}", HAIR[seed % 3], 0.6),
         "shirt": _m("shirt", (0.60, 0.58, 0.53), 0.8, noise=6), "boot": _m("boot", (0.028, 0.022, 0.018), 0.45),
         "coat": _m(f"coat_{tag}", coat, 0.92, 0.3, 4.0), "trou": _m(f"trou_{tag}", trou, 0.92, 0, 4.0),
         "waist": _m(f"waist_{tag}", waist), "neck": _m(f"neck_{tag}", neck), "hat": _m(f"hat_{tag}", hat, 0.6 if hk == "top" else 0.9),
         "band": _m("band", (0.012, 0.012, 0.014), 0.7)}
    o = B.build_figure(name, role, H, pose, seed=seed, mats=M, hat=hk)
    o["c26_role"] = f"man {tag} {role} {hk}"; return o

def _bonnet(bm, I, kind, mi, mi_band):
    hr, hd = I["head_rx"], I["head_ry"]; cy = (I["front"] + I["back"]) / 2; zc = I["crown"] - 0.095
    if kind == "cap":   # white day cap with a frill: a shell over the crown and back of the head
        B.lathe(bm, [(zc - 0.03, hr * 1.10, hd * 1.08, 0.012), (zc + 0.02, hr * 1.16, hd * 1.12, 0.01), (zc + 0.075, hr * 1.06, hd * 1.02, 0.008),
                     (I["crown"] + 0.012, hr * 0.5, hd * 0.5, 0.01)], mi, 18, cy=cy, close_bot=False)
        return
    # open-fronted bonnet: rings along y (back -> front brim), each an arc over the head open under the chin
    ys = [cy + hd * 1.05, cy + hd * 0.6, cy, cy - hd * 0.55, cy - hd * 1.05, cy - hd * 1.42]
    rs = [0.085, 0.112, 0.120, 0.124, 0.132, 0.150]
    th = [math.radians(a) for a in range(-112, 113, 14)]
    rings = []
    for y, r in zip(ys, rs):
        rings.append([bm.verts.new((r * 1.02 * math.sin(t), y, zc + 0.012 + r * math.cos(t))) for t in th])
    for A, C in zip(rings, rings[1:]):
        for j in range(len(th) - 1):
            f = bm.faces.new([A[j], A[j + 1], C[j + 1], C[j]]); f.material_index = mi
    c0 = bm.verts.new((0, ys[0] + 0.01, zc + 0.012))   # the bonnet's back (crown piece)
    for j in range(len(th) - 1):
        f = bm.faces.new([rings[0][j + 1], rings[0][j], c0]); f.material_index = mi
    # ribbon band round the crown piece
    rb = [[bm.verts.new((r * 1.045 * math.sin(t), y, zc + 0.012 + r * 1.045 * math.cos(t))) for t in th] for y, r in ((ys[1] + 0.012, rs[1]), (ys[1] - 0.012, rs[1] + 0.002))]
    for j in range(len(th) - 1):
        f = bm.faces.new([rb[0][j], rb[0][j + 1], rb[1][j + 1], rb[1][j]]); f.material_index = mi_band

def woman(name, v, H, seed, child=False):
    tag, dress, shawl, bk, bcol = WOMEN[v % len(WOMEN)]
    if child: bk = ("straw", "none", "straw")[seed % 3]
    rng = random.Random(seed)
    names = ["skin", "hair", "dress", "shawl", "bonnet", "band", "boot", "fringe"]
    idx = {n: i for i, n in enumerate(names)}
    M = {"skin": _m(f"skin{seed % 4}", SKIN[seed % 4], 0.55), "hair": _m(f"hair{seed % 3}", HAIR[seed % 3], 0.6),
         "dress": _m(f"dress_{tag}", dress, 0.88, 0.05, 5.0), "shawl": _m(f"shawl_{tag}", shawl, 0.95, 0.1, 3.0),
         "bonnet": _m(f"bonnet_{bk}_{tag if bk != 'cap' else ''}", bcol, 0.75, 0, 9.0 if bk == "straw" else 0.0),
         "band": _m(f"ribbon_{tag}", tuple(min(1, c * 1.4) for c in shawl), 0.5), "boot": _m("boot", (0.028, 0.022, 0.018), 0.45),
         "fringe": _m(f"fringe_{tag}", tuple(c * 0.7 for c in shawl), 0.95)}
    bm = bmesh.new()
    I = B._add_head(bm, H, idx["skin"], idx["hair"], None, sex="female")
    k = H / 1.62; Z = lambda f: f * H; neckz = I["cut"]
    R = rng.uniform(0.33, 0.39) * k * (0.85 if child else 1.0)
    # skirt over petticoats, hem just off the ground, front slightly flatter
    B.lathe(bm, [(0.012, R, R * 0.90), (Z(0.10), R * 0.97, R * 0.88), (Z(0.27), R * 0.82, R * 0.74), (Z(0.42), R * 0.60, R * 0.54),
                 (Z(0.53), 0.20 * k, 0.17 * k), (Z(0.595), 0.135 * k, 0.11 * k)], idx["dress"], 20, close_top=True, close_bot=True)
    for s in (-1, 1):   # toes of the boots peeping out under the hem
        B.ellipsoid(bm, Vector((s * 0.07 * k, -R * 0.86, 0.022)), (0.04 * k, 0.06 * k, 0.025), idx["boot"], 8)
    # fitted bodice to the neck
    B.lathe(bm, [(Z(0.59), 0.135 * k, 0.11 * k), (Z(0.66), 0.148 * k, 0.115 * k), (Z(0.73), 0.163 * k, 0.122 * k), (Z(0.785), 0.172 * k, 0.115 * k),
                 (Z(0.815), 0.13 * k, 0.09 * k), (max(neckz - 0.004, Z(0.83)), 0.062 * k, 0.058 * k)], idx["dress"], 18, close_top=False)
    # shawl over the shoulders: folded square worn as a cape, point low at the back, edges rising to a V in front over the
    # bodice; fringed edge. Front hem is lifted per vertex (rings returned by lathe) so the bodice shows below it.
    sl = rng.uniform(0.56, 0.60)
    rings = B.lathe(bm, [(Z(sl), 0.188 * k, 0.150 * k, 0.010), (Z(0.66), 0.192 * k, 0.146 * k, 0.006), (Z(0.74), 0.190 * k, 0.138 * k), (Z(0.795), 0.180 * k, 0.126 * k),
                 (Z(0.822), 0.122 * k, 0.090 * k), (max(neckz + 0.004, Z(0.835)), 0.068 * k, 0.063 * k)], idx["shawl"], 20, close_top=False, close_bot=False)
    fr = B.lathe(bm, [(Z(sl) - 0.028, 0.190 * k, 0.152 * k, 0.010), (Z(sl) + 0.002, 0.1885 * k, 0.1505 * k, 0.010)], idx["fringe"], 20, close_top=False, close_bot=False)
    def lift(v, top):
        if v.co.y < 0:
            f = min(1.0, -v.co.y / (0.15 * k)) ** 1.5 * (1 - min(1.0, abs(v.co.x) / (0.19 * k)) * 0.6)
            v.co.z = min(top, v.co.z + f * Z(0.17))
    def point(v):   # folded square shawl: the back hangs to a point at the centre-back
        if v.co.y > 0:
            v.co.z -= Z(0.085) * max(0.0, 1 - abs(v.co.x) / (0.16 * k)) ** 1.3
    for ring in (rings[0], rings[1], fr[0], fr[1]):
        for v in ring:
            lift(v, Z(0.76) if ring is not rings[1] else Z(0.775))
            if ring is not rings[1]: point(v)
    if bk != "none": _bonnet(bm, I, bk, idx["bonnet"], idx["band"])
    me = bpy.data.meshes.new(name); bm.to_mesh(me); bm.free()
    for n in names: me.materials.append(M[n])
    o = bpy.data.objects.new(name, me)
    sub = o.modifiers.new("sub", "SUBSURF"); sub.levels = 1; sub.render_levels = 1
    for p in me.polygons: p.use_smooth = True
    o["c26_role"] = f"woman {tag} {bk}"; o["c26_height_m"] = round(H, 3); return o
