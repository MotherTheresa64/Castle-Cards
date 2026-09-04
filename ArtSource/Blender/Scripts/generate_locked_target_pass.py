import bpy
import math
import random
from pathlib import Path
from mathutils import Vector

ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / "Models" / "Hero"
SRC = ROOT / "ArtSource" / "Blender" / "Hero"
OUT.mkdir(parents=True, exist_ok=True)
SRC.mkdir(parents=True, exist_ok=True)

# This pass is intentionally last in the asset pipeline.
# It locks the medieval tavern vertical slice to the approved visual targets:
# cinematic warm low-poly tavern, rich miniature battlefield, strong castle silhouettes,
# readable brunette opponent, and a physical reserve/card zone for cheating gameplay.

def material(name, rgb, roughness=.9, metallic=0.0, emission=None, emission_strength=0.0):
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

STONE_D = material("LOCK_StoneDark", (.105, .110, .112), .98)
STONE = material("LOCK_Stone", (.29, .285, .27), .97)
STONE_L = material("LOCK_StoneLight", (.43, .405, .36), .95)
STONE_WARM = material("LOCK_StoneWarm", (.35, .29, .23), .96)
MOSS = material("LOCK_Moss", (.075, .12, .055), .99)
WOOD_D = material("LOCK_WoodDark", (.040, .017, .010), .96)
WOOD = material("LOCK_Wood", (.13, .050, .020), .93)
WOOD_L = material("LOCK_WoodLight", (.245, .105, .040), .89)
IRON = material("LOCK_Iron", (.035, .040, .047), .40, .82)
STEEL = material("LOCK_Steel", (.255, .275, .29), .38, .68)
BRONZE = material("LOCK_Bronze", (.34, .18, .052), .46, .58)
GOLD = material("LOCK_Gold", (.48, .285, .07), .40, .63)
GRASS_D = material("LOCK_GrassDark", (.040, .075, .032), .99)
GRASS = material("LOCK_Grass", (.095, .155, .055), .99)
GRASS_L = material("LOCK_GrassLight", (.145, .215, .080), .99)
DIRT_D = material("LOCK_DirtDark", (.16, .085, .042), .99)
DIRT = material("LOCK_Dirt", (.275, .175, .085), .99)
WATER = material("LOCK_Water", (.030, .12, .18), .24, .05)
WATER_L = material("LOCK_WaterLight", (.075, .24, .31), .20, .04)
BLUE = material("LOCK_Blue", (.035, .080, .255), .96)
BLUE_D = material("LOCK_BlueDark", (.020, .040, .105), .98)
RED = material("LOCK_Red", (.30, .034, .022), .97)
RED_D = material("LOCK_RedDark", (.095, .018, .014), .98)
PARCHMENT = material("LOCK_Parchment", (.56, .40, .22), .96)
PARCHMENT_L = material("LOCK_ParchmentLight", (.72, .57, .34), .94)
CLOTH = material("LOCK_Cloak", (.022, .022, .028), .99)
TUNIC = material("LOCK_Tunic", (.095, .078, .060), .98)
LEATHER = material("LOCK_Leather", (.10, .035, .014), .93)
LEATHER_L = material("LOCK_LeatherLight", (.205, .072, .025), .90)
SKIN = material("LOCK_Skin", (.53, .31, .20), .87)
SKIN_S = material("LOCK_SkinShadow", (.34, .17, .105), .90)
HAIR = material("LOCK_Brunette", (.040, .016, .009), .96)
HAIR_L = material("LOCK_BrunetteLight", (.085, .032, .014), .94)
BONE = material("LOCK_Bone", (.66, .57, .43), .96)
BLACK = material("LOCK_Black", (.006, .007, .009), .99)
FIRE = material("LOCK_Fire", (1.0, .12, .008), .18, 0.0, (1.0, .06, .002), 7.0)

def clear_scene():
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)

def assign(obj, mat):
    if hasattr(obj.data, "materials"):
        obj.data.materials.append(mat)

def flat(obj):
    if hasattr(obj.data, "polygons"):
        for p in obj.data.polygons:
            p.use_smooth = False

def bevel(obj, width=.02):
    if width <= 0:
        return obj
    bpy.context.view_layer.objects.active = obj
    obj.select_set(True)
    mod = obj.modifiers.new("TargetBevel", "BEVEL")
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
    o = bpy.context.object
    o.name = name
    o.dimensions = dims
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    assign(o, mat)
    flat(o)
    bevel(o, b)
    return o

