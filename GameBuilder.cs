using Godot;

public partial class GameBuilder : Node3D
{
    private static readonly Color Wood = new(0.14f, 0.058f, 0.026f);
    private static readonly Color WoodLight = new(0.26f, 0.115f, 0.048f);
    private static readonly Color Parchment = new(0.63f, 0.48f, 0.29f);
    private static readonly Color Blue = new(0.040f, 0.095f, 0.28f);
    private static readonly Color BlueLight = new(0.10f, 0.22f, 0.52f);
    private static readonly Color Red = new(0.34f, 0.040f, 0.028f);
    private static readonly Color Felt = new(0.028f, 0.055f, 0.038f);

    private const float BoardY = 0.74f;
    private const float BoardCenterZ = -5.15f;

    public override void _Ready()
    {
        BuildEnvironment();
        BuildTavern();
        BuildWarTable();
        BuildTavernDress();
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
            BackgroundColor = new Color(0.008f, 0.006f, 0.005f),
            AmbientLightSource = Environment.AmbientSource.Color,
            AmbientLightColor = new Color(0.25f, 0.22f, 0.20f),
            AmbientLightEnergy = 0.74f
        };

        environment.Set("tonemap_mode", 4);
        environment.Set("tonemap_exposure", 1.55f);
        environment.Set("tonemap_agx_contrast", 1.10f);
        environment.Set("ssao_enabled", true);
        environment.Set("ssao_radius", 1.72f);
        environment.Set("ssao_intensity", 2.22f);
        environment.Set("ssao_power", 1.25f);
        environment.Set("ssao_detail", 0.92f);
        environment.Set("ssil_enabled", true);
        environment.Set("ssil_radius", 2.85f);
        environment.Set("ssil_intensity", 0.52f);
        environment.Set("glow_enabled", true);
        environment.Set("glow_intensity", 0.19f);
        environment.Set("glow_bloom", 0.055f);
        environment.Set("fog_enabled", true);
        environment.Set("fog_density", 0.0015f);
        environment.Set("fog_light_color", new Color(0.22f, 0.13f, 0.075f));
        environment.Set("fog_light_energy", 0.38f);

        AddChild(new WorldEnvironment { Name = "WorldEnvironment", Environment = environment });
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

    private void BuildTavernDress()
    {
        // The approved concepts frame the board with tavern storytelling rather than a bare wall.
        Spawn("barrel", new Vector3(-10.7f, 0.10f, -11.5f), 1.55f, new Vector3(0f, 16f, 0f));
        Spawn("barrel", new Vector3(-9.45f, -0.08f, -12.15f), 1.10f, new Vector3(0f, -18f, 0f));
        Spawn("crate", new Vector3(10.0f, -0.18f, -11.7f), 1.45f, new Vector3(0f, -14f, 0f));
        Spawn("crate", new Vector3(11.0f, 0.08f, -12.6f), 1.05f, new Vector3(0f, 8f, 0f));

        Spawn("weapon_rack", new Vector3(-7.9f, 0.05f, -16.4f), 1.38f, new Vector3(0f, 180f, 0f));
        Spawn("shield_decor", new Vector3(-10.6f, 2.65f, -17.0f), 1.10f, new Vector3(0f, 180f, 0f));
        Spawn("shelf", new Vector3(8.1f, 0.18f, -16.7f), 1.46f, new Vector3(0f, 180f, 0f));
        Spawn("bottle_cluster", new Vector3(8.0f, 2.10f, -16.2f), 1.14f, new Vector3(0f, 180f, 0f));
        Spawn("book_stack", new Vector3(10.25f, 1.55f, -16.15f), 1.08f, new Vector3(0f, 175f, 0f));
        Spawn("skull", new Vector3(6.65f, 2.20f, -16.18f), .82f, new Vector3(0f, 165f, 0f));

        Spawn("candle_cluster", new Vector3(-9.0f, 1.05f, -10.7f), 1.22f);
        Spawn("candle_cluster", new Vector3(9.0f, 1.16f, -10.8f), 1.18f);
        Spawn("mug", new Vector3(-10.25f, .72f, -8.6f), 1.18f, new Vector3(0f, 24f, 0f));

        AddBox("BlueTavernBanner", new Vector3(-12.2f, 4.10f, -16.75f), new Vector3(1.70f, 3.85f, .07f), Blue);
        AddBox("RedTavernBanner", new Vector3(12.2f, 4.10f, -16.75f), new Vector3(1.70f, 3.85f, .07f), Red);
        AddBox("BlueBannerPole", new Vector3(-12.2f, 6.15f, -16.72f), new Vector3(2.15f, .10f, .10f), WoodLight);
        AddBox("RedBannerPole", new Vector3(12.2f, 6.15f, -16.72f), new Vector3(2.15f, .10f, .10f), WoodLight);
    }

