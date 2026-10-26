import bpy,math,json,os,time
from pathlib import Path
from mathutils import Vector,Matrix
OUT=Path(os.environ.get('CRYSTAL_OUTPUT','crystal-palace-output')); OUT.mkdir(exist_ok=True)
for d in ['renders','compare','scripts']: (OUT/d).mkdir(exist_ok=True)
SOURCE=Path(os.environ['CRYSTAL_SOURCE'])
MAP=SOURCE/'maps'
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.fbx(filepath=str(SOURCE/'Crystal Palace_FBX.FBX'),use_image_search=True)
s=bpy.context.scene
for o in list(s.objects):
 if o.type in ['CAMERA','LIGHT']: bpy.data.objects.remove(o,do_unlink=True)
meshes=[o for o in s.objects if o.type=='MESH']
# Bake the FBX transforms, preserving world positions and UVs.
for o in meshes:
 o.data.transform(o.matrix_world);o.matrix_world=Matrix.Identity(4)
# Organize original source components without joining them.
model=bpy.data.collections.new('Crystal Palace | source geometry');s.collection.children.link(model)
for o in meshes:
 for col in list(o.users_collection): col.objects.unlink(o)
 model.objects.link(o)
rig=bpy.data.collections.new('Presentation | cameras and lights');s.collection.children.link(rig)
def move_rig(o):
 for c in list(o.users_collection):c.objects.unlink(o)
 rig.objects.link(o)
def camera(name,pos,target,scale):
 bpy.ops.object.camera_add(location=pos);o=bpy.context.object;o.name=name;o.rotation_euler=(Vector(target)-o.location).to_track_quat('-Z','Y').to_euler();o.data.type='ORTHO';o.data.ortho_scale=scale;o.data.clip_end=2000;move_rig(o);return o
cams=[camera('01 | Garden overview',(110,-150,105),(-1,0,17),180),camera('02 | Front elevation',(-1,-180,35),(-1,0,20),150),camera('03 | Entrance and ironwork',(30,-65,37),(0,-8,20),57),camera('04 | Reverse overview',(-105,150,95),(-1,0,17),165)]
s.world=bpy.data.worlds.new('Daylight');s.world.use_nodes=True;s.world.node_tree.nodes['Background'].inputs['Color'].default_value=(.68,.8,1,1);s.world.node_tree.nodes['Background'].inputs['Strength'].default_value=.45
s.camera=cams[0];s.render.resolution_x=1500;s.render.resolution_y=1000;s.render.resolution_percentage=100
# Reference is an actual render of the imported FBX; no historical photograph was supplied.
s.render.engine='BLENDER_WORKBENCH';s.display.shading.light='STUDIO';s.display.shading.color_type='MATERIAL';s.display.shading.show_cavity=True;s.display.shading.cavity_type='BOTH';s.display.shading.background_type='WORLD'
s.render.filepath=str(OUT/'compare/source-fbx.png');bpy.ops.render.render(write_still=True)
# Rebuild legacy renderer shaders as Principled materials.
if 'GLASS' not in bpy.data.materials:bpy.data.materials.new('GLASS')
for m in bpy.data.materials:
 col=tuple(m.diffuse_color);m.use_nodes=True;m.node_tree.nodes.clear();n=m.node_tree.nodes.new('ShaderNodeBsdfPrincipled');out=m.node_tree.nodes.new('ShaderNodeOutputMaterial');out.location=(600,0);m.node_tree.links.new(n.outputs['BSDF'],out.inputs['Surface']);n.inputs['Base Color'].default_value=col;n.inputs['Roughness'].default_value=.55
 if 'METAL' in m.name: n.inputs['Metallic'].default_value=.65;n.inputs['Roughness'].default_value=.32
 if 'GLASS' in m.name or 'Water' in m.name:
  n.inputs['Base Color'].default_value=(.92,.98,1,1);n.inputs['Transmission Weight'].default_value=1;n.inputs['Roughness'].default_value=.075;n.inputs['IOR'].default_value=1.333 if 'Water' in m.name else 1.45
bpy.data.objects['GLASS'].data.materials.clear();bpy.data.objects['GLASS'].data.materials.append(bpy.data.materials['GLASS'])
assignments=[]
def tex(mat,file,kind='color',strength=.2):
 m=bpy.data.materials[mat];nt=m.node_tree;p=next(n for n in nt.nodes if n.type=='BSDF_PRINCIPLED');im=bpy.data.images.load(str(MAP/file),check_existing=True)
 if kind!='color':im.colorspace_settings.name='Non-Color'
 t=nt.nodes.new('ShaderNodeTexImage');t.image=im;t.label=file;t.location=(-600,0)
 if kind=='color':nt.links.new(t.outputs['Color'],p.inputs['Base Color'])
 elif kind=='normal':
  n=nt.nodes.new('ShaderNodeNormalMap');n.inputs['Strength'].default_value=strength;nt.links.new(t.outputs['Color'],n.inputs['Color']);nt.links.new(n.outputs['Normal'],p.inputs['Normal'])
 elif kind=='bump':
  n=nt.nodes.new('ShaderNodeBump');n.inputs['Strength'].default_value=strength;n.inputs['Distance'].default_value=.015;nt.links.new(t.outputs['Color'],n.inputs['Height']);nt.links.new(n.outputs['Normal'],p.inputs['Normal'])
 elif kind=='gloss':
  n=nt.nodes.new('ShaderNodeMath');n.operation='SUBTRACT';n.inputs[0].default_value=1;nt.links.new(t.outputs['Color'],n.inputs[1]);nt.links.new(n.outputs[0],p.inputs['Roughness'])
 assignments.append({'material':mat,'map':file,'role':kind,'basis':'inferred from material name and map appearance; FBX had no texture links'})
