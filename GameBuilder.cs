using Godot;

public partial class GameBuilder : Node3D
{
    private static readonly Color Wood = new(0.105f, 0.040f, 0.016f);
    private static readonly Color WoodLight = new(0.235f, 0.090f, 0.030f);
    private static readonly Color Parchment = new(0.56f, 0.40f, 0.22f);
    private static readonly Color Blue = new(0.032f, 0.075f, 0.23f);
    private static readonly Color BlueLight = new(0.085f, 0.20f, 0.48f);
    private static readonly Color Red = new(0.31f, 0.035f, 0.022f);
    private static readonly Color Iron = new(0.085f, 0.095f, 0.105f);
    private static readonly Color Bronze = new(0.31f, 0.14f, 0.035f);

    private const float BoardY = 0.78f;
    private const float BoardCenterZ = -5.15f;

    private BoardPlacementGrid _placementGrid;

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
            BackgroundColor = new Color(0.0045f, 0.0032f, 0.0028f),
            AmbientLightSource = Environment.AmbientSource.Color,
            AmbientLightColor = new Color(0.24f, 0.25f, 0.30f),
            AmbientLightEnergy = 0.34f,
            ReflectedLightSource = Environment.ReflectionSource.Disabled
        };

        environment.Set("tonemap_mode", 4);
        environment.Set("tonemap_exposure", 1.28f);
        environment.Set("tonemap_agx_contrast", 1.24f);
        environment.Set("ssao_enabled", true);
        environment.Set("ssao_radius", 2.35f);
        environment.Set("ssao_intensity", 3.0f);
        environment.Set("ssao_power", 1.42f);
        environment.Set("ssao_detail", 1.15f);
        environment.Set("ssil_enabled", true);
        environment.Set("ssil_radius", 3.0f);
        environment.Set("ssil_intensity", 0.72f);
        environment.Set("ssr_enabled", true);
        environment.Set("glow_enabled", true);
        environment.Set("glow_intensity", 0.12f);
        environment.Set("glow_bloom", 0.035f);
        environment.Set("fog_enabled", true);
        environment.Set("fog_density", 0.00115f);
        environment.Set("fog_light_color", new Color(0.27f, 0.15f, 0.075f));
        environment.Set("fog_light_energy", 0.30f);

        AddChild(new WorldEnvironment { Name = "WorldEnvironment", Environment = environment });
    }

    private void BuildTavern()
    {
        Spawn("hero_tavern", new Vector3(0f, -3.14f, -1.35f), 1.0f, new Vector3(0f, 180f, 0f));
    }

    private void BuildWarTable()
    {
        if (AssetLibrary.Exists("hero_table"))
        {
            Spawn("hero_table", new Vector3(0f, -0.32f, -3.10f), 1.0f);
            return;
        }

        AddBox("WarTableFallback", new Vector3(0f, -0.32f, -3.10f), new Vector3(30.2f, 1.0f, 27.0f), Wood, .78f);
        AddBox("NearRailFallback", new Vector3(0f, 0.67f, 4.05f), new Vector3(23.2f, .28f, .38f), WoodLight, .66f);
        AddBox("FarRailFallback", new Vector3(0f, 0.67f, -14.35f), new Vector3(23.2f, .28f, .38f), WoodLight, .66f);
    }

    private void BuildTavernDress()
    {
        Spawn("barrel", new Vector3(-11.05f, 0.06f, -11.55f), 1.58f, new Vector3(0f, 14f, 0f));
        Spawn("barrel", new Vector3(-9.60f, -0.08f, -12.55f), 1.08f, new Vector3(0f, -20f, 0f));
        Spawn("crate", new Vector3(10.15f, -0.16f, -11.75f), 1.35f, new Vector3(0f, -12f, 0f));
        Spawn("crate", new Vector3(11.05f, 0.00f, -12.72f), 1.00f, new Vector3(0f, 10f, 0f));
        Spawn("weapon_rack", new Vector3(-9.25f, 0.02f, -16.52f), 1.18f, new Vector3(0f, 180f, 0f));
        Spawn("shield_decor", new Vector3(-11.05f, 2.70f, -17.02f), 1.08f, new Vector3(0f, 180f, 0f));
        Spawn("shelf", new Vector3(9.15f, 0.18f, -16.72f), 1.34f, new Vector3(0f, 180f, 0f));
        Spawn("bottle_cluster", new Vector3(8.75f, 2.14f, -16.16f), 1.08f, new Vector3(0f, 180f, 0f));
        Spawn("book_stack", new Vector3(10.35f, 1.55f, -16.12f), 1.02f, new Vector3(0f, 175f, 0f));
        Spawn("skull", new Vector3(7.35f, 2.22f, -16.15f), .78f, new Vector3(0f, 165f, 0f));
        Spawn("candle_cluster", new Vector3(-9.20f, 1.05f, -10.60f), 1.20f);
        Spawn("candle_cluster", new Vector3(9.10f, 1.15f, -10.72f), 1.16f);
        Spawn("mug", new Vector3(-10.25f, .74f, -8.48f), 1.12f, new Vector3(0f, 22f, 0f));
        Spawn("chandelier", new Vector3(8.85f, 5.48f, -12.82f), .72f, new Vector3(0f, 18f, 0f));

        AddBox("BlueTavernBanner", new Vector3(-12.80f, 4.20f, -16.90f), new Vector3(1.25f, 3.55f, .065f), Blue, .92f);
        AddBox("RedTavernBanner", new Vector3(12.80f, 4.20f, -16.90f), new Vector3(1.25f, 3.55f, .065f), Red, .92f);
    }

    private void BuildBattlefield()
    {
        Spawn("hero_battlefield", new Vector3(0f, BoardY, BoardCenterZ), 1.0f);
        BuildPlacementGrid();

        string playerCastle = AssetLibrary.Exists("hero_castle_blue") ? "hero_castle_blue" : "hero_castle";
        string enemyCastle = AssetLibrary.Exists("hero_castle_red") ? "hero_castle_red" : "hero_castle";

        Spawn(playerCastle, new Vector3(0f, BoardY + .015f, 1.18f), .62f);
        Spawn(enemyCastle, new Vector3(0f, BoardY + .015f, -11.08f), .36f, new Vector3(0f, 180f, 0f));
        Spawn("hero_opponent", new Vector3(0f, -2.22f, -14.55f), 1.56f);

        Spawn("throne", new Vector3(0f, BoardY + .02f, 1.26f), .16f, new Vector3(0f, 180f, 0f));
        Spawn("king", new Vector3(0f, BoardY + .03f, 1.42f), .19f, new Vector3(0f, 180f, 0f));
        Spawn("throne", new Vector3(0f, BoardY + .02f, -10.92f), .12f);
        Spawn("king", new Vector3(0f, BoardY + .03f, -10.80f), .15f);

        Spawn("castle_brazier", new Vector3(-4.55f, BoardY + .02f, 1.00f), .34f);
        Spawn("castle_brazier", new Vector3(4.55f, BoardY + .02f, 1.00f), .34f);
        Spawn("trebuchet", new Vector3(-6.15f, BoardY + .03f, -.30f), .28f, new Vector3(0f, -8f, 0f));
        Spawn("ballista", new Vector3(6.05f, BoardY + .03f, -.42f), .25f, new Vector3(0f, 8f, 0f));

        (int col, int row, string hero, string fallback, float scale, float yaw)[] playerUnits =
        {
            (2, 6, "hero_spearman", "spearman", .32f, -4f),
            (4, 6, "hero_archer", "archer", .30f, 3f),
            (6, 6, "hero_swordsman", "swordsman", .33f, 0f),
            (8, 6, "hero_archer", "archer", .30f, -3f),
            (10, 6, "hero_spearman", "spearman", .32f, 4f),
            (3, 5, "hero_swordsman", "swordsman", .29f, 7f),
            (9, 5, "hero_swordsman", "swordsman", .29f, -7f)
        };
        foreach (var unit in playerUnits)
            SpawnHeroUnit(unit.hero, unit.fallback, GridCell(unit.col, unit.row, .03f), unit.scale, unit.yaw);

        Spawn("wizard", GridCell(6, 5, .03f), .29f, new Vector3(0f, -5f, 0f));
        Spawn("royal_guard", GridCell(1, 5, .03f), .28f, new Vector3(0f, -8f, 0f));
        Spawn("knight", GridCell(11, 5, .03f), .28f, new Vector3(0f, 8f, 0f));

        (int col, int row, string hero, string fallback, float scale, float yaw)[] enemyUnits =
        {
            (2, 1, "hero_archer", "archer", .27f, 178f),
            (4, 1, "hero_swordsman", "swordsman", .28f, 182f),
            (6, 1, "hero_spearman", "spearman", .29f, 180f),
            (8, 1, "hero_swordsman", "swordsman", .28f, 178f),
            (10, 1, "hero_archer", "archer", .27f, 182f),
            (3, 2, "hero_spearman", "spearman", .26f, 174f),
            (7, 2, "hero_archer", "archer", .25f, 180f),
            (11, 2, "hero_swordsman", "swordsman", .26f, 186f)
        };
        foreach (var unit in enemyUnits)
            SpawnHeroUnit(unit.hero, unit.fallback, GridCell(unit.col, unit.row, .03f), unit.scale, unit.yaw);

        Spawn("catapult", new Vector3(6.62f, BoardY + .03f, -7.18f), .28f, new Vector3(0f, 18f, 0f));
        Spawn("ballista", new Vector3(-6.48f, BoardY + .03f, -7.30f), .24f, new Vector3(0f, 168f, 0f));
        Spawn("campfire", new Vector3(-7.55f, BoardY + .02f, -5.15f), .34f);
        Spawn("ruin_wall", new Vector3(7.36f, BoardY + .02f, -5.28f), .38f, new Vector3(0f, 20f, 0f));
    }

    private void BuildPlacementGrid()
    {
        _placementGrid = new BoardPlacementGrid { Name = "BoardPlacementGrid" };
        AddChild(_placementGrid);
        _placementGrid.CellSelected += OnGridCellSelected;
    }

    private Vector3 GridCell(int column, int row, float yOffset = 0f)
    {
        if (_placementGrid == null)
            return new Vector3(0f, BoardY + yOffset, BoardCenterZ);

        Vector3 center = _placementGrid.GetCellCenter(new Vector2I(column, row));
        center.Y = BoardY + yOffset;
        return center;
    }

    private void OnGridCellSelected(Vector2I cell)
    {
        GD.Print($"Castle Cards placement cell selected: {cell.X},{cell.Y}");
    }

    private void BuildPlayerEdge()
    {
        (float x, float z, string hero, string fallback, float yaw)[] reserves =
        {
            (-8.65f, 6.66f, "hero_spearman", "spearman", -4f),
            (-7.35f, 6.64f, "hero_archer", "archer", 3f),
            (-6.05f, 6.62f, "hero_swordsman", "swordsman", -2f),
            (-4.75f, 6.60f, "hero_spearman", "spearman", 4f),
            (-3.45f, 6.58f, "hero_archer", "archer", -3f),
            (-2.15f, 6.57f, "hero_swordsman", "swordsman", 2f)
        };
        foreach (var reserve in reserves)
            SpawnHeroUnit(reserve.hero, reserve.fallback, new Vector3(reserve.x, .77f, reserve.z), .34f, reserve.yaw);

        for (int i = 0; i < 4; i++)
        {
            float x = .05f + i * 1.55f;
            float angle = -6f + i * 3.6f;
            Color face = i == 2 ? new Color(.64f, .46f, .27f) : Parchment;
            Color art = i switch
            {
                0 => new Color(.18f, .12f, .08f),
                1 => new Color(.22f, .22f, .25f),
                2 => new Color(.28f, .12f, .07f),
                _ => new Color(.15f, .10f, .22f)
            };
            AddRotatedBox($"Card_{i}", new Vector3(x, .77f + i * .006f, 7.28f), new Vector3(1.34f, .055f, 1.98f), face, new Vector3(-7f, 0f, angle), .84f);
            AddRotatedBox($"CardArt_{i}", new Vector3(x, .81f + i * .006f, 7.02f), new Vector3(.92f, .018f, .84f), art, new Vector3(-7f, 0f, angle), .76f);
            AddRotatedBox($"CardTitle_{i}", new Vector3(x, .814f + i * .006f, 7.78f), new Vector3(.91f, .014f, .12f), new Color(.075f, .050f, .032f), new Vector3(-7f, 0f, angle), .78f);
        }

        for (int i = 0; i < 10; i++)
            AddRotatedBox($"DeckCard_{i}", new Vector3(7.00f + i * .022f, .72f + i * .025f, 7.16f - i * .012f), new Vector3(1.38f, .048f, 1.96f), Blue, new Vector3(-4f, 0f, -7f), .82f);
        AddRotatedBox("DeckEmblem", new Vector3(7.18f, .99f, 6.94f), new Vector3(.64f, .018f, .64f), Bronze, new Vector3(-4f, 0f, -7f), .46f, .48f);

        AddTokenStack("RedTokens", new Vector3(9.15f, .81f, 6.62f), Red, 5);
        AddTokenStack("ManaTokens", new Vector3(10.25f, .81f, 6.62f), BlueLight, 5);
        AddTokenStack("IronTokens", new Vector3(11.35f, .81f, 6.62f), Iron, 5, .42f);
        Spawn("mana_crystals", new Vector3(10.20f, .78f, 7.36f), .31f, new Vector3(0f, 12f, 0f));
        Spawn("suspicion_dial", new Vector3(11.35f, .78f, 7.36f), .28f, new Vector3(0f, -8f, 0f));
        Spawn("dice_cluster", new Vector3(9.10f, .78f, 7.36f), .31f);
        Spawn("cheat_stash", new Vector3(-10.25f, .78f, 7.20f), .29f, new Vector3(0f, 12f, 0f));
    }

    private void AddTokenStack(string prefix, Vector3 origin, Color color, int count, float metallic = .15f)
    {
        for (int i = 0; i < count; i++)
        {
            int row = i % 3;
            int column = i / 3;
            AddCylinder($"{prefix}_{i}", origin + new Vector3(column * .34f, i * .026f, row * .34f), .145f, .075f, color, .48f, metallic);
        }
    }

    private void BuildLighting()
    {
        var moonFill = new DirectionalLight3D
        {
            Name = "CoolAmbientFill",
            RotationDegrees = new Vector3(-54f, -24f, 0f),
            LightColor = new Color(.39f, .46f, .60f),
            LightEnergy = .18f,
            ShadowEnabled = true
        };
        AddChild(moonFill);

        AddSpot("BoardKey", new Vector3(-7.8f, 11.2f, 8.6f), new Vector3(0f, 0.9f, -4.6f), new Color(1f, .56f, .26f), 3.6f, 31f, 48f, true);
        AddSpot("BoardCoolFill", new Vector3(8.2f, 9.4f, 4.8f), new Vector3(0f, 1.1f, -4.8f), new Color(.34f, .43f, .62f), 1.12f, 29f, 52f, false);
        AddSpot("OpponentFaceKey", new Vector3(4.4f, 7.5f, -9.8f), new Vector3(0f, 3.1f, -14.1f), new Color(1f, .43f, .17f), 2.9f, 15f, 38f, true);
        AddSpot("OpponentRim", new Vector3(-5.6f, 7.0f, -14.8f), new Vector3(0f, 3.7f, -14.1f), new Color(.34f, .42f, .60f), 1.05f, 12f, 42f, false);

        AddFlicker("LeftTavernLantern", new Vector3(-10.5f, 6.7f, -9.6f), new Color(1f, .38f, .10f), 2.05f, 8.8f, true, .09f);
        AddFlicker("RightTavernLantern", new Vector3(10.2f, 6.9f, -9.9f), new Color(1f, .42f, .12f), 2.05f, 8.8f, true, .10f);
        AddFlicker("NearTableCandleL", new Vector3(-9.6f, 1.75f, 5.55f), new Color(1f, .38f, .10f), 1.30f, 4.8f, true, .14f);
        AddFlicker("NearTableCandleR", new Vector3(10.1f, 1.85f, 5.40f), new Color(1f, .38f, .10f), 1.15f, 4.6f, true, .14f);
        AddFlicker("PlayerCastleTorchL", new Vector3(-4.55f, 2.2f, 1.0f), new Color(1f, .30f, .07f), 1.25f, 4.5f, true, .16f);
        AddFlicker("PlayerCastleTorchR", new Vector3(4.55f, 2.2f, 1.0f), new Color(1f, .30f, .07f), 1.25f, 4.5f, true, .16f);
        AddFlicker("EnemyCastleTorch", new Vector3(0f, 2.0f, -10.9f), new Color(1f, .33f, .08f), .92f, 4.2f, true, .16f);
    }

    private void BuildCamera()
    {
        var rig = new CinematicCameraController { Name = "CinematicCameraRig" };
        AddChild(rig);

        var camera = new Camera3D
        {
            Name = "PlayerCamera",
            Fov = 47.0f,
            Near = 0.08f,
            Far = 150f,
            Current = true
        };
        rig.AddChild(camera);
        rig.Configure(camera, new Vector3(0f, 1.20f, -4.85f), 20.1f, 0f, 27.5f);
    }

    private void BuildHud()
    {
        var layer = new CanvasLayer { Name = "HUD" };
        AddChild(layer);

        var backing = new ColorRect
        {
            Name = "CameraHintBacking",
            AnchorLeft = .5f,
            AnchorRight = .5f,
            AnchorTop = 1f,
            AnchorBottom = 1f,
            OffsetLeft = -222f,
            OffsetRight = 222f,
            OffsetTop = -44f,
            OffsetBottom = -12f,
            Color = new Color(.008f, .006f, .005f, .42f),
            MouseFilter = Control.MouseFilterEnum.Ignore
        };
        layer.AddChild(backing);

        var label = new Label
        {
            Name = "CameraHint",
            Text = "RMB LOOK   •   WHEEL ZOOM   •   WASD PAN   •   F RESET",
            AnchorLeft = .5f,
            AnchorRight = .5f,
            AnchorTop = 1f,
            AnchorBottom = 1f,
            OffsetLeft = -215f,
            OffsetRight = 215f,
            OffsetTop = -38f,
            OffsetBottom = -16f,
            HorizontalAlignment = HorizontalAlignment.Center,
            Modulate = new Color(.86f, .78f, .66f, .64f),
            MouseFilter = Control.MouseFilterEnum.Ignore
        };
        label.AddThemeFontSizeOverride("font_size", 12);
        layer.AddChild(label);
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

    private void AddBox(string name, Vector3 position, Vector3 size, Color color, float roughness = .82f, float metallic = 0f)
    {
        var mesh = new MeshInstance3D
        {
            Name = name,
            Position = position,
            Mesh = new BoxMesh { Size = size },
            MaterialOverride = MakeMaterial(color, roughness, metallic)
        };
        AddChild(mesh);
    }

    private void AddRotatedBox(string name, Vector3 position, Vector3 size, Color color, Vector3 rotationDegrees, float roughness = .82f, float metallic = 0f)
    {
        var mesh = new MeshInstance3D
        {
            Name = name,
            Position = position,
            RotationDegrees = rotationDegrees,
            Mesh = new BoxMesh { Size = size },
            MaterialOverride = MakeMaterial(color, roughness, metallic)
        };
        AddChild(mesh);
    }

    private void AddCylinder(string name, Vector3 position, float radius, float height, Color color, float roughness, float metallic)
    {
        var mesh = new MeshInstance3D
        {
            Name = name,
            Position = position,
            Mesh = new CylinderMesh { TopRadius = radius, BottomRadius = radius, Height = height, RadialSegments = 24 },
            MaterialOverride = MakeMaterial(color, roughness, metallic)
        };
        AddChild(mesh);
    }

    private StandardMaterial3D MakeMaterial(Color color, float roughness, float metallic = 0f)
    {
        return new StandardMaterial3D
        {
            AlbedoColor = color,
            Roughness = roughness,
            Metallic = metallic
        };
    }

    private void AddFlicker(string name, Vector3 position, Color color, float energy, float range, bool shadows, float variation)
    {
        var light = new FlickerLight
        {
            Name = name,
            Position = position,
            LightColor = color,
            BaseEnergy = energy,
            LightEnergy = energy,
            OmniRange = range,
            ShadowEnabled = shadows,
            Variation = variation,
            FlickerSpeed = 5.3f
        };
        AddChild(light);
    }

    private void AddSpot(string name, Vector3 position, Vector3 target, Color color, float energy, float range, float angle, bool shadows)
    {
        var light = new SpotLight3D
        {
            Name = name,
            Position = position,
            LightColor = color,
            LightEnergy = energy,
            SpotRange = range,
            SpotAngle = angle,
            SpotAngleAttenuation = 1.1f,
            ShadowEnabled = shadows
        };
        AddChild(light);
        light.LookAt(target, Vector3.Up);
    }
}
