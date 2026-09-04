import bpy
import math
import random
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
MODELS = ROOT / "Models"
SOURCE = ROOT / "ArtSource" / "Blender" / "GeneratedGameplay"
random.seed(90426)

for p in (MODELS, SOURCE):
    p.mkdir(parents=True, exist_ok=True)


def clear_scene():
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)


def material(name, rgb, roughness=.9, metallic=0.0, emission=None, emission_strength=4.0):
    m = bpy.data.materials.get(name)
    if m:
        return m
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    bsdf = m.node_tree.nodes.get("Principled BSDF")
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
    return m


STONE = material("CCG_Stone", (.33,.32,.30), .98)
STONE_D = material("CCG_StoneDark", (.15,.16,.16), .99)
STONE_L = material("CCG_StoneLight", (.47,.44,.39), .98)
WOOD = material("CCG_Wood", (.24,.095,.032), .94)
WOOD_D = material("CCG_WoodDark", (.085,.028,.012), .97)
WOOD_L = material("CCG_WoodLight", (.39,.17,.05), .91)
IRON = material("CCG_Iron", (.05,.055,.065), .48, .82)
STEEL = material("CCG_Steel", (.28,.30,.33), .42, .72)
BRASS = material("CCG_Brass", (.38,.20,.055), .50, .62)
BLUE = material("CCG_Blue", (.035,.10,.30), .98)
RED = material("CCG_Red", (.36,.035,.025), .98)
PURPLE = material("CCG_Purple", (.22,.055,.30), .98)
GREEN = material("CCG_Green", (.075,.28,.13), .98)
TAN = material("CCG_Tan", (.40,.30,.17), .98)
LEATHER = material("CCG_Leather", (.16,.055,.020), .95)
SKIN = material("CCG_Skin", (.67,.43,.29), .92)
BONE = material("CCG_Bone", (.68,.61,.46), .98)
PARCHMENT = material("CCG_Parchment", (.62,.46,.25), .96)
BLACK = material("CCG_Black", (.018,.020,.025), .90)
FIRE = material("CCG_Fire", (.95,.22,.02), .28, 0.0, emission=(1.0,.11,.01), emission_strength=6.0)
ARCANE = material("CCG_Arcane", (.16,.44,1.0), .25, 0.0, emission=(.10,.35,1.0), emission_strength=5.5)
HEAL = material("CCG_Heal", (.10,.82,.38), .28, 0.0, emission=(.08,.72,.28), emission_strength=5.0)
SUSPICION = material("CCG_Suspicion", (.95,.32,.06), .32, 0.0, emission=(.85,.16,.02), emission_strength=3.2)


def assign(o, m):
    if hasattr(o.data, "materials"):
        o.data.materials.append(m)


def flat(o):
    if hasattr(o.data, "polygons"):
        for p in o.data.polygons:
            p.use_smooth = False


def bevel(o, width=.02):
    if width <= 0:
        return
    bpy.context.view_layer.objects.active = o
    o.select_set(True)
    mod = o.modifiers.new("Bevel", "BEVEL")
    mod.width = width
    mod.segments = 1
    try:
        bpy.ops.object.modifier_apply(modifier=mod.name)
    except Exception:
        pass


def cube(name, loc, dims, mat, rot=(0,0,0), b=.02):
    bpy.ops.mesh.primitive_cube_add(location=loc, rotation=rot)
    o = bpy.context.object
    o.name = name
    o.dimensions = dims
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    assign(o, mat); flat(o); bevel(o, b)
    return o


def cyl(name, loc, radius, depth, mat, verts=10, rot=(0,0,0), b=.012):
    bpy.ops.mesh.primitive_cylinder_add(vertices=verts, radius=radius, depth=depth, location=loc, rotation=rot)
    o = bpy.context.object
    o.name = name
    assign(o, mat); flat(o); bevel(o, b)
    return o


def cone(name, loc, r1, r2, depth, mat, verts=8, rot=(0,0,0)):
    bpy.ops.mesh.primitive_cone_add(vertices=verts, radius1=r1, radius2=r2, depth=depth, location=loc, rotation=rot)
    o = bpy.context.object
    o.name = name
    assign(o, mat); flat(o)
    return o


