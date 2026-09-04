"""Castle Cards seated opponent hero V4.

A deliberately less toy-like, more angular stylized-realistic tavern rival built for the
reference camera.  This replaces the round/symmetrical V3 forms with an adult head, layered
hair and beard clumps, a draped cloak silhouette, articulated arms/hands and a forward seated
pose.  The same authored model is exported to both runtime and review fallback paths.
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
SOURCE_BLEND = ROOT / "ArtSource" / "Blender" / "HeroSources" / "opponent_hero_v4.blend"

spec = importlib.util.spec_from_file_location("castle_cards_realistic_base_v4", BASE_PATH)
base = importlib.util.module_from_spec(spec)
spec.loader.exec_module(base)

# Material names intentionally retain family tokens consumed by the cinematic PBR pass.
SKIN = base.mat("V4_Skin", (.34, .145, .070), .70)
SKIN_LIGHT = base.mat("V4_Warm_Skin", (.44, .205, .105), .66)
SKIN_SHADOW = base.mat("V4_Skin_Shadow", (.205, .070, .030), .76)
LIP = base.mat("V4_Skin_Lip", (.205, .048, .035), .76)
SCLERA = base.mat("V4_Eye_Sclera", (.42, .39, .34), .60)
IRIS = base.mat("V4_Eye_Iris", (.045, .028, .014), .42)
PUPIL = base.mat("V4_Eye_Pupil", (.004, .003, .002), .36)
HAIR = base.mat("V4_Hair", (.012, .005, .003), .90)
HAIR_MID = base.mat("V4_Hair_Highlight", (.036, .012, .006), .88)
CLOTH = base.mat("V4_Black_Cloth", (.010, .012, .016), .97)
CLOTH_MID = base.mat("V4_Charcoal_Cloth", (.025, .027, .033), .95)
CLOTH_EDGE = base.mat("V4_Worn_Cloth", (.048, .047, .052), .93)
LEATHER = base.mat("V4_Dark_Leather", (.048, .015, .006), .86)
BRONZE = base.mat("V4_Bronze_Metal", (.22, .085, .018), .40, .72)
WOOD = base.mat("V4_Dark_Wood", (.055, .016, .006), .86)
WOOD_MID = base.mat("V4_Oak_Wood", (.105, .032, .010), .81)
PARCHMENT = base.mat("V4_Parchment", (.40, .255, .115), .88)
CARD_RED = base.mat("V4_Red_Cloth", (.205, .018, .012), .92)
CARD_GOLD = base.mat("V4_Card_Bronze_Metal", (.27, .105, .022), .42, .64)


def sphere(name, loc, scale, material, seg=40, rings=28):
    return base.sphere(name, loc, scale, material, seg=seg, rings=rings, do_smooth=True)


def cube(name, loc, dims, material, rot=(0, 0, 0), bevel=.025, segments=3):
    return base.cube(name, loc, dims, material, rot=rot, b=bevel, seg=segments)


def beam(name, a, b, radius, material, verts=24):
    return base.beam(name, a, b, radius, material, verts)


def torus(name, loc, major, minor, material, rot=(0, 0, 0), major_segments=36, minor_segments=10):
    return base.torus(name, loc, major, minor, material, rot=rot,
                      major_segments=major_segments, minor_segments=minor_segments)


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


def apply_bevel(obj, width=.012, segments=2):
    mod = obj.modifiers.new("V4Bevel", "BEVEL")
    mod.width = width
    mod.segments = segments
    try:
        bpy.context.view_layer.objects.active = obj
        obj.select_set(True)
        bpy.ops.object.modifier_apply(modifier=mod.name)
    except Exception:
        pass
    return obj


def tapered_beam(name, a, b, r_start, r_end, material, verts=10):
    a = Vector(a); b = Vector(b); d = b - a
    mid = (a + b) * .5
    bpy.ops.mesh.primitive_cone_add(vertices=verts, radius1=r_start, radius2=r_end,
                                    depth=d.length, location=mid)
    obj = bpy.context.object
    obj.name = name
    obj.rotation_mode = 'QUATERNION'
    obj.rotation_quaternion = Vector((0, 0, 1)).rotation_difference(d.normalized())
    base.add_mat(obj, material)
    base.smooth(obj)
    apply_bevel(obj, min(r_start, r_end) * .08, 2)
    return obj


def build_head():
    """Angular adult head, intentionally narrower and less bobble-headed than V3."""
    cy = -1.04
    cz = 4.90
    # z, width, face depth, rear depth.  Jaw and temples taper much harder than V3.
    rings = [
        (-.66, .22, .19, .18),
        (-.54, .33, .27, .24),
        (-.36, .43, .33, .29),
        (-.14, .50, .37, .32),
        (.08, .52, .38, .33),
        (.29, .49, .35, .32),
        (.48, .43, .30, .28),
        (.62, .31, .22, .21),
    ]
    segments = 32
    verts = []
    for zoff, width, front, rear in rings:
        for i in range(segments):
            a = math.tau * i / segments
            c, s = math.cos(a), math.sin(a)
            depth = front if s < 0 else rear
            # flatten side planes slightly for the low-poly cinematic face read
            x = width * c
            y = cy + depth * s
            if abs(c) > .72:
                y += .018
            if zoff < -.28:
                x *= .93
            verts.append((x, y, cz + zoff))
    faces = []
    for r in range(len(rings) - 1):
        for i in range(segments):
            j = (i + 1) % segments
            faces.append((r*segments+i, r*segments+j, (r+1)*segments+j, (r+1)*segments+i))
    bottom = len(verts); verts.append((0, cy, cz-.69))
    top = len(verts); verts.append((0, cy+.01, cz+.66))
    for i in range(segments):
        j = (i + 1) % segments
        faces.append((bottom, j, i))
        start = (len(rings)-1)*segments
        faces.append((top, start+i, start+j))
    head = add_custom_mesh("Head_Skin", verts, faces, SKIN, smooth=True)
    apply_bevel(head, .010, 2)

    # neck mostly hidden by cloak
    sphere("Neck_Skin_Shadow", (0, -.73, 4.27), (.245, .22, .31), SKIN_SHADOW, 30, 20)
    for side in (-1, 1):
        sphere(f"Ear_{side}_Skin_Shadow", (side*.505, -1.025, 4.91),
               (.085, .058, .145), SKIN_SHADOW, 24, 16)

    # Cheek and brow planes are subtle, not spherical cartoon features.
    for side in (-1, 1):
        sphere(f"Cheek_{side}_Skin", (side*.265, -1.365, 4.79),
               (.19, .055, .16), SKIN_LIGHT, 28, 18)
        beam(f"BrowPlane_{side}_Skin_Shadow",
             (side*.08, -1.382, 5.095), (side*.39, -1.350, 5.115),
             .032, SKIN_SHADOW, 18)

    # Long, angular nose bridge and compact nose tip.
    tapered_beam("NoseBridge_Skin", (0, -1.31, 5.12), (0, -1.455, 4.90),
                 .070, .095, SKIN_LIGHT, 12)
    sphere("NoseTip_Skin", (0, -1.495, 4.86), (.115, .085, .085), SKIN_LIGHT, 26, 16)
    sphere("NostrilL_Skin_Shadow", (-.052, -1.565, 4.845), (.025, .014, .015), SKIN_SHADOW, 14, 8)
    sphere("NostrilR_Skin_Shadow", (.052, -1.565, 4.845), (.025, .014, .015), SKIN_SHADOW, 14, 8)

    # Small, deep-set eyes like the target artwork.
    for side in (-1, 1):
        x = side*.205
        sphere(f"EyeWhite_{side}_Eye", (x, -1.395, 5.045), (.082, .024, .043), SCLERA, 24, 14)
        sphere(f"Iris_{side}_Eye", (x, -1.416, 5.043), (.030, .010, .029), IRIS, 18, 10)
        sphere(f"Pupil_{side}_Eye", (x, -1.424, 5.043), (.012, .007, .012), PUPIL, 14, 8)
        beam(f"UpperLid_{side}_Skin", (x-.080, -1.402, 5.080), (x+.080, -1.402, 5.072), .014, SKIN_SHADOW, 14)
        # heavy, low eyebrows provide the stern look
        tapered_beam(f"Brow_{side}_Hair", (x-.120, -1.418, 5.160), (x+.125, -1.420, 5.175),
                     .026, .034, HAIR, 8)

    cube("UpperLip_Skin_Lip", (0, -1.425, 4.685), (.205, .020, .025), LIP, bevel=.005)
    cube("MouthCrease_Skin_Shadow", (0, -1.438, 4.655), (.180, .014, .012), SKIN_SHADOW, bevel=.003)
    cube("LowerLip_Skin_Lip", (0, -1.418, 4.628), (.160, .018, .023), LIP, bevel=.004)


def build_hair_and_beard():
    # Hair cap kept close to skull; pointed/tapered clumps replace the V3 puffball silhouette.
    sphere("HairSkull_Hair", (0, -.995, 5.28), (.535, .34, .315), HAIR, 34, 22)
    locks = [
        ((-.43,-1.10,5.39), (-.31,-1.29,5.08), .16,.10, -8),
        ((-.26,-1.16,5.52), (-.12,-1.31,5.24), .18,.09, -4),
        ((-.06,-1.18,5.56), (.05,-1.31,5.28), .17,.08, 1),
        ((.18,-1.16,5.53), (.28,-1.29,5.24), .17,.09, 5),
        ((.39,-1.10,5.41), (.46,-1.22,5.10), .15,.08, 9),
        ((-.50,-.98,5.25), (-.48,-1.05,4.91), .13,.07, -4),
        ((.50,-.98,5.25), (.48,-1.05,4.91), .13,.07, 4),
    ]
    for i,(a,b,r1,r2,rz) in enumerate(locks):
        obj=tapered_beam(f"HairLock_{i}_Hair", a,b,r1,r2, HAIR_MID if i in (1,4) else HAIR, 9)
        obj.rotation_euler.z += math.radians(rz)

    # Side beard hugs the jaw; central clumps taper downward and forward.
    for side in (-1,1):
        tapered_beam(f"SideBeard_{side}_Hair", (side*.40,-1.30,4.82), (side*.30,-1.39,4.48),
                     .17,.105, HAIR_MID if side < 0 else HAIR, 9)
        tapered_beam(f"JawBeard_{side}_Hair", (side*.28,-1.37,4.61), (side*.18,-1.43,4.31),
                     .16,.085, HAIR, 9)
    tapered_beam("BeardCenterA_Hair", (-.11,-1.42,4.48), (-.06,-1.43,4.18), .15,.055, HAIR_MID, 9)
    tapered_beam("BeardCenterB_Hair", (.11,-1.42,4.48), (.06,-1.43,4.18), .15,.055, HAIR, 9)
    tapered_beam("BeardPoint_Hair", (0,-1.41,4.40), (0,-1.39,4.10), .13,.035, HAIR, 9)
    beam("MustacheL_Hair", (-.015,-1.445,4.71), (-.23,-1.430,4.66), .030, HAIR, 12)
    beam("MustacheR_Hair", (.015,-1.445,4.71), (.23,-1.430,4.66), .030, HAIR, 12)


def build_cloak_shell():
    # Broad shoulders, narrow waist, lap spread. Grid depth creates actual cloth folds.
    zs = [4.20, 3.96, 3.66, 3.30, 2.90, 2.52, 2.22]
    widths = [1.03, 1.18, 1.25, 1.20, 1.13, 1.08, 1.02]
    cols = 9
    verts=[]
    for row,(z,w) in enumerate(zip(zs,widths)):
        for col in range(cols):
            t=-1+2*col/(cols-1)
            x=t*w
            fold=.035*math.cos(t*math.pi*4.0 + row*.42)
            # leaned forward chest, draping back at lap
            y=-.50 - .035*row + fold
            if row < 2:
                y -= .05*(1-abs(t))
            verts.append((x,y,z))
    faces=[]
    for row in range(len(zs)-1):
        for col in range(cols-1):
            a=row*cols+col; b=a+1; c=(row+1)*cols+col+1; d=(row+1)*cols+col
            faces.append((a,b,c,d))
    cloak=add_custom_mesh("CloakFront_Black_Cloth", verts, faces, CLOTH, smooth=True)
    solid=cloak.modifiers.new("CloakThickness","SOLIDIFY"); solid.thickness=.032
    try:
        bpy.context.view_layer.objects.active=cloak; cloak.select_set(True)
        bpy.ops.object.modifier_apply(modifier=solid.name)
    except Exception:
        pass

    # shoulder mantle forms one low continuous silhouette rather than two ball shoulders
    mantle_verts=[
        (-1.18,-.20,4.03),(-.70,-.58,4.20),(0,-.64,4.26),(.70,-.58,4.20),(1.18,-.20,4.03),
        (-1.07,-.04,3.79),(-.56,-.43,3.88),(0,-.49,3.93),(.56,-.43,3.88),(1.07,-.04,3.79)
    ]
    mantle_faces=[]
    for i in range(4): mantle_faces.append((i,i+1,6+i,5+i))
    mantle=add_custom_mesh("ShoulderMantle_Charcoal_Cloth",mantle_verts,mantle_faces,CLOTH_MID,True)
    solid=mantle.modifiers.new("MantleThickness","SOLIDIFY"); solid.thickness=.055
    try:
        bpy.context.view_layer.objects.active=mantle; mantle.select_set(True)
        bpy.ops.object.modifier_apply(modifier=solid.name)
    except Exception:
        pass


def build_body():
    # Hidden anatomy masses only support the cloak shape.
    sphere("TorsoUnder_Black_Cloth", (0,-.08,3.28), (.82,.48,1.06), CLOTH, 36, 24)
    build_cloak_shell()
    torus("Cowl_Charcoal_Cloth", (0,-.52,4.18), .53,.11,CLOTH_MID,rot=(math.pi/2,0,0),major_segments=32,minor_segments=8)
    torus("Brooch_Bronze_Metal", (0,-.70,4.11), .105,.026,BRONZE,rot=(math.pi/2,0,0),major_segments=22,minor_segments=7)
    cube("Belt_Dark_Leather", (0,-.56,2.42),(1.50,.09,.12),LEATHER,bevel=.018)


def make_finger(name,start,end,radius):
    tapered_beam(name,start,end,radius,radius*.82,SKIN,12)
    sphere(name+"_Tip_Skin",end,(radius*.85,radius*.70,radius*.72),SKIN_LIGHT,18,10)


def build_arms_and_hands():
    # Asymmetrical, forward table-playing posture.
    sl=Vector((-.96,-.27,3.80)); el=Vector((-1.22,-.88,3.28)); wl=Vector((-1.03,-1.65,3.22))
    sr=Vector((.96,-.27,3.78)); er=Vector((1.25,-.92,3.12)); wr=Vector((.99,-1.79,2.58))
    tapered_beam("UpperArmL_Charcoal_Cloth",sl,el,.22,.19,CLOTH_MID,18)
    tapered_beam("ForearmL_Skin",el,wl,.16,.13,SKIN,20)
    tapered_beam("UpperArmR_Charcoal_Cloth",sr,er,.22,.19,CLOTH_MID,18)
    tapered_beam("ForearmR_Skin",er,wr,.16,.13,SKIN,20)

    sphere("PalmL_Skin",(-1.03,-1.72,3.21),(.22,.105,.155),SKIN_LIGHT,26,16)
    sphere("PalmR_Skin",(.99,-1.85,2.57),(.235,.105,.145),SKIN_LIGHT,26,16)

    card_rot=(math.radians(-9),math.radians(2),math.radians(-6))
    cube("HeldCard_Parchment",(-1.03,-1.92,3.38),(.54,.045,.76),PARCHMENT,rot=card_rot,bevel=.025,segments=3)
    cube("HeldCardFace_Red_Cloth",(-1.03,-1.946,3.38),(.42,.010,.63),CARD_RED,rot=card_rot,bevel=.012,segments=2)
    torus("HeldCardSeal_Bronze_Metal",(-1.03,-1.960,3.38),.082,.018,CARD_GOLD,
          rot=(math.pi/2,0,math.radians(-6)),major_segments=20,minor_segments=6)

    make_finger("CardThumb_Skin",(-.84,-1.78,3.28),(-.83,-1.94,3.32),.032)
    make_finger("CardIndex_Skin",(-1.18,-1.78,3.53),(-1.19,-1.94,3.50),.027)
    make_finger("CardMiddle_Skin",(-1.20,-1.78,3.42),(-1.21,-1.94,3.40),.027)
    make_finger("CardRing_Skin",(-1.19,-1.77,3.31),(-1.20,-1.93,3.30),.025)

    for i,dx in enumerate((-.105,-.035,.035,.105)):
        make_finger(f"RestFinger_{i}_Skin",(.99+dx,-1.90,2.55),(.99+dx*1.10,-2.10-.025*i,2.51-.012*i),.027-i*.001)
    make_finger("RestThumb_Skin",(.82,-1.84,2.59),(.70,-1.98,2.53),.032)


def build_chair():
    # Slim, dark chair; intentionally subordinate to the character silhouette.
    cube("ChairBack_Dark_Wood",(0,.78,3.82),(1.90,.14,2.65),WOOD,bevel=.045)
    cube("ChairTop_Oak_Wood",(0,.78,5.18),(2.10,.20,.20),WOOD_MID,bevel=.055)
    for side in (-1,1):
        cube(f"ChairPost_{side}_Dark_Wood",(side*.98,.79,3.72),(.16,.16,3.22),WOOD,bevel=.038)
        sphere(f"ChairFinial_{side}_Wood",(side*.98,.79,5.27),(.12,.12,.15),WOOD_MID,22,14)


def add_studio_lights():
    # Useful when the generated source .blend is opened directly in Rendered view.
    bpy.ops.object.light_add(type='AREA', location=(-2.4,-3.8,6.6))
    key=bpy.context.object; key.name="V4_Key"; key.data.energy=650; key.data.size=3.0
    key.rotation_euler=(math.radians(26),0,math.radians(-28))
    bpy.ops.object.light_add(type='AREA', location=(2.7,-1.5,5.0))
    rim=bpy.context.object; rim.name="V4_Rim"; rim.data.energy=360; rim.data.size=2.5
    rim.rotation_euler=(math.radians(60),0,math.radians(140))


def build():
    base.clear()
    build_chair()
    build_body()
    build_head()
    build_hair_and_beard()
    build_arms_and_hands()
    add_studio_lights()

    HERO_OUT.parent.mkdir(parents=True,exist_ok=True)
    FALLBACK_OUT.parent.mkdir(parents=True,exist_ok=True)
    SOURCE_BLEND.parent.mkdir(parents=True,exist_ok=True)

    # Save editable authored source before the GLB-only material post pass mutates the scene.
    bpy.ops.wm.save_as_mainfile(filepath=str(SOURCE_BLEND),check_existing=False)
    base.export(HERO_OUT)
    base.export(FALLBACK_OUT)

    # Apply the same embedded PBR treatment used by the rest of the game, but only to this hero.
    polish_path=SCRIPT.with_name("generate_cinematic_material_pass.py")
    try:
        pspec=importlib.util.spec_from_file_location("castle_cards_cinematic_v4",polish_path)
        polish=importlib.util.module_from_spec(pspec); pspec.loader.exec_module(polish)
        polish.process_glb(HERO_OUT,401)
        polish.process_glb(FALLBACK_OUT,402)
    except Exception as exc:
        print(f"[CastleCards Opponent V4] Material polish warning: {exc}")

    print(f"[CastleCards Opponent V4] Source blend: {SOURCE_BLEND.relative_to(ROOT)}")
    print("[CastleCards Opponent V4] Rebuilt adult stylized-realistic seated rival.")


if __name__ == "__main__":
    build()
