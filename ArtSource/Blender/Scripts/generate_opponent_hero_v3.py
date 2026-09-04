"""Castle Cards opponent hero V3.

Rebuilds the seated tavern opponent as a stylized-realistic hero asset instead of a primitive
blockout. The asset is exported to both the hero runtime path and the legacy opponent fallback
path so Blender review and Godot see the same upgraded character.
"""
import bpy
import importlib.util
import math
from pathlib import Path
from mathutils import Vector

SCRIPT = Path(__file__).resolve()
ROOT = SCRIPT.parents[3]
BASE_PATH = SCRIPT.with_name("generate_realistic_target_pass.py")
HERO_OUT = ROOT / "Models" / "Hero" / "opponent_hero.glb"
FALLBACK_OUT = ROOT / "Models" / "Opponent" / "seated_opponent.glb"
SOURCE_BLEND = ROOT / "ArtSource" / "Blender" / "HeroSources" / "opponent_hero_v3.blend"

spec = importlib.util.spec_from_file_location("castle_cards_realistic_base_v3", BASE_PATH)
base = importlib.util.module_from_spec(spec)
spec.loader.exec_module(base)

# Material names intentionally include family words used by the cinematic PBR pass.
SKIN = base.mat("V3_Skin", (.39, .185, .095), .68)
SKIN_LIGHT = base.mat("V3_Warm_Skin", (.49, .245, .125), .65)
SKIN_SHADOW = base.mat("V3_Skin_Shadow", (.245, .090, .042), .76)
LIP = base.mat("V3_Skin_Lip", (.245, .070, .046), .74)
SCLERA = base.mat("V3_Eye_Sclera", (.49, .45, .38), .56)
IRIS = base.mat("V3_Eye_Iris", (.055, .038, .020), .40)
PUPIL = base.mat("V3_Eye_Pupil", (.006, .004, .003), .34)
HAIR = base.mat("V3_Hair", (.018, .007, .004), .88)
HAIR_MID = base.mat("V3_Hair_Highlight", (.048, .017, .008), .86)
CLOTH = base.mat("V3_Black_Cloth", (.014, .016, .020), .96)
CLOTH_MID = base.mat("V3_Charcoal_Cloth", (.034, .035, .042), .94)
CLOTH_EDGE = base.mat("V3_Worn_Cloth", (.060, .058, .064), .92)
LEATHER = base.mat("V3_Dark_Leather", (.060, .019, .008), .84)
BRONZE = base.mat("V3_Bronze_Metal", (.25, .105, .025), .38, .70)
WOOD = base.mat("V3_Dark_Wood", (.070, .022, .009), .84)
WOOD_MID = base.mat("V3_Oak_Wood", (.125, .040, .014), .80)
PARCHMENT = base.mat("V3_Parchment", (.46, .31, .15), .86)
CARD_RED = base.mat("V3_Red_Cloth", (.255, .025, .016), .90)
CARD_GOLD = base.mat("V3_Card_Bronze_Metal", (.31, .135, .030), .42, .60)


def sphere(name, loc, scale, material, seg=36, rings=24):
    return base.sphere(name, loc, scale, material, seg=seg, rings=rings, do_smooth=True)


def cube(name, loc, dims, material, rot=(0, 0, 0), bevel=.035, segments=3):
    return base.cube(name, loc, dims, material, rot=rot, b=bevel, seg=segments)


def beam(name, a, b, radius, material, verts=24):
    return base.beam(name, a, b, radius, material, verts)


def torus(name, loc, major, minor, material, rot=(0, 0, 0), major_segments=36, minor_segments=10):
    return base.torus(name, loc, major, minor, material, rot=rot,
                      major_segments=major_segments, minor_segments=minor_segments)


def ico(name, loc, scale, material, sub=2):
    obj = base.ico(name, loc, scale, material, sub=sub)
    # Keep hair/beard intentionally faceted but not razor sharp.
    if hasattr(obj.data, "polygons"):
        for poly in obj.data.polygons:
            poly.use_smooth = True
    return obj


