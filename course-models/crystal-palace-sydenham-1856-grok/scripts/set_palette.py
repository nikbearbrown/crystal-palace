"""Toggle Owen Jones-style polychromy (U) on iron: blender -b X.blend -P scripts/set_palette.py -- <0|1> <out.blend>"""
import bpy, sys
a = sys.argv[sys.argv.index('--')+1:]; v = float(a[0])
for m in bpy.data.materials:
    if m.node_tree and 'OJ_TOGGLE' in m.node_tree.nodes: m.node_tree.nodes['OJ_TOGGLE'].outputs[0].default_value = v; print('set', m.name, v)
bpy.ops.wm.save_as_mainfile(filepath=a[1], compress=True)
