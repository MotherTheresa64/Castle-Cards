using Godot;

public partial class GameBuilder : Node3D
{
    private static readonly Color WoodDark = new(0.050f, 0.018f, 0.009f);
    private static readonly Color Wood = new(0.145f, 0.055f, 0.018f);
    private static readonly Color WoodLight = new(0.265f, 0.115f, 0.036f);
    private static readonly Color Iron = new(0.045f, 0.050f, 0.058f);
    private static readonly Color Brass = new(0.37f, 0.19f, 0.052f);
    private static readonly Color Parchment = new(0.56f, 0.39f, 0.20f);
    private static readonly Color Blue = new(0.035f, 0.095f, 0.30f);
    private static readonly Color Red = new(0.34f, 0.032f, 0.024f);
    private static readonly Color Felt = new(0.020f, 0.038f, 0.032f);

    public override void _Ready()
    {
        BuildEnvironment();
        BuildHeroRoom();
        BuildWarTable();
        BuildHeroBattlefield();
        BuildPlayerTabletop();
        BuildLighting();
        BuildCamera();
        BuildHud();
    }

    private void BuildEnvironment()
    {
        var environment = new Environment
        {
            BackgroundMode = Environment.BGMode.Color,
            BackgroundColor = new Color(0.005f, 0.006f, 0.009f),
            AmbientLightSource = Environment.AmbientSource.Color,
            AmbientLightColor = new Color(0.18f, 0.215f, 0.29f),
            AmbientLightEnergy = 0.66f
        };

        // Keep this dynamic so the project remains resilient to minor API naming changes.
        environment.Set("tonemap_mode", 4);
        environment.Set("tonemap_exposure", 1.0f);
        environment.Set("tonemap_agx_contrast", 1.32f);
        environment.Set("ssao_enabled", true);
        environment.Set("ssao_radius", 1.25f);
        environment.Set("ssao_intensity", 2.35f);
        environment.Set("ssao_power", 1.48f);
        environment.Set("ssao_detail", 0.72f);
        environment.Set("ssil_enabled", true);
        environment.Set("ssil_radius", 3.4f);
        environment.Set("ssil_intensity", 0.72f);
        environment.Set("glow_enabled", true);
        environment.Set("glow_intensity", 0.28f);
        environment.Set("glow_bloom", 0.08f);
        environment.Set("fog_enabled", true);
        environment.Set("fog_density", 0.0065f);
        environment.Set("fog_light_color", new Color(0.12f, 0.14f, 0.19f));
        environment.Set("fog_light_energy", 0.52f);

        AddChild(new WorldEnvironment
        {
            Name = "WorldEnvironment",
            Environment = environment
        });
    }

    private void BuildHeroRoom()
    {
        // The Blender room was authored facing the opposite axis from Godot's camera,
        // so turn it once here. This replaces the old box-wall tavern completely.
        Spawn("hero_tavern", new Vector3(0f, -3.20f, -2.0f), 1.0f, new Vector3(0f, 180f, 0f));

        // Additional deep-background silhouette pieces make the room feel occupied.
        Spawn("weapon_rack", new Vector3(-15.4f, -2.85f, -18.35f), 1.05f, new Vector3(0f, 0f, 0f));
        Spawn("weapon_rack", new Vector3(15.4f, -2.85f, -18.35f), 1.05f, new Vector3(0f, 0f, 0f));
        Spawn("brazier", new Vector3(-16.0f, -2.95f, -10.8f), 1.15f);
        Spawn("brazier", new Vector3(16.0f, -2.95f, -10.2f), 1.15f);
    }

