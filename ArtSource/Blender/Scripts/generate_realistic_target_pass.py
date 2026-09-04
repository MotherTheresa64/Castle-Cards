import bpy
import math
import random
from pathlib import Path
from mathutils import Vector

ROOT = Path(__file__).resolve().parents[3]
HERO = ROOT / "Models" / "Hero"
TERRAIN = ROOT / "Models" / "Terrain" / "Medieval"
UNITS = ROOT / "Models" / "Units" / "Human"
SIEGE = ROOT / "Models" / "Siege" / "Medieval"
for p in (HERO, TERRAIN, UNITS, SIEGE):
    p.mkdir(parents=True, exist_ok=True)

RNG = random.Random(271828)


def mat(name, color, rough=.8, metal=0.0):
    m = bpy.data.materials.get(name)
    if m is None:
        m = bpy.data.materials.new(name)
    m.use_nodes = True
    bsdf = m.node_tree.nodes.get("Principled BSDF")
    if bsdf:
        bsdf.inputs["Base Color"].default_value = (*color, 1.0)
        bsdf.inputs["Roughness"].default_value = rough
        bsdf.inputs["Metallic"].default_value = metal
    return m


STONE = mat("R_Stone", (.245, .235, .220), .91)
STONE2 = mat("R_Stone2", (.315, .300, .275), .90)
STONE3 = mat("R_Stone3", (.185, .185, .180), .94)
MORTAR = mat("R_Mortar", (.105, .102, .095), .97)
WOOD = mat("R_Wood", (.115, .044, .018), .82)
WOOD2 = mat("R_Wood2", (.205, .083, .028), .78)
WOOD3 = mat("R_Wood3", (.055, .022, .010), .88)
IRON = mat("R_Iron", (.055, .060, .066), .35, .82)
STEEL = mat("R_Steel", (.260, .285, .305), .32, .72)
BRONZE = mat("R_Bronze", (.330, .160, .040), .42, .62)
BLUE = mat("R_Blue", (.035, .075, .230), .88)
BLUE2 = mat("R_Blue2", (.055, .145, .365), .84)
RED = mat("R_Red", (.285, .030, .018), .88)
RED2 = mat("R_Red2", (.435, .060, .025), .84)
LEATHER = mat("R_Leather", (.105, .035, .014), .84)
LEATHER2 = mat("R_Leather2", (.205, .075, .025), .80)
CLOTH = mat("R_Cloth", (.025, .026, .032), .96)
CLOTH2 = mat("R_Cloth2", (.055, .052, .060), .95)
SKIN = mat("R_Skin", (.55, .30, .18), .72)
SKIN2 = mat("R_Skin2", (.38, .18, .105), .78)
HAIR = mat("R_Hair", (.030, .012, .007), .88)
HAIR2 = mat("R_Hair2", (.075, .027, .011), .86)
WHITE = mat("R_White", (.68, .63, .55), .62)
EYE = mat("R_Eye", (.018, .012, .008), .44)
GRASS = mat("R_Grass", (.115, .205, .080), .96)
GRASS2 = mat("R_Grass2", (.165, .250, .105), .96)
GRASS3 = mat("R_Grass3", (.080, .145, .060), .97)
DIRT = mat("R_Dirt", (.235, .150, .078), .98)
DIRT2 = mat("R_Dirt2", (.155, .090, .045), .98)
WATER = mat("R_Water", (.035, .170, .230), .18, .0)
WATER2 = mat("R_Water2", (.055, .255, .320), .15, .0)
LEAF = mat("R_Leaf", (.055, .165, .060), .95)
LEAF2 = mat("R_Leaf2", (.090, .225, .075), .94)
LEAF3 = mat("R_Leaf3", (.040, .105, .045), .97)
PARCHMENT = mat("R_Parchment", (.38, .24, .115), .89)
FIRE = mat("R_Fire", (1.0, .18, .015), .12)


def clear():
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)


def add_mat(obj, material):
    if hasattr(obj.data, "materials"):
        obj.data.materials.append(material)


def smooth(obj):
    if hasattr(obj.data, "polygons"):
        for p in obj.data.polygons:
            p.use_smooth = True


def flat(obj):
    if hasattr(obj.data, "polygons"):
        for p in obj.data.polygons:
            p.use_smooth = False


def bevel(obj, width=.035, segments=2):
    if width <= 0:
        return obj
    bpy.context.view_layer.objects.active = obj
    obj.select_set(True)
    mod = obj.modifiers.new("RealisticBevel", "BEVEL")
    mod.width = width
    mod.segments = segments
    try:
        mod.affect = 'EDGES'
    except Exception:
        pass
    try:
        bpy.ops.object.modifier_apply(modifier=mod.name)
    except Exception:
        pass
    return obj


