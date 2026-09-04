using Godot;

public partial class GameBuilder : Node3D
{
    private static readonly Color WoodDark = new(0.10f, 0.040f, 0.018f);
    private static readonly Color Wood = new(0.22f, 0.090f, 0.030f);
    private static readonly Color WoodLight = new(0.34f, 0.155f, 0.055f);
    private static readonly Color StoneDark = new(0.17f, 0.17f, 0.18f);
    private static readonly Color Stone = new(0.32f, 0.31f, 0.30f);
    private static readonly Color StoneLight = new(0.43f, 0.41f, 0.38f);
    private static readonly Color Grass = new(0.105f, 0.18f, 0.085f);
    private static readonly Color GrassDark = new(0.055f, 0.105f, 0.050f);
    private static readonly Color River = new(0.055f, 0.18f, 0.25f);
    private static readonly Color Road = new(0.30f, 0.225f, 0.135f);
    private static readonly Color Iron = new(0.08f, 0.085f, 0.095f);
    private static readonly Color Blue = new(0.055f, 0.12f, 0.34f);
    private static readonly Color Red = new(0.39f, 0.055f, 0.035f);
    private static readonly Color Parchment = new(0.55f, 0.38f, 0.19f);

    public override void _Ready()
    {
        BuildEnvironment();
        BuildTavern();
        BuildWarTable();
        BuildBattlefield();
        BuildPlayerSide();
        BuildOpponent();
        BuildLighting();
        BuildCamera();
    }

    private void BuildEnvironment()
    {
        var environment = new Environment
        {
            BackgroundMode = Environment.BGMode.Color,
            BackgroundColor = new Color(0.012f, 0.010f, 0.014f),
            AmbientLightSource = Environment.AmbientSource.Color,
            AmbientLightColor = new Color(0.25f, 0.26f, 0.34f),
            AmbientLightEnergy = 0.72f
        };

        AddChild(new WorldEnvironment
        {
            Name = "WorldEnvironment",
            Environment = environment
        });
    }

    private void BuildTavern()
    {
        AddBox("Floor", new Vector3(0f, -3.0f, -3f), new Vector3(34f, 0.45f, 34f), WoodDark);
        AddBox("BackWall", new Vector3(0f, 7f, -19f), new Vector3(34f, 20f, 0.7f), new Color(0.075f, 0.055f, 0.048f));
        AddBox("LeftWall", new Vector3(-17f, 7f, -3f), new Vector3(0.7f, 20f, 32f), new Color(0.065f, 0.048f, 0.043f));
        AddBox("RightWall", new Vector3(17f, 7f, -3f), new Vector3(0.7f, 20f, 32f), new Color(0.065f, 0.048f, 0.043f));

        for (int x = -15; x <= 15; x += 5)
            AddBox($"BackBeam_{x}", new Vector3(x, 7f, -18.55f), new Vector3(0.5f, 19f, 0.45f), WoodDark);

        AddBox("BackBeamTop", new Vector3(0f, 13.2f, -18.5f), new Vector3(33f, 0.55f, 0.55f), WoodDark);
        AddBox("BackBeamMid", new Vector3(0f, 5.7f, -18.5f), new Vector3(33f, 0.45f, 0.45f), WoodDark);

        BuildShelf(new Vector3(-12.8f, 1.8f, -17.7f));
        BuildShelf(new Vector3(11.7f, 1.8f, -17.7f));

        AddBanner(new Vector3(-7.5f, 7.0f, -18.05f), Blue);
        AddBanner(new Vector3(7.5f, 7.0f, -18.05f), Red);

        for (int i = 0; i < 4; i++)
        {
            float z = -14.5f + i * 4.0f;
            AddBox($"LeftBarrel_{i}", new Vector3(-15.3f, -1.8f, z), new Vector3(1.25f, 2.0f, 1.25f), Wood);
            AddBox($"LeftBarrelBandA_{i}", new Vector3(-15.3f, -1.25f, z), new Vector3(1.35f, 0.12f, 1.35f), Iron);
            AddBox($"LeftBarrelBandB_{i}", new Vector3(-15.3f, -2.30f, z), new Vector3(1.35f, 0.12f, 1.35f), Iron);
        }

        BuildLantern(new Vector3(-11.5f, 6.5f, -17.3f), "WallLanternLeft");
        BuildLantern(new Vector3(11.5f, 6.5f, -17.3f), "WallLanternRight");
    }