    private void BuildWarTable()
    {
        // Layered construction instead of a single rectangular slab.
        AddBox("WarTableBody", new Vector3(0f, -0.32f, -3.1f), new Vector3(30.3f, 0.95f, 27.1f), WoodDark, .16f);
        AddBox("WarTableTop", new Vector3(0f, 0.19f, -3.1f), new Vector3(29.9f, 0.16f, 26.7f), Wood, .11f);

        AddBox("NearRail", new Vector3(0f, 0.39f, 10.15f), new Vector3(30.0f, .46f, .74f), WoodLight, .07f);
        AddBox("FarRail", new Vector3(0f, 0.39f, -16.35f), new Vector3(30.0f, .46f, .74f), WoodLight, .07f);
        AddBox("LeftRail", new Vector3(-14.62f, 0.39f, -3.1f), new Vector3(.74f, .46f, 25.8f), WoodLight, .07f);
        AddBox("RightRail", new Vector3(14.62f, 0.39f, -3.1f), new Vector3(.74f, .46f, 25.8f), WoodLight, .07f);

        // Battlefield recess frame.
        AddBox("BoardWell", new Vector3(0f, 0.48f, -5.0f), new Vector3(23.0f, .20f, 18.45f), Felt, .10f);
        AddBox("BoardFrameNear", new Vector3(0f, .66f, 4.12f), new Vector3(23.0f,.20f,.35f), WoodLight, .04f);
        AddBox("BoardFrameFar", new Vector3(0f, .66f, -14.12f), new Vector3(23.0f,.20f,.35f), WoodLight, .04f);
        AddBox("BoardFrameLeft", new Vector3(-11.32f,.66f,-5.0f), new Vector3(.35f,.20f,18.55f), WoodLight, .04f);
        AddBox("BoardFrameRight", new Vector3(11.32f,.66f,-5.0f), new Vector3(.35f,.20f,18.55f), WoodLight, .04f);

        // Iron corner plates and rivets give the table weight.
        Vector3[] corners =
        {
            new(-14.25f,.68f,9.88f), new(14.25f,.68f,9.88f),
            new(-14.25f,.68f,-16.10f), new(14.25f,.68f,-16.10f)
        };
        for (int i = 0; i < corners.Length; i++)
        {
            AddBox($"CornerPlate_{i}", corners[i], new Vector3(.82f,.10f,.82f), Iron, .045f);
            AddSphere($"CornerRivet_{i}", corners[i] + new Vector3(0f,.09f,0f), new Vector3(.10f,.055f,.10f), Brass);
        }

        for (int i = 0; i < 15; i++)
        {
            float x = -12.8f + i * 1.82f;
            AddSphere($"NearRivet_{i}", new Vector3(x,.69f,10.14f), new Vector3(.07f,.04f,.07f), Iron);
        }
    }

    private void BuildHeroBattlefield()
    {
        Spawn("hero_battlefield", new Vector3(0f, 0.73f, -5.0f), 1.0f);

        // Fully modeled hero castles replace the old modular cylinder-wall compositions.
        Spawn("hero_castle", new Vector3(0f, 0.74f, 1.05f), .72f);
        Spawn("hero_castle", new Vector3(0f, 0.74f, -11.45f), .75f, new Vector3(0f, 180f, 0f));

        // Kings make the real objective physically present.
        Spawn("throne", new Vector3(0f,.76f,.35f), .28f, new Vector3(0f,180f,0f));
        Spawn("king", new Vector3(0f,.77f,.60f), .36f, new Vector3(0f,180f,0f));
        Spawn("throne", new Vector3(0f,.76f,-10.78f), .28f);
        Spawn("king", new Vector3(0f,.77f,-10.48f), .36f);

        // More tabletop-scale troops than the prototype pass, with varied silhouettes.
        Spawn("spearman", new Vector3(-3.3f,.77f,-1.85f), .52f);
        Spawn("archer", new Vector3(-1.8f,.77f,-2.65f), .50f);
        Spawn("swordsman", new Vector3(.20f,.77f,-2.10f), .50f);
        Spawn("knight", new Vector3(2.25f,.77f,-3.10f), .43f);
        Spawn("wizard", new Vector3(-.65f,.77f,-4.15f), .45f);
        Spawn("royal_guard", new Vector3(3.55f,.77f,-1.65f), .46f);
        Spawn("catapult", new Vector3(5.6f,.77f,-4.0f), .43f, new Vector3(0f,12f,0f));
        Spawn("trebuchet", new Vector3(-7.0f,.77f,-3.9f), .36f, new Vector3(0f,-14f,0f));

        Spawn("spearman", new Vector3(3.25f,.77f,-8.35f), .50f, new Vector3(0f,180f,0f));
        Spawn("archer", new Vector3(1.55f,.77f,-9.10f), .49f, new Vector3(0f,180f,0f));
        Spawn("swordsman", new Vector3(-.15f,.77f,-8.55f), .49f, new Vector3(0f,180f,0f));
        Spawn("knight", new Vector3(-2.25f,.77f,-7.85f), .42f, new Vector3(0f,180f,0f));
        Spawn("assassin", new Vector3(4.60f,.77f,-6.65f), .43f, new Vector3(0f,168f,0f));
        Spawn("royal_guard", new Vector3(-3.65f,.77f,-9.75f), .45f, new Vector3(0f,180f,0f));
        Spawn("ballista", new Vector3(-6.15f,.77f,-8.65f), .40f, new Vector3(0f,190f,0f));

        // Spell consequences and defensive gameplay read directly on the board.
        Spawn("fireball_scorch", new Vector3(3.55f,.76f,-5.10f), .42f, new Vector3(0f,20f,0f));
        Spawn("healing_rune", new Vector3(-3.15f,.76f,-4.25f), .43f, new Vector3(0f,-10f,0f));
        Spawn("trap_spikes", new Vector3(-3.65f,.76f,-.10f), .28f, new Vector3(0f,16f,0f));
        Spawn("reinforcement_outpost", new Vector3(-8.20f,.76f,-.70f), .31f, new Vector3(0f,18f,0f));

        // The opponent is a hero asset, not a procedural mannequin.
        Spawn("hero_opponent", new Vector3(0f, -0.05f, -18.15f), 1.02f);
    }