def add_custom_mesh(name, vertices, faces, material, smooth=True):
    mesh = bpy.data.meshes.new(name + "_Mesh")
    mesh.from_pydata(vertices, [], faces)
    mesh.update()
    obj = bpy.data.objects.new(name, mesh)
    bpy.context.collection.objects.link(obj)
    base.add_mat(obj, material)
    if smooth:
        base.smooth(obj)
    return obj


def build_head_mesh():
    """Closed ring-based head with adult jaw/cheek/forehead proportions and a deeper face plane."""
    center_y = -1.035
    center_z = 4.995
    # z offset, half width, front depth, back depth
    rings = [
        (-.72, .27, .24, .22),
        (-.58, .39, .34, .29),
        (-.40, .49, .42, .34),
        (-.18, .57, .47, .37),
        (.05, .61, .50, .39),
        (.29, .59, .47, .38),
        (.49, .54, .41, .35),
        (.66, .43, .33, .29),
    ]
    segments = 28
    verts = []
    for zoff, width, front, back in rings:
        for i in range(segments):
            angle = math.tau * i / segments
            c = math.cos(angle)
            s = math.sin(angle)
            # More projection on the face side (negative Y) than the skull rear.
            depth = front if s < 0.0 else back
            x = width * c
            y = center_y + depth * s
            # Subtle temple taper and cheek plane: sides sit slightly farther back.
            if abs(c) > .70 and zoff > .18:
                y += .025
            verts.append((x, y, center_z + zoff))

    faces = []
    for r in range(len(rings) - 1):
        for i in range(segments):
            ni = (i + 1) % segments
            a = r * segments + i
            b = r * segments + ni
            c = (r + 1) * segments + ni
            d = (r + 1) * segments + i
            faces.append((a, b, c, d))

    bottom_index = len(verts)
    verts.append((0.0, center_y, center_z - .75))
    top_index = len(verts)
    verts.append((0.0, center_y + .01, center_z + .72))
    for i in range(segments):
        ni = (i + 1) % segments
        faces.append((bottom_index, ni, i))
        top_start = (len(rings) - 1) * segments
        faces.append((top_index, top_start + i, top_start + ni))

    obj = add_custom_mesh("Head_Skin", verts, faces, SKIN, smooth=True)
    bevel = obj.modifiers.new("HeadMicroBevel", "BEVEL")
    bevel.width = .012
    bevel.segments = 2
    try:
        bpy.context.view_layer.objects.active = obj
        obj.select_set(True)
        bpy.ops.object.modifier_apply(modifier=bevel.name)
    except Exception:
        pass
    return obj


def make_cloak_panel():
    """Front cloak panel with real silhouette taper and modeled fold depth."""
    zs = [4.14, 3.82, 3.42, 3.00, 2.57, 2.25]
    widths = [.72, .98, 1.10, 1.18, 1.20, 1.12]
    cols = 7
    verts = []
    for row, (z, width) in enumerate(zip(zs, widths)):
        for col in range(cols):
            t = -1.0 + 2.0 * col / (cols - 1)
            x = t * width
            # Alternating broad folds; lower rows drape more strongly forward.
            fold = .055 * math.cos(t * math.pi * 3.0 + row * .45)
            forward = -.61 - row * .018 + fold
            verts.append((x, forward, z))
    faces = []
    for row in range(len(zs) - 1):
        for col in range(cols - 1):
            a = row * cols + col
            b = a + 1
            c = (row + 1) * cols + col + 1
            d = (row + 1) * cols + col
            faces.append((a, b, c, d))
    obj = add_custom_mesh("CloakFront_Black_Cloth", verts, faces, CLOTH, smooth=True)
    solid = obj.modifiers.new("CloakThickness", "SOLIDIFY")
    solid.thickness = .035
    try:
        bpy.context.view_layer.objects.active = obj
        obj.select_set(True)
        bpy.ops.object.modifier_apply(modifier=solid.name)
    except Exception:
        pass
    return obj


