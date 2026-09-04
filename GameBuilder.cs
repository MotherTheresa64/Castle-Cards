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
    private static readonly Color Iron = new(0.12f, 0.13f, 0.14f);

    private const float BoardY = 0.74f;
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
            BackgroundColor = new Color(0.006f, 0.004f, 0.003f),
            AmbientLightSource = Environment.AmbientSource.Color,
            AmbientLightColor = new Color(0.22f, 0.19f, 0.17f),
            AmbientLightEnergy = 0.50f
        };

        environment.Set("tonemap_mode", 4);
        environment.Set("tonemap_exposure", 1.54f);
        environment.Set("tonemap_agx_contrast", 1.18f);
        environment.Set("ssao_enabled", true);
        environment.Set("ssao_radius", 2.05f);
        environment.Set("ssao_intensity", 2.55f);
        environment.Set("ssao_power", 1.30f);
        environment.Set("ssao_detail", 1.0f);
        environment.Set("ssil_enabled", true);
        environment.Set("ssil_radius", 3.2f);
        environment.Set("ssil_intensity", 0.62f);
        environment.Set("glow_enabled", true);
        environment.Set("glow_intensity", 0.17f);
        environment.Set("glow_bloom", 0.05f);
        environment.Set("fog_enabled", true);
        environment.Set("fog_density", 0.00145f);
        environment.Set("fog_light_color", new Color(0.24f, 0.13f, 0.065f));
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
        Spawn("chandelier", new Vector3(8.8f, 5.45f, -12.8f), .72f, new Vector3(0f, 18f, 0f));

        AddBox("BlueTavernBanner", new Vector3(-12.8f, 4.20f, -16.90f), new Vector3(1.25f, 3.55f, .07f), Blue);
        AddBox("RedTavernBanner", new Vector3(12.8f, 4.20f, -16.90f), new Vector3(1.25f, 3.55f, .07f), Red);
        AddBox("BlueBannerPole", new Vector3(-12.8f, 6.05f, -16.87f), new Vector3(1.75f, .10f, .10f), WoodLight);
        AddBox("RedBannerPole", new Vector3(12.8f, 6.05f, -16.87f), new Vector3(1.75f, .10f, .10f), WoodLight);
    }

    private void BuildBattlefield()
    {
        Spawn("hero_battlefield", new Vector3(0f, BoardY, BoardCenterZ), 1.0f);
        BuildPlacementGrid();

        string playerCastle = AssetLibrary.Exists("hero_castle_blue") ? "hero_castle_blue" : "hero_castle";
        string enemyCastle = AssetLibrary.Exists("hero_castle_red") ? "hero_castle_red" : "hero_castle";

        Spawn(playerCastle, new Vector3(0f, BoardY + .01f, 1.25f), .62f);
        Spawn(enemyCastle, new Vector3(0f, BoardY + .01f, -11.15f), .34f, new Vector3(0f, 180f, 0f));
        Spawn("hero_opponent", new Vector3(0f, -2.20f, -14.55f), 1.56f);

        Spawn("throne", new Vector3(0f, BoardY + .02f, 1.35f), .16f, new Vector3(0f, 180f, 0f));
        Spawn("king", new Vector3(0f, BoardY + .03f, 1.47f), .19f, new Vector3(0f, 180f, 0f));
        Spawn("throne", new Vector3(0f, BoardY + .02f, -10.96f), .12f);
        Spawn("king", new Vector3(0f, BoardY + .03f, -10.86f), .15f);

        Spawn("castle_brazier", new Vector3(-4.55f, BoardY + .02f, 1.00f), .34f);
        Spawn("castle_brazier", new Vector3(4.55f, BoardY + .02f, 1.00f), .34f);
        Spawn("trebuchet", new Vector3(-6.35f, BoardY + .03f, -.45f), .28f, new Vector3(0f, -8f, 0f));
        Spawn("ballista", new Vector3(6.20f, BoardY + .03f, -.45f), .25f, new Vector3(0f, 8f, 0f));

        int[] playerCols = { 2, 3, 4, 5, 6, 7, 8, 9, 10 };
        string[] blueHero = { "hero_spearman", "hero_archer", "hero_swordsman", "hero_spearman", "hero_swordsman", "hero_spearman", "hero_archer", "hero_swordsman", "hero_spearman" };
        string[] blueFallback = { "spearman", "archer", "swordsman", "spearman", "swordsman", "spearman", "archer", "swordsman", "spearman" };
        for (int i = 0; i < playerCols.Length; i++)
            SpawnHeroUnit(blueHero[i], blueFallback[i], GridCell(playerCols[i], 7, .03f), .31f, (i - 4) * 1.5f);

        int[] supportCols = { 1, 3, 5, 7, 9, 11 };
        for (int i = 0; i < supportCols.Length; i++)
        {
            string hero = i % 2 == 0 ? "hero_archer" : "hero_swordsman";
            string fallback = i % 2 == 0 ? "archer" : "swordsman";
            SpawnHeroUnit(hero, fallback, GridCell(supportCols[i], 6, .03f), .28f, (i - 2) * 2f);
        }

        (int col, int row, string hero, string fallback, float scale, float yaw)[] centerUnits =
        {
            (1, 5, "hero_spearman", "spearman", .27f, 10f),
            (3, 5, "hero_archer", "archer", .26f, -5f),
            (5, 5, "hero_swordsman", "swordsman", .27f, 4f),
            (7, 5, "hero_spearman", "spearman", .27f, 8f),
            (9, 5, "hero_archer", "archer", .26f, 10f),
            (11, 5, "hero_swordsman", "swordsman", .27f, 12f),
            (2, 3, "hero_swordsman", "swordsman", .26f, 174f),
            (4, 3, "hero_archer", "archer", .25f, 180f),
            (6, 3, "hero_spearman", "spearman", .26f, 180f),
            (8, 3, "hero_archer", "archer", .25f, 178f),
            (10, 3, "hero_swordsman", "swordsman", .26f, 184f)
        };
        foreach (var unit in centerUnits)
            SpawnHeroUnit(unit.hero, unit.fallback, GridCell(unit.col, unit.row, .03f), unit.scale, unit.yaw);

        Spawn("wizard", GridCell(6, 4, .03f), .28f, new Vector3(0f, -5f, 0f));
        Spawn("knight", GridCell(10, 4, .03f), .26f, new Vector3(0f, 12f, 0f));
        Spawn("royal_guard", GridCell(2, 4, .03f), .27f, new Vector3(0f, -8f, 0f));

        int[] enemyCols = { 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11 };
        for (int i = 0; i < enemyCols.Length; i++)
        {
            string hero = i % 3 == 0 ? "hero_archer" : (i % 3 == 1 ? "hero_swordsman" : "hero_spearman");
            string fallback = i % 3 == 0 ? "archer" : (i % 3 == 1 ? "swordsman" : "spearman");
            SpawnHeroUnit(hero, fallback, GridCell(enemyCols[i], i % 2, .03f), .25f, 180f + (i - 5));
        }

        Spawn("catapult", new Vector3(6.65f, BoardY + .03f, -6.35f), .28f, new Vector3(0f, 18f, 0f));
        Spawn("ballista", new Vector3(-6.55f, BoardY + .03f, -7.30f), .24f, new Vector3(0f, 168f, 0f));
        Spawn("trebuchet", new Vector3(-6.95f, BoardY + .03f, -5.55f), .25f, new Vector3(0f, 160f, 0f));

        (float x, float z, string asset, float scale, float yaw)[] terrain =
        {
            (-8.85f, -1.85f, "pine_tree", .66f, -10f), (-8.10f, -2.55f, "pine_tree", .56f, 13f),
            (-7.55f, -3.20f, "oak_tree", .50f, -8f), (-8.45f, -6.05f, "oak_tree", .60f, 17f),
            (-7.65f, -6.70f, "pine_tree", .50f, -7f), (-8.70f, -8.15f, "pine_tree", .54f, 12f),
            (8.80f, -1.80f, "pine_tree", .64f, 12f), (8.05f, -2.55f, "oak_tree", .54f, -16f),
            (7.45f, -3.25f, "pine_tree", .50f, 14f), (8.45f, -6.05f, "pine_tree", .62f, -12f),
            (7.65f, -6.72f, "pine_tree", .49f, 20f), (8.75f, -8.05f, "oak_tree", .52f, -10f),
            (-6.75f, 2.05f, "rock_cluster", .42f, 18f), (6.85f, 2.00f, "rock_cluster", .44f, -12f),
            (-6.45f, -4.80f, "rock_cluster", .34f, -8f), (6.15f, -4.65f, "rock_cluster", .36f, 15f),
            (-7.75f, -5.15f, "campfire", .34f, 0f), (7.45f, -5.35f, "ruin_wall", .38f, 20f),
            (-8.25f, -9.10f, "watchtower", .28f, -8f), (8.10f, -9.00f, "ruin_wall", .34f, -18f)
        };
        foreach (var t in terrain)
            Spawn(t.asset, new Vector3(t.x, BoardY + .02f, t.z), t.scale, new Vector3(0f, t.yaw, 0f));
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
        AddBox("ReserveTrayBase", new Vector3(-7.60f, .66f, 6.62f), new Vector3(5.75f, .16f, 2.35f), new Color(.070f, .029f, .014f));
        AddBox("ReserveTrayBack", new Vector3(-7.60f, .84f, 5.58f), new Vector3(5.82f, .34f, .14f), WoodLight);
        AddBox("ReserveTrayFront", new Vector3(-7.60f, .84f, 7.66f), new Vector3(5.82f, .34f, .14f), WoodLight);
        AddBox("ReserveTrayLeft", new Vector3(-10.44f, .84f, 6.62f), new Vector3(.14f, .34f, 2.20f), WoodLight);
        AddBox("ReserveTrayRight", new Vector3(-4.76f, .84f, 6.62f), new Vector3(.14f, .34f, 2.20f), WoodLight);
        AddBox("ReserveDividerA", new Vector3(-8.55f, .79f, 6.62f), new Vector3(.10f, .22f, 2.05f), Wood);
        AddBox("ReserveDividerB", new Vector3(-6.65f, .79f, 6.62f), new Vector3(.10f, .22f, 2.05f), Wood);

        (float x, float z, string hero, string fallback)[] reserves =
        {
            (-9.55f, 6.25f, "hero_spearman", "spearman"), (-8.85f, 6.88f, "hero_archer", "archer"),
            (-7.70f, 6.28f, "hero_swordsman", "swordsman"), (-7.02f, 6.88f, "hero_spearman", "spearman"),
            (-5.90f, 6.28f, "hero_archer", "archer"), (-5.25f, 6.88f, "hero_swordsman", "swordsman")
        };
        foreach (var reserve in reserves)
            SpawnHeroUnit(reserve.hero, reserve.fallback, new Vector3(reserve.x, .76f, reserve.z), .34f, 0f);

        AddBox("ReserveFalseBottom", new Vector3(-7.60f, .69f, 7.33f), new Vector3(4.95f, .07f, .36f), new Color(.040f, .018f, .010f));
        Spawn("cheat_stash", new Vector3(-9.95f, .76f, 7.28f), .31f, new Vector3(0f, 10f, 0f));

        for (int i = 0; i < 4; i++)
        {
            float x = -2.65f + i * 1.62f;
            float angle = (i - 1.5f) * 3.5f;
            Color face = i == 2 ? new Color(.66f, .50f, .30f) : Parchment;
            Color art = i switch
            {
                0 => BlueLight,
                1 => new Color(.36f, .34f, .40f),
                2 => new Color(.34f, .20f, .12f),
                _ => new Color(.24f, .15f, .30f)
            };
            AddRotatedBox($"Card_{i}", new Vector3(x, .75f, 7.48f), new Vector3(1.38f, .065f, 2.04f), face, new Vector3(-7f, 0f, angle));
            AddRotatedBox($"CardArt_{i}", new Vector3(x, .80f, 7.17f), new Vector3(.92f, .018f, .86f), art, new Vector3(-7f, 0f, angle));
            AddRotatedBox($"CardTitle_{i}", new Vector3(x, .805f, 7.91f), new Vector3(.90f, .014f, .12f), new Color(.095f, .070f, .045f), new Vector3(-7f, 0f, angle));
        }

        for (int i = 0; i < 8; i++)
            AddRotatedBox($"DeckCard_{i}", new Vector3(4.60f + i * .030f, .73f + i * .032f, 7.26f - i * .020f), new Vector3(1.42f, .052f, 1.98f), Blue, new Vector3(-4f, 0f, -7f));
        AddRotatedBox("DeckEmblem", new Vector3(4.77f, 1.00f, 7.02f), new Vector3(.68f, .018f, .68f), new Color(.58f, .38f, .10f), new Vector3(-4f, 0f, -7f));

        AddBox("ResourceTrayBase", new Vector3(8.30f, .66f, 6.65f), new Vector3(4.75f, .16f, 2.35f), new Color(.070f, .029f, .014f));
        AddBox("ResourceTrayBack", new Vector3(8.30f, .84f, 5.60f), new Vector3(4.82f, .34f, .14f), WoodLight);
        AddBox("ResourceTrayFront", new Vector3(8.30f, .84f, 7.70f), new Vector3(4.82f, .34f, .14f), WoodLight);
        AddBox("ResourceDividerA", new Vector3(7.52f, .80f, 6.65f), new Vector3(.10f, .22f, 2.05f), Wood);
        AddBox("ResourceDividerB", new Vector3(9.08f, .80f, 6.65f), new Vector3(.10f, .22f, 2.05f), Wood);

        AddTokenStack("RedTokens", new Vector3(6.72f, .80f, 6.45f), Red, 5);
        AddTokenStack("ManaTokens", new Vector3(8.28f, .80f, 6.45f), BlueLight, 5);
        AddTokenStack("IronTokens", new Vector3(9.85f, .80f, 6.45f), Iron, 5);
        Spawn("mana_crystals", new Vector3(8.25f, .76f, 7.12f), .34f, new Vector3(0f, 12f, 0f));
        Spawn("suspicion_dial", new Vector3(9.83f, .76f, 7.15f), .31f, new Vector3(0f, -8f, 0f));
        Spawn("dice_cluster", new Vector3(6.68f, .76f, 7.18f), .34f);
    }

    private void AddTokenStack(string prefix, Vector3 origin, Color color, int count)
    {
        for (int i = 0; i < count; i++)
        {
            float row = i % 3;
            float column = i / 3;
            AddRotatedBox($"{prefix}_{i}", origin + new Vector3(column * .38f, i * .025f, row * .36f), new Vector3(.30f, .13f, .30f), color, new Vector3(0f, i * 11f, 0f));
        }
    }

    private void BuildLighting()
    {
        var fill = new DirectionalLight3D
        {
            Name = "CoolAmbientFill",
            RotationDegrees = new Vector3(-56f, -22f, 0f),
            LightColor = new Color(.44f, .49f, .59f),
            LightEnergy = .20f,
            ShadowEnabled = true
        };
        AddChild(fill);

        AddOmni("OpponentWarmKey", new Vector3(3.2f, 6.55f, -13.20f), new Color(1f, .49f, .20f), 3.45f, 11.8f, true);
        AddOmni("OpponentFaceFill", new Vector3(-2.8f, 5.55f, -12.35f), new Color(.46f, .56f, .72f), .74f, 8.8f, false);
        AddOmni("BoardCenterWarm", new Vector3(-1.0f, 5.25f, -4.35f), new Color(1f, .65f, .33f), 2.45f, 13.0f, true);
        AddOmni("BoardCoolLift", new Vector3(5.3f, 5.7f, -2.6f), new Color(.39f, .48f, .62f), .58f, 12.2f, false);
        AddOmni("PlayerCastleTorchL", new Vector3(-4.5f, 2.9f, 1.1f), new Color(1f, .35f, .09f), 1.50f, 5.5f, true);
        AddOmni("PlayerCastleTorchR", new Vector3(4.5f, 2.9f, 1.1f), new Color(1f, .35f, .09f), 1.50f, 5.5f, true);
        AddOmni("EnemyCastleWarm", new Vector3(0f, 3.8f, -10.9f), new Color(1f, .43f, .14f), 1.48f, 6.5f, true);
        AddOmni("LeftTavernLantern", new Vector3(-10.5f, 6.8f, -9.6f), new Color(1f, .42f, .15f), 1.90f, 8.8f, true);
        AddOmni("RightTavernLantern", new Vector3(10.2f, 7.0f, -9.9f), new Color(1f, .46f, .17f), 1.92f, 8.8f, true);
        AddOmni("NearTableCandleL", new Vector3(-10.2f, 2.0f, 5.9f), new Color(1f, .45f, .16f), 1.45f, 5.2f, true);
        AddOmni("NearTableCandleR", new Vector3(10.4f, 2.2f, 5.6f), new Color(1f, .43f, .14f), 1.30f, 5.0f, true);
    }

    private void BuildCamera()
    {
        var camera = new Camera3D
        {
            Name = "PlayerCamera",
            Position = new Vector3(0f, 9.15f, 15.85f),
            Fov = 50.5f,
            Near = 0.08f,
            Far = 120f,
            Current = true
        };
        AddChild(camera);
        camera.LookAt(new Vector3(0f, 1.30f, -4.85f), Vector3.Up);
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
        var rect = new ColorRect { Position = position, Size = size, Color = new Color(.014f, .010f, .010f, .50f), MouseFilter = Control.MouseFilterEnum.Ignore };
        layer.AddChild(rect);
    }

    private void AddHudLabel(CanvasLayer layer, string text, Vector2 position, int fontSize, Color color)
    {
        var label = new Label { Text = text, Position = position, Modulate = color, MouseFilter = Control.MouseFilterEnum.Ignore };
        label.AddThemeFontSizeOverride("font_size", fontSize);
        layer.AddChild(label);
    }
}