def cube(name, loc, dims, material, rot=(0, 0, 0), b=.04, seg=2):
    bpy.ops.mesh.primitive_cube_add(location=loc, rotation=rot)
    o = bpy.context.object
    o.name = name
    o.dimensions = dims
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    add_mat(o, material)
    bevel(o, b, seg)
    return o


def cyl(name, loc, radius, depth, material, verts=24, rot=(0, 0, 0), b=.02, do_smooth=False):
    bpy.ops.mesh.primitive_cylinder_add(vertices=verts, radius=radius, depth=depth, location=loc, rotation=rot)
    o = bpy.context.object
    o.name = name
    add_mat(o, material)
    bevel(o, b, 2)
    if do_smooth:
        smooth(o)
    return o


def cone(name, loc, r1, r2, depth, material, verts=24, rot=(0, 0, 0), do_smooth=False):
    bpy.ops.mesh.primitive_cone_add(vertices=verts, radius1=r1, radius2=r2, depth=depth, location=loc, rotation=rot)
    o = bpy.context.object
    o.name = name
    add_mat(o, material)
    if do_smooth:
        smooth(o)
    return o


def sphere(name, loc, scale, material, seg=28, rings=18, do_smooth=True):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=seg, ring_count=rings, radius=1.0, location=loc)
    o = bpy.context.object
    o.name = name
    o.scale = scale
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    add_mat(o, material)
    if do_smooth:
        smooth(o)
    return o


def ico(name, loc, scale, material, sub=2):
    bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=sub, radius=1.0, location=loc)
    o = bpy.context.object
    o.name = name
    o.scale = scale
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    add_mat(o, material)
    flat(o)
    return o


def beam(name, a, b, radius, material, verts=16):
    a = Vector(a)
    b = Vector(b)
    d = b - a
    mid = (a + b) * .5
    bpy.ops.mesh.primitive_cylinder_add(vertices=verts, radius=radius, depth=d.length, location=mid)
    o = bpy.context.object
    o.name = name
    o.rotation_mode = 'QUATERNION'
    o.rotation_quaternion = Vector((0, 0, 1)).rotation_difference(d.normalized())
    add_mat(o, material)
    bevel(o, radius * .12, 2)
    smooth(o)
    return o


def torus(name, loc, major, minor, material, rot=(0, 0, 0), major_segments=28, minor_segments=8):
    bpy.ops.mesh.primitive_torus_add(major_radius=major, minor_radius=minor, major_segments=major_segments,
                                    minor_segments=minor_segments, location=loc, rotation=rot)
    o = bpy.context.object
    o.name = name
    add_mat(o, material)
    smooth(o)
    return o


def export(path):
    path.parent.mkdir(parents=True, exist_ok=True)
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.export_scene.gltf(filepath=str(path), export_format='GLB', use_selection=True,
                              export_materials='EXPORT', export_normals=True, export_animations=False,
                              export_yup=True)
    print(f"[CastleCards Realistic] Exported {path.relative_to(ROOT)}")


def stone_block(name, x, y, z, sx, sy, sz, seed_offset=0):
    mats = (STONE, STONE2, STONE3)
    material = mats[(seed_offset + int(abs(x * 3 + z * 5))) % len(mats)]
    jitter = .015 * ((seed_offset % 3) - 1)
    return cube(name, (x + jitter, y, z), (sx, sy, sz), material, b=.022, seg=2)


def battlements(prefix, y, z, xs, depth=.72, width=.52):
    for i, x in enumerate(xs):
        stone_block(f"{prefix}_Merlon_{i}", x, y, z, width, depth, .52, i)


def tower(prefix, x, y, radius=1.25, height=3.2, team=None):
    cyl(f"{prefix}_Core", (x, y, height * .5), radius, height, STONE, verts=32, b=.035, do_smooth=False)
    cyl(f"{prefix}_BaseBand", (x, y, .32), radius * 1.07, .34, STONE3, verts=32, b=.02)
    cyl(f"{prefix}_TopBand", (x, y, height - .28), radius * 1.06, .28, STONE2, verts=32, b=.018)
    for ring in range(3):
        z = .72 + ring * .86
        for a in range(12):
            angle = math.tau * a / 12.0 + (ring % 2) * .11
            bx = x + math.cos(angle) * (radius + .015)
            by = y + math.sin(angle) * (radius + .015)
            stone_block(f"{prefix}_Stone_{ring}_{a}", bx, by, z, .44, .16, .34, ring + a)
    for a in range(10):
        angle = math.tau * a / 10.0
        bx = x + math.cos(angle) * radius * .83
        by = y + math.sin(angle) * radius * .83
        stone_block(f"{prefix}_Batt_{a}", bx, by, height + .20, .42, .42, .54, a)
    for side in (-1, 1):
        cube(f"{prefix}_Slit_{side}", (x + side * .45, y - radius - .025, height * .55), (.10, .025, .62), MORTAR, b=.006)
    if team is not None:
        banner = BLUE if team == "blue" else RED
        cube(f"{prefix}_Banner", (x, y - radius - .08, height * .73), (.54, .055, .95), banner, b=.012)


