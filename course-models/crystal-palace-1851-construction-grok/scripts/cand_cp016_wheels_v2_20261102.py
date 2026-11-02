"""2026-11-02 CANDIDATE v2 (Grok Bot executor, not a verdict): CP016_wheels 'wheels' read.
Base: the live CP016_wheels blend rounds/candidates/c06_cp016wheels.blend (KEEP 2026-11-02, CN43). Saves
rounds/candidates/c06_cp016wheels_v2.blend (CP016_wheels only; never render other shots from it).
Flags (after --):
  --stub-axles    move wagon side frames (axle bearer, posts, sole beam) 3 in inboard so each iron wheel sits
                  outboard on a stub axle, its outer face clear of the bearer (DEPARTURES CN44, inferred)
  --glaziers      two people_lib 1850s workmen (cap, smock, trousers, boots) on wagon_0's deck (CN44)
  --swap-workers  people_lib 1850s workmen (hero < 40 ft, else mid) for every still-visible KWORKER_*_CP016 (wagons 1-3 and the
                  gutter men). At 32 mm all of them exceed the people_lib 3.4 close-up gate (8% of frame height), so render-time
                  swap would leave them as grey block proxies. Pose map: kneel/work -> working, reach -> pointing (no kneel pose in 3.4).
  --cam V         camera variant: keep | kneel (operator kneels on the 24 ft deck, eye 27.0 ft) | ...
blender -b rounds/candidates/c06_cp016wheels.blend -P scripts/cand_cp016_wheels_v2_20261102.py -- --stub-axles --glaziers --cam kneel"""
import bpy, mathutils, os, sys
F = 0.3048
argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
def arg(n, d=None): return argv[argv.index(n) + 1] if n in argv else d
OUTB = arg("--out")
def aim(name, pos, look, lens=50.0):
    ob = bpy.data.objects[name]
    ob.location = mathutils.Vector(pos) * F
    d = mathutils.Vector(look) * F - ob.location
    ob.rotation_mode = 'XYZ'; ob.rotation_euler = d.to_track_quat('-Z', 'Y').to_euler(); ob.data.lens = lens
    ob["cand_v2_20261102"] = f"cam {arg('--cam', 'keep')}"
CAMS = {
    "keep": None,
    # operator kneels on the same deck (eye 3.0 ft above deck 24); aim lower, onto the SW wheel/gutter
    "kneel": (((332.0, -212.0, 27.0), (328.8, -196.0, 22.9)), ((332.0, -210.5, 27.0), (328.6, -196.0, 22.8))),
    "kneel_low": (((332.0, -212.0, 27.0), (328.8, -196.0, 22.4)), ((332.0, -210.5, 27.0), (328.6, -196.0, 22.3))),
    "front": (((332.0, -208.6, 29.25), (328.8, -196.0, 22.6)), ((331.0, -208.6, 29.25), (328.6, -196.0, 22.5))),
    "front_kneel": (((332.0, -208.6, 27.0), (329.0, -196.0, 22.9)), ((331.0, -208.6, 27.0), (328.8, -196.0, 22.8))),
    # operator at the north lip of the roof-edge deck (deck y -216..-208), still between the x 328 / 336 standards;
    # 40 mm, aimed at the deck so wheels, gutter and seated glaziers are all in frame; end = 3 ft slide west along the deck
    "front40": (((333.5, -208.6, 29.25), (329.8, -194.5, 24.3), 40.0), ((330.5, -208.6, 29.25), (329.6, -194.5, 24.3), 40.0)),
    # 32 / 28 mm: wide enough that standing glaziers' heads (~30 ft, near eye height) and the wheels in the gutter both fit
    "front32": (((333.5, -208.6, 29.25), (329.8, -194.5, 25.4), 32.0), ((330.5, -208.6, 29.25), (329.6, -194.5, 25.4), 32.0)),   # aim 25.4: SW wheel clear of the bottom edge
    "front28": (((333.5, -208.6, 29.25), (329.8, -194.5, 26.1), 28.0), ((330.5, -208.6, 29.25), (329.6, -194.5, 26.1), 28.0)),
    "front40b": (((333.5, -208.6, 29.25), (329.8, -194.5, 23.9), 40.0), ((330.5, -208.6, 29.25), (329.6, -194.5, 23.9), 40.0)),
}
v = CAMS[arg("--cam", "keep")]
if v:
    aim("CP016_wheels_start", *v[0]); aim("CP016_wheels_end", *v[1])