def cyl(name, loc, radius, depth, mat, verts=10, rot=(0,0,0), b=.01):
    bpy.ops.mesh.primitive_cylinder_add(vertices=verts, radius=radius, depth=depth, location=loc, rotation=rot)
    o = bpy.context.object
    o.name = name
    assign(o, mat)
    flat(o)
    bevel(o, b)
    return o

def cone(name, loc, r1, r2, depth, mat, verts=8, rot=(0,0,0)):
    bpy.ops.mesh.primitive_cone_add(vertices=verts, radius1=r1, radius2=r2, depth=depth, location=loc, rotation=rot)
    o = bpy.context.object
    o.name = name
    assign(o, mat)
    flat(o)
    return o

def ico(name, loc, scale, mat, sub=1, rot=(0,0,0)):
    bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=sub, radius=1, location=loc, rotation=rot)
    o = bpy.context.object
    o.name = name
    o.scale = scale
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    assign(o, mat)
    flat(o)
    return o

def torus(name, loc, major, minor, mat, rot=(0,0,0), major_segments=12, minor_segments=4):
    bpy.ops.mesh.primitive_torus_add(major_radius=major, minor_radius=minor, major_segments=major_segments,
        minor_segments=minor_segments, location=loc, rotation=rot)
    o = bpy.context.object
    o.name = name
    assign(o, mat)
    flat(o)
    return o

def beam(name, a, b, radius, mat, verts=8):
    a, b = Vector(a), Vector(b)
    d = b - a
    mid = (a + b) * .5
    bpy.ops.mesh.primitive_cylinder_add(vertices=verts, radius=radius, depth=d.length, location=mid)
    o = bpy.context.object
    o.name = name
    o.rotation_mode = 'QUATERNION'
    o.rotation_quaternion = Vector((0,0,1)).rotation_difference(d.normalized())
    assign(o, mat)
    flat(o)
    bevel(o, radius * .08)
    return o

def mesh_obj(name, verts, faces, mats, indices=None):
    m = bpy.data.meshes.new(name + "Mesh")
    m.from_pydata(verts, [], faces)
    m.update()
    o = bpy.data.objects.new(name, m)
    bpy.context.collection.objects.link(o)
    for mat in mats:
        m.materials.append(mat)
    if indices:
        for p, idx in zip(m.polygons, indices):
            p.material_index = idx
    flat(o)
    return o

def export_asset(objects, filename):
    bpy.ops.object.select_all(action='DESELECT')
    for o in objects:
        if o and o.name in bpy.context.view_layer.objects:
            o.select_set(True)
    if objects:
        bpy.context.view_layer.objects.active = objects[0]
    bpy.ops.wm.save_as_mainfile(filepath=str(SRC / f"{filename}.blend"))
    bpy.ops.export_scene.gltf(filepath=str(OUT / f"{filename}.glb"), export_format='GLB',
        use_selection=True, export_materials='EXPORT', export_normals=True, export_animations=False, export_yup=True)
    print(f"[CastleCards Locked Target] Exported {filename}")

def build_table():
    clear_scene()
    o = []
    o.append(cube("TableBody", (0, 0, -.18), (30.5, 27.3, .98), WOOD_D, b=.17))
    o.append(cube("TableTop", (0, 0, .38), (30.0, 26.8, .18), WOOD, b=.08))
    plank_w = 29.2 / 11
    for i in range(11):
        x = -14.6 + plank_w * (i + .5)
        mat = WOOD_L if i in (2, 7) else WOOD
        o.append(cube(f"Plank_{i}", (x, 0, .505), (plank_w - .055, 26.0, .065), mat, b=.012))
    cy = 1.55
    w, d = 23.45, 18.8
    o.append(cube("BoardBed", (0, cy, .64), (w, d, .15), GRASS_D, b=.07))
    for y in (cy - d/2, cy + d/2):
        o.append(cube(f"InnerRailY_{y:.2f}", (0, y, .82), (w+.55, .50, .32), WOOD_L, b=.05))
    for x in (-w/2, w/2):
        o.append(cube(f"InnerRailX_{x:.2f}", (x, cy, .82), (.50, d+.55, .32), WOOD_L, b=.05))
    o.append(cube("PlayerShelf", (0, 12.1, .68), (27.0, 3.55, .24), WOOD, b=.08))
    o.append(cube("PlayerLip", (0, 13.62, .84), (27.2, .18, .48), WOOD_D, b=.04))
    o.append(cube("FarLip", (0, -13.28, .72), (29.5, .55, .44), WOOD_D, b=.055))
    o.append(cube("PlayerInlay", (0, 10.55, .875), (22.4, .07, .045), BRONZE, b=.006))
    o.append(cube("FarInlay", (0, -12.95, .90), (24.8, .07, .045), BRONZE, b=.006))
    export_asset(o, "war_table_hero")

