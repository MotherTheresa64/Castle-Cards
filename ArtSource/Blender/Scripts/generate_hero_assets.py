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
random.seed(40926)


def clear_scene():
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)


def material(name, rgb, roughness=.92, metallic=0.0, emission=None, emission_strength=0.0):
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


WOOD_D = material("HQ_WoodDark", (.065,.022,.010), .96)
WOOD = material("HQ_Wood", (.18,.070,.023), .92)
WOOD_L = material("HQ_WoodLight", (.31,.135,.042), .88)
STONE_D = material("HQ_StoneDark", (.16,.17,.17), .99)
STONE = material("HQ_Stone", (.34,.33,.30), .99)
STONE_L = material("HQ_StoneLight", (.47,.44,.38), .98)
IRON = material("HQ_Iron", (.045,.050,.058), .42, .84)
STEEL = material("HQ_Steel", (.31,.33,.34), .40, .70)
BRONZE = material("HQ_Bronze", (.38,.20,.055), .50, .55)
GRASS_D = material("HQ_GrassDark", (.045,.095,.035), .99)
GRASS = material("HQ_Grass", (.095,.18,.055), .99)
GRASS_L = material("HQ_GrassLight", (.15,.26,.075), .99)
DIRT = material("HQ_Dirt", (.28,.18,.085), .99)
DIRT_D = material("HQ_DirtDark", (.15,.09,.045), .99)
WATER = material("HQ_Water", (.035,.16,.25), .26, .04)
RED = material("HQ_RedCloth", (.31,.030,.022), .98)
BLUE = material("HQ_BlueCloth", (.035,.090,.28), .98)
CLOTH = material("HQ_DarkCloth", (.040,.033,.048), .99)
TAN = material("HQ_TanCloth", (.28,.20,.12), .98)
LEATHER = material("HQ_Leather", (.16,.050,.018), .95)
SKIN = material("HQ_Skin", (.58,.36,.24), .88)
HAIR = material("HQ_Hair", (.065,.028,.015), .95)
BLACK = material("HQ_Black", (.010,.011,.013), .98)
BONE = material("HQ_Bone", (.62,.56,.43), .96)
FIRE = material("HQ_Fire", (1.0,.13,.01), .20, 0.0, (1.0,.10,.005), 7.0)


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
    mod = obj.modifiers.new("HQBevel", "BEVEL")
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


def cube(name, loc, dims, mat, rot=(0,0,0), b=.025):
    bpy.ops.mesh.primitive_cube_add(location=loc, rotation=rot)
    o=bpy.context.object
    o.name=name
    o.dimensions=dims
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    assign(o,mat); flat(o); bevel(o,b)
    return o


def cyl(name, loc, radius, depth, mat, verts=10, rot=(0,0,0), b=.012):
    bpy.ops.mesh.primitive_cylinder_add(vertices=verts, radius=radius, depth=depth, location=loc, rotation=rot)
    o=bpy.context.object
    o.name=name
    assign(o,mat); flat(o); bevel(o,b)
    return o


def cone(name, loc, r1, r2, depth, mat, verts=8, rot=(0,0,0)):
    bpy.ops.mesh.primitive_cone_add(vertices=verts, radius1=r1, radius2=r2, depth=depth, location=loc, rotation=rot)
    o=bpy.context.object
    o.name=name
    assign(o,mat); flat(o)
    return o


def ico(name, loc, scale, mat, sub=1, rot=(0,0,0)):
    bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=sub, radius=1.0, location=loc, rotation=rot)
    o=bpy.context.object
    o.name=name
    o.scale=scale
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    assign(o,mat); flat(o)
    return o


def torus(name, loc, major, minor, mat, rot=(0,0,0), major_segments=12, minor_segments=4):
    bpy.ops.mesh.primitive_torus_add(major_radius=major, minor_radius=minor, major_segments=major_segments, minor_segments=minor_segments, location=loc, rotation=rot)
    o=bpy.context.object
    o.name=name
    assign(o,mat); flat(o)
    return o