me = bpy.data.meshes["glazing_wagon"]
if "--stub-axles" in argv:
    tyre = [m.name for m in me.materials].index("GT_CartTyre"); moved = set()
    for poly in me.polygons:
        if poly.material_index == tyre: continue
        vs = [me.vertices[i].co / F for i in poly.vertices]
        for sy in (-4.0, 4.0):
            if all(abs(c.y - sy) <= 2.05 / 12 and c.z <= 1.91 for c in vs):
                for i in poly.vertices:
                    if i not in moved:
                        me.vertices[i].co.y -= (0.25 * F) * (1 if sy > 0 else -1); moved.add(i)
    me.update(); print("STUB_AXLES moved verts", len(moved))
if "--glaziers" in argv:
    sys.path.insert(0, "/workspace/crystal-palace-survey/people")
    import people_lib as PL
    deck = 22.17 + 2.05
    # name avoids people_lib figure prefixes so the render-time swap leaves them as built (hero LOD, clothed)
    # people_lib 3.4 'seated' is broken at close range (smock shell lost, floating sleeves and cap: tested 2026-11-02),
    # so both glaziers stand, near the c05 wagon_0 worker spots (KWORKER_013 / 014; #1 moved behind the pane crate so the two never overlap), facing the south slope being glazed (rz 0 = -y)
    spec = [("GLAZIER_CP016W_0", "working", 2207, (329.0, -193.8, deck), 10.0),
            ("GLAZIER_CP016W_1", "standing", 3301, (330.9, -189.4, deck), -25.0)]
    col = bpy.data.objects["KWAGON_0"].users_collection[0]
    for name, pose, seed, pos, rz in spec:
        tmp = PL._build_person("1850s_workman", pose, "hero", seed)
        ob = bpy.data.objects.new(name, tmp.data); col.objects.link(ob)
        bpy.data.objects.remove(tmp, do_unlink=True)
        ob.location = mathutils.Vector(pos) * F; ob.rotation_euler = (0, 0, __import__("math").radians(rz))
        ob["cand_v2_20261102"] = f"people_lib {PL.PEOPLE_VERSION} 1850s_workman {pose} hero"; ob["only_cams"] = "CP016_wheels"
        print("GLAZIER", name, pose, [round(c, 2) for c in ob.dimensions])
if "--swap-workers" in argv:
    sys.path.insert(0, "/workspace/crystal-palace-survey/people")
    import people_lib as PL, hashlib
    cam = bpy.data.objects["CP016_wheels_start"].matrix_world.translation
    PMAP = {"kneel": "working", "work": "working", "reach": "pointing"}; n = 0
    for o in list(bpy.data.objects):
        if o.name.startswith("KWORKER_") and o.name.endswith("_CP016") and not o.hide_render:
            d = (o.matrix_world.translation - cam).length / F; lod = "hero" if d < 40 else "mid"
            seed = int(hashlib.md5(o.name.encode()).hexdigest()[:6], 16)
            tmp = PL._build_person("1850s_workman", PMAP.get(o.get("pose"), "working"), lod, seed)
            mw = o.matrix_world.copy(); o.data = tmp.data; bpy.data.objects.remove(tmp, do_unlink=True)
            o.matrix_world = mw; o.scale = (1, 1, 1); o["cpl_people"] = PL.PEOPLE_TAG; o["cand_v2_20261102"] = f"people_lib swap {lod} (gate bypass, CP016_wheels only)"; n += 1
    print("SWAP_WORKERS", n)
here = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
out = OUTB or os.path.join(here, "rounds", "candidates", "c06_cp016wheels_v2.blend")
bpy.ops.wm.save_as_mainfile(filepath=out, copy=True, compress=True); print("SAVED", out)