def height_at(x, y):
    h = .12*math.sin(x*.42) + .09*math.cos(y*.55) + .055*math.sin((x-y)*.70)
    h += .045*math.cos(x*.20 + y*.27)
    h += .025 * abs(x)
    return h

def ribbon(name, points, half_width, z, mat):
    verts, faces = [], []
    for i, (x, y) in enumerate(points):
        if i == 0:
            dx, dy = points[1][0]-x, points[1][1]-y
        elif i == len(points)-1:
            dx, dy = x-points[i-1][0], y-points[i-1][1]
        else:
            dx, dy = points[i+1][0]-points[i-1][0], points[i+1][1]-points[i-1][1]
        L = max(.001, math.hypot(dx, dy))
        nx, ny = -dy/L, dx/L
        verts.extend([(x+nx*half_width, y+ny*half_width, z), (x-nx*half_width, y-ny*half_width, z)])
    for i in range(len(points)-1):
        a = i*2
        faces.append((a, a+1, a+3, a+2))
    return mesh_obj(name, verts, faces, [mat], [0]*len(faces))

def add_pine(o, name, x, y, z, s):
    o.append(cyl(name+"Trunk", (x,y,z+.36*s), .095*s, .72*s, WOOD_D, verts=7, b=.004))
    for j, (dz, r) in enumerate(((.56,.44),(.86,.36),(1.12,.27))):
        o.append(cone(f"{name}Crown{j}", (x,y,z+dz*s), r*s, .035*s, .55*s,
                      (GRASS_D,GRASS,GRASS_L)[j], verts=7))

def build_battlefield():
    clear_scene()
    o=[]
    nx, ny = 45, 35
    width, depth = 22.8, 18.0
    verts=[]
    for j in range(ny):
        y=-depth/2 + depth*j/(ny-1)
        for i in range(nx):
            x=-width/2 + width*i/(nx-1)
            verts.append((x,y,height_at(x,y)))
    faces=[]
    indices=[]
    mats=[GRASS, GRASS_D, GRASS_L, DIRT, STONE_WARM]
    for j in range(ny-1):
        for i in range(nx-1):
            a=j*nx+i
            faces.extend([(a,a+1,a+1+nx),(a,a+1+nx,a+nx)])
            cx=-width/2 + width*(i+.5)/(nx-1)
            cy=-depth/2 + depth*(j+.5)/(ny-1)
            patch=math.sin(cx*.32)+.70*math.cos(cy*.39)+.35*math.sin((cx+cy)*.24)
            idx=2 if patch>.9 else 1 if patch<-.75 else 0
            if abs(cx - .18*math.sin(cy*.52)) < .62:
                idx=3
            indices.extend([idx,idx])
    o.append(mesh_obj("Terrain", verts, faces, mats, indices))
    river=[]
    for k in range(31):
        y=-8.6+k*(17.2/30)
        x=-4.4 + .75*math.sin(y*.45) + .15*math.sin(y*1.2)
        river.append((x,y))
    o.append(ribbon("River", river, .67, .045, WATER))
    o.append(ribbon("RiverHighlight", river, .29, .052, WATER_L))
    main_path=[]
    for k in range(28):
        y=-8.4+k*(16.8/27)
        x=.22*math.sin(y*.40)
        main_path.append((x,y))
    o.append(ribbon("MainRoad", main_path, .48, .075, DIRT))
    o.append(ribbon("EastRoad", [(0,-1.2),(2.0,-2.2),(4.1,-3.1),(6.1,-4.0),(8.5,-4.7)], .30, .078, DIRT_D))
    by=-.65
    rx=-4.4 + .75*math.sin(by*.45) + .15*math.sin(by*1.2)
    for i in range(10):
        x=rx-1.30+i*.29
        o.append(cube(f"BridgePlank{i}", (x,by,.28), (.25,1.75,.12), WOOD_L if i%2 else WOOD, b=.009))
    o.append(beam("BridgeRailL",(rx-1.35,by-.78,.52),(rx+1.35,by-.78,.52),.045,WOOD_D,7))
    o.append(beam("BridgeRailR",(rx-1.35,by+.78,.52),(rx+1.35,by+.78,.52),.045,WOOD_D,7))
    rng=random.Random(45811)
    tree_specs=[
        (-9.5,-6.7,.62),(-8.7,-5.9,.54),(-9.7,-4.7,.57),(-8.6,-3.7,.48),
        (-9.3,1.8,.55),(-8.7,3.0,.50),(-9.6,4.5,.62),(-8.2,5.5,.48),
        (9.0,-6.5,.58),(8.3,-5.2,.49),(9.6,-3.8,.55),(8.7,1.0,.47),
        (9.3,2.2,.53),(8.6,3.8,.47),(9.4,5.2,.59),(7.8,6.2,.45)
    ]
    for i,(x,y,s) in enumerate(tree_specs):
        add_pine(o,f"Pine{i}",x,y,height_at(x,y),s)
    for i in range(42):
        x=rng.uniform(-10.1,10.1)
        y=rng.uniform(-7.9,7.9)
        if abs(x)<1.0 or abs(x+4.4-.75*math.sin(y*.45))<1.0:
            continue
        z=height_at(x,y)
        sx=rng.uniform(.08,.26)
        o.append(ico(f"Rock{i}",(x,y,z+.06),(sx,sx*rng.uniform(.65,1.05),sx*rng.uniform(.45,.78)),
                     STONE_D if i%3 else STONE,sub=1,rot=(rng.random(),rng.random(),rng.random())))
    for q,(x,y) in enumerate(((-7.0,-1.8),(6.8,3.0))):
        z=height_at(x,y)
        o.append(cube(f"Ruin{q}A",(x,y,z+.28),(.85,.26,.58),STONE_D,rot=(0,0,.20 if q else -.15),b=.02))
        o.append(cube(f"Ruin{q}B",(x+.32,y+.18,z+.17),(.32,.55,.34),STONE,b=.015))
    for q,(x,y) in enumerate(((4.8,-5.2),(-2.0,4.3))):
        z=height_at(x,y)
        o.append(cyl(f"Beacon{q}",(x,y,z+.22),.20,.44,STONE_D,verts=8,b=.008))
        o.append(ico(f"BeaconFlame{q}",(x,y,z+.58),(.09,.08,.18),FIRE,sub=1))
    export_asset(o,"battlefield_terrain_hero")