    private void BuildBattlefield()
    {
        Spawn("hero_battlefield", new Vector3(0f, BoardY, BoardCenterZ), 1.0f);

        string playerCastle = AssetLibrary.Exists("hero_castle_blue") ? "hero_castle_blue" : "hero_castle";
        string enemyCastle = AssetLibrary.Exists("hero_castle_red") ? "hero_castle_red" : "hero_castle";

        // Reference #1 hierarchy: a substantial player fortress in the near third and a smaller enemy fortress.
        Spawn(playerCastle, new Vector3(0f, BoardY + .01f, 1.55f), .69f);
        Spawn(enemyCastle, new Vector3(0f, BoardY + .01f, -11.15f), .36f, new Vector3(0f, 180f, 0f));

        // Human-sized opponent rises immediately behind the enemy side and leans over the board.
        Spawn("hero_opponent", new Vector3(0f, -0.72f, -14.65f), 1.34f);

        Spawn("throne", new Vector3(0f, BoardY + .02f, 1.50f), .17f, new Vector3(0f, 180f, 0f));
        Spawn("king", new Vector3(0f, BoardY + .03f, 1.60f), .20f, new Vector3(0f, 180f, 0f));
        Spawn("throne", new Vector3(0f, BoardY + .02f, -11.02f), .13f);
        Spawn("king", new Vector3(0f, BoardY + .03f, -10.92f), .16f);

        // Blue defensive rank immediately outside the fortress.
        SpawnHeroUnit("hero_spearman", "spearman", new Vector3(-4.80f, BoardY + .03f, -.15f), .35f, 0f);
        SpawnHeroUnit("hero_swordsman", "swordsman", new Vector3(-3.20f, BoardY + .03f, -.38f), .35f, -4f);
        Spawn("knight", new Vector3(-1.60f, BoardY + .03f, -.56f), .31f);
        Spawn("royal_guard", new Vector3(0f, BoardY + .03f, -.62f), .30f);
        Spawn("knight", new Vector3(1.60f, BoardY + .03f, -.56f), .31f);
        SpawnHeroUnit("hero_archer", "archer", new Vector3(3.20f, BoardY + .03f, -.38f), .34f, 4f);
        SpawnHeroUnit("hero_spearman", "spearman", new Vector3(4.80f, BoardY + .03f, -.15f), .35f, 0f);

        // Contested center: enough units to feel alive without burying the terrain.
        SpawnHeroUnit("hero_spearman", "spearman", new Vector3(-4.1f, BoardY + .03f, -3.15f), .28f, 12f);
        Spawn("royal_guard", new Vector3(-1.85f, BoardY + .03f, -3.95f), .28f, new Vector3(0f, -8f, 0f));
        Spawn("wizard", new Vector3(.45f, BoardY + .03f, -4.25f), .29f, new Vector3(0f, -10f, 0f));
        SpawnHeroUnit("hero_archer", "archer", new Vector3(2.70f, BoardY + .03f, -3.72f), .28f, 8f);
        SpawnHeroUnit("hero_swordsman", "swordsman", new Vector3(4.45f, BoardY + .03f, -4.45f), .28f, 14f);

        // Enemy formation near the far fortress.
        SpawnHeroUnit("hero_swordsman", "swordsman", new Vector3(-4.15f, BoardY + .03f, -8.55f), .27f, 178f);
        Spawn("royal_guard", new Vector3(-2.55f, BoardY + .03f, -8.92f), .27f, new Vector3(0f, 180f, 0f));
        SpawnHeroUnit("hero_archer", "archer", new Vector3(-.85f, BoardY + .03f, -9.12f), .27f, 180f);
        SpawnHeroUnit("hero_spearman", "spearman", new Vector3(.90f, BoardY + .03f, -9.10f), .27f, 180f);
        Spawn("wizard", new Vector3(2.55f, BoardY + .03f, -8.90f), .27f, new Vector3(0f, 180f, 0f));
        SpawnHeroUnit("hero_swordsman", "swordsman", new Vector3(4.15f, BoardY + .03f, -8.48f), .27f, 182f);

        Spawn("trebuchet", new Vector3(-7.15f, BoardY + .03f, -1.55f), .28f, new Vector3(0f, -14f, 0f));
        Spawn("catapult", new Vector3(6.95f, BoardY + .03f, -5.95f), .28f, new Vector3(0f, 18f, 0f));
        Spawn("ballista", new Vector3(-6.65f, BoardY + .03f, -7.25f), .24f, new Vector3(0f, 168f, 0f));

        Spawn("campfire", new Vector3(-7.7f, BoardY + .02f, -5.4f), .34f);
        Spawn("ruin_wall", new Vector3(7.55f, BoardY + .02f, -2.0f), .36f, new Vector3(0f, 20f, 0f));
    }

