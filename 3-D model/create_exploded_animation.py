"""Create an exploded-view animation from refuse-collection-truck.glb.

Run in Blender: open Blender > Scripting > Open > this file > Run Script.
The script imports the GLB, groups its named mesh parts under animation empties,
creates a simple studio camera/light setup, and prepares a 12-second animation.
It does not overwrite the source GLB.
"""
import bpy
import os
import math
from mathutils import Vector

BASE_DIR = os.path.dirname(os.path.abspath(__file__)) if "__file__" in globals() else bpy.path.abspath("//")
GLB_PATH = os.path.join(BASE_DIR, "refuse-collection-truck.glb")
OUTPUT_BLEND = os.path.join(BASE_DIR, "refuse_truck_exploded.blend")
RENDER_PATH = os.path.join(BASE_DIR, "refuse_truck_exploded.mp4")
FPS = 30
DURATION_SECONDS = 12

if not os.path.exists(GLB_PATH):
    raise FileNotFoundError("Could not find GLB: " + GLB_PATH)

# Start clean, then import the source model.
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)
for datablocks in (bpy.data.collections,):
    pass
bpy.ops.import_scene.gltf(filepath=GLB_PATH)

meshes = [o for o in bpy.context.scene.objects if o.type == 'MESH']
if not meshes:
    raise RuntimeError("No mesh objects were imported from the GLB.")

# Calculate the model's world-space bounds and identify its long/width axes.
points = [o.matrix_world @ Vector(corner) for o in meshes for corner in o.bound_box]
mins = Vector((min(v[i] for v in points) for i in range(3)))
maxs = Vector((max(v[i] for v in points) for i in range(3)))
center = (mins + maxs) * 0.5
dims = maxs - mins
horizontal_axes = sorted((0, 1), key=lambda i: dims[i], reverse=True)
length_axis, width_axis = horizontal_axes
vertical_axis = 2
length_sign = 1.0

# Store mesh object names in semantic groups. Each group gets one animated empty,
# so detailed sub-parts stay assembled relative to one another during the motion.
groups = {}
def add(group, obj):
    groups.setdefault(group, []).append(obj)

for obj in meshes:
    n = obj.name.lower()
    # Wheels are grouped as complete wheel assemblies, by axle and vehicle side.
    if 'wheel' in n and any(s in n for s in ('axle 1', 'axle 2', 'axle 3')):
        axle = next((a for a in ('axle 1', 'axle 2', 'axle 3') if a in n), 'axle')
        side = '-1' if 'wheel -1' in n else '1'
        add(f'{axle.title()} wheel side {side}', obj)
    elif n.startswith(('axle 1', 'axle 2', 'axle 3')):
        axle = next((a for a in ('axle 1', 'axle 2', 'axle 3') if n.startswith(a)), 'axle')
        add(f'{axle.title()} suspension and differential', obj)
    elif any(k in n for k in ('compactor', 'packer blade', 'rear hopper', 'rear crew', 'rear seated', 'rear lamp', 'rear stop', 'rear turn')):
        add('Rear compactor and hopper mechanism', obj)
    elif any(k in n for k in ('sculpted hollow cab', 'cab ', 'door grip', 'mirror ', 'front headlamp', 'front indicator', 'roof ', 'windscreen', 'steering ', 'instrument ', 'cab entry')):
        add('Cab assembly and fittings', obj)
    elif any(k in n for k in ('refuse shaped hollow container', 'refuse body', 'finite sloping rear loading hopper')):
        add('Refuse body shell and reinforcement', obj)
    elif any(k in n for k in ('chassis', 'bumper', 'radiator grille backing')):
        add('Main chassis and bumpers', obj)
    else:
        add('Other vehicle fittings', obj)

# Direction vectors in Blender coordinates.
length_vec = Vector((1 if length_axis == 0 else 0, 1 if length_axis == 1 else 0, 0))
width_vec = Vector((1 if width_axis == 0 else 0, 1 if width_axis == 1 else 0, 0))

# Create one empty per group at that group's center and preserve each object's
# world transform when parenting it to the empty.
rigs = {}
for group_name, objects in groups.items():
    group_points = [o.matrix_world @ Vector(corner) for o in objects for corner in o.bound_box]
    gmin = Vector((min(v[i] for v in group_points) for i in range(3)))
    gmax = Vector((max(v[i] for v in group_points) for i in range(3)))
    gcenter = (gmin + gmax) * 0.5
    empty = bpy.data.objects.new('EXPLODE_CTRL | ' + group_name, None)
    bpy.context.collection.objects.link(empty)
    empty.empty_display_type = 'SPHERE'
    empty.empty_display_size = max(dims) * 0.025
    empty.location = gcenter
    for obj in objects:
        world = obj.matrix_world.copy()
        obj.parent = empty
        obj.matrix_world = world
    rigs[group_name] = (empty, gcenter)