def add_merlons(o,prefix,a,b,z,count,depth=.48,mat=STONE):
    ax,ay=a; bx,by=b
    ang=math.atan2(by-ay,bx-ax)
    for i in range(count):
        t=(i+.5)/count
        x=ax+(bx-ax)*t; y=ay+(by-ay)*t
        o.append(cube(f"{prefix}Merlon{i}",(x,y,z),(.34,depth,.52),mat if i%3 else STONE_L,rot=(0,0,ang),b=.015))

def wall(o,prefix,a,b,h=2.2,t=.46):
    ax,ay=a; bx,by=b
    mx,my=(ax+bx)/2,(ay+by)/2
    L=math.hypot(bx-ax,by-ay)
    ang=math.atan2(by-ay,bx-ax)
    o.append(cube(prefix+"Core",(mx,my,h/2),(L,t,h),STONE,rot=(0,0,ang),b=.027))
    o.append(cube(prefix+"Cap",(mx,my,h+.05),(L+.10,t+.10,.16),STONE_D,rot=(0,0,ang),b=.01))
    add_merlons(o,prefix,a,b,h+.34,max(3,int(L/.62)),depth=t+.08)

def tower(o,prefix,x,y,r,h,rear=False):
    base=STONE_D if rear else STONE
    o.append(cyl(prefix+"Core",(x,y,h/2),r,h,base,verts=10,b=.032))
    o.append(cyl(prefix+"Band",(x,y,h-.17),r+.09,.22,STONE_L,verts=10,b=.015))
    for i in range(10):
        a=math.tau*i/10
        o.append(cube(f"{prefix}Merlon{i}",(x+math.cos(a)*(r-.02),y+math.sin(a)*(r-.02),h+.31),
                      (.33,.43,.56),STONE if i%3 else STONE_L,rot=(0,0,a),b=.014))
    for j,a in enumerate((0,math.pi/2,math.pi,3*math.pi/2)):
        o.append(cube(f"{prefix}Slit{j}",(x+math.cos(a)*(r+.025),y+math.sin(a)*(r+.025),h*.56),
                      (.065,.045,.42),BLACK,rot=(0,0,a),b=.002))

