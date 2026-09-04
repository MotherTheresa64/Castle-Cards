import bpy
import math
from pathlib import Path
from mathutils import Vector

ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / "Models" / "Hero"
SRC = ROOT / "ArtSource" / "Blender" / "Hero"
BASE_CASTLE = OUT / "castle_hero.glb"
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


STONE = material("APPROVED_Stone", (.31, .30, .285), .96)
STONE_D = material("APPROVED_StoneDark", (.13, .135, .14), .98)
STONE_L = material("APPROVED_StoneLight", (.46, .43, .38), .94)
CLOAK = material("APPROVED_Cloak", (.025, .027, .032), .99)
TUNIC = material("APPROVED_Tunic", (.12, .095, .075), .97)
LEATHER = material("APPROVED_Leather", (.105, .040, .018), .93)
LEATHER_L = material("APPROVED_LeatherLight", (.23, .090, .034), .91)
SKIN = material("APPROVED_Skin", (.60, .36, .23), .88)
SKIN_SHADOW = material("APPROVED_SkinShadow", (.43, .235, .145), .91)
HAIR = material("APPROVED_Hair", (.038, .017, .010), .96)
HAIR_L = material("APPROVED_HairHighlight", (.090, .038, .018), .94)
EYE = material("APPROVED_Eye", (.012, .010, .008), .78)
WHITE = material("APPROVED_EyeWhite", (.62, .56, .47), .84)
BRONZE = material("APPROVED_Bronze", (.36, .20, .055), .48, .52)
WOOD = material("APPROVED_Wood", (.15, .058, .024), .94)
BLUE = (.045, .105, .31)
RED = (.38, .045, .030)


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
    mod = obj.modifiers.new("ApprovedBevel", "BEVEL")
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


def cube(name, loc, dims, mat, rot=(0, 0, 0), b=.02):
    bpy.ops.mesh.primitive_cube_add(location=loc, rotation=rot)
    obj = bpy.context.object
    obj.name = name
    obj.dimensions = dims
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    assign(obj, mat)
    flat(obj)
    bevel(obj, b)
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


def cone(name, loc, r1, r2, depth, mat, verts=10, rot=(0, 0, 0)):
    bpy.ops.mesh.primitive_cone_add(vertices=verts, radius1=r1, radius2=r2, depth=depth, location=loc, rotation=rot)
    obj = bpy.context.object
    obj.name = name
    assign(obj, mat)
    flat(obj)
    bevel(obj, .018)
    return obj


def cyl(name, loc, radius, depth, mat, verts=10, rot=(0, 0, 0), b=.012):
    bpy.ops.mesh.primitive_cylinder_add(vertices=verts, radius=radius, depth=depth, location=loc, rotation=rot)
    obj = bpy.context.object
    obj.name = name
    assign(obj, mat)
    flat(obj)
    bevel(obj, b)
    return obj


def beam(name, a, b, radius, mat, verts=8):
    a = Vector(a)
    b = Vector(b)
    d = b - a
    mid = (a + b) * .5
    bpy.ops.mesh.primitive_cylinder_add(vertices=verts, radius=radius, depth=d.length, location=mid)
    obj = bpy.context.object
    obj.name = name
    obj.rotation_mode = 'QUATERNION'
    obj.rotation_quaternion = Vector((0, 0, 1)).rotation_difference(d.normalized())
    assign(obj, mat)
    flat(obj)
    return obj


def export_scene(filename):
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.export_scene.gltf(
        filepath=str(OUT / filename),
        export_format='GLB',
        use_selection=True,
        export_materials='EXPORT',
        export_normals=True,
        export_animations=False,
        export_yup=True,
    )
    print(f"[CastleCards Approved] Exported {filename}")


def import_gltf(path):
    before = set(bpy.data.objects)
    bpy.ops.import_scene.gltf(filepath=str(path))
    imported = [obj for obj in bpy.data.objects if obj not in before]
    if not imported:
        raise RuntimeError(f"No objects imported from {path}")
    return imported


