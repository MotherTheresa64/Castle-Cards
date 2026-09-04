import bpy
import math
from pathlib import Path
from mathutils import Vector

ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / "Models" / "Hero"
SRC = ROOT / "ArtSource" / "Blender" / "Hero"
OUT.mkdir(parents=True, exist_ok=True)
SRC.mkdir(parents=True, exist_ok=True)


def material(name, rgb, roughness=.92, metallic=0.0):
    m=bpy.data.materials.get(name)
    if m:
        return m
    m=bpy.data.materials.new(name)
    m.use_nodes=True
    bsdf=m.node_tree.nodes.get("Principled BSDF")
    if bsdf:
        if "Base Color" in bsdf.inputs: bsdf.inputs["Base Color"].default_value=(*rgb,1.0)
        if "Roughness" in bsdf.inputs: bsdf.inputs["Roughness"].default_value=roughness
        if "Metallic" in bsdf.inputs: bsdf.inputs["Metallic"].default_value=metallic
    return m

WOOD_D=material("HQT_WoodDark",(.055,.020,.010),.95)
WOOD=material("HQT_Wood",(.17,.064,.020),.91)
WOOD_L=material("HQT_WoodLight",(.30,.13,.042),.87)
IRON=material("HQT_Iron",(.045,.050,.058),.40,.84)
STEEL=material("HQT_Steel",(.31,.33,.34),.38,.70)
BRONZE=material("HQT_Bronze",(.38,.20,.055),.50,.54)
STONE_D=material("HQT_StoneDark",(.17,.18,.18),.98)
BLUE=material("HQT_Blue",(.035,.095,.30),.98)
RED=material("HQT_Red",(.34,.032,.024),.98)
TAN=material("HQT_Tan",(.30,.22,.13),.98)
CLOTH_D=material("HQT_ClothDark",(.042,.035,.050),.99)
LEATHER=material("HQT_Leather",(.16,.050,.018),.95)
SKIN=material("HQT_Skin",(.58,.36,.24),.88)
BONE=material("HQT_Bone",(.64,.58,.45),.96)


def clear_scene():
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)


def assign(o,m):
    if hasattr(o.data,"materials"): o.data.materials.append(m)


def flat(o):
    if hasattr(o.data,"polygons"):
        for p in o.data.polygons: p.use_smooth=False


def bevel(o,width=.02):
    if width<=0: return o
    bpy.context.view_layer.objects.active=o
    o.select_set(True)
    mod=o.modifiers.new("HQTBevel","BEVEL")
    mod.width=width; mod.segments=1
    try: mod.affect='EDGES'
    except Exception: pass
    try: bpy.ops.object.modifier_apply(modifier=mod.name)
    except Exception: pass
    return o


def cube(name,loc,dims,mat,rot=(0,0,0),b=.02):
    bpy.ops.mesh.primitive_cube_add(location=loc,rotation=rot)
    o=bpy.context.object; o.name=name; o.dimensions=dims
    bpy.ops.object.transform_apply(location=False,rotation=False,scale=True)
    assign(o,mat); flat(o); bevel(o,b); return o


def cyl(name,loc,radius,depth,mat,verts=10,rot=(0,0,0),b=.01):
    bpy.ops.mesh.primitive_cylinder_add(vertices=verts,radius=radius,depth=depth,location=loc,rotation=rot)
    o=bpy.context.object; o.name=name; assign(o,mat); flat(o); bevel(o,b); return o


def cone(name,loc,r1,r2,depth,mat,verts=8,rot=(0,0,0)):
    bpy.ops.mesh.primitive_cone_add(vertices=verts,radius1=r1,radius2=r2,depth=depth,location=loc,rotation=rot)
    o=bpy.context.object; o.name=name; assign(o,mat); flat(o); return o


def ico(name,loc,scale,mat,sub=1,rot=(0,0,0)):
    bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=sub,radius=1.0,location=loc,rotation=rot)
    o=bpy.context.object; o.name=name; o.scale=scale
    bpy.ops.object.transform_apply(location=False,rotation=False,scale=True)
    assign(o,mat); flat(o); return o


def torus(name,loc,major,minor,mat,rot=(0,0,0),major_segments=12,minor_segments=4):
    bpy.ops.mesh.primitive_torus_add(major_radius=major,minor_radius=minor,major_segments=major_segments,minor_segments=minor_segments,location=loc,rotation=rot)
    o=bpy.context.object; o.name=name; assign(o,mat); flat(o); return o


def beam(name,a,b,radius,mat,verts=8):
    a=Vector(a); b=Vector(b); d=b-a; mid=(a+b)*.5
    bpy.ops.mesh.primitive_cylinder_add(vertices=verts,radius=radius,depth=d.length,location=mid)
    o=bpy.context.object; o.name=name; o.rotation_mode='QUATERNION'; o.rotation_quaternion=Vector((0,0,1)).rotation_difference(d.normalized())
    assign(o,mat); flat(o); bevel(o,radius*.08); return o


