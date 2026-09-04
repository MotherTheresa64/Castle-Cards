import bpy
import math
import random
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
MODELS = ROOT / "Models"
SOURCE = ROOT / "ArtSource" / "Blender" / "GeneratedDetails"
random.seed(9042026)

for p in [MODELS, SOURCE]:
    p.mkdir(parents=True, exist_ok=True)


def clear_scene():
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)


def material(name, rgb, roughness=.9, metallic=0.0, emission=None, emission_strength=5.0):
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


STONE = material("CCD_Stone", (.31,.30,.29), .98)
STONE_HI = material("CCD_StoneHi", (.43,.41,.37), .98)
STONE_LO = material("CCD_StoneLo", (.15,.16,.17), .99)
MORTAR = material("CCD_Mortar", (.10,.105,.105), 1.0)
WOOD = material("CCD_Wood", (.25,.10,.036), .94)
WOOD_HI = material("CCD_WoodHi", (.39,.19,.060), .92)
WOOD_LO = material("CCD_WoodLo", (.085,.030,.012), .98)
IRON = material("CCD_Iron", (.050,.055,.062), .50, .80)
STEEL = material("CCD_Steel", (.26,.28,.30), .44, .70)
BRONZE = material("CCD_Bronze", (.34,.18,.055), .58, .52)
BLUE = material("CCD_Blue", (.030,.082,.24), .98)
RED = material("CCD_Red", (.30,.028,.020), .98)
TAN = material("CCD_Tan", (.31,.24,.145), .98)
CREAM = material("CCD_Cream", (.62,.51,.31), .98)
LEATHER = material("CCD_Leather", (.14,.050,.019), .95)
SKIN = material("CCD_Skin", (.62,.36,.22), .93)
HAIR = material("CCD_Hair", (.045,.022,.012), .99)
GREEN_D = material("CCD_GreenDark", (.040,.115,.040), .99)
GREEN_M = material("CCD_GreenMid", (.075,.20,.060), .99)
GREEN_L = material("CCD_GreenLight", (.12,.29,.075), .99)
ROCK = material("CCD_Rock", (.235,.245,.24), .99)
RIVER = material("CCD_River", (.035,.12,.20), .82)
WAX = material("CCD_Wax", (.66,.54,.30), .98)
GLASS_G = material("CCD_GlassGreen", (.055,.19,.10), .55)
GLASS_B = material("CCD_GlassBlue", (.045,.12,.17), .55)
PARCHMENT = material("CCD_Parchment", (.53,.37,.19), .98)
FLAME = material("CCD_Flame", (.96,.22,.02), .22, 0.0, emission=(1.0,.11,.0), emission_strength=7.0)


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
    mod = o.modifiers.new("DetailBevel", "BEVEL")
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
        export_yup=True
    )
    print(f"[CastleCards Details] exported {rel_dir}/{filename}.glb")


# -----------------------------------------------------------------------------
# Terrain and battlefield clutter
# -----------------------------------------------------------------------------

def build_pine_tree():
    clear_scene(); o=[]
    o.append(cyl("Trunk", (0,0,1.85), .28,3.7,WOOD_LO,verts=9,b=.01))
    layers=[(1.8,1.45,.82,GREEN_D),(2.45,1.25,.78,GREEN_M),(3.05,1.03,.72,GREEN_D),(3.60,.82,.64,GREEN_L),(4.08,.58,.52,GREEN_M)]
    for i,(z,r,d,m) in enumerate(layers):
        o.append(cone(f"Needles_{i}",(0,0,z),r,.10,d,m,verts=8))
    for i in range(5):
        a=random.random()*math.tau; rr=random.uniform(.45,.92)
        o.append(ico(f"Rock_{i}",(math.cos(a)*rr,math.sin(a)*rr,.12),(.22,.18,.14),ROCK,sub=1))
    export_asset(o,"Terrain/Medieval","pine_tree")


