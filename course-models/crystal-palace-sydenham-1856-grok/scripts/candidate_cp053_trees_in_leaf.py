"""CP053 CANDIDATE (2026-11-19, no verdict): the Festival of Empire grounds, summer 1911 - the lower-park trees in leaf.

usage: blender -b rounds/sydenham-late11-r14.blend -P scripts/candidate_cp053_trees_in_leaf.py [-- out.blend]
       (env CP053_NOSAVE=1: build in memory only)
Base = rounds/sydenham-late11-r14.blend (md5 9f90df23, unchanged since 1c96ad7) - the blend the live hero
  renders/r14_late11_CAM_CP053_empire_pavilions_wide_35mm.png (md5 9236eda7; COVERAGE.md CP053 hero) was rendered from:
  survey look v1.1 /workspace/crystal-palace-survey/look/apply_render.py --scene-id CP053 --era 1852 --tod exterior_afternoon
  --spp 24 --res 1280x720 --no-people (look/sydenham_logs/CP053.log, verdict 'improved', 1b3c92d); re-rendered 2026-11-19 max diff 0.
  -> rounds/candidates/sydenham-late11-r14_cp053trees.blend
Live hero shows: a summer festival lawn with the palace on the skyline, but every tree in the frame is an r03 PLACEHOLDER
  (nine smooth pastel-green icospheres on a thin 8-sided stick): round green lollipops - the most toy-like thing in the frame,
  and the reason the park reads as a model rather than a 55-year-old landscape park in full summer leaf.
Adds ONE dated collection SY11_lower_park_trees_in_leaf__summer1911 (cp_state SY11-LATE_FestivalOfEmpire_summer1911) for
  every PLACEHOLDER_park_tree_*_crown whose crown lies in or near the CAM_CP053_empire_pavilions_wide_35mm frustum (the
  other park placeholders are left as they are - logged as a departure):
  * cp053_leaf_canopy: broadleaf foliage - one point per twig spray on and outside the visible surface of each placeholder
    crown (points inside another sphere of the same crown skipped); a geometry-nodes modifier (cp053_leaf_sprays) instances
    a spray of 8 leaf blades (6-gon ellipses 0.14-0.30 m long, lime / plane / sycamore / horse-chestnut leaflet class) on
    every point with a random rotation, so the foliage is dense without a huge mesh in the blend; per tree a few 'bites' (gaps) and 'lobes' (clusters pushed further out) break the round silhouette.
    Material cp053_summer_foliage: dark -> light summer green per spray (point attribute 'cvar' + per-instance random),
    thin-leaf translucency.
  * cp053_limbs: primary limbs + forks from the r03 trunk top out into each crown, the round's own 'bark' material (unedited).
Sources: storyboard CP053 (1911, SY11; the company's bankruptcy year - the Festival of Empire summer); Festival of Empire 1911
  (May-Oct 1911 in the palace grounds; Wikipedia / Piggott 'Reflections of empire') R for a summer festival in the park;
  1857 park plan 0591 / r03 placeholder positions (R position, I form). Species, leaf size, crown form: I.
Cameras NOT moved, world/sun/exposure/look NOT changed. Nothing deleted or hidden; every existing object/material untouched.
"""
import bpy, bmesh, math, os, sys, random
import numpy as np
from mathutils import Vector, Matrix
from bpy_extras.object_utils import world_to_camera_view

argv = sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else []
OUT = '--nosave' if os.environ.get('CP053_NOSAVE') else (argv[0] if argv and argv[0].endswith('.blend') else 'rounds/candidates/sydenham-late11-r14_cp053trees.blend')
STATE = 'SY11-LATE_FestivalOfEmpire_summer1911'
CNAME = 'SY11_lower_park_trees_in_leaf__summer1911'
HERO = 'CAM_CP053_empire_pavilions_wide_35mm'
assert bpy.data.collections.get(CNAME) is None, 'base already dressed'
RNG = random.Random(1911)
NPR = np.random.default_rng(1911)
sc = bpy.context.scene
n_before = len(bpy.data.objects); nmat_before = len(bpy.data.materials)
hidden_before = sorted(o.name for o in bpy.data.objects if o.hide_render)
col = bpy.data.collections.new(CNAME); sc.collection.children.link(col); col['cp_state'] = STATE
INFO = {}