def export_asset(objs,name):
    bpy.ops.object.select_all(action='DESELECT')
    for o in objs: o.select_set(True)
    if objs: bpy.context.view_layer.objects.active=objs[0]
    bpy.ops.wm.save_as_mainfile(filepath=str(SRC/f"{name}.blend"))
    bpy.ops.export_scene.gltf(filepath=str(OUT/f"{name}.glb"),export_format='GLB',use_selection=True,export_materials='EXPORT',export_normals=True,export_animations=False,export_yup=True)
    print(f"[CastleCards HQT] Exported {name}")


def build_table():
    clear_scene(); o=[]
    # Table top at local Z=0.5. Spawn in Godot at Y=-0.32, Z=-3.1.
    o.append(cube("Body",(0,0,0),(30.2,27.0,1.0),WOOD,b=.17))
    # Individual top boards create grain-like breakup even without textures.
    board_w=30.0/18
    for i in range(18):
        x=-15.0+board_w*(i+.5)
        m=(WOOD_D,WOOD,WOOD_L)[i%3]
        o.append(cube(f"TopBoard{i}",(x,0,.56),(board_w-.028,26.65,.12),m,b=.025))
    # Battlefield inset is 1.9 units toward the far side in Blender Y -> Godot -Z.
    cy=1.90; w=23.1; d=18.55
    o.append(cube("BoardWell",(0,cy,.69),(w,d,.16),CLOTH_D,b=.10))
    for y in (cy-d/2+.18,cy+d/2-.18):
        o.append(cube(f"BoardRailY{y}",(0,y,.88),(w-.25,.34,.27),WOOD_L,b=.045))
    for x in (-w/2+.18,w/2-.18):
        o.append(cube(f"BoardRailX{x}",(x,cy,.88),(.34,d-.25,.27),WOOD_L,b=.045))
    # Thick outer lip.
    for y in (-13.05,13.05):
        o.append(cube(f"OuterY{y}",(0,y,.78),(29.55,.68,.40),WOOD_D,b=.065))
        o.append(cube(f"InlayY{y}",(0,y,.99),(28.55,.12,.07),BRONZE,b=.015))
    for x in (-14.28,14.28):
        o.append(cube(f"OuterX{x}",(x,0,.78),(.68,25.6,.40),WOOD_D,b=.065))
    # Corner plates and rivets.
    for i,(x,y) in enumerate(((-14.05,-12.84),(14.05,-12.84),(-14.05,12.84),(14.05,12.84))):
        o.append(cube(f"Plate{i}",(x,y,1.02),(.82,.82,.10),IRON,b=.045))
        for j,(dx,dy) in enumerate(((-.23,-.23),(.23,-.23),(-.23,.23),(.23,.23))):
            o.append(ico(f"Rivet{i}_{j}",(x+dx,y+dy,1.10),(.055,.055,.040),BRONZE,sub=1))
    # Near carved/runic strip.
    for i in range(11):
        x=-10+i*2.0
        o.append(cube(f"Rune{i}",(x,-12.88,1.08),(1.02,.055,.055),BRONZE,rot=(0,0,math.radians(10 if i%2==0 else -10)),b=.010))
    export_asset(o,"war_table_hero")


def base(o):
    o.append(cyl("Base",(0,0,.08),.76,.16,IRON,verts=18,b=.018))
    o.append(cyl("BaseStone",(0,0,.19),.67,.12,STONE_D,verts=18,b=.014))
    o.append(torus("BaseRim",(0,0,.25),.61,.033,BRONZE,major_segments=18,minor_segments=4))


def body(o,cloth,cape=True,hood=False):
    for side,x in (("L",-.19),("R",.19)):
        o.append(cube(f"Boot{side}",(x,-.04,.47),(.25,.35,.24),LEATHER,b=.023))
        o.append(cyl(f"Leg{side}",(x,0,.83),.12,.62,CLOTH_D,verts=8,b=.009))
    o.append(cone("Tunic",(0,0,1.49),.48,.36,1.02,cloth,verts=9))
    o.append(cube("Belt",(0,-.02,1.32),(.82,.56,.11),LEATHER,b=.012))
    o.append(cube("Buckle",(0,-.32,1.32),(.14,.06,.14),BRONZE,b=.007))
    o.append(ico("Shoulders",(0,0,1.93),(.54,.36,.31),cloth,sub=1))
    if cape:
        o.append(cone("Cape",(0,.25,1.43),.43,.30,1.18,RED,verts=6,rot=(math.radians(-7),0,0)))
    o.append(ico("Head",(0,-.02,2.39),(.29,.28,.33),SKIN,sub=2))
    if hood:
        o.append(ico("Hood",(0,.03,2.48),(.38,.36,.42),TAN,sub=1))
        o.append(ico("FaceOpening",(0,-.33,2.40),(.22,.07,.22),SKIN,sub=1))
    else:
        o.append(ico("Helmet",(0,0,2.60),(.35,.33,.24),STEEL,sub=1))
        o.append(cyl("HelmetRim",(0,0,2.54),.35,.07,IRON,verts=10,b=.005))
        o.append(cube("Nasal",(0,-.35,2.45),(.05,.05,.31),STEEL,b=.003))


