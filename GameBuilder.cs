using Godot;

public partial class GameBuilder : Node3D
{
    private static readonly Color Wood = new(0.14f, 0.058f, 0.026f);
    private static readonly Color WoodLight = new(0.26f, 0.115f, 0.048f);
    private static readonly Color Parchment = new(0.58f, 0.43f, 0.25f);
    private static readonly Color Blue = new(0.040f, 0.095f, 0.28f);
    private static readonly Color Red = new(0.31f, 0.040f, 0.028f);
    private static readonly Color Felt = new(0.028f, 0.055f, 0.038f);

    private const float BoardY = 0.74f;
    private const float BoardCenterZ = -5.15f;

    public override void _Ready()
    {
        BuildEnvironment();
        BuildTavern();
        BuildWarTable();
        BuildBattlefield();
        BuildPlayerEdge();
        BuildLighting();
        BuildCamera();
        BuildHud();
    }

    private void BuildEnvironment()
    {
        var environment = new Environment
        {
            BackgroundMode = Environment.BGMode.Color,
            BackgroundColor = new Color(0.012f, 0.009f, 0.008f),
            AmbientLightSource = Environment.AmbientSource.Color,
            AmbientLightColor = new Color(0.29f, 0.295f, 0.315f),
            AmbientLightEnergy = 0.78f
        };

        environment.Set("tonemap_mode", 4);
        environment.Set("tonemap_exposure", 1.24f);
        environment.Set("tonemap_agx_contrast", 1.10f);
        environment.Set("ssao_enabled", true);
        environment.Set("ssao_radius", 1.35f);
        environment.Set("ssao_intensity", 1.85f);
        environment.Set("ssao_power", 1.24f);
        environment.Set("ssao_detail", 0.72f);
        environment.Set("ssil_enabled", true);
        environment.Set("ssil_radius", 2.8f);
        environment.Set("ssil_intensity", 0.38f);
        environment.Set("glow_enabled", true);
        environment.Set("glow_intensity", 0.11f);
        environment.Set("glow_bloom", 0.035f);
        environment.Set("fog_enabled", true);
        environment.Set("fog_density", 0.0017f);
        environment.Set("fog_light_color", new Color(0.16f, 0.13f, 0.115f));
        environment.Set("fog_light_energy", 0.30f);

        AddChild(new WorldEnvironment
        {
            Name = "WorldEnvironment",
            Environment = environment
        });
    }

    private void BuildTavern()
    {
        Spawn("hero_tavern", new Vector3(0f, -3.10f, -1.35f), 1.0f, new Vector3(0f, 180f, 0f));
    }

    private void BuildWarTable()
    {
        if (AssetLibrary.Exists("hero_table"))
        {
            Spawn("hero_table", new Vector3(0f, -0.32f, -3.10f), 1.0f);
            return;
        }

        AddBox("WarTableBody", new Vector3(0f, -0.32f, -3.10f), new Vector3(30.2f, 1.0f, 27.0f), Wood);
        AddBox("BoardWell", new Vector3(0f, 0.48f, BoardCenterZ), new Vector3(23.1f, .18f, 18.5f), Felt);
        AddBox("NearRail", new Vector3(0f, 0.67f, 4.05f), new Vector3(23.2f, .28f, .38f), WoodLight);
        AddBox("FarRail", new Vector3(0f, 0.67f, -14.35f), new Vector3(23.2f, .28f, .38f), WoodLight);
        AddBox("LeftRail", new Vector3(-11.42f, 0.67f, BoardCenterZ), new Vector3(.38f, .28f, 18.8f), WoodLight);
        AddBox("RightRail", new Vector3(11.42f, 0.67f, BoardCenterZ), new Vector3(.38f, .28f, 18.8f), WoodLight);
    }

