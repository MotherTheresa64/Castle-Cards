"""Castle Cards final material polish pass.

Runs after geometry generation. It re-imports the visible GLB assets, adds subtle embedded
procedural PBR albedo/normal treatment to the project's flat generated materials, ensures
meshes have UVs where needed, and exports the assets back to GLB. No external texture files
are required at runtime because the generated images are embedded in each GLB.
"""

import bpy
import math
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
SIZE = 128
TAU = math.tau

VISIBLE_ROOTS = [
    ROOT / "Models" / "Hero",
    ROOT / "Models" / "Units" / "Human",
    ROOT / "Models" / "Siege" / "Medieval",
    ROOT / "Models" / "Props" / "Containers",
    ROOT / "Models" / "Props" / "Decor",
    ROOT / "Models" / "Props" / "Gameplay",
    ROOT / "Models" / "Tavern" / "Furniture",
    ROOT / "Models" / "Tavern" / "Lighting",
]

TERRAIN_FILES = [
    ROOT / "Models" / "Terrain" / "Medieval" / "campfire.glb",
    ROOT / "Models" / "Terrain" / "Medieval" / "ruin_wall.glb",
    ROOT / "Models" / "Terrain" / "Medieval" / "watchtower.glb",
    ROOT / "Models" / "Terrain" / "Medieval" / "rock_cluster.glb",
]

FAMILY_TOKENS = {
    "wood": ("wood", "timber", "plank", "oak", "brown"),
    "stone": ("stone", "rock", "mortar", "masonry", "slate"),
    "grass": ("grass", "moss", "ground_green"),
    "dirt": ("dirt", "earth", "mud", "soil"),
    "cloth": ("cloth", "fabric", "cloak", "blue", "red", "banner", "tunic"),
    "leather": ("leather", "hide"),
    "skin": ("skin", "flesh"),
    "hair": ("hair", "beard"),
    "metal": ("iron", "steel", "bronze", "metal", "blade", "armor"),
    "parchment": ("parchment", "paper", "card"),
    "leaf": ("leaf", "foliage", "needle"),
    "water": ("water", "river"),
}

ROUGHNESS = {"wood": .76, "stone": .89, "grass": .95, "dirt": .97, "cloth": .93, "leather": .80, "skin": .67, "hair": .86, "metal": .34, "parchment": .88, "leaf": .92, "water": .20}
NORMAL_STRENGTH = {"wood": 1.7, "stone": 2.6, "grass": 1.9, "dirt": 2.1, "cloth": .75, "leather": 1.1, "skin": .35, "hair": 1.0, "metal": .45, "parchment": .45, "leaf": .8, "water": .65}


def clean_name(value):
    return re.sub(r"[^A-Za-z0-9_]+", "_", value)[:48]


def hash_value(ix, iy, seed):
    value = math.sin(ix * 127.1 + iy * 311.7 + seed * 74.7) * 43758.5453123
    return value - math.floor(value)


def smoothstep(t):
    return t * t * (3.0 - 2.0 * t)


def value_noise(x, y, seed):
    ix = math.floor(x); iy = math.floor(y)
    fx = smoothstep(x - ix); fy = smoothstep(y - iy)
    a = hash_value(ix, iy, seed); b = hash_value(ix + 1, iy, seed)
    c = hash_value(ix, iy + 1, seed); d = hash_value(ix + 1, iy + 1, seed)
    ab = a + (b - a) * fx; cd = c + (d - c) * fx
    return ab + (cd - ab) * fy


def fbm(u, v, seed, scale=4.0, octaves=4):
    total = 0.0; amplitude = .55; frequency = scale; norm = 0.0
    for octave in range(octaves):
        total += value_noise(u * frequency, v * frequency, seed + octave * 13) * amplitude
        norm += amplitude; amplitude *= .5; frequency *= 2.03
    return total / max(norm, 1e-6)


