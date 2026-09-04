import bpy
import math
from pathlib import Path
from mathutils import Vector

ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / "Models" / "Hero"
CACHE = ROOT / ".asset-cache" / "kaykit"
MED_ROOT = CACHE / "medieval" / "addons" / "kaykit_medieval_hexagon_pack" / "Assets" / "gltf"
OUT.mkdir(parents=True, exist_ok=True)

CASTLE_CENTRAL = {
    "blue": MED_ROOT / "buildings" / "blue" / "building_castle_blue.gltf",
    "red": MED_ROOT / "buildings" / "red" / "building_castle_red.gltf",
}
TOWER_A = {
    "blue": MED_ROOT / "buildings" / "blue" / "building_tower_A_blue.gltf",
    "red": MED_ROOT / "buildings" / "red" / "building_tower_A_red.gltf",
}
TOWER_B = {
    "blue": MED_ROOT / "buildings" / "blue" / "building_tower_B_blue.gltf",
    "red": MED_ROOT / "buildings" / "red" / "building_tower_B_red.gltf",
}
WALL = MED_ROOT / "buildings" / "neutral" / "wall_straight.gltf"
WALL_GATE = MED_ROOT / "buildings" / "neutral" / "wall_straight_gate.gltf"
BRIDGE = MED_ROOT / "buildings" / "neutral" / "building_bridge_A.gltf"
TREE_A = MED_ROOT / "decoration" / "nature" / "tree_single_A.gltf"
TREE_B = MED_ROOT / "decoration" / "nature" / "tree_single_B.gltf"
ROCK_A = MED_ROOT / "decoration" / "nature" / "rock_single_A.gltf"
ROCK_C = MED_ROOT / "decoration" / "nature" / "rock_single_C.gltf"
BASE_TERRAIN = OUT / "battlefield_terrain_hero.glb"


def require_sources():
    required = [*CASTLE_CENTRAL.values(), *TOWER_A.values(), *TOWER_B.values(), WALL, WALL_GATE,
                BRIDGE, TREE_A, TREE_B, ROCK_A, ROCK_C, BASE_TERRAIN]
    missing = [str(path) for path in required if not path.exists()]
    if missing:
        raise RuntimeError("Castle Cards quality source assets are missing. Run Scripts/Acquire-Quality-Assets.ps1 first.\n" + "\n".join(missing))


def clear_scene():
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete(use_global=False)


def import_gltf(path):
    before = set(bpy.data.objects)
    bpy.ops.import_scene.gltf(filepath=str(path))
    imported = [obj for obj in bpy.data.objects if obj not in before]
    if not imported:
        raise RuntimeError(f"Blender imported no objects from {path}")
    return imported


def root_objects(objects):
    lookup = set(objects)
    return [obj for obj in objects if obj.parent not in lookup]


def world_bounds(objects):
    points = []
    for obj in objects:
        if obj.type != "MESH" or not hasattr(obj, "bound_box"):
            continue
        for corner in obj.bound_box:
            points.append(obj.matrix_world @ Vector(corner))
    if not points:
        raise RuntimeError("No mesh bounds were available for imported asset.")
    min_v = Vector((min(p.x for p in points), min(p.y for p in points), min(p.z for p in points)))
    max_v = Vector((max(p.x for p in points), max(p.y for p in points), max(p.z for p in points)))
    return min_v, max_v


def place_import(path, label, location=(0, 0, 0), rotation_deg=0.0,
                 target_width=None, target_height=None, target_depth=None):
    objects = import_gltf(path)
    roots = root_objects(objects)
    lo, hi = world_bounds(objects)
    center = (lo + hi) * 0.5
    dims = hi - lo
    shift = Vector((-center.x, -center.y, -lo.z))
    for obj in roots:
        obj.location += shift
    factors = []
    if target_width and dims.x > 1e-5:
        factors.append(target_width / dims.x)
    if target_height and dims.z > 1e-5:
        factors.append(target_height / dims.z)
    if target_depth and dims.y > 1e-5:
        factors.append(target_depth / dims.y)
    scale = min(factors) if factors else 1.0
    parent = bpy.data.objects.new(label, None)
    bpy.context.collection.objects.link(parent)
    for obj in roots:
        matrix = obj.matrix_world.copy()
        obj.parent = parent
        obj.matrix_world = matrix
    parent.scale = (scale, scale, scale)
    parent.rotation_euler[2] = math.radians(rotation_deg)
    parent.location = Vector(location)
    return parent, objects


def export_scene(filename):
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.export_scene.gltf(filepath=str(OUT / filename), export_format="GLB", use_selection=True,
                              export_materials="EXPORT", export_normals=True, export_animations=False)
    print(f"[CastleCards Quality] Exported {filename}")


