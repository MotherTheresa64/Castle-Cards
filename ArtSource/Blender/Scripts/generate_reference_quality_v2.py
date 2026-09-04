"""Reference-quality V2 hero rebuild for Castle Cards.

This deliberately replaces the biggest visual offenders in the gameplay camera after the legacy
asset pipeline runs: the opponent, both castles, and the battlefield terrain. It reuses the stable
geometry/export helpers from generate_realistic_target_pass.py, then the existing cinematic
material pass adds embedded PBR breakup to the results.
"""
import importlib.util
import math
import random
from pathlib import Path

SCRIPT = Path(__file__).resolve()
ROOT = SCRIPT.parents[3]
HERO = ROOT / "Models" / "Hero"
TERRAIN = ROOT / "Models" / "Terrain" / "Medieval"
BASE_PATH = SCRIPT.with_name("generate_realistic_target_pass.py")

spec = importlib.util.spec_from_file_location("castle_cards_realistic_base", BASE_PATH)
base = importlib.util.module_from_spec(spec)
spec.loader.exec_module(base)
RNG = random.Random(9042026)

# Darker, more reference-like palette. Names intentionally contain material-family tokens so the
# cinematic PBR pass can classify them.
STONE = base.mat("V2_Weathered_Stone", (.195, .195, .180), .91)
STONE_DARK = base.mat("V2_Dark_Stone", (.080, .085, .082), .95)
STONE_LIGHT = base.mat("V2_Cut_Stone", (.280, .268, .238), .88)
MOSS_STONE = base.mat("V2_Moss_Stone", (.125, .145, .090), .95)
WOOD = base.mat("V2_Weathered_Wood", (.085, .030, .011), .84)
WOOD_MID = base.mat("V2_Oak_Wood", (.155, .055, .018), .79)
IRON = base.mat("V2_Black_Iron_Metal", (.035, .040, .045), .34, .84)
BRONZE = base.mat("V2_Bronze_Metal", (.300, .140, .036), .40, .66)
BLUE = base.mat("V2_Blue_Cloth", (.026, .060, .155), .93)
RED = base.mat("V2_Red_Cloth", (.235, .026, .016), .93)
CLOTH = base.mat("V2_Black_Cloth", (.016, .018, .022), .97)
CLOTH_MID = base.mat("V2_Charcoal_Cloth", (.042, .042, .048), .95)
LEATHER = base.mat("V2_Dark_Leather", (.075, .023, .010), .85)
SKIN = base.mat("V2_Skin", (.410, .205, .112), .73)
SKIN_SHADOW = base.mat("V2_Skin_Shadow", (.240, .095, .052), .79)
HAIR = base.mat("V2_Hair", (.020, .009, .005), .90)
HAIR_LIGHT = base.mat("V2_Hair_Highlight", (.055, .019, .009), .88)
EYE = base.mat("V2_Eye", (.008, .006, .004), .42)
PARCHMENT = base.mat("V2_Parchment", (.445, .300, .145), .90)
GRASS = base.mat("V2_Grass", (.085, .130, .050), .97)
GRASS_DARK = base.mat("V2_Dark_Grass", (.040, .073, .030), .98)
GRASS_LIGHT = base.mat("V2_Moss_Grass", (.130, .175, .065), .96)
DIRT = base.mat("V2_Dirt", (.145, .080, .035), .98)
DIRT_LIGHT = base.mat("V2_Dry_Dirt", (.215, .130, .060), .97)
WATER = base.mat("V2_River_Water", (.020, .082, .120), .20)
LEAF = base.mat("V2_Leaf", (.038, .092, .032), .96)
LEAF_MID = base.mat("V2_Leaf_Mid", (.062, .132, .044), .95)
LEAF_LIGHT = base.mat("V2_Leaf_Light", (.095, .168, .052), .94)


