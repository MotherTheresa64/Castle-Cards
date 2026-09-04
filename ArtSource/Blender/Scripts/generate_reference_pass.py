import bpy
import math
import random
from pathlib import Path
from mathutils import Vector

ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / "Models" / "Hero"
SRC = ROOT / "ArtSource" / "Blender" / "Hero"
OUT.mkdir(parents=True, exist_ok=True)
SRC.mkdir(parents=True, exist_ok=True)


def material(name, rgb, roughness=.92, metallic=0.0, emission=None, emission_strength=0.0):
    mat = bpy.data.materials.get(name)
    if mat:
        return mat
    mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    if bsdf:
        if "Base Color" in bsdf.inputs:
            bsdf.inputs["Base Color"].default_value = (*rgb, 1.0)
        if "Roughness" in bsdf.inputs:
            bsdf.inputs["Roughness"].default_value = roughness
        if "Metallic" in bsdf.inputs:
            bsdf.inputs["Metallic"].default_value = metallic
        if emission:
            key = "Emission Color" if "Emission Color" in bsdf.inputs else "Emission"
            if key in bsdf.inputs:
                bsdf.inputs[key].default_value = (*emission, 1.0)
            if "Emission Strength" in bsdf.inputs:
                bsdf.inputs["Emission Strength"].default_value = emission_strength
    return mat


# Reference-pass palette: warm, desaturated, readable in the dark tavern lighting.
STONE_D = material("REF_StoneDark", (.115, .120, .118), .98)
STONE = material("REF_Stone", (.285, .278, .255), .98)
STONE_L = material("REF_StoneLight", (.405, .382, .335), .96)
STONE_MOSS = material("REF_StoneMoss", (.155, .190, .120), .99)
WOOD_D = material("REF_WoodDark", (.050, .018, .009), .95)
WOOD = material("REF_Wood", (.150, .054, .018), .92)
WOOD_L = material("REF_WoodLight", (.245, .100, .034), .88)
IRON = material("REF_Iron", (.038, .043, .050), .42, .84)
STEEL = material("REF_Steel", (.285, .300, .305), .38, .72)
BRONZE = material("REF_Bronze", (.34, .175, .045), .46, .58)
BLUE = material("REF_BlueCloth", (.030, .080, .250), .98)
RED = material("REF_RedCloth", (.285, .025, .020), .98)
CLOTH = material("REF_Cloak", (.026, .025, .033), .99)
TUNIC = material("REF_Tunic", (.095, .085, .075), .98)
LEATHER = material("REF_Leather", (.120, .038, .015), .93)
LEATHER_L = material("REF_LeatherLight", (.220, .082, .026), .90)
SKIN = material("REF_Skin", (.50, .295, .185), .88)
SKIN_SHADOW = material("REF_SkinShadow", (.36, .185, .115), .90)
HAIR = material("REF_Brunette", (.050, .020, .010), .95)
HAIR_L = material("REF_BrunetteLight", (.105, .042, .018), .94)
BONE = material("REF_Bone", (.63, .56, .43), .96)
BLACK = material("REF_Black", (.008, .009, .011), .99)
FIRE = material("REF_Fire", (1.0, .12, .008), .18, 0.0, (1.0, .07, .003), 8.0)


def clear_scene():
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)


def assign(obj, mat):
    if hasattr(obj.data, "materials"):
        obj.data.materials.append(mat)


def flat(obj):
    if hasattr(obj.data, "polygons"):
        for poly in obj.data.polygons:
            poly.use_smooth = False


def bevel(obj, width=.02):
    if width <= 0:
        return obj
    bpy.context.view_layer.objects.active = obj
    obj.select_set(True)
    mod = obj.modifiers.new("RefBevel", "BEVEL")
    mod.width = width
    mod.segments = 1
    try:
        mod.affect = 'EDGES'
    except Exception:
        pass
    try:
        bpy.ops.object.modifier_apply(modifier=mod.name)
    except Exception:
        pass
    return obj