def build_bush_cluster():
    clear_scene(); o=[]
    specs=[((0,0,.32),(.58,.50,.40),GREEN_D),((-.42,.05,.30),(.42,.38,.33),GREEN_M),((.40,-.03,.31),(.44,.39,.34),GREEN_M),((-.15,-.36,.39),(.37,.33,.31),GREEN_L),((.18,.34,.40),(.39,.34,.31),GREEN_L)]
    for i,(loc,scale,m) in enumerate(specs):
        o.append(ico(f"Leaf_{i}",loc,scale,m,sub=1,rot=(random.random(),random.random(),random.random())))
    export_asset(o,"Terrain/Medieval","bush_cluster")


def build_rock_cluster():
    clear_scene(); o=[]
    specs=[((0,0,.22),(.70,.54,.38)),((-.55,.15,.18),(.46,.39,.31)),((.52,.10,.16),(.40,.34,.27)),((.12,-.46,.14),(.34,.30,.23)),((-.18,.42,.12),(.31,.28,.20))]
    for i,(loc,scale) in enumerate(specs):
        o.append(ico(f"Rock_{i}",loc,scale,ROCK if i%2 else STONE_LO,sub=1,rot=(random.random(),random.random(),random.random())))
    export_asset(o,"Terrain/Medieval","rock_cluster")


def build_fence_section():
    clear_scene(); o=[]
    for i,x in enumerate((-2.2,-1.1,0,1.1,2.2)):
        o.append(cube(f"Post_{i}",(x,0,.62),(.16,.18,1.24),WOOD_LO,b=.012))
        o.append(cone(f"Tip_{i}",(x,0,1.36),.12,0,.28,WOOD_LO,verts=4,rot=(0,0,math.radians(45))))
    o.append(cube("RailTop",(0,0,.95),(4.7,.14,.16),WOOD_HI,b=.012))
    o.append(cube("RailBottom",(0,0,.42),(4.7,.14,.16),WOOD,b=.012))
    export_asset(o,"Terrain/Medieval","fence_section")


def build_ruin_wall():
    clear_scene(); o=[]
    heights=[1.8,2.2,1.65,2.55,1.95,1.40]
    for i,h in enumerate(heights):
        x=-2.15+i*.85
        o.append(cube(f"RuinColumn_{i}",(x,0,h/2),(.74,.78,h),random.choice((STONE,STONE,STONE_HI,STONE_LO)),rot=(0,0,random.uniform(-.035,.035)),b=.035))
    for i in range(7):
        a=random.random()*math.tau; rr=random.uniform(.8,2.5)
        o.append(ico(f"Rubble_{i}",(math.cos(a)*rr,math.sin(a)*rr,.14),(.24,.20,.18),ROCK,sub=1))
    export_asset(o,"Terrain/Medieval","ruin_wall")


def build_tent():
    clear_scene(); o=[]
    o.append(cone("Canvas",(0,0,1.15),1.45,.06,2.25,TAN,verts=4,rot=(0,0,math.radians(45))))
    o.append(cyl("Pole",(0,0,1.35),.045,2.7,WOOD_HI,verts=8,b=.005))
    o.append(cube("FlapL",(-.32,-1.02,.85),(.55,.05,1.35),RED,rot=(math.radians(8),0,math.radians(-8)),b=.008))
    o.append(cube("FlapR",(.32,-1.02,.85),(.55,.05,1.35),RED,rot=(math.radians(8),0,math.radians(8)),b=.008))
    export_asset(o,"Terrain/Medieval","tent")