    private void BuildBattlefield()
    {
        Spawn("hero_battlefield", new Vector3(0f, BoardY, BoardCenterZ), 1.0f);

        // The final art pass builds these from authored low-poly castle/tower/wall source meshes.
        // Keep the older procedural castle only as a fallback if generation failed.
        string playerCastle = AssetLibrary.Exists("hero_castle_blue") ? "hero_castle_blue" : "hero_castle";
        string enemyCastle = AssetLibrary.Exists("hero_castle_red") ? "hero_castle_red" : "hero_castle";

        Spawn(playerCastle, new Vector3(0f, BoardY + .01f, 2.58f), .50f);
        Spawn(enemyCastle, new Vector3(0f, BoardY + .01f, -11.95f), .34f, new Vector3(0f, 180f, 0f));

        // The authored opponent is normalized to human scale in Blender. Most of the lower body is
        // below the far rail, leaving the torso/head framed above the enemy castle like the target.
        Spawn("hero_opponent", new Vector3(0f, -2.42f, -15.30f), 1.0f, new Vector3(0f, 180f, 0f));

        Spawn("throne", new Vector3(0f, BoardY + .02f, 2.34f), .17f, new Vector3(0f, 180f, 0f));
        Spawn("king", new Vector3(0f, BoardY + .03f, 2.46f), .20f, new Vector3(0f, 180f, 0f));
        Spawn("throne", new Vector3(0f, BoardY + .02f, -11.64f), .14f);
        Spawn("king", new Vector3(0f, BoardY + .03f, -11.52f), .17f);

        SpawnHeroUnit("hero_spearman", "spearman", new Vector3(-3.55f, BoardY + .03f, 0.62f), .34f, 0f);
        SpawnHeroUnit("hero_swordsman", "swordsman", new Vector3(-1.25f, BoardY + .03f, -.10f), .34f, -5f);
        Spawn("knight", new Vector3(1.12f, BoardY + .03f, -.38f), .29f, new Vector3(0f, -5f, 0f));
        SpawnHeroUnit("hero_archer", "archer", new Vector3(3.45f, BoardY + .03f, .42f), .32f, 8f);

        SpawnHeroUnit("hero_spearman", "spearman", new Vector3(-2.48f, BoardY + .03f, -3.70f), .29f, 13f);
        Spawn("royal_guard", new Vector3(.30f, BoardY + .03f, -4.18f), .28f, new Vector3(0f, -8f, 0f));
        Spawn("wizard", new Vector3(3.18f, BoardY + .03f, -4.95f), .29f, new Vector3(0f, -12f, 0f));

        SpawnHeroUnit("hero_swordsman", "swordsman", new Vector3(-2.60f, BoardY + .03f, -8.30f), .28f, 178f);
        SpawnHeroUnit("hero_archer", "archer", new Vector3(.45f, BoardY + .03f, -8.05f), .27f, 180f);
        Spawn("royal_guard", new Vector3(3.15f, BoardY + .03f, -7.30f), .27f, new Vector3(0f, 171f, 0f));

        Spawn("trebuchet", new Vector3(-7.25f, BoardY + .03f, -1.88f), .26f, new Vector3(0f, -14f, 0f));
        Spawn("catapult", new Vector3(7.15f, BoardY + .03f, -6.10f), .26f, new Vector3(0f, 18f, 0f));
    }

    private void BuildPlayerEdge()
    {
        // Reserve miniatures are intentional gameplay objects. Keeping several physical pieces
        // visible gives the cheating system something tangible to miscount/hide/manipulate.
        SpawnHeroUnit("hero_spearman", "spearman", new Vector3(-11.15f, .76f, 8.56f), .40f, 0f);
        SpawnHeroUnit("hero_swordsman", "swordsman", new Vector3(-9.90f, .76f, 8.62f), .40f, 0f);
        SpawnHeroUnit("hero_archer", "archer", new Vector3(-8.65f, .76f, 8.58f), .39f, 0f);
        SpawnHeroUnit("hero_spearman", "spearman", new Vector3(-7.40f, .76f, 8.64f), .39f, 0f);

        // Three readable physical cards instead of a flat five-card UI strip.
        for (int i = 0; i < 3; i++)
        {
            float x = -1.55f + i * 1.72f;
            float angle = (i - 1f) * 4.0f;
            Color face = i == 1 ? new Color(.20f, .27f, .18f) : Parchment;
            AddRotatedBox($"Card_{i}", new Vector3(x, .75f, 9.18f), new Vector3(1.32f, .060f, 1.82f), face, new Vector3(-7f, 0f, angle));
            AddRotatedBox($"CardArt_{i}", new Vector3(x, .79f, 8.94f), new Vector3(.88f, .018f, .72f), i == 1 ? Blue : Red, new Vector3(-7f, 0f, angle));
        }

        Spawn("cheat_stash", new Vector3(-12.25f, .72f, 9.65f), .27f, new Vector3(0f, 12f, 0f));
        Spawn("spellbook_open", new Vector3(9.70f, .73f, 8.52f), .50f, new Vector3(0f, -10f, 0f));
        Spawn("mana_crystals", new Vector3(7.80f, .74f, 8.78f), .48f, new Vector3(0f, 12f, 0f));
        Spawn("suspicion_dial", new Vector3(11.68f, .74f, 8.68f), .43f, new Vector3(0f, -8f, 0f));
    }