def wall_segment(prefix, x1, x2, y, height=2.15, depth=.70):
    width = abs(x2 - x1)
    cx = (x1 + x2) * .5
    cube(f"{prefix}_Mass", (cx, y, height * .5), (width, depth, height), MORTAR, b=.025)
    rows = 6
    block_h = height / rows
    for row in range(rows):
        z = block_h * (.5 + row)
        block_w = .72
        count = max(1, int(width / block_w))
        offset = (row % 2) * block_w * .5
        for i in range(count + 1):
            x = x1 + i * block_w + offset
            if x > x2 - .08:
                continue
            bw = min(block_w - .035, x2 - x)
            stone_block(f"{prefix}_Block_{row}_{i}", x + bw * .5, y - depth * .51, z, bw, .18, block_h - .035, row + i)
    xs = []
    step = .82
    x = x1 + .25
    while x < x2 - .15:
        xs.append(x)
        x += step
    battlements(prefix, y, height + .28, xs, depth=.64, width=.48)


def build_castle(team):
    clear()
    accent = BLUE if team == "blue" else RED
    accent2 = BLUE2 if team == "blue" else RED2

    # Wide, grounded fortress matching the reference rather than a fairy-tale tower.
    wall_segment(f"{team}_WallL", -4.9, -1.15, -1.65, 2.22, .76)
    wall_segment(f"{team}_WallR", 1.15, 4.9, -1.65, 2.22, .76)
    tower(f"{team}_TowerL", -5.05, -1.52, 1.30, 3.25, team)
    tower(f"{team}_TowerR", 5.05, -1.52, 1.30, 3.25, team)
    tower(f"{team}_InnerL", -2.55, .18, 1.05, 3.05, team)
    tower(f"{team}_InnerR", 2.55, .18, 1.05, 3.05, team)

    # Gatehouse and recessed keep.
    cube(f"{team}_Gatehouse", (0, -1.42, 1.58), (2.65, 1.18, 3.16), STONE, b=.055, seg=3)
    for row in range(7):
        for col in range(4):
            x = -1.05 + col * .70 + (row % 2) * .18
            if x > 1.08:
                continue
            stone_block(f"{team}_GateStone_{row}_{col}", x, -2.02, .34 + row * .40, .63, .17, .36, row + col)
    cube(f"{team}_GateDark", (0, -2.045, .78), (1.06, .06, 1.45), WOOD3, b=.10, seg=3)
    torus(f"{team}_GateArch", (0, -2.09, 1.36), .58, .10, STONE2, rot=(math.pi / 2, 0, 0), major_segments=28, minor_segments=8)
    for i, x in enumerate((-1.02, 1.02)):
        cube(f"{team}_GateButtress_{i}", (x, -1.96, 1.02), (.42, .55, 2.04), STONE3, b=.035)
    battlements(f"{team}_Gate", -1.50, 3.34, [-1.05, -.35, .35, 1.05], depth=.82, width=.46)

    cube(f"{team}_Keep", (0, .95, 2.22), (3.65, 2.40, 4.44), STONE3, b=.07, seg=3)
    cube(f"{team}_KeepFace", (0, -.29, 2.30), (3.28, .18, 3.90), STONE, b=.035)
    for floor in range(3):
        for side in (-1, 1):
            cube(f"{team}_KeepWindow_{floor}_{side}", (side * .86, -.40, 1.25 + floor * .88), (.18, .035, .54), MORTAR, b=.02)
    battlements(f"{team}_KeepBatt", .80, 4.72, [-1.45, -.78, 0, .78, 1.45], depth=.72, width=.46)

    # Side curtain walls angle back into the keep.
    for side in (-1, 1):
        x = side * 3.82
        cube(f"{team}_SideWall_{side}", (x, -.14, 1.10), (2.55, .70, 2.20), STONE, rot=(0, 0, math.radians(22 * side)), b=.045)
        cube(f"{team}_SideBanner_{side}", (side * 3.15, -.63, 1.72), (.50, .05, .95), accent, b=.01)

    # Torches, metal gate braces, flags.
    for i, x in enumerate((-4.30, -1.30, 1.30, 4.30)):
        cyl(f"{team}_TorchPole_{i}", (x, -2.08, 2.38), .035, .56, IRON, verts=12, b=.006)
        sphere(f"{team}_Flame_{i}", (x, -2.08, 2.72), (.09, .07, .18), FIRE, seg=16, rings=10)
    for y in (.56, .94, 1.32):
        cube(f"{team}_GateBrace_{y}", (0, -2.09, y), (1.02, .055, .07), IRON, b=.01)
    cube(f"{team}_GateBanner", (0, -2.14, 2.36), (.72, .045, 1.08), accent2, b=.015)

    export(HERO / f"castle_{team}_hero.glb")


