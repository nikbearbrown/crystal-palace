"""CP032 arrival near-foreground ground (2026-11-02, Grok; CANDIDATE, no verdict; DEPARTURES MV17).

blender -b rounds/m02.blend -P scripts/candidate_cp032_foreground.py -- [--out rounds/candidates/m02_cp032fg.blend]
blender -b ROUND.blend -P scripts/candidate_cp032_foreground.py -- --live     # apply in place (only after a KEEP call)
Idempotent; always prints `CP032_FG_IN_PLACE True|False`.

Diagnosis (ray probe 2026-11-02): the white slab across the lower third of CP032_arrival_start/end is NOT the clay.
look v1 (`_ensure_horizon_ground`) adds a 2 km CPL_HorizonGround disk at render time at min(local ground tops) - 0.02
m. m02 holds several regions; the flat K_GROUND / DEP_GRASS tops are z = 0, so the disk sits at z = -0.02 m. The
Sydenham arrival yard slopes ~1 in 14 down to the west, and the clay under the camera is at z -0.3 to -0.5 m, so the
disk cuts through it. The disk is untextured (its tint is sampled from a noise material's unlinked 0.8 grey default)
and has visible_shadow off, so it renders as a flat, shadowless near-white plane.

Fix (candidate blend only):
 1. grok_states: hide CPL_HorizonGround for cameras starting `CP032_arrival` (render_shots.py per-shot hook). The
    arrival ground ARR_GRASS (-500..1400 ft E, rising east) already fills the horizon there; other m02 cameras keep
    the disk. The shared look library is not edited.
 2. ARR_CLAY (only; the spoil heaps keep GT_SydenhamClay) gets GT_SydenhamClayYard: the trodden, cart-worked
    receiving yard on London Clay, darker and finer-grained than the 0.3/m pink-tan noise (grey-brown base, wetter
    darker patches, finer bump). Colours are by-eye interpretive (grade D), matched in value to the departure
    yard's GT_TroddenGround. No geometry, dimensions, figures, cameras or exposure change.
Live rounds/m02.blend is never written without --live.
"""
import os, sys, json, argparse
import bpy

argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
ap = argparse.ArgumentParser(); ap.add_argument("--out", default="rounds/candidates/m02_cp032fg.blend")
ap.add_argument("--live", action="store_true")
a = ap.parse_args(argv)
here = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if a.live:
    out = os.path.abspath(bpy.data.filepath)
else:
    out = os.path.join(here, a.out) if not os.path.isabs(a.out) else a.out
    assert os.path.abspath(out) != os.path.abspath(bpy.data.filepath), "refusing to overwrite the opened blend without --live"

STATE_KEY = "CP032_arrival"; HIDE = ["CPL_HorizonGround"]; MATN = "GT_SydenhamClayYard"
C_DRY0, C_DRY1 = (0.135, 0.105, 0.070), (0.235, 0.185, 0.120)   # trodden grey-brown clay, by eye (D)
C_WET = (0.070, 0.056, 0.040)                                    # puddled / cart-worked patches


def yard_mat():
    m = bpy.data.materials.get(MATN)
    if m: return m
    m = bpy.data.materials.new(MATN); m.use_nodes = True; nt = m.node_tree; n = nt.nodes; l = nt.links
    b = n["Principled BSDF"]; tc = n.new("ShaderNodeTexCoord")
    fine = n.new("ShaderNodeTexNoise"); fine.inputs["Scale"].default_value = 1.6; fine.inputs["Detail"].default_value = 8.0
    fine.inputs["Roughness"].default_value = 0.6
    l.new(tc.outputs["Object"], fine.inputs["Vector"])
    r1 = n.new("ShaderNodeValToRGB"); r1.color_ramp.elements[0].position = 0.35; r1.color_ramp.elements[1].position = 0.65
    r1.color_ramp.elements[0].color = (*C_DRY0, 1); r1.color_ramp.elements[1].color = (*C_DRY1, 1)
    l.new(fine.outputs["Fac"], r1.inputs[0])
    big = n.new("ShaderNodeTexNoise"); big.inputs["Scale"].default_value = 0.45; big.inputs["Detail"].default_value = 3.0
    l.new(tc.outputs["Object"], big.inputs["Vector"])
    r2 = n.new("ShaderNodeValToRGB"); r2.color_ramp.elements[0].position = 0.38; r2.color_ramp.elements[1].position = 0.50
    l.new(big.outputs["Fac"], r2.inputs[0])            # 0 -> wet patch, 1 -> dry
    mix = n.new("ShaderNodeMix"); mix.data_type = "RGBA"
    mix.inputs[6].default_value = (*C_WET, 1)
    l.new(r2.outputs["Color"], mix.inputs[0]); l.new(r1.outputs["Color"], mix.inputs[7])
    l.new(mix.outputs[2], b.inputs["Base Color"])
    rr = n.new("ShaderNodeMapRange"); rr.inputs["To Min"].default_value = 0.72; rr.inputs["To Max"].default_value = 0.95
    l.new(r2.outputs["Color"], rr.inputs["Value"]); l.new(rr.outputs["Result"], b.inputs["Roughness"])
    bn = n.new("ShaderNodeTexNoise"); bn.inputs["Scale"].default_value = 14.0; bn.inputs["Detail"].default_value = 6.0
    l.new(tc.outputs["Object"], bn.inputs["Vector"])
    bp = n.new("ShaderNodeBump"); bp.inputs["Strength"].default_value = 0.35; bp.inputs["Distance"].default_value = 0.02
    l.new(bn.outputs["Fac"], bp.inputs["Height"]); l.new(bp.outputs["Normal"], b.inputs["Normal"])
    if "Specular IOR Level" in b.inputs: b.inputs["Specular IOR Level"].default_value = 0.3
    b.inputs["Base Color"].default_value = (*[(x + y) / 2 for x, y in zip(C_DRY0, C_DRY1)], 1)
    m.diffuse_color = b.inputs["Base Color"].default_value
    return m


def states():
    t = bpy.data.texts.get("grok_states")
    return json.loads(t.as_string()) if t else {}


def in_place():
    s = states(); cl = bpy.data.objects.get("ARR_CLAY")
    return (s.get(STATE_KEY, {}).get("hide") == HIDE and cl is not None
            and len(cl.data.materials) == 1 and cl.data.materials[0] is not None and cl.data.materials[0].name == MATN)


already = in_place()
info = {}
if already:
    print("CP032_FG already applied; nothing changed")
else:
    s = states(); s.setdefault(STATE_KEY, {})["hide"] = HIDE
    t = bpy.data.texts.get("grok_states") or bpy.data.texts.new("grok_states"); t.clear(); t.write(json.dumps(s))
    cl = bpy.data.objects["ARR_CLAY"]; old = [m.name for m in cl.data.materials]
    assert len(cl.data.materials) == 1, old
    cl.data.materials[0] = yard_mat()
    info = {"grok_states": s, "ARR_CLAY_material": [old, MATN],
            "spoil_material": [m.name for m in bpy.data.objects["ARR_SPOIL"].data.materials]}
print("CP032_FG_INFO " + json.dumps(info))
print("CP032_FG_IN_PLACE", in_place())
if not already or not a.live:
    os.makedirs(os.path.dirname(out), exist_ok=True)
    bpy.ops.wm.save_as_mainfile(filepath=out, copy=True, compress=True)
    print("CP032_FG saved", out)
