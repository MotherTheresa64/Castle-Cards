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


# Cohesive reference palette. Values are intentionally lighter than the old pass so
# shape detail survives the cinematic tavern lighting.
STONE_D = material("REF2_StoneDark", (.15, .155, .150), .98)
STONE = material("REF2_Stone", (.34, .33, .30), .97)
STONE_L = material("REF2_StoneLight", (.48, .45, .39), .95)
MOSS = material("REF2_Moss", (.14, .20, .105), .99)
WOOD_D = material("REF2_WoodDark", (.060, .025, .014), .95)
WOOD = material("REF2_Wood", (.18, .075, .030), .91)
WOOD_L = material("REF2_WoodLight", (.30, .135, .052), .87)
IRON = material("REF2_Iron", (.045, .050, .058), .40, .82)
STEEL = material("REF2_Steel", (.31, .33, .34), .36, .70)
BRONZE = material("REF2_Bronze", (.39, .22, .065), .46, .56)
GRASS_D = material("REF2_GrassDark", (.060, .105, .045), .99)
GRASS = material("REF2_Grass", (.115, .185, .070), .99)
GRASS_L = material("REF2_GrassLight", (.17, .255, .095), .99)
DIRT = material("REF2_Dirt", (.30, .20, .105), .99)
DIRT_D = material("REF2_DirtDark", (.19, .115, .060), .99)
WATER = material("REF2_Water", (.040, .15, .22), .28, .04)
BLUE = material("REF2_Blue", (.040, .095, .28), .97)
RED = material("REF2_Red", (.32, .040, .028), .97)
CLOTH = material("REF2_Cloak", (.035, .032, .040), .99)
TUNIC = material("REF2_Tunic", (.16, .125, .090), .97)
LEATHER = material("REF2_Leather", (.14, .050, .022), .94)
LEATHER_L = material("REF2_LeatherLight", (.27, .11, .042), .90)
SKIN = material("REF2_Skin", (.59, .37, .245), .87)
SKIN_S = material("REF2_SkinShadow", (.43, .245, .155), .90)
HAIR = material("REF2_Brunette", (.055, .024, .013), .95)
HAIR_L = material("REF2_BrunetteLight", (.12, .052, .024), .93)
BONE = material("REF2_Bone", (.68, .61, .47), .95)
BLACK = material("REF2_Black", (.010, .011, .013), .99)
FELT = material("REF2_Felt", (.034, .061, .043), .99)
FIRE = material("REF2_Fire", (1.0, .20, .018), .18, 0.0, (1.0, .11, .008), 6.0)


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
    mod = obj.modifiers.new("Ref2Bevel", "BEVEL")
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
    print(f"[CastleCards Reference V2] Exported {filename}")


# -----------------------------------------------------------------------------
# War table: one coherent timber surface, not alternating black stripes.
# -----------------------------------------------------------------------------
def build_table():
    clear_scene()
    o = []

    o.append(cube("TableBody", (0, 0, -.12), (30.2, 27.0, .92), WOOD_D, b=.15))
    o.append(cube("TableTop", (0, 0, .39), (29.8, 26.6, .18), WOOD, b=.07))

    board_w = 29.2 / 12
    for i in range(12):
        x = -14.6 + board_w * (i + .5)
        mat = (WOOD, WOOD_L, WOOD)[i % 3]
        o.append(cube(f"TopBoard_{i}", (x, 0, .51), (board_w - .045, 26.0, .07), mat, b=.015))

    cy = 1.95
    w = 23.15
    d = 18.55
    o.append(cube("BoardWell", (0, cy, .64), (w, d, .16), FELT, b=.08))

    for y in (cy - d / 2, cy + d / 2):
        o.append(cube(f"BoardRailY_{y}", (0, y, .82), (w + .48, .46, .31), WOOD_L, b=.045))
    for x in (-w / 2, w / 2):
        o.append(cube(f"BoardRailX_{x}", (x, cy, .82), (.46, d + .48, .31), WOOD_L, b=.045))

    for y in (-13.05, 13.05):
        o.append(cube(f"OuterRailY_{y}", (0, y, .66), (29.55, .74, .42), WOOD_D, b=.060))
        o.append(cube(f"BronzeInlayY_{y}", (0, y, .90), (25.8, .075, .055), BRONZE, b=.008))
    for x in (-14.28, 14.28):
        o.append(cube(f"OuterRailX_{x}", (x, 0, .66), (.74, 25.75, .42), WOOD_D, b=.060))

    for i, (x, y) in enumerate(((-14.0, -12.8), (14.0, -12.8), (-14.0, 12.8), (14.0, 12.8))):
        o.append(cube(f"CornerPlate_{i}", (x, y, .94), (.78, .78, .08), IRON, b=.035))
        o.append(ico(f"CornerRivet_{i}", (x, y, 1.02), (.08, .08, .045), BRONZE, sub=1))

    export_asset(o, "war_table_hero")