def terrain_height(x, y):
    base = .15 * math.sin(x * .44) + .11 * math.cos(y * .39) + .055 * math.sin((x + y) * .91)
    edge = .06 * math.cos(x * .18 - y * .12)
    return base + edge


def make_terrain_mesh():
    nx, ny = 51, 43
    xmin, xmax = -10.7, 10.7
    ymin, ymax = -8.9, 8.9
    verts = []
    faces = []
    for iy in range(ny):
        y = ymin + (ymax - ymin) * iy / (ny - 1)
        for ix in range(nx):
            x = xmin + (xmax - xmin) * ix / (nx - 1)
            h = terrain_height(x, y)
            verts.append((x, y, h))
    for iy in range(ny - 1):
        for ix in range(nx - 1):
            a = iy * nx + ix
            faces.append((a, a + 1, a + nx + 1, a + nx))
    mesh = bpy.data.meshes.new("RealisticBattlefieldMesh")
    mesh.from_pydata(verts, [], faces)
    mesh.materials.append(GRASS)
    mesh.materials.append(GRASS2)
    mesh.materials.append(GRASS3)
    mesh.materials.append(DIRT)
    obj = bpy.data.objects.new("RealisticBattlefield", mesh)
    bpy.context.collection.objects.link(obj)
    for p in mesh.polygons:
        cx = sum(mesh.vertices[i].co.x for i in p.vertices) / len(p.vertices)
        cy = sum(mesh.vertices[i].co.y for i in p.vertices) / len(p.vertices)
        n = math.sin(cx * 1.7 + cy * .8) + math.cos(cy * 1.2 - cx * .5)
        if abs(cx) < 1.1:
            p.material_index = 3
        elif n > .9:
            p.material_index = 1
        elif n < -.9:
            p.material_index = 2
        else:
            p.material_index = 0
        p.use_smooth = True
    bevel(obj, .015, 1)
    return obj


def ribbon(name, points, width, material, z=.16):
    verts = []
    faces = []
    for i, (x, y) in enumerate(points):
        if i == 0:
            dx, dy = points[1][0] - x, points[1][1] - y
        elif i == len(points) - 1:
            dx, dy = x - points[i - 1][0], y - points[i - 1][1]
        else:
            dx, dy = points[i + 1][0] - points[i - 1][0], points[i + 1][1] - points[i - 1][1]
        length = max(.001, math.hypot(dx, dy))
        nx, ny = -dy / length, dx / length
        verts.append((x + nx * width * .5, y + ny * width * .5, z))
        verts.append((x - nx * width * .5, y - ny * width * .5, z))
    for i in range(len(points) - 1):
        a = i * 2
        faces.append((a, a + 1, a + 3, a + 2))
    mesh = bpy.data.meshes.new(name + "Mesh")
    mesh.from_pydata(verts, [], faces)
    mesh.materials.append(material)
    obj = bpy.data.objects.new(name, mesh)
    bpy.context.collection.objects.link(obj)
    for p in mesh.polygons:
        p.use_smooth = True
    return obj


def make_tree(prefix, x, y, s=1.0, pine=True):
    z = terrain_height(x, y)
    cyl(prefix + "_Trunk", (x, y, z + .70 * s), .16 * s, 1.40 * s, WOOD3, verts=16, b=.018, do_smooth=True)
    if pine:
        for i, (rz, rr) in enumerate(((1.20, .92), (1.72, .72), (2.18, .52))):
            cone(prefix + f"_Needles_{i}", (x, y, z + rz * s), rr * s, .08 * s, 1.05 * s,
                 (LEAF, LEAF2, LEAF3)[i % 3], verts=20, do_smooth=True)
    else:
        sphere(prefix + "_CrownA", (x - .22 * s, y, z + 1.72 * s), (.75 * s, .60 * s, .72 * s), LEAF, seg=20, rings=14)
        sphere(prefix + "_CrownB", (x + .32 * s, y + .08 * s, z + 1.82 * s), (.66 * s, .58 * s, .67 * s), LEAF2, seg=20, rings=14)
        sphere(prefix + "_CrownC", (x, y - .28 * s, z + 2.08 * s), (.57 * s, .50 * s, .55 * s), LEAF3, seg=20, rings=14)


