"""Render named cameras from a transept .blend.
blender -b rounds/rNN.blend -P render_views.py -- --cams A,B --outdir renders/rNN --res 960x540 --samples 48 [--portrait A] [--claude path.blend [--no-furrow]]"""
import bpy, sys, os

# crystal-palace-look v1 (shared grade)
try:
    from cpl_look import apply_look, era_for_scene, tod_for_scene
except ImportError:
    import sys as _s
    _s.path.insert(0, "/workspace/crystal-palace-survey/look")
    from crystal_palace_look import apply_look, era_for_scene, tod_for_scene

# crystal-palace-people v2 (swap lathe crowds → articulated; skip with --no-people)
try:
    from cpl_people import swap_scene_people, PEOPLE_VERSION as _PPL_VER
except ImportError:
    import sys as _s
    from pathlib import Path as _P
    _s.path.insert(0, "/workspace/crystal-palace-survey/people")
    try:
        from people_lib import swap_scene_people, PEOPLE_VERSION as _PPL_VER
    except ImportError:
        swap_scene_people = None; _PPL_VER = None

argv = sys.argv[sys.argv.index("--") + 1:]
def arg(n, d=None): return argv[argv.index(n) + 1] if n in argv else d
cams = arg("--cams").split(","); outdir = arg("--outdir"); W, H = map(int, arg("--res", "960x540").split("x"))
portrait = set((arg("--portrait", "") or "").split(","))
sc = bpy.context.scene; sc.cycles.samples = int(arg("--samples", "48"))
if arg("--exposure"): sc.view_settings.exposure = float(arg("--exposure"))   # review-only override (REV_combo seam check)
sc.render.threads_mode = 'FIXED'; sc.render.threads = int(arg("--threads", "8"))
claude = arg("--claude")
if claude:   # append Claude's model collection read-only (never saved)
    with bpy.data.libraries.load(claude, link=False) as (src, dst):
        dst.collections = [c for c in src.collections if c == "MODEL"]
    for c in dst.collections:
        if c: sc.collection.children.link(c)
    # hide our duplicates on Claude's line 37 (x = -36 ft)
    for ob in bpy.data.objects:
        if ob.get("claude_line37") or ob.get("claude_overlap"): ob.hide_render = True
        if ob.get("show_with_claude"): ob.hide_render = False   # r09: Muse Una at its catalogue cell S29 (Claude's zone)
        elif ob.get("part_kind") in ("column", "girder", "roof") and ob.location.x < -0.3048 * 36.5: ob.hide_render = True
    # RL02: Claude's appended roof units get our roof glass at render time (seam match); his file is never saved
    rg = bpy.data.materials.get("GT_Glass"); n = 0
    if rg:   # RL03: Claude's roof mesh has no usable UVs -> drive any UV-based bar mask from object coords (ft)
        cl = rg.copy(); cl.name = "GT_Glass_CL"
        for tc in [x for x in cl.node_tree.nodes if x.type == 'TEX_COORD']:
            for dst in [lk.to_socket for lk in tc.outputs["UV"].links]:
                v = cl.node_tree.nodes.new("ShaderNodeVectorMath"); v.operation = 'SCALE'; v.inputs["Scale"].default_value = 1 / 0.3048
                cl.node_tree.links.new(tc.outputs["Object"], v.inputs[0]); cl.node_tree.links.new(v.outputs[0], dst)
        rg = cl
    def roofglass(m):   # RL04: exterior roof-glass recipe (EX19: tint .58/.64/.64, milk .025 @ .55) for the combined review
        for nd in m.node_tree.nodes:
            if nd.type == 'BSDF_TRANSPARENT': nd.inputs[0].default_value = (0.58, 0.64, 0.64, 1)
            if nd.type == 'BSDF_DIFFUSE' and nd.inputs[0].default_value[0] > 0.85: nd.inputs[0].default_value = (0.55, 0.58, 0.58, 1)
            if nd.type == 'MIX_SHADER' and not nd.inputs[0].is_linked and abs(nd.inputs[0].default_value - 0.06) < 1e-3: nd.inputs[0].default_value = 0.025
        return m
    if rg: roofglass(rg)
    own = {}
    for ob in bpy.data.objects:   # our own flat roof units in the combined review get the same recipe
        if ob.get("part_kind") == "roof" and ob.type == 'MESH':
            for sl in ob.material_slots:
                if sl.material and sl.material.name in ("GT_Glass", "GT_RoofGlass"):
                    if "r" not in own: own["r"] = roofglass(sl.material.copy()); own["r"].name = "GT_Glass_ROOFREV"
                    sl.link = 'OBJECT'; sl.material = own["r"]
    for c in bpy.data.collections:
        if c.name.startswith("PART_RoofUnit") and c.library is None:
            for ob in c.all_objects:
                for sl in ob.material_slots:
                    if rg and sl.material and sl.material.name.startswith("MAT_Glass"): sl.material = rg; n += 1
    print("CLAUDE_ROOF_OVERRIDE slots", n, flush=True)
    if "--no-furrow" not in argv:   # RL05: flat roof units (his and ours) -> Muse's furrow bay, instanced, render time only
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        import furrow; furrow.swap_flat_roofs()
# apply shared look once per blend (override with --era / --tod)
# --keep-lighting: people-only pass — preserve blend world/sun/exposure/grade
_era = arg("--era", "1851"); _tod = arg("--tod", "interior_daylit")
if "--keep-lighting" in argv:
    print("KEEP_LIGHTING exposure", sc.view_settings.exposure,
          "look", sc.view_settings.look, flush=True)
else:
    apply_look(era=_era, time_of_day=_tod)
if arg("--exposure"):
    sc.view_settings.exposure = float(arg("--exposure"))
    print("EXPOSURE_OVERRIDE", sc.view_settings.exposure, flush=True)
os.makedirs(outdir, exist_ok=True)
for c in cams:
    cam = bpy.data.objects.get(c)
    if not cam: print("NO CAM", c); continue
    sc.camera = cam
    if swap_scene_people is not None and "--no-people" not in argv:
        _pst = swap_scene_people(era=_era, camera=cam)
        print("PEOPLE", _PPL_VER, _pst, flush=True)
    if c in portrait: sc.render.resolution_x, sc.render.resolution_y = H * 3 // 4, int(H * 1.0)
    else: sc.render.resolution_x, sc.render.resolution_y = W, H
    sc.render.filepath = os.path.join(outdir, c + ".png")
    bpy.ops.render.render(write_still=True)
    print("WROTE", sc.render.filepath, flush=True)