# Timeline: assembled hold -> exploded -> hold -> reassembled.
scene = bpy.context.scene
scene.render.fps = FPS
scene.frame_start = 1
scene.frame_end = FPS * DURATION_SECONDS
f_assembled, f_split, f_hold, f_return = 1, 65, 230, 360

for group_name, (empty, origin) in rigs.items():
    n = group_name.lower()
    offset = Vector((0, 0, 0))
    if 'wheel side' in n:
        side = -1.0 if 'side -1' in n else 1.0
        offset = width_vec * side * (dims[width_axis] * 0.48) + Vector((0, 0, 0.25))
    elif 'suspension and differential' in n:
        offset = Vector((0, 0, -dims.z * 0.42))
    elif 'main chassis' in n:
        offset = Vector((0, 0, -dims.z * 0.34))
    elif 'refuse body shell' in n:
        offset = Vector((0, 0, dims.z * 0.48))
    elif 'cab assembly' in n:
        offset = Vector((0, 0, dims.z * 0.38)) + length_vec * (dims[length_axis] * 0.10)
    elif 'rear compactor' in n:
        # Rear mechanism separates longitudinally and slightly upward.
        side_of_center = 1.0 if (origin - center).dot(length_vec) >= 0 else -1.0
        offset = length_vec * side_of_center * (dims[length_axis] * 0.22) + Vector((0, 0, dims.z * 0.22))
    elif 'other vehicle fittings' in n:
        offset = Vector((0, 0, -dims.z * 0.12))
    else:
        offset = width_vec * (dims[width_axis] * 0.28) + Vector((0, 0, dims.z * 0.12))

    # A small stagger makes the exploded view read clearly without scattering parts too far.
    empty.location = origin
    empty.keyframe_insert(data_path='location', frame=f_assembled)
    empty.location = origin + offset
    empty.keyframe_insert(data_path='location', frame=f_split)
    empty.keyframe_insert(data_path='location', frame=f_hold)
    empty.location = origin
    empty.keyframe_insert(data_path='location', frame=f_return)

# Blender's default keyframe interpolation is Bezier, giving smooth motion.

# Studio camera: target the vehicle center, with a gentle orbit around the model.
cam_data = bpy.data.cameras.new('Exploded View Camera')
cam = bpy.data.objects.new('Exploded View Camera', cam_data)
scene.collection.objects.link(cam)
cam.location = center + Vector((dims.x * 1.15, -dims.y * 1.55, dims.z * 0.95))
cam_data.lens = 48
track = cam.constraints.new(type='TRACK_TO')
track.target = bpy.data.objects.new('Camera Target', None)
scene.collection.objects.link(track.target)
track.target.location = center
track.track_axis = 'TRACK_NEGATIVE_Z'
track.up_axis = 'UP_Y'
scene.camera = cam

# Area lights for readable mechanical forms.
def area_light(name, location, power, size):
    data = bpy.data.lights.new(name, type='AREA')
    data.energy = power
    data.shape = 'DISK'
    data.size = size
    obj = bpy.data.objects.new(name, data)
    scene.collection.objects.link(obj)
    obj.location = location
    c = obj.constraints.new(type='TRACK_TO')
    c.target = track.target
    c.track_axis = 'TRACK_NEGATIVE_Z'
    c.up_axis = 'UP_Y'
    return obj

scale = max(dims)
area_light('Key softbox', center + Vector((scale, -scale, scale * 1.3)), 1800, scale * 0.9)
area_light('Fill softbox', center + Vector((-scale, -scale * 0.4, scale * 0.55)), 1100, scale * 0.8)
area_light('Rim softbox', center + Vector((0, scale, scale)), 2200, scale * 0.7)

# Neutral studio world and render configuration.
world = scene.world or bpy.data.worlds.new('Studio World')
scene.world = world
world.use_nodes = True
world.node_tree.nodes['Background'].inputs['Color'].default_value = (0.12, 0.14, 0.18, 1)
world.node_tree.nodes['Background'].inputs['Strength'].default_value = 0.45
try:
    scene.render.engine = 'BLENDER_EEVEE_NEXT'
except Exception:
    scene.render.engine = 'BLENDER_EEVEE'
scene.render.resolution_x = 1920
scene.render.resolution_y = 1080
scene.render.resolution_percentage = 100
scene.render.image_settings.file_format = 'FFMPEG'
scene.render.ffmpeg.format = 'MPEG4'
scene.render.ffmpeg.codec = 'H264'
scene.render.filepath = RENDER_PATH
scene.view_settings.view_transform = 'AgX'
scene.frame_set(1)

# Save the editable Blender project. Render with Render > Render Animation (Ctrl+F12).
bpy.ops.wm.save_as_mainfile(filepath=OUTPUT_BLEND)
print('Exploded animation setup complete.')
print('Groups created:', len(rigs))
print('Mesh objects:', len(meshes))
print('Saved Blender project:', OUTPUT_BLEND)
print('Render output configured:', RENDER_PATH)