def make_rock(prefix, x, y, s=1.0):
    z = terrain_height(x, y)
    for i in range(3):
        ox = (i - 1) * .38 * s + RNG.uniform(-.08, .08)
        oy = RNG.uniform(-.25, .25) * s
        ico(prefix + f"_{i}", (x + ox, y + oy, z + .24 * s), (.50 * s, .42 * s, .38 * s), (STONE3, STONE, STONE2)[i], sub=2)


def build_battlefield():
    clear()
    make_terrain_mesh()

    river_points = []
    for i in range(33):
        x = -10.8 + i * (21.6 / 32)
        y = .55 * math.sin(x * .46) + .18 * math.sin(x * 1.1)
        river_points.append((x, y))
    ribbon("River", river_points, 1.28, WATER, .19)
    ribbon("RiverHighlight", [(x, y - .12) for x, y in river_points], .36, WATER2, .205)

    road_points = []
    for i in range(25):
        y = -8.5 + i * (17.0 / 24)
        x = .35 * math.sin(y * .38)
        road_points.append((x, y))
    ribbon("MainRoad", road_points, 1.05, DIRT, .22)
    ribbon("RoadCenter", [(x + .08, y) for x, y in road_points], .24, DIRT2, .228)

    # Stone bridge across the river.
    cube("BridgeDeck", (0, .02, .50), (2.20, 2.15, .28), STONE2, b=.08, seg=3)
    for i in range(7):
        cube(f"BridgePlank_{i}", (-.90 + i * .30, -.02, .68), (.24, 2.00, .10), STONE, b=.025)
    for side in (-1, 1):
        cube(f"BridgeRail_{side}", (side * 1.02, .02, .82), (.14, 2.05, .36), STONE3, b=.035)

    # Dense but lane-aware forest framing like the reference.
    tree_spots = [
        (-9.3,-6.7),(-8.4,-6.2),(-7.5,-7.4),(-9.2,-4.7),(-8.0,-3.8),(-9.5,-1.8),
        (-8.8,2.0),(-7.7,2.8),(-9.2,4.4),(-8.1,5.4),(-7.1,6.6),(-9.5,7.2),
        (9.3,-6.7),(8.4,-6.2),(7.5,-7.4),(9.2,-4.7),(8.0,-3.8),(9.5,-1.8),
        (8.8,2.0),(7.7,2.8),(9.2,4.4),(8.1,5.4),(7.1,6.6),(9.5,7.2),
        (-6.4,-5.8),(-6.9,4.8),(6.4,-5.8),(6.9,4.8)
    ]
    for i, (x, y) in enumerate(tree_spots):
        make_tree(f"Tree_{i}", x, y, .68 + (i % 4) * .07, pine=(i % 3 != 0))

    rock_spots = [(-7.2,-1.9),(-6.5,1.3),(-5.9,5.7),(-7.2,7.1),(7.0,-2.1),(6.4,1.4),(5.8,5.8),(7.2,7.0),(-4.8,-6.8),(4.9,-6.7)]
    for i, (x, y) in enumerate(rock_spots):
        make_rock(f"Rock_{i}", x, y, .72 + (i % 3) * .08)

    export(HERO / "battlefield_terrain_hero.glb")


def build_tree_asset(name, pine=True):
    clear()
    make_tree(name, 0, 0, 1.0, pine=pine)
    export(TERRAIN / f"{name}.glb")


def build_rock_asset():
    clear()
    make_rock("RockCluster", 0, 0, 1.0)
    export(TERRAIN / "rock_cluster.glb")


def miniature_base():
    cyl("Base", (0, 0, .10), .72, .20, IRON, verts=32, b=.025, do_smooth=True)
    cyl("BaseTop", (0, 0, .22), .65, .10, STONE3, verts=32, b=.02, do_smooth=True)
    torus("BaseRim", (0, 0, .25), .59, .035, BRONZE)