def build_campfire():
    clear_scene(); o=[]
    for i,a in enumerate((0,math.pi/3,2*math.pi/3)):
        o.append(cyl(f"Log_{i}",(0,0,.18),.10,1.35,WOOD_LO,verts=8,rot=(math.pi/2,a,0),b=.008))
    for i in range(8):
        a=i*math.tau/8
        o.append(ico(f"FireStone_{i}",(math.cos(a)*.62,math.sin(a)*.62,.10),(.19,.15,.12),ROCK,sub=1))
    o.append(ico("FlameA",(-.12,0,.55),(.20,.18,.38),FLAME,sub=1))
    o.append(ico("FlameB",(.12,.03,.72),(.16,.14,.48),FLAME,sub=1))
    export_asset(o,"Terrain/Medieval","campfire")


def build_watchtower():
    clear_scene(); o=[]
    for i,(x,y) in enumerate(((-.88,-.88),(.88,-.88),(-.88,.88),(.88,.88))):
        o.append(cube(f"Post_{i}",(x,y,1.75),(.25,.25,3.5),WOOD_LO,b=.022))
    o.append(cube("Platform",(0,0,3.30),(2.55,2.55,.28),WOOD,b=.03))
    for y in (-1.06,1.06):
        o.append(cube("Rail",(0,y,3.88),(2.45,.12,.14),WOOD_HI,b=.01))
        for x in (-.95,-.32,.32,.95):
            o.append(cube("RailPost",(x,y,3.62),(.10,.10,.70),WOOD_LO,b=.008))
    o.append(cone("Roof",(0,0,4.65),1.75,.20,1.35,WOOD_LO,verts=4,rot=(0,0,math.radians(45))))
    for i in range(6):
        z=.52+i*.43
        o.append(cube(f"Rung_{i}",(0,-1.03,z),(.78,.08,.08),WOOD_HI,b=.006))
    export_asset(o,"Terrain/Medieval","watchtower")


def build_bridge_detail():
    clear_scene(); o=[]
    for i,x in enumerate([i*.52-2.6 for i in range(11)]):
        o.append(cube(f"Plank_{i}",(x,0,.18),(.46,2.75,.18),WOOD if i%2 else WOOD_HI,b=.015))
    for side,y in enumerate((-1.30,1.30)):
        for i,x in enumerate((-2.45,-1.2,0,1.2,2.45)):
            o.append(cube(f"Post_{side}_{i}",(x,y,.70),(.12,.12,1.15),WOOD_LO,b=.01))
        o.append(cube(f"Rail_{side}",(0,y,1.00),(5.25,.12,.14),WOOD_HI,b=.01))
    export_asset(o,"Terrain/Medieval","bridge_detail")


# -----------------------------------------------------------------------------
# Castle expansion
# -----------------------------------------------------------------------------

def build_castle_keep():
    clear_scene(); o=[]
    o.append(cube("KeepCore",(0,0,2.55),(4.55,4.05,5.10),STONE,b=.05))
    o.append(cube("KeepFoot",(0,0,.28),(4.90,4.35,.56),STONE_LO,b=.03))
    o.append(cube("KeepBand",(0,0,5.00),(4.80,4.25,.25),STONE_LO,b=.02))
    for x in (-1.75,-.88,0,.88,1.75):
        o.append(cube("FrontMerlon",(x,-1.75,5.50),(.52,.58,.76),STONE,b=.025))
        o.append(cube("BackMerlon",(x,1.75,5.50),(.52,.58,.76),STONE,b=.025))
    for y in (-.88,0,.88):
        o.append(cube("LeftMerlon",(-2.0,y,5.50),(.58,.52,.76),STONE,b=.025))
        o.append(cube("RightMerlon",(2.0,y,5.50),(.58,.52,.76),STONE,b=.025))
    o.append(cube("DoorInset",(0,-2.07,1.25),(1.15,.08,2.25),MORTAR,b=.015))
    for i,x in enumerate((-.42,-.21,0,.21,.42)):
        o.append(cube(f"Door_{i}",(x,-2.14,1.22),(.17,.08,2.0),WOOD,b=.01))
    for x in (-1.3,1.3):
        o.append(cube("Window",(x,-2.08,3.25),(.35,.08,.70),IRON,b=.006))
    o.append(cyl("FlagPole",(0,-1.8,5.8),.035,1.8,IRON,verts=8,b=.004))
    o.append(cube("Flag",(0,-1.86,5.9),(.82,.045,1.0),BLUE,b=.006))
    export_asset(o,"Castles/Medieval","castle_keep")