    private void BuildShelf(Vector3 origin)
    {
        AddBox("ShelfBack", origin, new Vector3(5.0f, 5.6f, 0.35f), WoodDark);
        AddBox("ShelfLeft", origin + new Vector3(-2.3f, 0f, -0.25f), new Vector3(0.3f, 5.6f, 1.1f), Wood);
        AddBox("ShelfRight", origin + new Vector3(2.3f, 0f, -0.25f), new Vector3(0.3f, 5.6f, 1.1f), Wood);

        for (int i = 0; i < 4; i++)
        {
            float y = -0.9f + i * 1.55f;
            AddBox($"ShelfPlank_{i}", origin + new Vector3(0f, y, -0.45f), new Vector3(4.8f, 0.20f, 1.15f), WoodLight);
        }

        AddBox("ShelfCrateA", origin + new Vector3(-1.25f, -1.95f, -0.75f), new Vector3(1.45f, 1.0f, 0.9f), Wood);
        AddBox("ShelfCrateB", origin + new Vector3(0.7f, -0.35f, -0.75f), new Vector3(1.1f, 0.85f, 0.9f), WoodLight);
        AddBox("ShelfBottleA", origin + new Vector3(-1.25f, 1.25f, -0.75f), new Vector3(0.35f, 0.85f, 0.35f), new Color(0.10f, 0.22f, 0.12f));
        AddBox("ShelfBottleB", origin + new Vector3(-0.55f, 1.18f, -0.75f), new Vector3(0.30f, 0.72f, 0.30f), new Color(0.20f, 0.11f, 0.07f));
        AddBox("ShelfBottleC", origin + new Vector3(1.35f, 2.65f, -0.75f), new Vector3(0.34f, 0.80f, 0.34f), new Color(0.08f, 0.16f, 0.19f));
    }

    private void AddBanner(Vector3 position, Color color)
    {
        AddBox("BannerPole", position + new Vector3(0f, 1.7f, 0f), new Vector3(2.7f, 0.12f, 0.12f), Iron);
        AddBox("BannerCloth", position, new Vector3(2.2f, 3.0f, 0.16f), color);
        AddBox("BannerTip", position + new Vector3(0f, -1.65f, 0f), new Vector3(1.15f, 0.35f, 0.18f), color);
    }

    private void BuildWarTable()
    {
        AddBox("WarTableTop", new Vector3(0f, -0.15f, -2.4f), new Vector3(27f, 1.0f, 25f), Wood);
        AddBox("WarTableNearTrim", new Vector3(0f, 0.25f, 10.0f), new Vector3(27.5f, 0.65f, 0.7f), WoodLight);
        AddBox("WarTableFarTrim", new Vector3(0f, 0.25f, -14.8f), new Vector3(27.5f, 0.65f, 0.7f), WoodLight);
        AddBox("WarTableLeftTrim", new Vector3(-13.35f, 0.25f, -2.4f), new Vector3(0.7f, 0.65f, 24.3f), WoodLight);
        AddBox("WarTableRightTrim", new Vector3(13.35f, 0.25f, -2.4f), new Vector3(0.7f, 0.65f, 24.3f), WoodLight);

        AddBox("BattleBoard", new Vector3(0f, 0.53f, -4.0f), new Vector3(20.5f, 0.26f, 16.4f), GrassDark);
        AddBox("BattlefieldSurface", new Vector3(0f, 0.68f, -4.0f), new Vector3(19.6f, 0.12f, 15.5f), Grass);
    }

    private void BuildBattlefield()
    {
        BuildRiver();
        BuildRoad();
        BuildBridge();

        BuildForest(new Vector3(-7.2f, 0.85f, -5.0f), 5, 1.15f);
        BuildForest(new Vector3(7.2f, 0.85f, -7.2f), 4, 1.0f);
        BuildForest(new Vector3(6.6f, 0.85f, 0.0f), 3, 0.9f);

        AddRockCluster(new Vector3(-7.0f, 0.85f, -10.0f));
        AddRockCluster(new Vector3(6.8f, 0.85f, 2.2f));

        BuildCastle(new Vector3(0f, 0.80f, 2.0f), Blue, false);
        BuildCastle(new Vector3(0f, 0.80f, -10.2f), Red, true);

        BuildMiniature(new Vector3(-3.6f, 0.85f, -0.1f), Blue, "PlayerSpearmanA");
        BuildMiniature(new Vector3(-1.8f, 0.85f, -1.7f), Blue, "PlayerSpearmanB");
        BuildMiniature(new Vector3(2.8f, 0.85f, -0.8f), Blue, "PlayerArcher");

        BuildMiniature(new Vector3(3.4f, 0.85f, -7.0f), Red, "EnemySpearmanA");
        BuildMiniature(new Vector3(1.3f, 0.85f, -8.0f), Red, "EnemySpearmanB");
        BuildMiniature(new Vector3(-3.0f, 0.85f, -7.4f), Red, "EnemyArcher");
    }