def beam(name, a, b, radius, mat, verts=8):
    a=Vector(a); b=Vector(b)
    direction=b-a
    length=direction.length
    mid=(a+b)*.5
    bpy.ops.mesh.primitive_cylinder_add(vertices=verts, radius=radius, depth=length, location=mid)
    o=bpy.context.object
    o.name=name
    o.rotation_mode='QUATERNION'
    o.rotation_quaternion=Vector((0,0,1)).rotation_difference(direction.normalized())
    assign(o,mat); flat(o); bevel(o,radius*.08)
    return o


def mesh_obj(name, verts, faces, mats, face_indices=None):
    mesh=bpy.data.meshes.new(name+"Mesh")
    mesh.from_pydata(verts, [], faces)
    mesh.update()
    o=bpy.data.objects.new(name,mesh)
    bpy.context.collection.objects.link(o)
    for m in mats:
        mesh.materials.append(m)
    if face_indices:
        for p,idx in zip(mesh.polygons,face_indices):
            p.material_index=idx
    flat(o)
    return o


def export_asset(objs, filename):
    bpy.ops.object.select_all(action='DESELECT')
    for o in objs:
        if o and o.name in bpy.context.view_layer.objects:
            o.select_set(True)
    if objs:
        bpy.context.view_layer.objects.active=objs[0]
    bpy.ops.wm.save_as_mainfile(filepath=str(SRC / f"{filename}.blend"))
    bpy.ops.export_scene.gltf(filepath=str(OUT / f"{filename}.glb"), export_format='GLB', use_selection=True, export_materials='EXPORT', export_normals=True, export_animations=False, export_yup=True)
    print(f"[CastleCards HQ] Exported {filename}")


# -----------------------------------------------------------------------------
# Tavern room
# -----------------------------------------------------------------------------

