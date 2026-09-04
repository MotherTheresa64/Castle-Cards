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
CLOAK = material("APPROVED_Cloak", (.022, .024, .030), .99)
CLOAK_HI = material("APPROVED_CloakHighlight", (.045, .047, .055), .98)
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
FIRE = material("APPROVED_Fire", (1.0, .20, .02), .20, 0.0, (1.0, .13, .01), 5.0)
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


def torus(name, loc, major, minor, mat, rot=(0, 0, 0), major_segments=12, minor_segments=5):
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


def mesh_obj(name, verts, faces, mats, face_indices=None):
    mesh = bpy.data.meshes.new(name + "Mesh")
    mesh.from_pydata(verts, [], faces)
    mesh.update()
    obj = bpy.data.objects.new(name, mesh)
    bpy.context.collection.objects.link(obj)
    for mat in mats:
        mesh.materials.append(mat)
    if face_indices:
        for poly, idx in zip(mesh.polygons, face_indices):
            poly.material_index = idx
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

    accent = material(
        f"APPROVED_{team}_accent",
        BLUE if team == "blue" else RED,
        .96,
    )
    accent_dark = material(
        f"APPROVED_{team}_accent_dark",
        tuple(c * .50 for c in (BLUE if team == "blue" else RED)),
        .97,
    )

    # Extra front-facing heraldry and fire make the fortress read as a hero miniature at gameplay distance.
    for idx, x in enumerate((-2.65, 2.65)):
        cube(f"TeamBanner_{idx}", (x, -2.49, 2.78), (.58, .065, 1.08), accent if idx == 0 else accent_dark, b=.008)
        cyl(f"BannerPole_{idx}", (x, -2.45, 3.32), .025, 1.55, STONE_D, verts=7, b=.002)

    for idx, x in enumerate((-4.70, 4.70)):
        cyl(f"HeroTorchPole_{idx}", (x, -1.85, 3.28), .035, .55, WOOD, verts=7, b=.003)
        ico(f"HeroTorchFlame_{idx}", (x, -1.86, 3.67), (.08, .07, .18), FIRE, sub=1)

    export_scene(f"castle_{team}_hero.glb")