# -----------------------------------------------------------------------------
# Props and tavern dressing
# -----------------------------------------------------------------------------

def build_crate():
    clear_scene(); o=[]
    o.append(cube("CrateBody",(0,0,.62),(1.35,1.35,1.24),WOOD,b=.025))
    for z in (.13,1.11):
        o.append(cube("BandZ",(0,0,z),(1.48,1.48,.12),WOOD_HI,b=.01))
    for x in (-.55,.55):
        o.append(cube("Brace",(x,-.70,.62),(.13,.08,1.05),WOOD_LO,rot=(0,0,math.radians(20 if x<0 else -20)),b=.008))
    export_asset(o,"Props/Containers","crate")


def build_mug():
    clear_scene(); o=[]
    o.append(cyl("Cup",(0,0,.42),.33,.76,WOOD_HI,verts=10,b=.012))
    o.append(cyl("Rim",(0,0,.82),.36,.08,IRON,verts=10,b=.006))
    o.append(cube("HandleA",(.42,0,.48),(.18,.16,.48),WOOD,b=.02))
    o.append(cube("HandleB",(.54,0,.48),(.16,.16,.18),WOOD,b=.02))
    export_asset(o,"Props/Decor","mug")


def build_bottle_cluster():
    clear_scene(); o=[]
    data=[(-.28,.0,.30,.18,.54,GLASS_G),(.05,.04,.38,.15,.70,GLASS_B),(.31,-.02,.25,.20,.46,GLASS_G)]
    for i,(x,y,z,r,h,m) in enumerate(data):
        o.append(cyl(f"BottleBody_{i}",(x,y,z),r,h,m,verts=10,b=.008))
        o.append(cyl(f"BottleNeck_{i}",(x,y,z+h*.55),r*.45,h*.38,m,verts=10,b=.005))
        o.append(cyl(f"Cork_{i}",(x,y,z+h*.78),r*.38,.10,WOOD_LO,verts=8,b=.003))
    export_asset(o,"Props/Decor","bottle_cluster")


def build_candle_cluster():
    clear_scene(); o=[]
    for i,(x,y,h) in enumerate(((-.28,.08,.66),(0,-.08,.94),(.30,.07,.52))):
        o.append(cyl(f"Candle_{i}",(x,y,h/2),.09,h,WAX,verts=10,b=.006))
        o.append(cyl(f"Wick_{i}",(x,y,h+.035),.012,.08,IRON,verts=6,b=.002))
        o.append(ico(f"Flame_{i}",(x,y,h+.16),(.06,.055,.15),FLAME,sub=1))
    o.append(cyl("Plate",(0,0,.045),.56,.09,BRONZE,verts=12,b=.008))
    export_asset(o,"Props/Decor","candle_cluster")


def build_weapon_rack():
    clear_scene(); o=[]
    o.append(cube("Back",(0,.10,1.75),(3.25,.18,3.50),WOOD_LO,b=.02))
    o.append(cube("Top",(0,0,3.38),(3.45,.32,.18),WOOD,b=.014))
    o.append(cube("Mid",(0,0,1.58),(3.45,.32,.18),WOOD,b=.014))
    for i,x in enumerate((-1.02,0,1.02)):
        o.append(cube(f"Blade_{i}",(x,-.11,2.25),(.09,.055,1.38),STEEL,b=.004))
        o.append(cube(f"Guard_{i}",(x,-.11,1.56),(.48,.07,.07),BRONZE,b=.004))
        o.append(cyl(f"Grip_{i}",(x,-.11,1.34),.045,.34,LEATHER,verts=8,b=.003))
    export_asset(o,"Props/Decor","weapon_rack")