def cube(*args, **kwargs): return base.cube(*args, **kwargs)
def cyl(*args, **kwargs): return base.cyl(*args, **kwargs)
def cone(*args, **kwargs): return base.cone(*args, **kwargs)
def ico(*args, **kwargs): return base.ico(*args, **kwargs)
def torus(*args, **kwargs): return base.torus(*args, **kwargs)
def beam(*args, **kwargs): return base.beam(*args, **kwargs)


def battlements(prefix, center_x, y, z, width, count):
    for i in range(count):
        x = center_x - width * .5 + width * (i + .5) / count
        cube(f"{prefix}_{i}", (x, y, z), (.44, .50, .46), STONE_LIGHT if i % 3 == 0 else STONE, b=.025)


def build_castle(team):
    base.clear()
    accent = BLUE if team == "blue" else RED
    cube("Foundation_Stone", (0, .18, .12), (10.8, 4.35, .26), STONE_DARK, b=.12, seg=3)

    # Low, broad front wall and corner towers. This removes the old giant rectangular keep read.
    for side in (-1, 1):
        cx = side * 3.12
        cube(f"FrontWall_{side}_Stone", (cx, -1.28, 1.12), (3.70, .76, 2.05), STONE, b=.055, seg=3)
        for row in range(5):
            z = .33 + row * .37
            for col in range(5):
                x = cx - 1.42 + col * .71 + (row % 2) * .15
                if x > cx + 1.54:
                    continue
                mat = (STONE, STONE_LIGHT, STONE_DARK)[(row + col) % 3]
                cube(f"WallBlock_{side}_{row}_{col}", (x, -1.67, z), (.64, .16, .32), mat, b=.015)
        battlements(f"WallBatt_{side}", cx, -1.28, 2.39, 3.30, 5)

        x = side * 5.02
        cyl(f"CornerTower_{side}_Stone", (x, -1.08, 1.40), 1.22, 2.80, STONE, verts=28, b=.035)
        cyl(f"TowerBandLow_{side}_Stone", (x, -1.08, .40), 1.29, .18, STONE_DARK, verts=28, b=.02)
        cyl(f"TowerBandHigh_{side}_Stone", (x, -1.08, 2.42), 1.27, .16, STONE_LIGHT, verts=28, b=.02)
        for a in range(10):
            ang = math.tau * a / 10
            cube(f"TowerBatt_{side}_{a}", (x + math.cos(ang)*1.0, -1.08 + math.sin(ang)*1.0, 2.96), (.40,.40,.44), STONE, b=.022)
        cube(f"TowerBanner_{side}_Cloth", (x, -2.31, 1.86), (.44,.035,.82), accent, b=.012)

    # Gatehouse and layered rear keep.
    cube("Gatehouse_Cut_Stone", (0, -1.39, 1.38), (2.65, 1.05, 2.76), STONE_LIGHT, b=.065, seg=3)
    cube("GateShadow_Dark_Stone", (0, -1.94, .76), (1.0, .055, 1.35), STONE_DARK, b=.14, seg=3)
    torus("GateArch_Dark_Stone", (0, -1.98, 1.31), .55, .095, STONE_DARK, rot=(math.pi/2,0,0), major_segments=24, minor_segments=8)
    battlements("GateBatt", 0, -1.39, 2.94, 2.30, 4)
    cube("GateBanner_Cloth", (0, -2.01, 2.22), (.60,.035,.90), accent, b=.012)

    cube("RearKeep_Dark_Stone", (0, .78, 1.95), (3.28, 2.20, 3.62), STONE_DARK, b=.075, seg=3)
    cube("RearKeepFace_Stone", (0, -.35, 1.96), (2.92, .17, 3.24), STONE, b=.04)
    for floor in range(3):
        for side in (-1, 1):
            cube(f"KeepWindow_{floor}_{side}", (side*.74, -.45, 1.12 + floor*.76), (.15,.026,.44), STONE_DARK, b=.012)
    battlements("KeepBatt", 0, .77, 3.91, 2.95, 5)

    for side in (-1, 1):
        cube(f"ReturnWall_{side}_Stone", (side*3.55, .14, 1.05), (2.52,.68,1.98), STONE,
             rot=(0,0,math.radians(18*side)), b=.045, seg=3)
        cyl(f"InnerTower_{side}_Stone", (side*2.52,.34,1.34), .86, 2.64, STONE, verts=24, b=.03)
        for a in range(8):
            ang = math.tau*a/8
            cube(f"InnerBatt_{side}_{a}", (side*2.52+math.cos(ang)*.70, .34+math.sin(ang)*.70, 2.78), (.34,.34,.40), STONE_LIGHT, b=.02)

    # Moss/age breakup and metal torch brackets.
    for i, (x,z,sx,sz) in enumerate(((-3.0,.52,.72,.38),(3.45,.76,.52,.31),(-4.65,1.04,.38,.48),(1.72,2.20,.54,.28))):
        cube(f"MossPatch_{i}_Stone", (x,-1.675,z), (sx,.022,sz), MOSS_STONE, b=.014)
    for i, x in enumerate((-4.15,-1.22,1.22,4.15)):
        cyl(f"TorchBracket_{i}_Iron", (x,-2.00,2.08), .03,.44,IRON,verts=10,b=.004)
        ico(f"TorchFlame_{i}", (x,-2.01,2.34), (.075,.065,.14), base.FIRE, sub=2)

    base.export(HERO / f"castle_{team}_hero.glb")