    private void BuildRiver()
    {
        AddRotatedBox("RiverA", new Vector3(-5.8f, 0.77f, -1.4f), new Vector3(2.15f, 0.08f, 5.2f), River, new Vector3(0f, 8f, 0f));
        AddRotatedBox("RiverB", new Vector3(-5.0f, 0.77f, -5.8f), new Vector3(2.15f, 0.08f, 4.2f), River, new Vector3(0f, -12f, 0f));
        AddRotatedBox("RiverC", new Vector3(-5.6f, 0.77f, -9.6f), new Vector3(2.15f, 0.08f, 3.7f), River, new Vector3(0f, 9f, 0f));
    }

    private void BuildRoad()
    {
        AddRotatedBox("RoadA", new Vector3(0.0f, 0.78f, -1.3f), new Vector3(2.4f, 0.06f, 4.3f), Road, new Vector3(0f, -5f, 0f));
        AddRotatedBox("RoadB", new Vector3(-0.4f, 0.78f, -5.2f), new Vector3(2.2f, 0.06f, 4.0f), Road, new Vector3(0f, 8f, 0f));
        AddRotatedBox("RoadC", new Vector3(0.1f, 0.78f, -8.4f), new Vector3(2.0f, 0.06f, 2.9f), Road, new Vector3(0f, -6f, 0f));
    }

    private void BuildBridge()
    {
        for (int i = 0; i < 7; i++)
        {
            AddBox($"BridgePlank_{i}", new Vector3(-5.25f + i * 0.34f, 0.94f, -4.05f), new Vector3(0.28f, 0.16f, 2.6f), i % 2 == 0 ? WoodLight : Wood);
        }
        AddBox("BridgeRailL", new Vector3(-5.9f, 1.25f, -4.05f), new Vector3(0.12f, 0.55f, 2.7f), WoodDark);
        AddBox("BridgeRailR", new Vector3(-4.0f, 1.25f, -4.05f), new Vector3(0.12f, 0.55f, 2.7f), WoodDark);
    }

    private void BuildForest(Vector3 origin, int count, float spacing)
    {
        for (int i = 0; i < count; i++)
        {
            float x = origin.X + ((i % 3) - 1) * spacing;
            float z = origin.Z + (i / 3) * spacing;
            BuildTree(new Vector3(x, origin.Y, z), 0.85f + 0.1f * (i % 2));
        }
    }

    private void BuildTree(Vector3 origin, float scale)
    {
        AddBox("TreeTrunk", origin + new Vector3(0f, 0.72f * scale, 0f), new Vector3(0.34f * scale, 1.45f * scale, 0.34f * scale), WoodDark);
        AddRotatedBox("TreeCanopyA", origin + new Vector3(0f, 1.65f * scale, 0f), new Vector3(1.45f * scale, 0.85f * scale, 1.25f * scale), new Color(0.075f, 0.20f, 0.07f), new Vector3(0f, 22f, 0f));
        AddRotatedBox("TreeCanopyB", origin + new Vector3(-0.35f * scale, 2.05f * scale, 0.05f), new Vector3(1.05f * scale, 0.75f * scale, 1.0f * scale), new Color(0.10f, 0.27f, 0.085f), new Vector3(0f, -18f, 0f));
        AddRotatedBox("TreeCanopyC", origin + new Vector3(0.35f * scale, 2.12f * scale, -0.10f), new Vector3(0.95f * scale, 0.70f * scale, 0.95f * scale), new Color(0.065f, 0.155f, 0.055f), new Vector3(0f, 40f, 0f));
    }

    private void AddRockCluster(Vector3 origin)
    {
        AddRotatedBox("RockA", origin + new Vector3(-0.35f, 0.30f, 0f), new Vector3(0.8f, 0.55f, 0.65f), StoneDark, new Vector3(12f, 22f, 5f));
        AddRotatedBox("RockB", origin + new Vector3(0.35f, 0.22f, 0.18f), new Vector3(0.65f, 0.42f, 0.8f), Stone, new Vector3(-8f, -15f, 8f));
        AddRotatedBox("RockC", origin + new Vector3(0.0f, 0.15f, -0.42f), new Vector3(0.55f, 0.35f, 0.5f), StoneLight, new Vector3(5f, 38f, -6f));
    }