    private void BuildPlayerTabletop()
    {
        // Reserve tray.
        AddBox("ReserveTray", new Vector3(-9.55f,.59f,7.22f), new Vector3(6.65f,.34f,3.30f), WoodDark, .09f);
        AddBox("ReserveFelt", new Vector3(-9.55f,.79f,7.22f), new Vector3(6.15f,.045f,2.82f), Felt, .045f);
        for (int i = 0; i < 4; i++)
            AddBox($"ReserveDivider_{i}", new Vector3(-11.85f + i*1.55f,.88f,7.22f), new Vector3(.09f,.22f,2.70f), WoodLight, .025f);

        Spawn("spearman", new Vector3(-11.25f,.81f,7.18f), .68f);
        Spawn("spearman", new Vector3(-9.60f,.81f,7.18f), .68f);
        Spawn("archer", new Vector3(-7.95f,.81f,7.18f), .68f);

        // Five command cards with layered faces instead of plain blocks.
        for (int i = 0; i < 5; i++)
        {
            float x = -3.65f + i*1.83f;
            float angle = (i-2)*2.5f;
            Color face = i==2 ? new Color(.15f,.24f,.18f) : Parchment;
            AddRotatedBox($"Card_{i}", new Vector3(x,.75f,7.55f), new Vector3(1.48f,.095f,2.17f), face, new Vector3(-5f,0f,angle), .045f);
            AddRotatedBox($"CardArt_{i}", new Vector3(x,.815f,7.22f), new Vector3(.98f,.025f,.92f), i==2 ? Blue : Red, new Vector3(-5f,0f,angle), .018f);
            AddRotatedBox($"CardTextA_{i}", new Vector3(x,.835f,7.62f), new Vector3(.70f,.020f,.055f), WoodDark, new Vector3(-5f,0f,angle), .008f);
            AddRotatedBox($"CardTextB_{i}", new Vector3(x,.837f,7.79f), new Vector3(.52f,.020f,.045f), WoodDark, new Vector3(-5f,0f,angle), .008f);
            AddSphere($"CardPip_{i}", new Vector3(x,.86f,6.89f), new Vector3(.10f,.028f,.10f), i==2 ? Blue : Red);
        }

        // Deck, spellbook, mana and cheating apparatus.
        AddBox("Deck", new Vector3(6.75f,.89f,7.28f), new Vector3(2.35f,.64f,3.20f), WoodDark, .08f);
        AddBox("DeckTop", new Vector3(6.75f,1.24f,7.28f), new Vector3(2.08f,.055f,2.92f), Parchment, .035f);
        AddBox("DeckStrapV", new Vector3(6.75f,1.29f,7.28f), new Vector3(.25f,.05f,2.95f), new Color(.13f,.045f,.016f), .018f);
        AddBox("DeckStrapH", new Vector3(6.75f,1.30f,7.28f), new Vector3(2.05f,.05f,.24f), new Color(.13f,.045f,.016f), .018f);

        Spawn("spellbook_open", new Vector3(10.65f,.73f,8.20f), .70f, new Vector3(0f,-12f,0f));
        Spawn("mana_crystals", new Vector3(9.80f,.74f,6.55f), .78f, new Vector3(0f,15f,0f));
        Spawn("suspicion_dial", new Vector3(12.20f,.74f,6.85f), .74f, new Vector3(0f,-8f,0f));
        Spawn("karma_medallion", new Vector3(8.35f,.75f,8.65f), .64f);
        Spawn("cheat_stash", new Vector3(12.70f,.50f,9.25f), .58f, new Vector3(0f,180f,0f));
        Spawn("reinforcement_cart", new Vector3(-5.75f,.73f,8.05f), .55f, new Vector3(0f,12f,0f));

        // Small lived-in clutter, deliberately limited so gameplay pieces stay readable.
        Spawn("dice_cluster", new Vector3(4.85f,.73f,8.85f), .68f, new Vector3(0f,25f,0f));
        Spawn("mug", new Vector3(13.45f,.73f,8.45f), .88f, new Vector3(0f,-16f,0f));
        Spawn("candle_cluster", new Vector3(-13.35f,.73f,8.55f), .72f);
    }