def terrain_height_v2(x, y):
    radial = max(abs(x)/10.7, abs(y)/8.9)
    edge_hill = max(0.0, radial - .52) ** 1.55 * 1.70
    broad = .15*math.sin(x*.38) + .13*math.cos(y*.44) + .09*math.sin((x-y)*.58)
    lane = -.17*math.exp(-(x*x)/7.0)
    river_y = .53*math.sin(x*.46) + .12*math.sin(x*1.05)
    river_basin = -.19*math.exp(-((y-river_y)**2)/.55)
    return .18 + edge_hill + broad + lane + river_basin


def make_tree(prefix, x, y, scale, pine=True):
    z = terrain_height_v2(x, y)
    beam(prefix+"_Trunk_Wood", (x,y,z+.04), (x+RNG.uniform(-.06,.06),y+RNG.uniform(-.05,.05),z+1.14*scale), .105*scale, WOOD, 12)
    if pine:
        for i,(oz,r,h) in enumerate(((.65,.55,.58),(1.00,.48,.56),(1.34,.38,.50),(1.62,.27,.42))):
            ico(prefix+f"_Needles_{i}_Leaf", (x+RNG.uniform(-.07,.07),y+RNG.uniform(-.06,.06),z+oz*scale),
                (r*scale,r*.78*scale,h*scale),(LEAF,LEAF_MID,LEAF_LIGHT)[i%3],sub=2)
    else:
        crowns=[(-.26,.00,1.26,.46),(.25,.04,1.34,.45),(0,-.22,1.48,.41),(.02,.22,1.55,.39),(0,0,1.74,.34)]
        for i,(ox,oy,oz,r) in enumerate(crowns):
            ico(prefix+f"_Crown_{i}_Leaf", (x+ox*scale,y+oy*scale,z+oz*scale), (r*scale,r*.82*scale,r*.88*scale), (LEAF,LEAF_MID,LEAF_LIGHT)[i%3], sub=2)