def recolor_team(objects, team):
    accent = BLUE if team == "blue" else RED
    accent_dark = tuple(c * .48 for c in accent)
    seen = set()
    for obj in objects:
        if obj.type != 'MESH' or not hasattr(obj.data, 'materials'):
            continue
        for slot in obj.material_slots:
            mat = slot.material
            if not mat or mat.name in seen:
                continue
            seen.add(mat.name)
            lname = mat.name.lower()
            if "blue" not in lname and "red" not in lname and "banner" not in lname:
                continue
            if not mat.use_nodes:
                mat.use_nodes = True
            bsdf = mat.node_tree.nodes.get("Principled BSDF")
            if bsdf and "Base Color" in bsdf.inputs:
                target = accent_dark if "dark" in lname else accent
                bsdf.inputs["Base Color"].default_value = (*target, 1.0)


def build_castle_variant(team):
    if not BASE_CASTLE.exists():
        raise RuntimeError(f"Missing reference fortress: {BASE_CASTLE}")
    clear_scene()
    imported = import_gltf(BASE_CASTLE)
    recolor_team(imported, team)
    export_scene(f"castle_{team}_hero.glb")


def build_opponent():
    clear_scene()
    o = []

    # Chair is intentionally mostly hidden by the table; it anchors the human scale.
    o.append(cube("ChairBack", (0, 1.10, 3.65), (3.05, .34, 5.55), WOOD, b=.065))

    # Forward-leaning torso and broad cloak silhouette match the approved hero concepts.
    o.append(cone("Torso", (0, -.15, 3.80), 1.48, 1.10, 2.95, TUNIC, verts=10, rot=(math.radians(13), 0, 0)))
    o.append(ico("Shoulders", (0, -.42, 4.93), (1.78, .72, .50), CLOAK, sub=1))
    o.append(cube("CloakLeft", (-1.05, -.20, 3.78), (1.22, .34, 2.90), CLOAK, rot=(math.radians(10), math.radians(-3), math.radians(-12)), b=.045))
    o.append(cube("CloakRight", (1.05, -.20, 3.78), (1.22, .34, 2.90), CLOAK, rot=(math.radians(10), math.radians(3), math.radians(12)), b=.045))
    o.append(cube("Belt", (0, -.48, 2.92), (2.05, .40, .18), LEATHER, b=.018))
    o.append(cube("Buckle", (0, -.70, 2.92), (.30, .08, .25), BRONZE, b=.010))

    # Neck and faceted head are pushed toward the board so the character reads as leaning in.
    o.append(cyl("Neck", (0, -.52, 5.18), .32, .58, SKIN_SHADOW, verts=9, b=.010))
    o.append(ico("Head", (0, -.72, 6.05), (.78, .64, .92), SKIN, sub=2))
    o.append(ico("Jaw", (0, -.88, 5.72), (.64, .48, .52), SKIN_SHADOW, sub=1))

    # Layered brunette hair, deliberately avoiding round ear-like side masses.
    o.append(ico("HairCap", (0, -.57, 6.64), (.86, .66, .47), HAIR, sub=1))
    o.append(ico("HairTopL", (-.33, -.78, 6.72), (.46, .28, .28), HAIR_L, sub=1, rot=(0, 0, -.18)))
    o.append(ico("HairTopR", (.34, -.76, 6.70), (.48, .29, .27), HAIR, sub=1, rot=(0, 0, .16)))
    o.append(ico("HairSideL", (-.69, -.63, 6.16), (.22, .26, .56), HAIR, sub=1, rot=(0, 0, -.08)))
    o.append(ico("HairSideR", (.69, -.63, 6.16), (.22, .26, .56), HAIR_L, sub=1, rot=(0, 0, .08)))

    # Eyes, brows and nose give the face a readable stern expression at gameplay distance.
    for side in (-1, 1):
        x = .27 * side
        o.append(ico(f"EyeWhite_{side}", (x, -1.30, 6.17), (.13, .045, .075), WHITE, sub=1))
        o.append(ico(f"Eye_{side}", (x, -1.345, 6.17), (.050, .024, .050), EYE, sub=1))
        o.append(cube(f"Brow_{side}", (x, -1.34, 6.37), (.36, .055, .080), HAIR, rot=(0, 0, math.radians(-8 * side)), b=.004))
    o.append(cone("Nose", (0, -1.40, 6.00), .10, .035, .42, SKIN_SHADOW, verts=6, rot=(math.radians(90), 0, 0)))

    # Full beard and moustache, one of the strongest identifying shapes in the approved art.
    o.append(ico("BeardCenter", (0, -1.10, 5.58), (.50, .24, .50), HAIR, sub=1))
    o.append(ico("BeardL", (-.34, -1.08, 5.76), (.31, .20, .39), HAIR_L, sub=1))
    o.append(ico("BeardR", (.34, -1.08, 5.76), (.31, .20, .39), HAIR, sub=1))
    o.append(cube("MoustacheL", (-.16, -1.36, 5.91), (.29, .045, .075), HAIR, rot=(0, 0, math.radians(-12)), b=.003))
    o.append(cube("MoustacheR", (.16, -1.36, 5.91), (.29, .045, .075), HAIR, rot=(0, 0, math.radians(12)), b=.003))

    # Arms are planted toward the table rather than hanging vertically.
    shoulder_l = (-1.38, -.52, 4.72)
    elbow_l = (-1.78, -1.25, 3.92)
    wrist_l = (-1.42, -2.18, 3.30)
    shoulder_r = (1.38, -.52, 4.72)
    elbow_r = (1.78, -1.25, 3.92)
    wrist_r = (1.42, -2.18, 3.30)
    o.append(beam("UpperArmL", shoulder_l, elbow_l, .31, CLOAK, 9))
    o.append(beam("UpperArmR", shoulder_r, elbow_r, .31, CLOAK, 9))
    o.append(beam("ForearmL", elbow_l, wrist_l, .24, SKIN, 9))
    o.append(beam("ForearmR", elbow_r, wrist_r, .24, SKIN, 9))
    o.append(cyl("BracerL", (-1.61, -1.70, 3.60), .25, .68, LEATHER_L, verts=8, rot=(math.radians(58), 0, math.radians(-18)), b=.008))
    o.append(cyl("BracerR", (1.61, -1.70, 3.60), .25, .68, LEATHER_L, verts=8, rot=(math.radians(58), 0, math.radians(18)), b=.008))
    o.append(ico("HandL", wrist_l, (.39, .31, .31), SKIN, sub=1))
    o.append(ico("HandR", wrist_r, (.39, .31, .31), SKIN, sub=1))
    for hand_idx, (wx, wy, wz, sign) in enumerate(((*wrist_l, -1), (*wrist_r, 1))):
        for finger in range(4):
            x = wx + (finger - 1.5) * .07
            o.append(beam(f"Finger_{hand_idx}_{finger}", (x, wy - .08, wz - .02), (x + sign * .015, wy - .36, wz - .07), .025, SKIN, 6))

    o.append(ico("Brooch", (0, -.88, 5.03), (.20, .07, .20), BRONZE, sub=1))
    o.append(beam("PendantChain", (0, -.82, 4.91), (0, -.91, 4.50), .017, BRONZE, 6))
    o.append(ico("Pendant", (0, -.94, 4.37), (.10, .055, .15), BRONZE, sub=1))

    export_scene("opponent_hero.glb")


def main():
    build_castle_variant("blue")
    build_castle_variant("red")
    build_opponent()
    print("[CastleCards Approved] Final approved-reference hero pass complete.")


if __name__ == "__main__":
    main()
