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
            BackgroundColor = new Color(0.010f, 0.007f, 0.006f),
            AmbientLightSource = Environment.AmbientSource.Color,
            AmbientLightColor = new Color(0.22f, 0.20f, 0.20f),
            AmbientLightEnergy = 0.62f
        };
        environment.Set("tonemap_mode", 4);
        environment.Set("tonemap_exposure", 1.38f);
        environment.Set("tonemap_agx_contrast", 1.16f);
        environment.Set("ssao_enabled", true);
        environment.Set("ssao_radius", 1.55f);
        environment.Set("ssao_intensity", 2.05f);
        environment.Set("ssao_power", 1.32f);
        environment.Set("ssao_detail", 0.82f);
        environment.Set("ssil_enabled", true);
        environment.Set("ssil_radius", 2.6f);
        environment.Set("ssil_intensity", 0.46f);
        environment.Set("glow_enabled", true);
        environment.Set("glow_intensity", 0.15f);
        environment.Set("glow_bloom", 0.045f);
        environment.Set("fog_enabled", true);
        environment.Set("fog_density", 0.0021f);
        environment.Set("fog_light_color", new Color(0.18f, 0.115f, 0.075f));
        environment.Set("fog_light_energy", 0.34f);
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

    private void BuildBattlefield()
    {
        Spawn("hero_battlefield", new Vector3(0f, BoardY, BoardCenterZ), 1.0f);
        string playerCastle = AssetLibrary.Exists("hero_castle_blue") ? "hero_castle_blue" : "hero_castle";
        string enemyCastle = AssetLibrary.Exists("hero_castle_red") ? "hero_castle_red" : "hero_castle";

        Spawn(playerCastle, new Vector3(0f, BoardY + .01f, 2.15f), .58f);
        Spawn(enemyCastle, new Vector3(0f, BoardY + .01f, -11.55f), .31f, new Vector3(0f, 180f, 0f));

        // The Blender quality pass now bakes the character's forward orientation. Do not turn him around again here.
        Spawn("hero_opponent", new Vector3(0f, -1.05f, -14.80f), 1.22f);

        Spawn("throne", new Vector3(0f, BoardY + .02f, 2.00f), .17f, new Vector3(0f, 180f, 0f));
        Spawn("king", new Vector3(0f, BoardY + .03f, 2.12f), .20f, new Vector3(0f, 180f, 0f));
        Spawn("throne", new Vector3(0f, BoardY + .02f, -11.30f), .13f);
        Spawn("king", new Vector3(0f, BoardY + .03f, -11.18f), .16f);

        SpawnHeroUnit("hero_spearman", "spearman", new Vector3(-4.20f, BoardY + .03f, 0.35f), .35f, 0f);
        SpawnHeroUnit("hero_swordsman", "swordsman", new Vector3(-2.15f, BoardY + .03f, -.10f), .35f, -5f);
        Spawn("knight", new Vector3(0f, BoardY + .03f, -.34f), .30f, new Vector3(0f, 0f, 0f));
        SpawnHeroUnit("hero_archer", "archer", new Vector3(2.18f, BoardY + .03f, -.05f), .34f, 7f);
        SpawnHeroUnit("hero_spearman", "spearman", new Vector3(4.15f, BoardY + .03f, .38f), .34f, 0f);

        SpawnHeroUnit("hero_spearman", "spearman", new Vector3(-3.20f, BoardY + .03f, -3.35f), .29f, 12f);
        Spawn("royal_guard", new Vector3(-.70f, BoardY + .03f, -4.05f), .28f, new Vector3(0f, -8f, 0f));
        Spawn("wizard", new Vector3(2.55f, BoardY + .03f, -4.55f), .29f, new Vector3(0f, -12f, 0f));
        SpawnHeroUnit("hero_swordsman", "swordsman", new Vector3(-2.85f, BoardY + .03f, -7.55f), .28f, 178f);
        SpawnHeroUnit("hero_archer", "archer", new Vector3(.15f, BoardY + .03f, -7.90f), .27f, 180f);
        Spawn("royal_guard", new Vector3(3.05f, BoardY + .03f, -7.15f), .27f, new Vector3(0f, 171f, 0f));
        Spawn("trebuchet", new Vector3(-7.15f, BoardY + .03f, -1.65f), .27f, new Vector3(0f, -14f, 0f));
        Spawn("catapult", new Vector3(7.05f, BoardY + .03f, -6.00f), .27f, new Vector3(0f, 18f, 0f));
    }

    private void BuildPlayerEdge()
    {
        float[] reserveX = { -8.8f, -7.35f, -5.90f, 5.90f, 7.35f, 8.80f };
        string[] hero = { "hero_spearman", "hero_swordsman", "hero_archer", "hero_archer", "hero_swordsman", "hero_spearman" };
        string[] fallback = { "spearman", "swordsman", "archer", "archer", "swordsman", "spearman" };
        for (int i = 0; i < reserveX.Length; i++)
            SpawnHeroUnit(hero[i], fallback[i], new Vector3(reserveX[i], .76f, 8.12f + (i % 2) * .10f), .38f, 0f);

        for (int i = 0; i < 4; i++)
        {
            float x = -2.58f + i * 1.72f;
            float angle = (i - 1.5f) * 3.2f;
            Color face = i == 1 ? new Color(.20f, .27f, .18f) : Parchment;
            AddRotatedBox($"Card_{i}", new Vector3(x, .75f, 8.86f), new Vector3(1.32f, .060f, 1.82f), face, new Vector3(-7f, 0f, angle));
            AddRotatedBox($"CardArt_{i}", new Vector3(x, .79f, 8.62f), new Vector3(.88f, .018f, .72f), i == 1 ? Blue : Red, new Vector3(-7f, 0f, angle));
        }

        Spawn("cheat_stash", new Vector3(-10.45f, .72f, 8.65f), .30f, new Vector3(0f, 12f, 0f));
        Spawn("spellbook_open", new Vector3(10.10f, .73f, 8.48f), .46f, new Vector3(0f, -10f, 0f));
        Spawn("mana_crystals", new Vector3(9.20f, .74f, 9.20f), .43f, new Vector3(0f, 12f, 0f));
        Spawn("suspicion_dial", new Vector3(11.20f, .74f, 9.05f), .38f, new Vector3(0f, -8f, 0f));
    }

    private void BuildLighting()
    {
        var fill = new DirectionalLight3D
        {
            Name = "CoolAmbientFill",
            RotationDegrees = new Vector3(-58f, -24f, 0f),
            LightColor = new Color(.46f, .50f, .58f),
            LightEnergy = .26f,
            ShadowEnabled = true
        };
        AddChild(fill);

        AddOmni("OpponentWarmKey", new Vector3(3.8f, 7.5f, -13.0f), new Color(1f, .53f, .25f), 2.35f, 10.5f, true);
        AddOmni("OpponentFaceFill", new Vector3(-3.5f, 6.0f, -12.5f), new Color(.50f, .57f, .68f), .72f, 8.5f, false);
        AddOmni("BoardCenterWarm", new Vector3(-1.5f, 5.6f, -4.6f), new Color(1f, .67f, .39f), 1.65f, 12.5f, true);
        AddOmni("BoardCoolLift", new Vector3(5.2f, 6.1f, -2.8f), new Color(.42f, .50f, .61f), .62f, 12.0f, false);
        AddOmni("PlayerCastleTorchL", new Vector3(-4.4f, 2.8f, 2.1f), new Color(1f, .40f, .15f), 1.10f, 5.0f, true);
        AddOmni("PlayerCastleTorchR", new Vector3(4.4f, 2.8f, 2.1f), new Color(1f, .40f, .15f), 1.10f, 5.0f, true);
        AddOmni("LeftTavernLantern", new Vector3(-10.8f, 7.2f, -8.0f), new Color(1f, .43f, .18f), 1.25f, 7.5f, true);
        AddOmni("RightTavernLantern", new Vector3(10.2f, 7.4f, -10.0f), new Color(1f, .48f, .20f), 1.45f, 8.5f, true);
    }

    private void BuildCamera()
    {
        // Reference #1 balance: enough height to see the physical hand/reserves, while keeping the board dominant.
        var camera = new Camera3D
        {
            Name = "PlayerCamera",
            Position = new Vector3(0f, 8.25f, 16.10f),
            Fov = 52.0f,
            Near = 0.08f,
            Far = 120f,
            Current = true
        };
        AddChild(camera);
        camera.LookAt(new Vector3(0f, 1.48f, -5.15f), Vector3.Up);
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
        var mesh = new MeshInstance3D { Name = name, Position = position, Mesh = new BoxMesh { Size = size }, MaterialOverride = MakeMaterial(color) };
        AddChild(mesh);
    }

    private void AddRotatedBox(string name, Vector3 position, Vector3 size, Color color, Vector3 rotationDegrees)
    {
        var mesh = new MeshInstance3D { Name = name, Position = position, RotationDegrees = rotationDegrees, Mesh = new BoxMesh { Size = size }, MaterialOverride = MakeMaterial(color) };
        AddChild(mesh);
    }

    private StandardMaterial3D MakeMaterial(Color color) => new() { AlbedoColor = color, Roughness = .88f };

    private void AddOmni(string name, Vector3 position, Color color, float energy, float range, bool shadows)
    {
        var light = new OmniLight3D { Name = name, Position = position, LightColor = color, LightEnergy = energy, OmniRange = range, ShadowEnabled = shadows };
        AddChild(light);
    }

    private void AddHudPanel(CanvasLayer layer, Vector2 position, Vector2 size)
    {
        var rect = new ColorRect { Position = position, Size = size, Color = new Color(.014f, .010f, .010f, .42f), MouseFilter = Control.MouseFilterEnum.Ignore };
        layer.AddChild(rect);
    }

    private void AddHudLabel(CanvasLayer layer, string text, Vector2 position, int fontSize, Color color)
    {
        var label = new Label { Text = text, Position = position, Modulate = color, MouseFilter = Control.MouseFilterEnum.Ignore };
        label.AddThemeFontSizeOverride("font_size", fontSize);
        layer.AddChild(label);
    }
}
