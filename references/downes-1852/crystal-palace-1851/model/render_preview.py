"""Render review views of a Crystal Palace model: white model on a dark ground, soft key light.

  blender --background model/crystal-palace-slice-01_v002.blend --python-exit-code 1 \
    --python model/render_preview.py -- --out-dir model/previews --tag slice01_v002 \
    [--views section,iso,nave,gallery,voidend] [--focus-x -852] [--flat] [--exposure 2.5] [--samples 32] [--scale 1.0] [--device CPU|GPU]

Nothing here is specific to this Mac: every path, the resolution, the sample count and the device are
arguments, so the same file renders the final frames on Explorer (check the Blender version there first;
this was written against 5.1.2). It never saves the .blend. Views:
  section  orthographic, from the west, looking east: compare directly with Plate VI (the transverse section)
  iso      perspective from the south-west, high, to see the stepped tiers and the roof
  nave     perspective inside the nave, low, to see the frame and the roof from within
  gallery  perspective from the nave void at gallery height, looking at the floor strip and railing
  voidend  perspective from inside the nave void, looking west at the cross railing at the void's end (set --focus-x to that line)
  stairs, stairgal, stairsec  a staircase from the nave floor, from the gallery, and in section along the flights (set --focus-x to the middle of the stair bay, -720)
Geometry is in metres; positions below are in feet, converted.
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
ap.add_argument("--out-dir", required=True)
ap.add_argument("--tag", required=True, help="file name stem, e.g. slice01_v002")
ap.add_argument("--views", default="section,iso,nave")
ap.add_argument("--samples", type=int, default=32)
ap.add_argument("--scale", type=float, default=1.0, help="resolution multiplier")
ap.add_argument("--device", choices=["CPU", "GPU"], default="CPU")
ap.add_argument("--flat", action="store_true",
                help="flat white emission on black, no lighting: for overlays on the plates, where shadow must not hide a part")
ap.add_argument("--exposure", type=float, default=0.0,
                help="stops added to the exposure (colour management); the interior views under the roofs are dark at 0")
ap.add_argument("--focus-x", type=float, default=-816.0,
                help="ft along the length that the cameras look at (default: the middle of slice 01)")
args = ap.parse_args(argv)
out = Path(args.out_dir)
out.mkdir(parents=True, exist_ok=True)

scene = bpy.context.scene
scene.render.engine = "CYCLES"
scene.cycles.samples = args.samples
scene.cycles.use_denoising = True
scene.cycles.device = "GPU" if args.device == "GPU" else "CPU"
scene.render.image_settings.file_format = "PNG"
scene.view_settings.view_transform = "Standard"
scene.view_settings.exposure = args.exposure

# materials: white iron, pale glass, grey floor ----------------------------------------------------
look = {"MAT_Iron": (0.85, 0.85, 0.83), "MAT_Glass": (0.62, 0.74, 0.82), "MAT_Floor": (0.32, 0.32, 0.33),
        "MAT_Wood": (0.50, 0.40, 0.30)}
for name, rgb in look.items():
    m = bpy.data.materials.get(name)
    if m is None:
        continue
    m.use_nodes = True
    bsdf = next((n for n in m.node_tree.nodes if n.type == "BSDF_PRINCIPLED"), None)
    if bsdf:
        bsdf.inputs["Base Color"].default_value = (*rgb, 1.0)
        bsdf.inputs["Roughness"].default_value = 0.8

if args.flat:  # every surface emits white; the background is black; nothing depends on the lights
    for m in bpy.data.materials:
        m.use_nodes = True
        b = next((n for n in m.node_tree.nodes if n.type == "BSDF_PRINCIPLED"), None)
        if b:
            b.inputs["Base Color"].default_value = (0, 0, 0, 1)
            b.inputs["Emission Color"].default_value = (1, 1, 1, 1)
            b.inputs["Emission Strength"].default_value = 1.0

# world and lights -----------------------------------------------------------------------------------
world = bpy.data.worlds.get("World") or bpy.data.worlds.new("World")
scene.world = world
world.use_nodes = True
bg = world.node_tree.nodes["Background"]
bg.inputs["Color"].default_value = (0, 0, 0, 1) if args.flat else (0.012, 0.014, 0.018, 1)
bg.inputs["Strength"].default_value = 1.0


def add_light(kind, name, loc, energy, rot=None, size=None):
    d = bpy.data.lights.new(name, kind)
    d.energy = energy
    if size is not None and kind == "AREA":
        d.size = size
    o = bpy.data.objects.new(name, d)
    o.location = loc
    if rot:
        o.rotation_euler = rot
    scene.collection.objects.link(o)
    return o


# key from the south-west and above, a weaker fill from the north-east; warm key (about 3000 K) as in the reference film
add_light("SUN", "KEY", (0, 0, 0), 0.0 if args.flat else 3.0, rot=(math.radians(55), 0, math.radians(-50)))
add_light("SUN", "FILL", (0, 0, 0), 0.0 if args.flat else 0.7, rot=(math.radians(70), 0, math.radians(135)))
scene.world.node_tree.nodes["Background"].inputs["Strength"].default_value = 0.0 if args.flat else 0.6
key = bpy.data.objects["KEY"].data
key.color = (1.0, 0.82, 0.62)
key.angle = math.radians(2.0)

F = args.focus_x
target = Vector((F * FT, 0, 32 * FT))  # the focus point: middle of the part being reviewed


def camera(name, loc_ft, look_at=target, lens=35, ortho=None, rot=None, clip_end_ft=None):
    cam = bpy.data.cameras.new(name)
    cam.lens = lens
    cam.clip_start, cam.clip_end = 0.5, (clip_end_ft * FT if clip_end_ft else 4000)
    ob = bpy.data.objects.new(name, cam)
    ob.location = Vector(loc_ft) * FT
    scene.collection.objects.link(ob)
    if ortho:
        cam.type = "ORTHO"
        cam.ortho_scale = ortho * FT
        ob.rotation_euler = rot
    else:
        c = ob.constraints.new("TRACK_TO")
        c.target = bpy.data.objects.new(name + "_target", None)
        c.target.location = look_at
        scene.collection.objects.link(c.target)
        c.track_axis, c.up_axis = "TRACK_NEGATIVE_Z", "UP_Y"
    return ob


views = {
    # looking along +X: rotate 90 deg about X (look +Y), then -90 deg about Z (look +X)
    "section": dict(cam=lambda: camera("cam_section", (F - 184, 0, 32), ortho=440,
                                       rot=(math.radians(90), 0, math.radians(-90))), res=(3000, 800)),
    "iso": dict(cam=lambda: camera("cam_iso", (F - 194, -330, 110), look_at=Vector((F * FT, 30 * FT, 36 * FT)),
                                   lens=30), res=(2000, 1100)),
    "nave": dict(cam=lambda: camera("cam_nave", (F - 84, -70, 28), look_at=Vector(((F + 16) * FT, 40 * FT, 52 * FT)),
                                    lens=22), res=(2000, 1100)),
    "gallery": dict(cam=lambda: camera("cam_gallery", (F - 46, -20, 31), look_at=Vector(((F + 4) * FT, 40 * FT, 26 * FT)),
                                       lens=26), res=(2000, 1100)),
    # inside the nave void, 60 ft east of the line where it begins, looking west at the cross railing and floor
    "voidend": dict(cam=lambda: camera("cam_voidend", (F + 60, -8, 31), look_at=Vector((F * FT, 4 * FT, 26 * FT)),
                                       lens=22), res=(2000, 1100)),
}
views.update({
    # a staircase (focus x = the middle of its 24 ft bay): from the nave floor looking at the north avenue's stair
    "stairs": dict(cam=lambda: camera("cam_stairs", (F - 22, -4, 7), look_at=Vector(((F + 2) * FT, 84 * FT, 11 * FT)),
                                      lens=20), res=(2000, 1300)),
    # from the nave-side gallery looking north over the cross gallery, the wells and the landing
    "stairgal": dict(cam=lambda: camera("cam_stairgal", (F - 14, 44, 31), look_at=Vector(((F + 2) * FT, 84 * FT, 18 * FT)),
                                        lens=20), res=(2000, 1300)),
    # orthographic along the flights (looking west from the east), north avenue at the centre: overlay on Plate XV's section.
    # The camera sits 13 ft east of the focus and sees only 26 ft in front of it (the stair bay and a little more).
    "stairsec": dict(cam=lambda: camera("cam_stairsec", (F + 13, 84, 14), ortho=56,
                                        rot=(math.radians(90), 0, math.radians(90)), clip_end_ft=26), res=(2800, 1500)),
})
for v in [x.strip() for x in args.views.split(",") if x.strip()]:
    spec = views[v]
    cam = spec["cam"]()
    scene.camera = cam
    scene.render.resolution_x = int(spec["res"][0] * args.scale)
    scene.render.resolution_y = int(spec["res"][1] * args.scale)
    scene.render.filepath = str(out / f"{args.tag}_{v}.png")
    bpy.ops.render.render(write_still=True)
    print("rendered", scene.render.filepath, "samples", args.samples, "device", args.device)
    bpy.data.objects.remove(cam, do_unlink=True)