def build_battlefield():
    base.clear()
    # Monkey-patching keeps the stable mesh builder while giving it much stronger sculpting.
    base.terrain_height = terrain_height_v2
    base.GRASS, base.GRASS2, base.GRASS3, base.DIRT = GRASS, GRASS_LIGHT, GRASS_DARK, DIRT
    base.WATER, base.WATER2 = WATER, WATER
    base.make_terrain_mesh()

    river=[]
    for i in range(39):
        x=-10.5+i*(21.0/38); y=.53*math.sin(x*.46)+.12*math.sin(x*1.05); river.append((x,y))
    base.ribbon("V2_River_Water",river,1.05,WATER,.03)
    road=[]
    for i in range(31):
        y=-8.35+i*(16.7/30); x=.30*math.sin(y*.34); road.append((x,y))
    base.ribbon("V2_MainRoad_Dirt",road,.82,DIRT_LIGHT,.04)

    # Irregular forest walls frame the playable lanes instead of evenly spaced toy trees.
    spots=[]
    for side in (-1,1):
        for y in (-7.2,-6.2,-5.0,-3.7,-2.4,-1.1,1.1,2.4,3.8,5.2,6.5,7.3):
            spots.append((side*(8.0+RNG.uniform(.0,1.2)),y,RNG.uniform(.62,.86),RNG.random()<.72))
        for y in (-6.5,-3.0,2.9,5.8):
            spots.append((side*(6.65+RNG.uniform(.0,.55)),y,RNG.uniform(.52,.70),RNG.random()<.62))
    for i,(x,y,s,pine) in enumerate(spots): make_tree(f"V2_Tree_{i}",x,y,s,pine)

    for i,(x,y,s) in enumerate(((-7.1,-7.5,.88),(-6.5,-1.7,.70),(-5.8,4.8,.66),(-7.4,6.6,.78),(7.2,-7.4,.88),(6.4,-1.5,.72),(5.9,4.9,.65),(7.3,6.5,.80))):
        z=terrain_height_v2(x,y)
        for j in range(4):
            ox=RNG.uniform(-.38,.38)*s; oy=RNG.uniform(-.28,.28)*s
            ico(f"V2_Rock_{i}_{j}_Stone",(x+ox,y+oy,z+.16*s),(RNG.uniform(.25,.44)*s,RNG.uniform(.20,.36)*s,RNG.uniform(.18,.32)*s),(STONE_DARK,STONE,STONE_LIGHT)[j%3],sub=1)

    base.export(HERO / "battlefield_terrain_hero.glb")