def build_castle():
    clear_scene()
    o=[]
    tower(o,"FrontL",-3.65,-2.35,1.0,3.35)
    tower(o,"FrontR",3.65,-2.35,1.0,3.35)
    tower(o,"WingL",-5.55,-1.55,.72,2.48)
    tower(o,"WingR",5.55,-1.55,.72,2.48)
    tower(o,"RearL",-3.55,1.75,.78,2.86,True)
    tower(o,"RearR",3.55,1.75,.78,2.86,True)
    wall(o,"FrontLeft",(-3.65,-2.35),(-1.12,-2.35),2.16,.50)
    wall(o,"FrontRight",(1.12,-2.35),(3.65,-2.35),2.16,.50)
    wall(o,"WingLeft",(-5.55,-1.55),(-3.65,-2.35),1.80,.43)
    wall(o,"WingRight",(3.65,-2.35),(5.55,-1.55),1.80,.43)
    wall(o,"LeftSide",(-3.65,-2.35),(-3.55,1.75),2.05,.46)
    wall(o,"RightSide",(3.65,-2.35),(3.55,1.75),2.05,.46)
    wall(o,"Rear",(-3.55,1.75),(3.55,1.75),1.90,.44)
    o.append(cube("GatePierL",(-.74,-2.48,1.48),(.72,.88,2.96),STONE,b=.036))
    o.append(cube("GatePierR",(.74,-2.48,1.48),(.72,.88,2.96),STONE,b=.036))
    o.append(cube("GateLintel",(0,-2.48,3.12),(2.20,.90,.86),STONE_L,b=.034))
    o.append(cube("GateVoid",(0,-2.94,1.35),(1.10,.045,2.25),BLACK,b=.001))
    for i,x in enumerate((-.48,-.32,-.16,0,.16,.32,.48)):
        o.append(cube(f"PortV{i}",(x,-2.99,1.35),(.028,.035,2.18),IRON,b=.001))
    for i,z in enumerate((.53,.92,1.31,1.70,2.09)):
        o.append(cube(f"PortH{i}",(0,-2.99,z),(1.05,.035,.028),IRON,b=.001))
    add_merlons(o,"Gate",(-1.12,-2.48),(1.12,-2.48),3.76,6,depth=.78)
    o.append(cube("Keep",(0,.45,2.25),(3.65,2.75,4.50),STONE_D,b=.052))
    o.append(cube("KeepFront",(0,-.94,2.25),(3.35,.10,4.24),STONE,b=.020))
    o.append(cube("KeepCap",(0,.45,4.55),(3.95,3.05,.22),STONE_L,b=.019))
    add_merlons(o,"KeepFront",(-1.65,-.92),(1.65,-.92),4.95,7,depth=.50)
    o.append(cyl("UpperTurret",(-.88,.42,5.20),.62,1.22,STONE,verts=9,b=.022))
    for i in range(8):
        a=math.tau*i/8
        o.append(cube(f"UpperMerlon{i}",(-.88+math.cos(a)*.54,.42+math.sin(a)*.54,6.02),
                      (.26,.34,.43),STONE_L,rot=(0,0,a),b=.010))
    for i,(x,mat) in enumerate(((-1.02,BLUE),(1.02,BLUE))):
        o.append(cyl(f"BannerPole{i}",(x,-3.01,3.50),.024,1.35,IRON,verts=7,b=.002))
        o.append(cube(f"Banner{i}",(x,-3.04,3.35),(.50,.045,.82),mat,b=.005))
    for i,x in enumerate((-.90,.90)):
        o.append(beam(f"Torch{i}",(x,-3.02,2.20),(x,-3.12,2.55),.022,WOOD_D,6))
        o.append(ico(f"Flame{i}",(x,-3.15,2.70),(.07,.055,.15),FIRE,sub=1))
    rng=random.Random(8302)
    for i in range(34):
        x=rng.uniform(-5.7,5.7)
        y=rng.uniform(-2.0,1.8)
        if abs(x)<1.25 and y<-1.0:
            continue
        s=rng.uniform(.07,.18)
        o.append(ico(f"Rubble{i}",(x,y,.07),(s,s*.78,s*.58),STONE_D if i%2 else STONE,sub=1,
                     rot=(rng.random(),rng.random(),rng.random())))
    for i,(x,y,s) in enumerate(((-3.45,1.35,.42),(3.20,1.45,.38),(-5.1,-1.0,.28),(5.0,-.95,.25))):
        o.append(ico(f"Moss{i}",(x,y,.10),(s,s*.58,.05),MOSS,sub=1))
    export_asset(o,"castle_hero")