    private void BuildCastle(Vector3 origin, Color teamColor, bool enemy)
    {
        float face = enemy ? 1f : -1f;

        AddBox("CastleCourtyard", origin + new Vector3(0f, 0.15f, 0f), new Vector3(6.7f, 0.25f, 4.6f), StoneDark);
        AddBox("CastleKeep", origin + new Vector3(0f, 1.55f, 0.35f * face), new Vector3(2.45f, 2.9f, 2.2f), Stone);
        AddBox("KeepTop", origin + new Vector3(0f, 3.05f, 0.35f * face), new Vector3(2.75f, 0.28f, 2.5f), StoneLight);

        float wallZ = 1.72f * face;
        AddBox("CastleWallLeft", origin + new Vector3(-2.15f, 1.0f, wallZ), new Vector3(2.35f, 1.95f, 0.62f), Stone);
        AddBox("CastleWallRight", origin + new Vector3(2.15f, 1.0f, wallZ), new Vector3(2.35f, 1.95f, 0.62f), Stone);

        BuildTower(origin + new Vector3(-3.0f, 0f, wallZ), teamColor);
        BuildTower(origin + new Vector3(3.0f, 0f, wallZ), teamColor);

        AddBox("GateLintel", origin + new Vector3(0f, 1.75f, wallZ), new Vector3(1.55f, 0.55f, 0.72f), StoneLight);
        AddBox("Gate", origin + new Vector3(0f, 0.75f, wallZ + 0.05f * face), new Vector3(1.10f, 1.55f, 0.18f), WoodDark);

        for (int i = -2; i <= 2; i++)
        {
            AddBox($"KeepMerlon_{i}", origin + new Vector3(i * 0.52f, 3.45f, 0.35f * face), new Vector3(0.32f, 0.55f, 0.42f), StoneLight);
        }

        AddBox("CastleBannerPole", origin + new Vector3(0f, 4.15f, 0.35f * face), new Vector3(0.08f, 2.1f, 0.08f), Iron);
        AddBox("CastleBanner", origin + new Vector3(0.55f, 4.55f, 0.35f * face), new Vector3(1.05f, 0.75f, 0.10f), teamColor);
    }

    private void BuildTower(Vector3 origin, Color teamColor)
    {
        AddBox("TowerCore", origin + new Vector3(0f, 1.25f, 0f), new Vector3(1.45f, 2.55f, 1.45f), Stone);
        AddBox("TowerTop", origin + new Vector3(0f, 2.65f, 0f), new Vector3(1.75f, 0.26f, 1.75f), StoneLight);

        AddBox("TowerMerlonA", origin + new Vector3(-0.50f, 3.02f, -0.50f), new Vector3(0.38f, 0.55f, 0.38f), StoneLight);
        AddBox("TowerMerlonB", origin + new Vector3(0.50f, 3.02f, -0.50f), new Vector3(0.38f, 0.55f, 0.38f), StoneLight);
        AddBox("TowerMerlonC", origin + new Vector3(-0.50f, 3.02f, 0.50f), new Vector3(0.38f, 0.55f, 0.38f), StoneLight);
        AddBox("TowerMerlonD", origin + new Vector3(0.50f, 3.02f, 0.50f), new Vector3(0.38f, 0.55f, 0.38f), StoneLight);
        AddBox("TowerAccent", origin + new Vector3(0f, 1.72f, -0.76f), new Vector3(0.40f, 0.75f, 0.09f), teamColor);
    }