def build_opponent():
    base.clear()
    cube("Chair_Dark_Wood",(0,.92,3.04),(2.86,.30,4.45),WOOD,b=.10,seg=3)
    cube("ChairTop_Oak_Wood",(0,.94,5.30),(3.08,.36,.32),WOOD_MID,b=.10,seg=3)

    # Faceted, adult proportions. The old spherical face/large white eyes were the biggest reason
    # the opponent read like a children's toy instead of the reference character.
    cone("Torso_Black_Cloth",(0,-.18,2.90),1.22,.82,2.38,CLOTH,verts=16,rot=(math.radians(7),0,0))
    cube("Chest_Charcoal_Cloth",(0,-.72,3.56),(2.25,.38,1.32),CLOTH_MID,rot=(math.radians(-4),0,0),b=.13,seg=3)
    torus("CloakCollar_Charcoal_Cloth",(0,-.75,4.25),.61,.13,CLOTH_MID,rot=(math.pi/2,0,0),major_segments=28,minor_segments=8)
    cube("Belt_Dark_Leather",(0,-.82,2.28),(1.82,.22,.14),LEATHER,b=.03)
    cube("Buckle_Bronze_Metal",(0,-.95,2.28),(.26,.045,.22),BRONZE,b=.02)

    cyl("Neck_Skin_Shadow",(0,-.77,4.32),.27,.48,SKIN_SHADOW,verts=16,b=.014,do_smooth=True)
    ico("Head_Skin",(0,-1.00,5.00),(.62,.53,.74),SKIN,sub=2)
    ico("Jaw_Skin_Shadow",(0,-1.18,4.72),(.49,.40,.44),SKIN_SHADOW,sub=2)
    cone("Nose_Skin_Shadow",(0,-1.58,4.98),.095,.025,.36,SKIN_SHADOW,verts=12,rot=(math.pi/2,0,0))
    for side in (-1,1):
        x=.225*side
        ico(f"Eye_{side}_Eye",(x,-1.60,5.15),(.046,.024,.036),EYE,sub=2)
        cube(f"Brow_{side}_Hair",(x,-1.60,5.32),(.31,.035,.060),HAIR,rot=(0,0,math.radians(-9*side)),b=.01)
    cube("MouthShadow_Skin",(0,-1.59,4.73),(.22,.030,.034),SKIN_SHADOW,b=.007)

    ico("HairCap_Hair",(0,-.90,5.52),(.69,.55,.39),HAIR,sub=2)
    for i,(x,y,z,sx,sy,sz) in enumerate(((-.40,-1.15,5.48,.29,.20,.31),(-.10,-1.27,5.60,.33,.18,.26),(.22,-1.24,5.58,.34,.19,.27),(.44,-1.11,5.41,.24,.18,.34))):
        ico(f"HairLock_{i}_Hair",(x,y,z),(sx,sy,sz),HAIR_LIGHT if i%2 else HAIR,sub=1)
    ico("BeardCenter_Hair",(0,-1.39,4.62),(.42,.23,.44),HAIR,sub=2)
    ico("BeardLeft_Hair",(-.29,-1.35,4.80),(.28,.20,.33),HAIR_LIGHT,sub=1)
    ico("BeardRight_Hair",(.29,-1.35,4.80),(.28,.20,.33),HAIR,sub=1)
    cone("BeardPoint_Hair",(0,-1.31,4.34),.28,.07,.56,HAIR,verts=12)
    cube("MustacheL_Hair",(-.13,-1.59,4.84),(.24,.030,.052),HAIR,rot=(0,0,math.radians(-10)),b=.010)
    cube("MustacheR_Hair",(.13,-1.59,4.84),(.24,.030,.052),HAIR,rot=(0,0,math.radians(10)),b=.010)

    # Relaxed asymmetrical arms and a smaller held card.
    beam("UpperArmL_Cloth",(-.92,-.58,3.72),(-1.33,-1.10,3.12),.23,CLOTH_MID,16)
    beam("ForearmL_Skin",(-1.33,-1.10,3.12),(-1.04,-1.95,2.53),.19,SKIN,16)
    ico("HandL_Skin",(-1.03,-1.98,2.51),(.30,.23,.20),SKIN,sub=2)
    beam("UpperArmR_Cloth",(.92,-.58,3.72),(1.34,-1.08,3.12),.23,CLOTH_MID,16)
    beam("ForearmR_Skin",(1.34,-1.08,3.12),(1.08,-2.06,2.43),.19,SKIN,16)
    ico("HandR_Skin",(1.07,-2.09,2.41),(.31,.23,.20),SKIN,sub=2)
    cube("HeldCard_Parchment",(-1.16,-2.16,2.91),(.64,.050,.90),PARCHMENT,rot=(math.radians(-12),0,math.radians(-8)),b=.04,seg=3)
    cube("HeldCardInset_Red_Cloth",(-1.16,-2.195,2.91),(.47,.016,.70),RED,rot=(math.radians(-12),0,math.radians(-8)),b=.02)
    torus("Brooch_Bronze_Metal",(0,-1.00,4.13),.15,.042,BRONZE,rot=(math.pi/2,0,0),major_segments=18,minor_segments=6)

    base.export(HERO / "opponent_hero.glb")


def build_tree_asset(name, pine):
    base.clear(); make_tree(name,0,0,1.0,pine); base.export(TERRAIN / f"{name}.glb")


def main():
    print("\n[CastleCards V2] Rebuilding hero assets against approved reference...")
    build_castle("blue")
    build_castle("red")
    build_battlefield()
    build_opponent()
    build_tree_asset("pine_tree", True)
    build_tree_asset("oak_tree", False)
    print("[CastleCards V2] Hero rebuild complete.")


if __name__ == "__main__":
    main()
