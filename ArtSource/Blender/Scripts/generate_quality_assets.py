import bpy
import math
from pathlib import Path
from mathutils import Vector

ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / "Models" / "Hero"
CACHE = ROOT / ".asset-cache" / "kaykit"
MED_ROOT = CACHE / "medieval" / "addons" / "kaykit_medieval_hexagon_pack" / "Assets" / "gltf"
ADV_ROOT = CACHE / "adventurers" / "addons" / "kaykit_character_pack_adventures"
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
BARBARIAN = ADV_ROOT / "Characters" / "gltf" / "Barbarian.glb"
BASE_TERRAIN = OUT / "battlefield_terrain_hero.glb"


def require_sources():
    required = [*CASTLE_CENTRAL.values(), *TOWER_A.values(), *TOWER_B.values(), WALL, WALL_GATE,
                BRIDGE, TREE_A, TREE_B, ROCK_A, ROCK_C, BARBARIAN, BASE_TERRAIN]
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

    # Approved references use low, broad curtain-wall fortresses. The previous pass put KayKit's
    # tall fantasy castle at center stage, which created the huge blue spire visible in-game.
    # This composition makes the gatehouse and curtain wall the silhouette, with the keep recessed.
    place_import(WALL_GATE, f"{team}_MainGate", location=(0.0, -0.72, 0.0), target_width=3.15)

    # Front corner towers define a wide defensive line.
    place_import(TOWER_A[team], f"{team}_FrontTowerL", location=(-4.75, -0.55, 0.0), target_height=2.55)
    place_import(TOWER_B[team], f"{team}_FrontTowerR", location=(4.75, -0.55, 0.0), target_height=2.55)

    # Secondary towers sit slightly behind and inward, creating layered depth instead of vertical height.
    place_import(TOWER_B[team], f"{team}_InnerTowerL", location=(-2.65, 1.35, 0.0), target_height=2.20)
    place_import(TOWER_A[team], f"{team}_InnerTowerR", location=(2.65, 1.35, 0.0), target_height=2.20)

    # Recessed keep is deliberately short. It should never rise above the opponent's torso.
    place_import(CASTLE_CENTRAL[team], f"{team}_RearKeep", location=(0.0, 2.45, 0.0), target_height=2.65)

    wall_specs = [
        ((-3.35, -0.55, 0.0), 3.15, 0.0),
        ((3.35, -0.55, 0.0), 3.15, 0.0),
        ((-4.10, 0.75, 0.0), 2.70, -24.0),
        ((4.10, 0.75, 0.0), 2.70, 24.0),
        ((-1.45, 1.65, 0.0), 2.35, 0.0),
        ((1.45, 1.65, 0.0), 2.35, 0.0),
    ]
    for index, (location, width, rotation) in enumerate(wall_specs):
        place_import(WALL, f"{team}_Curtain_{index}", location=location, rotation_deg=rotation, target_width=width)

    export_scene(f"castle_{team}_hero.glb")


