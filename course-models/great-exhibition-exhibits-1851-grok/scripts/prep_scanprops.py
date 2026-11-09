"""Prep Hyde Park 1851 scan-model dressing props (CANDIDATE 2026-11-09, CP025 scanprops).

Source: origin/main e88ee17 scan-models/blend/<slug>.blend (Tripo H3.1 image-to-3D, ~1.4 M tris,
estimated scale). Read with `git show` into a scratch dir; scan-models/ is never edited or checked out.
This script opens ONE scratch copy, cleans it and saves OUR copy into assets/scanprops/<slug>_hp1851.blend:
  - strips floating crumbs (loose islands whose bbox diagonal < --crumb m and < 0.2% of faces)
  - decimates (collapse) to <= --tris triangles
  - rescales uniformly to the catalogued height (see SCALES; departures EX_SCN_*)
  - origin at bottom centre, base on z=0, front (print view) turned to -Y
  - textures downsized to --tex px and packed; tags cp_era='HP1851', cp_state='Hyde Park 1851'
  blender -b -P scripts/prep_scanprops.py -- --slug fig-52_greek-slave --src /workspace/tmp/cp025scan/src [--tris 60000] [--tex 1024]
"""
import bpy, bmesh, sys, os, math
from mathutils import Vector, Matrix
argv = sys.argv[sys.argv.index("--") + 1:]
def arg(n, d=None): return argv[argv.index(n) + 1] if n in argv else d
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
SLUG = arg("--slug"); SRC = arg("--src", "/workspace/tmp/cp025scan/src")
TRIS = int(arg("--tris", "60000")); TEX = int(arg("--tex", "1024")); CRUMB = float(arg("--crumb", "0.03"))
# catalogued heights (m) and the yaw (deg) that turns the print's view to face -Y
SCALES = {
  "fig-52_greek-slave": dict(h=1.655, yaw=float(arg("--yaw", "nan")), src="Raby Castle marble (the 1851 exhibit), 165.5 x 53.5 cm (Di Bello 2016, n.3); scan 1.65 m"),
  "fig-54_elkington-jewel-cabinet": dict(h=0.97, yaw=float(arg("--yaw", "nan")), src="Royal Collection RCIN 1562, 97 x 132 x 81 cm (H x W x D); scan max 1.40 m"),
  "unnumbered_watherston-brogden-vase": dict(h=0.457, yaw=float(arg("--yaw", "nan")), src="gold vase, 95 oz; ~18 in high (secondary summary of the 1851 Great Exhibition account; VERIFY); scan 1.20 m"),
}
# print view faces +X in the Tripo export (turntable check 2026-11-09); -90 turns it to -Y
DEFAULT_YAW = {"fig-52_greek-slave": -90.0, "fig-54_elkington-jewel-cabinet": -90.0, "unnumbered_watherston-brogden-vase": -90.0}
S = SCALES[SLUG]; yaw = S["yaw"] if not math.isnan(S["yaw"]) else DEFAULT_YAW[SLUG]
src = os.path.join(SRC, SLUG + ".blend")
out = os.path.join(ROOT, "assets/scanprops", SLUG + "_hp1851.blend")
bpy.ops.wm.open_mainfile(filepath=src)
ob = [o for o in bpy.data.objects if o.type == 'MESH'][0]
tris0 = len(ob.data.polygons)
# --- strip floating crumbs
bm = bmesh.new(); bm.from_mesh(ob.data); bm.faces.ensure_lookup_table()
seen = set(); islands = []
for f in bm.faces:
    if f.index in seen: continue
    stack = [f]; isl = []; seen.add(f.index)
    while stack:
        g = stack.pop(); isl.append(g)
        for e in g.edges:
            for h in e.link_faces:
                if h.index not in seen: seen.add(h.index); stack.append(h)
    islands.append(isl)
islands.sort(key=len, reverse=True)
kill = []; kept = 0
for isl in islands:
    vs = [v.co for f in isl for v in f.verts]
    mn = Vector((min(v.x for v in vs), min(v.y for v in vs), min(v.z for v in vs)))
    mx = Vector((max(v.x for v in vs), max(v.y for v in vs), max(v.z for v in vs)))
    if (mx - mn).length < CRUMB and len(isl) < 0.002 * tris0: kill.extend(isl)
    else: kept += 1
print("ISLANDS", SLUG, len(islands), "kept", kept, "crumb faces removed", len(kill), flush=True)
bmesh.ops.delete(bm, geom=list(set(kill)), context='FACES')
bm.to_mesh(ob.data); bm.free()
# --- decimate
bpy.context.view_layer.objects.active = ob; ob.select_set(True)
n = len(ob.data.polygons)
mod = ob.modifiers.new("dec", 'DECIMATE'); mod.decimate_type = 'COLLAPSE'; mod.ratio = min(1.0, TRIS / n * 0.98)
mod.use_collapse_triangulate = True
bpy.ops.object.modifier_apply(modifier="dec")
tris1 = len(ob.data.polygons)
# --- rescale to catalogued height, yaw, origin bottom centre
h0 = ob.dimensions.z; k = S["h"] / h0
me = ob.data
me.transform(Matrix.Rotation(math.radians(yaw), 4, 'Z') @ Matrix.Scale(k, 4))
xs = [v.co.x for v in me.vertices]; ys = [v.co.y for v in me.vertices]; zs = [v.co.z for v in me.vertices]
me.transform(Matrix.Translation((-(min(xs)+max(xs))/2, -(min(ys)+max(ys))/2, -min(zs))))
me.update(); ob.location = (0, 0, 0); ob.rotation_euler = (0, 0, 0); ob.scale = (1, 1, 1)
for p in me.polygons: p.use_smooth = True
# --- textures
for im in bpy.data.images:
    if im.size[0] > TEX:
        im.scale(TEX, TEX); im.pack()
for m in list(bpy.data.materials):
    if m.users == 0: bpy.data.materials.remove(m)
ob.name = "SCN_" + SLUG; me.name = "SCN_" + SLUG + "_mesh"
ob["cp_era"] = "HP1851"; ob["cp_state"] = "Hyde Park 1851"; ob["source"] = "origin/main e88ee17 scan-models/blend/%s.blend (Tripo H3.1, image-to-3D)" % SLUG
ob["scale_basis"] = S["src"]; ob["scale_factor"] = round(k, 4); ob["tris_source"] = tris0; ob["tris"] = tris1
ob["departure"] = "EX_SCN_" + SLUG.split("_")[0].upper()
print("PREP", SLUG, "tris", tris0, "->", tris1, "scale", round(k, 4), "dims", tuple(round(d, 3) for d in ob.dimensions), flush=True)
os.makedirs(os.path.dirname(out), exist_ok=True)
bpy.ops.wm.save_as_mainfile(filepath=out, compress=True)
print("SAVED", out, flush=True)