def build_shield_decor():
    clear_scene(); o=[]
    o.append(cyl("Shield",(0,0,.58),.72,.13,BLUE,verts=12,rot=(math.pi/2,0,0),b=.012))
    o.append(cyl("Boss",(0,-.08,.58),.19,.12,STEEL,verts=10,rot=(math.pi/2,0,0),b=.008))
    o.append(cube("StripeV",(0,-.075,.58),(.14,.06,1.05),STONE_HI,b=.006))
    o.append(cube("StripeH",(0,-.075,.58),(1.05,.06,.14),STONE_HI,b=.006))
    export_asset(o,"Props/Decor","shield_decor")


def build_book_stack():
    clear_scene(); o=[]
    colors=[RED,BLUE,TAN,PARCHMENT]
    for i in range(4):
        z=.10+i*.17
        o.append(cube(f"Book_{i}",(0.04*(i%2),0,z),(1.00-.05*i,.62,.13),colors[i],rot=(0,0,math.radians((-3+i*2))),b=.014))
        o.append(cube(f"Pages_{i}",(0.05,0,z),(0.82-.04*i,.55,.08),CREAM,b=.006))
    export_asset(o,"Props/Decor","book_stack")


def build_skull():
    clear_scene(); o=[]
    bone=material("CCD_Bone",(.62,.57,.44),.98)
    o.append(ico("Cranium",(0,0,.46),(.42,.38,.48),bone,sub=2))
    o.append(cube("Jaw",(0,-.08,.18),(.48,.34,.22),bone,b=.025))
    o.append(ico("EyeL",(-.15,-.32,.48),(.10,.07,.11),STONE_LO,sub=1))
    o.append(ico("EyeR",(.15,-.32,.48),(.10,.07,.11),STONE_LO,sub=1))
    export_asset(o,"Props/Decor","skull")


def build_dice_cluster():
    clear_scene(); o=[]
    for i,(x,y,z,r) in enumerate(((-.23,.05,.17,-.20),(.18,-.04,.18,.18),(.05,.30,.16,.40))):
        o.append(cube(f"Die_{i}",(x,y,z),(.30,.30,.30),CREAM,rot=(r,r*.5,r*.8),b=.035))
    export_asset(o,"Props/Decor","dice_cluster")


def build_chair():
    clear_scene(); o=[]
    o.append(cube("Seat",(0,0,1.02),(1.18,1.12,.20),WOOD,b=.025))
    for i,(x,y) in enumerate(((-.45,-.42),(.45,-.42),(-.45,.42),(.45,.42))):
        o.append(cube(f"Leg_{i}",(x,y,.50),(.16,.16,1.0),WOOD_LO,b=.014))
    o.append(cube("BackL",(-.45,.44,1.88),(.16,.16,1.65),WOOD_LO,b=.014))
    o.append(cube("BackR",(.45,.44,1.88),(.16,.16,1.65),WOOD_LO,b=.014))
    for i,z in enumerate((1.48,1.92,2.36)):
        o.append(cube(f"BackSlat_{i}",(0,.44,z),(.96,.13,.15),WOOD_HI,b=.012))
    export_asset(o,"Tavern/Furniture","chair")


def build_bench():
    clear_scene(); o=[]
    o.append(cube("Seat",(0,0,.92),(3.2,.92,.22),WOOD,b=.03))
    for i,x in enumerate((-1.18,1.18)):
        o.append(cube(f"Leg_{i}",(x,0,.46),(.30,.62,.90),WOOD_LO,b=.022))
        o.append(cube(f"Foot_{i}",(x,0,.13),(.78,.82,.18),WOOD_HI,b=.014))
    export_asset(o,"Tavern/Furniture","bench")