def ico(name, loc, scale, mat, sub=1, rot=(0,0,0)):
    bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=sub, radius=1.0, location=loc, rotation=rot)
    o = bpy.context.object
    o.name = name
    o.scale = scale
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    assign(o, mat); flat(o)
    return o


def torus(name, loc, major, minor, mat, rot=(0,0,0), major_segments=16, minor_segments=5):
    bpy.ops.mesh.primitive_torus_add(major_radius=major, minor_radius=minor,
        major_segments=major_segments, minor_segments=minor_segments,
        location=loc, rotation=rot)
    o = bpy.context.object
    o.name = name
    assign(o, mat); flat(o)
    return o


def export_asset(objs, rel_dir, filename):
    out_dir = MODELS / rel_dir
    src_dir = SOURCE / rel_dir
    out_dir.mkdir(parents=True, exist_ok=True)
    src_dir.mkdir(parents=True, exist_ok=True)

    bpy.ops.object.select_all(action='DESELECT')
    for o in objs:
        o.select_set(True)
    if objs:
        bpy.context.view_layer.objects.active = objs[0]

    bpy.ops.wm.save_as_mainfile(filepath=str(src_dir / f"{filename}.blend"))

    bpy.ops.object.select_all(action='DESELECT')
    for o in objs:
        o.select_set(True)
    if objs:
        bpy.context.view_layer.objects.active = objs[0]

    bpy.ops.export_scene.gltf(
        filepath=str(out_dir / f"{filename}.glb"),
        export_format='GLB',
        use_selection=True,
        export_materials='EXPORT',
        export_animations=False,
        export_yup=True)
    print(f"[CastleCards] exported {rel_dir}/{filename}.glb")


def mini_base(o, radius=.72):
    o.append(cyl("Base", (0,0,.08), radius, .16, IRON, verts=16, b=.018))
    o.append(cyl("BaseTop", (0,0,.19), radius-.09, .12, STONE_D, verts=16, b=.014))


def humanoid(o, cloth=BLUE, armor=False, helmet=True):
    for x in (-.18,.18):
        o.append(cube("Boot", (x,-.02,.46), (.24,.32,.25), LEATHER, b=.02))
        o.append(cyl("Leg", (x,0,.83), .12,.64, cloth if not armor else STEEL, verts=8,b=.008))
    o.append(cone("Torso", (0,0,1.50), .47,.36,1.04, cloth if not armor else STEEL, verts=8))
    o.append(cube("Belt", (0,-.01,1.34), (.80,.53,.10), LEATHER,b=.01))
    o.append(ico("Shoulders", (0,0,1.92), (.53,.37,.31), STEEL if armor else cloth, sub=1))
    o.append(ico("Head", (0,-.01,2.38), (.29,.27,.33), SKIN,sub=2))
    if helmet:
        o.append(ico("Helmet", (0,0,2.59), (.35,.33,.24), STEEL,sub=1))
        o.append(cyl("HelmetRim", (0,0,2.54), .35,.07, IRON, verts=10,b=.006))


def build_king():
    clear_scene(); o=[]; mini_base(o,.76)
    humanoid(o, PURPLE, armor=False, helmet=False)
    o.append(cone("CrownBase", (0,0,2.72), .30,.28,.18, BRASS, verts=8))
    for i,a in enumerate([i*math.tau/6 for i in range(6)]):
        o.append(cone(f"CrownPoint_{i}", (math.cos(a)*.22, math.sin(a)*.22, 2.92), .08, 0, .36, BRASS, verts=4))
    o.append(cube("RoyalCape", (0,.22,1.55), (.78,.12,1.25), RED, rot=(math.radians(-7),0,0), b=.015))
    o.append(cyl("Scepter", (.46,-.08,1.95), .035,1.75,BRASS,verts=8,rot=(0,0,math.radians(-10)),b=.004))
    o.append(ico("ScepterGem", (.62,-.08,2.78), (.12,.10,.14), ARCANE,sub=1))
    export_asset(o,"Units/Human","king")


