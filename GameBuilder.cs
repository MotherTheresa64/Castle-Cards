using Godot;

public partial class GameBuilder : Node3D
{
    private static readonly Color WoodDark = new(0.060f, 0.023f, 0.012f);
    private static readonly Color Wood = new(0.165f, 0.070f, 0.028f);
    private static readonly Color WoodLight = new(0.285f, 0.135f, 0.055f);
    private static readonly Color Wall = new(0.060f, 0.052f, 0.060f);
    private static readonly Color Iron = new(0.060f, 0.065f, 0.075f);
    private static readonly Color Grass = new(0.105f, 0.175f, 0.075f);
    private static readonly Color GrassDark = new(0.040f, 0.075f, 0.038f);
    private static readonly Color River = new(0.040f, 0.155f, 0.235f);
    private static readonly Color Road = new(0.31f, 0.225f, 0.125f);
    private static readonly Color Parchment = new(0.56f, 0.38f, 0.19f);
    private static readonly Color Blue = new(0.050f, 0.115f, 0.34f);
    private static readonly Color Red = new(0.38f, 0.045f, 0.030f);
    private static readonly Color Skin = new(0.61f, 0.37f, 0.23f);
    private static readonly Color Shirt = new(0.125f, 0.050f, 0.060f);

    public override void _Ready()
    {
        BuildEnvironment();
        BuildTavern();
        BuildWarTable();
        BuildBattlefield();
        BuildPlayerArea();
        BuildOpponent();
        BuildLighting();
        BuildCamera();
    }

    private void BuildEnvironment()
    {
        var environment = new Environment
        {
            BackgroundMode = Environment.BGMode.Color,
            BackgroundColor = new Color(0.009f, 0.009f, 0.014f),
            AmbientLightSource = Environment.AmbientSource.Color,
            AmbientLightColor = new Color(0.32f, 0.35f, 0.46f),
            AmbientLightEnergy = 1.12f
        };

        AddChild(new WorldEnvironment
        {
            Name = "WorldEnvironment",
            Environment = environment
        });
    }

    private void BuildTavern()
    {
        AddBox("Floor", new Vector3(0f, -3.2f, -3f), new Vector3(38f, 0.55f, 38f), WoodDark);
        AddBox("BackWall", new Vector3(0f, 7.0f, -21f), new Vector3(38f, 21f, 0.75f), Wall);
        AddBox("LeftWall", new Vector3(-19f, 7f, -3f), new Vector3(0.75f, 21f, 36f), Wall);
        AddBox("RightWall", new Vector3(19f, 7f, -3f), new Vector3(0.75f, 21f, 36f), Wall);
        AddBox("Ceiling", new Vector3(0f, 16.8f, -3f), new Vector3(38f, 0.7f, 38f), new Color(0.032f, 0.025f, 0.029f));

        for (int x = -16; x <= 16; x += 4)
            AddBox($"BackBeam_{x}", new Vector3(x, 7f, -20.55f), new Vector3(0.38f, 20f, 0.42f), WoodDark);

        AddBox("BackCrossBeamA", new Vector3(0f, 4.4f, -20.5f), new Vector3(36f, .42f, .42f), WoodDark);
        AddBox("BackCrossBeamB", new Vector3(0f, 11.6f, -20.5f), new Vector3(36f, .48f, .48f), WoodDark);

        Spawn("shelf", new Vector3(-12.5f, -2.9f, -19.8f), 1.25f);
        Spawn("shelf", new Vector3(12.5f, -2.9f, -19.8f), 1.25f);

        for (int i = 0; i < 4; i++)
        {
            Spawn("barrel", new Vector3(-16.4f, -2.9f, -15.0f + i * 3.2f), 1.1f);
            Spawn("barrel", new Vector3(16.4f, -2.9f, -14.0f + i * 3.4f), 1.0f);
        }

        AddBanner(new Vector3(-7.2f, 7.5f, -20.05f), Blue);
        AddBanner(new Vector3(7.2f, 7.5f, -20.05f), Red);
        AddLantern(new Vector3(-12f, 7.0f, -19.4f), "LanternLeft");
        AddLantern(new Vector3(12f, 7.0f, -19.4f), "LanternRight");

        AddBox("WeaponRack", new Vector3(-16.8f, 4.0f, -19.7f), new Vector3(2.7f, 5.4f, .28f), WoodDark);
        for (int i = 0; i < 3; i++)
            AddRotatedBox($"RackWeapon_{i}", new Vector3(-17.5f + i * .7f, 4.0f, -19.25f), new Vector3(.13f, 4.3f, .13f), Iron, new Vector3(0f, 0f, -14f + i * 14f));
    }