def build_tavern_room():
    clear_scene(); o=[]
    room_w=38.0; room_d=38.0

    # Individual floor planks catch light and create visible wood breakup.
    plank_w=room_w/22
    for i in range(22):
        x=-room_w/2+plank_w*(i+.5)
        mat=(WOOD_D,WOOD,WOOD_L)[i%3]
        o.append(cube(f"Floor_{i}",(x,-1.0,-.12+(i%4)*.004),(plank_w-.035,room_d,.24),mat,b=.018))

    # Back and side wall boards.
    for r in range(17):
        z=.55+r*.92
        o.append(cube(f"BackPlank_{r}",(0,-19.0,z),(37.4,.42,.86),WOOD if r%4 else WOOD_D,b=.018))
        o.append(cube(f"LeftPlank_{r}",(-18.75,-1.0,z),(.42,36.0,.86),WOOD_D if r%3==0 else WOOD,b=.016))
        o.append(cube(f"RightPlank_{r}",(18.75,-1.0,z),(.42,36.0,.86),WOOD_D if r%3==1 else WOOD,b=.016))

    # Heavy structural timber.
    for x in (-16,-12,-8,-4,0,4,8,12,16):
        o.append(cube(f"BackPost_{x}",(x,-18.68,7.8),(.46,.58,15.6),WOOD_D,b=.028))
    for z in (4.2,10.2,15.0):
        o.append(cube(f"BackCross_{z}",(0,-18.60,z),(37.0,.64,.52),WOOD_D,b=.028))
    for x in (-17.5,17.5):
        for y in (-15,-9,-3,3,9,15):
            o.append(cube(f"SidePost_{x}_{y}",(x,y,7.7),(.52,.52,15.4),WOOD_D,b=.028))

    # Ceiling rafters and diagonal braces.
    for x in (-15,-10,-5,0,5,10,15):
        o.append(cube(f"Rafter_{x}",(x,-1.0,15.35),(.48,35.3,.50),WOOD_D,b=.028))
        o.append(beam(f"BraceL_{x}",(x,-17.2,14.9),(x-1.25,-15.6,12.1),.18,WOOD_L))
        o.append(beam(f"BraceR_{x}",(x,-17.2,14.9),(x+1.25,-15.6,12.1),.18,WOOD_L))

    # Back-wall shelving and clutter.
    for sx,tag in ((-11.8,"L"),(11.8,"R")):
        for li,z in enumerate((2.2,4.7,7.2)):
            o.append(cube(f"Shelf_{tag}_{li}",(sx,-18.15,z),(8.5,1.0,.20),WOOD_L,b=.018))
        for i in range(11):
            x=sx-3.5+i*.70
            z=2.55+(i%3)*2.45
            if i%5==0:
                o.append(ico(f"Skull_{tag}_{i}",(x,-17.90,z+.20),(.25,.22,.28),BONE,sub=1))
                o.append(cube(f"Jaw_{tag}_{i}",(x,-18.05,z-.03),(.30,.20,.14),BONE,b=.014))
            elif i%3==0:
                o.append(cube(f"Book_{tag}_{i}",(x,-18.00,z),(.48,.56,.15),RED if tag=="R" else BLUE,rot=(0,0,math.radians((i%5-2)*3)),b=.010))
            else:
                h=.52+(i%3)*.15
                o.append(cyl(f"Bottle_{tag}_{i}",(x,-17.95,z+h*.45),.12+(i%2)*.02,h,STONE_D if i%2 else GRASS_D,verts=8,b=.006))
                o.append(cyl(f"Neck_{tag}_{i}",(x,-17.95,z+h+.04),.05,.28,STONE_D,verts=8,b=.003))

    # Banners, lanterns, chains.
    for idx,(x,mat) in enumerate(((-7.0,BLUE),(7.0,RED))):
        o.append(cyl(f"BannerPole_{idx}",(x,-18.05,9.2),.045,3.0,IRON,verts=8,rot=(0,math.pi/2,0),b=.004))
        o.append(cube(f"Banner_{idx}",(x,-17.98,7.9),(2.0,.08,3.2),mat,b=.010))
    for idx,x in enumerate((-13.3,13.3)):
        for link in range(7):
            o.append(torus(f"Chain_{idx}_{link}",(x,-17.35,13.7-link*.32),.11,.025,IRON,rot=(math.pi/2 if link%2 else 0,0,0),major_segments=8,minor_segments=4))
        o.append(cube(f"Lantern_{idx}",(x,-17.35,10.9),(.68,.52,.92),IRON,b=.018))
        o.append(ico(f"LanternFire_{idx}",(x,-17.35,10.9),(.17,.15,.29),FIRE,sub=1))

    # Chandelier.
    o.append(cyl("ChandelierChain",(0,-4.0,13.0),.045,4.6,IRON,verts=8,b=.004))
    o.append(torus("ChandelierRing",(0,-4.0,10.7),1.35,.09,IRON,major_segments=16,minor_segments=5))
    for i in range(8):
        a=math.tau*i/8; x=math.cos(a)*1.32; y=-4.0+math.sin(a)*1.32
        o.append(cyl(f"ChandelierCandle_{i}",(x,y,11.05),.065,.50,BONE,verts=8,b=.003))
        o.append(ico(f"ChandelierFlame_{i}",(x,y,11.39),(.05,.045,.13),FIRE,sub=1))

    # Side barrels, crates and hanging chain hooks.
    for side,x in (("L",-16.6),("R",16.6)):
        for i,y in enumerate((-13,-9,-5,0,5)):
            r=.68+(i%2)*.08
            o.append(cyl(f"Barrel_{side}_{i}",(x,y,r),r,1.34,WOOD,verts=12,b=.018))
            for dz in (-.46,0,.46):
                o.append(torus(f"Band_{side}_{i}_{dz}",(x,y,r+dz),r*.97,.032,IRON,rot=(math.pi/2,0,0),major_segments=12,minor_segments=4))
        o.append(cube(f"Crate_{side}",(x,10.0,.65),(1.6,1.6,1.3),WOOD_L,rot=(0,0,math.radians(8 if side=="L" else -8)),b=.035))
    for c,y in enumerate((-11,-6,-1,4)):
        for link in range(8):
            o.append(torus(f"WallChain_{c}_{link}",(18.45,y,11.5-link*.42),.12,.024,IRON,rot=(math.pi/2 if link%2 else 0,0,0),major_segments=8,minor_segments=4))
        o.append(cone(f"Hook_{c}",(18.28,y,7.7),.11,.02,.55,IRON,verts=6,rot=(0,math.radians(90),0)))

    export_asset(o,"tavern_room_hero")


# -----------------------------------------------------------------------------
# Sculpted battlefield
# -----------------------------------------------------------------------------

