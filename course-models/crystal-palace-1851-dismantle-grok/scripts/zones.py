"""HP-DISMANTLE work zone (DM03): one place for the coordinates the build and the render-time changes share.
apply(state) runs at render time on the combined scene (x05 exterior + this transept/dismantle blend + Claude's
west frame, all appended read-only and never saved): roof glass off in zone G, bays stripped in zone R, the girder
being lowered removed from its home position. Feet, Claude's frame (origin at the crossing, X east)."""
import bpy
FT = 0.3048
ZONE = {
    "lift_girder_name": "EGIR_T1_X_+168_-156", "lift_girder_xy": (168.0, -156.0), "lift_bottom_ft": 7.0, "lift_cant_deg": 15.0,
    "leg_feet": [(158.0, -147.0), (178.0, -147.0)], "apex_ft": (168.0, -155.0, 38.0),
    "winch_xy": (180.0, -127.0), "guy_anchors": [(168.0, -123.0), (168.0, -196.0)],
    "tag_men": [(152.0, -148.0), (184.0, -164.0)],
    "shored_girder": (180.0, 204.0, -156.0), "shored_girder_name": "EGIR_T1_X_+192_-156",
    "joint_xy": (180.0, -156.0), "deck_ft": 13.5, "deck_rect": (186.0, 195.0, -152.0, -145.0),
    "stack_rect": (210.0, 240.0, -150.0, -136.0), "trolley": (222.0, -168.0, 0.0),
    "pane_lower": (216.0, -148.3, 22.3),
    # roof zones: R = stripped (units gone), G = glass off, bars and gutters left (Muse furrow bay without panes)
    "R": [(156.0, 180.0, -204.0, -132.0)],
    "G": [(108.0, 324.0, -204.0, -132.0), (156.0, 252.0, -132.0, -60.0), (-36.0, 36.0, -204.0, -84.0)],
    "vault_open_y": -84.0,
}
def _in(x, y, rects): return any(x0 <= x <= x1 and y0 <= y <= y1 for x0, x1, y0, y1 in rects)
def bare_furrow():
    fm = bpy.data.meshes.get("FURROW_BAY_by_Muse")
    if fm is None: return None
    me = bpy.data.meshes.get("FURROW_BAY_by_Muse_bare")
    if me: return me
    me = fm.copy(); me.name = "FURROW_BAY_by_Muse_bare"
    import bmesh
    gi = [i for i, m in enumerate(me.materials) if m and m.name.startswith("GT_FurrowGlass")]
    bm = bmesh.new(); bm.from_mesh(me)
    bmesh.ops.delete(bm, geom=[f for f in bm.faces if f.material_index in gi], context='FACES')
    bm.to_mesh(me); bm.free(); me["credit"] = "Muse furrow bay, panes removed at render time (Grok DM04)"
    return me
def removed_glass():
    m = bpy.data.materials.get("GT_GlassRemoved")
    if m: return m
    m = bpy.data.materials.new("GT_GlassRemoved"); m.use_nodes = True; n = m.node_tree.nodes
    for x in list(n): n.remove(x)
    o = n.new("ShaderNodeOutputMaterial"); t = n.new("ShaderNodeBsdfTransparent"); m.node_tree.links.new(t.outputs[0], o.inputs[0])
    return m
def _hide(o): o.hide_render = True; o.hide_viewport = True
def apply(state):
    out = {"state": state, "R": 0, "G": 0, "G_glass_slots": 0, "vault": 0, "girder": 0}
    if state != "dismantle": return out
    bare = bare_furrow()
    for o in bpy.data.objects:
        if o.type != 'MESH': continue
        pk = o.get("part_kind"); x, y = o.location.x / FT, o.location.y / FT
        is_roof = pk == "roof" or o.get("furrow_proxy") or (o.data and o.data.name.startswith(("roof", "FURROW")))
        if is_roof and _in(x, y, ZONE["R"]): _hide(o); out["R"] += 1; continue
        if is_roof and _in(x, y, ZONE["G"]):
            if bare is not None and o.data.name == "FURROW_BAY_by_Muse": o.data = bare; out["G"] += 1
            else:
                for sl in o.material_slots:
                    if sl.material and "Glass" in sl.material.name: sl.link = 'OBJECT'; sl.material = removed_glass(); out["G_glass_slots"] += 1
                out["G"] += 1
            continue
        if pk == "vault_glass" and y < ZONE["vault_open_y"]: _hide(o); out["vault"] += 1
        if o.name.split(".")[0] == ZONE["lift_girder_name"]: _hide(o); out["girder"] += 1
    print("ZONES", out, flush=True)
    return out

def fix_floor_seam():
    """DM15: the transept's FLOOR_BOARDS and the exterior's EFLOOR_BOARDS are coplanar where they overlap (x ~133-143),
    and Cycles shades coplanar overlaps black (each sheet shadows the other). At render time only, drop the transept
    floor 0.03 ft (9 mm) so the exterior boards lie on top. Nothing saved."""
    n = 0
    for o in bpy.data.objects:
        if o.type == 'MESH' and o.name.split(".")[0] == "FLOOR_BOARDS" and not o.get("floor_seam_fixed"):
            o.location.z -= 0.03 * FT; o["floor_seam_fixed"] = True; n += 1
    print("FLOOR_SEAM", n, flush=True); return n
import math
def dusk():
    """DM16: CP031 dusk variant, render time only: sun 5 deg above the WSW horizon, warm, sky to match."""
    sun = bpy.data.objects.get("GT_Sun"); elev, rot = 5.0, 22.0
    if sun:
        sun.rotation_euler = (math.radians(90 - elev), 0, math.radians(rot - 180 + 90))
        sun.data.energy = 2.4; sun.data.color = (1.0, 0.58, 0.32); sun.data.angle = math.radians(1.0)
    w = bpy.context.scene.world
    for nd in w.node_tree.nodes:
        if nd.type == 'TEX_SKY':
            try: nd.sun_elevation = math.radians(elev); nd.sun_rotation = math.radians(rot)
            except AttributeError: pass
        if nd.type == 'BACKGROUND': nd.inputs[1].default_value = 0.3