# ------------------------------------------------------------------ parameters (m)
LEAF_L = (0.14, 0.30)        # leaf blade length (lime / plane / sycamore / horse-chestnut leaflet class, I)
LEAF_W = 0.45                # width / length
CLUSTER_PER_M2 = float(os.environ.get('CP053_DENSITY', 34.0))   # twig sprays per m2 of exposed crown surface
LEAVES_PER_CLUSTER = 8       # leaves per twig spray
CLUSTER_R = 0.40             # leaves within +-this of the spray centre
OUT_OFF = (0.00, 1.10)       # spray offset outside the placeholder sphere surface
LOBE_OFF = 2.2               # max extra offset inside a 'lobe'
BITES = (4, 7); LOBES = (3, 5)
MIN_LEAF_Z = 3.0             # lowest spray centre above the trunk foot (head-room under the crown, I)
FRUSTUM_MARGIN = 0.12        # crowns with any bbox corner / centre within this margin of the hero frame are dressed

def tag(m): m['cp_state'] = STATE; return m
def foliage_mat():
    m = tag(bpy.data.materials.new('cp053_summer_foliage')); nt = m.node_tree; n = nt.nodes; l = nt.links
    for x in list(n): n.remove(x)
    out = n.new('ShaderNodeOutputMaterial'); pb = n.new('ShaderNodeBsdfPrincipled'); tl = n.new('ShaderNodeBsdfTranslucent')
    mix = n.new('ShaderNodeMixShader'); at = n.new('ShaderNodeAttribute'); at.attribute_name = 'cvar'; at.attribute_type = 'INSTANCER'
    oi = n.new('ShaderNodeObjectInfo'); mx = n.new('ShaderNodeMath'); mx.operation = 'MULTIPLY_ADD'
    mx.inputs[1].default_value = 0.35; l.new(oi.outputs['Random'], mx.inputs[0]); l.new(at.outputs['Fac'], mx.inputs[2])
    ramp = n.new('ShaderNodeValToRGB'); el = ramp.color_ramp.elements
    el[0].position = 0.0; el[0].color = (0.030, 0.062, 0.020, 1)          # shade-leaf dark green
    el[1].position = 0.55; el[1].color = (0.062, 0.135, 0.038, 1)         # mid summer green (~ r03 foliage 0.07/0.16/0.05)
    e2 = el.new(0.9); e2.color = (0.110, 0.185, 0.045, 1)                 # sunlit yellow-green
    e3 = el.new(1.0); e3.color = (0.125, 0.170, 0.060, 1)                 # odd paler leaf
    l.new(mx.outputs[0], ramp.inputs[0])
    l.new(ramp.outputs['Color'], pb.inputs['Base Color']); pb.inputs['Roughness'].default_value = 0.58
    l.new(ramp.outputs['Color'], tl.inputs['Color'])
    mix.inputs[0].default_value = 0.30
    l.new(pb.outputs[0], mix.inputs[1]); l.new(tl.outputs[0], mix.inputs[2]); l.new(mix.outputs[0], out.inputs['Surface'])
    return m
M_LEAF = foliage_mat()
M_BARK = bpy.data.materials['bark']           # the round's own bark material, reused unedited

