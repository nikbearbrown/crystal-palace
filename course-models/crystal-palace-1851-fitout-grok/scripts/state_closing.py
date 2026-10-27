# HP51 closing (CP029): 15 October 1851, the exhibitors' closing ceremony under the transept. Exec'd after dressing.py
# (which dresses the building as hp51 for this state). DEPARTURES FT30-FT36.
exec(open(os.path.join(HERE, "state_common.py")).read())
info = {}; info["doors_open"] = open_south_doors()
DAIS = (-22.0, 22.0, 30.0, 58.0)    # FT31: inferred -- north of the crossing, where the opening throne stood
removed = []
for ob in list(bpy.data.objects):
    if ob.get("dress_kind") and ob.type in ('MESH', 'EMPTY'):
        x, y = ob.location.x / FT, ob.location.y / FT
        if DAIS[0] - 3 < x < DAIS[1] + 3 and DAIS[2] - 3 < y < DAIS[3] + 3: removed.append(ob.name); bpy.data.objects.remove(ob, do_unlink=True)
info["dressing_cleared_for_dais"] = len(removed)
CRIMSON = M_("crimson_cloth", (0.38, 0.03, 0.04), 0.85); GOLD = M_("gold_fringe", (0.72, 0.52, 0.18), 0.35, 1.0)
k = Kit([CRIMSON, TIMBER_DK, GOLD])
k.box(0, DAIS[0], DAIS[1], DAIS[2], DAIS[3], 0, 3.0)
for s in range(5):   # steps down to the south
    k.box(0, -10, 10, DAIS[2] - 1.0 * (s + 1), DAIS[2] - 1.0 * s, 0, 3.0 - 0.6 * (s + 1) + 0.6)
