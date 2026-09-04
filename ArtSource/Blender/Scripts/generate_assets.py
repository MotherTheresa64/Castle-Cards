import bpy
import math
import random
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
MODELS = ROOT / "Models"
SOURCE = ROOT / "ArtSource" / "Blender" / "Generated"
random.seed(4242)

for p in [MODELS, SOURCE]:
    p.mkdir(parents=True, exist_ok=True)


def clear_scene():
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)


def material(name, rgb, roughness=.9, metallic=0.0, emission=None):
    m = bpy.data.materials.get(name)
    if m:
        return m
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    bsdf = m.node_tree.nodes.get("Principled BSDF")
    if bsdf:
        bsdf.inputs["Base Color"].default_value = (*rgb, 1.0)
        bsdf.inputs["Roughness"].default_value = roughness
        bsdf.inputs["Metallic"].default_value = metallic
        if emission:
            key = "Emission Color" if "Emission Color" in bsdf.inputs else "Emission"
            if key in bsdf.inputs:
                bsdf.inputs[key].default_value = (*emission, 1.0)
            if "Emission Strength" in bsdf.inputs:
                bsdf.inputs["Emission Strength"].default_value = 5.0
    return m

STONE = material("CC_Stone", (0.34, .33, .31), .98)
STONE_HI = material("CC_StoneHi", (.45, .43, .39), .98)
STONE_LO = material("CC_StoneLo", (.19, .20, .20), .99)
WOOD = material("CC_Wood", (.28, .12, .045), .93)
WOOD_HI = material("CC_WoodHi", (.43, .22, .075), .91)
WOOD_LO = material("CC_WoodLo", (.11, .04, .018), .97)
IRON = material("CC_Iron", (.055, .06, .065), .48, .83)
STEEL = material("CC_Steel", (.26, .28, .30), .43, .74)
BRONZE = material("CC_Bronze", (.34, .19, .06), .55, .55)
BLUE = material("CC_Blue", (.035, .095, .26), .98)
RED = material("CC_Red", (.31, .032, .024), .98)
TAN = material("CC_Tan", (.34, .27, .17), .98)
LEATHER = material("CC_Leather", (.17, .065, .025), .95)
SKIN = material("CC_Skin", (.66, .42, .28), .92)
GREEN_D = material("CC_GreenD", (.055, .15, .055), .99)
GREEN_M = material("CC_GreenM", (.095, .245, .075), .99)
GREEN_L = material("CC_GreenL", (.14, .33, .095), .99)
FLAME = material("CC_Flame", (.95, .22, .02), .25, 0.0, emission=(1.0, .12, 0.0))


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
    bpy.context.view_layer.objects.active = objs[0]
    bpy.ops.export_scene.gltf(filepath=str(out_dir / f"{filename}.glb"), export_format='GLB', use_selection=True, export_materials='EXPORT', export_animations=False, export_yup=True)
    print(f"[CastleCards] exported {rel_dir}/{filename}.glb")


def masonry_face(o, prefix, y, width, height, z0=0.35, rows=6):
    row_h = height / rows
    for r in range(rows):
        count = 6
        bw = width / count
        offset = bw*.5 if r % 2 else 0
        for i in range(count+1):
            x = -width/2 + i*bw + offset
            if x < -width/2+.05 or x > width/2-.05:
                continue
            o.append(cube(f"{prefix}_{r}_{i}", (x,y,z0+row_h*(r+.5)), (bw*.83,.07,row_h*.72), random.choice((STONE,STONE,STONE_HI,STONE_LO)), b=.009))


def build_gatehouse():
    clear_scene(); o=[]
    for cx in (-2.35, 2.35):
        o.append(cyl("Tower", (cx,0,2.6), 1.45, 5.2, STONE, verts=12, b=.03))
        o.append(cyl("TowerFoot", (cx,0,.25), 1.62, .48, STONE_LO, verts=12, b=.02))
        for j in range(9):
            a = j*math.tau/9
            o.append(cube("Merlon", (cx+math.cos(a)*1.34, math.sin(a)*1.34, 5.55), (.48,.62,.74), STONE, rot=(0,0,a), b=.025))
    o.append(cube("GateLeft", (-1.18,0,2.05), (1.05,1.45,4.1), STONE, b=.035))
    o.append(cube("GateRight", (1.18,0,2.05), (1.05,1.45,4.1), STONE, b=.035))
    o.append(cube("Lintel", (0,0,4.10), (2.4,1.45,1.05), STONE, b=.035))
    for i,x in enumerate((-0.85,-.56,-.28,0,.28,.56,.85)):
        o.append(cube(f"Port_{i}", (x,-.78,1.55), (.055,.07,3.0), IRON, b=.004))
    for z in (.55,1.15,1.75,2.35,2.95):
        o.append(cube("PortH", (0,-.78,z), (1.85,.07,.055), IRON, b=.004))
    o.append(cyl("FlagPole", (0,-.82,5.25), .035, 1.8, IRON, verts=8))
    o.append(cube("Flag", (0,-.88,5.25), (.85,.045,1.05), RED, b=.008))
    for x in (-1.15,1.15):
        o.append(ico("Flame", (x,-.84,3.25), (.09,.09,.18), FLAME))
    export_asset(o, "Castles/Medieval", "castle_gatehouse")