def family_height(family, u, v, seed):
    n = fbm(u, v, seed)
    if family == "wood":
        grain = .5 + .5 * math.sin((u * 9.0 + n * 1.35 + .12 * math.sin(v * 5.0)) * TAU)
        return .60 * grain + .40 * n
    if family == "stone":
        return .72 * fbm(u, v, seed + 5, 3.2, 4) + .28 * fbm(u, v, seed + 21, 18.0, 2)
    if family in ("grass", "dirt", "leaf"):
        return .64 * n + .36 * fbm(u, v, seed + 9, 22.0, 2)
    if family == "cloth":
        weave = .5 + .5 * (math.sin(u * 92.0 * TAU) * math.sin(v * 92.0 * TAU))
        return .82 * n + .18 * weave
    if family == "leather":
        return .72 * n + .28 * fbm(u, v, seed + 31, 32.0, 2)
    if family == "skin":
        return .82 * fbm(u, v, seed + 17, 2.2, 3) + .18 * fbm(u, v, seed + 2, 20.0, 1)
    if family == "hair":
        strands = .5 + .5 * math.sin((u * 34.0 + .3 * n) * TAU)
        return .48 * n + .52 * strands
    if family == "metal":
        scratch = .5 + .5 * math.sin((u * 68.0 + v * 4.0 + n * .4) * TAU)
        return .82 * n + .18 * scratch
    if family == "parchment":
        return .78 * n + .22 * fbm(u, v, seed + 7, 28.0, 1)
    if family == "water":
        waves = .5 + .25 * math.sin((u * 5.5 + v * 1.6) * TAU) + .25 * math.sin((u * 2.4 - v * 5.8) * TAU)
        return .65 * waves + .35 * n
    return n


def classify_material(material):
    name = material.name.lower()
    for family, tokens in FAMILY_TOKENS.items():
        if any(token in name for token in tokens):
            return family
    return None


def get_principled(material):
    if not material.use_nodes:
        material.use_nodes = True
    return material.node_tree.nodes.get("Principled BSDF")


def ensure_uvs(objects):
    for obj in objects:
        if obj.type != "MESH" or len(obj.data.polygons) == 0 or len(obj.data.uv_layers) > 0:
            continue
        bpy.ops.object.select_all(action="DESELECT")
        obj.select_set(True); bpy.context.view_layer.objects.active = obj
        try:
            bpy.ops.object.mode_set(mode="EDIT")
            bpy.ops.mesh.select_all(action="SELECT")
            bpy.ops.uv.smart_project(angle_limit=math.radians(66.0), island_margin=.025)
            bpy.ops.object.mode_set(mode="OBJECT")
        except Exception as exc:
            try: bpy.ops.object.mode_set(mode="OBJECT")
            except Exception: pass
            print(f"[CastleCards Cinematic] UV unwrap skipped for {obj.name}: {exc}")


def generate_images(material, family, base_color, seed):
    heights = [[0.0 for _ in range(SIZE)] for _ in range(SIZE)]
    for y in range(SIZE):
        v = y / max(SIZE - 1, 1)
        for x in range(SIZE):
            u = x / max(SIZE - 1, 1)
            heights[y][x] = family_height(family, u, v, seed)

    albedo_pixels = []; normal_pixels = []
    strength = NORMAL_STRENGTH[family]
    base_r, base_g, base_b = base_color[:3]
    for y in range(SIZE):
        ym = (y - 1) % SIZE; yp = (y + 1) % SIZE
        for x in range(SIZE):
            xm = (x - 1) % SIZE; xp = (x + 1) % SIZE; h = heights[y][x]
            if family == "wood": shade = .82 + h * .34
            elif family == "stone": shade = .76 + h * .42
            elif family in ("grass", "leaf"): shade = .80 + h * .30
            elif family == "dirt": shade = .78 + h * .34
            elif family == "metal": shade = .88 + h * .20
            else: shade = .86 + h * .25
            albedo_pixels.extend((max(0.0, min(1.0, base_r * shade)), max(0.0, min(1.0, base_g * shade)), max(0.0, min(1.0, base_b * shade)), 1.0))
            dx = (heights[y][xm] - heights[y][xp]) * strength
            dy = (heights[ym][x] - heights[yp][x]) * strength; dz = 1.0
            length = math.sqrt(dx * dx + dy * dy + dz * dz)
            nx, ny, nz = dx / length, dy / length, dz / length
            normal_pixels.extend((nx * .5 + .5, ny * .5 + .5, nz * .5 + .5, 1.0))

    stem = clean_name(material.name)
    albedo = bpy.data.images.new(f"CC_{stem}_{family}_Albedo", width=SIZE, height=SIZE, alpha=True)
    albedo.pixels.foreach_set(albedo_pixels); albedo.update()
    normal = bpy.data.images.new(f"CC_{stem}_{family}_Normal", width=SIZE, height=SIZE, alpha=True)
    normal.colorspace_settings.name = "Non-Color"
    normal.pixels.foreach_set(normal_pixels); normal.update()
    try: albedo.pack(); normal.pack()
    except Exception: pass
    return albedo, normal


