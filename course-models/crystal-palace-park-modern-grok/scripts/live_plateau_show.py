"""Live-recipe helper (CP070 / CP067 heroes): dud-fix v4 rendered CP067 and CP070 BEFORE it hid the pk_grass_plateau
clipper for CP075/CP076 and then saved parknow-r02.blend with the clipper hidden. Re-showing it reproduces the live
CP070 and CP067 heroes at max pixel diff 0 (checked 2026-11-13: renders/r02/r02_CAM_CP070_begin_walk_35mm.png,
renders/r02/r02_CAM_CP067_dino_conservation_35mm.png, 1280x720 32 spp via render_cp076_look.py). CP075/CP076 renders
keep the clipper hidden (saved state; also max diff 0). Use: blender -b X.blend -P scripts/live_plateau_show.py -P ..."""
import bpy
o = bpy.data.objects.get("pk_grass_plateau")
print("LIVE_PLATEAU_SHOW", o is not None, "was_hidden", o.hide_render if o else None, flush=True)
if o: o.hide_render = False; o.hide_viewport = False