def spray_nodes():
    ng = bpy.data.node_groups.new('cp053_leaf_sprays', 'GeometryNodeTree'); ng['cp_state'] = STATE
    ng.interface.new_socket('Geometry', in_out='INPUT', socket_type='NodeSocketGeometry')
    ng.interface.new_socket('Geometry', in_out='OUTPUT', socket_type='NodeSocketGeometry')
    N = ng.nodes; L = ng.links
    gi = N.new('NodeGroupInput'); go = N.new('NodeGroupOutput')
    circ = N.new('GeometryNodeMeshCircle'); circ.fill_type = 'NGON'; circ.inputs['Vertices'].default_value = 6; circ.inputs['Radius'].default_value = 0.5
    shp = N.new('GeometryNodeTransform'); shp.inputs['Scale'].default_value = (1.0, LEAF_W, 1.0)
    L.new(circ.outputs['Mesh'], shp.inputs['Geometry'])
    pts = N.new('GeometryNodePoints'); pts.inputs['Count'].default_value = LEAVES_PER_CLUSTER
    rp = N.new('FunctionNodeRandomValue'); rp.data_type = 'FLOAT_VECTOR'; rp.inputs['Min'].default_value = (-CLUSTER_R,) * 3; rp.inputs['Max'].default_value = (CLUSTER_R,) * 3
    rp.inputs['Seed'].default_value = 11
    L.new(rp.outputs['Value'], pts.inputs['Position'])
    rr = N.new('FunctionNodeRandomValue'); rr.data_type = 'FLOAT_VECTOR'; rr.inputs['Min'].default_value = (0, 0, 0); rr.inputs['Max'].default_value = (6.2832,) * 3; rr.inputs['Seed'].default_value = 12
    e2r = N.new('FunctionNodeEulerToRotation'); L.new(rr.outputs['Value'], e2r.inputs['Euler'])
    rs = N.new('FunctionNodeRandomValue'); rs.data_type = 'FLOAT'; rs.inputs['Min'].default_value = LEAF_L[0]; rs.inputs['Max'].default_value = LEAF_L[1]; rs.inputs['Seed'].default_value = 13
    iop = N.new('GeometryNodeInstanceOnPoints')
    L.new(pts.outputs['Points'], iop.inputs['Points']); L.new(shp.outputs['Geometry'], iop.inputs['Instance'])
    L.new(e2r.outputs['Rotation'], iop.inputs['Rotation']); L.new(rs.outputs[1], iop.inputs['Scale'])
    real = N.new('GeometryNodeRealizeInstances'); L.new(iop.outputs['Instances'], real.inputs['Geometry'])
    smat = N.new('GeometryNodeSetMaterial'); smat.inputs['Material'].default_value = M_LEAF; L.new(real.outputs['Geometry'], smat.inputs['Geometry'])
    # one spray per input point
    cr = N.new('FunctionNodeRandomValue'); cr.data_type = 'FLOAT_VECTOR'; cr.inputs['Min'].default_value = (0, 0, 0); cr.inputs['Max'].default_value = (6.2832,) * 3; cr.inputs['Seed'].default_value = 21
    ce = N.new('FunctionNodeEulerToRotation'); L.new(cr.outputs['Value'], ce.inputs['Euler'])
    cs = N.new('FunctionNodeRandomValue'); cs.data_type = 'FLOAT'; cs.inputs['Min'].default_value = 0.85; cs.inputs['Max'].default_value = 1.15; cs.inputs['Seed'].default_value = 22
    iop2 = N.new('GeometryNodeInstanceOnPoints')
    L.new(gi.outputs[0], iop2.inputs['Points']); L.new(smat.outputs['Geometry'], iop2.inputs['Instance'])
    L.new(ce.outputs['Rotation'], iop2.inputs['Rotation']); L.new(cs.outputs[1], iop2.inputs['Scale'])
    L.new(iop2.outputs['Instances'], go.inputs[0])
    return ng
NG = spray_nodes()

# ------------------------------------------------------------------ which crowns: in / near the hero frame
cam = bpy.data.objects[HERO]
crowns_all = sorted((o for o in bpy.data.objects if o.name.startswith('PLACEHOLDER_park_tree_') and o.name.endswith('_crown')), key=lambda o: o.name)
crowns = []
for o in crowns_all:
    bb = [o.matrix_world @ Vector(c) for c in o.bound_box]
    for p in bb + [sum(bb, Vector()) / 8]:
        v = world_to_camera_view(sc, cam, p)
        if v.z > 0 and -FRUSTUM_MARGIN < v.x < 1 + FRUSTUM_MARGIN and -FRUSTUM_MARGIN < v.y < 1 + FRUSTUM_MARGIN:
            crowns.append(o); break
