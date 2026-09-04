using Godot;

public partial class GameBuilder : Node3D
{
    private static readonly Color WoodDark = new(0.045f, 0.018f, 0.010f);
    private static readonly Color Wood = new(0.145f, 0.060f, 0.025f);
    private static readonly Color WoodLight = new(0.270f, 0.125f, 0.050f);
    private static readonly Color Iron = new(0.040f, 0.045f, 0.052f);
    private static readonly Color Brass = new(0.38f, 0.22f, 0.075f);
    private static readonly Color Parchment = new(0.56f, 0.42f, 0.24f);
    private static readonly Color Blue = new(0.045f, 0.105f, 0.30f);
    private static readonly Color Red = new(0.34f, 0.045f, 0.030f);
    private static readonly Color Felt = new(0.025f, 0.050f, 0.035f);

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
            BackgroundColor = new Color(0.010f, 0.007f, 0.006f),
            AmbientLightSource = Environment.AmbientSource.Color,
            AmbientLightColor = new Color(0.17f, 0.19f, 0.23f),
            AmbientLightEnergy = 0.44f
        };

        // Runtime Set() keeps this project tolerant of small Godot 4.x property-name changes.
        environment.Set("tonemap_mode", 4);
        environment.Set("tonemap_exposure", 1.08f);
        environment.Set("tonemap_agx_contrast", 1.22f);
        environment.Set("ssao_enabled", true);
        environment.Set("ssao_radius", 1.65f);
        environment.Set("ssao_intensity", 3.0f);
        environment.Set("ssao_power", 1.55f);
        environment.Set("ssao_detail", 0.82f);
        environment.Set("ssil_enabled", true);
        environment.Set("ssil_radius", 3.2f);
        environment.Set("ssil_intensity", 0.58f);
        environment.Set("glow_enabled", true);
        environment.Set("glow_intensity", 0.18f);
        environment.Set("glow_bloom", 0.05f);
        environment.Set("fog_enabled", true);
        environment.Set("fog_density", 0.0042f);
        environment.Set("fog_height", -1.0f);
        environment.Set("fog_light_color", new Color(0.14f, 0.105f, 0.085f));
        environment.Set("fog_light_energy", 0.48f);

        AddChild(new WorldEnvironment
        {
            Name = "WorldEnvironment",
            Environment = environment
        });
    }

    private void BuildTavern()
    {
        // The room is scenery, not the subject. Keep it close enough to frame the table while
        // leaving a clear visual pocket for the opponent's head and shoulders.
        Spawn("hero_tavern", new Vector3(0f, -3.15f, -1.2f), 1.0f, new Vector3(0f, 180f, 0f));

        // Deliberate asymmetry mirrors the reference: denser shadow on the left, warm practicals
        // on the right, and only a few large readable props instead of repeated clutter.
        Spawn("weapon_rack", new Vector3(-14.9f, -2.65f, -14.0f), 1.05f, new Vector3(0f, 18f, 0f));
        Spawn("shelf", new Vector3(13.6f, -2.70f, -15.2f), 1.18f, new Vector3(0f, 180f, 0f));
        Spawn("barrel", new Vector3(-13.8f, -2.65f, -10.8f), 1.00f);
        Spawn("crate", new Vector3(-12.7f, -2.65f, -11.35f), 0.88f, new Vector3(0f, 12f, 0f));
        Spawn("brazier", new Vector3(13.55f, -2.55f, -10.7f), 1.12f);
    }

    private void BuildWarTable()
    {
        // Prefer the authored hero table. A restrained fallback is retained for first-run cases
        // before Blender-generated assets exist.
        if (AssetLibrary.Exists("hero_table"))
        {
            Spawn("hero_table", new Vector3(0f, -0.32f, -3.10f), 1.0f);
            return;
        }

        AddBox("WarTableBody", new Vector3(0f, -0.32f, -3.10f), new Vector3(30.2f, 1.0f, 27.0f), Wood, .12f);
        AddBox("BoardWell", new Vector3(0f, 0.48f, BoardCenterZ), new Vector3(23.1f, .18f, 18.5f), Felt, .08f);
        AddBox("NearRail", new Vector3(0f, 0.67f, 4.05f), new Vector3(23.2f, .28f, .38f), WoodLight, .04f);
        AddBox("FarRail", new Vector3(0f, 0.67f, -14.35f), new Vector3(23.2f, .28f, .38f), WoodLight, .04f);
        AddBox("LeftRail", new Vector3(-11.42f, 0.67f, BoardCenterZ), new Vector3(.38f, .28f, 18.8f), WoodLight, .04f);
        AddBox("RightRail", new Vector3(11.42f, 0.67f, BoardCenterZ), new Vector3(.38f, .28f, 18.8f), WoodLight, .04f);
    }

    private void BuildBattlefield()
    {
        Spawn("hero_battlefield", new Vector3(0f, BoardY, BoardCenterZ), 1.0f);

        // Reference composition: the near castle anchors the bottom edge instead of blocking the
        // middle of the board. The far castle is intentionally smaller so perspective can breathe.
        Spawn("hero_castle", new Vector3(0f, BoardY + .01f, 2.85f), .49f);
        Spawn("hero_castle", new Vector3(0f, BoardY + .01f, -12.55f), .43f, new Vector3(0f, 180f, 0f));

        // The opponent is a hero focal point and must remain visible above the far castle.
        Spawn("hero_opponent", new Vector3(0f, 0.62f, -15.70f), 1.13f);

        // Kings are the real objective. Position them inside the castle mouths where they can be
        // glimpsed during play without reading as loose miniatures in front of the walls.
        Spawn("throne", new Vector3(0f, BoardY + .02f, 2.35f), .20f, new Vector3(0f, 180f, 0f));
        Spawn("king", new Vector3(0f, BoardY + .03f, 2.55f), .24f, new Vector3(0f, 180f, 0f));
        Spawn("throne", new Vector3(0f, BoardY + .02f, -12.02f), .18f);
        Spawn("king", new Vector3(0f, BoardY + .03f, -11.82f), .22f);

        // Player line: collectible-miniature silhouettes in a shallow defensive arc.
        SpawnHeroUnit("hero_spearman", "spearman", new Vector3(-3.7f, BoardY + .03f, 0.55f), .42f, 0f);
        SpawnHeroUnit("hero_swordsman", "swordsman", new Vector3(-1.55f, BoardY + .03f, 0.08f), .42f, -5f);
        Spawn("knight", new Vector3(.85f, BoardY + .03f, -.25f), .35f, new Vector3(0f, -4f, 0f));
        SpawnHeroUnit("hero_archer", "archer", new Vector3(3.0f, BoardY + .03f, .58f), .40f, 8f);
        Spawn("wizard", new Vector3(4.75f, BoardY + .03f, -.35f), .37f, new Vector3(0f, -10f, 0f));

        // Midfield skirmish groups. They are deliberately staggered so the table reads like an
        // active battle rather than two neat rows of chess pieces.
        SpawnHeroUnit("hero_spearman", "spearman", new Vector3(-2.65f, BoardY + .03f, -3.55f), .34f, 14f);
        SpawnHeroUnit("hero_swordsman", "swordsman", new Vector3(-.72f, BoardY + .03f, -4.30f), .34f, 3f);
        Spawn("royal_guard", new Vector3(1.05f, BoardY + .03f, -3.78f), .34f, new Vector3(0f, -8f, 0f));
        Spawn("assassin", new Vector3(3.28f, BoardY + .03f, -4.85f), .32f, new Vector3(0f, -16f, 0f));

        SpawnHeroUnit("hero_spearman", "spearman", new Vector3(2.85f, BoardY + .03f, -7.35f), .33f, 185f);
        SpawnHeroUnit("hero_archer", "archer", new Vector3(.78f, BoardY + .03f, -8.10f), .32f, 180f);
        SpawnHeroUnit("hero_swordsman", "swordsman", new Vector3(-1.0f, BoardY + .03f, -7.52f), .33f, 176f);
        Spawn("knight", new Vector3(-3.10f, BoardY + .03f, -8.55f), .30f, new Vector3(0f, 180f, 0f));
        Spawn("royal_guard", new Vector3(-4.72f, BoardY + .03f, -7.10f), .31f, new Vector3(0f, 170f, 0f));

        // Siege engines live on the flanks so they do not hide the central route.
        Spawn("trebuchet", new Vector3(-7.6f, BoardY + .03f, -1.65f), .31f, new Vector3(0f, -15f, 0f));
        Spawn("catapult", new Vector3(7.10f, BoardY + .03f, -4.15f), .31f, new Vector3(0f, 18f, 0f));
        Spawn("ballista", new Vector3(-6.95f, BoardY + .03f, -9.12f), .29f, new Vector3(0f, 190f, 0f));

        // A few gameplay-state props communicate the design outline without filling the screen.
        Spawn("trap_spikes", new Vector3(-3.80f, BoardY + .02f, 1.62f), .21f, new Vector3(0f, 12f, 0f));
        Spawn("reinforcement_outpost", new Vector3(-8.35f, BoardY + .02f, 1.20f), .25f, new Vector3(0f, 18f, 0f));
        Spawn("fireball_scorch", new Vector3(3.55f, BoardY + .01f, -5.95f), .34f, new Vector3(0f, 20f, 0f));
        Spawn("healing_rune", new Vector3(-3.02f, BoardY + .01f, -5.35f), .34f, new Vector3(0f, -8f, 0f));
    }

    private void BuildPlayerEdge()
    {
        // Keep the gameplay hand out of the battlefield silhouette. The cards now sit low and
        // shallow along the near rail like real tabletop components.
        for (int i = 0; i < 4; i++)
        {
            float x = -4.5f + i * 1.62f;
            float angle = (i - 1.5f) * 2.2f;
            Color face = i == 2 ? new Color(.20f, .27f, .18f) : Parchment;
            AddRotatedBox($"Card_{i}", new Vector3(x, .78f, 8.55f), new Vector3(1.34f, .075f, 1.88f), face, new Vector3(-4f, 0f, angle), .035f);
            AddRotatedBox($"CardArt_{i}", new Vector3(x, .83f, 8.32f), new Vector3(.88f, .020f, .72f), i == 2 ? Blue : Red, new Vector3(-4f, 0f, angle), .012f);
        }

        Spawn("reinforcement_cart", new Vector3(-9.50f, .74f, 8.10f), .46f, new Vector3(0f, 15f, 0f));
        SpawnHeroUnit("hero_spearman", "spearman", new Vector3(-11.05f, .76f, 8.20f), .48f, 0f);
        SpawnHeroUnit("hero_archer", "archer", new Vector3(-7.95f, .76f, 8.22f), .46f, 0f);

        Spawn("spellbook_open", new Vector3(9.60f, .73f, 8.18f), .62f, new Vector3(0f, -10f, 0f));
        Spawn("mana_crystals", new Vector3(7.55f, .74f, 8.62f), .62f, new Vector3(0f, 12f, 0f));
        Spawn("suspicion_dial", new Vector3(11.82f, .74f, 8.35f), .56f, new Vector3(0f, -8f, 0f));
        Spawn("karma_medallion", new Vector3(6.22f, .75f, 8.76f), .48f);
        Spawn("dice_cluster", new Vector3(5.00f, .74f, 8.82f), .50f, new Vector3(0f, 18f, 0f));
        Spawn("mug", new Vector3(13.40f, .74f, 8.60f), .72f, new Vector3(0f, -12f, 0f));
    }

    private void BuildLighting()
    {
        // Cool, low-energy ambient key defines shapes. Warm practicals carry the mood.
        var key = new DirectionalLight3D
        {
            Name = "MoonFill",
            RotationDegrees = new Vector3(-58f, -24f, 0f),
            LightColor = new Color(.42f, .50f, .66f),
            LightEnergy = .34f,
            ShadowEnabled = true
        };
        AddChild(key);

        AddOmni("OpponentKey", new Vector3(-1.4f, 8.8f, -13.0f), new Color(1f, .48f, .22f), 2.65f, 9.5f, true);
        AddOmni("RightLantern", new Vector3(9.8f, 8.0f, -10.2f), new Color(1f, .39f, .13f), 2.15f, 10.0f, true);
        AddOmni("LeftBounce", new Vector3(-8.8f, 5.2f, -3.0f), new Color(.73f, .30f, .13f), 1.25f, 10.5f, false);
        AddOmni("BoardWarm", new Vector3(3.5f, 6.4f, -5.0f), new Color(1f, .47f, .20f), 1.18f, 14.0f, false);
        AddOmni("BoardCool", new Vector3(-4.0f, 7.8f, -4.0f), new Color(.29f, .42f, .62f), .72f, 15.0f, false);
        AddOmni("PlayerCastleTorch", new Vector3(0f, 2.5f, 2.1f), new Color(1f, .24f, .06f), 1.40f, 4.5f, false);
        AddOmni("EnemyCastleTorch", new Vector3(0f, 2.35f, -11.95f), new Color(1f, .24f, .06f), 1.15f, 4.2f, false);
    }

    private void BuildCamera()
    {
        var camera = new Camera3D
        {
            Name = "PlayerCamera",
            Position = new Vector3(0f, 8.15f, 19.2f),
            Fov = 50.5f,
            Near = 0.08f,
            Far = 120f,
            Current = true
        };
        AddChild(camera);
        camera.LookAt(new Vector3(0f, 2.00f, -5.85f), Vector3.Up);
    }

    private void BuildHud()
    {
        var layer = new CanvasLayer { Name = "HUD" };
        AddChild(layer);

        // Small information plates preserve the game state without competing with the diorama.
        AddHudPanel(layer, new Vector2(24, 18), new Vector2(176, 38));
        AddHudPanel(layer, new Vector2(1080, 18), new Vector2(176, 38));
        AddHudPanel(layer, new Vector2(516, 18), new Vector2(248, 36));
        AddHudPanel(layer, new Vector2(1092, 650), new Vector2(164, 48));

        AddHudLabel(layer, "CASTLE 20 / 20", new Vector2(36, 27), 16, new Color(.74f, .84f, 1f));
        AddHudLabel(layer, "ENEMY 20 / 20", new Vector2(1091, 27), 16, new Color(1f, .72f, .64f));
        AddHudLabel(layer, "ROUND 1  •  YOUR TURN", new Vector2(535, 27), 15, new Color(.96f, .84f, .60f));
        AddHudLabel(layer, "MANA 5 / 5", new Vector2(1106, 656), 15, new Color(.56f, .73f, 1f));
        AddHudLabel(layer, "SUSPICION 0%", new Vector2(1106, 677), 12, new Color(.88f, .72f, .47f));
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

    private void AddBox(string name, Vector3 position, Vector3 size, Color color, float bevel = 0f)
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

    private void AddRotatedBox(string name, Vector3 position, Vector3 size, Color color, Vector3 rotationDegrees, float bevel = 0f)
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
            Roughness = .90f
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
            Color = new Color(.014f, .010f, .010f, .64f),
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