def miniature_body(team_mat, cape=True, hood=False):
    for side in (-1, 1):
        x = side * .19
        cyl(f"Leg_{side}", (x, 0, .76), .115, .72, CLOTH, verts=16, b=.012, do_smooth=True)
        cube(f"Boot_{side}", (x, -.06, .39), (.25, .34, .22), LEATHER, b=.025, seg=2)
    cone("Torso", (0, 0, 1.48), .46, .34, 1.02, team_mat, verts=20, do_smooth=True)
    sphere("Shoulders", (0, 0, 1.92), (.54, .38, .30), team_mat, seg=22, rings=14)
    cube("Belt", (0, -.02, 1.27), (.78, .48, .11), LEATHER, b=.018)
    cube("Buckle", (0, -.27, 1.27), (.14, .06, .14), BRONZE, b=.008)
    if cape:
        cone("Cape", (0, .20, 1.45), .43, .26, 1.18, team_mat, verts=20, rot=(math.radians(-7), 0, 0), do_smooth=True)
    sphere("Head", (0, -.02, 2.36), (.29, .27, .34), SKIN, seg=24, rings=16)
    if hood:
        sphere("Hood", (0, .02, 2.46), (.37, .35, .42), LEATHER2, seg=22, rings=14)
        sphere("Face", (0, -.30, 2.37), (.22, .07, .23), SKIN, seg=20, rings=12)
    else:
        sphere("Helmet", (0, .01, 2.54), (.35, .33, .28), STEEL, seg=24, rings=14)
        cyl("HelmetBand", (0, 0, 2.47), .345, .08, IRON, verts=24, b=.01, do_smooth=True)


def build_unit(kind, hero_path, standard_path=None):
    clear()
    miniature_base()
    if kind == "archer":
        miniature_body(LEATHER2, cape=False, hood=True)
        beam("ArmL", (-.40,-.02,1.78), (-.69,-.14,1.92), .095, LEATHER2)
        beam("ArmR", (.40,-.02,1.82), (.66,-.12,2.00), .095, LEATHER2)
        beam("BowA", (-.72,-.16,2.00), (-.88,-.12,2.76), .026, WOOD2, 10)
        beam("BowB", (-.72,-.16,2.00), (-.86,-.12,1.18), .026, WOOD2, 10)
        beam("StringA", (-.88,-.12,2.76), (-.70,-.19,1.98), .010, WHITE, 6)
        beam("StringB", (-.70,-.19,1.98), (-.86,-.12,1.18), .010, WHITE, 6)
        cyl("Quiver", (.34,.28,1.52), .14, .84, LEATHER, verts=16, rot=(math.radians(8),0,math.radians(-18)), b=.008)
    elif kind == "swordsman":
        miniature_body(BLUE, cape=True, hood=False)
        beam("ArmL", (-.42,-.02,1.78), (-.63,-.16,1.50), .10, BLUE)
        beam("ArmR", (.42,-.02,1.84), (.66,-.12,1.72), .10, BLUE)
        cyl("Shield", (-.67,-.23,1.50), .55, .11, BLUE2, verts=28, rot=(math.pi/2,0,0), b=.012)
        torus("ShieldRim", (-.67,-.30,1.50), .50, .035, IRON, rot=(math.pi/2,0,0))
        cube("SwordBlade", (.82,-.10,2.26), (.09,.045,1.30), STEEL, rot=(0,0,math.radians(-18)), b=.006)
        cube("SwordGuard", (.61,-.10,1.72), (.44,.07,.08), BRONZE, rot=(0,0,math.radians(-18)), b=.006)
    else:
        miniature_body(BLUE, cape=True, hood=False)
        beam("ArmL", (-.42,-.02,1.78), (-.63,-.16,1.50), .10, BLUE)
        beam("ArmR", (.42,-.02,1.84), (.66,-.12,1.66), .10, BLUE)
        cyl("Shield", (-.67,-.23,1.50), .55, .11, BLUE2, verts=28, rot=(math.pi/2,0,0), b=.012)
        torus("ShieldRim", (-.67,-.30,1.50), .50, .035, IRON, rot=(math.pi/2,0,0))
        beam("Spear", (.66,-.10,.74), (.78,-.12,3.50), .032, WOOD2, 12)
        cone("SpearHead", (.80,-.13,3.72), .11, 0, .38, STEEL, verts=12, do_smooth=True)
    export(hero_path)
    if standard_path is not None:
        # Same high-detail miniature is also used by the fallback path.
        export(standard_path)