def build_spearman():
    clear_scene(); o=[]; base(o); body(o,BLUE,True,False)
    o.append(beam("ArmL",(-.43,-.02,1.80),(-.63,-.18,1.45),.10,BLUE)); o.append(beam("ArmR",(.43,-.02,1.84),(.64,-.12,1.62),.10,BLUE))
    o.append(cyl("Shield",(-.68,-.23,1.48),.58,.12,BLUE,verts=14,rot=(math.pi/2,0,0),b=.010)); o.append(torus("ShieldRim",(-.68,-.30,1.48),.54,.042,IRON,rot=(math.pi/2,0,0),major_segments=14,minor_segments=4)); o.append(cyl("ShieldBoss",(-.68,-.34,1.48),.16,.12,STEEL,verts=10,rot=(math.pi/2,0,0),b=.007))
    o.append(cyl("Spear",(.66,-.12,2.02),.043,3.50,WOOD_L,verts=8,rot=(math.radians(-3),0,math.radians(-4)),b=.003)); o.append(cone("SpearHead",(.78,-.16,3.77),.13,0,.42,STEEL,verts=4,rot=(math.radians(-3),0,math.radians(-4))))
    export_asset(o,"spearman_hero")


def build_archer():
    clear_scene(); o=[]; base(o); body(o,TAN,False,True)
    o.append(beam("ArmL",(-.42,-.04,1.78),(-.70,-.12,1.94),.095,TAN)); o.append(beam("ArmR",(.42,-.04,1.82),(.72,-.10,2.02),.095,TAN))
    o.append(beam("BowUpper",(-.74,-.14,1.93),(-.88,-.12,2.78),.032,WOOD_L,6)); o.append(beam("BowMid",(-.74,-.14,1.93),(-.92,-.12,1.92),.032,WOOD_L,6)); o.append(beam("BowLower",(-.92,-.12,1.92),(-.76,-.12,1.03),.032,WOOD_L,6)); o.append(beam("StringA",(-.88,-.12,2.78),(-.92,-.17,1.92),.012,BONE,4)); o.append(beam("StringB",(-.92,-.17,1.92),(-.76,-.12,1.03),.012,BONE,4))
    o.append(cyl("Quiver",(.36,.28,1.48),.15,.92,LEATHER,verts=8,rot=(math.radians(8),0,math.radians(-18)),b=.006))
    for i in range(5): o.append(cyl(f"Arrow{i}",(.24+i*.055,.30,2.02),.014,.66,WOOD_L,verts=6,rot=(math.radians(8),0,math.radians(-18)),b=.002))
    export_asset(o,"archer_hero")


def build_swordsman():
    clear_scene(); o=[]; base(o); body(o,RED,True,False)
    o.append(beam("ArmL",(-.43,-.02,1.78),(-.62,-.16,1.47),.10,RED)); o.append(beam("ArmR",(.43,-.02,1.84),(.65,-.12,1.70),.10,RED))
    o.append(cyl("Shield",(-.67,-.23,1.50),.56,.12,RED,verts=12,rot=(math.pi/2,0,0),b=.010)); o.append(torus("ShieldRim",(-.67,-.30,1.50),.52,.040,IRON,rot=(math.pi/2,0,0),major_segments=12,minor_segments=4))
    o.append(cube("Blade",(.82,-.11,2.32),(.10,.055,1.35),STEEL,rot=(0,0,math.radians(-18)),b=.003)); o.append(cube("Guard",(.61,-.11,1.77),(.46,.08,.08),BRONZE,rot=(0,0,math.radians(-18)),b=.004)); o.append(cyl("Grip",(.52,-.11,1.60),.044,.32,LEATHER,verts=8,rot=(0,0,math.radians(-18)),b=.003))
    export_asset(o,"swordsman_hero")


jobs=[build_table,build_spearman,build_archer,build_swordsman]
print("\n[CastleCards HQT] Generating hero tabletop set...\n")
for fn in jobs:
    print(f"[CastleCards HQT] {fn.__name__}")
    fn()
print(f"\n[CastleCards HQT] Complete: {len(jobs)} assets generated.\n")