def cube(name, loc, dims, mat, rot=(0, 0, 0), b=.025):
    bpy.ops.mesh.primitive_cube_add(location=loc, rotation=rot)
    obj = bpy.context.object
    obj.name = name
    obj.dimensions = dims
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    assign(obj, mat)
    flat(obj)
    bevel(obj, b)
    return obj


def cyl(name, loc, radius, depth, mat, verts=10, rot=(0, 0, 0), b=.012):
    bpy.ops.mesh.primitive_cylinder_add(vertices=verts, radius=radius, depth=depth, location=loc, rotation=rot)
    obj = bpy.context.object
    obj.name = name
    assign(obj, mat)
    flat(obj)
    bevel(obj, b)
    return obj


def cone(name, loc, r1, r2, depth, mat, verts=8, rot=(0, 0, 0)):
    bpy.ops.mesh.primitive_cone_add(vertices=verts, radius1=r1, radius2=r2, depth=depth, location=loc, rotation=rot)
    obj = bpy.context.object
    obj.name = name
    assign(obj, mat)
    flat(obj)
    return obj


def ico(name, loc, scale, mat, sub=1, rot=(0, 0, 0)):
    bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=sub, radius=1.0, location=loc, rotation=rot)
    obj = bpy.context.object
    obj.name = name
    obj.scale = scale
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    assign(obj, mat)
    flat(obj)
    return obj


def torus(name, loc, major, minor, mat, rot=(0, 0, 0), major_segments=12, minor_segments=4):
    bpy.ops.mesh.primitive_torus_add(
        major_radius=major,
        minor_radius=minor,
        major_segments=major_segments,
        minor_segments=minor_segments,
        location=loc,
        rotation=rot,
    )
    obj = bpy.context.object
    obj.name = name
    assign(obj, mat)
    flat(obj)
    return obj


def beam(name, a, b, radius, mat, verts=8):
    a = Vector(a)
    b = Vector(b)
    direction = b - a
    mid = (a + b) * .5
    bpy.ops.mesh.primitive_cylinder_add(vertices=verts, radius=radius, depth=direction.length, location=mid)
    obj = bpy.context.object
    obj.name = name
    obj.rotation_mode = 'QUATERNION'
    obj.rotation_quaternion = Vector((0, 0, 1)).rotation_difference(direction.normalized())
    assign(obj, mat)
    flat(obj)
    bevel(obj, radius * .08)
    return obj


def mesh_obj(name, verts, faces, materials, face_indices=None):
    mesh = bpy.data.meshes.new(name + "Mesh")
    mesh.from_pydata(verts, [], faces)
    mesh.update()
    obj = bpy.data.objects.new(name, mesh)
    bpy.context.collection.objects.link(obj)
    for mat in materials:
        mesh.materials.append(mat)
    if face_indices:
        for poly, idx in zip(mesh.polygons, face_indices):
            poly.material_index = idx
    flat(obj)
    return obj


def export_asset(objects, filename):
    bpy.ops.object.select_all(action='DESELECT')
    for obj in objects:
        if obj and obj.name in bpy.context.view_layer.objects:
            obj.select_set(True)
    if objects:
        bpy.context.view_layer.objects.active = objects[0]
    bpy.ops.wm.save_as_mainfile(filepath=str(SRC / f"{filename}.blend"))
    bpy.ops.export_scene.gltf(
        filepath=str(OUT / f"{filename}.glb"),
        export_format='GLB',
        use_selection=True,
        export_materials='EXPORT',
        export_normals=True,
        export_animations=False,
        export_yup=True,
    )
    print(f"[CastleCards Reference] Exported {filename}")