    private void BuildWarTable()
    {
        AddBox("WarTable", new Vector3(0f, -0.28f, -3.1f), new Vector3(30f, 1.0f, 27f), Wood);
        AddBox("NearTrim", new Vector3(0f, 0.25f, 10.2f), new Vector3(30.4f, .58f, .65f), WoodLight);
        AddBox("FarTrim", new Vector3(0f, 0.25f, -16.4f), new Vector3(30.4f, .58f, .65f), WoodLight);
        AddBox("LeftTrim", new Vector3(-14.75f, 0.25f, -3.1f), new Vector3(.65f, .58f, 26f), WoodLight);
        AddBox("RightTrim", new Vector3(14.75f, 0.25f, -3.1f), new Vector3(.65f, .58f, 26f), WoodLight);

        AddBox("BoardBase", new Vector3(0f, 0.42f, -5.0f), new Vector3(22.8f, .30f, 18.2f), GrassDark);
        AddBox("BattleSurface", new Vector3(0f, 0.60f, -5.0f), new Vector3(22.0f, .10f, 17.4f), Grass);
    }

    private void BuildBattlefield()
    {
        BuildRiver();
        BuildRoad();
        BuildBridge();

        BuildCastle(new Vector3(0f, 0.68f, 1.15f), false, .43f);
        BuildCastle(new Vector3(0f, 0.68f, -11.55f), true, .46f);

        BuildForest(new Vector3(-8.4f, 0.68f, -2.8f), 5, 1.40f);
        BuildForest(new Vector3(8.2f, 0.68f, -6.4f), 5, 1.36f);
        BuildForest(new Vector3(-8.1f, 0.68f, -10.0f), 3, 1.30f);

        Spawn("spearman", new Vector3(-3.2f, 0.72f, -1.8f), .59f);
        Spawn("archer", new Vector3(-1.0f, 0.72f, -3.2f), .59f);
        Spawn("swordsman", new Vector3(2.2f, 0.72f, -2.1f), .59f);
        Spawn("catapult", new Vector3(5.1f, 0.72f, -3.3f), .50f);

        Spawn("spearman", new Vector3(3.0f, 0.72f, -8.4f), .58f, new Vector3(0f, 180f, 0f));
        Spawn("archer", new Vector3(.8f, 0.72f, -9.2f), .58f, new Vector3(0f, 180f, 0f));
        Spawn("swordsman", new Vector3(-2.7f, 0.72f, -8.2f), .58f, new Vector3(0f, 180f, 0f));
    }

    private void BuildCastle(Vector3 origin, bool enemy, float scale)
    {
        Vector3 rotation = enemy ? new Vector3(0f, 180f, 0f) : Vector3.Zero;

        Spawn("castle_gatehouse", origin, scale, rotation);
        Spawn("castle_wall", origin + new Vector3(-3.0f, 0f, .12f), scale, rotation);
        Spawn("castle_wall", origin + new Vector3(3.0f, 0f, .12f), scale, rotation);
        Spawn("castle_tower", origin + new Vector3(-4.75f, 0f, .12f), scale, rotation);
        Spawn("castle_tower", origin + new Vector3(4.75f, 0f, .12f), scale, rotation);
    }

    private void BuildForest(Vector3 origin, int count, float spacing)
    {
        for (int i = 0; i < count; i++)
        {
            float x = origin.X + ((i % 3) - 1) * spacing;
            float z = origin.Z + (i / 3) * spacing;
            float scale = .55f + (i % 2) * .07f;
            Spawn("oak_tree", new Vector3(x, origin.Y, z), scale, new Vector3(0f, i * 37f, 0f));
        }
    }

    private void BuildRiver()
    {
        AddRotatedBox("RiverA", new Vector3(-5.7f, .67f, -2.0f), new Vector3(2.15f, .06f, 4.7f), River, new Vector3(0f, 11f, 0f));
        AddRotatedBox("RiverB", new Vector3(-5.1f, .67f, -5.9f), new Vector3(2.15f, .06f, 4.0f), River, new Vector3(0f, -10f, 0f));
        AddRotatedBox("RiverC", new Vector3(-5.6f, .67f, -9.6f), new Vector3(2.15f, .06f, 3.7f), River, new Vector3(0f, 8f, 0f));
    }

