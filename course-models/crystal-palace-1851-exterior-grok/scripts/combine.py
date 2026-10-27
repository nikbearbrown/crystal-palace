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
def claude_roof_glass(base):
    """EX26: Claude's roof mesh has no (usable) UVs, so the UV-driven sash-bar mask of GT_RoofGlassExt reads 0 everywhere
    and the whole sheet renders as bar paint (the white x04 seam). This copy drives the same bar lines from object
    coordinates in feet instead."""
    m = bpy.data.materials.get("GT_RoofGlassExt_CL")
    if m: return m
    m = base.copy(); m.name = "GT_RoofGlassExt_CL"; nt = m.node_tree
    for tc in [x for x in nt.nodes if x.type == 'TEX_COORD']:
        for dst in [lk.to_socket for lk in tc.outputs["UV"].links]:
            sc = nt.nodes.new("ShaderNodeVectorMath"); sc.operation = 'SCALE'; sc.inputs["Scale"].default_value = 1 / FT
            nt.links.new(tc.outputs["Object"], sc.inputs[0]); nt.links.new(sc.outputs[0], dst)   # replaces the UV link
    return m
def override_claude_roofs():
    """EX24/EX26: Claude's appended roof units (PART_RoofUnit 'roof' mesh, MAT_Glass) get Grok's exterior roof glass."""
    base = bpy.data.materials.get("GT_RoofGlassExt"); n = 0
    if not base: print("NO GT_RoofGlassExt"); return 0
    rg = claude_roof_glass(base)
    for c in bpy.data.collections:
        if c.name.startswith("PART_RoofUnit") and c.library is None:
            for ob in c.all_objects:
                for sl in ob.material_slots:
                    if sl.material and sl.material.name.startswith("MAT_Glass"): sl.material = rg; n += 1
    print("CLAUDE_ROOF_OVERRIDE slots", n, flush=True); return n
def _hide(ob):
    ob.hide_render = True; ob.hide_viewport = True
def combine(claude=None, transept=None, roof_override=True, furrow=False):
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
            if claude and ob.get("show_with_claude"):
                ob.hide_render = False; ob.hide_viewport = False                # transept r09: Muse's Una at catalogue cell S29
            if ob.name.startswith(("WALL_N1_", "WALLF_N1_", "WLOUV_N1_", "WALL_NE1", "WALLF_NE1", "WLOUV_NE1")):
                _hide(ob)                                                  # opens into the north strip (EX06)
            if pk in ("wall", "wall_fill", "louvre") and abs(abs(x) - 132) < 0.2 and abs(y) < 132:
                _hide(ob)                                                  # arm clerestory is interior once tier 2 runs on (EX07)
        for ob in bpy.data.objects:                                        # one park plane only: the transept's (EX16)
            if ob.name.startswith("EGROUND_PARK"): _hide(ob)
    if furrow:   # EX27: render-time only -- flat roof units (Claude's + ours) become Muse's furrow bay
        import os, sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        import furrow as F; out["furrow"] = F.swap_flat_roofs()
    return out
