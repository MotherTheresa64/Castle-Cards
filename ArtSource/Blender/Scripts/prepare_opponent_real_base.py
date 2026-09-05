"""Prepare the Castle Cards opponent reboot from Blender Studio's CC0 Human Base Meshes.

This deliberately does NOT build a character out of primitives. It locates the official Blender
Studio human-base-mesh bundle acquired by Scripts/Acquire-Quality-Assets.ps1, appends the best
matching realistic male body asset, normalizes it into Castle Cards scale, and saves a clean
editable source .blend. The finished opponent will be authored from this source rather than from
legacy procedural character generators.
"""

import bpy
from pathlib import Path
from mathutils import Vector

ROOT = Path(__file__).resolve().parents[3]
CACHE = ROOT / ".asset-cache" / "blender-human-base" / "bundle-v1.2.0"
OUT = ROOT / "ArtSource" / "Blender" / "HeroSources" / "opponent_real_base.blend"


def clear_scene():
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete(use_global=False)
    for collection in list(bpy.data.collections):
        if collection.users == 0:
            bpy.data.collections.remove(collection)


def score_name(name: str) -> int:
    value = name.lower()
    score = 0
    positive = {
        "realistic": 30,
        "male": 26,
        "body": 20,
        "human": 8,
        "base": 4,
        "mesh": 2,
    }
    negative = {
        "female": 80,
        "stylized": 50,
        "stylised": 50,
        "head": 20,
        "hand": 18,
        "foot": 18,
        "skull": 30,
        "eye": 30,
        "teeth": 30,
        "mouth": 20,
        "armature": 15,
        "rig": 12,
    }
    for token, points in positive.items():
        if token in value:
            score += points
    for token, points in negative.items():
        if token in value:
            score -= points
    return score


def discover_candidate():
    blend_files = sorted(CACHE.rglob("*.blend"))
    if not blend_files:
        raise RuntimeError(
            f"No Human Base Mesh .blend files found under {CACHE}. "
            "Run Scripts/Acquire-Quality-Assets.ps1 first."
        )

    candidates = []
    for blend in blend_files:
        try:
            with bpy.data.libraries.load(str(blend), link=False) as (data_from, _data_to):
                for object_name in data_from.objects:
                    candidates.append((score_name(object_name), "OBJECT", blend, object_name))
                for collection_name in data_from.collections:
                    candidates.append((score_name(collection_name) - 3, "COLLECTION", blend, collection_name))
        except Exception as exc:
            print(f"[CastleCards Art Reboot] Could not inspect {blend}: {exc}")

    candidates.sort(key=lambda item: item[0], reverse=True)
    if not candidates or candidates[0][0] < 20:
        preview = "\n".join(
            f"  {kind}: {name} ({score}) @ {blend.name}"
            for score, kind, blend, name in candidates[:30]
        )
        raise RuntimeError(
            "Could not confidently locate a realistic male body in the Human Base Mesh bundle.\n"
            "Top discovered assets:\n" + preview
        )

    print("[CastleCards Art Reboot] Best source candidates:")
    for score, kind, blend, name in candidates[:10]:
        print(f"  {score:>3} {kind:<10} {name} @ {blend.name}")
    return candidates[0]


def append_candidate(kind: str, blend: Path, name: str):
    if kind == "OBJECT":
        with bpy.data.libraries.load(str(blend), link=False) as (data_from, data_to):
            if name not in data_from.objects:
                raise RuntimeError(f"Object disappeared from source bundle: {name}")
            data_to.objects = [name]
        objects = [obj for obj in data_to.objects if obj is not None]
        for obj in objects:
            if obj.name not in bpy.context.scene.objects:
                bpy.context.collection.objects.link(obj)
        return objects

    with bpy.data.libraries.load(str(blend), link=False) as (data_from, data_to):
        if name not in data_from.collections:
            raise RuntimeError(f"Collection disappeared from source bundle: {name}")
        data_to.collections = [name]
    collections = [col for col in data_to.collections if col is not None]
    for col in collections:
        try:
            bpy.context.scene.collection.children.link(col)
        except RuntimeError:
            pass
    objects = []
    for col in collections:
        objects.extend(list(col.all_objects))
    return list(dict.fromkeys(objects))


def bounds(objects):
    points = []
    for obj in objects:
        if obj.type != "MESH" or not hasattr(obj, "bound_box"):
            continue
        for corner in obj.bound_box:
            points.append(obj.matrix_world @ Vector(corner))
    if not points:
        raise RuntimeError("The selected Human Base Mesh asset contains no mesh geometry.")
    lo = Vector((min(p.x for p in points), min(p.y for p in points), min(p.z for p in points)))
    hi = Vector((max(p.x for p in points), max(p.y for p in points), max(p.z for p in points)))
    return lo, hi


def roots(objects):
    lookup = set(objects)
    return [obj for obj in objects if obj.parent not in lookup]


def normalize(objects):
    lo, hi = bounds(objects)
    size = hi - lo
    height = max(size.z, 1e-5)
    target_height = 5.65
    uniform = target_height / height

    for obj in roots(objects):
        obj.scale *= uniform

    bpy.context.view_layer.update()
    lo, hi = bounds(objects)
    center = (lo + hi) * 0.5
    shift = Vector((-center.x, -center.y, -lo.z))
    for obj in roots(objects):
        obj.location += shift

    bpy.context.view_layer.update()
    lo, hi = bounds(objects)
    print(
        f"[CastleCards Art Reboot] Normalized source size: "
        f"{hi.x-lo.x:.3f} x {hi.y-lo.y:.3f} x {hi.z-lo.z:.3f}"
    )


def clean_names(objects):
    for index, obj in enumerate(objects):
        if obj.type == "MESH":
            obj.name = "OpponentRealBase" if index == 0 else f"OpponentRealBase_{index:02d}"
            if obj.data:
                obj.data.name = obj.name + "_Mesh"


def add_review_floor():
    bpy.ops.mesh.primitive_plane_add(size=12, location=(0, 0, -0.012))
    floor = bpy.context.object
    floor.name = "REVIEW_FLOOR_DELETE_BEFORE_EXPORT"
    mat = bpy.data.materials.new("ReviewNeutral")
    mat.diffuse_color = (0.055, 0.060, 0.065, 1.0)
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    if bsdf:
        bsdf.inputs["Base Color"].default_value = (0.055, 0.060, 0.065, 1.0)
        bsdf.inputs["Roughness"].default_value = 0.92
    floor.data.materials.append(mat)


def main():
    clear_scene()
    score, kind, blend, name = discover_candidate()
    print(f"[CastleCards Art Reboot] Using {kind}: {name} from {blend}")
    objects = append_candidate(kind, blend, name)
    objects = [obj for obj in objects if obj is not None]
    if not objects:
        raise RuntimeError("Human Base Mesh append produced no objects.")

    normalize(objects)
    clean_names(objects)
    add_review_floor()

    for obj in objects:
        obj.select_set(True)
    if objects:
        bpy.context.view_layer.objects.active = objects[0]

    OUT.parent.mkdir(parents=True, exist_ok=True)
    bpy.ops.wm.save_as_mainfile(filepath=str(OUT), check_existing=False)
    print(f"[CastleCards Art Reboot] Clean realistic opponent base saved: {OUT.relative_to(ROOT)}")
    print("[CastleCards Art Reboot] Legacy primitive opponent generators are NOT used by this file.")


if __name__ == "__main__":
    main()