def build_opponent():
    clear_scene()
    o=[]
    o.append(cube("ChairBack",(0,1.02,4.15),(3.25,.32,6.0),WOOD_D,b=.07))
    o.append(cube("ChairSeat",(0,.48,1.34),(3.2,2.05,.26),WOOD,b=.05))
    o.append(cone("Torso",(0,-.20,4.55),1.45,1.03,3.10,TUNIC,verts=10,rot=(math.radians(7),0,0)))
    o.append(ico("Shoulders",(0,-.18,5.62),(1.82,.74,.56),CLOTH,sub=2))
    cloak_verts=[
        (-1.62,-.54,5.62),(-.32,-.84,5.40),(-.38,-.66,3.05),(-1.24,-.26,2.80),
        (.32,-.84,5.40),(1.62,-.54,5.62),(1.24,-.26,2.80),(.38,-.66,3.05)
    ]
    o.append(mesh_obj("CloakPanels",cloak_verts,[(0,1,2,3),(4,5,6,7)],[CLOTH],[0,0]))
    o.append(torus("Collar",(0,-.23,6.02),.63,.14,CLOTH,rot=(math.pi/2,0,0),major_segments=12,minor_segments=5))
    o.append(cube("Belt",(0,-.32,3.28),(2.08,.56,.16),LEATHER,b=.018))
    o.append(cube("Buckle",(0,-.63,3.28),(.28,.09,.24),BRONZE,b=.009))
    o.append(beam("StrapL",(-.72,-.67,5.42),(.38,-.64,3.60),.063,LEATHER_L,7))
    o.append(beam("StrapR",(.72,-.67,5.42),(-.38,-.64,3.60),.063,LEATHER,7))
    o.append(cyl("Neck",(0,-.28,6.17),.32,.52,SKIN_S,verts=9,b=.01))
    o.append(ico("Head",(0,-.46,7.03),(.88,.72,.98),SKIN,sub=2))
    o.append(ico("Jaw",(0,-.58,6.63),(.61,.57,.42),SKIN_S,sub=1))
    o.append(ico("Nose",(0,-1.07,7.04),(.12,.15,.25),SKIN,sub=1))
    o.append(ico("CheekL",(-.44,-.92,6.99),(.20,.075,.15),SKIN,sub=1))
    o.append(ico("CheekR",(.44,-.92,6.99),(.20,.075,.15),SKIN,sub=1))
    for side,x in (("L",-.29),("R",.29)):
        o.append(ico(f"Eye{side}",(x,-1.03,7.28),(.085,.035,.055),BONE,sub=1))
        o.append(ico(f"Pupil{side}",(x,-1.065,7.28),(.035,.018,.035),BLACK,sub=1))
        rz=math.radians(-9 if side=="L" else 9)
        o.append(cube(f"Brow{side}",(x,-1.07,7.49),(.31,.048,.065),HAIR,rot=(0,0,rz),b=.003))
    o.append(ico("HairCrown",(0,-.31,7.77),(.93,.75,.52),HAIR,sub=2))
    for i,(x,y,z,s) in enumerate(((-.67,-.47,7.63,.31),(.67,-.47,7.63,.31),(-.82,-.05,7.35,.28),
                                   (.82,-.05,7.35,.28),(-.45,.22,7.67,.29),(.45,.22,7.67,.29),
                                   (-.14,-.78,7.86,.24),(.17,-.76,7.86,.24))):
        o.append(ico(f"HairLock{i}",(x,y,z),(s,s*.72,s*.48),HAIR_L if i in (0,4,6) else HAIR,sub=1,
                     rot=(i*.08,i*.11,(i-3)*.07)))
    o.append(cone("Beard",(0,-.92,6.51),.54,.10,.82,HAIR,verts=9,rot=(math.radians(6),0,0)))
    o.append(ico("BeardL",(-.31,-.88,6.76),(.31,.17,.36),HAIR_L,sub=1))
    o.append(ico("BeardR",(.31,-.88,6.76),(.31,.17,.36),HAIR,sub=1))
    o.append(cube("MustacheL",(-.17,-1.06,6.88),(.28,.045,.075),HAIR,rot=(0,0,math.radians(-10)),b=.003))
    o.append(cube("MustacheR",(.17,-1.06,6.88),(.28,.045,.075),HAIR,rot=(0,0,math.radians(10)),b=.003))
    shoulder_l=(-1.50,-.18,5.30); elbow_l=(-2.00,-.95,4.22); wrist_l=(-1.82,-2.12,3.05)
    shoulder_r=(1.50,-.18,5.30); elbow_r=(1.90,-.98,4.30); wrist_r=(1.40,-2.48,3.12)
    o.append(beam("UpperArmL",shoulder_l,elbow_l,.29,CLOTH,10))
    o.append(beam("UpperArmR",shoulder_r,elbow_r,.29,CLOTH,10))
    o.append(beam("ForearmL",elbow_l,wrist_l,.24,SKIN,10))
    o.append(beam("ForearmR",elbow_r,wrist_r,.24,SKIN,10))
    o.append(cyl("BracerL",(-1.92,-1.53,3.65),.24,.66,LEATHER,verts=9,rot=(math.radians(68),0,math.radians(-7)),b=.009))
    o.append(cyl("BracerR",(1.68,-1.70,3.72),.24,.68,LEATHER,verts=9,rot=(math.radians(68),0,math.radians(8)),b=.009))
    for idx,(w,sign) in enumerate(((wrist_l,-1),(wrist_r,1))):
        wx,wy,wz=w
        o.append(ico(f"Hand{idx}",w,(.36,.29,.39),SKIN,sub=2))
        for f in range(4):
            xx=wx + sign*(f-1.5)*.062
            o.append(beam(f"Finger{idx}_{f}",(xx,wy-.10,wz-.06),(xx+sign*.015,wy-.34,wz-.11),.024,SKIN,6))
    o.append(ico("Brooch",(0,-.84,5.78),(.20,.065,.20),BRONZE,sub=1))
    export_asset(o,"opponent_hero")

