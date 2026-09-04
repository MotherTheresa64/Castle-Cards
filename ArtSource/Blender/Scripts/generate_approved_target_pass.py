import bpy
import math
from pathlib import Path
from mathutils import Vector

ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / "Models" / "Hero"
OUT.mkdir(parents=True, exist_ok=True)


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


CLOAK = material("APPROVED_Cloak", (.018, .020, .026), .99)
CLOAK_HI = material("APPROVED_CloakHighlight", (.040, .043, .052), .98)
TUNIC = material("APPROVED_Tunic", (.090, .070, .055), .97)
LEATHER = material("APPROVED_Leather", (.085, .030, .014), .93)
SKIN = material("APPROVED_Skin", (.60, .36, .23), .88)
SKIN_SHADOW = material("APPROVED_SkinShadow", (.43, .235, .145), .91)
HAIR = material("APPROVED_Hair", (.030, .014, .008), .96)
HAIR_L = material("APPROVED_HairHighlight", (.075, .030, .014), .94)
EYE = material("APPROVED_Eye", (.008, .007, .006), .78)
WHITE = material("APPROVED_EyeWhite", (.62, .56, .47), .84)
BRONZE = material("APPROVED_Bronze", (.36, .20, .055), .48, .52)
WOOD = material("APPROVED_Wood", (.12, .045, .020), .94)
CARD = material("APPROVED_Card", (.24, .055, .030), .88)
CARD_EDGE = material("APPROVED_CardEdge", (.58, .38, .16), .76)
CARD_FACE = material("APPROVED_CardFace", (.42, .11, .055), .84)


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
    bpy.ops.mesh.primitive_torus_add(major_radius=major, minor_radius=minor, major_segments=major_segments,
                                    minor_segments=minor_segments, location=loc, rotation=rot)
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
    bpy.ops.export_scene.gltf(filepath=str(OUT / filename), export_format='GLB', use_selection=True,
                              export_materials='EXPORT', export_normals=True, export_animations=False,
                              export_yup=True)
    print(f"[CastleCards Approved] Exported {filename}")