def make_finger(name, start, end, radius=.035, material=SKIN):
    finger = beam(name, start, end, radius, material, 14)
    sphere(name + "_Knuckle_Skin", end, (radius * 1.18, radius * 1.05, radius * 1.08),
           material, seg=20, rings=12)
    return finger


def build_chair():
    # Mostly hidden in gameplay, but enough structure to read as a real chair in Blender review.
    cube("Chair_BackPanel_Dark_Wood", (0, .92, 4.05), (2.20, .18, 2.60), WOOD, bevel=.07)
    cube("Chair_TopRail_Oak_Wood", (0, .90, 5.42), (2.58, .28, .26), WOOD_MID, bevel=.08)
    for side in (-1, 1):
        cube(f"Chair_Post_{side}_Dark_Wood", (side * 1.18, .91, 3.68),
             (.22, .22, 3.62), WOOD, bevel=.055)
        sphere(f"Chair_Finial_{side}_Wood", (side * 1.18, .91, 5.54),
               (.17, .17, .21), WOOD_MID, seg=24, rings=16)


def build_body():
    # Leaned-in torso mass under the cloak. The overlapping organic forms prevent a box silhouette.
    sphere("TorsoCore_Black_Cloth", (0, -.10, 3.30), (1.00, .56, 1.20), CLOTH, seg=40, rings=26)
    sphere("ChestMass_Charcoal_Cloth", (0, -.34, 3.72), (1.08, .47, .72),
           CLOTH_MID, seg=40, rings=24)
    for side in (-1, 1):
        sphere(f"Shoulder_{side}_Charcoal_Cloth", (side * .88, -.29, 3.86),
               (.43, .47, .46), CLOTH_MID, seg=32, rings=20)
    make_cloak_panel()
    # Cowl and layered collar.
    torus("CowlOuter_Charcoal_Cloth", (0, -.54, 4.18), .62, .16, CLOTH_MID,
          rot=(math.pi / 2, 0, 0))
    torus("CowlInner_Worn_Cloth", (0, -.60, 4.19), .46, .065, CLOTH_EDGE,
          rot=(math.pi / 2, 0, 0), major_segments=32, minor_segments=8)
    cube("Belt_Dark_Leather", (0, -.56, 2.45), (1.75, .12, .16), LEATHER, bevel=.025)
    cube("Buckle_Bronze_Metal", (0, -.64, 2.45), (.25, .045, .22), BRONZE, bevel=.018)
    torus("Brooch_Bronze_Metal", (0, -.80, 4.16), .15, .038, BRONZE,
          rot=(math.pi / 2, 0, 0), major_segments=24, minor_segments=8)