def build_royal_guard():
    clear_scene(); o=[]; mini_base(o,.74); humanoid(o, RED, armor=True, helmet=True)
    o.append(cyl("Shield",(-.58,-.20,1.50),.55,.11,RED,verts=12,rot=(math.pi/2,0,0),b=.012))
    o.append(cube("ShieldCrossV",(-.58,-.28,1.50),(.13,.06,.92),BRASS,b=.006))
    o.append(cube("ShieldCrossH",(-.58,-.28,1.50),(.92,.06,.13),BRASS,b=.006))
    o.append(cyl("Halberd",(.62,-.05,2.05),.042,3.15,WOOD_L,verts=8,b=.004))
    o.append(cube("HalberdBlade",(.62,-.05,3.55),(.42,.08,.34),STEEL,rot=(0,0,math.radians(25)),b=.006))
    export_asset(o,"Units/Human","royal_guard")


def build_wizard():
    clear_scene(); o=[]; mini_base(o,.72)
    for x in (-.17,.17):
        o.append(cube("Boot",(x,0,.42),(.22,.30,.24),LEATHER,b=.018))
    o.append(cone("Robe",(0,0,1.35),.62,.34,1.75,PURPLE,verts=9))
    o.append(ico("Head",(0,-.01,2.35),(.29,.27,.33),SKIN,sub=2))
    o.append(cone("Hat",(0,.02,2.88),.46,.02,1.25,PURPLE,verts=9,rot=(0,0,math.radians(-7))))
    o.append(cyl("Staff",(.55,0,1.88),.045,3.0,WOOD_L,verts=8,b=.004))
    o.append(torus("StaffRing",(.55,0,3.34),.25,.045,BRASS,rot=(math.pi/2,0,0)))
    o.append(ico("StaffOrb",(.55,0,3.34),(.14,.14,.14),ARCANE,sub=2))
    export_asset(o,"Units/Human","wizard")


def build_assassin():
    clear_scene(); o=[]; mini_base(o,.70)
    humanoid(o, BLACK, armor=False, helmet=False)
    o.append(cone("Hood",(0,.01,2.56),.38,.22,.58,BLACK,verts=8))
    o.append(cube("Mask",(0,-.29,2.37),(.42,.06,.22),BLACK,b=.008))
    o.append(cube("DaggerL",(-.47,-.08,1.78),(.08,.05,.72),STEEL,rot=(0,0,math.radians(-32)),b=.004))
    o.append(cube("DaggerR",(.47,-.08,1.78),(.08,.05,.72),STEEL,rot=(0,0,math.radians(32)),b=.004))
    o.append(cube("Cape",(0,.22,1.50),(.72,.10,1.18),BLACK,rot=(math.radians(-8),0,0),b=.012))
    export_asset(o,"Units/Human","assassin")


def build_trebuchet():
    clear_scene(); o=[]
    for x in (-1.05,1.05):
        for y in (-1.35,1.35):
            o.append(cyl("Wheel",(x,y,.45),.50,.20,WOOD_D,verts=12,rot=(0,math.pi/2,0),b=.014))
    o.append(cube("RailL",(-.72,0,.78),(.30,3.3,.30),WOOD,b=.026))
    o.append(cube("RailR",(.72,0,.78),(.30,3.3,.30),WOOD,b=.026))
    for x in (-.78,.78):
        o.append(cube("Post",(x,.18,2.38),(.30,.34,3.65),WOOD_D,rot=(0,math.radians(-6 if x<0 else 6),0),b=.025))
    o.append(cyl("Axle",(0,.18,4.10),.14,2.1,IRON,verts=10,rot=(0,math.pi/2,0),b=.010))
    o.append(cube("ThrowArm",(0,-.20,4.28),(.28,5.1,.28),WOOD_L,rot=(math.radians(-18),0,0),b=.022))
    o.append(cube("Counterweight",(0,1.90,3.70),(1.18,.90,1.06),STONE_D,rot=(math.radians(-18),0,0),b=.04))
    o.append(cube("Sling",(0,-2.45,5.15),(.58,.68,.16),LEATHER,rot=(math.radians(-18),0,0),b=.018))
    export_asset(o,"Siege/Medieval","trebuchet")