    private void BuildMiniature(Vector3 origin, Color teamColor, string prefix)
    {
        AddBox($"{prefix}_Base", origin + new Vector3(0f, 0.12f, 0f), new Vector3(0.85f, 0.22f, 0.85f), Iron);
        AddBox($"{prefix}_Legs", origin + new Vector3(0f, 0.55f, 0f), new Vector3(0.42f, 0.70f, 0.35f), WoodDark);
        AddBox($"{prefix}_Body", origin + new Vector3(0f, 1.18f, 0f), new Vector3(0.72f, 0.85f, 0.46f), teamColor);
        AddBox($"{prefix}_Head", origin + new Vector3(0f, 1.82f, -0.02f), new Vector3(0.43f, 0.43f, 0.43f), new Color(0.57f, 0.36f, 0.24f));
        AddBox($"{prefix}_Helmet", origin + new Vector3(0f, 2.05f, -0.02f), new Vector3(0.52f, 0.20f, 0.52f), StoneLight);
        AddBox($"{prefix}_Spear", origin + new Vector3(0.46f, 1.42f, 0f), new Vector3(0.08f, 2.55f, 0.08f), WoodLight);
        AddBox($"{prefix}_SpearTip", origin + new Vector3(0.46f, 2.74f, 0f), new Vector3(0.18f, 0.25f, 0.18f), StoneLight);
        AddBox($"{prefix}_Shield", origin + new Vector3(-0.43f, 1.24f, -0.25f), new Vector3(0.18f, 0.80f, 0.68f), teamColor);
    }

    private void BuildPlayerSide()
    {
        AddBox("ReserveTray", new Vector3(-8.6f, 0.68f, 7.25f), new Vector3(5.4f, 0.28f, 2.4f), WoodDark);
        AddBox("ReserveTrayLipNear", new Vector3(-8.6f, 0.95f, 8.35f), new Vector3(5.5f, 0.42f, 0.18f), WoodLight);
        AddBox("ReserveTrayLipFar", new Vector3(-8.6f, 0.95f, 6.15f), new Vector3(5.5f, 0.42f, 0.18f), WoodLight);

        for (int i = 0; i < 3; i++)
            BuildMiniature(new Vector3(-10.0f + i * 1.35f, 0.85f, 7.2f), Blue, $"ReserveUnit_{i}");

        for (int i = 0; i < 5; i++)
        {
            float x = -3.2f + i * 1.65f;
            float tilt = -8f + i * 4f;
            AddRotatedBox($"Card_{i}", new Vector3(x, 0.92f, 8.65f), new Vector3(1.35f, 0.11f, 2.15f), i == 2 ? Parchment : new Color(0.28f, 0.095f, 0.045f), new Vector3(-5f, tilt, 0f));
            AddRotatedBox($"CardInset_{i}", new Vector3(x, 0.995f, 8.48f), new Vector3(0.92f, 0.035f, 1.20f), i == 2 ? new Color(0.15f, 0.28f, 0.16f) : new Color(0.43f, 0.26f, 0.12f), new Vector3(-5f, tilt, 0f));
        }

        AddBox("Deck", new Vector3(6.8f, 0.88f, 8.2f), new Vector3(1.55f, 0.50f, 2.35f), new Color(0.16f, 0.045f, 0.026f));
        AddBox("DeckTop", new Vector3(6.8f, 1.16f, 8.2f), new Vector3(1.45f, 0.08f, 2.25f), Parchment);

        AddBox("ManaTray", new Vector3(9.7f, 0.72f, 7.4f), new Vector3(3.7f, 0.24f, 2.6f), WoodDark);
        for (int i = 0; i < 4; i++)
            AddRotatedBox($"ManaGem_{i}", new Vector3(8.55f + i * 0.75f, 1.02f, 7.4f), new Vector3(0.42f, 0.42f, 0.42f), new Color(0.12f, 0.38f, 0.62f), new Vector3(20f, 35f + i * 10f, 15f));
    }