    private void BuildRoad()
    {
        AddRotatedBox("RoadA", new Vector3(.2f, .68f, -2.4f), new Vector3(2.1f, .045f, 4.0f), Road, new Vector3(0f, -5f, 0f));
        AddRotatedBox("RoadB", new Vector3(-.2f, .68f, -6.0f), new Vector3(1.9f, .045f, 3.7f), Road, new Vector3(0f, 8f, 0f));
        AddRotatedBox("RoadC", new Vector3(.1f, .68f, -9.2f), new Vector3(1.75f, .045f, 2.7f), Road, new Vector3(0f, -7f, 0f));
    }

    private void BuildBridge()
    {
        for (int i = 0; i < 8; i++)
            AddRotatedBox($"BridgePlank_{i}", new Vector3(-6.22f + i * .33f, .82f, -5.05f), new Vector3(.28f, .14f, 2.45f), i % 2 == 0 ? WoodLight : Wood, new Vector3(0f, 7f, 0f));
    }

    private void BuildPlayerArea()
    {
        AddBox("ReserveTray", new Vector3(-9.5f, .50f, 7.05f), new Vector3(6.5f, .30f, 3.15f), WoodDark);
        AddBox("ReserveInset", new Vector3(-9.5f, .68f, 7.05f), new Vector3(6.0f, .08f, 2.65f), new Color(.035f, .027f, .025f));

        Spawn("spearman", new Vector3(-11.2f, .70f, 7.0f), .74f);
        Spawn("spearman", new Vector3(-9.5f, .70f, 7.0f), .74f);
        Spawn("archer", new Vector3(-7.8f, .70f, 7.0f), .74f);

        for (int i = 0; i < 5; i++)
        {
            float x = -3.7f + i * 1.85f;
            AddRotatedBox($"Card_{i}", new Vector3(x, .68f, 7.55f), new Vector3(1.45f, .10f, 2.15f), i == 2 ? new Color(.17f, .25f, .20f) : Parchment, new Vector3(-5f, 0f, (i - 2) * 2.6f));
            AddBox($"CardInset_{i}", new Vector3(x, .75f, 7.28f), new Vector3(.95f, .035f, 1.20f), i == 2 ? Blue : new Color(.27f, .085f, .040f));
        }

        AddBox("Deck", new Vector3(6.8f, .83f, 7.25f), new Vector3(2.25f, .60f, 3.1f), WoodDark);
        AddBox("DeckTop", new Vector3(6.8f, 1.16f, 7.25f), new Vector3(2.05f, .06f, 2.9f), Parchment);

        for (int i = 0; i < 5; i++)
            AddRotatedBox($"Mana_{i}", new Vector3(9.5f + i * .55f, .86f, 6.6f + (i % 2) * .30f), new Vector3(.38f, .28f, .48f), new Color(.055f, .20f, .66f), new Vector3(15f, i * 18f, 15f));
    }

    private void BuildOpponent()
    {
        Vector3 basePos = new(0f, 0f, -18.0f);

        AddCapsule("OpponentTorso", basePos + new Vector3(0f, 4.7f, 0f), 1.55f, 4.5f, Shirt, Vector3.Zero);
        AddSphere("OpponentChest", basePos + new Vector3(0f, 5.35f, .08f), new Vector3(2.15f, .70f, 1.25f), Shirt);
        AddSphere("OpponentHead", basePos + new Vector3(0f, 8.0f, .25f), new Vector3(1.28f, 1.48f, 1.12f), Skin);
        AddSphere("OpponentHair", basePos + new Vector3(0f, 8.75f, .10f), new Vector3(1.34f, .58f, 1.18f), new Color(.045f, .025f, .018f));
        AddSphere("OpponentNose", basePos + new Vector3(0f, 7.95f, 1.22f), new Vector3(.18f, .22f, .28f), Skin);

        AddCapsule("UpperArmL", basePos + new Vector3(-2.25f, 4.8f, .45f), .48f, 3.15f, Shirt, new Vector3(0f, 0f, -52f));
        AddCapsule("UpperArmR", basePos + new Vector3(2.25f, 4.8f, .45f), .48f, 3.15f, Shirt, new Vector3(0f, 0f, 52f));
        AddCapsule("ForearmL", basePos + new Vector3(-3.25f, 2.8f, 1.75f), .42f, 3.0f, Skin, new Vector3(58f, 0f, -20f));
        AddCapsule("ForearmR", basePos + new Vector3(3.25f, 2.8f, 1.75f), .42f, 3.0f, Skin, new Vector3(58f, 0f, 20f));
        AddSphere("HandL", basePos + new Vector3(-3.65f, 1.62f, 3.0f), new Vector3(.55f, .32f, .72f), Skin);
        AddSphere("HandR", basePos + new Vector3(3.65f, 1.62f, 3.0f), new Vector3(.55f, .32f, .72f), Skin);
    }

