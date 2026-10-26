"""Make the published files for the course repo from a built Crystal Palace .blend: scene with lights and cameras,
renders, and a GLB.

  blender --background crystal-palace-west-03_v001.blend --python-exit-code 1 --python publish_assets.py -- \
      --stage-dir STAGE [--samples 64] [--scale 1.0] [--steps blend,shaded,glb,flat] [--views overview,iso,...]

Derived from model/render_preview.py (same white-iron look, same two sun lights, same camera definitions for the views
that existed there) plus two new cameras: `overview`, that frames the whole built length, and `joint`, a close-up of a column head. Steps:
  blend   write STAGE/crystal-palace-1851.blend with the look, lights and one camera per view (the opened file is not changed)
  shaded  render each view lit, to STAGE/renders/<view>.png
  glb     export STAGE/crystal-palace-1851.glb (flat PBR colours; collection instances become shared meshes)
  flat    render `section` and `stairsec` as white-on-black emission for the plate overlays (done last: it changes the materials)
Geometry is in metres; positions in the table below are in feet, converted. Never saves over the opened file.
"""
import argparse
import math
import sys
from pathlib import Path

import bpy
from mathutils import Vector

FT = 0.3048
argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
ap = argparse.ArgumentParser()
ap.add_argument("--stage-dir", required=True)
ap.add_argument("--samples", type=int, default=64)
ap.add_argument("--scale", type=float, default=1.0)
ap.add_argument("--steps", default="blend,shaded,glb,flat")
ap.add_argument("--views", default="overview,iso,section,nave,gallery,voidend,stairs,stairgal,joint,stairsec")
args = ap.parse_args(argv)
stage = Path(args.stage_dir)
(stage / "renders").mkdir(parents=True, exist_ok=True)
steps = set(args.steps.split(","))
scene = bpy.context.scene

scene.render.engine = "CYCLES"
scene.cycles.samples = args.samples
scene.cycles.use_denoising = True
scene.cycles.device = "CPU"
scene.render.image_settings.file_format = "PNG"
scene.view_settings.view_transform = "Standard"

look = {"MAT_Iron": (0.85, 0.85, 0.83), "MAT_Glass": (0.62, 0.74, 0.82), "MAT_Floor": (0.32, 0.32, 0.33), "MAT_Wood": (0.50, 0.40, 0.30)}
for name, rgb in look.items():
    m = bpy.data.materials.get(name)
    if m is None:
        continue
    m.use_nodes = True
    b = next((n for n in m.node_tree.nodes if n.type == "BSDF_PRINCIPLED"), None)
    if b:
        b.inputs["Base Color"].default_value = (*rgb, 1.0)
        b.inputs["Roughness"].default_value = 0.8

world = bpy.data.worlds.get("World") or bpy.data.worlds.new("World")
scene.world = world
world.use_nodes = True
bg = world.node_tree.nodes["Background"]
bg.inputs["Color"].default_value = (0.012, 0.014, 0.018, 1)
bg.inputs["Strength"].default_value = 0.6

rig = bpy.data.collections.new("CAMERAS_AND_LIGHTS")
scene.collection.children.link(rig)


def add_light(name, rot, energy, color=None, angle=None):
    d = bpy.data.lights.new(name, "SUN")
    d.energy = energy
    if color:
        d.color = color
    if angle:
        d.angle = angle
    o = bpy.data.objects.new(name, d)
    o.rotation_euler = rot
    rig.objects.link(o)
    return o


# key from the south-west and above (warm, about 3000 K), a weaker fill from the north-east
add_light("KEY", (math.radians(55), 0, math.radians(-50)), 3.0, (1.0, 0.82, 0.62), math.radians(2.0))
add_light("FILL", (math.radians(70), 0, math.radians(135)), 0.7)


def camera(name, loc_ft, look_at=None, lens=35, ortho=None, rot=None, clip_end_ft=None):
    cam = bpy.data.cameras.new(name)
    cam.lens = lens
    cam.clip_start, cam.clip_end = 0.5, (clip_end_ft * FT if clip_end_ft else 6000 * FT)
    ob = bpy.data.objects.new(name, cam)
    ob.location = Vector(loc_ft) * FT
    rig.objects.link(ob)
    if ortho:
        cam.type = "ORTHO"
        cam.ortho_scale = ortho * FT
        ob.rotation_euler = rot
    else:
        t = bpy.data.objects.new(name + "_target", None)
        t.location = look_at
        rig.objects.link(t)
        c = ob.constraints.new("TRACK_TO")
        c.target = t
        c.track_axis, c.up_axis = "TRACK_NEGATIVE_Z", "UP_Y"
    return ob


def target(x_ft, y_ft, z_ft):
    return Vector((x_ft * FT, y_ft * FT, z_ft * FT))


