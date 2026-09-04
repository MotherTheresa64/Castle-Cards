using Godot;
using System.Collections.Generic;

public static class AssetLibrary
{
    private static readonly Dictionary<string, string> Paths = new()
    {
        ["castle_gatehouse"] = "res://Models/Castles/Medieval/castle_gatehouse.glb",
        ["castle_tower"] = "res://Models/Castles/Medieval/castle_tower.glb",
        ["castle_wall"] = "res://Models/Castles/Medieval/castle_wall.glb",
        ["oak_tree"] = "res://Models/Terrain/Medieval/oak_tree.glb",
        ["spearman"] = "res://Models/Units/Human/spearman.glb",
        ["swordsman"] = "res://Models/Units/Human/swordsman.glb",
        ["archer"] = "res://Models/Units/Human/archer.glb",
        ["catapult"] = "res://Models/Siege/Medieval/catapult.glb",
        ["barrel"] = "res://Models/Props/Containers/barrel.glb",
        ["shelf"] = "res://Models/Tavern/Furniture/shelf.glb",
    };

    private static readonly Dictionary<string, PackedScene> Cache = new();

    public static bool Exists(string name)
    {
        return Paths.TryGetValue(name, out string path) && ResourceLoader.Exists(path);
    }

    public static PackedScene Get(string name)
    {
        if (Cache.TryGetValue(name, out PackedScene cached))
            return cached;

        if (!Paths.TryGetValue(name, out string path))
        {
            GD.PushError($"Unknown asset: {name}");
            return null;
        }

        PackedScene scene = GD.Load<PackedScene>(path);
        if (scene == null)
        {
            GD.PushError($"Failed to load asset: {path}");
            return null;
        }

        Cache[name] = scene;
        return scene;
    }

    public static Node3D Spawn(string name, Node parent, Vector3 position, Vector3 scale, Vector3 rotationDegrees)
    {
        PackedScene scene = Get(name);
        if (scene == null)
            return null;

        Node3D instance = scene.Instantiate<Node3D>();
        parent.AddChild(instance);
        instance.Position = position;
        instance.Scale = scale;
        instance.RotationDegrees = rotationDegrees;
        return instance;
    }

    public static Node3D Spawn(string name, Node parent, Vector3 position, float uniformScale = 1f)
    {
        return Spawn(name, parent, position, Vector3.One * uniformScale, Vector3.Zero);
    }
}