def build_castle(team):
    clear_scene()

    place_import(WALL_GATE, f"{team}_MainGate", location=(0.0, -1.00, 0.0), target_width=3.30)
    place_import(TOWER_A[team], f"{team}_FrontTowerL", location=(-4.75, -0.78, 0.0), target_height=2.45)
    place_import(TOWER_B[team], f"{team}_FrontTowerR", location=(4.75, -0.78, 0.0), target_height=2.45)
    place_import(TOWER_B[team], f"{team}_OuterTowerL", location=(-6.15, 0.55, 0.0), target_height=2.05)
    place_import(TOWER_A[team], f"{team}_OuterTowerR", location=(6.15, 0.55, 0.0), target_height=2.05)
    place_import(TOWER_B[team], f"{team}_InnerTowerL", location=(-2.55, 1.35, 0.0), target_height=2.15)
    place_import(TOWER_A[team], f"{team}_InnerTowerR", location=(2.55, 1.35, 0.0), target_height=2.15)
    place_import(CASTLE_CENTRAL[team], f"{team}_RearKeep", location=(0.0, 2.60, 0.0), target_height=2.42)

    wall_specs = [
        ((-3.35, -0.78, 0.0), 3.30, 0.0), ((3.35, -0.78, 0.0), 3.30, 0.0),
        ((-5.55, -0.05, 0.0), 2.55, -28.0), ((5.55, -0.05, 0.0), 2.55, 28.0),
        ((-5.00, 1.25, 0.0), 2.35, -8.0), ((5.00, 1.25, 0.0), 2.35, 8.0),
        ((-3.75, 1.78, 0.0), 2.45, -18.0), ((3.75, 1.78, 0.0), 2.45, 18.0),
        ((-1.45, 1.78, 0.0), 2.35, 0.0), ((1.45, 1.78, 0.0), 2.35, 0.0),
    ]
    for index, (location, width, rotation) in enumerate(wall_specs):
        place_import(WALL, f"{team}_Curtain_{index}", location=location, rotation_deg=rotation, target_width=width)

    export_scene(f"castle_{team}_hero.glb")


def augment_battlefield():
    clear_scene()
    import_gltf(BASE_TERRAIN)
    place_import(BRIDGE, "HeroBridge", location=(-5.05, -0.55, 0.22), target_width=2.70)

    trees = [
        (TREE_A, (-9.2, -6.2, 0.18), 1.60, -16), (TREE_B, (-8.45, -5.4, 0.16), 1.38, 24),
        (TREE_A, (-9.0, -3.9, 0.16), 1.44, 8), (TREE_B, (-8.2, -3.0, 0.14), 1.25, -22),
        (TREE_A, (-9.25, -.7, 0.14), 1.42, 18), (TREE_B, (-8.3, .2, 0.12), 1.22, -12),
        (TREE_A, (-9.3, 2.6, 0.14), 1.50, 10), (TREE_B, (-8.3, 3.7, 0.12), 1.25, -24),
        (TREE_B, (-7.25, 5.8, 0.10), 1.12, -30), (TREE_A, (-8.45, 5.1, 0.10), 1.18, 8),
        (TREE_A, (9.2, -6.3, 0.18), 1.58, 18), (TREE_B, (8.45, -5.4, 0.16), 1.34, -9),
        (TREE_A, (9.0, -3.8, 0.16), 1.45, -17), (TREE_B, (8.2, -3.0, 0.14), 1.24, 24),
        (TREE_A, (9.2, -.8, 0.14), 1.43, -20), (TREE_B, (8.25, .2, 0.12), 1.20, 31),
        (TREE_A, (8.8, 2.1, 0.14), 1.48, -20), (TREE_B, (9.4, 3.5, 0.12), 1.28, 31),
        (TREE_B, (6.95, 5.7, 0.10), 1.10, 5), (TREE_A, (8.25, 5.0, 0.10), 1.18, -16),
        (TREE_B, (-5.8, -6.7, 0.10), .92, 11), (TREE_B, (5.9, -6.5, 0.10), .90, -8),
        (TREE_B, (-5.9, 2.9, 0.10), .86, -14), (TREE_B, (5.8, 2.8, 0.10), .88, 16),
    ]
    for index, (path, location, height, rotation) in enumerate(trees):
        place_import(path, f"AuthoredTree_{index}", location=location, rotation_deg=rotation, target_height=height)

    rocks = [
        (ROCK_A, (-7.9, -7.5, 0.08), .78, 12), (ROCK_C, (-6.9, -6.9, 0.06), .58, -18),
        (ROCK_C, (-7.7, -1.7, 0.06), .68, 27), (ROCK_A, (-6.8, -.8, 0.05), .60, -11),
        (ROCK_C, (-6.1, 4.8, 0.05), .52, 18), (ROCK_A, (-7.0, 4.2, 0.05), .55, -8),
        (ROCK_A, (7.9, -7.5, 0.08), .78, -12), (ROCK_C, (6.9, -6.8, 0.06), .58, 18),
        (ROCK_C, (7.5, -2.0, 0.06), .68, -27), (ROCK_A, (6.8, -.7, 0.05), .60, 11),
        (ROCK_C, (5.9, 4.8, 0.05), .52, -18), (ROCK_A, (6.9, 4.1, 0.05), .55, 8),
    ]
    for index, (path, location, width, rotation) in enumerate(rocks):
        place_import(path, f"AuthoredRock_{index}", location=location, rotation_deg=rotation, target_width=width)

    export_scene("battlefield_terrain_hero.glb")


def main():
    require_sources()
    build_castle("blue")
    build_castle("red")
    augment_battlefield()
    print("[CastleCards Quality] Final authored castle/terrain pass complete; approved custom opponent preserved.")


if __name__ == "__main__":
    main()