    private void BuildPlayerEdge()
    {
        // Reserve tray is physically reachable and visually supports the cheating mechanic.
        AddBox("ReserveTrayBase", new Vector3(-6.70f, .66f, 6.45f), new Vector3(5.25f, .16f, 2.00f), new Color(.085f, .036f, .018f));
        AddBox("ReserveTrayBack", new Vector3(-6.70f, .82f, 5.55f), new Vector3(5.30f, .32f, .14f), WoodLight);
        AddBox("ReserveTrayFront", new Vector3(-6.70f, .82f, 7.35f), new Vector3(5.30f, .32f, .14f), WoodLight);

        float[] reserveX = { -8.55f, -7.35f, -6.15f, -4.95f, 4.85f, 6.05f, 7.25f, 8.45f };
        string[] hero = { "hero_spearman", "hero_swordsman", "hero_archer", "hero_spearman", "hero_archer", "hero_swordsman", "hero_spearman", "hero_archer" };
        string[] fallback = { "spearman", "swordsman", "archer", "spearman", "archer", "swordsman", "spearman", "archer" };
        for (int i = 0; i < reserveX.Length; i++)
        {
            float z = i < 4 ? 6.32f + (i % 2) * .12f : 6.28f + (i % 2) * .12f;
            SpawnHeroUnit(hero[i], fallback[i], new Vector3(reserveX[i], .76f, z), .37f, 0f);
        }

        // Three readable physical cards occupy the player hand zone from the approved target.
        for (int i = 0; i < 3; i++)
        {
            float x = -1.82f + i * 1.82f;
            float angle = (i - 1) * 4.0f;
            Color face = i == 1 ? new Color(.66f, .50f, .30f) : Parchment;
            Color art = i == 0 ? BlueLight : (i == 1 ? new Color(.31f, .25f, .12f) : new Color(.24f, .15f, .30f));
            AddRotatedBox($"Card_{i}", new Vector3(x, .75f, 7.10f), new Vector3(1.42f, .065f, 1.95f), face, new Vector3(-7f, 0f, angle));
            AddRotatedBox($"CardArt_{i}", new Vector3(x, .80f, 6.83f), new Vector3(.95f, .018f, .82f), art, new Vector3(-7f, 0f, angle));
            AddRotatedBox($"CardTitle_{i}", new Vector3(x, .805f, 7.52f), new Vector3(.92f, .014f, .12f), new Color(.095f, .070f, .045f), new Vector3(-7f, 0f, angle));
        }

        // Physical draw deck on the right.
        for (int i = 0; i < 7; i++)
        {
            AddRotatedBox($"DeckCard_{i}", new Vector3(9.20f + i * .035f, .73f + i * .035f, 6.95f - i * .025f), new Vector3(1.55f, .055f, 2.02f), Blue, new Vector3(-4f, 0f, -8f));
        }
        AddRotatedBox("DeckEmblem", new Vector3(9.38f, 1.00f, 6.70f), new Vector3(.72f, .018f, .72f), new Color(.58f, .38f, .10f), new Vector3(-4f, 0f, -8f));

        Spawn("cheat_stash", new Vector3(-9.45f, .74f, 7.00f), .34f, new Vector3(0f, 10f, 0f));
        Spawn("dice_cluster", new Vector3(-8.65f, .76f, 7.12f), .42f);
        Spawn("mana_crystals", new Vector3(7.95f, .76f, 7.38f), .40f, new Vector3(0f, 12f, 0f));
        Spawn("suspicion_dial", new Vector3(6.95f, .76f, 7.45f), .35f, new Vector3(0f, -8f, 0f));
    }