def build_small_table():
    clear_scene(); o=[]
    o.append(cyl("Top",(0,0,1.28),1.12,.18,WOOD,verts=12,b=.025))
    o.append(cyl("Stem",(0,0,.70),.25,1.10,WOOD_LO,verts=10,b=.018))
    for i,a in enumerate((0,math.pi/2,math.pi,3*math.pi/2)):
        o.append(cube(f"Foot_{i}",(math.cos(a)*.50,math.sin(a)*.50,.15),(1.0,.18,.18),WOOD_HI,rot=(0,0,a),b=.012))
    export_asset(o,"Tavern/Furniture","small_table")


def build_chandelier():
    clear_scene(); o=[]
    o.append(cyl("Stem",(0,0,1.2),.06,2.4,IRON,verts=8,b=.004))
    o.append(cyl("Hub",(0,0,.22),.28,.16,IRON,verts=10,b=.008))
    for i,a in enumerate([i*math.tau/6 for i in range(6)]):
        x=math.cos(a)*1.35; y=math.sin(a)*1.35
        o.append(cube(f"Arm_{i}",(x*.52,y*.52,.18),(1.35,.10,.10),IRON,rot=(0,0,a),b=.006))
        o.append(cyl(f"Cup_{i}",(x,y,.32),.18,.18,BRONZE,verts=8,b=.006))
        o.append(cyl(f"Candle_{i}",(x,y,.62),.07,.50,WAX,verts=8,b=.004))
        o.append(ico(f"Flame_{i}",(x,y,.96),(.055,.05,.14),FLAME,sub=1))
    export_asset(o,"Tavern/Lighting","chandelier")


def build_brazier():
    clear_scene(); o=[]
    o.append(cyl("Foot",(0,0,.12),.48,.18,IRON,verts=10,b=.01))
    o.append(cyl("Stem",(0,0,.72),.10,1.16,IRON,verts=8,b=.008))
    o.append(cone("Bowl",(0,0,1.35),.62,.42,.38,IRON,verts=10))
    for i in range(5):
        a=random.random()*math.tau; rr=random.uniform(.0,.30)
        o.append(ico(f"Coal_{i}",(math.cos(a)*rr,math.sin(a)*rr,1.52),(.12,.10,.08),STONE_LO,sub=1))
    o.append(ico("FlameA",(-.10,0,1.78),(.13,.11,.27),FLAME,sub=1))
    o.append(ico("FlameB",(.10,.02,1.88),(.11,.10,.35),FLAME,sub=1))
    export_asset(o,"Tavern/Lighting","brazier")


# -----------------------------------------------------------------------------
# Extra units / siege
# -----------------------------------------------------------------------------

def miniature_base(o):
    o.append(cyl("Base",(0,0,.08),.72,.16,IRON,verts=16,b=.018))
    o.append(cyl("BaseTop",(0,0,.19),.63,.12,STONE_LO,verts=16,b=.014))


def build_knight():
    clear_scene(); o=[]; miniature_base(o)
    o.append(ico("HorseBody",(0,.05,1.08),(.62,.92,.50),WOOD_LO,sub=2))
    o.append(ico("HorseChest",(0,-.62,1.18),(.48,.52,.55),WOOD,sub=1))
    o.append(ico("HorseHead",(0,-1.05,1.62),(.30,.42,.36),WOOD,sub=1,rot=(math.radians(-10),0,0)))
    o.append(cube("Muzzle",(0,-1.34,1.54),(.28,.30,.22),WOOD_HI,b=.02))
    for i,(x,y) in enumerate(((-.30,-.42),(.30,-.42),(-.30,.48),(.30,.48))):
        o.append(cyl(f"HorseLeg_{i}",(x,y,.62),.095,.78,WOOD_LO,verts=8,b=.008))
    o.append(cube("Saddle",(0,0,1.53),(.66,.65,.17),LEATHER,b=.02))
    o.append(cone("RiderTorso",(0,0,2.13),.40,.31,.86,BLUE,verts=8))
    o.append(ico("RiderHead",(0,-.02,2.78),(.26,.25,.29),SKIN,sub=2))
    o.append(ico("Helmet",(0,0,2.96),(.31,.30,.22),STEEL,sub=1))
    o.append(cyl("Lance",(.52,-.18,2.34),.038,3.55,WOOD_HI,verts=8,rot=(math.radians(-16),0,math.radians(-7)),b=.004))
    o.append(cyl("Shield",(-.48,-.16,2.20),.42,.10,BLUE,verts=10,rot=(math.pi/2,0,0),b=.01))
    export_asset(o,"Units/Human","knight")