    private void BuildLighting()
    {
        var key = new DirectionalLight3D
        {
            Name = "SoftCoolFill",
            RotationDegrees = new Vector3(-56f, -26f, 0f),
            LightColor = new Color(.56f, .61f, .70f),
            LightEnergy = .40f,
            ShadowEnabled = true
        };
        AddChild(key);

        // Warm tavern key + cool shadow separation, but expose the board enough that model/texture
        // detail survives instead of collapsing into black.
        AddOmni("OpponentWarmKey", new Vector3(3.8f, 7.0f, -13.3f), new Color(1f, .62f, .38f), 1.85f, 9.5f, true);
        AddOmni("OpponentCoolFill", new Vector3(-4.8f, 6.2f, -13.7f), new Color(.42f, .52f, .68f), .96f, 9.0f, false);
        AddOmni("RightLantern", new Vector3(9.8f, 7.6f, -10.0f), new Color(1f, .51f, .25f), 1.55f, 10.0f, true);
        AddOmni("BoardSoftbox", new Vector3(0f, 6.4f, -4.2f), new Color(.90f, .80f, .70f), 1.48f, 16.0f, false);
        AddOmni("BoardCoolLift", new Vector3(-4.0f, 6.7f, -2.5f), new Color(.39f, .49f, .64f), .72f, 14.5f, false);
        AddOmni("PlayerCastleWarm", new Vector3(1.0f, 2.8f, 2.4f), new Color(1f, .48f, .22f), .92f, 4.8f, false);
    }

    private void BuildCamera()
    {
        var camera = new Camera3D
        {
            Name = "PlayerCamera",
            Position = new Vector3(0f, 6.35f, 19.30f),
            Fov = 48.0f,
            Near = 0.08f,
            Far = 120f,
            Current = true
        };
        AddChild(camera);
        camera.LookAt(new Vector3(0f, 1.30f, -5.50f), Vector3.Up);
    }

    private void BuildHud()
    {
        var layer = new CanvasLayer { Name = "HUD" };
        AddChild(layer);

        AddHudPanel(layer, new Vector2(24, 18), new Vector2(162, 34));
        AddHudPanel(layer, new Vector2(1094, 18), new Vector2(162, 34));
        AddHudPanel(layer, new Vector2(520, 18), new Vector2(240, 33));
        AddHudPanel(layer, new Vector2(1102, 658), new Vector2(154, 40));

        AddHudLabel(layer, "CASTLE 20 / 20", new Vector2(35, 25), 15, new Color(.78f, .86f, 1f));
        AddHudLabel(layer, "ENEMY 20 / 20", new Vector2(1104, 25), 15, new Color(1f, .76f, .68f));
        AddHudLabel(layer, "ROUND 1  •  YOUR TURN", new Vector2(538, 25), 14, new Color(.98f, .86f, .64f));
        AddHudLabel(layer, "MANA 5 / 5", new Vector2(1113, 662), 14, new Color(.60f, .76f, 1f));
        AddHudLabel(layer, "SUSPICION 0%", new Vector2(1113, 680), 11, new Color(.90f, .75f, .50f));
    }

    private Node3D Spawn(string name, Vector3 position, float scale, Vector3? rotation = null)
    {
        if (!AssetLibrary.Exists(name))
            return null;
        return AssetLibrary.Spawn(name, this, position, Vector3.One * scale, rotation ?? Vector3.Zero);
    }

    private Node3D SpawnHeroUnit(string heroName, string fallbackName, Vector3 position, float scale, float yaw)
    {
        string name = AssetLibrary.Exists(heroName) ? heroName : fallbackName;
        return Spawn(name, position, scale, new Vector3(0f, yaw, 0f));
    }

    private void AddBox(string name, Vector3 position, Vector3 size, Color color)
    {
        var mesh = new MeshInstance3D
        {
            Name = name,
            Position = position,
            Mesh = new BoxMesh { Size = size },
            MaterialOverride = MakeMaterial(color)
        };
        AddChild(mesh);
    }

    private void AddRotatedBox(string name, Vector3 position, Vector3 size, Color color, Vector3 rotationDegrees)
    {
        var mesh = new MeshInstance3D
        {
            Name = name,
            Position = position,
            RotationDegrees = rotationDegrees,
            Mesh = new BoxMesh { Size = size },
            MaterialOverride = MakeMaterial(color)
        };
        AddChild(mesh);
    }

    private StandardMaterial3D MakeMaterial(Color color)
    {
        return new StandardMaterial3D
        {
            AlbedoColor = color,
            Roughness = .88f
        };
    }

    private void AddOmni(string name, Vector3 position, Color color, float energy, float range, bool shadows)
    {
        var light = new OmniLight3D
        {
            Name = name,
            Position = position,
            LightColor = color,
            LightEnergy = energy,
            OmniRange = range,
            ShadowEnabled = shadows
        };
        AddChild(light);
    }

    private void AddHudPanel(CanvasLayer layer, Vector2 position, Vector2 size)
    {
        var rect = new ColorRect
        {
            Position = position,
            Size = size,
            Color = new Color(.014f, .010f, .010f, .42f),
            MouseFilter = Control.MouseFilterEnum.Ignore
        };
        layer.AddChild(rect);
    }

    private void AddHudLabel(CanvasLayer layer, string text, Vector2 position, int fontSize, Color color)
    {
        var label = new Label
        {
            Text = text,
            Position = position,
            Modulate = color,
            MouseFilter = Control.MouseFilterEnum.Ignore
        };
        label.AddThemeFontSizeOverride("font_size", fontSize);
        layer.AddChild(label);
    }
}