def terrain_height(x,y):
    h=.15*math.sin(x*.55)+.10*math.cos(y*.64)+.06*math.sin((x+y)*1.10)+.04*math.sin(x*1.7+y*.8)
    if y>5.5 or y<-5.5:
        h*=.20
    river_x=-5.4+.52*math.sin(y*.55)
    d=abs(x-river_x)
    if d<1.50:
        h-=.28*(1.0-d/1.50)
    road_x=.28*math.sin(y*.48)
    if abs(x-road_x)<1.15:
        h*=.32
    return h


def ribbon(name,path,half_width,z,mat):
    verts=[]; faces=[]
    for i,(x,y) in enumerate(path):
        if i==0:
            dx=path[1][0]-x; dy=path[1][1]-y
        else:
            dx=x-path[i-1][0]; dy=y-path[i-1][1]
        length=max(.001,math.sqrt(dx*dx+dy*dy)); nx=-dy/length; ny=dx/length
        verts.append((x+nx*half_width,y+ny*half_width,z)); verts.append((x-nx*half_width,y-ny*half_width,z))
    for i in range(len(path)-1):
        a=i*2; faces.append((a,a+1,a+3,a+2))
    return mesh_obj(name,verts,faces,[mat],[0]*len(faces))


def add_tree(o,name,x,y,z,scale,pine=False):
    o.append(cyl(name+"Trunk",(x,y,z+.70*scale),.18*scale,1.42*scale,WOOD_D,verts=8,b=.006))
    if pine:
        for i,(zz,r) in enumerate(((1.20,.68),(1.68,.58),(2.10,.46))):
            o.append(cone(f"{name}Pine{i}",(x,y,z+zz*scale),r*scale,.07*scale,.76*scale,(GRASS_D,GRASS,GRASS_L)[i%3],verts=7))
    else:
        for i,(dx,dy,dz,r) in enumerate(((0,0,1.55,.62),(-.40,.02,1.60,.42),(.40,.04,1.64,.43),(0,.34,1.90,.40),(-.18,-.30,1.96,.36))):
            o.append(ico(f"{name}Leaf{i}",(x+dx*scale,y+dy*scale,z+dz*scale),(r*scale,r*.86*scale,r*.70*scale),(GRASS_D,GRASS,GRASS_L)[i%3],sub=1,rot=(i*.25,i*.4,i*.15)))