def build_special_unit(kind, path):
    clear()
    miniature_base()
    if kind == "wizard":
        miniature_body(CLOTH2, cape=True, hood=True)
        beam("Staff", (.52,-.08,.66), (.70,-.10,3.18), .035, WOOD2, 12)
        sphere("StaffGem", (.72,-.10,3.36), (.14,.14,.18), BLUE2, seg=20, rings=12)
    elif kind == "king":
        miniature_body(RED2, cape=True, hood=False)
        cone("Crown", (0,0,2.80), .35, .24, .32, BRONZE, verts=12)
        beam("Sword", (.48,-.12,1.35), (.76,-.13,2.72), .035, STEEL, 12)
    else:
        miniature_body(BLUE2, cape=True, hood=False)
        cyl("Shield", (-.67,-.23,1.50), .57, .12, BLUE, verts=28, rot=(math.pi/2,0,0), b=.012)
        beam("Polearm", (.58,-.10,.75), (.68,-.10,3.35), .035, WOOD2, 12)
        cone("PolearmHead", (.70,-.10,3.55), .13, 0, .42, STEEL, verts=12, do_smooth=True)
    export(path)


def build_opponent():
    clear()

    # Chair/seat is mostly hidden, but gives a believable seated silhouette.
    cube("ChairBack", (0, 1.05, 3.45), (3.35, .35, 5.25), WOOD3, b=.10, seg=3)
    cube("ChairTop", (0, 1.08, 6.04), (3.60, .42, .38), WOOD2, b=.12, seg=3)

    # Large, smooth upper body leaning over the table.
    sphere("Torso", (0, -.45, 3.52), (1.58, .86, 1.70), CLOTH, seg=32, rings=20)
    sphere("Shoulders", (0, -.72, 4.52), (2.05, .82, .60), CLOTH2, seg=32, rings=18)
    cone("CloakBody", (0, -.10, 3.40), 1.78, 1.18, 3.15, CLOTH, verts=32, rot=(math.radians(8),0,0), do_smooth=True)
    torus("CloakCollar", (0, -.77, 4.88), .77, .17, CLOTH2, rot=(math.pi/2,0,0), major_segments=36, minor_segments=10)
    cube("Belt", (0, -.95, 2.80), (2.18, .34, .17), LEATHER, b=.035)
    cube("Buckle", (0, -1.14, 2.80), (.34, .07, .27), BRONZE, b=.025)

    # Neck/head with softer, higher segment geometry.
    cyl("Neck", (0, -.95, 4.95), .34, .62, SKIN2, verts=24, b=.015, do_smooth=True)
    sphere("Head", (0, -1.28, 5.78), (.78, .67, .92), SKIN, seg=36, rings=24)
    sphere("Jaw", (0, -1.40, 5.42), (.62, .50, .56), SKIN2, seg=30, rings=20)
    sphere("EarL", (-.75, -1.20, 5.72), (.14,.10,.20), SKIN, seg=18, rings=12)
    sphere("EarR", (.75, -1.20, 5.72), (.14,.10,.20), SKIN, seg=18, rings=12)

    # Hair is layered rather than a round helmet cap.
    sphere("HairCap", (0, -1.12, 6.36), (.86,.67,.46), HAIR, seg=30, rings=18)
    for i, (x, y, z, sx, sy, sz) in enumerate((
        (-.46,-1.46,6.30,.42,.22,.26),(-.10,-1.54,6.46,.44,.20,.25),(.32,-1.48,6.42,.45,.22,.25),
        (-.68,-1.25,6.02,.24,.18,.42),(.68,-1.25,6.03,.24,.18,.42))):
        sphere(f"HairLock_{i}", (x,y,z), (sx,sy,sz), HAIR2 if i % 2 else HAIR, seg=20, rings=12)

    # Eyes/brows/nose/mouth.
    for side in (-1, 1):
        x = .28 * side
        sphere(f"EyeWhite_{side}", (x, -1.90, 5.94), (.14,.045,.075), WHITE, seg=18, rings=10)
        sphere(f"Eye_{side}", (x, -1.935, 5.94), (.055,.025,.055), EYE, seg=14, rings=8)
        cube(f"Brow_{side}", (x, -1.93, 6.14), (.39,.055,.075), HAIR, rot=(0,0,math.radians(-10 * side)), b=.012)
    cone("Nose", (0,-1.93,5.78), .11,.035,.42, SKIN2, verts=18, rot=(math.radians(90),0,0), do_smooth=True)
    cube("Mouth", (0,-1.94,5.49), (.27,.045,.055), SKIN2, b=.01)

    # Full beard with many smooth layered volumes.
    sphere("BeardCenter", (0,-1.60,5.26), (.52,.27,.50), HAIR, seg=24, rings=16)
    sphere("BeardL", (-.34,-1.58,5.48), (.34,.23,.40), HAIR2, seg=22, rings=14)
    sphere("BeardR", (.34,-1.58,5.48), (.34,.23,.40), HAIR, seg=22, rings=14)
    cone("BeardPoint", (0,-1.52,4.94), .34,.10,.68, HAIR, verts=20, do_smooth=True)
    cube("MoustacheL", (-.17,-1.92,5.66), (.31,.045,.075), HAIR, rot=(0,0,math.radians(-12)), b=.015)
    cube("MoustacheR", (.17,-1.92,5.66), (.31,.045,.075), HAIR, rot=(0,0,math.radians(12)), b=.015)

    # Right arm braces on the table; left arm holds a physical card toward the player.
    beam("UpperArmR", (1.48,-.78,4.35), (1.84,-1.55,3.55), .34, CLOTH2, 20)
    beam("ForearmR", (1.84,-1.55,3.55), (1.35,-2.74,2.55), .27, SKIN, 20)
    sphere("HandR", (1.35,-2.78,2.52), (.45,.34,.28), SKIN, seg=22, rings=14)
    for i in range(4):
        x = 1.18 + i * .105
        beam(f"FingerR_{i}", (x,-2.91,2.45), (x,-3.25,2.36), .030, SKIN, 10)

    beam("UpperArmL", (-1.48,-.80,4.37), (-1.72,-1.44,4.00), .34, CLOTH2, 20)
    beam("ForearmL", (-1.72,-1.44,4.00), (-1.18,-2.12,4.28), .27, SKIN, 20)
    sphere("HandL", (-1.14,-2.16,4.28), (.42,.31,.28), SKIN, seg=22, rings=14)
    # Card angled toward camera.
    cube("HeldCard", (-1.11,-2.43,4.68), (.86,.075,1.20), PARCHMENT, rot=(math.radians(-10),0,math.radians(-6)), b=.055, seg=3)
    cube("HeldCardInset", (-1.11,-2.475,4.68), (.66,.022,.96), RED, rot=(math.radians(-10),0,math.radians(-6)), b=.03, seg=2)
    sphere("CardSeal", (-1.11,-2.50,4.69), (.17,.028,.17), BRONZE, seg=18, rings=10)

    sphere("Brooch", (0,-1.25,4.77), (.22,.08,.22), BRONZE, seg=20, rings=12)

    export(HERO / "opponent_hero.glb")