    private void BuildLighting()
    {
        var key = new DirectionalLight3D
        {
            Name = "CoolKey",
            RotationDegrees = new Vector3(-52f,-28f,0f),
            LightColor = new Color(.48f,.58f,.78f),
            LightEnergy = .52f,
            ShadowEnabled = true
        };
        AddChild(key);

        AddOmni("ChandelierWarm", new Vector3(0f,10.4f,-5.1f), new Color(1f,.43f,.16f), 3.1f, 14f, true);
        AddOmni("TableWarmLeft", new Vector3(-8.8f,5.8f,1.4f), new Color(1f,.31f,.10f), 2.45f, 12f, true);
        AddOmni("TableWarmRight", new Vector3(9.0f,5.4f,-1.8f), new Color(1f,.46f,.18f), 2.15f, 11f, true);
        AddOmni("OpponentFace", new Vector3(0f,8.0f,-14.8f), new Color(1f,.48f,.25f), 1.55f, 7.5f, false);
        AddOmni("CastleTorchPlayer", new Vector3(0f,2.5f,.2f), new Color(1f,.22f,.055f), 1.45f, 5.0f, false);
        AddOmni("CastleTorchEnemy", new Vector3(0f,2.5f,-10.3f), new Color(1f,.22f,.055f), 1.25f, 5.0f, false);
        AddOmni("BoardCoolFill", new Vector3(0f,6.8f,-6.0f), new Color(.25f,.38f,.58f), .90f, 16f, false);
    }

    private void BuildCamera()
    {
        var camera = new Camera3D
        {
            Name = "PlayerCamera",
            Position = new Vector3(0f,7.35f,21.2f),
            Fov = 54f,
            Current = true
        };
        AddChild(camera);
        camera.LookAt(new Vector3(0f,1.85f,-5.2f), Vector3.Up);
    }

    private void BuildHud()
    {
        var layer = new CanvasLayer { Name = "HUD" };
        AddChild(layer);

        AddHudPanel(layer,new Vector2(18,16),new Vector2(218,52));
        AddHudPanel(layer,new Vector2(1044,16),new Vector2(218,52));
        AddHudPanel(layer,new Vector2(500,16),new Vector2(280,45));
        AddHudPanel(layer,new Vector2(1050,642),new Vector2(212,55));

        AddHudLabel(layer,"CASTLE  20 / 20",new Vector2(33,28),20,new Color(.70f,.82f,1f));
        AddHudLabel(layer,"ENEMY  20 / 20",new Vector2(1058,28),20,new Color(1f,.67f,.58f));
        AddHudLabel(layer,"ROUND 1   •   YOUR TURN",new Vector2(522,27),18,new Color(.92f,.84f,.62f));
        AddHudLabel(layer,"MANA  5 / 5",new Vector2(1066,651),17,new Color(.48f,.68f,1f));
        AddHudLabel(layer,"SUSPICION  0%",new Vector2(1066,674),14,new Color(.87f,.73f,.50f));
    }

    private Node3D Spawn(string name, Vector3 position, float scale, Vector3? rotation = null)
    {
        if (!AssetLibrary.Exists(name))
            return null;
        return AssetLibrary.Spawn(name, this, position, Vector3.One*scale, rotation ?? Vector3.Zero);
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

    private void AddSphere(string name, Vector3 position, Vector3 scale, Color color)
    {
        var mesh = new MeshInstance3D
        {
            Name = name,
            Position = position,
            Scale = scale,
            Mesh = new SphereMesh { Radius = 1f, Height = 2f },
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
            Color = new Color(.012f,.012f,.016f,.78f),
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
        label.AddThemeFontSizeOverride("font_size",fontSize);
        layer.AddChild(label);
    }
}