def build_tower():
    clear_scene(); o=[]
    o.append(cyl("Tower", (0,0,2.65), 1.65, 5.3, STONE, verts=12, b=.03))
    o.append(cyl("Foot", (0,0,.25), 1.82, .5, STONE_LO, verts=12, b=.02))
    for j in range(10):
        a=j*math.tau/10
        o.append(cube("Merlon", (math.cos(a)*1.53, math.sin(a)*1.53,5.65), (.48,.64,.78), STONE, rot=(0,0,a), b=.025))
    o.append(cyl("Pole", (0,-1.72,4.85), .035,1.6,IRON,verts=8))
    o.append(cube("Banner", (0,-1.78,4.78), (.78,.045,1.0), BLUE,b=.008))
    export_asset(o, "Castles/Medieval", "castle_tower")


def build_wall():
    clear_scene(); o=[]
    o.append(cube("Core", (0,0,1.55), (5.4,1.05,3.1), STONE,b=.035))
    o.append(cube("Foot", (0,0,.25), (5.7,1.25,.48), STONE_LO,b=.02))
    masonry_face(o,"StoneFront",-.56,5.1,2.65)
    masonry_face(o,"StoneBack",.56,5.1,2.65)
    for x in (-2.35,-1.18,0,1.18,2.35):
        o.append(cube("Merlon", (x,0,3.55), (.58,1.05,.76), STONE,b=.025))
    export_asset(o, "Castles/Medieval", "castle_wall")


def build_tree():
    clear_scene(); o=[]
    o.append(cyl("TrunkLow", (0,0,.9), .42,1.8,WOOD_LO,verts=9,b=.01))
    o.append(cyl("TrunkHigh", (0,0,2.0), .30,1.35,WOOD,verts=9,b=.01))
    for i,a in enumerate((0,.9,1.8,2.7,3.6,4.5,5.4)):
        o.append(cube(f"Root_{i}", (math.cos(a)*.38,math.sin(a)*.38,.12), (.9,.15,.15), WOOD_LO, rot=(0,0,a), b=.01))
    canopy=[((0,0,3.7),(1.2,1.05,.85),GREEN_D),((-.8,.05,3.8),(.85,.78,.7),GREEN_M),((.8,.05,3.85),(.85,.78,.7),GREEN_M),((-.35,-.65,4.2),(.72,.68,.62),GREEN_L),((.35,.68,4.25),(.72,.68,.62),GREEN_L),((0,.05,4.65),(.85,.78,.66),GREEN_M)]
    for i,(loc,scale,m) in enumerate(canopy):
        o.append(ico(f"Leaf_{i}",loc,scale,m,sub=1,rot=(random.random(),random.random(),random.random())))
    export_asset(o, "Terrain/Medieval", "oak_tree")


def miniature_base(o):
    o.append(cyl("Base", (0,0,.08), .72,.16,IRON,verts=16,b=.018))
    o.append(cyl("BaseTop", (0,0,.19), .63,.12,STONE_LO,verts=16,b=.014))


def miniature_body(o, cloth):
    for x in (-.18,.18):
        o.append(cube("Boot", (x,-.02,.46), (.24,.32,.25),LEATHER,b=.02))
        o.append(cyl("Leg", (x,0,.82), .12,.62,cloth,verts=8,b=.008))
    o.append(cone("Tunic", (0,0,1.48), .46,.36,1.02,cloth,verts=8))
    o.append(cube("Belt", (0,-.01,1.33), (.78,.52,.10),LEATHER,b=.01))
    o.append(ico("Shoulders", (0,0,1.90), (.52,.36,.32),cloth,sub=1))
    o.append(ico("Head", (0,-.01,2.36), (.29,.27,.33),SKIN,sub=2))
    o.append(ico("Helmet", (0,0,2.57), (.34,.32,.24),STEEL,sub=1))
    o.append(cyl("HelmetRim", (0,0,2.53), .34,.07,IRON,verts=10,b=.006))