# focus x: 108 ft from the west end (slice 01), the nave-void line (72 ft in), the first stair bay (204 ft in)
F, FV, FS = -816.0, -852.0, -720.0
ORTHO_X = math.radians(90), 0, math.radians(-90)     # looking along +X
VIEWS = {  # name: (camera factory, resolution, exposure in stops)
    # the whole built length (888 ft between end column lines) from the south-west and high
    "overview": (lambda: camera("cam_overview", (-1230, -770, 330), target(-474, 0, 14), lens=40), (2400, 1200), 0.0),
    "iso": (lambda: camera("cam_iso", (F - 194, -330, 110), target(F, 30, 36), lens=30), (2000, 1100), 0.0),
    # orthographic from the west looking east, 440 ft across: the view to set beside Plate VI
    "section": (lambda: camera("cam_section", (F - 184, 0, 32), ortho=440, rot=ORTHO_X), (3000, 800), 0.0),
    "nave": (lambda: camera("cam_nave", (F - 84, -70, 28), target(F + 16, 40, 52), lens=22), (2000, 1100), 2.5),
    "gallery": (lambda: camera("cam_gallery", (F - 46, -20, 31), target(F + 4, 40, 26), lens=26), (2000, 1100), 2.5),
    "voidend": (lambda: camera("cam_voidend", (FV + 60, -8, 31), target(FV, 4, 26), lens=22), (2000, 1100), 2.5),
    "stairs": (lambda: camera("cam_stairs", (FS - 22, -4, 7), target(FS + 2, 84, 11), lens=20), (2000, 1300), 2.5),
    "stairgal": (lambda: camera("cam_stairgal", (FS - 14, 44, 31), target(FS + 2, 84, 18), lens=20), (2000, 1300), 2.5),
    # a close-up of a column head on grid line 5 (108 ft in), row y = 60 ft: shaft, connecting piece, girders, floor edge, railing
    "joint": (lambda: camera("cam_joint", (-830, 26, 13), target(-804, 60, 21), lens=35), (2000, 1300), 2.5),
    # orthographic along the flights, north avenue at the centre: the view to set beside Plate XV
    "stairsec": (lambda: camera("cam_stairsec", (FS + 13, 84, 14), ortho=56, rot=(math.radians(90), 0, math.radians(90)),
                                clip_end_ft=26), (2800, 1500), 2.5),
}
want = [v.strip() for v in args.views.split(",") if v.strip()]
cams = {}
for v in VIEWS:                      # every camera is saved in the .blend, whichever views are rendered now
    cams[v] = VIEWS[v][0]()
    cams[v]["view_resolution"] = list(VIEWS[v][1])
    cams[v]["view_exposure"] = VIEWS[v][2]


def use(v, suffix=""):
    scene.camera = cams[v]
    res, exp = VIEWS[v][1], VIEWS[v][2]
    scene.render.resolution_x, scene.render.resolution_y = int(res[0] * args.scale), int(res[1] * args.scale)
    scene.view_settings.exposure = exp


if "blend" in steps:
    use("iso")
    bpy.ops.wm.save_as_mainfile(filepath=str(stage / "crystal-palace-1851.blend"), copy=True)
    print("saved", stage / "crystal-palace-1851.blend")

if "shaded" in steps:
    for v in want:
        use(v)
        scene.render.filepath = str(stage / "renders" / f"{v}.png")
        bpy.ops.render.render(write_still=True)
        print("rendered", scene.render.filepath, "samples", args.samples)

if "glb" in steps:
    scene.view_settings.exposure = 0.0
    bpy.ops.export_scene.gltf(filepath=str(stage / "crystal-palace-1851.glb"), export_format="GLB", use_selection=False,
                              export_cameras=False, export_lights=False, export_apply=False)
    print("exported", stage / "crystal-palace-1851.glb")

if "flat" in steps:   # white emission on black, nothing depends on the lights: for the overlays on the plates
    for m in bpy.data.materials:
        m.use_nodes = True
        b = next((n for n in m.node_tree.nodes if n.type == "BSDF_PRINCIPLED"), None)
        if b:
            b.inputs["Base Color"].default_value = (0, 0, 0, 1)
            b.inputs["Emission Color"].default_value = (1, 1, 1, 1)
            b.inputs["Emission Strength"].default_value = 1.0
    for o in rig.objects:
        if o.type == "LIGHT":
            o.data.energy = 0.0
    bg.inputs["Color"].default_value = (0, 0, 0, 1)
    bg.inputs["Strength"].default_value = 0.0
    for v in ("section", "stairsec"):
        use(v)
        scene.view_settings.exposure = 0.0
        scene.render.filepath = str(stage / "renders" / f"{v}_flat.png")
        bpy.ops.render.render(write_still=True)
        print("rendered", scene.render.filepath, "flat")
