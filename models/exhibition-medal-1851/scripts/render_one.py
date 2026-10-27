#!/usr/bin/env python3
"""Render one view from the saved blend: blender -b <blend> -P render_one.py -- <view>
Also prints mesh stats on the 'stats' pseudo-view."""
import bpy, sys, os

argv = sys.argv[sys.argv.index("--") + 1:]
view = argv[0]
BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
scene = bpy.context.scene
medal = bpy.data.objects["exhibition-medal-1851"]
tris = sum(len(p.vertices) - 2 for p in medal.data.polygons)
print(f"TRIANGLES: {tris}")
print("DIMS: %.5f x %.5f x %.5f m" % tuple(medal.dimensions))
print("ORIGIN (object location):", tuple(medal.location))

if view == "stats":
    sys.exit(0)
camname = {"front": "CamFront", "reverse": "CamReverse",
           "side": "CamSide", "three-quarter": "CamTQ"}[view]
scene.camera = bpy.data.objects[camname]
scene.render.filepath = os.path.join(BASE, "renders", view + ".png")
bpy.ops.render.render(write_still=True)
print("rendered", view)