def build_tavern():
    clear_scene()
    o=[]
    room_w, room_d = 38.0, 38.0
    for i in range(18):
        x=-room_w/2 + (room_w/18)*(i+.5)
        o.append(cube(f"Floor{i}",(x,-1.0,-.88),(room_w/18-.035,room_d,.24),WOOD_D if i%5==0 else WOOD,b=.012))
    for row in range(16):
        z=.42+row*.93
        o.append(cube(f"BackBoard{row}",(0,-19.0,z),(37.4,.38,.86),WOOD_D if row%4==0 else WOOD,b=.012))
    for row in range(15):
        z=.52+row*.98
        o.append(cube(f"LeftBoard{row}",(-18.75,-1.0,z),(.38,36.0,.90),WOOD_D if row%3==0 else WOOD,b=.012))
        o.append(cube(f"RightBoard{row}",(18.75,-1.0,z),(.38,36.0,.90),WOOD_D if row%4==0 else WOOD,b=.012))
    for x in (-16.2,-10.5,10.8,16.1):
        o.append(cube(f"Post{x}",(x,-18.65,7.4),(.48,.58,14.8),WOOD_D,b=.026))
    for z in (4.5,10.7,14.6):
        o.append(cube(f"BackBeam{z}",(0,-18.60,z),(36.6,.56,.44),WOOD_D,b=.022))
    for side,x0,w in (("L",-12.4,8.0),("R",12.7,6.8)):
        for j,z in enumerate((2.25,4.65,7.05)):
            o.append(cube(f"{side}Shelf{j}",(x0,-18.08,z),(w,1.0,.18),WOOD_L,b=.014))
    rng=random.Random(9127)
    for i in range(22):
        left=i<13
        x=rng.uniform(-15.8,-9.2) if left else rng.uniform(10.0,15.4)
        z=(2.48 if i%3==0 else 4.88 if i%3==1 else 7.28)
        if i==5:
            o.append(ico("ShelfSkull",(x,-17.78,z+.18),(.29,.23,.27),BONE,sub=1))
        elif i%5==0:
            o.append(cube(f"Book{i}",(x,-17.80,z),(.46,.44,.14),RED if i%10==0 else BLUE,rot=(0,0,(i%3-1)*.07),b=.007))
        else:
            h=.42+(i%4)*.07
            o.append(cyl(f"Bottle{i}",(x,-17.80,z+h*.45),.095,h,GRASS_D if i%2 else STONE_D,verts=8,b=.003))
    for i,(x,y) in enumerate(((-15.5,-10.5),(-14.0,-8.8),(15.7,-10.8),(14.4,-7.6))):
        o.append(cyl(f"Barrel{i}",(x,y,.66),.64,1.32,WOOD,verts=12,b=.015))
        o.append(torus(f"BarrelBandA{i}",(x,y,.30),.62,.026,IRON,rot=(math.pi/2,0,0)))
        o.append(torus(f"BarrelBandB{i}",(x,y,1.02),.62,.026,IRON,rot=(math.pi/2,0,0)))
    for i,x in enumerate((-14.5,-13.5,-12.5,12.6,13.6)):
        o.append(beam(f"Spear{i}",(x,-17.75,3.0),(x+(.25 if i%2 else -.25),-17.75,7.7),.035,WOOD_L,7))
        o.append(cone(f"SpearHead{i}",(x+(.25 if i%2 else -.25),-17.75,7.92),.11,0,.42,STEEL,verts=4))
    for i,(x,mat) in enumerate(((-16.8,BLUE_D),(16.7,RED_D))):
        o.append(cyl(f"BannerPole{i}",(x,-18.0,7.4),.035,5.0,IRON,verts=8,b=.003))
        o.append(cube(f"WallBanner{i}",(x,-17.78,7.0),(2.0,.055,3.5),mat,b=.008))
    for q,(x,z) in enumerate(((-8.8,9.6),(9.8,10.2))):
        for link in range(8):
            o.append(torus(f"Chain{q}_{link}",(x,-17.1,z+2.1-link*.27),.085,.020,IRON,
                           rot=(math.pi/2 if link%2 else 0,0,0),major_segments=8,minor_segments=4))
        o.append(cube(f"LanternFrame{q}",(x,-17.1,z),(.62,.54,.88),IRON,b=.016))
        o.append(ico(f"LanternFlame{q}",(x,-17.1,z),(.13,.12,.23),FIRE,sub=1))
    export_asset(o,"tavern_room_hero")