    private void BuildLighting()
    {
        var coolFill = new DirectionalLight3D
        {
            Name = "CoolFill",
            RotationDegrees = new Vector3(-48f, -24f, 0f),
            LightColor = new Color(.48f, .58f, .82f),
            LightEnergy = 1.38f,
            ShadowEnabled = true
        };
        AddChild(coolFill);

        AddWarmLight("PlayerFire", new Vector3(-10f, 7.5f, 8f), 4.8f, 23f);
        AddWarmLight("EnemyFire", new Vector3(10f, 7f, -11f), 3.8f, 20f);
        AddWarmLight("OpponentKey", new Vector3(-2f, 10f, -14f), 4.6f, 17f);
        AddCoolLight("TableFill", new Vector3(0f, 7.5f, 5f), 2.5f, 24f);
        AddWarmLight("LanternLeftGlow", new Vector3(-12f, 7.0f, -18.6f), 1.9f, 10f);
        AddWarmLight("LanternRightGlow", new Vector3(12f, 7.0f, -18.6f), 1.9f, 10f);
    }

    private void AddWarmLight(string name, Vector3 position, float energy, float range)
    {
        var light = new OmniLight3D
        {
            Name = name,
            Position = position,
            LightColor = new Color(1f, .50f, .23f),
            LightEnergy = energy,
            OmniRange = range,
            ShadowEnabled = true
        };
        AddChild(light);
    }

    private void AddCoolLight(string name, Vector3 position, float energy, float range)
    {
        var light = new OmniLight3D
        {
            Name = name,
            Position = position,
            LightColor = new Color(.38f, .50f, .80f),
            LightEnergy = energy,
            OmniRange = range,
            ShadowEnabled = false
        };
        AddChild(light);
    }

    private void AddLantern(Vector3 position, string name)
    {
        AddBox(name + "Frame", position, new Vector3(.55f, 1.1f, .55f), Iron);
        AddBox(name + "Glow", position, new Vector3(.24f, .48f, .24f), new Color(1f, .32f, .06f), true);
    }

    private void AddBanner(Vector3 position, Color color)
    {
        AddBox("BannerPole", position + new Vector3(0f, 1.65f, 0f), new Vector3(2.6f, .10f, .10f), Iron);
        AddBox("Banner", position, new Vector3(2.1f, 2.9f, .12f), color);
    }

    private void BuildCamera()
    {
        var camera = new Camera3D
        {
            Name = "PlayerCamera",
            Position = new Vector3(0f, 7.2f, 21.4f),
            Fov = 54f,
            Current = true
        };
        AddChild(camera);
        camera.LookAt(new Vector3(0f, 1.75f, -5.4f), Vector3.Up);
    }

    private Node3D Spawn(string name, Vector3 position, float scale, Vector3? rotation = null)
    {
        if (!AssetLibrary.Exists(name))
            return null;

        return AssetLibrary.Spawn(name, this, position, Vector3.One * scale, rotation ?? Vector3.Zero);
    }

    private void AddBox(string name, Vector3 position, Vector3 size, Color color, bool emissive = false)
    {
        var material = MakeMaterial(color, emissive);
        var mesh = new MeshInstance3D
        {
            Name = name,
            Position = position,
            Mesh = new BoxMesh { Size = size },
            MaterialOverride = material
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

    private void AddCapsule(string name, Vector3 position, float radius, float height, Color color, Vector3 rotationDegrees)
    {
        var mesh = new MeshInstance3D
        {
            Name = name,
            Position = position,
            RotationDegrees = rotationDegrees,
            Mesh = new CapsuleMesh { Radius = radius, Height = height },
            MaterialOverride = MakeMaterial(color)
        };
        AddChild(mesh);
    }

    private StandardMaterial3D MakeMaterial(Color color, bool emissive = false)
    {
        var material = new StandardMaterial3D
        {
            AlbedoColor = color,
            Roughness = emissive ? .35f : .92f
        };

        if (emissive)
        {
            material.EmissionEnabled = true;
            material.Emission = color;
            material.EmissionEnergyMultiplier = 4.0f;
        }

        return material;
    }
}
