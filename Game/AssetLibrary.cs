using Godot;
using System.Collections.Generic;

public static class AssetLibrary
{
    private static readonly Dictionary<string, string> Paths = new()
    {
        // Core castle kit
        ["castle_gatehouse"] = "res://Models/Castles/Medieval/castle_gatehouse.glb",
        ["castle_tower"] = "res://Models/Castles/Medieval/castle_tower.glb",
        ["castle_wall"] = "res://Models/Castles/Medieval/castle_wall.glb",
        ["castle_keep"] = "res://Models/Castles/Medieval/castle_keep.glb",

        // Terrain
        ["oak_tree"] = "res://Models/Terrain/Medieval/oak_tree.glb",
        ["pine_tree"] = "res://Models/Terrain/Medieval/pine_tree.glb",
        ["bush_cluster"] = "res://Models/Terrain/Medieval/bush_cluster.glb",
        ["rock_cluster"] = "res://Models/Terrain/Medieval/rock_cluster.glb",
        ["fence_section"] = "res://Models/Terrain/Medieval/fence_section.glb",
        ["ruin_wall"] = "res://Models/Terrain/Medieval/ruin_wall.glb",
        ["tent"] = "res://Models/Terrain/Medieval/tent.glb",
        ["campfire"] = "res://Models/Terrain/Medieval/campfire.glb",
        ["watchtower"] = "res://Models/Terrain/Medieval/watchtower.glb",
        ["bridge_detail"] = "res://Models/Terrain/Medieval/bridge_detail.glb",

        // Units
        ["spearman"] = "res://Models/Units/Human/spearman.glb",
        ["swordsman"] = "res://Models/Units/Human/swordsman.glb",
        ["archer"] = "res://Models/Units/Human/archer.glb",
        ["knight"] = "res://Models/Units/Human/knight.glb",
        ["ogre"] = "res://Models/Units/Monsters/ogre.glb",

        // Siege
        ["catapult"] = "res://Models/Siege/Medieval/catapult.glb",
        ["ballista"] = "res://Models/Siege/Medieval/ballista.glb",

        // Containers
        ["barrel"] = "res://Models/Props/Containers/barrel.glb",
        ["crate"] = "res://Models/Props/Containers/crate.glb",

        // Tavern furniture
        ["shelf"] = "res://Models/Tavern/Furniture/shelf.glb",
        ["chair"] = "res://Models/Tavern/Furniture/chair.glb",
        ["bench"] = "res://Models/Tavern/Furniture/bench.glb",
        ["small_table"] = "res://Models/Tavern/Furniture/small_table.glb",

        // Tavern lights
        ["chandelier"] = "res://Models/Tavern/Lighting/chandelier.glb",
        ["brazier"] = "res://Models/Tavern/Lighting/brazier.glb",

        // Decorative props
        ["mug"] = "res://Models/Props/Decor/mug.glb",
        ["bottle_cluster"] = "res://Models/Props/Decor/bottle_cluster.glb",
        ["candle_cluster"] = "res://Models/Props/Decor/candle_cluster.glb",
        ["weapon_rack"] = "res://Models/Props/Decor/weapon_rack.glb",
        ["shield_decor"] = "res://Models/Props/Decor/shield_decor.glb",
        ["book_stack"] = "res://Models/Props/Decor/book_stack.glb",
        ["skull"] = "res://Models/Props/Decor/skull.glb",
        ["dice_cluster"] = "res://Models/Props/Decor/dice_cluster.glb",

        // Opponent
        ["opponent"] = "res://Models/Opponent/seated_opponent.glb",
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

    public static void ClearCache()
    {
        Cache.Clear();
    }
}