    private void BuildLighting()
    {
        var fill = new DirectionalLight3D
        {
            Name = "CoolAmbientFill",
            RotationDegrees = new Vector3(-56f, -22f, 0f),
            LightColor = new Color(.48f, .52f, .60f),
            LightEnergy = .32f,
            ShadowEnabled = true
        };
        AddChild(fill);

        AddOmni("OpponentWarmKey", new Vector3(3.7f, 7.2f, -13.15f), new Color(1f, .52f, .23f), 2.95f, 11.2f, true);
        AddOmni("OpponentFaceFill", new Vector3(-3.3f, 6.2f, -12.7f), new Color(.50f, .58f, .70f), .88f, 9.0f, false);
        AddOmni("BoardCenterWarm", new Vector3(-1.4f, 5.5f, -4.4f), new Color(1f, .67f, .37f), 2.05f, 12.8f, true);
        AddOmni("BoardCoolLift", new Vector3(5.4f, 5.8f, -2.6f), new Color(.42f, .50f, .62f), .72f, 12.0f, false);
        AddOmni("PlayerCastleTorchL", new Vector3(-4.7f, 3.0f, 1.4f), new Color(1f, .38f, .12f), 1.42f, 5.5f, true);
        AddOmni("PlayerCastleTorchR", new Vector3(4.7f, 3.0f, 1.4f), new Color(1f, .38f, .12f), 1.42f, 5.5f, true);
        AddOmni("LeftTavernLantern", new Vector3(-10.4f, 6.8f, -9.7f), new Color(1f, .43f, .16f), 1.75f, 8.8f, true);
        AddOmni("RightTavernLantern", new Vector3(10.1f, 7.0f, -10.0f), new Color(1f, .47f, .18f), 1.72f, 8.8f, true);
        AddOmni("NearTableCandle", new Vector3(-10.0f, 2.0f, 5.7f), new Color(1f, .45f, .16f), 1.25f, 5.0f, true);
    }

    private void BuildCamera()
    {
        // Locked against approved concept #1: intimate player-seat view with board dominating the frame.
        var camera = new Camera3D
        {
            Name = "PlayerCamera",
            Position = new Vector3(0f, 7.35f, 13.65f),
            Fov = 50.0f,
            Near = 0.08f,
            Far = 120f,
            Current = true
        };
        AddChild(camera);
        camera.LookAt(new Vector3(0f, 1.46f, -4.70f), Vector3.Up);
    }

    private void BuildHud()
    {
        var layer = new CanvasLayer { Name = "HUD" };
        AddChild(layer);

        AddHudPanel(layer, new Vector2(18, 16), new Vector2(188, 38));
        AddHudPanel(layer, new Vector2(1074, 16), new Vector2(188, 38));
        AddHudPanel(layer, new Vector2(516, 16), new Vector2(248, 36));
        AddHudPanel(layer, new Vector2(1090, 650), new Vector2(172, 48));

        AddHudLabel(layer, "CASTLE 20 / 20", new Vector2(34, 25), 16, new Color(.78f, .87f, 1f));
        AddHudLabel(layer, "ENEMY 20 / 20", new Vector2(1094, 25), 16, new Color(1f, .79f, .70f));
        AddHudLabel(layer, "ROUND 1  •  YOUR TURN", new Vector2(536, 24), 15, new Color(.99f, .87f, .64f));
        AddHudLabel(layer, "MANA 5 / 5", new Vector2(1108, 655), 15, new Color(.62f, .78f, 1f));
        AddHudLabel(layer, "SUSPICION 0%", new Vector2(1108, 676), 11, new Color(.92f, .76f, .48f));
    }

    private Node3D Spawn(string name, Vector3 position, float scale, Vector3? rotation = null)
    {
        if (!AssetLibrary.Exists(name)) return null;
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

    private StandardMaterial3D MakeMaterial(Color color) => new()
    {
        AlbedoColor = color,
        Roughness = .88f
    };

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
            Color = new Color(.014f, .010f, .010f, .58f),
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