    private void BuildOpponent()
    {
        Vector3 origin = new(0f, 0f, -16.6f);

        AddBox("OpponentChairBack", origin + new Vector3(0f, 4.3f, 1.0f), new Vector3(5.2f, 7.8f, 0.65f), WoodDark);
        AddBox("OpponentTorso", origin + new Vector3(0f, 5.15f, 0.15f), new Vector3(4.3f, 4.8f, 1.8f), new Color(0.11f, 0.12f, 0.16f));
        AddBox("OpponentShoulders", origin + new Vector3(0f, 6.75f, 0.02f), new Vector3(5.4f, 1.0f, 2.0f), new Color(0.14f, 0.15f, 0.20f));
        AddBox("OpponentNeck", origin + new Vector3(0f, 8.15f, 0.02f), new Vector3(0.9f, 1.1f, 0.9f), new Color(0.44f, 0.28f, 0.20f));
        AddBox("OpponentHead", origin + new Vector3(0f, 9.3f, 0.0f), new Vector3(1.75f, 2.0f, 1.55f), new Color(0.50f, 0.32f, 0.22f));
        AddBox("OpponentHair", origin + new Vector3(0f, 10.25f, 0.08f), new Vector3(1.9f, 0.55f, 1.7f), new Color(0.09f, 0.055f, 0.035f));
        AddBox("OpponentBrow", origin + new Vector3(0f, 9.52f, -0.82f), new Vector3(1.35f, 0.14f, 0.10f), new Color(0.10f, 0.065f, 0.045f));

        AddRotatedBox("OpponentArmLeft", origin + new Vector3(-3.2f, 3.1f, 2.0f), new Vector3(1.05f, 4.7f, 1.05f), new Color(0.14f, 0.15f, 0.20f), new Vector3(42f, 0f, 18f));
        AddRotatedBox("OpponentArmRight", origin + new Vector3(3.2f, 3.1f, 2.0f), new Vector3(1.05f, 4.7f, 1.05f), new Color(0.14f, 0.15f, 0.20f), new Vector3(42f, 0f, -18f));
        AddBox("OpponentHandLeft", origin + new Vector3(-3.95f, 1.55f, 3.5f), new Vector3(1.0f, 0.48f, 1.3f), new Color(0.50f, 0.32f, 0.22f));
        AddBox("OpponentHandRight", origin + new Vector3(3.95f, 1.55f, 3.5f), new Vector3(1.0f, 0.48f, 1.3f), new Color(0.50f, 0.32f, 0.22f));
    }

    private void BuildLantern(Vector3 position, string name)
    {
        AddBox($"{name}_Frame", position, new Vector3(0.65f, 1.0f, 0.65f), Iron);
        AddBox($"{name}_Glow", position, new Vector3(0.35f, 0.62f, 0.35f), new Color(0.90f, 0.34f, 0.08f));

        var light = new OmniLight3D
        {
            Name = $"{name}_Light",
            Position = position,
            LightColor = new Color(1.0f, 0.43f, 0.18f),
            LightEnergy = 3.3f,
            OmniRange = 10f,
            ShadowEnabled = true
        };
        AddChild(light);
    }

    private void BuildLighting()
    {
        var coolFill = new DirectionalLight3D
        {
            Name = "CoolFill",
            RotationDegrees = new Vector3(-52f, -28f, 0f),
            LightColor = new Color(0.42f, 0.52f, 0.80f),
            LightEnergy = 1.15f,
            ShadowEnabled = true
        };
        AddChild(coolFill);

        var playerKey = new OmniLight3D
        {
            Name = "PlayerWarmKey",
            Position = new Vector3(-7f, 8.5f, 9f),
            LightColor = new Color(1.0f, 0.42f, 0.15f),
            LightEnergy = 7.0f,
            OmniRange = 26f,
            ShadowEnabled = true
        };
        AddChild(playerKey);

        var boardFill = new OmniLight3D
        {
            Name = "BoardWarmFill",
            Position = new Vector3(7f, 6f, -5f),
            LightColor = new Color(1.0f, 0.64f, 0.30f),
            LightEnergy = 4.2f,
            OmniRange = 22f,
            ShadowEnabled = true
        };
        AddChild(boardFill);

        var enemyRim = new OmniLight3D
        {
            Name = "EnemyRim",
            Position = new Vector3(-5f, 9f, -15f),
            LightColor = new Color(0.45f, 0.52f, 0.82f),
            LightEnergy = 3.2f,
            OmniRange = 15f
        };
        AddChild(enemyRim);
    }

    private void BuildCamera()
    {
        var camera = new Camera3D
        {
            Name = "PlayerCamera",
            Position = new Vector3(0f, 7.3f, 18.5f),
            Fov = 62f,
            Current = true
        };

        AddChild(camera);
        camera.LookAt(new Vector3(0f, 2.1f, -4.4f), Vector3.Up);
    }

    private MeshInstance3D AddBox(string name, Vector3 position, Vector3 size, Color color)
    {
        var material = new StandardMaterial3D
        {
            AlbedoColor = color,
            Roughness = 0.92f
        };

        var mesh = new MeshInstance3D
        {
            Name = name,
            Position = position,
            Mesh = new BoxMesh { Size = size },
            MaterialOverride = material
        };

        AddChild(mesh);
        return mesh;
    }

    private MeshInstance3D AddRotatedBox(string name, Vector3 position, Vector3 size, Color color, Vector3 rotationDegrees)
    {
        MeshInstance3D mesh = AddBox(name, position, size, color);
        mesh.RotationDegrees = rotationDegrees;
        return mesh;
    }
}