def add_crenellations(objects, prefix, a, b, z, height=.58, width=.42, depth=.62, mat=STONE):
    ax, ay = a
    bx, by = b
    length = math.hypot(bx - ax, by - ay)
    count = max(3, int(length / .72))
    ang = math.atan2(by - ay, bx - ax)
    for i in range(count):
        t = (i + .5) / count
        x = ax + (bx - ax) * t
        y = ay + (by - ay) * t
        objects.append(cube(f"{prefix}_Merlon_{i}", (x, y, z), (width, depth, height), mat, rot=(0, 0, ang), b=.018))


def add_wall(objects, prefix, a, b, height=2.55, thick=.48):
    ax, ay = a
    bx, by = b
    mid = ((ax + bx) * .5, (ay + by) * .5, height * .5)
    length = math.hypot(bx - ax, by - ay)
    ang = math.atan2(by - ay, bx - ax)
    objects.append(cube(prefix + "_Core", mid, (length, thick, height), STONE, rot=(0, 0, ang), b=.032))
    objects.append(cube(prefix + "_Cap", (mid[0], mid[1], height + .04), (length + .10, thick + .10, .18), STONE_D, rot=(0, 0, ang), b=.014))
    add_crenellations(objects, prefix, a, b, height + .38, height=.62, width=.40, depth=thick + .12)

    # Sparse irregular face stones catch highlights without turning the wall into visual noise.
    count = max(2, int(length / 1.45))
    for row in range(3):
        z = .48 + row * .67
        for i in range(count):
            t = (i + .5 + (row % 2) * .25) / count
            t = min(.94, max(.06, t))
            x = ax + (bx - ax) * t
            y = ay + (by - ay) * t
            normal = Vector((-(by - ay), bx - ax, 0)).normalized()
            x += normal.x * (thick * .51)
            y += normal.y * (thick * .51)
            mat = (STONE_D, STONE_L, STONE)[(i + row) % 3]
            objects.append(cube(f"{prefix}_Face_{row}_{i}", (x, y, z), (.62, .055, .30), mat, rot=(0, 0, ang), b=.006))


def add_tower(objects, prefix, x, y, radius, height, accent=None):
    accent = accent or STONE_L
    objects.append(cyl(prefix + "_Core", (x, y, height * .5), radius, height, STONE, verts=10, b=.038))
    objects.append(cyl(prefix + "_Foot", (x, y, .22), radius + .15, .44, STONE_D, verts=10, b=.024))
    objects.append(cyl(prefix + "_TopBand", (x, y, height - .18), radius + .09, .20, accent, verts=10, b=.018))

    for i in range(10):
        angle = math.tau * i / 10
        xx = x + math.cos(angle) * (radius - .03)
        yy = y + math.sin(angle) * (radius - .03)
        objects.append(cube(f"{prefix}_Merlon_{i}", (xx, yy, height + .35), (.40, .52, .62), STONE, rot=(0, 0, angle), b=.020))

    for row in range(4):
        z = .65 + row * max(.52, (height - 1.2) / 4)
        for i in range(5):
            angle = math.tau * (i + (row % 2) * .5) / 5
            xx = x + math.cos(angle) * (radius + .015)
            yy = y + math.sin(angle) * (radius + .015)
            mat = (STONE_D, STONE_L, STONE)[(row + i) % 3]
            objects.append(cube(f"{prefix}_Stone_{row}_{i}", (xx, yy, z), (.48, .050, .28), mat, rot=(0, 0, angle), b=.006))

    # Deep arrow slits on the front and outside faces.
    for j, angle in enumerate((0, math.pi / 2, math.pi, 3 * math.pi / 2)):
        xx = x + math.cos(angle) * (radius + .025)
        yy = y + math.sin(angle) * (radius + .025)
        objects.append(cube(f"{prefix}_Slit_{j}", (xx, yy, height * .56), (.08, .055, .42), BLACK, rot=(0, 0, angle), b=.003))


