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
        BuildPlayerHand();
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
            AmbientLightColor = new Color(0.245f, 0.255f, 0.285f),
            AmbientLightEnergy = 0.58f
        };

        environment.Set("tonemap_mode", 4);
        environment.Set("tonemap_exposure", 1.15f);
        environment.Set("tonemap_agx_contrast", 1.16f);
        environment.Set("ssao_enabled", true);
        environment.Set("ssao_radius", 1.55f);
        environment.Set("ssao_intensity", 2.65f);
        environment.Set("ssao_power", 1.45f);
        environment.Set("ssao_detail", 0.82f);
        environment.Set("ssil_enabled", true);
        environment.Set("ssil_radius", 3.0f);
        environment.Set("ssil_intensity", 0.46f);
        environment.Set("glow_enabled", true);
        environment.Set("glow_intensity", 0.12f);
        environment.Set("glow_bloom", 0.035f);
        environment.Set("fog_enabled", true);
        environment.Set("fog_density", 0.0020f);
        environment.Set("fog_light_color", new Color(0.16f, 0.125f, 0.105f));
        environment.Set("fog_light_energy", 0.30f);

        AddChild(new WorldEnvironment
        {
            Name = "WorldEnvironment",
            Environment = environment
        });
    }

    private void BuildTavern()
    {
        // The room is a cinematic frame around a physical tabletop game. It should never compete
        // with the cards, miniatures, castles or the opponent.
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
        // The core fantasy is a card game that physically becomes a miniature battlefield. The
        // landscape is therefore the hero surface; it should read like an authored diorama rather
        // than an RTS map squeezed onto a table.
        Spawn("hero_battlefield", new Vector3(0f, BoardY, BoardCenterZ), 1.0f);

        // Castles anchor opposite ends but leave the middle open for cards becoming creatures,
        // reinforcements, spells and terrain changes.
        Spawn("hero_castle", new Vector3(0f, BoardY + .01f, 2.58f), .50f);
        Spawn("hero_castle", new Vector3(0f, BoardY + .01f, -11.72f), .31f, new Vector3(0f, 180f, 0f));

        // The opponent should feel like a real person seated across the same table, not a giant
        // board-piece. Scale is larger than the last pass, but the root is lowered so the hands sit
        // naturally near the far rail and the head remains in the cinematic pocket above the board.
        Spawn("hero_opponent", new Vector3(0f, -2.18f, -14.95f), 1.22f);

        Spawn("throne", new Vector3(0f, BoardY + .02f, 2.15f), .18f, new Vector3(0f, 180f, 0f));
        Spawn("king", new Vector3(0f, BoardY + .03f, 2.34f), .21f, new Vector3(0f, 180f, 0f));
        Spawn("throne", new Vector3(0f, BoardY + .02f, -11.40f), .13f);
        Spawn("king", new Vector3(0f, BoardY + .03f, -11.25f), .16f);

        // A tabletop-card-battler opening state: a few committed pieces with plenty of empty land
        // for the player to create the battle during play. This is intentionally not a pre-filled
        // war scene.
        SpawnHeroUnit("hero_spearman", "spearman", new Vector3(-3.45f, BoardY + .03f, .20f), .33f, 2f);
        SpawnHeroUnit("hero_swordsman", "swordsman", new Vector3(-.65f, BoardY + .03f, -.48f), .33f, -4f);
        SpawnHeroUnit("hero_archer", "archer", new Vector3(3.10f, BoardY + .03f, .15f), .31f, 8f);

        SpawnHeroUnit("hero_spearman", "spearman", new Vector3(-2.10f, BoardY + .03f, -4.05f), .28f, 13f);
        Spawn("wizard", new Vector3(2.55f, BoardY + .03f, -4.75f), .28f, new Vector3(0f, -10f, 0f));

        SpawnHeroUnit("hero_swordsman", "swordsman", new Vector3(-2.45f, BoardY + .03f, -7.85f), .27f, 178f);
        SpawnHeroUnit("hero_archer", "archer", new Vector3(2.10f, BoardY + .03f, -7.55f), .26f, 181f);

        // Siege is a special commitment and belongs on the flanks rather than filling every lane.
        Spawn("trebuchet", new Vector3(-7.20f, BoardY + .03f, -2.10f), .25f, new Vector3(0f, -14f, 0f));
    }

    private void BuildPlayerHand()
    {
        // Cards are physical objects at the player's edge. Most of each card stays near the bottom
        // of the frame so the battlefield remains dominant; during interaction a selected card can
        // later lift toward the board and resolve into a creature/spell/terrain effect.
        for (int i = 0; i < 5; i++)
        {
            float x = -3.15f + i * 1.48f;
            float angle = (i - 2f) * 3.2f;
            Color face = i == 2 ? new Color(.21f, .28f, .18f) : Parchment;
            AddRotatedBox($"Card_{i}", new Vector3(x, .72f, 10.18f), new Vector3(1.18f, .060f, 1.72f), face, new Vector3(-8f, 0f, angle));
            AddRotatedBox($"CardArt_{i}", new Vector3(x, .765f, 9.96f), new Vector3(.76f, .018f, .61f), i == 2 ? Blue : Red, new Vector3(-8f, 0f, angle));
        }

        // Only a few diegetic tools remain visible. Avoid turning the near edge into a control desk.
        Spawn("mana_crystals", new Vector3(8.65f, .73f, 9.65f), .46f, new Vector3(0f, 10f, 0f));
        Spawn("spellbook_open", new Vector3(10.75f, .72f, 9.48f), .45f, new Vector3(0f, -9f, 0f));
        Spawn("suspicion_dial", new Vector3(12.30f, .73f, 9.72f), .38f, new Vector3(0f, -7f, 0f));
    }

    private void BuildLighting()
    {
        var key = new DirectionalLight3D
        {
            Name = "SoftCoolFill",
            RotationDegrees = new Vector3(-58f, -25f, 0f),
            LightColor = new Color(.52f, .58f, .70f),
            LightEnergy = .42f,
            ShadowEnabled = true
        };
        AddChild(key);

        // Warm/cool separation is the target-image look: warm face/table highlights, cool shape
        // definition in the shadows, and enough board light to keep small miniatures readable.
        AddOmni("OpponentWarmKey", new Vector3(4.5f, 7.6f, -12.2f), new Color(1f, .58f, .31f), 2.15f, 10.0f, true);
        AddOmni("OpponentCoolFill", new Vector3(-5.1f, 6.6f, -13.0f), new Color(.38f, .49f, .67f), 1.00f, 9.5f, false);
        AddOmni("BoardWarm", new Vector3(3.8f, 6.8f, -3.8f), new Color(1f, .62f, .36f), 1.35f, 15.0f, false);
        AddOmni("BoardCool", new Vector3(-4.5f, 6.5f, -3.2f), new Color(.39f, .50f, .68f), .78f, 14.5f, false);
        AddOmni("FarLantern", new Vector3(9.6f, 8.6f, -12.2f), new Color(1f, .46f, .20f), 1.65f, 10.5f, true);
        AddOmni("PlayerCastleWarm", new Vector3(1.1f, 3.0f, 2.0f), new Color(1f, .48f, .22f), .90f, 4.8f, false);
    }

    private void BuildCamera()
    {
        // Closer, lower and more intimate than the previous pass. The board should fill most of the
        // frame like a premium tabletop diorama, with just enough tavern visible to establish place.
        var camera = new Camera3D
        {
            Name = "PlayerCamera",
            Position = new Vector3(0f, 5.72f, 18.35f),
            Fov = 45.0f,
            Near = 0.08f,
            Far = 120f,
            Current = true
        };
        AddChild(camera);
        camera.LookAt(new Vector3(0f, 1.18f, -5.60f), Vector3.Up);
    }

    private void BuildHud()
    {
        var layer = new CanvasLayer { Name = "HUD" };
        AddChild(layer);

        // The physical game is the interface. HUD is intentionally quiet and leaves the center
        // untouched so cards, miniatures and the opponent carry the scene.
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
            Color = new Color(.014f, .010f, .010f, .30f),
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