def build_opponent():
    clear_scene()
    o = []

    # Low chair and hidden seat establish the human scale without exposing a standing lower body.
    o.append(cube("ChairBack", (0, 1.20, 3.55), (3.20, .34, 5.25), WOOD, b=.065))
    o.append(cube("ChairSeat", (0, .25, 1.45), (3.05, 1.85, .22), WOOD, b=.045))

    # Torso is deliberately pitched and shifted toward the board. This is the dominant silhouette in references 1-4.
    o.append(cone("Torso", (0, -.52, 3.62), 1.58, 1.12, 2.92, TUNIC, verts=10, rot=(math.radians(24), 0, 0)))
    o.append(ico("Shoulders", (0, -.78, 4.68), (1.90, .76, .50), CLOAK, sub=1))

    # Angular cloak panels widen the shoulders but taper before the table, avoiding the old rectangular mannequin look.
    cloak_verts = [
        (-1.72, -.72, 4.78), (-.44, -1.10, 4.55), (-.55, -1.28, 2.42), (-1.18, -.34, 2.10),
        (.44, -1.10, 4.55), (1.72, -.72, 4.78), (1.18, -.34, 2.10), (.55, -1.28, 2.42),
    ]
    o.append(mesh_obj("CloakPanels", cloak_verts, [(0, 1, 2, 3), (4, 5, 6, 7)], [CLOAK, CLOAK_HI], [0, 1]))
    o.append(torus("CloakCollar", (0, -.72, 4.95), .68, .15, CLOAK_HI, rot=(math.pi / 2, 0, 0)))
    o.append(cube("Belt", (0, -.76, 2.74), (2.05, .40, .18), LEATHER, rot=(math.radians(10), 0, 0), b=.018))
    o.append(cube("Buckle", (0, -1.00, 2.74), (.30, .08, .25), BRONZE, b=.010))

    # Head moves forward with the torso; the face is slightly larger for readability at 1280x720.
    o.append(cyl("Neck", (0, -.90, 5.02), .33, .58, SKIN_SHADOW, verts=9, b=.010))
    o.append(ico("Head", (0, -1.15, 5.82), (.82, .66, .94), SKIN, sub=2))
    o.append(ico("Jaw", (0, -1.30, 5.48), (.66, .49, .54), SKIN_SHADOW, sub=1))

    # Layered brunette hair with a pointed, swept silhouette rather than round side blobs.
    o.append(ico("HairCap", (0, -1.00, 6.42), (.90, .68, .46), HAIR, sub=1))
    o.append(ico("HairTopL", (-.36, -1.20, 6.53), (.50, .29, .28), HAIR_L, sub=1, rot=(0, 0, -.20)))
    o.append(ico("HairTopR", (.37, -1.18, 6.50), (.51, .29, .27), HAIR, sub=1, rot=(0, 0, .18)))
    o.append(cone("HairSweepL", (-.70, -1.03, 6.03), .22, .06, .78, HAIR, verts=7, rot=(0, math.radians(-7), math.radians(-10))))
    o.append(cone("HairSweepR", (.70, -1.03, 6.03), .22, .06, .78, HAIR_L, verts=7, rot=(0, math.radians(7), math.radians(10))))

    for side in (-1, 1):
        x = .28 * side
        o.append(ico(f"EyeWhite_{side}", (x, -1.72, 5.94), (.13, .045, .075), WHITE, sub=1))
        o.append(ico(f"Eye_{side}", (x, -1.765, 5.94), (.050, .024, .050), EYE, sub=1))
        o.append(cube(f"Brow_{side}", (x, -1.76, 6.15), (.38, .055, .082), HAIR, rot=(0, 0, math.radians(-10 * side)), b=.004))
    o.append(cone("Nose", (0, -1.82, 5.78), .10, .035, .42, SKIN_SHADOW, verts=6, rot=(math.radians(90), 0, 0)))

    # Dense beard and moustache are the strongest character-identification cues from the approved art.
    o.append(ico("BeardCenter", (0, -1.50, 5.34), (.54, .25, .52), HAIR, sub=1))
    o.append(ico("BeardL", (-.36, -1.47, 5.52), (.33, .21, .41), HAIR_L, sub=1))
    o.append(ico("BeardR", (.36, -1.47, 5.52), (.33, .21, .41), HAIR, sub=1))
    o.append(cone("BeardPoint", (0, -1.42, 4.98), .36, .08, .66, HAIR, verts=8))
    o.append(cube("MoustacheL", (-.17, -1.77, 5.68), (.30, .045, .075), HAIR, rot=(0, 0, math.radians(-13)), b=.003))
    o.append(cube("MoustacheR", (.17, -1.77, 5.68), (.30, .045, .075), HAIR, rot=(0, 0, math.radians(13)), b=.003))

    # Hands rest over the far table edge. The low wrists are what make the whole character read as seated and engaged.
    shoulder_l = (-1.48, -.82, 4.48)
    elbow_l = (-1.88, -1.66, 3.68)
    wrist_l = (-1.42, -2.78, 2.50)
    shoulder_r = (1.48, -.82, 4.48)
    elbow_r = (1.88, -1.66, 3.68)
    wrist_r = (1.42, -2.78, 2.50)
    o.append(beam("UpperArmL", shoulder_l, elbow_l, .32, CLOAK, 9))
    o.append(beam("UpperArmR", shoulder_r, elbow_r, .32, CLOAK, 9))
    o.append(beam("ForearmL", elbow_l, wrist_l, .245, SKIN, 9))
    o.append(beam("ForearmR", elbow_r, wrist_r, .245, SKIN, 9))
    o.append(ico("HandL", wrist_l, (.42, .34, .30), SKIN, sub=1, rot=(.10, 0, -.10)))
    o.append(ico("HandR", wrist_r, (.42, .34, .30), SKIN, sub=1, rot=(.10, 0, .10)))

    for hand_idx, (wx, wy, wz, sign) in enumerate(((*wrist_l, -1), (*wrist_r, 1))):
        for finger in range(4):
            x = wx + (finger - 1.5) * .075
            o.append(beam(f"Finger_{hand_idx}_{finger}", (x, wy - .10, wz - .03), (x + sign * .018, wy - .42, wz - .10), .026, SKIN, 6))

    o.append(ico("Brooch", (0, -1.18, 4.80), (.21, .07, .21), BRONZE, sub=1))
    o.append(beam("PendantChain", (0, -1.10, 4.66), (0, -1.20, 4.28), .017, BRONZE, 6))
    o.append(ico("Pendant", (0, -1.23, 4.16), (.10, .055, .15), BRONZE, sub=1))

    export_scene("opponent_hero.glb")


def main():
    build_castle_variant("blue")
    build_castle_variant("red")
    build_opponent()
    print("[CastleCards Approved] Refined fortress/opponent hero pass complete.")


if __name__ == "__main__":
    main()