# -----------------------------------------------------------------------------
# Tavern: asymmetrical and open behind the opponent. No central chandelier.
# -----------------------------------------------------------------------------
def build_tavern():
    clear_scene()
    o = []
    room_w = 38.0
    room_d = 38.0

    for i in range(18):
        x = -room_w / 2 + (room_w / 18) * (i + .5)
        mat = WOOD if i % 4 else WOOD_D
        o.append(cube(f"Floor_{i}", (x, -1.0, -.88), (room_w / 18 - .035, room_d, .24), mat, b=.016))

    for row in range(16):
        z = .45 + row * .94
        mat = WOOD if row % 3 else WOOD_D
        o.append(cube(f"BackBoard_{row}", (0, -19.0, z), (37.4, .40, .87), mat, b=.014))

    for row in range(15):
        z = .55 + row * .98
        o.append(cube(f"LeftWall_{row}", (-18.75, -1.0, z), (.40, 36.0, .90), WOOD_D if row % 3 == 0 else WOOD, b=.014))
        o.append(cube(f"RightWall_{row}", (18.75, -1.0, z), (.40, 36.0, .90), WOOD_D if row % 4 == 0 else WOOD, b=.014))

    for x in (-16.0, -11.0, 10.5, 15.5):
        o.append(cube(f"BackPost_{x}", (x, -18.72, 7.5), (.48, .58, 15.0), WOOD_D, b=.028))
    for z in (4.4, 10.8, 14.7):
        o.append(cube(f"BackBeam_{z}", (0, -18.64, z), (36.8, .58, .46), WOOD_D, b=.025))

    o.append(cube("NearSupport", (-10.7, -7.0, 7.3), (.72, .72, 14.6), WOOD_D, b=.035))

    for z in (2.2, 4.65, 7.1):
        o.append(cube(f"LeftShelf_{z}", (-11.5, -18.15, z), (8.0, 1.0, .20), WOOD_L, b=.016))
    for i in range(13):
        x = -14.8 + (i % 7) * 1.0
        z = 2.55 + (i // 7) * 2.45 + (i % 3) * .05
        if i == 5:
            o.append(ico("ShelfSkull", (x, -17.86, z + .22), (.30, .24, .28), BONE, sub=1))
        elif i % 4 == 0:
            o.append(cube(f"Book_{i}", (x, -17.90, z), (.54, .52, .17), RED if i % 8 else BLUE, rot=(0, 0, math.radians((i % 3 - 1) * 5)), b=.010))
        else:
            h = .52 + (i % 3) * .10
            o.append(cyl(f"Bottle_{i}", (x, -17.88, z + h * .45), .12, h, GRASS_D if i % 2 else STONE_D, verts=8, b=.005))
            o.append(cyl(f"BottleNeck_{i}", (x, -17.88, z + h + .04), .048, .22, STONE_D, verts=8, b=.003))

    o.append(cube("WeaponRail", (11.6, -18.12, 7.0), (9.1, .45, .22), WOOD_L, b=.018))
    for i, x in enumerate((8.2, 10.0, 12.0, 14.0)):
        o.append(beam(f"Spear_{i}", (x, -17.88, 4.3), (x + (-.35 if i % 2 else .35), -17.88, 9.2), .045, WOOD_L, 7))
        o.append(cone(f"SpearHead_{i}", (x + (-.35 if i % 2 else .35), -17.88, 9.45), .13, 0, .48, STEEL, verts=4))
    for i, x in enumerate((9.0, 13.3)):
        o.append(ico(f"Shield_{i}", (x, -17.88, 5.25), (.75, .15, .75), BLUE if i == 0 else RED, sub=2))
        o.append(ico(f"ShieldBoss_{i}", (x, -17.70, 5.25), (.16, .08, .16), STEEL, sub=1))

    for link in range(9):
        o.append(torus(f"LanternChain_{link}", (9.6, -17.0, 13.8 - link * .32), .10, .023, IRON, rot=(math.pi / 2 if link % 2 else 0, 0, 0), major_segments=8, minor_segments=4))
    o.append(cube("LanternFrame", (9.6, -17.0, 10.65), (.72, .62, 1.05), IRON, b=.020))
    o.append(ico("LanternFlame", (9.6, -17.0, 10.64), (.16, .14, .27), FIRE, sub=1))

    for i, (x, y) in enumerate(((-16.0, -10.5), (-15.0, -8.8), (15.7, -11.2))):
        o.append(cyl(f"Barrel_{i}", (x, y, .68), .68, 1.36, WOOD, verts=12, b=.016))
        for dz in (-.42, .42):
            o.append(torus(f"BarrelBand_{i}_{dz}", (x, y, .68 + dz), .66, .030, IRON, rot=(math.pi / 2, 0, 0), major_segments=12, minor_segments=4))

    export_asset(o, "tavern_room_hero")


# -----------------------------------------------------------------------------
# Battlefield: sculpted miniature terrain with coherent large patches.
# -----------------------------------------------------------------------------
def terrain_height(x, y):
    h = .12 * math.sin(x * .48) + .08 * math.cos(y * .60) + .05 * math.sin((x + y) * .88)
    h += .055 * math.sin(x * .21 - y * .33)
    river_x = -5.0 + .55 * math.sin(y * .50)
    d = abs(x - river_x)
    if d < 1.3:
        h -= .22 * (1.0 - d / 1.3)
    road_x = .18 * math.sin(y * .42)
    if abs(x - road_x) < 1.0:
        h *= .36
    return h


def ribbon(name, path, half_width, z, mat):
    verts = []
    faces = []
    for i, (x, y) in enumerate(path):
        if i == 0:
            dx = path[1][0] - x
            dy = path[1][1] - y
        else:
            dx = x - path[i - 1][0]
            dy = y - path[i - 1][1]
        length = max(.001, math.sqrt(dx * dx + dy * dy))
        nx = -dy / length
        ny = dx / length
        verts.append((x + nx * half_width, y + ny * half_width, z))
        verts.append((x - nx * half_width, y - ny * half_width, z))
    for i in range(len(path) - 1):
        a = i * 2
        faces.append((a, a + 1, a + 3, a + 2))
    return mesh_obj(name, verts, faces, [mat], [0] * len(faces))


def add_tree(o, name, x, y, z, scale, pine=False):
    o.append(cyl(name + "Trunk", (x, y, z + .55 * scale), .13 * scale, 1.10 * scale, WOOD_D, verts=7, b=.005))
    if pine:
        for i, (zz, radius) in enumerate(((1.0, .55), (1.40, .47), (1.76, .37))):
            o.append(cone(f"{name}Pine_{i}", (x, y, z + zz * scale), radius * scale, .05 * scale, .68 * scale, (GRASS_D, GRASS, GRASS_L)[i % 3], verts=7))
    else:
        for i, (dx, dy, dz, radius) in enumerate(((0, 0, 1.28, .52), (-.32, .02, 1.35, .34), (.34, .04, 1.38, .35), (.04, .26, 1.58, .32))):
            o.append(ico(f"{name}Leaf_{i}", (x + dx * scale, y + dy * scale, z + dz * scale), (radius * scale, radius * .86 * scale, radius * .70 * scale), (GRASS_D, GRASS, GRASS_L)[i % 3], sub=1, rot=(i * .12, i * .21, i * .16)))


def build_battlefield():
    clear_scene()
    o = []
    nx = 35
    ny = 29
    width = 22.0
    depth = 17.4
    verts = []

    for j in range(ny):
        y = -depth / 2 + depth * j / (ny - 1)
        for i in range(nx):
            x = -width / 2 + width * i / (nx - 1)
            verts.append((x, y, terrain_height(x, y)))

    faces = []
    face_mats = []
    mats = [GRASS, GRASS_D, GRASS_L, DIRT]
    for j in range(ny - 1):
        for i in range(nx - 1):
            a = j * nx + i
            faces.append((a, a + 1, a + 1 + nx, a + nx))
            cx = -width / 2 + width * (i + .5) / (nx - 1)
            cy = -depth / 2 + depth * (j + .5) / (ny - 1)
            road_x = .18 * math.sin(cy * .42)
            river_x = -5.0 + .55 * math.sin(cy * .50)
            if abs(cx - road_x) < 1.05:
                idx = 3
            elif abs(cx - river_x) < 1.25:
                idx = 1
            else:
                patch = math.sin(cx * .42) + .65 * math.cos(cy * .35) + .45 * math.sin((cx - cy) * .19)
                if patch > .85:
                    idx = 2
                elif patch < -.72:
                    idx = 1
                else:
                    idx = 0
            face_mats.append(idx)
    o.append(mesh_obj("SculptedGround", verts, faces, mats, face_mats))

    river_path = []
    road_path = []
    for k in range(27):
        y = -8.3 + k * (16.6 / 26)
        river_path.append((-5.0 + .55 * math.sin(y * .50), y))
        road_path.append((.18 * math.sin(y * .42), y))
    o.append(ribbon("River", river_path, .68, .025, WATER))
    o.append(ribbon("MainRoad", road_path, .60, .060, DIRT))
    o.append(ribbon("BranchRoad", [(0, -.3), (1.3, -1.2), (2.8, -2.1), (4.6, -3.0), (6.3, -3.55)], .36, .064, DIRT_D))

    rng = random.Random(2409)

    for i in range(26):
        y = -7.8 + i * (15.6 / 25)
        rx = -5.0 + .55 * math.sin(y * .50)
        side = -1 if i % 2 else 1
        x = rx + side * rng.uniform(.82, 1.18)
        o.append(ico(f"BankRock_{i}", (x, y, terrain_height(x, y) + .08), (rng.uniform(.10, .22), rng.uniform(.08, .18), rng.uniform(.06, .13)), STONE_D if i % 3 else STONE, sub=1, rot=(rng.random(), rng.random(), rng.random())))

    bridge_y = -.55
    rx = -5.0 + .55 * math.sin(bridge_y * .50)
    for i in range(9):
        x = rx - 1.30 + i * .325
        o.append(cube(f"BridgePlank_{i}", (x, bridge_y, .30), (.28, 1.90, .15), WOOD_L if i % 2 else WOOD, rot=(0, 0, math.radians((i - 4) * 1.3)), b=.012))

    tree_specs = (
        (-9.0, -4.6, .72, False), (-8.4, -3.5, .60, False), (-9.2, -2.1, .66, True),
        (-8.8, 2.6, .58, True), (-9.4, 4.0, .64, False), (8.8, -6.8, .68, False),
        (9.3, -5.3, .58, True), (8.5, 1.9, .60, False), (9.1, 3.5, .55, True),
        (7.8, 5.2, .50, False), (-7.5, -7.2, .50, True), (7.1, -1.0, .48, False),
    )
    for i, (x, y, s, pine) in enumerate(tree_specs):
        add_tree(o, f"Tree_{i}", x, y, terrain_height(x, y), s, pine)

    for i, (x, y, angle) in enumerate(((-7.4, -5.5, 16), (6.5, -1.8, -14), (7.4, -7.0, 25))):
        z = terrain_height(x, y)
        for block in range(3):
            o.append(cube(f"Ruin_{i}_{block}", (x + (block - 1) * .34, y, z + .22 + block * .06), (.42, .30, .42 + block * .12), STONE_D if block % 2 else STONE, rot=(0, 0, math.radians(angle + block * 4)), b=.018))

    for i in range(28):
        x = rng.uniform(-9.8, 9.8)
        y = rng.uniform(-7.8, 7.8)
        if abs(x) < 1.0 or abs(x - (-5.0 + .55 * math.sin(y * .50))) < 1.3:
            continue
        z = terrain_height(x, y)
        if i % 3 == 0:
            o.append(ico(f"Pebble_{i}", (x, y, z + .06), (rng.uniform(.07, .15), rng.uniform(.06, .12), rng.uniform(.04, .09)), STONE_D if i % 2 else STONE, sub=1))
        else:
            o.append(ico(f"GrassClump_{i}", (x, y, z + .06), (.17, .12, .08), GRASS_L if i % 2 else GRASS_D, sub=1))

    export_asset(o, "battlefield_terrain_hero")


# -----------------------------------------------------------------------------
# Fortress: broad, layered, readable and less cylindrical/toy-like.
# -----------------------------------------------------------------------------
def add_merlons(o, prefix, a, b, z, count, depth=.46):
    ax, ay = a
    bx, by = b
    angle = math.atan2(by - ay, bx - ax)
    for i in range(count):
        t = (i + .5) / count
        x = ax + (bx - ax) * t
        y = ay + (by - ay) * t
        o.append(cube(f"{prefix}_Merlon_{i}", (x, y, z), (.38, depth, .54), STONE_L if i % 3 == 0 else STONE, rot=(0, 0, angle), b=.016))


def wall(o, prefix, a, b, height=2.15, thick=.46):
    ax, ay = a
    bx, by = b
    mx = (ax + bx) * .5
    my = (ay + by) * .5
    length = math.hypot(bx - ax, by - ay)
    angle = math.atan2(by - ay, bx - ax)
    o.append(cube(prefix + "Core", (mx, my, height * .5), (length, thick, height), STONE, rot=(0, 0, angle), b=.030))
    o.append(cube(prefix + "Cap", (mx, my, height + .04), (length + .08, thick + .08, .16), STONE_D, rot=(0, 0, angle), b=.012))
    add_merlons(o, prefix, a, b, height + .34, max(3, int(length / .72)), depth=thick + .08)


def tower(o, prefix, x, y, radius, height, rear=False):
    o.append(cyl(prefix + "Core", (x, y, height * .5), radius, height, STONE_D if rear else STONE, verts=8, b=.035))
    o.append(cyl(prefix + "Crown", (x, y, height - .10), radius + .10, .25, STONE_L, verts=8, b=.018))
    for i in range(8):
        angle = math.tau * i / 8
        xx = x + math.cos(angle) * (radius - .04)
        yy = y + math.sin(angle) * (radius - .04)
        o.append(cube(f"{prefix}_Merlon_{i}", (xx, yy, height + .30), (.38, .46, .56), STONE, rot=(0, 0, angle), b=.016))
    for angle in (0, math.pi / 2, math.pi, math.pi * 1.5):
        xx = x + math.cos(angle) * (radius + .02)
        yy = y + math.sin(angle) * (radius + .02)
        o.append(cube(f"{prefix}_Slit_{int(angle * 100)}", (xx, yy, height * .55), (.07, .045, .38), BLACK, rot=(0, 0, angle), b=.002))


def build_castle():
    clear_scene()
    o = []

    tower(o, "FrontL", -3.55, -1.95, .94, 3.25)
    tower(o, "FrontR", 3.55, -1.95, .94, 3.25)
    tower(o, "RearL", -3.75, 1.72, .76, 2.82, rear=True)
    tower(o, "RearR", 3.75, 1.72, .76, 2.82, rear=True)

    wall(o, "LeftWall", (-3.55, -1.95), (-3.75, 1.72), 2.05, .48)
    wall(o, "RightWall", (3.55, -1.95), (3.75, 1.72), 2.05, .48)
    wall(o, "RearWall", (-3.75, 1.72), (3.75, 1.72), 1.95, .44)
    wall(o, "FrontLeft", (-3.55, -1.95), (-1.10, -1.95), 2.00, .48)
    wall(o, "FrontRight", (1.10, -1.95), (3.55, -1.95), 2.00, .48)

    wall(o, "WingL", (-4.10, -.75), (-5.95, -.50), 1.48, .40)
    wall(o, "WingR", (4.10, -.75), (5.95, -.48), 1.48, .40)
    tower(o, "WingTowerL", -6.05, -.46, .58, 1.95, rear=True)
    tower(o, "WingTowerR", 6.05, -.43, .58, 1.95, rear=True)

    o.append(cube("GatePierL", (-.76, -2.02, 1.28), (.76, .88, 2.56), STONE, b=.036))
    o.append(cube("GatePierR", (.76, -2.02, 1.28), (.76, .88, 2.56), STONE, b=.036))
    o.append(cube("GateTop", (0, -2.02, 2.72), (2.28, .90, .82), STONE_L, b=.034))
    o.append(cube("GateVoid", (0, -2.49, 1.12), (1.06, .06, 2.05), BLACK, b=.002))
    for i, x in enumerate((-.45, -.30, -.15, 0, .15, .30, .45)):
        o.append(cube(f"PortV_{i}", (x, -2.53, 1.12), (.030, .035, 1.94), IRON, b=.001))
    for i, z in enumerate((.48, .86, 1.24, 1.62, 2.0)):
        o.append(cube(f"PortH_{i}", (0, -2.53, z), (1.02, .035, .030), IRON, b=.001))
    add_merlons(o, "Gate", (-1.05, -2.02), (1.05, -2.02), 3.28, 5, depth=.76)

    o.append(cube("Keep", (0, .45, 2.05), (3.45, 2.70, 4.10), STONE_D, b=.052))
    o.append(cube("KeepFace", (0, -.93, 2.05), (3.22, .09, 3.92), STONE, b=.022))
    o.append(cube("KeepCap", (0, .45, 4.16), (3.72, 2.98, .22), STONE_L, b=.020))
    add_merlons(o, "KeepFront", (-1.52, -.92), (1.52, -.92), 4.55, 5, depth=.50)

    o.append(cyl("WatchTurret", (-.90, .40, 4.66), .50, 1.00, STONE, verts=8, b=.022))
    for i in range(7):
        a = math.tau * i / 7
        o.append(cube(f"WatchMerlon_{i}", (-.90 + math.cos(a) * .43, .40 + math.sin(a) * .43, 5.34), (.22, .30, .36), STONE_L, rot=(0, 0, a), b=.010))

    for i, (x, z) in enumerate(((-.82, 2.45), (.82, 2.45), (-.82, 3.30), (.82, 3.30))):
        o.append(cube(f"Window_{i}", (x, -1.00, z), (.18, .045, .38), BLACK, b=.002))
    for x in (-1.92, 1.92):
        o.append(cube(f"Buttress_{x}", (x, -1.28, 1.0), (.40, .64, 2.0), STONE_D, rot=(0, 0, math.radians(3 if x < 0 else -3)), b=.025))

    o.append(cube("Drawbridge", (0, -3.06, .16), (1.52, 2.05, .20), WOOD_L, rot=(math.radians(3), 0, 0), b=.020))
    for x in (-.54, .54):
        o.append(beam(f"BridgeChain_{x}", (x, -2.50, 2.30), (x, -3.58, .42), .026, IRON, 6))

    for i, (x, mat) in enumerate(((-1.16, BLUE), (1.16, RED))):
        o.append(cyl(f"BannerPole_{i}", (x, -2.48, 3.22), .025, 1.24, IRON, verts=7, b=.002))
        o.append(cube(f"Banner_{i}", (x, -2.52, 2.98), (.54, .045, .82), mat, b=.005))

    for i, x in enumerate((-.95, .95)):
        o.append(beam(f"Torch_{i}", (x, -2.48, 2.04), (x, -2.56, 2.42), .024, WOOD_D, 6))
        o.append(ico(f"Flame_{i}", (x, -2.60, 2.55), (.055, .050, .13), FIRE, sub=1))

    rng = random.Random(912)
    for i in range(15):
        x = rng.uniform(-5.8, 5.8)
        y = rng.uniform(-2.6, 2.0)
        if abs(x) < 1.25 and y < -1.3:
            continue
        s = rng.uniform(.08, .18)
        o.append(ico(f"Rubble_{i}", (x, y, .07), (s, s * .80, s * .62), STONE_D if i % 2 else STONE, sub=1, rot=(rng.random(), rng.random(), rng.random())))
    for i, (x, y, s) in enumerate(((-3.2, 1.35, .34), (2.9, 1.34, .28), (-5.6, -.25, .22), (5.55, -.18, .20))):
        o.append(ico(f"Moss_{i}", (x, y, .09), (s, s * .55, .05), MOSS, sub=1))

    export_asset(o, "castle_hero")


# -----------------------------------------------------------------------------
# Opponent: smaller seated proportions, readable face and hands on the table.
# -----------------------------------------------------------------------------
def build_opponent():
    clear_scene()
    o = []

    o.append(cube("ChairBack", (0, .95, 3.80), (2.70, .30, 5.35), WOOD_D, b=.065))
    o.append(cube("ChairSeat", (0, .28, 1.18), (2.85, 1.85, .26), WOOD, b=.045))

    o.append(beam("ThighL", (-.52, .10, 2.15), (-.70, -.65, 1.48), .29, CLOTH, 9))
    o.append(beam("ThighR", (.52, .10, 2.15), (.70, -.65, 1.48), .29, CLOTH, 9))

    o.append(cone("Torso", (0, -.34, 4.18), 1.28, .98, 2.70, TUNIC, verts=10, rot=(math.radians(7), 0, 0)))
    o.append(ico("Shoulders", (0, -.24, 5.17), (1.56, .68, .50), CLOTH, sub=2))
    cloak_verts = [
        (-1.46, -.48, 5.10), (-.26, -.82, 4.98), (-.35, -.68, 2.92), (-1.12, -.22, 2.60),
        (.26, -.82, 4.98), (1.46, -.48, 5.10), (1.12, -.22, 2.60), (.35, -.68, 2.92),
    ]
    o.append(mesh_obj("CloakPanels", cloak_verts, [(0, 1, 2, 3), (4, 5, 6, 7)], [CLOTH], [0, 0]))
    o.append(torus("Collar", (0, -.28, 5.47), .57, .13, CLOTH, rot=(math.pi / 2, 0, 0), major_segments=12, minor_segments=5))
    o.append(cube("Belt", (0, -.46, 3.12), (1.88, .54, .16), LEATHER, b=.018))
    o.append(cube("Buckle", (0, -.75, 3.12), (.27, .08, .24), BRONZE, b=.010))
    o.append(beam("StrapL", (-.66, -.75, 5.05), (.34, -.68, 3.45), .060, LEATHER_L, 7))
    o.append(beam("StrapR", (.68, -.74, 5.05), (-.34, -.67, 3.45), .060, LEATHER, 7))

    o.append(cyl("Neck", (0, -.42, 5.63), .30, .46, SKIN_S, verts=9, b=.010))
    o.append(ico("Head", (0, -.58, 6.38), (.80, .69, .90), SKIN, sub=2))
    o.append(ico("Jaw", (0, -.68, 5.98), (.58, .55, .42), SKIN_S, sub=1))
    o.append(ico("Nose", (0, -1.20, 6.40), (.12, .15, .20), SKIN, sub=1))
    o.append(ico("EarL", (-.77, -.55, 6.32), (.15, .10, .21), SKIN_S, sub=1))
    o.append(ico("EarR", (.77, -.55, 6.32), (.15, .10, .21), SKIN_S, sub=1))

    for side, x in (("L", -.27), ("R", .27)):
        o.append(ico(f"EyeWhite_{side}", (x, -1.13, 6.58), (.085, .040, .060), BONE, sub=1))
        o.append(ico(f"Iris_{side}", (x, -1.17, 6.58), (.038, .020, .038), BLACK, sub=1))
        o.append(cube(f"Brow_{side}", (x, -1.13, 6.78), (.31, .050, .060), HAIR, rot=(0, 0, math.radians(-10 if side == "L" else 10)), b=.004))

    o.append(ico("HairCrown", (0, -.48, 7.02), (.84, .72, .50), HAIR, sub=2))
    locks = (
        (-.58, -.77, 6.95, .30, -.18), (.58, -.77, 6.95, .30, .18),
        (-.72, -.42, 6.70, .27, -.10), (.72, -.42, 6.70, .27, .10),
        (-.42, -.18, 6.94, .29, -.12), (.42, -.18, 6.94, .29, .12),
        (-.14, -.92, 7.10, .24, -.05), (.14, -.92, 7.10, .24, .05),
    )
    for i, (x, y, z, s, rz) in enumerate(locks):
        o.append(ico(f"HairLock_{i}", (x, y, z), (s, s * .72, s * .46), HAIR_L if i in (0, 4, 6) else HAIR, sub=1, rot=(i * .08, i * .05, rz)))

    o.append(ico("BeardChin", (0, -1.00, 5.83), (.43, .18, .42), HAIR, sub=1))
    o.append(ico("BeardL", (-.30, -.99, 6.03), (.27, .16, .34), HAIR_L, sub=1, rot=(0, 0, -.10)))
    o.append(ico("BeardR", (.30, -.99, 6.03), (.27, .16, .34), HAIR, sub=1, rot=(0, 0, .10)))
    o.append(cube("MustacheL", (-.16, -1.18, 6.14), (.26, .045, .070), HAIR, rot=(0, 0, math.radians(-10)), b=.003))
    o.append(cube("MustacheR", (.16, -1.18, 6.14), (.26, .045, .070), HAIR, rot=(0, 0, math.radians(10)), b=.003))

    shoulder_l = (-1.28, -.35, 4.93)
    elbow_l = (-1.82, -.92, 3.95)
    wrist_l = (-1.72, -1.92, 2.72)
    shoulder_r = (1.28, -.35, 4.93)
    elbow_r = (1.82, -.92, 3.95)
    wrist_r = (1.72, -1.92, 2.72)
    o.append(beam("UpperArmL", shoulder_l, elbow_l, .27, CLOTH, 9))
    o.append(beam("UpperArmR", shoulder_r, elbow_r, .27, CLOTH, 9))
    o.append(beam("ForearmL", elbow_l, wrist_l, .225, SKIN, 9))
    o.append(beam("ForearmR", elbow_r, wrist_r, .225, SKIN, 9))
    o.append(cyl("BracerL", (-1.78, -1.42, 3.30), .23, .62, LEATHER, verts=8, rot=(math.radians(66), 0, math.radians(-6)), b=.008))
    o.append(cyl("BracerR", (1.78, -1.42, 3.30), .23, .62, LEATHER, verts=8, rot=(math.radians(66), 0, math.radians(6)), b=.008))
    o.append(ico("HandL", wrist_l, (.34, .28, .34), SKIN, sub=2, rot=(.12, 0, -.08)))
    o.append(ico("HandR", wrist_r, (.34, .28, .34), SKIN, sub=2, rot=(.12, 0, .08)))

    for hand_idx, (wx, wy, wz, sign) in enumerate(((*wrist_l, -1), (*wrist_r, 1))):
        for finger in range(4):
            x = wx + sign * (finger - 1.5) * .060
            o.append(beam(f"Finger_{hand_idx}_{finger}", (x, wy - .10, wz - .05), (x + sign * .015, wy - .30, wz - .08), .024, SKIN, 6))

    o.append(ico("Brooch", (0, -.86, 5.25), (.18, .060, .18), BRONZE, sub=1))
    o.append(beam("PendantChain", (0, -.81, 5.10), (0, -.84, 4.58), .016, BRONZE, 6))
    o.append(ico("Pendant", (0, -.86, 4.47), (.11, .05, .15), BRONZE, sub=1))

    export_asset(o, "opponent_hero")


jobs = [build_table, build_tavern, build_battlefield, build_castle, build_opponent]
print("\n[CastleCards Reference V2] Generating target-quality scene assets...\n")
for fn in jobs:
    print(f"[CastleCards Reference V2] {fn.__name__}")
    fn()
print(f"\n[CastleCards Reference V2] Complete: {len(jobs)} assets regenerated.\n")