def build_face():
    build_head_mesh()
    sphere("Neck_Skin_Shadow", (0, -.73, 4.37), (.27, .23, .34), SKIN_SHADOW,
           seg=28, rings=18)
    # Ears.
    for side in (-1, 1):
        sphere(f"Ear_{side}_Skin_Shadow", (side * .59, -1.03, 4.98),
               (.105, .070, .18), SKIN_SHADOW, seg=24, rings=16)

    # Nose is layered rather than a single cone.
    sphere("NoseBridge_Skin", (0, -1.47, 5.04), (.105, .105, .27), SKIN_LIGHT,
           seg=28, rings=18)
    sphere("NoseTip_Skin", (0, -1.565, 4.91), (.145, .105, .115), SKIN_LIGHT,
           seg=28, rings=18)
    sphere("NostrilL_Skin_Shadow", (-.060, -1.655, 4.89), (.030, .018, .020),
           SKIN_SHADOW, seg=16, rings=10)
    sphere("NostrilR_Skin_Shadow", (.060, -1.655, 4.89), (.030, .018, .020),
           SKIN_SHADOW, seg=16, rings=10)

    # Narrow, inset eyes with lids/brows, not cartoon circles.
    for side in (-1, 1):
        x = side * .225
        sphere(f"EyeWhite_{side}_Eye", (x, -1.515, 5.125), (.120, .034, .061),
               SCLERA, seg=28, rings=16)
        sphere(f"Iris_{side}_Eye", (x, -1.548, 5.123), (.045, .015, .043),
               IRIS, seg=20, rings=12)
        sphere(f"Pupil_{side}_Eye", (x, -1.560, 5.123), (.020, .010, .020),
               PUPIL, seg=16, rings=10)
        # Upper lid and lower lid subtly frame the eye.
        beam(f"UpperLid_{side}_Skin", (x - .105, -1.535, 5.168),
             (x + .105, -1.535, 5.158), .020, SKIN_SHADOW, 16)
        beam(f"Brow_{side}_Hair", (x - .135, -1.555, 5.285 + side * .008),
             (x + .135, -1.555, 5.305 - side * .008), .035, HAIR, 16)

    # Mouth/lip plane, mostly buried by moustache/beard.
    cube("UpperLip_Skin_Lip", (0, -1.532, 4.755), (.245, .032, .036), LIP, bevel=.008)
    cube("MouthCrease_Skin_Shadow", (0, -1.548, 4.724), (.205, .018, .018),
         SKIN_SHADOW, bevel=.004)
    cube("LowerLip_Skin_Lip", (0, -1.525, 4.690), (.205, .028, .032), LIP, bevel=.008)

    # Hair mass with a visible center part and layered locks.
    sphere("HairBack_Hair", (0, -.92, 5.47), (.68, .49, .43), HAIR, seg=32, rings=20)
    locks = [
        (-.42, -1.18, 5.45, .28, .18, .34, -10),
        (-.18, -1.28, 5.59, .31, .17, .27, -5),
        (.12, -1.29, 5.61, .31, .17, .26, 5),
        (.39, -1.18, 5.46, .27, .18, .34, 10),
        (-.52, -.98, 5.25, .19, .17, .34, -14),
        (.52, -.98, 5.25, .19, .17, .34, 14),
    ]
    for i, (x, y, z, sx, sy, sz, rotz) in enumerate(locks):
        obj = ico(f"HairLock_{i}_Hair", (x, y, z), (sx, sy, sz),
                  HAIR_MID if i in (1, 4) else HAIR, sub=2)
        obj.rotation_euler.z = math.radians(rotz)

    # Beard shell plus overlapping clumps creates a unified beard instead of a gemstone cluster.
    sphere("BeardBase_Hair", (0, -1.36, 4.57), (.48, .22, .46), HAIR,
           seg=30, rings=20)
    beard_clumps = [
        (-.34, -1.39, 4.72, .25, .18, .34, HAIR_MID),
        (.34, -1.39, 4.72, .25, .18, .34, HAIR),
        (-.20, -1.42, 4.48, .24, .17, .33, HAIR),
        (.20, -1.42, 4.48, .24, .17, .33, HAIR_MID),
        (0, -1.40, 4.31, .24, .16, .34, HAIR),
    ]
    for i, (x, y, z, sx, sy, sz, material) in enumerate(beard_clumps):
        ico(f"BeardClump_{i}_Hair", (x, y, z), (sx, sy, sz), material, sub=2)
    beam("MustacheL_Hair", (-.02, -1.565, 4.79), (-.27, -1.545, 4.75), .046, HAIR, 14)
    beam("MustacheR_Hair", (.02, -1.565, 4.79), (.27, -1.545, 4.75), .046, HAIR, 14)