def build_battlefield():
    clear_scene(); o=[]
    nx=31; ny=25; width=22.0; depth=17.4
    verts=[]
    for j in range(ny):
        y=-depth/2+depth*j/(ny-1)
        for i in range(nx):
            x=-width/2+width*i/(nx-1)
            verts.append((x,y,terrain_height(x,y)))
    faces=[]; fm=[]; rng=random.Random(818)
    mats=[GRASS,GRASS_D,GRASS_L,DIRT,DIRT_D]
    for j in range(ny-1):
        for i in range(nx-1):
            a=j*nx+i; faces.append((a,a+1,a+1+nx,a+nx))
            cx=-width/2+width*(i+.5)/(nx-1); cy=-depth/2+depth*(j+.5)/(ny-1)
            road_x=.28*math.sin(cy*.48); river_x=-5.4+.52*math.sin(cy*.55)
            if abs(cx-road_x)<1.08: idx=3 if rng.random()>.20 else 4
            elif abs(cx-river_x)<1.50: idx=1
            else:
                r=rng.random(); idx=0 if r<.42 else (1 if r<.70 else (2 if r<.90 else 3))
            fm.append(idx)
    o.append(mesh_obj("SculptedGround",verts,faces,mats,fm))

    river_path=[]; road_path=[]
    for k in range(23):
        y=-8.2+k*(16.4/22)
        river_path.append((-5.4+.52*math.sin(y*.55),y)); road_path.append((.28*math.sin(y*.48),y))
    o.append(ribbon("River",river_path,.80,.02,WATER)); o.append(ribbon("Road",road_path,.72,.055,DIRT))
    o.append(ribbon("BranchRoad",[(0,-.2),(1.3,-1.3),(2.9,-2.3),(4.8,-3.2),(6.7,-3.7)],.44,.058,DIRT_D))

    rng=random.Random(2026)
    for i in range(34):
        y=-7.7+i*(15.4/33); rx=-5.4+.52*math.sin(y*.55); side=-1 if i%2==0 else 1
        x=rx+side*(1.00+rng.uniform(.08,.42)); z=terrain_height(x,y)+.10
        o.append(ico(f"BankRock{i}",(x,y,z),(rng.uniform(.11,.26),rng.uniform(.09,.22),rng.uniform(.07,.15)),STONE_D if i%3 else STONE,sub=1,rot=(rng.random(),rng.random(),rng.random())))

    for i in range(95):
        x=rng.uniform(-10.2,10.2); y=rng.uniform(-8.0,8.0)
        if abs(x)<1.1 or abs(x-(-5.4+.52*math.sin(y*.55)))<1.5 or y>5.8 or y<-5.8:
            continue
        z=terrain_height(x,y)
        if i%4==0:
            o.append(ico(f"Pebble{i}",(x,y,z+.07),(rng.uniform(.07,.17),rng.uniform(.06,.14),rng.uniform(.04,.10)),STONE if i%8 else STONE_D,sub=1))
        else:
            for blade in range(3):
                o.append(cone(f"Grass{i}_{blade}",(x+(blade-1)*.055,y,z+.13),.040,0,.28,GRASS_L if (i+blade)%3 else GRASS_D,verts=4,rot=(rng.uniform(-.10,.10),rng.uniform(-.10,.10),rng.uniform(-.18,.18))))

    for i,(x,y,s,pine) in enumerate(((-9.1,-4.0,.78,False),(-8.3,-2.8,.66,False),(-9.3,-.9,.72,True),(8.8,-6.8,.74,False),(9.2,-4.8,.67,False),(8.2,-8.0,.62,True),(-8.4,3.1,.64,True),(-9.2,4.4,.70,False),(8.6,2.4,.67,False),(9.0,4.1,.58,True),(-7.4,-7.4,.58,True),(7.0,-1.2,.55,False))):
        add_tree(o,f"Tree{i}",x,y,terrain_height(x,y),s,pine)

    for i,(x,y,ang) in enumerate(((-7.1,-5.6,18),(6.5,-1.6,-15),(7.6,-7.2,28))):
        z=terrain_height(x,y)
        for bidx in range(4):
            o.append(cube(f"Ruin{i}_{bidx}",(x+(bidx-1.5)*.36,y,z+.24+(bidx%2)*.11),(.46,.34,.45+(bidx%2)*.20),STONE_D if bidx%2 else STONE,rot=(0,0,math.radians(ang+bidx*5)),b=.022))

    bridge_y=-.5; rx=-5.4+.52*math.sin(bridge_y*.55)
    for i in range(9):
        x=rx-1.4+i*.35
        o.append(cube(f"BridgePlank{i}",(x,bridge_y,.32),(.30,2.20,.18),WOOD_L if i%2 else WOOD,rot=(0,0,math.radians((i-4)*1.5)),b=.016))
    o.append(beam("BridgeRailL",(rx-1.4,bridge_y-1.0,.78),(rx+1.4,bridge_y-1.0,.78),.065,WOOD_D))
    o.append(beam("BridgeRailR",(rx-1.4,bridge_y+1.0,.78),(rx+1.4,bridge_y+1.0,.78),.065,WOOD_D))

    export_asset(o,"battlefield_terrain_hero")


# -----------------------------------------------------------------------------
# Castle hero
# -----------------------------------------------------------------------------

def add_tower(o,name,x,y,radius,height):
    o.append(cyl(name+"Core",(x,y,height*.5),radius,height,STONE,verts=12,b=.032))
    o.append(cyl(name+"Foot",(x,y,.20),radius+.14,.40,STONE_D,verts=12,b=.022))
    o.append(cyl(name+"Band",(x,y,height-.18),radius+.10,.22,STONE_L,verts=12,b=.016))
    for row in range(5):
        z=.62+row*(height-.9)/5
        for i in range(8):
            a=math.tau*i/8+(row%2)*math.pi/8; xx=x+math.cos(a)*(radius+.015); yy=y+math.sin(a)*(radius+.015)
            o.append(cube(f"{name}Stone{row}_{i}",(xx,yy,z),(.50,.060,.34),(STONE,STONE_L,STONE_D)[(i+row)%3],rot=(0,0,a),b=.007))
    for i in range(10):
        a=math.tau*i/10; xx=x+math.cos(a)*(radius-.03); yy=y+math.sin(a)*(radius-.03)
        o.append(cube(f"{name}Merlon{i}",(xx,yy,height+.38),(.42,.56,.66),STONE,rot=(0,0,a),b=.020))
    for i,a in enumerate((0,math.pi/2,math.pi,3*math.pi/2)):
        xx=x+math.cos(a)*(radius+.05); yy=y+math.sin(a)*(radius+.05)
        o.append(cube(f"{name}Slit{i}",(xx,yy,height*.56),(.065,.05,.45),BLACK,rot=(0,0,a),b=.003))


