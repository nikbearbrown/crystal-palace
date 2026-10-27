"""Shared assembly logic for the combined 1851 building (used by render_views.py and assemble_hp1851.py).
Appends (copies) Claude's MODEL and Grok's TRANSEPT_GROK read-only into the open exterior scene; never saves their files."""
import bpy
FT = 0.3048
def append(path, name):
    sc = bpy.context.scene
    with bpy.data.libraries.load(path, link=False) as (src, dst):
        dst.collections = [c for c in src.collections if c == name]
    for c in dst.collections:
        if c: sc.collection.children.link(c); return c
def override_claude_roofs():
    """EX24: Claude's appended roof units (PART_RoofUnit 'roof' mesh, MAT_Glass) get Grok's exterior roof glass."""
    rg = bpy.data.materials.get("GT_RoofGlassExt"); n = 0
    if not rg: print("NO GT_RoofGlassExt"); return 0
    for c in bpy.data.collections:
        if c.name.startswith("PART_RoofUnit") and c.library is None:
            for ob in c.all_objects:
                for sl in ob.material_slots:
                    if sl.material and sl.material.name.startswith("MAT_Glass"): sl.material = rg; n += 1
    print("CLAUDE_ROOF_OVERRIDE slots", n, flush=True); return n
def _hide(ob):
    ob.hide_render = True; ob.hide_viewport = True
def combine(claude=None, transept=None, roof_override=True):
    out = {}
    if claude:
        out["claude"] = append(claude, "MODEL")
        if roof_override: out["roof_slots"] = override_claude_roofs()
    if transept:
        T = append(transept, "TRANSEPT_GROK"); out["transept"] = T
        for ob in [o for o in T.all_objects if o is not None]:
            x, y, z = ob.location / FT; pk = ob.get("part_kind")
            if claude and (ob.get("claude_line37") or ob.get("claude_overlap") or (pk in ("column", "girder", "roof") and x < -36.5)):
                _hide(ob)
            if ob.name.startswith(("WALL_N1_", "WALLF_N1_", "WLOUV_N1_", "WALL_NE1", "WALLF_NE1", "WLOUV_NE1")):
                _hide(ob)                                                  # opens into the north strip (EX06)
            if pk in ("wall", "wall_fill", "louvre") and abs(abs(x) - 132) < 0.2 and abs(y) < 132:
                _hide(ob)                                                  # arm clerestory is interior once tier 2 runs on (EX07)
        for ob in bpy.data.objects:                                        # one park plane only: the transept's (EX16)
            if ob.name.startswith("EGROUND_PARK"): _hide(ob)
    return out