def build_arms_and_hands():
    # Viewer-left arm raises the card; viewer-right arm rests toward the table.
    shoulder_l = Vector((-.91, -.28, 3.82))
    elbow_l = Vector((-1.28, -.79, 3.30))
    wrist_l = Vector((-1.04, -1.72, 3.16))
    shoulder_r = Vector((.91, -.28, 3.80))
    elbow_r = Vector((1.30, -.91, 3.18))
    wrist_r = Vector((1.03, -1.82, 2.62))

    beam("UpperArmL_Charcoal_Cloth", shoulder_l, elbow_l, .245, CLOTH_MID, 24)
    sphere("ElbowL_Cloth", elbow_l, (.27, .27, .27), CLOTH_MID, seg=28, rings=18)
    beam("ForearmL_Skin", elbow_l, wrist_l, .175, SKIN, 24)
    sphere("PalmL_Skin", (-1.04, -1.82, 3.16), (.27, .145, .20), SKIN_LIGHT,
           seg=30, rings=18)

    beam("UpperArmR_Charcoal_Cloth", shoulder_r, elbow_r, .245, CLOTH_MID, 24)
    sphere("ElbowR_Cloth", elbow_r, (.27, .27, .27), CLOTH_MID, seg=28, rings=18)
    beam("ForearmR_Skin", elbow_r, wrist_r, .175, SKIN, 24)
    sphere("PalmR_Skin", (1.03, -1.88, 2.60), (.30, .145, .18), SKIN_LIGHT,
           seg=30, rings=18)

    # Card: beveled physical card with inset face, border and central medallion.
    card_rot = (math.radians(-7), math.radians(2), math.radians(-7))
    cube("HeldCard_Parchment", (-1.04, -2.02, 3.34), (.64, .055, .90),
         PARCHMENT, rot=card_rot, bevel=.035, segments=4)
    cube("HeldCardFace_Red_Cloth", (-1.04, -2.052, 3.34), (.50, .014, .74),
         CARD_RED, rot=card_rot, bevel=.020, segments=3)
    torus("HeldCardSeal_Bronze_Metal", (-1.04, -2.073, 3.34), .105, .025, CARD_GOLD,
          rot=(math.pi / 2, 0, math.radians(-7)), major_segments=24, minor_segments=8)

    # Left fingers visibly wrap around card edges.
    make_finger("CardThumb_Skin", (-.83, -1.91, 3.24), (-.84, -2.065, 3.31), .040)
    make_finger("CardIndex_Skin", (-1.23, -1.90, 3.56), (-1.25, -2.055, 3.52), .034)
    make_finger("CardMiddle_Skin", (-1.25, -1.89, 3.43), (-1.27, -2.055, 3.41), .034)
    make_finger("CardRing_Skin", (-1.24, -1.88, 3.30), (-1.26, -2.048, 3.29), .032)

    # Resting hand gets four separated fingers and a thumb to avoid the mitten read.
    for i, dx in enumerate((-.12, -.04, .04, .12)):
        start = (1.00 + dx, -1.94, 2.57 - abs(dx) * .12)
        end = (1.00 + dx * 1.20, -2.19 - .03 * i, 2.53 - .018 * i)
        make_finger(f"RestFinger_{i}_Skin", start, end, .033 - i * .0015)
    make_finger("RestThumb_Skin", (.84, -1.90, 2.60), (.70, -2.04, 2.52), .040)


def build():
    base.clear()
    build_chair()
    build_body()
    build_face()
    build_arms_and_hands()

    # Small cloth folds around the lap/waist to break the last large uninterrupted silhouette.
    for i, x in enumerate((-.62, -.31, 0.0, .31, .62)):
        beam(f"LapFold_{i}_Worn_Cloth", (x * .75, -.67, 2.62),
             (x, -.72, 2.20), .035, CLOTH_EDGE, 12)

    HERO_OUT.parent.mkdir(parents=True, exist_ok=True)
    FALLBACK_OUT.parent.mkdir(parents=True, exist_ok=True)
    SOURCE_BLEND.parent.mkdir(parents=True, exist_ok=True)

    # Same authored model powers the runtime hero and the legacy/review fallback.
    base.export(HERO_OUT)
    base.export(FALLBACK_OUT)
    bpy.ops.wm.save_as_mainfile(filepath=str(SOURCE_BLEND), check_existing=False)
    print(f"[CastleCards Opponent V3] Source blend: {SOURCE_BLEND.relative_to(ROOT)}")
    print("[CastleCards Opponent V3] Stylized-realistic seated opponent rebuilt.")


if __name__ == "__main__":
    build()