def build_ogre():
    clear_scene(); o=[]
    o.append(cyl("Base",(0,0,.09),.84,.18,IRON,verts=16,b=.018))
    for x in (-.28,.28):
        o.append(cube("Foot",(x,-.06,.42),(.38,.52,.26),LEATHER,b=.028))
        o.append(cyl("Leg",(x,0,.82),.18,.70,GREEN_M,verts=8,b=.012))
    o.append(cone("Body",(0,0,1.64),.70,.50,1.34,GREEN_M,verts=8))
    o.append(ico("Shoulders",(0,0,2.18),(.82,.52,.42),GREEN_M,sub=1))
    o.append(ico("Head",(0,-.02,2.73),(.43,.39,.45),GREEN_L,sub=2))
    o.append(cube("Belt",(0,0,1.38),(1.05,.65,.14),LEATHER,b=.014))
    o.append(cyl("Club",(.80,-.04,1.90),.13,1.95,WOOD_LO,verts=8,rot=(math.radians(-8),0,math.radians(22)),b=.008))
    o.append(ico("ClubHead",(1.06,-.12,2.78),(.34,.29,.42),WOOD,sub=1))
    export_asset(o,"Units/Monsters","ogre")


def build_ballista():
    clear_scene(); o=[]
    for x in (-.72,.72):
        for y in (-.70,.70):
            o.append(cyl("Wheel",(x,y,.34),.36,.16,WOOD_LO,verts=12,rot=(0,math.pi/2,0),b=.012))
    o.append(cube("Frame",(0,0,.62),(1.45,1.85,.26),WOOD,b=.02))
    o.append(cyl("Turntable",(0,0,.82),.56,.18,IRON,verts=12,b=.012))
    o.append(cube("Stock",(0,-.12,1.14),(.28,2.75,.24),WOOD_HI,b=.02))
    o.append(cube("BowL",(-.72,-.98,1.20),(1.55,.14,.16),WOOD_LO,rot=(0,0,math.radians(17)),b=.014))
    o.append(cube("BowR",(.72,-.98,1.20),(1.55,.14,.16),WOOD_LO,rot=(0,0,math.radians(-17)),b=.014))
    o.append(cyl("Bolt",(0,-1.05,1.28),.03,2.75,WOOD_HI,verts=6,rot=(math.pi/2,0,0),b=.003))
    export_asset(o,"Siege/Medieval","ballista")


# -----------------------------------------------------------------------------
# Opponent hero prop
# -----------------------------------------------------------------------------

