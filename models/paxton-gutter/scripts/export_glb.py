#!/usr/bin/env python3
"""Export paxton-gutter.glb from the saved .blend (all prop objects)."""
import bpy

bpy.ops.wm.open_mainfile(
    filepath="/home/hatch/workspace/cp-models/paxton-gutter/paxton-gutter.blend")
bpy.ops.object.select_all(action='SELECT')
bpy.ops.export_scene.gltf(
    filepath="/home/hatch/workspace/cp-models/paxton-gutter/paxton-gutter.glb",
    export_format='GLB', export_apply=True)
print("GLB exported")