INFO['park_crowns_total'] = len(crowns_all); INFO['dressed'] = len(crowns)

def spheres_of(o):
    me = o.data; mw = o.matrix_world
    V = np.array([tuple(mw @ v.co) for v in me.vertices])
    polys = list(me.polygons); assert len(polys) % 80 == 0, (o.name, len(polys))
    out = []
    for k in range(len(polys) // 80):
        fs = polys[k*80:(k+1)*80]; vi = sorted({i for p in fs for i in p.vertices}); P = V[vi]
        c = P.mean(0); r = float(np.linalg.norm(P - c, axis=1).mean())
        out.append((c, r, fs))
    return V, out
def unit(a): return a / np.linalg.norm(a, axis=-1, keepdims=True)

PTS, PVAR = [], []
limbBM = bmesh.new()
def limb(p0, p1, r0, r1, seg=6):
    d = Vector(p1) - Vector(p0); Ln = d.length
    if Ln < 1e-4: return
    q = d.normalized().to_track_quat('Z', 'Y').to_matrix().to_4x4()
    res = bmesh.ops.create_cone(limbBM, cap_ends=False, segments=seg, radius1=r0, radius2=r1, depth=Ln)
    bmesh.ops.transform(limbBM, matrix=Matrix.Translation((Vector(p0) + Vector(p1)) / 2) @ q, verts=res['verts'])

per = []
for o in crowns:
    V, sph = spheres_of(o)
    SC = np.array([s[0] for s in sph]); SR = np.array([s[1] for s in sph])
    trunk = bpy.data.objects[o.name.replace('_crown', '_trunk')]
    tb = [trunk.matrix_world @ Vector(c) for c in trunk.bound_box]
    tx, ty = sum(v.x for v in tb) / 8, sum(v.y for v in tb) / 8; ttop = max(v.z for v in tb); tbot = min(v.z for v in tb)
    cc = SC.mean(0); ctop0 = float(max(SC[:, 2] + SR))
    bites = unit(NPR.normal(size=(RNG.randint(*BITES), 3))); bite_r = NPR.uniform(0.10, 0.22, len(bites))   # cos-space radius
    lobes = unit(NPR.normal(size=(RNG.randint(*LOBES), 3)) * np.array([1, 1, 0.6])); lobe_r = NPR.uniform(0.3, 0.5, len(lobes))
    n0 = len(PTS); zmax = -1e9
    for k, (c, r, fs) in enumerate(sph):
        for p in fs:
            a = p.area
            if a <= 0: continue
            ncl = NPR.poisson(a * CLUSTER_PER_M2)
            if ncl == 0: continue
            vv = V[list(p.vertices)[:3]]
            uv = NPR.random((ncl, 2)); m_ = uv.sum(1) > 1; uv[m_] = 1 - uv[m_]
            pt = vv[0] + uv[:, :1] * (vv[1] - vv[0]) + uv[:, 1:] * (vv[2] - vv[0])
            nrm = unit(pt - c); dirc = unit(pt - cc)
            off = NPR.uniform(*OUT_OFF, ncl)
            lob = np.max(np.clip((dirc @ lobes.T - (1 - lobe_r)) / lobe_r, 0, 1), 1)
            off = off + lob * NPR.uniform(0.3, 1.0, ncl) * LOBE_OFF
            bit = np.max(np.clip((dirc @ bites.T - (1 - bite_r)) / bite_r, 0, 1), 1)
            off = off * (1 - bit) + bit * NPR.uniform(0.0, 0.15, ncl)   # 'bites': foliage held in at the placeholder surface (indent, in shade)
            q = pt + nrm * off[:, None]
            dd = np.linalg.norm(q[:, None, :] - SC[None], axis=2)
            inside = (dd < SR[None] * 0.97); inside[:, k] = False
            keep = ~inside.any(1) & (q[:, 2] > tbot + MIN_LEAF_Z)   # nothing inside another sphere; lowest leaves >= 3 m above the ground
            q = q[keep]
            if not len(q): continue
            up = (q[:, 2] - cc[2]) / max(ctop0 - cc[2], 1e-3)
            var = np.clip(NPR.beta(2.0, 2.2, len(q)) * 0.75 + 0.18 * np.clip(up, -1, 1) - 0.35 * bit[keep], 0, 1)
            PTS.extend(map(tuple, q)); PVAR.extend(var.tolist()); zmax = max(zmax, float(q[:, 2].max()))
    base = Vector((tx, ty, ttop - 0.6)); nlimb = RNG.randint(6, 8)
    for j in range(nlimb):
        c, r, _ = sph[(j * 4 + RNG.randrange(9)) % len(sph)]
        dirn = (Vector(tuple(c)) - base); dirn.z = abs(dirn.z) + 0.8; dirn.normalize()
        tip = Vector(tuple(c)) + dirn * (r * RNG.uniform(0.7, 1.0))
        mid = base + (tip - base) * 0.45 + Vector((RNG.uniform(-.6, .6), RNG.uniform(-.6, .6), RNG.uniform(0, .6)))
        limb(base, mid, 0.20, 0.13); limb(mid, tip, 0.13, 0.04)
        fd = Vector((RNG.uniform(-1, 1), RNG.uniform(-1, 1), RNG.uniform(0.2, 1))).normalized()
        limb(mid, mid + fd * RNG.uniform(1.8, 3.2), 0.08, 0.025, seg=5)
    per.append((o.name.replace('PLACEHOLDER_park_tree_', 'T').replace('_crown', ''), len(PTS) - n0, round(ttop - tbot, 2), round(ctop0 - tbot, 2), round(zmax + CLUSTER_R + LEAF_L[1] - tbot, 2)))

me = bpy.data.meshes.new('cp053_leaf_canopy'); me.from_pydata(PTS, [], [])
at = me.attributes.new('cvar', 'FLOAT', 'POINT'); at.data.foreach_set('value', np.array(PVAR, dtype=np.float32)); me.update()
canopy = bpy.data.objects.new('cp053_leaf_canopy', me); col.objects.link(canopy); canopy['cp_state'] = STATE
mod = canopy.modifiers.new('cp053_leaf_sprays', 'NODES'); mod.node_group = NG
me = bpy.data.meshes.new('cp053_limbs'); limbBM.to_mesh(me); limbBM.free(); me.materials.append(M_BARK)
limbs = bpy.data.objects.new('cp053_limbs', me); col.objects.link(limbs); limbs['cp_state'] = STATE
INFO['sprays'] = len(PTS); INFO['leaves'] = len(PTS) * LEAVES_PER_CLUSTER
col['evidence'] = ('storyboard CP053 1911 SY11 (company bankrupt; Festival of Empire summer) R as brief; Festival of Empire May-Oct 1911 in the '
                   'grounds (Wikipedia; Piggott) R; r03 park placeholder positions (plan 0591) R/I; species, leaf size, crown form I; only crowns '
                   'in/near the CAM_CP053_empire_pavilions_wide_35mm frustum dressed')
col['dressed_crowns'] = str([o.name for o in crowns])
col['per_tree'] = str(per)
bpy.context.view_layer.update()
INFO['objects'] = len(col.objects); INFO['new_objects_total'] = len(bpy.data.objects) - n_before
INFO['new_materials'] = len(bpy.data.materials) - nmat_before
assert sorted(o.name for o in bpy.data.objects if o.hide_render) == hidden_before
assert len(bpy.data.objects) - n_before == len(col.objects), 'every new object must be in the one dated collection'
print('CP053 BUILT', INFO)
for p in per: print('CP053 TREE', p)
if OUT != '--nosave':
    os.makedirs(os.path.dirname(os.path.abspath(OUT)), exist_ok=True)
    bpy.ops.wm.save_as_mainfile(filepath=os.path.abspath(OUT), copy=True)
    print('CP053 SAVED', OUT)