def build_reinforcement_cart():
    clear_scene(); o=[]
    o.append(cube("Bed",(0,0,.72),(2.25,3.0,.28),WOOD,b=.025))
    for x in (-1.0,1.0):
        for y in (-1.05,1.05):
            o.append(cyl("Wheel",(x,y,.45),.48,.18,WOOD_D,verts=12,rot=(0,math.pi/2,0),b=.014))
    for x in (-.9,.9):
        o.append(cube("Rail",(x,0,1.25),(.16,2.85,.80),WOOD_L,b=.012))
    for i in range(6):
        x=-.60+(i%3)*.60; y=-.55+(i//3)*1.10
        o.append(cyl(f"ReserveBase_{i}",(x,y,1.02),.22,.08,IRON,verts=10,b=.006))
        o.append(cyl(f"ReserveBody_{i}",(x,y,1.35),.10,.55,BLUE if i<3 else RED,verts=8,b=.005))
    export_asset(o,"Props/Gameplay","reinforcement_cart")


def build_reinforcement_outpost():
    clear_scene(); o=[]
    o.append(cube("Platform",(0,0,.22),(3.0,2.4,.36),STONE_D,b=.025))
    for x in (-1.15,1.15):
        o.append(cube("Post",(x,.65,1.65),(.20,.20,2.75),WOOD_D,b=.014))
    o.append(cube("RoofBeam",(0,.65,2.85),(2.65,.22,.20),WOOD_L,b=.014))
    o.append(cone("Roof",(0,.65,3.45),1.85,.15,1.18,RED,verts=4,rot=(0,0,math.radians(45))))
    o.append(cube("SupplyCrateA",(-.55,-.40,.72),(.85,.72,.72),WOOD,b=.018))
    o.append(cube("SupplyCrateB",(.48,-.45,.64),(.70,.62,.58),WOOD_L,b=.018))
    o.append(cyl("BannerPole",(0,-.92,2.0),.035,2.7,IRON,verts=8,b=.004))
    o.append(cube("Banner",(0,-.96,2.40),(.70,.045,1.02),BLUE,b=.006))
    export_asset(o,"Props/Gameplay","reinforcement_outpost")


def build_trap_spikes():
    clear_scene(); o=[]
    o.append(cube("Pit",(0,0,.05),(2.8,2.1,.10),BLACK,b=.005))
    for i in range(14):
        x=-1.15+(i%7)*.38; y=-.55+(i//7)*1.05
        h=.65+(i%3)*.10
        o.append(cone(f"Spike_{i}",(x,y,h*.5+.08),.10,0,h,WOOD_D,verts=5,
                      rot=(math.radians((i%2)*5),math.radians((i%3)*4),0)))
    for x in (-1.3,1.3):
        o.append(cube("Edge",(x,0,.16),(.16,2.25,.20),WOOD,b=.01))
    export_asset(o,"Props/Gameplay","trap_spikes")


def build_castle_brazier():
    clear_scene(); o=[]
    o.append(cyl("Foot",(0,0,.08),.40,.14,IRON,verts=10,b=.008))
    o.append(cyl("Stem",(0,0,.58),.09,.92,IRON,verts=8,b=.006))
    o.append(cone("Bowl",(0,0,1.10),.52,.34,.32,IRON,verts=10))
    for i in range(3):
        o.append(ico(f"Flame_{i}",((i-1)*.10,0,1.44+(.10 if i==1 else 0)),(.10,.09,.25),FIRE,sub=1))
    export_asset(o,"Props/Gameplay","castle_brazier")


def build_throne():
    clear_scene(); o=[]
    o.append(cube("Seat",(0,0,.82),(1.35,1.05,.24),WOOD,b=.025))
    o.append(cube("Back",(0,.42,2.18),(1.45,.28,2.9),WOOD_D,b=.025))
    for x in (-.62,.62):
        o.append(cube("Post",(x,.42,2.18),(.18,.22,3.2),WOOD_L,b=.014))
        o.append(cone("Finial",(x,.42,3.88),.16,0,.34,BRASS,verts=6))
    o.append(cube("Cushion",(0,-.05,.98),(1.12,.86,.20),RED,b=.04))
    o.append(cube("BackCushion",(0,.25,2.20),(1.02,.14,1.45),RED,b=.035))
    o.append(ico("Crest",(0,.16,3.12),(.25,.10,.28),BRASS,sub=1))
    export_asset(o,"Props/Gameplay","throne")


def build_spellbook_open():
    clear_scene(); o=[]
    o.append(cube("CoverL",(-.48,0,.10),(.94,1.25,.12),LEATHER,rot=(0,math.radians(-9),math.radians(4)),b=.018))
    o.append(cube("CoverR",(.48,0,.10),(.94,1.25,.12),LEATHER,rot=(0,math.radians(9),math.radians(-4)),b=.018))
    o.append(cube("PagesL",(-.45,-.02,.18),(.82,1.10,.08),PARCHMENT,rot=(0,math.radians(-8),math.radians(4)),b=.010))
    o.append(cube("PagesR",(.45,-.02,.18),(.82,1.10,.08),PARCHMENT,rot=(0,math.radians(8),math.radians(-4)),b=.010))
    for side,x in ((-1,-.45),(1,.45)):
        for i in range(4):
            o.append(cube(f"Rune_{side}_{i}",(x + side*(i%2)*.08,-.30+i*.18,.24),(.32,.025,.035),ARCANE,rot=(0,0,math.radians(side*6)),b=.002))
    o.append(ico("CenterGem",(0,-.02,.30),(.10,.08,.10),ARCANE,sub=1))
    export_asset(o,"Props/Gameplay","spellbook_open")


def build_mana_crystals():
    clear_scene(); o=[]
    specs=[(-.34,.04,.36,.18,.70),(-.05,-.12,.48,.22,.95),(.28,.08,.40,.19,.78),(.05,.32,.28,.15,.55)]
    for i,(x,y,z,r,h) in enumerate(specs):
        o.append(cone(f"Crystal_{i}",(x,y,z),r*.85,r*.38,h,ARCANE,verts=6,rot=(math.radians(i*5),0,math.radians(i*18))))
    o.append(ico("RockBase",(0,0,.12),(.72,.56,.18),STONE_D,sub=1))
    export_asset(o,"Props/Gameplay","mana_crystals")


def build_suspicion_dial():
    clear_scene(); o=[]
    o.append(cyl("DialBase",(0,0,.08),.70,.16,WOOD_D,verts=16,b=.016))
    o.append(cyl("DialFace",(0,0,.18),.62,.07,PARCHMENT,verts=16,b=.010))
    for i in range(9):
        a=math.radians(-120+i*30)
        o.append(cube(f"Tick_{i}",(math.cos(a)*.48,math.sin(a)*.48,.24),(.05,.14,.035),IRON,rot=(0,0,a),b=.002))
    o.append(cube("Needle",(0,-.10,.29),(.055,.46,.045),SUSPICION,rot=(0,0,math.radians(-28)),b=.003))
    o.append(cyl("Hub",(0,0,.30),.09,.08,BRASS,verts=10,b=.004))
    export_asset(o,"Props/Gameplay","suspicion_dial")


def build_karma_medallion():
    clear_scene(); o=[]
    o.append(cyl("Coin",(0,0,.08),.56,.16,BRASS,verts=18,b=.014))
    o.append(torus("Rim",(0,0,.17),.46,.045,IRON))
    o.append(cube("BalanceV",(0,0,.23),(.08,.62,.05),BONE,b=.004))
    o.append(cube("BalanceH",(0,.12,.23),(.62,.08,.05),BONE,b=.004))
    o.append(cyl("PanL",(-.25,-.15,.23),.12,.05,BONE,verts=10,b=.003))
    o.append(cyl("PanR",(.25,-.15,.23),.12,.05,BONE,verts=10,b=.003))
    export_asset(o,"Props/Gameplay","karma_medallion")


def build_cheat_stash():
    clear_scene(); o=[]
    o.append(cube("Drawer",(0,0,.30),(3.0,1.7,.60),WOOD_D,b=.025))
    o.append(cube("DrawerLip",(0,-.82,.42),(3.15,.14,.52),WOOD_L,b=.012))
    o.append(cyl("Pull",(0,-.94,.45),.10,.28,BRASS,verts=10,rot=(math.pi/2,0,0),b=.005))
    # Concealed extra miniatures and mana crystal: cheats physically exist on the table.
    for i,x in enumerate((-0.82,-.28,.28,.82)):
        o.append(cyl(f"HiddenBase_{i}",(x,.10,.68),.20,.07,IRON,verts=10,b=.004))
        o.append(cyl(f"HiddenTroop_{i}",(x,.10,.96),.09,.48,BLUE,verts=8,b=.004))
    o.append(cone("HiddenMana",(1.12,.10,.90),.16,.07,.65,ARCANE,verts=6))
    export_asset(o,"Props/Gameplay","cheat_stash")


def build_fireball_scorch():
    clear_scene(); o=[]
    o.append(cyl("Scorch",(0,0,.035),1.30,.07,BLACK,verts=16,b=.004))
    for i in range(8):
        a=i*math.tau/8; rr=.78+(i%2)*.18
        o.append(ico(f"CharRock_{i}",(math.cos(a)*rr,math.sin(a)*rr,.12),(.20,.16,.11),STONE_D,sub=1))
    for i in range(4):
        a=i*math.tau/4+0.3; rr=.45
        o.append(ico(f"Flame_{i}",(math.cos(a)*rr,math.sin(a)*rr,.32),(.10,.09,.24),FIRE,sub=1))
    export_asset(o,"Props/Gameplay","fireball_scorch")


def build_healing_rune():
    clear_scene(); o=[]
    o.append(torus("OuterRune",(0,0,.06),1.05,.055,HEAL))
    o.append(torus("InnerRune",(0,0,.07),.62,.04,HEAL))
    for i in range(6):
        a=i*math.tau/6
        o.append(cube(f"RuneBar_{i}",(math.cos(a)*.82,math.sin(a)*.82,.09),(.34,.055,.04),HEAL,rot=(0,0,a+math.pi/2),b=.002))
    o.append(ico("HealCore",(0,0,.20),(.18,.18,.18),HEAL,sub=2))
    export_asset(o,"Props/Gameplay","healing_rune")


def build_upgrade_totem():
    clear_scene(); o=[]
    o.append(cyl("Base",(0,0,.10),1.15,.20,STONE_D,verts=12,b=.016))
    colors=[BLUE,RED,PURPLE,GREEN]
    names=["Defense","Troops","Spells","Terrain"]
    for i,a in enumerate([0,math.pi/2,math.pi,3*math.pi/2]):
        x=math.cos(a)*.62; y=math.sin(a)*.62
        o.append(cyl(names[i],(x,y,.30),.28,.12,colors[i],verts=10,b=.008))
        o.append(ico(f"Gem_{i}",(x,y,.42),(.10,.10,.10),BRASS if i<2 else ARCANE,sub=1))
    o.append(cyl("Center",(0,0,.34),.30,.26,BRASS,verts=10,b=.008))
    export_asset(o,"Props/Gameplay","upgrade_totem")


jobs = [
    build_king,
    build_royal_guard,
    build_wizard,
    build_assassin,
    build_trebuchet,
    build_reinforcement_cart,
    build_reinforcement_outpost,
    build_trap_spikes,
    build_castle_brazier,
    build_throne,
    build_spellbook_open,
    build_mana_crystals,
    build_suspicion_dial,
    build_karma_medallion,
    build_cheat_stash,
    build_fireball_scorch,
    build_healing_rune,
    build_upgrade_totem,
]

print("\n[CastleCards] Generating gameplay-driven detail assets...\n")
for job in jobs:
    print(f"[CastleCards] {job.__name__}")
    job()
print(f"\n[CastleCards] Gameplay detail generation complete: {len(jobs)} assets.\n")