def build_castle():
    clear_scene()
    objects = []

    # Low, broad silhouette inspired by the target frame. Front towers are intentionally heavier,
    # while the keep stays back so the gate remains the focal point.
    add_tower(objects, "FrontL", -2.85, -2.12, 1.05, 3.70, STONE_L)
    add_tower(objects, "FrontR", 2.92, -2.12, 1.08, 3.82, STONE_L)
    add_tower(objects, "RearL", -3.10, 1.80, .86, 3.25, STONE_D)
    add_tower(objects, "RearR", 3.08, 1.85, .84, 3.15, STONE_D)

    add_wall(objects, "LeftWall", (-2.85, -2.12), (-3.10, 1.80), 2.35, .50)
    add_wall(objects, "RightWall", (2.92, -2.12), (3.08, 1.85), 2.35, .50)
    add_wall(objects, "RearWall", (-3.10, 1.80), (3.08, 1.85), 2.25, .48)
    add_wall(objects, "FrontLeft", (-2.85, -2.12), (-1.05, -2.12), 2.26, .50)
    add_wall(objects, "FrontRight", (1.05, -2.12), (2.92, -2.12), 2.26, .50)

    # Wider curtain-wall wings create the same broad fortress footprint visible in the reference.
    add_wall(objects, "WingL", (-3.55, -.92), (-5.38, -.75), 1.78, .44)
    add_wall(objects, "WingR", (3.55, -.92), (5.42, -.72), 1.82, .44)
    add_tower(objects, "WingTowerL", -5.55, -.70, .66, 2.40, STONE_D)
    add_tower(objects, "WingTowerR", 5.60, -.67, .66, 2.44, STONE_D)

    # Gatehouse is built around a real void instead of a dark rectangle pasted on a wall.
    objects.append(cube("GatePierL", (-.72, -2.18, 1.45), (.70, .82, 2.90), STONE, b=.038))
    objects.append(cube("GatePierR", (.72, -2.18, 1.45), (.70, .82, 2.90), STONE, b=.038))
    objects.append(cube("GateBridge", (0, -2.18, 3.05), (2.10, .84, .95), STONE_L, b=.038))
    objects.append(cube("GateShadow", (0, -2.61, 1.30), (1.08, .055, 2.35), BLACK, b=.002))
    for i, x in enumerate((-.48, -.32, -.16, 0, .16, .32, .48)):
        objects.append(cube(f"PortcullisV_{i}", (x, -2.66, 1.35), (.032, .040, 2.28), IRON, b=.002))
    for i, z in enumerate((.52, .92, 1.32, 1.72, 2.12)):
        objects.append(cube(f"PortcullisH_{i}", (0, -2.66, z), (1.05, .040, .032), IRON, b=.002))
    add_crenellations(objects, "Gate", (-1.08, -2.18), (1.08, -2.18), 3.73, height=.62, width=.34, depth=.75)

    # Drawbridge and chain hardware make the entrance feel functional.
    objects.append(cube("Drawbridge", (0, -3.18, .20), (1.55, 2.15, .22), WOOD_L, rot=(math.radians(4), 0, 0), b=.025))
    for x in (-.55, .55):
        objects.append(beam(f"BridgeChain_{x}", (x, -2.58, 2.55), (x, -3.85, .48), .030, IRON, 6))
    for i in range(5):
        objects.append(cube(f"BridgePlank_{i}", (-.58 + i * .29, -3.25, .34), (.22, 1.95, .075), WOOD, b=.008))

    # Central keep, offset rearward so it layers instead of becoming one giant central block.
    objects.append(cube("KeepCore", (0, .55, 2.18), (3.55, 2.90, 4.36), STONE_D, b=.060))
    objects.append(cube("KeepFront", (0, -.93, 2.16), (3.28, .10, 4.12), STONE, b=.024))
    objects.append(cube("KeepCap", (0, .55, 4.47), (3.82, 3.16, .24), STONE_L, b=.022))
    add_crenellations(objects, "KeepFront", (-1.55, -.91), (1.55, -.91), 4.88, height=.68, width=.38, depth=.55)
    add_crenellations(objects, "KeepBack", (-1.55, 1.98), (1.55, 1.98), 4.88, height=.68, width=.38, depth=.55)

    # Small upper tower gives an authored asymmetry rather than a perfectly mirrored toy castle.
    objects.append(cyl("KeepTurret", (-.86, .54, 5.03), .58, 1.20, STONE, verts=9, b=.026))
    for i in range(8):
        a = math.tau * i / 8
        objects.append(cube(f"KeepTurretMerlon_{i}", (-.86 + math.cos(a) * .50, .54 + math.sin(a) * .50, 5.86), (.24, .34, .42), STONE_L, rot=(0, 0, a), b=.012))

    # Windows, buttresses, banners and flame sources are sized to remain readable at gameplay scale.
    for i, (x, z) in enumerate(((-.85, 2.55), (.85, 2.55), (-.85, 3.48), (.85, 3.48))):
        objects.append(cube(f"KeepWindow_{i}", (x, -1.00, z), (.20, .055, .42), BLACK, b=.003))
        objects.append(cube(f"KeepLintel_{i}", (x, -1.04, z + .27), (.34, .08, .08), STONE_L, b=.004))
    for i, x in enumerate((-1.80, 1.80)):
        objects.append(cube(f"Buttress_{i}", (x, -1.42, 1.06), (.42, .72, 2.12), STONE_D, rot=(0, 0, math.radians(3 if x < 0 else -3)), b=.028))

    for i, (x, mat, z) in enumerate(((-1.12, BLUE, 3.54), (1.12, RED, 3.44))):
        objects.append(cyl(f"BannerPole_{i}", (x, -2.66, z + .28), .028, 1.50, IRON, verts=8, b=.002))
        objects.append(cube(f"Banner_{i}", (x, -2.70, z), (.58, .050, .92), mat, b=.006))

    for i, x in enumerate((-.92, .92)):
        objects.append(beam(f"GateTorch_{i}", (x, -2.65, 2.25), (x, -2.75, 2.68), .026, WOOD_D, 6))
        objects.append(ico(f"GateFlame_{i}", (x, -2.80, 2.83), (.065, .055, .15), FIRE, sub=1))

    # Grounding debris and moss patches break the perfect kit-bash feeling.
    rng = random.Random(921)
    for i in range(20):
        x = rng.uniform(-5.7, 5.7)
        y = rng.uniform(-2.9, 2.3)
        if abs(x) < 1.25 and y < -1.35:
            continue
        scale = rng.uniform(.09, .22)
        objects.append(ico(f"Rubble_{i}", (x, y, .08), (scale, scale * .78, scale * .66), STONE_D if i % 2 else STONE, sub=1, rot=(rng.random(), rng.random(), rng.random())))
    for i, (x, y, s) in enumerate(((-3.0, 1.45, .42), (2.68, 1.40, .34), (-5.25, -.42, .28), (5.18, -.35, .26))):
        objects.append(ico(f"Moss_{i}", (x, y, .12), (s, s * .58, .055), STONE_MOSS, sub=1))

    export_asset(objects, "castle_hero")


