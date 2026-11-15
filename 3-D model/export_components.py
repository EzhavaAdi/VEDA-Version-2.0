"""
VEDA V2 — Export truck components as separate GLB files.

HOW TO RUN:
1. Open Blender
2. Open the file: refuse_truck_exploded.blend  (File > Open)
3. Go to the Scripting workspace (top tab bar)
4. Click "Open" and select this file: export_components.py
5. Click "Run Script" (the Play button, or Alt+P)

OUTPUT:
Each component group is exported as a separate GLB into:
  C:/VEDA_2.0/3-D model/components/

Files created:
  axle_wheels.glb
  axle_suspension.glb
  cab_assembly.glb
  refuse_body.glb
  chassis.glb
  rear_compactor.glb
  other_fittings.glb
  full_truck.glb  (complete assembled model for reference)
"""
/*******************
 import bpy
import os

OUTPUT_DIR = r"C:\VEDA_2.0\3-D model\components"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ── Deselect everything to start clean ───────────────────────────────────────
def deselect_all():
    bpy.ops.object.select_all(action='DESELECT')

# ── Select objects whose name matches keywords ────────────────────────────────
def select_by_keywords(keywords):
    deselect_all()
    count = 0
    for obj in bpy.context.scene.objects:
        if obj.type != 'MESH':
            continue
        n = obj.name.lower()
        if any(k.lower() in n for k in keywords):
            obj.select_set(True)
            count += 1
    return count

# ── Export selected objects as GLB ────────────────────────────────────────────
def export_selected(filename):
    filepath = os.path.join(OUTPUT_DIR, filename)
    bpy.ops.export_scene.gltf(
        filepath=filepath,
        use_selection=True,
        export_format='GLB',
        export_apply=True,
        export_animations=False,
        export_materials='EXPORT',
        export_normals=True,
    )
    print(f"  Exported: {filepath}")
    return filepath

# ── Reset all objects to frame 1 (assembled position) ─────────────────────────
bpy.context.scene.frame_set(1)
bpy.context.view_layer.update()

print("=" * 55)
print("  VEDA — Component GLB Export")
print("=" * 55)

# ── 1. Wheels ─────────────────────────────────────────────────────────────────
print("\n[1] Wheels...")
n = select_by_keywords(['wheel', 'tyre', 'tire'])
print(f"  Selected {n} objects")
if n > 0:
    export_selected("axle_wheels.glb")

# ── 2. Axle / Suspension / Differential ──────────────────────────────────────
print("\n[2] Axle & Suspension...")
n = select_by_keywords([
    'axle', 'suspension', 'differential', 'spring saddle',
    'leaf spring', 'through housing', 'bearing hub', 'wheel stud'
])
print(f"  Selected {n} objects")
if n > 0:
    export_selected("axle_suspension.glb")

# ── 3. Cab ────────────────────────────────────────────────────────────────────
print("\n[3] Cab Assembly...")
n = select_by_keywords([
    'cab', 'door', 'mirror', 'windscreen', 'steering',
    'instrument', 'roof', 'grille', 'headlamp', 'indicator',
    'step', 'glazing', 'glass'
])
print(f"  Selected {n} objects")
if n > 0:
    export_selected("cab_assembly.glb")

# ── 4. Refuse body shell ──────────────────────────────────────────────────────
print("\n[4] Refuse Body...")
n = select_by_keywords([
    'refuse', 'body', 'container', 'hopper', 'shell',
    'reinforcement', 'panel'
])
print(f"  Selected {n} objects")
if n > 0:
    export_selected("refuse_body.glb")

# ── 5. Chassis ────────────────────────────────────────────────────────────────
print("\n[5] Chassis & Frame...")
n = select_by_keywords([
    'chassis', 'crossmember', 'longitudinal', 'rail',
    'bumper', 'mounting', 'isolator', 'frame'
])
print(f"  Selected {n} objects")
if n > 0:
    export_selected("chassis.glb")

# ── 6. Rear compactor / hopper mechanism ─────────────────────────────────────
print("\n[6] Rear Compactor...")
n = select_by_keywords([
    'compactor', 'packer', 'rear', 'crew', 'grab handle',
    'transverse bumper', 'lamp', 'stop lamp', 'turn lamp'
])
print(f"  Selected {n} objects")
if n > 0:
    export_selected("rear_compactor.glb")

# ── 7. Other fittings ─────────────────────────────────────────────────────────
print("\n[7] Other Fittings...")
# Select everything NOT already in the main groups
all_keywords = [
    'wheel', 'tyre', 'tire', 'axle', 'suspension', 'differential',
    'spring', 'bearing', 'cab', 'door', 'mirror', 'windscreen',
    'steering', 'instrument', 'roof', 'grille', 'headlamp', 'indicator',
    'step', 'glazing', 'glass', 'refuse', 'body', 'container', 'hopper',
    'shell', 'chassis', 'crossmember', 'longitudinal', 'rail', 'bumper',
    'mounting', 'isolator', 'frame', 'compactor', 'packer', 'rear', 'crew',
    'grab', 'lamp',
]
deselect_all()
count = 0
for obj in bpy.context.scene.objects:
    if obj.type != 'MESH':
        continue
    n_lower = obj.name.lower()
    if not any(k.lower() in n_lower for k in all_keywords):
        obj.select_set(True)
        count += 1
print(f"  Selected {count} objects")
if count > 0:
    export_selected("other_fittings.glb")

# ── 8. Full assembled truck (all meshes) ──────────────────────────────────────
print("\n[8] Full Truck (all meshes)...")
deselect_all()
total = 0
for obj in bpy.context.scene.objects:
    if obj.type == 'MESH':
        obj.select_set(True)
        total += 1
print(f"  Selected {total} objects")
export_selected("full_truck.glb")

# ── Done ──────────────────────────────────────────────────────────────────────
print("\n" + "=" * 55)
print("  EXPORT COMPLETE")
print(f"  Output folder: {OUTPUT_DIR}")
print("=" * 55)
print("\nFiles created:")
for f in os.listdir(OUTPUT_DIR):
    if f.endswith('.glb'):
        size = os.path.getsize(os.path.join(OUTPUT_DIR, f))
        print(f"  {f:30s}  {size/1024/1024:.1f} MB")