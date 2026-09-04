using Godot;

public partial class GameBuilder : Node3D
{
    private static readonly Color Wood = new(0.14f, 0.058f, 0.026f);
    private static readonly Color WoodLight = new(0.26f, 0.115f, 0.048f);
    private static readonly Color Parchment = new(0.58f, 0.43f, 0.25f);
    private static readonly Color ParchmentLight = new(0.72f, 0.58f, 0.35f);
    private static readonly Color Blue = new(0.040f, 0.095f, 0.28f);
    private static readonly Color Red = new(0.31f, 0.040f, 0.028f);
    private static readonly Color Gold = new(0.46f, 0.26f, 0.07f);
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
            BackgroundColor = new Color(0.008f, 0.006f, 0.005f),
            AmbientLightSource = Environment.AmbientSource.Color,
            AmbientLightColor = new Color(0.22f, 0.235f, 0.27f),
            AmbientLightEnergy = 0.52f
        };

        environment.Set("tonemap_mode", 4);
        environment.Set("tonemap_exposure", 1.08f);
        environment.Set("tonemap_agx_contrast", 1.20f);
        environment.Set("ssao_enabled", true);
        environment.Set("ssao_radius", 1.55f);
        environment.Set("ssao_intensity", 2.75f);
        environment.Set("ssao_power", 1.48f);
        environment.Set("ssao_detail", 0.84f);
        environment.Set("ssil_enabled", true);
        environment.Set("ssil_radius", 3.2f);
        environment.Set("ssil_intensity", 0.48f);
        environment.Set("glow_enabled", true);
        environment.Set("glow_intensity", 0.13f);
        environment.Set("glow_bloom", 0.035f);
        environment.Set("fog_enabled", true);
        environment.Set("fog_density", 0.0018f);
        environment.Set("fog_light_color", new Color(0.15f, 0.115f, 0.095f));
        environment.Set("fog_light_energy", 0.27f);

        AddChild(new WorldEnvironment
        {
            Name = "WorldEnvironment",
            Environment = environment
        });
    }

    private void BuildTavern()
    {
        Spawn("hero_tavern", new Vector3(0f, -3.05f, -1.15f), 1.0f, new Vector3(0f, 180f, 0f));
    }

    private void BuildWarTable()
    {
        if (AssetLibrary.Exists("hero_table"))
        {
            Spawn("hero_table", new Vector3(0f, -0.34f, -3.05f), 1.0f);
            return;
        }

        AddBox("WarTableBody", new Vector3(0f, -0.34f, -3.05f), new Vector3(30.4f, 1.0f, 27.2f), Wood);
        AddBox("BoardWell", new Vector3(0f, 0.48f, BoardCenterZ), new Vector3(23.4f, .18f, 18.8f), Felt);
        AddBox("NearRail", new Vector3(0f, 0.68f, 4.10f), new Vector3(23.7f, .30f, .40f), WoodLight);
        AddBox("FarRail", new Vector3(0f, 0.68f, -14.40f), new Vector3(23.7f, .30f, .40f), WoodLight);
    }

    private void BuildBattlefield()
    {
        Spawn("hero_battlefield", new Vector3(0f, BoardY, BoardCenterZ), 1.0f);

        Spawn("hero_castle", new Vector3(0f, BoardY + .01f, 2.45f), .42f);
        Spawn("hero_castle", new Vector3(0f, BoardY + .01f, -11.68f), .29f, new Vector3(0f, 180f, 0f));
        Spawn("hero_opponent", new Vector3(0f, -1.78f, -15.20f), 1.10f);

        Spawn("throne", new Vector3(0f, BoardY + .02f, 2.12f), .16f, new Vector3(0f, 180f, 0f));
        Spawn("king", new Vector3(0f, BoardY + .03f, 2.28f), .19f, new Vector3(0f, 180f, 0f));
        Spawn("throne", new Vector3(0f, BoardY + .02f, -11.34f), .12f);
        Spawn("king", new Vector3(0f, BoardY + .03f, -11.20f), .15f);

        SpawnHeroUnit("hero_spearman", "spearman", new Vector3(-3.65f, BoardY + .03f, .30f), .34f, 2f);
        SpawnHeroUnit("hero_swordsman", "swordsman", new Vector3(-1.15f, BoardY + .03f, -.42f), .34f, -4f);
        SpawnHeroUnit("hero_archer", "archer", new Vector3(1.65f, BoardY + .03f, -.12f), .32f, 7f);
        Spawn("knight", new Vector3(4.05f, BoardY + .03f, .50f), .28f, new Vector3(0f, -5f, 0f));

        SpawnHeroUnit("hero_spearman", "spearman", new Vector3(-2.50f, BoardY + .03f, -3.55f), .29f, 12f);
        Spawn("royal_guard", new Vector3(.15f, BoardY + .03f, -4.20f), .27f, new Vector3(0f, -7f, 0f));
        Spawn("wizard", new Vector3(2.85f, BoardY + .03f, -4.85f), .27f, new Vector3(0f, -12f, 0f));

        SpawnHeroUnit("hero_swordsman", "swordsman", new Vector3(-3.10f, BoardY + .03f, -7.35f), .27f, 178f);
        SpawnHeroUnit("hero_archer", "archer", new Vector3(-.35f, BoardY + .03f, -8.05f), .26f, 180f);
        Spawn("royal_guard", new Vector3(2.35f, BoardY + .03f, -7.55f), .26f, new Vector3(0f, 173f, 0f));
        Spawn("assassin", new Vector3(4.35f, BoardY + .03f, -8.55f), .24f, new Vector3(0f, 168f, 0f));

        Spawn("trebuchet", new Vector3(-7.15f, BoardY + .03f, -2.10f), .24f, new Vector3(0f, -14f, 0f));
        Spawn("catapult", new Vector3(6.95f, BoardY + .03f, -6.10f), .23f, new Vector3(0f, 18f, 0f));
    }

    private void BuildPlayerEdge()
    {
        Spawn("hero_reserve_rack", new Vector3(-8.35f, .69f, 9.55f), .76f, new Vector3(0f, 0f, 0f));

        float[] reserveX = { -10.15f, -8.95f, -7.75f, -6.55f };
        string[] reserveHero = { "hero_spearman", "hero_swordsman", "hero_archer", "hero_spearman" };
        string[] reserveFallback = { "spearman", "swordsman", "archer", "spearman" };
        for (int i = 0; i < reserveX.Length; i++)
            SpawnHeroUnit(reserveHero[i], reserveFallback[i], new Vector3(reserveX[i], .78f, 9.48f), .38f, 0f);

        AddCard("Card_0", new Vector3(-2.35f, .77f, 9.94f), new Vector3(-7f, 0f, -5f), Red);
        AddCard("Card_1", new Vector3(-.62f, .78f, 10.06f), new Vector3(-7f, 0f, -1f), Blue);
        AddCard("Card_2", new Vector3(1.15f, .77f, 9.98f), new Vector3(-7f, 0f, 5f), new Color(.23f, .30f, .16f));

        Spawn("hero_card_deck", new Vector3(9.80f, .72f, 9.72f), .82f, new Vector3(0f, -8f, 0f));
        Spawn("mana_crystals", new Vector3(7.55f, .73f, 9.78f), .43f, new Vector3(0f, 10f, 0f));
        Spawn("suspicion_dial", new Vector3(11.55f, .73f, 9.82f), .37f, new Vector3(0f, -7f, 0f));
        Spawn("cheat_stash", new Vector3(-11.65f, .68f, 10.12f), .28f, new Vector3(0f, 14f, 0f));
    }

    private void BuildLighting()
    {
        var coolFill = new DirectionalLight3D
        {
            Name = "CoolShapeFill",
            RotationDegrees = new Vector3(-58f, -26f, 0f),
            LightColor = new Color(.48f, .55f, .68f),
            LightEnergy = .36f,
            ShadowEnabled = true
        };
        AddChild(coolFill);

        AddOmni("OpponentKey", new Vector3(4.8f, 7.9f, -12.3f), new Color(1f, .54f, .28f), 2.00f, 10.0f, true);
        AddOmni("OpponentFill", new Vector3(-4.9f, 6.6f, -13.1f), new Color(.34f, .46f, .66f), .92f, 9.5f, false);
        AddOmni("BoardKey", new Vector3(2.8f, 7.4f, -3.8f), new Color(1f, .66f, .40f), 1.42f, 15.5f, false);
        AddOmni("BoardFill", new Vector3(-4.8f, 6.8f, -3.4f), new Color(.38f, .50f, .69f), .72f, 14.5f, false);
        AddOmni("RightLantern", new Vector3(9.8f, 8.8f, -11.6f), new Color(1f, .43f, .18f), 1.55f, 10.0f, true);
        AddOmni("LeftLantern", new Vector3(-8.9f, 8.2f, -10.6f), new Color(1f, .48f, .22f), 1.12f, 9.0f, false);
        AddOmni("NearCastleTorch", new Vector3(.9f, 3.1f, 2.1f), new Color(1f, .43f, .17f), .82f, 4.5f, false);
        AddOmni("FarCastleTorch", new Vector3(-.4f, 2.6f, -11.5f), new Color(1f, .43f, .17f), .62f, 3.8f, false);
    }

    private void BuildCamera()
    {
        var camera = new Camera3D
        {
            Name = "PlayerCamera",
            Position = new Vector3(0f, 7.20f, 20.15f),
            Fov = 49.5f,
            Near = 0.08f,
            Far = 120f,
            Current = true
        };
        AddChild(camera);
        camera.LookAt(new Vector3(0f, 1.35f, -5.35f), Vector3.Up);
    }

    private void BuildHud()
    {
        var layer = new CanvasLayer { Name = "HUD" };
        AddChild(layer);

        AddHudPanel(layer, new Vector2(24, 18), new Vector2(152, 30));
        AddHudPanel(layer, new Vector2(1102, 18), new Vector2(154, 30));
        AddHudPanel(layer, new Vector2(532, 18), new Vector2(216, 30));
        AddHudPanel(layer, new Vector2(1114, 665), new Vector2(142, 34));

        AddHudLabel(layer, "CASTLE 20 / 20", new Vector2(34, 23), 14, new Color(.80f, .87f, 1f));
        AddHudLabel(layer, "ENEMY 20 / 20", new Vector2(1112, 23), 14, new Color(1f, .78f, .69f));
        AddHudLabel(layer, "ROUND 1  •  YOUR TURN", new Vector2(548, 23), 13, new Color(.98f, .87f, .65f));
        AddHudLabel(layer, "MANA 5 / 5", new Vector2(1124, 670), 13, new Color(.62f, .78f, 1f));
        AddHudLabel(layer, "SUSPICION 0%", new Vector2(1124, 685), 10, new Color(.91f, .76f, .51f));
    }

    private void AddCard(string name, Vector3 position, Vector3 rotation, Color art)
    {
        AddRotatedBox(name, position, new Vector3(1.34f, .055f, 1.88f), Parchment, rotation);
        AddRotatedBox(name + "_Border", position + new Vector3(0f, .032f, -.02f), new Vector3(1.16f, .014f, 1.68f), ParchmentLight, rotation);
        AddRotatedBox(name + "_Art", position + new Vector3(0f, .044f, -.14f), new Vector3(.84f, .012f, .78f), art, rotation);
        AddRotatedBox(name + "_Pip", position + new Vector3(.40f, .050f, .55f), new Vector3(.20f, .010f, .20f), Gold, rotation);
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
            Color = new Color(.014f, .010f, .010f, .28f),
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