k.box(2, DAIS[0], DAIS[1], DAIS[2] - 0.05, DAIS[2], 2.6, 3.0)
k.box(0, -4, 4, DAIS[3] - 6, DAIS[3] - 2, 3.0, 4.2)                      # upper step for the chair of state
CH = Kit([CRIMSON, GOLD]); CH.box(0, -1.6, 1.6, -1.4, 1.4, 0, 1.8); CH.box(0, -1.6, 1.6, 1.1, 1.4, 1.8, 5.8); CH.box(1, -1.7, 1.7, 1.0, 1.5, 5.8, 6.2)
prop("DAIS", k.done("dais"), 0, 0, 0, 0, part_kind="dais", inferred=True)
prop("CHAIR_OF_STATE", CH.done("chair_state"), 0, DAIS[3] - 4, 4.2, 0, part_kind="chair")
# canopy and hangings behind the dais
CAN = Kit([CRIMSON, GOLD, TIMBER_DK])
for sx in (-14, 14): CAN.cyl(2, (sx, DAIS[3] - 1, 3), (sx, DAIS[3] - 1, 24), 0.35, 10)
CAN.box(0, -15, 15, DAIS[3] - 3, DAIS[3] + 0.5, 24, 26.5); CAN.box(1, -15, 15, DAIS[3] - 3.1, DAIS[3] - 2.9, 23.3, 24)
CAN.box(0, -13.5, 13.5, DAIS[3] - 0.6, DAIS[3] - 0.3, 6, 24)
prop("DAIS_CANOPY", CAN.done("dais_canopy"), 0, 0, 0, 0, part_kind="canopy", inferred=True)
BLACK = M_("coat_black3", (0.03, 0.03, 0.035)); HAT = M_("hat_black3", (0.02, 0.02, 0.02))
dig = [pmesh("man", [BLACK, M_("trou_blk3", (0.05, 0.05, 0.05)), SKIN2[j % 2], HAT, WK["shirt"]], {"hat": ("top", "low")[j % 2], "frock": True, "cravat": True}, f"dignitary_{j}") for j in range(2)]
court = pmesh("man", [M_("court_blue", (0.05, 0.07, 0.20)), M_("court_white", (0.80, 0.78, 0.72)), SKIN2[0], HAT, GOLD], {"hat": "low", "frock": True, "belt": True}, "court")
nd = 0
for j in range(26):
    x = -19 + (j % 13) * 3.2 + SRND.uniform(-0.5, 0.5); y = DAIS[2] + 4 + (j // 13) * 5 + SRND.uniform(-0.6, 0.6)
    if abs(x) < 5 and y > DAIS[3] - 7: continue
    person(f"DAIS_{j:02d}", court if j % 7 == 3 else dig[j % 2], x, y, 3.0, heading_rz(0, -1) + SRND.uniform(-0.3, 0.3), trade="commissioner"); nd += 1
person("DAIS_ALBERT_standin", court, 0, DAIS[3] - 9, 4.2 - 1.2, heading_rz(0, -1), trade="royal_standin", note="unnamed stand-in, not a likeness")
info["dais_figures"] = nd + 1
# FT32: the ceremony crowd: dense under the transept facing the dais, and full galleries (dressing.spawn + its keep-outs)
face_dais = lambda x, y: heading_rz(-x, 46 - y)
OCC.append((0, 44, 26.0, "dais"))
extra = spawn([((-33, 33, -150, -26), 3.0), ((-26, 26, -26, 26), 1.5), ((-33, -24, 26, 70), 1.0), ((24, 33, 26, 70), 1.0)], 620, 0.0, "CL",
              lambda x, y: math.hypot(x, y) > 16.5, seg_r=8.0, cone_d=30.0, cone_a=18.0, face=face_dais)
GT = GALLERY_TOP
extra_g = spawn([((37.3, 40.0, 40, 178), 1), ((-40.0, -37.3, 40, 178), 1), ((37.3, 40.0, -152, -40), 1), ((-40.0, -37.3, -152, -40), 1),
                 ((40.5, 44.0, -152, 178), 1.4), ((-44.0, -40.5, -152, 178), 1.4), ((-34, 34, -162, -157), 0.6)], 260, GT, "CLG", None,
                seg_r=6, cone_d=14, cone_a=12, face=face_dais)
# FT40 (c02): drop spectators standing within 18 ft in front of a closing camera (CP029_gallery had one filling the left foreground)
_cl_cams = [((-39.5, -44.0), (0.0, 48.0))]   # gallery cam only; the dais shot keeps its floor foreground
_drop = 0
for _o in list(bpy.data.objects):
    if not _o.name.startswith("CROWD_") or not _o.get("person"): continue
    _x, _y = _o.location.x / FT, _o.location.y / FT
    for (_cx, _cy), (_lx, _ly) in _cl_cams:
        _dx, _dy = _x - _cx, _y - _cy; _vx, _vy = _lx - _cx, _ly - _cy
        if math.hypot(_dx, _dy) < 18 and (_dx * _vx + _dy * _vy) > 0 and abs(_o.location.z / FT - (22.92 if _cx < -30 else 0)) < 1:
            bpy.data.objects.remove(_o); _drop += 1; break
info["cam_foreground_dropped"] = _drop
info["ceremony_crowd"] = [extra, extra_g]
# FT34: October -- the elms' leaves turning (interpretive), a lower afternoon sun
LEAF = bpy.data.materials.get("GT_ElmLeaf")
try:
    for nd_ in LEAF.node_tree.nodes:
        if nd_.type == 'VALTORGB':
            for el in nd_.color_ramp.elements: c = el.color; el.color = (c[0] * 0.6 + 0.30, c[1] * 0.75 + 0.06, c[2] * 0.3, 1)
    LEAF.diffuse_color = (0.36, 0.27, 0.07, 1); info["leaf"] = "autumn tint"
except Exception as ex: info["leaf"] = f"unchanged ({ex})"
so_ = bpy.data.objects.get("GT_Sun")
if so_: so_.rotation_euler.x = min(so_.rotation_euler.x + math.radians(18), math.radians(72)); so_.data.color = (1.0, 0.90, 0.78)
STATE_INFO = info
print("CLOSING", info, flush=True)