def shield(o, x, color):
    o.append(cyl("Shield", (x,-.20,1.48), .54,.11,color,verts=12,rot=(math.pi/2,0,0),b=.012))
    o.append(cyl("Boss", (x,-.28,1.48), .15,.10,STEEL,verts=10,rot=(math.pi/2,0,0),b=.008))


def build_spearman():
    clear_scene(); o=[]; miniature_base(o); miniature_body(o,BLUE)
    o.append(cyl("ArmL", (-.43,0,1.72), .10,.76,SKIN,verts=8,rot=(0,math.radians(-12),math.radians(-20))))
    o.append(cyl("ArmR", (.43,0,1.80), .10,.76,SKIN,verts=8,rot=(0,math.radians(12),math.radians(20))))
    shield(o,-.58,BLUE)
    o.append(cyl("Spear", (.62,-.06,2.0), .042,3.25,WOOD_HI,verts=8,rot=(math.radians(-4),0,math.radians(-4))))
    o.append(cone("SpearHead", (.74,-.10,3.64), .12,0,.40,STEEL,verts=4))
    export_asset(o,"Units/Human","spearman")


def build_swordsman():
    clear_scene(); o=[]; miniature_base(o); miniature_body(o,RED)
    shield(o,-.58,RED)
    o.append(cube("Blade", (.56,-.06,2.18), (.09,.05,1.30),STEEL,rot=(0,0,math.radians(-18)),b=.005))
    o.append(cube("Guard", (.45,-.06,1.62), (.44,.07,.07),BRONZE,rot=(0,0,math.radians(-18)),b=.005))
    export_asset(o,"Units/Human","swordsman")


def build_archer():
    clear_scene(); o=[]; miniature_base(o); miniature_body(o,TAN)
    o.append(cube("BowUpper", (-.60,-.08,2.10), (.07,.05,.85),WOOD_HI,rot=(0,0,math.radians(-18)),b=.004))
    o.append(cube("BowLower", (-.60,-.08,1.36), (.07,.05,.85),WOOD_HI,rot=(0,0,math.radians(18)),b=.004))
    o.append(cyl("Arrow", (.42,-.08,1.92), .018,1.35,WOOD_HI,verts=6,rot=(0,math.radians(90),0),b=.002))
    export_asset(o,"Units/Human","archer")


def build_catapult():
    clear_scene(); o=[]
    for x in (-.92,.92):
        for y in (-.98,.98):
            o.append(cyl("Wheel", (x,y,.42), .44,.18,WOOD_LO,verts=12,rot=(0,math.pi/2,0),b=.014))
    o.append(cube("Frame", (0,0,.72), (1.7,2.1,.30),WOOD,b=.025))
    for x in (-.66,.66):
        o.append(cube("Post", (x,.10,1.85), (.24,.26,2.45),WOOD_LO,rot=(0,math.radians(-7 if x<0 else 7),0),b=.02))
    o.append(cyl("Axle", (0,.10,2.85), .12,1.75,IRON,verts=10,rot=(0,math.pi/2,0),b=.01))
    o.append(cube("Arm", (0,-.35,3.10), (.24,3.7,.26),WOOD_HI,rot=(math.radians(-18),0,0),b=.02))
    o.append(cube("Bucket", (0,-2.0,3.55), (.65,.72,.25),LEATHER,rot=(math.radians(-18),0,0),b=.025))
    export_asset(o,"Siege/Medieval","catapult")


def build_barrel():
    clear_scene(); o=[]
    for i,(z,r) in enumerate(((.18,.56),(.55,.63),(.95,.66),(1.35,.63),(1.72,.56))):
        o.append(cyl(f"Body_{i}",(0,0,z),r,.38,WOOD if i%2 else WOOD_HI,verts=12,b=.015))
    for z in (.18,.78,1.38,1.72):
        o.append(cyl("Band",(0,0,z),.68,.08,IRON,verts=12,b=.008))
    export_asset(o,"Props/Containers","barrel")


def build_shelf():
    clear_scene(); o=[]
    o.append(cube("Back",(0,.18,2.0),(3.7,.18,4.0),WOOD_LO,b=.02))
    for z in (.35,1.4,2.45,3.5):
        o.append(cube("Shelf",(0,0,z),(3.8,.72,.18),WOOD,b=.018))
    for x in (-1.7,1.7):
        o.append(cube("Side",(x,0,2.0),(.20,.72,4.0),WOOD_HI,b=.018))
    export_asset(o,"Tavern/Furniture","shelf")


jobs=[build_gatehouse,build_tower,build_wall,build_tree,build_spearman,build_swordsman,build_archer,build_catapult,build_barrel,build_shelf]
print("\n[CastleCards] Generating production starter assets...\n")
for job in jobs:
    job()
print("\n[CastleCards] Asset generation complete.\n")