def augment_battlefield():
    clear_scene()
    import_gltf(BASE_TERRAIN)
    place_import(BRIDGE, "HeroBridge", location=(-5.05, -0.55, 0.22), target_width=2.70)
    trees = [
        (TREE_A, (-9.0, -5.6, 0.18), 1.55, -16), (TREE_B, (-8.2, -4.7, 0.16), 1.35, 24),
        (TREE_A, (-9.3, 2.6, 0.14), 1.50, 10), (TREE_B, (-8.3, 3.7, 0.12), 1.25, -24),
        (TREE_A, (8.8, -6.2, 0.15), 1.52, 18), (TREE_B, (9.4, -4.9, 0.14), 1.30, -9),
        (TREE_A, (8.7, 2.1, 0.14), 1.48, -20), (TREE_B, (9.4, 3.5, 0.12), 1.28, 31),
        (TREE_B, (6.9, 5.7, 0.10), 1.10, 5), (TREE_A, (-7.3, 6.0, 0.10), 1.16, -30),
    ]
    for index, (path, location, height, rotation) in enumerate(trees):
        place_import(path, f"AuthoredTree_{index}", location=location, rotation_deg=rotation, target_height=height)
    rocks = [
        (ROCK_A, (-7.7, -1.7, 0.08), 0.72, 12), (ROCK_C, (-7.1, 0.3, 0.06), 0.58, -18),
        (ROCK_C, (7.3, -2.4, 0.06), 0.68, 27), (ROCK_A, (7.8, 0.7, 0.05), 0.60, -11),
        (ROCK_C, (5.9, 4.8, 0.05), 0.52, 18), (ROCK_A, (-6.1, 4.7, 0.05), 0.55, -8),
    ]
    for index, (path, location, width, rotation) in enumerate(rocks):
        place_import(path, f"AuthoredRock_{index}", location=location, rotation_deg=rotation, target_width=width)
    export_scene("battlefield_terrain_hero.glb")


def choose_pose_action():
    actions = list(bpy.data.actions)
    if not actions:
        return None
    priorities = ("idle_a", "idle", "relaxed", "interact", "talk")
    lowered = [(action, action.name.lower()) for action in actions]
    for key in priorities:
        for action, name in lowered:
            if key in name:
                return action
    return actions[0]


def freeze_current_character(imported):
    armatures = [obj for obj in imported if obj.type == "ARMATURE"]
    if armatures:
        action = choose_pose_action()
        if action is not None:
            for armature in armatures:
                if armature.animation_data is None:
                    armature.animation_data_create()
                armature.animation_data.action = action
            start, end = action.frame_range
            bpy.context.scene.frame_set(int((start + end) * 0.5))
            bpy.context.view_layer.update()
    depsgraph = bpy.context.evaluated_depsgraph_get()
    static_meshes = []
    for obj in imported:
        if obj.type != "MESH":
            continue
        evaluated = obj.evaluated_get(depsgraph)
        mesh = bpy.data.meshes.new_from_object(evaluated, preserve_all_data_layers=True, depsgraph=depsgraph)
        frozen = bpy.data.objects.new(obj.name + "_Static", mesh)
        bpy.context.collection.objects.link(frozen)
        frozen.matrix_world = obj.matrix_world.copy()
        static_meshes.append(frozen)
    for obj in list(imported):
        if obj.name in bpy.data.objects:
            bpy.data.objects.remove(obj, do_unlink=True)
    if not static_meshes:
        raise RuntimeError("Failed to freeze KayKit character into static meshes.")
    return static_meshes


def normalize_static(objects, target_height):
    lo, hi = world_bounds(objects)
    center = (lo + hi) * 0.5
    height = max(hi.z - lo.z, 1e-5)
    scale = target_height / height
    parent = bpy.data.objects.new("OpponentRoot", None)
    bpy.context.collection.objects.link(parent)
    shift = Vector((-center.x, -center.y, -lo.z))
    for obj in objects:
        obj.location += shift
        matrix = obj.matrix_world.copy()
        obj.parent = parent
        obj.matrix_world = matrix
    parent.scale = (scale, scale, scale)
    return parent


def build_opponent():
    clear_scene()
    imported = import_gltf(BARBARIAN)
    frozen = freeze_current_character(imported)
    root = normalize_static(frozen, target_height=7.25)

    # The KayKit character's authored forward axis is opposite the previous Godot assumption.
    # Rotate the frozen model here so the exported GLB has a stable, intentional front.
    root.rotation_euler[2] = math.radians(180.0)
    root.rotation_euler[0] = math.radians(4.0)
    export_scene("opponent_hero.glb")


def main():
    require_sources()
    build_castle("blue")
    build_castle("red")
    augment_battlefield()
    build_opponent()
    print("[CastleCards Quality] Grounded authored quality pass complete.")


if __name__ == "__main__":
    main()