tex('CONCRETE','Archexterior01_08_Concrete.jpg');tex('CONCRETE','Archexterior01_08_Concrete_NRM.jpg','normal',.35)
tex('Sandstone','5a6be048f658.jpg');tex('white stone','000005750421_C - copia - copia.png');tex('stone','b74a5c4e2346.jpg')
tex('Material #56597','Grass0138_1_seamless_L.jpg');tex('Material #56597','02 Cesped con astillas BW.jpg','bump',.15)
wood=sorted((MAP/'OAK WOOD BOARDS').glob('*colormatched_01*'))[0];tex('WOOD FLOOR BOARDS',str(wood.relative_to(MAP)))
for name in ['METAL','GREY METAL','BROWN METAL','BLUE METAL','YELLOW METAL']:tex(name,'metal_glossiness.jpg','gloss');tex(name,'OXIDO2 BUMP.jpg','bump',.08)
# Single sun plus broad sky; no invented geometry.
bpy.ops.object.light_add(type='SUN',location=(0,-70,100));sun=bpy.context.object;sun.name='Sun | late afternoon';sun.rotation_euler=(math.radians(24),math.radians(-28),math.radians(-30));sun.data.energy=2.5;sun.data.angle=math.radians(12);move_rig(sun)
s.render.engine='CYCLES';s.cycles.samples=32;s.cycles.use_denoising=True;s.cycles.max_bounces=8;s.cycles.transmission_bounces=6;s.cycles.transparent_max_bounces=12
s.view_settings.view_transform='AgX';s.unit_settings.system='METRIC';s.unit_settings.scale_length=1
for area in bpy.context.screen.areas:
 if area.type=='VIEW_3D':area.spaces.active.region_3d.view_perspective='CAMERA';area.spaces.active.clip_end=2000
bpy.ops.object.select_all(action='DESELECT');bpy.context.view_layer.objects.active=None
s['conversion_notes']='Source FBX geometry and UVs retained. Map assignments inferred, not recovered from original Max shaders. Source scale retained; historical dimensions not verified.'
s['prepared_for']='Nik Bear Brown';s['builder']='Codex';s['source_fbx']='Crystal Palace_FBX.FBX'
bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=str(OUT.parent/'crystal-palace-full.blend'),compress=True)
print('FULL_SAVED',flush=True)
# Lightweight course version: only structural mesh is decimated. Full-resolution native stays local.
o=bpy.data.objects['STRUCTURE'];bpy.context.view_layer.objects.active=o;o.select_set(True)
mod=o.modifiers.new('Course copy | structural reduction','DECIMATE');mod.ratio=.20;mod.use_collapse_triangulate=True
bpy.ops.object.modifier_apply(modifier=mod.name);o.select_set(False)
print('DECIMATION_COMPLETE',len(o.data.polygons),flush=True)
# Downsample packed maps in publication copy, retaining original maps in full native.
for im in bpy.data.images:
 if im.size[0] and max(im.size)>2048:
  factor=2048/max(im.size);im.scale(max(1,int(im.size[0]*factor)),max(1,int(im.size[1]*factor)));im.pack()
bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'crystal-palace.blend'),compress=True)
report={'blender':bpy.app.version_string,'texture_assignments':assignments,'mesh_objects':len(meshes),'vertices':sum(len(o.data.vertices) for o in meshes),'polygons':sum(len(o.data.polygons) for o in meshes),'materials':len([m for m in bpy.data.materials if m.users]),'images':len(bpy.data.images),'objects':[]}
for o in meshes:
 o.data.calc_loop_triangles();pts=[o.matrix_world@Vector(c) for c in o.bound_box];report['objects'].append({'name':o.name,'vertices':len(o.data.vertices),'triangles':len(o.data.loop_triangles),'dimensions':list(o.dimensions),'bounds':[[min(p[i] for p in pts) for i in range(3)],[max(p[i] for p in pts) for i in range(3)]]})
report['triangles']=sum(o['triangles'] for o in report['objects']);(OUT/'audit.json').write_text(json.dumps(report,indent=2))
# Matching geometry-only render isolates simplification changes.
s.render.engine='BLENDER_WORKBENCH';s.render.filepath=str(OUT/'compare/converted-geometry.png');bpy.ops.render.render(write_still=True)
s.render.engine='CYCLES'
for cam,slug in zip(cams,['overview','front','entrance','reverse']):
 s.camera=cam;s.render.filepath=str(OUT/'renders'/f'{slug}.png');bpy.ops.render.render(write_still=True);print('RENDERED',slug,flush=True)
s.camera=cams[0];s.render.filepath='//renders/overview.png';bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'crystal-palace.blend'),compress=True)
bpy.ops.object.select_all(action='DESELECT')
for o in meshes:o.select_set(True)
bpy.ops.export_scene.gltf(filepath=str(OUT/'crystal-palace.glb'),export_format='GLB',use_selection=True,export_apply=True,export_image_format='JPEG',export_jpeg_quality=85,export_draco_mesh_compression_enable=True,export_draco_mesh_compression_level=6)
print('BUILD_COMPLETE',flush=True)