def build_opponent():
    clear_scene()

    cube("ChairBack", (0, .90, 3.05), (2.65, .24, 2.85), WOOD, b=.055)
    cube("ChairSeat", (0, .18, 1.55), (2.80, 1.55, .20), WOOD, b=.040)

    cone("Torso", (0, -.58, 3.48), 1.55, 1.08, 2.78, TUNIC, verts=10, rot=(math.radians(23), 0, 0))
    ico("Shoulders", (0, -.86, 4.48), (1.92, .76, .48), CLOAK, sub=1)

    cloak_verts = [
        (-1.78, -.80, 4.55), (-.40, -1.18, 4.42), (-.50, -1.35, 2.22), (-1.35, -.30, 1.95),
        (.40, -1.18, 4.42), (1.78, -.80, 4.55), (1.35, -.30, 1.95), (.50, -1.35, 2.22),
    ]
    mesh_obj("CloakPanels", cloak_verts, [(0, 1, 2, 3), (4, 5, 6, 7)], [CLOAK, CLOAK_HI], [0, 1])
    torus("CloakCollar", (0, -.84, 4.75), .68, .15, CLOAK_HI, rot=(math.pi / 2, 0, 0))
    cube("Belt", (0, -.82, 2.60), (1.95, .36, .17), LEATHER, rot=(math.radians(10), 0, 0), b=.018)
    cube("Buckle", (0, -1.03, 2.60), (.28, .07, .23), BRONZE, b=.010)

    cyl("Neck", (0, -.96, 4.82), .31, .54, SKIN_SHADOW, verts=9, b=.010)
    ico("Head", (0, -1.22, 5.58), (.80, .64, .91), SKIN, sub=2)
    ico("Jaw", (0, -1.38, 5.25), (.64, .47, .52), SKIN_SHADOW, sub=1)

    ico("HairCap", (0, -1.08, 6.15), (.88, .66, .45), HAIR, sub=1)
    ico("HairTopL", (-.35, -1.29, 6.26), (.49, .28, .27), HAIR_L, sub=1, rot=(0, 0, -.20))
    ico("HairTopR", (.36, -1.27, 6.24), (.50, .28, .27), HAIR, sub=1, rot=(0, 0, .18))
    cone("HairSweepL", (-.68, -1.12, 5.82), .21, .055, .72, HAIR, verts=7, rot=(0, math.radians(-7), math.radians(-10)))
    cone("HairSweepR", (.68, -1.12, 5.82), .21, .055, .72, HAIR_L, verts=7, rot=(0, math.radians(7), math.radians(10)))

    for side in (-1, 1):
        x = .27 * side
        ico(f"EyeWhite_{side}", (x, -1.77, 5.70), (.125, .042, .070), WHITE, sub=1)
        ico(f"Eye_{side}", (x, -1.812, 5.70), (.047, .022, .047), EYE, sub=1)
        cube(f"Brow_{side}", (x, -1.81, 5.90), (.36, .052, .078), HAIR, rot=(0, 0, math.radians(-10 * side)), b=.004)
    cone("Nose", (0, -1.87, 5.54), .095, .032, .40, SKIN_SHADOW, verts=6, rot=(math.radians(90), 0, 0))

    ico("BeardCenter", (0, -1.55, 5.10), (.52, .24, .50), HAIR, sub=1)
    ico("BeardL", (-.35, -1.52, 5.28), (.32, .20, .39), HAIR_L, sub=1)
    ico("BeardR", (.35, -1.52, 5.28), (.32, .20, .39), HAIR, sub=1)
    cone("BeardPoint", (0, -1.48, 4.77), .34, .075, .62, HAIR, verts=8)
    cube("MoustacheL", (-.16, -1.82, 5.45), (.29, .042, .070), HAIR, rot=(0, 0, math.radians(-13)), b=.003)
    cube("MoustacheR", (.16, -1.82, 5.45), (.29, .042, .070), HAIR, rot=(0, 0, math.radians(13)), b=.003)

    shoulder_r = (1.48, -.90, 4.28)
    elbow_r = (1.82, -1.72, 3.45)
    wrist_r = (1.34, -2.82, 2.38)
    beam("UpperArmR", shoulder_r, elbow_r, .32, CLOAK, 9)
    beam("ForearmR", elbow_r, wrist_r, .245, CLOAK_HI, 9)
    ico("HandR", wrist_r, (.42, .34, .30), SKIN, sub=1, rot=(.10, 0, .10))
    for finger in range(4):
        x = wrist_r[0] + (finger - 1.5) * .075
        beam(f"RightFinger_{finger}", (x, wrist_r[1] - .08, wrist_r[2] - .03),
             (x + .015, wrist_r[1] - .42, wrist_r[2] - .10), .026, SKIN, 6)

    shoulder_l = (-1.48, -.90, 4.28)
    elbow_l = (-1.72, -1.52, 4.30)
    wrist_l = (-1.15, -2.08, 4.55)
    beam("UpperArmL", shoulder_l, elbow_l, .32, CLOAK, 9)
    beam("ForearmL", elbow_l, wrist_l, .245, CLOAK_HI, 9)
    ico("HandL", wrist_l, (.39, .31, .29), SKIN, sub=1, rot=(0, 0, -.08))

    card_rot = (math.radians(-4), math.radians(2), math.radians(-7))
    cube("HeldCard", (-1.15, -2.37, 4.64), (.78, .060, 1.08), CARD, rot=card_rot, b=.025)
    cube("HeldCardBorder", (-1.15, -2.405, 4.64), (.60, .015, .88), CARD_EDGE, rot=card_rot, b=.010)
    cube("HeldCardFace", (-1.15, -2.420, 4.64), (.42, .010, .58), CARD_FACE, rot=card_rot, b=.008)
    ico("HeldCardEmblem", (-1.15, -2.438, 4.64), (.13, .018, .13), BRONZE, sub=1)

    for idx, xoff in enumerate((-.16, -.05, .06)):
        beam(f"CardFinger_{idx}", (wrist_l[0] + xoff, wrist_l[1] - .04, wrist_l[2] + .02),
             (-1.15 + xoff, -2.31, 4.92), .024, SKIN, 6)

    ico("Brooch", (0, -1.22, 4.58), (.21, .07, .21), BRONZE, sub=1)
    beam("PendantChain", (0, -1.14, 4.44), (0, -1.24, 4.07), .017, BRONZE, 6)
    ico("Pendant", (0, -1.27, 3.95), (.10, .055, .15), BRONZE, sub=1)

    export_scene("opponent_hero.glb")


def main():
    build_opponent()
    print("[CastleCards Approved] Final approved-reference opponent pass complete. Castle/terrain quality is finalized by generate_quality_assets.py after this step.")


if __name__ == "__main__":
    main()