def build_table():
    clear()
    # Rounded, heavy oak table with many visible planks and metal corner hardware.
    cube("TableBody", (0,0,0), (30.2,27.0,1.0), WOOD3, b=.20, seg=4)
    plank_w = 30.0 / 16
    for i in range(16):
        x = -15.0 + plank_w * (i + .5)
        material = (WOOD, WOOD2, WOOD3)[i % 3]
        cube(f"Plank_{i}", (x,0,.59), (plank_w-.035,26.55,.15), material, b=.045, seg=2)
    cy = 1.90
    cube("BoardInset", (0,cy,.75), (23.2,18.65,.22), WOOD3, b=.14, seg=4)
    # Border rails around the diorama.
    for y in (cy-9.28, cy+9.28):
        cube(f"BoardRailY_{y}", (0,y,1.00), (23.45,.48,.48), WOOD2, b=.10, seg=3)
    for x in (-11.62,11.62):
        cube(f"BoardRailX_{x}", (x,cy,1.00), (.48,18.55,.48), WOOD2, b=.10, seg=3)
    for i,(x,y) in enumerate(((-14.2,-12.7),(14.2,-12.7),(-14.2,12.7),(14.2,12.7))):
        cube(f"CornerIron_{i}", (x,y,1.02), (.90,.90,.12), IRON, b=.09, seg=3)
        for j,(dx,dy) in enumerate(((-.25,-.25),(.25,-.25),(-.25,.25),(.25,.25))):
            sphere(f"Rivet_{i}_{j}", (x+dx,y+dy,1.11), (.055,.055,.035), BRONZE, seg=14, rings=8)
    export(HERO / "war_table_hero.glb")


def main():
    print("\n[CastleCards Realistic] Building semi-realistic final visual pass...")
    build_table()
    build_battlefield()
    build_castle("blue")
    build_castle("red")
    build_opponent()

    build_tree_asset("pine_tree", pine=True)
    build_tree_asset("oak_tree", pine=False)
    build_rock_asset()

    build_unit("spearman", HERO / "spearman_hero.glb", UNITS / "spearman.glb")
    build_unit("archer", HERO / "archer_hero.glb", UNITS / "archer.glb")
    build_unit("swordsman", HERO / "swordsman_hero.glb", UNITS / "swordsman.glb")
    build_special_unit("wizard", UNITS / "wizard.glb")
    build_special_unit("king", UNITS / "king.glb")
    build_special_unit("guard", UNITS / "royal_guard.glb")
    build_special_unit("guard", UNITS / "knight.glb")

    print("[CastleCards Realistic] Final semi-realistic hero assets complete.")


if __name__ == "__main__":
    main()