def build_seated_opponent():
    clear_scene(); o=[]
    shirt = material("CCD_OpponentShirt",(.095,.035,.050),.98)
    trouser = material("CCD_OpponentTrouser",(.055,.050,.060),.98)

    # Chair visible behind the player model.
    o.append(cube("ChairSeat",(0,.35,1.25),(3.1,2.0,.30),WOOD,b=.03))
    o.append(cube("ChairBack",(0,1.05,4.45),(3.2,.32,6.1),WOOD_LO,b=.035))
    for x in (-1.35,1.35):
        o.append(cube("ChairPost",(x,1.05,4.75),(.25,.30,6.7),WOOD_HI,b=.02))

    # Legs beneath table line.
    for x in (-.72,.72):
        o.append(cyl("Thigh",(x,.15,2.10),.43,2.25,trouser,verts=10,rot=(math.radians(72),0,0),b=.015))

    # Torso / shoulders.
    o.append(cone("Torso",(0,0,4.80),1.62,1.28,3.55,shirt,verts=10))
    o.append(ico("ShoulderMass",(0,-.05,6.00),(2.15,.72,.62),shirt,sub=1))
    o.append(cyl("Neck",(0,-.02,6.65),.42,.72,SKIN,verts=10,b=.012))

    # Head with deliberate low-poly facial planes.
    o.append(ico("Head",(0,-.05,7.55),(1.05,.90,1.17),SKIN,sub=2))
    o.append(ico("Nose",(0,-.88,7.52),(.15,.18,.24),SKIN,sub=1))
    o.append(cube("BrowL",(-.34,-.82,7.82),(.34,.07,.07),HAIR,rot=(0,0,math.radians(-4)),b=.004))
    o.append(cube("BrowR",(.34,-.82,7.82),(.34,.07,.07),HAIR,rot=(0,0,math.radians(4)),b=.004))
    o.append(ico("EyeL",(-.34,-.88,7.64),(.07,.05,.055),STONE_LO,sub=1))
    o.append(ico("EyeR",(.34,-.88,7.64),(.07,.05,.055),STONE_LO,sub=1))
    o.append(cube("Mouth",(0,-.94,7.22),(.34,.04,.055),HAIR,b=.003))

    # Hair / short beard.
    o.append(ico("HairCap",(0,.02,8.38),(1.10,.94,.58),HAIR,sub=1))
    o.append(cone("Beard",(0,-.72,6.96),.55,.16,.82,HAIR,verts=8,rot=(math.radians(8),0,0)))

    # Arms resting toward table.
    o.append(cyl("UpperArmL",(-1.70,-.05,5.30),.38,2.45,shirt,verts=10,rot=(0,math.radians(-4),math.radians(-55)),b=.012))
    o.append(cyl("UpperArmR",(1.70,-.05,5.30),.38,2.45,shirt,verts=10,rot=(0,math.radians(4),math.radians(55)),b=.012))
    o.append(cyl("ForearmL",(-2.55,-1.03,3.68),.34,2.25,SKIN,verts=10,rot=(math.radians(62),0,math.radians(-18)),b=.012))
    o.append(cyl("ForearmR",(2.55,-1.03,3.68),.34,2.25,SKIN,verts=10,rot=(math.radians(62),0,math.radians(18)),b=.012))
    o.append(ico("HandL",(-2.80,-2.05,2.85),(.48,.36,.60),SKIN,sub=1))
    o.append(ico("HandR",(2.80,-2.05,2.85),(.48,.36,.60),SKIN,sub=1))

    # Small jewelry/details.
    o.append(cyl("PendantChain",(0,-1.24,5.20),.025,1.0,BRONZE,verts=8,rot=(math.radians(18),0,0),b=.002))
    o.append(ico("Pendant",(0,-1.38,4.72),(.14,.08,.18),BRONZE,sub=1))

    export_asset(o,"Opponent","seated_opponent")


jobs = [
    build_pine_tree,
    build_bush_cluster,
    build_rock_cluster,
    build_fence_section,
    build_ruin_wall,
    build_tent,
    build_campfire,
    build_watchtower,
    build_bridge_detail,
    build_castle_keep,
    build_crate,
    build_mug,
    build_bottle_cluster,
    build_candle_cluster,
    build_weapon_rack,
    build_shield_decor,
    build_book_stack,
    build_skull,
    build_dice_cluster,
    build_chair,
    build_bench,
    build_small_table,
    build_chandelier,
    build_brazier,
    build_knight,
    build_ogre,
    build_ballista,
    build_seated_opponent,
]

print("\n[CastleCards] Generating high-detail expansion assets...\n")
for job in jobs:
    print(f"[CastleCards] {job.__name__}")
    job()
print(f"\n[CastleCards] Detail asset generation complete: {len(jobs)} assets.\n")
