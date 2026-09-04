import bpy
import math
from pathlib import Path
from mathutils import Vector

ROOT = Path(__file__).resolve().parents[3]
MODELS_ROOT = ROOT / "Models"
INDIVIDUAL_ROOT = ROOT / "ArtSource" / "Blender" / "IndividualModels"
REVIEW_ROOT = ROOT / "ArtSource" / "Blender" / "ModelReview"
REVIEW_FILE = REVIEW_ROOT / "AllModels_Review.blend"


def clear_scene():
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete(use_global=False)
    for collection in list(bpy.data.collections):
        if collection.name != "Collection" and collection.users == 0:
            bpy.data.collections.remove(collection)


def import_glb(path: Path):
    before = set(bpy.data.objects)
    bpy.ops.import_scene.gltf(filepath=str(path))
    imported = [obj for obj in bpy.data.objects if obj not in before]
    if not imported:
        raise RuntimeError(f"No objects were imported from {path}")
    return imported


def mesh_bounds(objects):
    points = []
    for obj in objects:
        if obj.type != "MESH" or not hasattr(obj, "bound_box"):
            continue
        for corner in obj.bound_box:
            points.append(obj.matrix_world @ Vector(corner))
    if not points:
        return Vector((-1, -1, 0)), Vector((1, 1, 2))
    lo = Vector((min(p.x for p in points), min(p.y for p in points), min(p.z for p in points)))
    hi = Vector((max(p.x for p in points), max(p.y for p in points), max(p.z for p in points)))
    return lo, hi


def root_objects(objects):
    lookup = set(objects)
    return [obj for obj in objects if obj.parent not in lookup]


def center_on_origin(objects):
    lo, hi = mesh_bounds(objects)
    center = (lo + hi) * 0.5
    roots = root_objects(objects)
    shift = Vector((-center.x, -center.y, -lo.z))
    for obj in roots:
        obj.location += shift
    return hi - lo


def save_individual(path: Path, relative: Path):
    clear_scene()
    objects = import_glb(path)
    center_on_origin(objects)
    out = (INDIVIDUAL_ROOT / relative).with_suffix(".blend")
    out.parent.mkdir(parents=True, exist_ok=True)
    bpy.ops.wm.save_as_mainfile(filepath=str(out), check_existing=False)
    print(f"[CastleCards ModelReview] Individual: {out.relative_to(ROOT)}")
    return out


def make_label(text, location, scale=0.42):
    bpy.ops.object.text_add(location=location, rotation=(math.radians(90), 0, 0))
    label = bpy.context.object
    label.name = "Label_" + text.replace("/", "_")[:48]
    label.data.body = text
    label.data.align_x = "CENTER"
    label.data.align_y = "CENTER"
    label.data.size = scale
    label.data.extrude = 0.01
    return label


def build_review(model_files):
    clear_scene()
    REVIEW_ROOT.mkdir(parents=True, exist_ok=True)

    cols = max(5, int(math.ceil(math.sqrt(len(model_files)))))
    cell_x = 7.0
    cell_y = 7.0

    for index, path in enumerate(model_files):
        relative = path.relative_to(MODELS_ROOT)
        objects = import_glb(path)
        dims = center_on_origin(objects)
        roots = root_objects(objects)

        max_dim = max(dims.x, dims.y, dims.z, 0.001)
        review_scale = min(1.0, 4.3 / max_dim)
        col = index % cols
        row = index // cols
        position = Vector(((col - (cols - 1) * 0.5) * cell_x, row * cell_y, 0))

        for obj in roots:
            obj.scale *= review_scale
            obj.location = obj.location * review_scale + position

        make_label(relative.as_posix(), (position.x, position.y - 2.75, 0.05), 0.33)

    rows = max(1, int(math.ceil(len(model_files) / cols)))
    bpy.ops.mesh.primitive_plane_add(size=2, location=(0, (rows - 1) * cell_y * 0.5, -0.03))
    floor = bpy.context.object
    floor.name = "ReviewFloor"
    floor.scale = (cols * cell_x * 0.55, rows * cell_y * 0.55, 1)

    bpy.ops.object.light_add(type="AREA", location=(0, rows * cell_y * 0.35, 18))
    key = bpy.context.object
    key.name = "ReviewKey"
    key.data.energy = 1800
    key.data.shape = "DISK"
    key.data.size = 12

    bpy.ops.object.light_add(type="AREA", location=(-14, rows * cell_y * 0.25, 9))
    fill = bpy.context.object
    fill.name = "ReviewFill"
    fill.data.energy = 900
    fill.data.size = 10
    fill.rotation_euler = (math.radians(45), 0, math.radians(-35))

    # Do not force a render engine here. Blender's accepted engine identifiers differ
    # between versions, and this workspace is intended for inspection/editing rather
    # than a final render. Leaving the user's/default engine untouched is the most
    # version-compatible behavior.
    scene = bpy.context.scene
    scene.render.resolution_x = 1600
    scene.render.resolution_y = 900
    scene.render.resolution_percentage = 100

    bpy.ops.wm.save_as_mainfile(filepath=str(REVIEW_FILE), check_existing=False)
    print(f"[CastleCards ModelReview] Review workspace: {REVIEW_FILE.relative_to(ROOT)}")


def main():
    if not MODELS_ROOT.exists():
        raise RuntimeError("Models folder does not exist. Run Update-Project.bat first so the GLB assets are generated.")

    model_files = sorted(p for p in MODELS_ROOT.rglob("*.glb") if p.is_file())
    if not model_files:
        raise RuntimeError("No GLB assets were found under Models. Run Update-Project.bat first.")

    INDIVIDUAL_ROOT.mkdir(parents=True, exist_ok=True)
    print(f"[CastleCards ModelReview] Preparing {len(model_files)} individual Blender files...")
    for path in model_files:
        save_individual(path, path.relative_to(MODELS_ROOT))

    print("[CastleCards ModelReview] Building all-model review workspace...")
    build_review(model_files)
    print(f"[CastleCards ModelReview] Complete. {len(model_files)} individual .blend files created.")


if __name__ == "__main__":
    main()
