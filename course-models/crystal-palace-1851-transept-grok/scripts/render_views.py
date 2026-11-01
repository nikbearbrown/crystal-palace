"""Render named cameras from a transept .blend.
blender -b rounds/rNN.blend -P render_views.py -- --cams A,B --outdir renders/rNN --res 960x540 --samples 48 [--portrait A] [--shot-exposure] [--claude path.blend [--no-furrow]]"""
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
# Per-shot exposure cheat (2026-11-01; pattern from the exhibits folder's per-shot --exposure).
# Opt-in with --shot-exposure: without the flag every camera renders exactly as before.
# Cameras absent from the table keep the scene/look/--exposure value unchanged.
# 2026-11-01 envelope v2 review: the table is now per-blend. The -2.2 cheat was tuned for
# r11_envelope.blend's extra lights and applies ONLY to that blend. r11_envelope_v2.blend
# (CP023 live source) renders at the normal look exposure; no per-shot entry.
SHOT_EXPOSURE = {
    "r11_envelope.blend": {
        "CP023_into_nave_start": -2.2,   # HP interior envelope v1 (superseded): reads at -1.6..-2.2 (envjudge)
        "CP023_into_nave_end": -2.2,
    },
}
_blend_name = os.path.basename(bpy.data.filepath)
_shot_tab = SHOT_EXPOSURE.get(_blend_name, {})
_use_shot_exp = "--shot-exposure" in argv
_base_exp = sc.view_settings.exposure
# 2026-11-01 people close-up gate, per shot (always on, not opt-in).
# people_lib 3.4 skips any figure taller than CLOSE_UP_FRAME_FRAC (8%) of frame height and
# leaves the old block stand-in. On eye-level CP023 that is 103 of 104 visible figures, so
# when CP023 is rendered first (short runs) the whole crowd stays blocky; in the 14-camera
# round they were already swapped by earlier wide cameras (order-dependent leak). For the
# cameras below the gate is off: every figure is swapped for THIS camera's LOD ranking,
# whatever ran before. Other cameras keep the library default.
SHOT_PEOPLE_GATE_OFF = {"CP023_into_nave_start", "CP023_into_nave_end"}
_PG = getattr(swap_scene_people, "__globals__", None) if swap_scene_people else None
_gate_lib = _PG.get("_is_close_up_for_base_mesh") if _PG else None
# 2026-11-01 CP023 crowd dressing (DEPARTURES PPL-C01..C04): for the two CP023 cameras only,
# figures above the gate get standing poses and all ladies a back-of-head bonnet (wrappers around
# the library's pose pick and build_bonnet, private mesh cache, installed only for this call), then cp023_dressing.dress() moves/hides figures cut by the
# frame edge or within ~3 m of the camera and hides stray hat parts; undone after the render.
# Shared people_lib unchanged. --no-cp023-dressing renders the previous behaviour.
SHOT_CROWD_DRESSING = {"CP023_into_nave_start", "CP023_into_nave_end"}
try:
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    import cp023_dressing as _cpd
except ImportError:
    _cpd = None
_use_dress = _cpd is not None and "--no-cp023-dressing" not in argv
# 2026-11-01 boots + foreground CANDIDATE (DEPARTURES PPL-C05/C06), opt-in, CP023 dressing only:
#   --cp023-boots       foot-fitted ~27-28 cm period boots (cp023_dressing.make_boots) in the CP023 swap
#   --cp023-foreground  before the swap, move a few off-frame floor figures into the empty lower third
#                       (cp023_dressing.foreground: 4-7 m, fully in frame, clear of the nave axis)
#   --save-blend-dir D  after dressing each camera, save a copy of the dressed scene to D/<blend>_<cam>.blend
# Without these flags the live CP023 pipeline (render_cp023_v2.sh) is unchanged.
_use_boots = "--cp023-boots" in argv
_use_fg = "--cp023-foreground" in argv
_save_dir = arg("--save-blend-dir")
os.makedirs(outdir, exist_ok=True)
for c in cams:
    cam = bpy.data.objects.get(c)
    if not cam: print("NO CAM", c); continue
    sc.camera = cam
    sc.view_settings.exposure = _shot_tab[c] if (_use_shot_exp and c in _shot_tab) else _base_exp
    if _use_shot_exp and c in _shot_tab: print("SHOT_EXPOSURE", _blend_name, c, sc.view_settings.exposure, flush=True)
    _dr = False
    if swap_scene_people is not None and "--no-people" not in argv:
        _off = c in SHOT_PEOPLE_GATE_OFF and _gate_lib is not None
        _dr = _use_dress and c in SHOT_CROWD_DRESSING and _PG is not None
        if _dr: sc.render.resolution_x, sc.render.resolution_y = W, H   # gate/edge tests at the render frame
        if _off: _PG["_is_close_up_for_base_mesh"] = lambda ob, cam, threshold=None: False
        _fg_undo = None
        if _dr and _use_fg:
            _fst, _flog, _fg_undo = _cpd.foreground(cam, _PG["_is_figure"], _PG["_infer_kind"])
            for _l in _flog: print("CP023_FG", c, _l, flush=True)
            print("CP023_FG_STATS", c, _fst, flush=True)
        try:
            if _dr:
                with _cpd.people_patch(_PG, _gate_lib, cam, boots=_use_boots) as _pp:
                    _pst = swap_scene_people(era=_era, camera=cam)
                _pst["pose_replaced"] = _pp["pose_replaced"]
                if _use_boots: _pst["cp023_boots"] = _pp.get("boots", 0); _pst["boot_dims"] = sorted(_pp.get("boot_dims", ()))
            else:
                _pst = swap_scene_people(era=_era, camera=cam)
        finally:
            if _off: _PG["_is_close_up_for_base_mesh"] = _gate_lib
        print("PEOPLE", _PPL_VER, _pst, "gate_off" if _off else "gate_lib", flush=True)
        if _dr:
            _dst, _dlog, _undo = _cpd.dress(cam, _PG["_is_figure"])
            for _l in _dlog: print("CP023_DRESS", c, _l, flush=True)
            print("CP023_DRESS_STATS", c, _dst, flush=True)
    if c in portrait: sc.render.resolution_x, sc.render.resolution_y = H * 3 // 4, int(H * 1.0)
    else: sc.render.resolution_x, sc.render.resolution_y = W, H
    sc.render.filepath = os.path.join(outdir, c + ".png")
    bpy.ops.render.render(write_still=True)
    print("WROTE", sc.render.filepath, flush=True)
    if _save_dir:
        os.makedirs(_save_dir, exist_ok=True)
        _bp = os.path.join(os.path.abspath(_save_dir), os.path.splitext(_blend_name)[0] + "_" + c + ".blend")
        bpy.ops.wm.save_as_mainfile(filepath=_bp, copy=True, compress=True)
        print("SAVED_BLEND", _bp, flush=True)
    if _dr:
        _undo()
        if _fg_undo: _fg_undo()