def build_reserve_rack():
    clear_scene()
    o=[]
    o.append(cube("RackBase",(0,0,.12),(6.8,2.05,.24),WOOD_D,b=.08))
    o.append(cube("RackInset",(0,0,.27),(6.45,1.72,.08),WOOD,b=.05))
    for i in range(6):
        x=-2.55+i*1.02
        o.append(cyl(f"Slot{i}",(x,0,.34),.38,.035,BLACK,verts=20,b=.001))
        o.append(torus(f"SlotRing{i}",(x,0,.36),.40,.025,BRONZE,major_segments=16,minor_segments=4))
    o.append(cube("FalseBottomLine",(0,-.87,.32),(4.7,.035,.035),IRON,b=.003))
    o.append(cube("HiddenLatch",(2.65,-.87,.36),(.48,.10,.15),BRONZE,b=.012))
    export_asset(o,"reserve_rack_hero")

def build_card_deck():
    clear_scene()
    o=[]
    for i in range(9):
        z=.035+i*.032
        o.append(cube(f"Card{i}",(0,0,z),(1.35,1.92,.045),PARCHMENT if i==8 else BLUE_D,
                      rot=(0,0,math.radians((i-4)*.45)),b=.025))
    o.append(cube("DeckEmblem",(0,0,.34),(.58,.72,.018),GOLD,rot=(0,0,math.radians(2)),b=.05))
    export_asset(o,"card_deck_hero")

def build_miniature(filename, role):
    clear_scene()
    o=[]
    team=BLUE
    o.append(cyl("Base",(0,0,.08),.48,.16,BLACK,verts=20,b=.02))
    o.append(torus("BaseRing",(0,0,.17),.43,.025,BRONZE,major_segments=16,minor_segments=4))
    o.append(cyl("LegL",(-.13,0,.55),.09,.72,IRON,verts=7,b=.004))
    o.append(cyl("LegR",(.13,0,.55),.09,.72,IRON,verts=7,b=.004))
    o.append(cone("Torso",(0,0,1.20),.33,.25,.78,team,verts=8))
    o.append(ico("Head",(0,-.02,1.72),(.25,.22,.27),SKIN,sub=1))
    o.append(cyl("Helmet",(0,-.01,1.88),.27,.24,STEEL,verts=8,b=.006))
    if role=="spearman":
        o.append(beam("Spear",(.30,0,.90),(.34,0,2.55),.025,WOOD_L,6))
        o.append(cone("SpearHead",(.34,0,2.72),.09,0,.32,STEEL,verts=4))
        o.append(beam("Arm",(.18,0,1.35),(.32,0,1.20),.07,SKIN,7))
    elif role=="archer":
        o.append(beam("BowTop",(.32,0,1.10),(.48,0,1.78),.025,WOOD_L,6))
        o.append(beam("BowBot",(.32,0,1.10),(.48,0,.46),.025,WOOD_L,6))
        o.append(beam("String",(.48,0,.46),(.48,0,1.78),.008,BONE,5))
        o.append(beam("Arrow",(-.16,-.02,1.30),(.60,-.02,1.30),.012,WOOD_L,5))
    else:
        o.append(cube("Shield",(-.34,-.02,1.19),(.10,.58,.70),BLUE_D,rot=(0,math.radians(9),0),b=.03))
        o.append(beam("Sword",(.28,0,1.15),(.62,0,1.82),.035,STEEL,6))
        o.append(cube("Guard",(.38,0,1.35),(.32,.07,.05),BRONZE,b=.006))
    export_asset(o,filename)

jobs=[
    build_table,
    build_battlefield,
    build_castle,
    build_opponent,
    build_tavern,
    build_reserve_rack,
    build_card_deck,
    lambda: build_miniature("spearman_hero","spearman"),
    lambda: build_miniature("archer_hero","archer"),
    lambda: build_miniature("swordsman_hero","swordsman"),
]

print("\n[CastleCards Locked Target] Generating approved-target vertical slice assets...\n")
for fn in jobs:
    fn()
print(f"\n[CastleCards Locked Target] Complete: {len(jobs)} assets regenerated.\n")
