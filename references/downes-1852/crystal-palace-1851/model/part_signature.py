"""Print a short hash over every placed part of a model: name, kind, position, rotation and custom properties.

  blender --background model/crystal-palace-west-02_v001.blend --python-exit-code 1 --python model/part_signature.py

Used as the regression test for build_slice.py: a new version of the builder must reproduce the old files' hashes for
the ranges that existed before (positions are rounded to 0.1 mm, so geometry changes inside a part library do NOT
change the hash; it guards the plan, the placement and the properties). Known values, 2026-10-17:
  crystal-palace-slice-01_v004.blend   31d28a05cb53a430  308 parts   (build_slice.py --lines 4:5)
  crystal-palace-west-01_v001.blend    baa9ab74096de122  1328 parts  (--lines 0:6)
  crystal-palace-west-02_v001.blend    ede6c112ab6a9a58  2580 parts  (--lines 0:12)
  crystal-palace-west-03_v001.blend    af709609ae4364c6  7757 parts  (--lines 0:37)
Never saves anything.
"""
import hashlib
import json

import bpy

rows = []
for o in sorted(bpy.data.objects, key=lambda o: o.name):
    if o.get("part_kind"):
        rows.append([o.name, o["part_kind"], round(o.location.x, 4), round(o.location.y, 4), round(o.location.z, 4),
                     round(o.rotation_euler.z, 4), sorted((k, str(o[k])) for k in o.keys())])
print("SIG", hashlib.sha256(json.dumps(rows).encode()).hexdigest()[:16], len(rows))
