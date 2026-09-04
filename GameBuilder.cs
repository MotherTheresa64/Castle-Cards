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
            BackgroundColor = new Color(0.007f, 0.005f, 0.004f),
            AmbientLightSource = Environment.AmbientSource.Color,
            AmbientLightColor = new Color(0.24f, 0.21f, 0.19f),
            AmbientLightEnergy = 0.62f
        };

        environment.Set("tonemap_mode", 4);
        environment.Set("tonemap_exposure", 1.62f);
        environment.Set("tonemap_agx_contrast", 1.16f);
        environment.Set("ssao_enabled", true);
        environment.Set("ssao_radius", 1.90f);
        environment.Set("ssao_intensity", 2.35f);
        environment.Set("ssao_power", 1.28f);
        environment.Set("ssao_detail", 0.96f);
        environment.Set("ssil_enabled", true);
        environment.Set("ssil_radius", 3.0f);
        environment.Set("ssil_intensity", 0.56f);
        environment.Set("glow_enabled", true);
        environment.Set("glow_intensity", 0.20f);
        environment.Set("glow_bloom", 0.06f);
        environment.Set("fog_enabled", true);
        environment.Set("fog_density", 0.00135f);
        environment.Set("fog_light_color", new Color(0.23f, 0.135f, 0.075f));
        environment.Set("fog_light_energy", 0.40f);

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
        // Keep the room asymmetric and busy around the edges, while leaving a clean silhouette behind the opponent.
        Spawn("barrel", new Vector3(-10.9f, 0.10f, -11.65f), 1.60f, new Vector3(0f, 16f, 0f));
        Spawn("barrel", new Vector3(-9.45f, -0.08f, -12.50f), 1.08f, new Vector3(0f, -18f, 0f));
        Spawn("crate", new Vector3(10.2f, -0.18f, -11.80f), 1.38f, new Vector3(0f, -14f, 0f));
        Spawn("crate", new Vector3(11.1f, 0.05f, -12.75f), 1.02f, new Vector3(0f, 8f, 0f));

        Spawn("weapon_rack", new Vector3(-9.25f, 0.02f, -16.55f), 1.18f, new Vector3(0f, 180f, 0f));
        Spawn("shield_decor", new Vector3(-11.0f, 2.65f, -17.05f), 1.05f, new Vector3(0f, 180f, 0f));
        Spawn("shelf", new Vector3(9.15f, 0.18f, -16.75f), 1.32f, new Vector3(0f, 180f, 0f));
        Spawn("bottle_cluster", new Vector3(8.75f, 2.12f, -16.20f), 1.10f, new Vector3(0f, 180f, 0f));
        Spawn("book_stack", new Vector3(10.35f, 1.55f, -16.15f), 1.03f, new Vector3(0f, 175f, 0f));
        Spawn("skull", new Vector3(7.35f, 2.20f, -16.18f), .78f, new Vector3(0f, 165f, 0f));

        Spawn("candle_cluster", new Vector3(-9.2f, 1.05f, -10.65f), 1.22f);
        Spawn("candle_cluster", new Vector3(9.1f, 1.16f, -10.75f), 1.18f);
        Spawn("mug", new Vector3(-10.3f, .72f, -8.55f), 1.15f, new Vector3(0f, 24f, 0f));

        AddBox("BlueTavernBanner", new Vector3(-12.8f, 4.20f, -16.90f), new Vector3(1.25f, 3.55f, .07f), Blue);
        AddBox("RedTavernBanner", new Vector3(12.8f, 4.20f, -16.90f), new Vector3(1.25f, 3.55f, .07f), Red);
        AddBox("BlueBannerPole", new Vector3(-12.8f, 6.05f, -16.87f), new Vector3(1.75f, .10f, .10f), WoodLight);
        AddBox("RedBannerPole", new Vector3(12.8f, 6.05f, -16.87f), new Vector3(1.75f, .10f, .10f), WoodLight);
    }

    private void BuildBattlefield()
    {
        Spawn("hero_battlefield", new Vector3(0f, BoardY, BoardCenterZ), 1.0f);

        string playerCastle = AssetLibrary.Exists("hero_castle_blue") ? "hero_castle_blue" : "hero_castle";
        string enemyCastle = AssetLibrary.Exists("hero_castle_red") ? "hero_castle_red" : "hero_castle";

        // Approved reference #1: broad foreground fortress, clearly smaller enemy fortress, and the opponent towering behind both.
        Spawn(playerCastle, new Vector3(0f, BoardY + .01f, 1.20f), .82f);
        Spawn(enemyCastle, new Vector3(0f, BoardY + .01f, -11.15f), .43f, new Vector3(0f, 180f, 0f));

        // Lowering the human behind the table hides the standing lower body and makes the pose read as seated/leaning.
        Spawn("hero_opponent", new Vector3(0f, -2.08f, -14.45f), 1.58f, new Vector3(8f, 0f, 0f));

        Spawn("throne", new Vector3(0f, BoardY + .02f, 1.30f), .18f, new Vector3(0f, 180f, 0f));
        Spawn("king", new Vector3(0f, BoardY + .03f, 1.42f), .21f, new Vector3(0f, 180f, 0f));
        Spawn("throne", new Vector3(0f, BoardY + .02f, -10.98f), .14f);
        Spawn("king", new Vector3(0f, BoardY + .03f, -10.88f), .17f);

        // Castle-edge fire and siege silhouettes create the fortified foreground seen in the approved concepts.
        Spawn("castle_brazier", new Vector3(-5.45f, BoardY + .02f, 1.12f), .42f);
        Spawn("castle_brazier", new Vector3(5.45f, BoardY + .02f, 1.12f), .42f);
        Spawn("trebuchet", new Vector3(-6.45f, BoardY + .03f, -.70f), .30f, new Vector3(0f, -8f, 0f));
        Spawn("ballista", new Vector3(6.35f, BoardY + .03f, -.55f), .27f, new Vector3(0f, 8f, 0f));

        // Blue defensive rank immediately outside the fortress.
        float[] blueX = { -5.15f, -3.85f, -2.55f, -1.25f, 0f, 1.25f, 2.55f, 3.85f, 5.15f };
        string[] blueHero = { "hero_spearman", "hero_archer", "hero_swordsman", "hero_spearman", "hero_swordsman", "hero_spearman", "hero_archer", "hero_swordsman", "hero_spearman" };
        string[] blueFallback = { "spearman", "archer", "swordsman", "spearman", "swordsman", "spearman", "archer", "swordsman", "spearman" };
        for (int i = 0; i < blueX.Length; i++)
        {
            float z = -.72f - (i % 2) * .24f;
            SpawnHeroUnit(blueHero[i], blueFallback[i], new Vector3(blueX[i], BoardY + .03f, z), .34f, (i - 4) * 1.5f);
        }

        // Contested middle: staggered skirmish groups rather than a sparse empty field.
        SpawnHeroUnit("hero_spearman", "spearman", new Vector3(-4.85f, BoardY + .03f, -3.05f), .29f, 12f);
        Spawn("royal_guard", new Vector3(-3.15f, BoardY + .03f, -3.65f), .29f, new Vector3(0f, -7f, 0f));
        SpawnHeroUnit("hero_archer", "archer", new Vector3(-1.45f, BoardY + .03f, -4.15f), .28f, -4f);
        Spawn("wizard", new Vector3(.25f, BoardY + .03f, -4.35f), .30f, new Vector3(0f, -9f, 0f));
        SpawnHeroUnit("hero_swordsman", "swordsman", new Vector3(1.90f, BoardY + .03f, -4.05f), .29f, 6f);
        SpawnHeroUnit("hero_spearman", "spearman", new Vector3(3.55f, BoardY + .03f, -3.55f), .29f, 11f);
        Spawn("knight", new Vector3(5.05f, BoardY + .03f, -4.35f), .27f, new Vector3(0f, 10f, 0f));

        // Enemy formation forms a readable red-side line before the far fortress.
        float[] redX = { -4.75f, -3.35f, -1.95f, -.65f, .65f, 1.95f, 3.35f, 4.75f };
        string[] redHero = { "hero_swordsman", "hero_archer", "hero_spearman", "hero_swordsman", "hero_spearman", "hero_archer", "hero_swordsman", "hero_spearman" };
        string[] redFallback = { "swordsman", "archer", "spearman", "swordsman", "spearman", "archer", "swordsman", "spearman" };
        for (int i = 0; i < redX.Length; i++)
        {
            float z = -8.75f - (i % 2) * .20f;
            SpawnHeroUnit(redHero[i], redFallback[i], new Vector3(redX[i], BoardY + .03f, z), .27f, 180f + (i - 4));
        }

        Spawn("catapult", new Vector3(6.65f, BoardY + .03f, -6.35f), .29f, new Vector3(0f, 18f, 0f));
        Spawn("ballista", new Vector3(-6.55f, BoardY + .03f, -7.30f), .25f, new Vector3(0f, 168f, 0f));

        // Terrain clusters make the board feel sculpted and authored instead of like a flat mat.
        (float x, float z, string asset, float scale, float yaw)[] terrain =
        {
            (-8.70f, -2.25f, "pine_tree", .64f, -10f), (-7.90f, -2.85f, "pine_tree", .54f, 13f),
            (-8.25f, -6.25f, "oak_tree", .58f, 17f), (-7.45f, -6.75f, "pine_tree", .48f, -7f),
            (8.65f, -2.10f, "pine_tree", .62f, 12f), (7.85f, -2.85f, "oak_tree", .52f, -16f),
            (8.35f, -6.15f, "pine_tree", .60f, -12f), (7.55f, -6.75f, "pine_tree", .47f, 20f),
            (-6.75f, 2.15f, "rock_cluster", .42f, 18f), (6.85f, 2.10f, "rock_cluster", .44f, -12f),
            (-6.40f, -4.80f, "rock_cluster", .34f, -8f), (6.15f, -4.65f, "rock_cluster", .36f, 15f),
            (-7.75f, -5.15f, "campfire", .34f, 0f), (7.45f, -5.35f, "ruin_wall", .38f, 20f)
        };
        foreach (var t in terrain)
            Spawn(t.asset, new Vector3(t.x, BoardY + .02f, t.z), t.scale, new Vector3(0f, t.yaw, 0f));
    }

    private void BuildPlayerEdge()
    {
        // Reserve tray is intentionally visible in-frame because physical reserves are part of the cheating mechanic.
        AddBox("ReserveTrayBase", new Vector3(-6.70f, .66f, 6.60f), new Vector3(5.35f, .16f, 2.05f), new Color(.085f, .036f, .018f));
        AddBox("ReserveTrayBack", new Vector3(-6.70f, .82f, 5.68f), new Vector3(5.40f, .32f, .14f), WoodLight);
        AddBox("ReserveTrayFront", new Vector3(-6.70f, .82f, 7.52f), new Vector3(5.40f, .32f, .14f), WoodLight);

        float[] reserveX = { -8.55f, -7.35f, -6.15f, -4.95f, 4.75f, 5.95f, 7.15f, 8.35f };
        string[] hero = { "hero_spearman", "hero_swordsman", "hero_archer", "hero_spearman", "hero_archer", "hero_swordsman", "hero_spearman", "hero_archer" };
        string[] fallback = { "spearman", "swordsman", "archer", "spearman", "archer", "swordsman", "spearman", "archer" };
        for (int i = 0; i < reserveX.Length; i++)
        {
            float z = i < 4 ? 6.48f + (i % 2) * .12f : 6.42f + (i % 2) * .12f;
            SpawnHeroUnit(hero[i], fallback[i], new Vector3(reserveX[i], .76f, z), .38f, 0f);
        }

        // Three large physical cards and a draw deck mirror the approved concept's player-hand silhouette.
        for (int i = 0; i < 3; i++)
        {
            float x = -1.84f + i * 1.84f;
            float angle = (i - 1) * 4.0f;
            Color face = i == 1 ? new Color(.66f, .50f, .30f) : Parchment;
            Color art = i == 0 ? BlueLight : (i == 1 ? new Color(.31f, .25f, .12f) : new Color(.24f, .15f, .30f));
            AddRotatedBox($"Card_{i}", new Vector3(x, .75f, 7.48f), new Vector3(1.50f, .065f, 2.08f), face, new Vector3(-7f, 0f, angle));
            AddRotatedBox($"CardArt_{i}", new Vector3(x, .80f, 7.18f), new Vector3(1.00f, .018f, .88f), art, new Vector3(-7f, 0f, angle));
            AddRotatedBox($"CardTitle_{i}", new Vector3(x, .805f, 7.93f), new Vector3(.96f, .014f, .12f), new Color(.095f, .070f, .045f), new Vector3(-7f, 0f, angle));
        }

        for (int i = 0; i < 8; i++)
            AddRotatedBox($"DeckCard_{i}", new Vector3(9.25f + i * .035f, .73f + i * .035f, 7.22f - i * .025f), new Vector3(1.58f, .055f, 2.08f), Blue, new Vector3(-4f, 0f, -8f));
        AddRotatedBox("DeckEmblem", new Vector3(9.45f, 1.02f, 6.95f), new Vector3(.74f, .018f, .74f), new Color(.58f, .38f, .10f), new Vector3(-4f, 0f, -8f));

        Spawn("cheat_stash", new Vector3(-9.50f, .74f, 7.18f), .35f, new Vector3(0f, 10f, 0f));
        Spawn("dice_cluster", new Vector3(-8.65f, .76f, 7.34f), .43f);
        Spawn("mana_crystals", new Vector3(7.95f, .76f, 7.62f), .41f, new Vector3(0f, 12f, 0f));
        Spawn("suspicion_dial", new Vector3(6.92f, .76f, 7.68f), .36f, new Vector3(0f, -8f, 0f));
    }

    private void BuildLighting()
    {
        var fill = new DirectionalLight3D
        {
            Name = "CoolAmbientFill",
            RotationDegrees = new Vector3(-56f, -22f, 0f),
            LightColor = new Color(.46f, .51f, .60f),
            LightEnergy = .25f,
            ShadowEnabled = true
        };
        AddChild(fill);

        AddOmni("OpponentWarmKey", new Vector3(3.5f, 6.7f, -13.10f), new Color(1f, .50f, .22f), 3.25f, 11.5f, true);
        AddOmni("OpponentFaceFill", new Vector3(-3.0f, 5.6f, -12.40f), new Color(.49f, .58f, .72f), .82f, 9.0f, false);
        AddOmni("BoardCenterWarm", new Vector3(-1.1f, 5.2f, -4.3f), new Color(1f, .66f, .35f), 2.25f, 12.8f, true);
        AddOmni("BoardCoolLift", new Vector3(5.2f, 5.6f, -2.6f), new Color(.40f, .49f, .63f), .66f, 12.0f, false);
        AddOmni("PlayerCastleTorchL", new Vector3(-5.1f, 3.15f, 1.2f), new Color(1f, .36f, .10f), 1.65f, 5.8f, true);
        AddOmni("PlayerCastleTorchR", new Vector3(5.1f, 3.15f, 1.2f), new Color(1f, .36f, .10f), 1.65f, 5.8f, true);
        AddOmni("EnemyCastleWarm", new Vector3(0f, 3.8f, -10.9f), new Color(1f, .44f, .15f), 1.35f, 6.5f, true);
        AddOmni("LeftTavernLantern", new Vector3(-10.5f, 6.8f, -9.6f), new Color(1f, .43f, .16f), 1.85f, 8.8f, true);
        AddOmni("RightTavernLantern", new Vector3(10.2f, 7.0f, -9.9f), new Color(1f, .47f, .18f), 1.82f, 8.8f, true);
        AddOmni("NearTableCandle", new Vector3(-10.0f, 2.0f, 6.0f), new Color(1f, .45f, .16f), 1.35f, 5.2f, true);
    }

    private void BuildCamera()
    {
        // Slightly higher/back than the previous pass: foreground cards/reserves stay visible without shrinking the board.
        var camera = new Camera3D
        {
            Name = "PlayerCamera",
            Position = new Vector3(0f, 8.55f, 15.10f),
            Fov = 49.0f,
            Near = 0.08f,
            Far = 120f,
            Current = true
        };
        AddChild(camera);
        camera.LookAt(new Vector3(0f, 1.42f, -4.72f), Vector3.Up);
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