def add_wall(o,name,a,b,height=2.75,thick=.52):
    ax,ay=a; bx,by=b; mx=(ax+bx)/2; my=(ay+by)/2; length=math.hypot(bx-ax,by-ay); ang=math.atan2(by-ay,bx-ax)
    o.append(cube(name+"Core",(mx,my,height*.5),(length,thick,height),STONE,rot=(0,0,ang),b=.030))
    o.append(cube(name+"Lip",(mx,my,height+.03),(length+.12,thick+.10,.17),STONE_D,rot=(0,0,ang),b=.014))
    count=max(3,int(length/.65))
    for i in range(count):
        t=(i+.5)/count; x=ax+(bx-ax)*t; y=ay+(by-ay)*t
        o.append(cube(f"{name}Merlon{i}",(x,y,height+.36),(.40,thick+.04,.58),STONE,rot=(0,0,ang),b=.018))


def build_castle():
    clear_scene(); o=[]
    add_tower(o,"FrontL",-3.05,-2.05,1.14,4.2); add_tower(o,"FrontR",3.05,-2.05,1.20,4.45)
    add_tower(o,"RearL",-3.28,2.00,.98,3.8); add_tower(o,"RearR",3.22,2.08,.92,3.55)
    add_wall(o,"LeftWall",(-3.05,-2.05),(-3.28,2.0),2.72,.54); add_wall(o,"RightWall",(3.05,-2.05),(3.22,2.08),2.82,.54)
    add_wall(o,"RearWall",(-3.28,2.0),(3.22,2.08),2.62,.52); add_wall(o,"FrontLeft",(-3.05,-2.05),(-1.15,-2.08),2.62,.54); add_wall(o,"FrontRight",(1.15,-2.08),(3.05,-2.05),2.62,.54)

    # Gatehouse with actual opening.
    o.append(cube("GateL",(-.78,-2.08,1.68),(.72,.88,3.36),STONE,b=.038)); o.append(cube("GateR",(.78,-2.08,1.68),(.72,.88,3.36),STONE,b=.038))
    o.append(cube("GateUpper",(0,-2.08,3.32),(2.28,.90,1.50),STONE_L,b=.038))
    for i,x in enumerate((-.66,-.44,-.22,0,.22,.44,.66)):
        o.append(cube(f"PortV{i}",(x,-2.58,1.42),(.045,.055,2.52),IRON,b=.003))
    for i,z in enumerate((.55,1.05,1.55,2.05,2.55)):
        o.append(cube(f"PortH{i}",(0,-2.58,z),(1.42,.055,.045),IRON,b=.003))
    for i,x in enumerate((-1.0,-.5,0,.5,1.0)):
        o.append(cube(f"GateMerlon{i}",(x,-2.08,4.38),(.34,.80,.56),STONE,b=.018))

    # Central keep and asymmetrical details.
    o.append(cube("Keep",(0,.44,2.52),(3.7,3.1,5.04),STONE_D,b=.055)); o.append(cube("KeepFace",(0,-1.14,2.56),(3.44,.10,4.72),STONE,b=.025)); o.append(cube("KeepTop",(0,.44,5.15),(3.92,3.32,.25),STONE_L,b=.022))
    for i,x in enumerate((-1.44,-.72,0,.72,1.44)):
        o.append(cube(f"KeepFront{i}",(x,-.92,5.62),(.40,.54,.70),STONE,b=.018)); o.append(cube(f"KeepBack{i}",(x,1.80,5.62),(.40,.54,.70),STONE,b=.018))
    for i,(x,z) in enumerate(((-.85,3.35),(.85,3.35),(-.85,4.18),(.85,4.18))):
        o.append(cube(f"Window{i}",(x,-1.20,z),(.22,.055,.44),BLACK,b=.003)); o.append(cube(f"Lintel{i}",(x,-1.23,z+.29),(.38,.09,.09),STONE_L,b=.005))
    for i,x in enumerate((-2.05,2.05)):
        o.append(cube(f"Buttress{i}",(x,-2.28,1.22),(.46,.70,2.44),STONE_D,rot=(0,0,math.radians(3 if x<0 else -3)),b=.030))

    # Stone stair and wooden scaffold.
    for i in range(6):
        o.append(cube(f"Stair{i}",(-4.18+i*.37,.65+i*.11,.19+i*.21),(.78,.72,.21),STONE_L,b=.018))
    o.append(beam("ScaffoldA",(4.12,.25,.15),(4.12,.25,3.0),.095,WOOD_D)); o.append(beam("ScaffoldB",(4.72,.25,.15),(4.72,.25,2.6),.095,WOOD_D))
    o.append(cube("ScaffoldDeck",(4.42,.25,2.08),(1.20,1.02,.17),WOOD_L,b=.016)); o.append(beam("ScaffoldBrace",(4.08,-.18,.40),(4.75,.62,2.42),.065,WOOD))

    # Banners and gate torches.
    for i,(x,mat,z) in enumerate(((-1.02,BLUE,4.30),(1.02,RED,4.12))):
        o.append(cyl(f"BannerPole{i}",(x,-2.58,z+.34),.032,1.65,IRON,verts=8,b=.003)); o.append(cube(f"Banner{i}",(x,-2.63,z),(.62,.05,.96),mat,b=.007))
    for i,x in enumerate((-.95,.95)):
        o.append(beam(f"Torch{i}",(x,-2.62,2.62),(x,-2.70,3.15),.032,WOOD_D)); o.append(ico(f"TorchFire{i}",(x,-2.74,3.29),(.075,.065,.17),FIRE,sub=1))

    rng=random.Random(77)
    for i in range(16):
        x=rng.uniform(-4.0,4.0); y=rng.uniform(-2.9,2.8)
        if abs(x)<1.4 and y<-1.5: continue
        o.append(ico(f"Rubble{i}",(x,y,.11),(rng.uniform(.10,.24),rng.uniform(.08,.19),rng.uniform(.07,.17)),STONE_D if i%2 else STONE,sub=1,rot=(rng.random(),rng.random(),rng.random())))
    export_asset(o,"castle_hero")