def build_opponent():
    clear_scene()
    objects = []

    # The chair exists mostly as silhouette. The character is leaned forward so the face and hands
    # read clearly over the far edge of the war table, matching the reference composition.
    objects.append(cube("ChairBack", (0, 1.10, 4.25), (3.20, .34, 6.35), WOOD_D, b=.080))
    objects.append(cube("ChairSeat", (0, .45, 1.30), (3.25, 2.05, .28), WOOD, b=.055))
    for x in (-1.36, 1.36):
        objects.append(cube(f"ChairPost_{x}", (x, 1.08, 4.58), (.26, .30, 6.80), WOOD_L, b=.030))
        objects.append(ico(f"ChairCap_{x}", (x, 1.08, 8.02), (.20, .20, .24), BRONZE, sub=1))

    # Seated lower body stays dark so it recedes behind the tabletop.
    objects.append(beam("ThighL", (-.58, .18, 2.55), (-.82, -.82, 1.75), .34, CLOTH, 10))
    objects.append(beam("ThighR", (.58, .18, 2.55), (.82, -.82, 1.75), .34, CLOTH, 10))

    # Layered torso: tunic, leather cross-straps, belt, cloak and collar.
    objects.append(cone("Torso", (0, -.10, 4.68), 1.50, 1.12, 3.18, TUNIC, verts=10, rot=(math.radians(4), 0, 0)))
    objects.append(ico("ShoulderMass", (0, -.05, 5.80), (1.92, .80, .60), CLOTH, sub=2))
    cloak_verts = [
        (-1.64, -.50, 5.70), (-.28, -.84, 5.45), (-.36, -.72, 3.15), (-1.28, -.28, 2.78),
        (.28, -.84, 5.45), (1.64, -.50, 5.70), (1.28, -.28, 2.78), (.36, -.72, 3.15),
    ]
    objects.append(mesh_obj("CloakPanels", cloak_verts, [(0, 1, 2, 3), (4, 5, 6, 7)], [CLOTH], [0, 0]))
    objects.append(torus("CloakCollar", (0, -.12, 6.15), .68, .16, CLOTH, rot=(math.pi / 2, 0, 0), major_segments=12, minor_segments=5))
    objects.append(cube("Belt", (0, -.24, 3.42), (2.18, .62, .18), LEATHER, b=.022))
    objects.append(cube("Buckle", (0, -.56, 3.42), (.30, .10, .27), BRONZE, b=.012))
    objects.append(beam("StrapL", (-.78, -.62, 5.58), (.38, -.62, 3.72), .075, LEATHER_L, 8))
    objects.append(beam("StrapR", (.82, -.61, 5.58), (-.36, -.61, 3.72), .075, LEATHER, 8))

    # Neck/head are moved slightly forward (negative Blender Y -> positive Godot Z) to prevent the
    # face from being swallowed by the chair/back wall.
    objects.append(cyl("Neck", (0, -.22, 6.35), .35, .58, SKIN_SHADOW, verts=10, b=.012))
    objects.append(ico("Head", (0, -.34, 7.26), (.94, .80, 1.02), SKIN, sub=2))
    objects.append(ico("Jaw", (0, -.45, 6.78), (.67, .64, .47), SKIN_SHADOW, sub=1))
    objects.append(ico("Nose", (0, -1.12, 7.27), (.135, .16, .23), SKIN, sub=1))
    objects.append(ico("CheekL", (-.49, -.94, 7.17), (.19, .08, .16), SKIN, sub=1))
    objects.append(ico("CheekR", (.49, -.94, 7.17), (.19, .08, .16), SKIN, sub=1))

    for side, x in (("L", -.31), ("R", .31)):
        objects.append(ico(f"EyeWhite_{side}", (x, -1.04, 7.49), (.095, .045, .065), BONE, sub=1))
        objects.append(ico(f"Iris_{side}", (x, -1.09, 7.49), (.042, .022, .042), BLACK, sub=1))
        brow_rot = math.radians(-8 if side == "L" else 8)
        objects.append(cube(f"Brow_{side}", (x, -1.08, 7.71), (.34, .060, .072), HAIR, rot=(0, 0, brow_rot), b=.005))

    # Brunette hair uses overlapping low-poly masses rather than a single helmet-like cap.
    objects.append(ico("HairCrown", (0, -.22, 8.01), (.98, .81, .56), HAIR, sub=2))
    hair_locks = (
        (-.70, -.50, 7.88, .34, -.22), (.68, -.48, 7.90, .34, .20),
        (-.84, -.05, 7.58, .30, -.10), (.82, -.02, 7.60, .30, .12),
        (-.48, .30, 7.92, .32, -.18), (.46, .32, 7.94, .32, .16),
        (-.18, -.76, 8.12, .28, -.08), (.20, -.74, 8.14, .27, .08),
    )
    for i, (x, y, z, s, rz) in enumerate(hair_locks):
        objects.append(ico(f"HairLock_{i}", (x, y, z), (s, s * .72, s * .48), HAIR_L if i in (0, 4, 6) else HAIR, sub=1, rot=(i * .12, i * .08, rz)))

    # Beard and moustache are layered to keep the mouth/chin silhouette readable.
    objects.append(cone("BeardMain", (0, -.92, 6.66), .58, .12, .88, HAIR, verts=9, rot=(math.radians(7), 0, 0)))
    objects.append(ico("BeardL", (-.33, -.89, 6.91), (.33, .19, .40), HAIR_L, sub=1, rot=(0, 0, -.12)))
    objects.append(ico("BeardR", (.33, -.89, 6.91), (.33, .19, .40), HAIR, sub=1, rot=(0, 0, .12)))
    objects.append(cube("MustacheL", (-.18, -1.09, 7.00), (.30, .052, .085), HAIR, rot=(0, 0, math.radians(-11)), b=.004))
    objects.append(cube("MustacheR", (.18, -1.09, 7.00), (.30, .052, .085), HAIR, rot=(0, 0, math.radians(11)), b=.004))

    # Forward-reaching arms. The hands sit lower and farther forward than the old pass so they feel
    # planted on/near the table instead of dangling beside the torso.
    shoulder_l = (-1.58, -.12, 5.46)
    elbow_l = (-2.18, -.82, 4.32)
    wrist_l = (-2.00, -2.08, 3.18)
    shoulder_r = (1.58, -.12, 5.46)
    elbow_r = (2.15, -.84, 4.34)
    wrist_r = (1.92, -2.10, 3.20)
    objects.append(beam("UpperArmL", shoulder_l, elbow_l, .31, CLOTH, 10))
    objects.append(beam("UpperArmR", shoulder_r, elbow_r, .31, CLOTH, 10))
    objects.append(cyl("BracerL", (-2.11, -1.48, 3.72), .26, .72, LEATHER, verts=9, rot=(math.radians(68), 0, math.radians(-8)), b=.010))
    objects.append(cyl("BracerR", (2.04, -1.50, 3.74), .26, .72, LEATHER, verts=9, rot=(math.radians(68), 0, math.radians(8)), b=.010))
    objects.append(beam("ForearmL", elbow_l, wrist_l, .255, SKIN, 10))
    objects.append(beam("ForearmR", elbow_r, wrist_r, .255, SKIN, 10))
    objects.append(ico("HandL", wrist_l, (.39, .31, .42), SKIN, sub=2, rot=(.18, 0, -.10)))
    objects.append(ico("HandR", wrist_r, (.39, .31, .42), SKIN, sub=2, rot=(.18, 0, .10)))

    for hand_idx, (wx, wy, wz, sign) in enumerate(((*wrist_l, -1), (*wrist_r, 1))):
        for finger in range(4):
            x = wx + sign * (finger - 1.5) * .070
            objects.append(beam(f"Finger_{hand_idx}_{finger}", (x, wy - .14, wz - .08), (x + sign * .018, wy - .38, wz - .12), .028, SKIN, 6))

    # Brooch/pendant gives the warm metallic focal point visible in the target image.
    objects.append(ico("Brooch", (0, -.86, 5.91), (.21, .075, .21), BRONZE, sub=1))
    objects.append(beam("PendantChain", (0, -.79, 5.75), (0, -.82, 5.12), .018, BRONZE, 6))
    objects.append(ico("Pendant", (0, -.84, 4.99), (.13, .06, .17), BRONZE, sub=1))

    export_asset(objects, "opponent_hero")


jobs = [build_castle, build_opponent]
print("\n[CastleCards Reference] Generating reference-composition hero assets...\n")
for fn in jobs:
    print(f"[CastleCards Reference] {fn.__name__}")
    fn()
print(f"\n[CastleCards Reference] Complete: {len(jobs)} hero assets regenerated.\n")
