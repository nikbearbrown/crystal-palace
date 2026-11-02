"""2026-11-02 CANDIDATE (Grok Bot executor, not a verdict): CP016_wheels reframe.
Live c06 CP016_wheels_start sits 4.1 ft directly behind a roof-edge scaffold standard (KSCAF_ROOFEDGE pole x 328, y -208),
which fills frame centre and hides the SW wagon wheel the shot exists for.
Change (cameras only, no geometry): eye stays on the roof-edge deck (deck 24 ft, eye 29.25 ft, y -212, CN15/CN42),
moved into the bay between standards (x 328 / 336), lens stays 50 mm (85 mm tried: wheel still unreadable, and the
near glaziers are left as lathe proxies by the people_lib 3.4 close-up gate).   start: pos (332.0,-212,29.25)   look (328.6,-196.1,22.8)  (wagon_0 + SW wheel centred)
  end:   pos (332.0,-210.5,29.25) look (328.4,-196.1,22.6)  (1.5 ft push-in across the deck, still on it: deck y -216..-208)
  (an aim held left of the gutter glazier, look x 326, was tried: the wagon is squeezed into the top-right corner)
The three wagon_0 glaziers (KWORKER_013/014/027_CP016) fill >8% of this frame, so people_lib 3.4 leaves them as grey
lathe proxies; this blend hides them and the two panes they hold (KPANE_SLIDING_0, KPANE_HELD_0; hide_render) - CP016_wheels-only blend, never render other shots from it.
The men stay in CP016_trolley (DEPARTURES CN43).
Plus (material only, no geometry): the four 1 ft wagon wheels get the existing GT_CartTyre iron material instead of
GT_WagonTimber, so the wheels separate from the timber bearer (DEPARTURES CN43, inferred: iron gutter wheels).
Saves rounds/candidates/c06_cp016wheels.blend (live rounds/c06.blend untouched).
blender -b rounds/c06.blend -P scripts/cand_cp016_wheels_20261102.py"""
import bpy, mathutils, os
F = 0.3048
def aim(name, pos, look, lens):
    ob = bpy.data.objects[name]
    ob.location = mathutils.Vector(pos) * F
    d = mathutils.Vector(look) * F - ob.location
    ob.rotation_mode = 'XYZ'; ob.rotation_euler = d.to_track_quat('-Z', 'Y').to_euler()
    ob.data.lens = lens
    ob["cand_20261102"] = "CP016 wheels reframe off scaffold standard, 85 mm"
aim("CP016_wheels_start", (332.0, -212.0, 29.25), (328.6, -196.1, 22.8), 50.0)
aim("CP016_wheels_end", (332.0, -210.5, 29.25), (328.4, -196.1, 22.6), 50.0)
for n in ("KWORKER_013_CP016", "KWORKER_014_CP016", "KWORKER_027_CP016", "KPANE_SLIDING_0", "KPANE_HELD_0"):   # panes go with the hidden men
    bpy.data.objects[n].hide_render = True; bpy.data.objects[n]["cand_20261102"] = "hidden for CP016_wheels only"
me = bpy.data.meshes["glazing_wagon"]; tyre = bpy.data.materials["GT_CartTyre"]
if tyre.name not in [m.name for m in me.materials if m]: me.materials.append(tyre)
ti = [m.name for m in me.materials].index(tyre.name); n = 0
for poly in me.polygons:                      # wheel faces: all verts within 0.51 ft of a wheel centre (x +-1.9, y +-4.0, z 2 in)
    vs = [me.vertices[i].co / F for i in poly.vertices]
    for sx in (-1.9, 1.9):
        for sy in (-4.0, 4.0):
            if all(((v.x - sx) ** 2 + (v.z - 2 / 12) ** 2) ** 0.5 <= 0.51 and abs(v.y - sy) <= 0.11 for v in vs):
                poly.material_index = ti; n += 1
print("WHEEL_FACES", n)
here = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
out = os.path.join(here, "rounds", "candidates", "c06_cp016wheels.blend")
bpy.ops.wm.save_as_mainfile(filepath=out, copy=True, compress=True)
print("SAVED", out)