# -----------------------------------------------------------------------------
# Opponent hero
# -----------------------------------------------------------------------------

def build_opponent():
    clear_scene(); o=[]
    # Chair.
    o.append(cube("ChairBack",(0,1.15,4.5),(3.25,.38,6.7),WOOD_D,b=.075)); o.append(cube("ChairSeat",(0,.35,1.35),(3.35,2.1,.30),WOOD,b=.055))
    for x in (-1.35,1.35):
        o.append(cube(f"ChairPost{x}",(x,1.10,4.75),(.28,.32,7.1),WOOD_L,b=.032)); o.append(ico(f"ChairCap{x}",(x,1.10,8.35),(.22,.22,.26),BRONZE,sub=1))

    # Legs, torso, belt and cloak.
    o.append(beam("ThighL",(-.65,.10,2.65),(-.80,-1.10,1.75),.38,CLOTH,10)); o.append(beam("ThighR",(.65,.10,2.65),(.80,-1.10,1.75),.38,CLOTH,10))
    o.append(cone("Torso",(0,0,4.70),1.48,1.16,3.22,TAN,verts=10)); o.append(cube("Belt",(0,-.15,3.45),(2.22,.70,.18),LEATHER,b=.022)); o.append(cube("Buckle",(0,-.53,3.45),(.30,.10,.28),BRONZE,b=.012))
    o.append(ico("CloakShoulders",(0,.05,5.92),(2.15,.86,.70),CLOTH,sub=2))
    cloak_verts=[(-1.75,-.60,5.80),(-.18,-.82,5.55),(-.25,-.70,3.35),(-1.34,-.35,2.86),(.18,-.82,5.55),(1.75,-.60,5.80),(1.34,-.35,2.86),(.25,-.70,3.35)]
    o.append(mesh_obj("CloakPanels",cloak_verts,[(0,1,2,3),(4,5,6,7)],[CLOTH],[0,0])); o.append(torus("CloakCollar",(0,-.10,6.38),.67,.17,CLOTH,rot=(math.pi/2,0,0),major_segments=12,minor_segments=5))

    # Head / face.
    o.append(cyl("Neck",(0,-.05,6.52),.37,.60,SKIN,verts=10,b=.012)); o.append(ico("Head",(0,-.10,7.50),(1.00,.85,1.10),SKIN,sub=2)); o.append(ico("Jaw",(0,-.16,6.96),(.69,.70,.50),SKIN,sub=1)); o.append(ico("Nose",(0,-.89,7.49),(.14,.17,.24),SKIN,sub=1))
    for side,x in (("L",-.34),("R",.34)):
        o.append(ico(f"EyeWhite{side}",(x,-.85,7.67),(.10,.05,.07),BONE,sub=1)); o.append(ico(f"Eye{side}",(x,-.90,7.67),(.042,.022,.042),BLACK,sub=1)); o.append(cube(f"Brow{side}",(x,-.87,7.88),(.35,.065,.07),HAIR,rot=(0,0,math.radians(-8 if side=="L" else 8)),b=.006))

    # Angular hair and beard silhouette.
    o.append(ico("HairCap",(0,.02,8.29),(1.04,.90,.60),HAIR,sub=2))
    for i,(x,y,z,s) in enumerate(((-.72,-.34,8.06,.38),(.72,-.34,8.06,.38),(-.84,.05,7.80,.33),(.84,.05,7.80,.33),(-.54,.40,8.14,.36),(.54,.40,8.14,.36))):
        o.append(ico(f"HairLock{i}",(x,y,z),(s,s*.72,s*.50),HAIR,sub=1,rot=(i*.20,i*.15,i*.32)))
    o.append(cone("Beard",(0,-.70,6.95),.62,.17,.92,HAIR,verts=8,rot=(math.radians(8),0,0))); o.append(cube("MustacheL",(-.20,-.90,7.20),(.32,.055,.09),HAIR,rot=(0,0,math.radians(-12)),b=.005)); o.append(cube("MustacheR",(.20,-.90,7.20),(.32,.055,.09),HAIR,rot=(0,0,math.radians(12)),b=.005))

    # Natural resting arms and fingers.
    sl=(-1.70,-.08,5.52); el=(-2.42,-.60,4.28); wl=(-2.58,-1.68,3.12); sr=(1.70,-.08,5.52); er=(2.38,-.64,4.30); wr=(2.23,-1.72,3.12)
    o.append(beam("UpperArmL",sl,el,.33,CLOTH,10)); o.append(beam("UpperArmR",sr,er,.33,CLOTH,10)); o.append(beam("ForearmL",el,wl,.27,SKIN,10)); o.append(beam("ForearmR",er,wr,.27,SKIN,10))
    o.append(ico("HandL",wl,(.40,.33,.46),SKIN,sub=2,rot=(.2,0,-.14))); o.append(ico("HandR",wr,(.40,.33,.46),SKIN,sub=2,rot=(.2,0,.14)))
    for hidx,(wx,wy,wz,sgn) in enumerate(((*wl,-1),(*wr,1))):
        for f in range(4):
            x=wx+sgn*(f-1.5)*.075
            o.append(beam(f"Finger{hidx}_{f}",(x,wy-.16,wz-.08),(x+sgn*.02,wy-.42,wz-.12),.030,SKIN,6))

    # Brooch and pendant.
    o.append(ico("Brooch",(0,-.81,6.12),(.21,.08,.21),BRONZE,sub=1)); o.append(beam("PendantChain",(0,-.74,5.98),(0,-.76,5.30),.020,BRONZE,6)); o.append(ico("Pendant",(0,-.78,5.16),(.14,.07,.18),BRONZE,sub=1))
    export_asset(o,"opponent_hero")


jobs=[build_tavern_room,build_battlefield,build_castle,build_opponent]
print("\n[CastleCards HQ] Generating hero-quality assets...\n")
for fn in jobs:
    print(f"[CastleCards HQ] {fn.__name__}")
    fn()
print(f"\n[CastleCards HQ] Complete: {len(jobs)} hero assets generated.\n")