def decorate_material(material, seed):
    family = classify_material(material)
    if family is None: return False
    bsdf = get_principled(material)
    if bsdf is None: return False
    base_input = bsdf.inputs.get("Base Color")
    if base_input is None or base_input.is_linked: return False
    base_color = tuple(base_input.default_value)
    albedo, normal = generate_images(material, family, base_color, seed)
    nodes = material.node_tree.nodes; links = material.node_tree.links
    albedo_node = nodes.new("ShaderNodeTexImage"); albedo_node.name = "CC_CinematicAlbedo"; albedo_node.image = albedo; albedo_node.interpolation = "Linear"
    links.new(albedo_node.outputs["Color"], base_input)
    normal_tex = nodes.new("ShaderNodeTexImage"); normal_tex.name = "CC_CinematicNormal"; normal_tex.image = normal; normal_tex.interpolation = "Linear"
    normal_map = nodes.new("ShaderNodeNormalMap"); normal_map.name = "CC_CinematicNormalMap"; normal_map.inputs["Strength"].default_value = .58 if family not in ("stone", "dirt") else .78
    links.new(normal_tex.outputs["Color"], normal_map.inputs["Color"]); links.new(normal_map.outputs["Normal"], bsdf.inputs["Normal"])
    rough_input = bsdf.inputs.get("Roughness")
    if rough_input is not None: rough_input.default_value = ROUGHNESS[family]
    metallic_input = bsdf.inputs.get("Metallic")
    if metallic_input is not None and family == "metal": metallic_input.default_value = max(float(metallic_input.default_value), .62)
    return True


def clear_scene_and_data():
    bpy.ops.object.select_all(action="SELECT"); bpy.ops.object.delete(use_global=False)
    for datablocks in (bpy.data.meshes, bpy.data.curves, bpy.data.cameras, bpy.data.lights):
        for block in list(datablocks):
            if block.users == 0: datablocks.remove(block)
    for material in list(bpy.data.materials):
        if material.users == 0: bpy.data.materials.remove(material)
    for image in list(bpy.data.images):
        if image.users == 0 and image.name not in {"Render Result", "Viewer Node"}: bpy.data.images.remove(image)


def process_glb(path, index):
    if not path.exists(): return
    clear_scene_and_data(); bpy.ops.import_scene.gltf(filepath=str(path))
    ensure_uvs(list(bpy.context.scene.objects)); changed = 0
    for material_index, material in enumerate(list(bpy.data.materials)):
        if decorate_material(material, seed=101 + index * 31 + material_index * 7): changed += 1
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.export_scene.gltf(filepath=str(path), export_format="GLB", use_selection=True, export_materials="EXPORT", export_normals=True, export_tangents=True, export_animations=False, export_yup=True)
    print(f"[CastleCards Cinematic] {path.relative_to(ROOT)}: polished {changed} material(s)")


def gather_assets():
    paths = []
    for folder in VISIBLE_ROOTS:
        if folder.exists(): paths.extend(sorted(folder.glob("*.glb")))
    paths.extend(path for path in TERRAIN_FILES if path.exists())
    unique = []; seen = set()
    for path in paths:
        key = str(path.resolve()).lower()
        if key not in seen: seen.add(key); unique.append(path)
    return unique


def main():
    assets = gather_assets()
    print(f"\n[CastleCards Cinematic] Polishing {len(assets)} visible GLB assets...")
    for index, path in enumerate(assets): process_glb(path, index)
    clear_scene_and_data()
    print("[CastleCards Cinematic] Embedded PBR material pass complete.")


if __name__ == "__main__":
    main()
