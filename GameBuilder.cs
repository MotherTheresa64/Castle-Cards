using Godot;

public partial class GameBuilder : Node3D
{
    private static readonly Color WoodDark = new(0.075f, 0.028f, 0.012f);
    private static readonly Color Wood = new(0.19f, 0.075f, 0.025f);
    private static readonly Color WoodLight = new(0.31f, 0.14f, 0.045f);
    private static readonly Color Wall = new(0.055f, 0.046f, 0.050f);
    private static readonly Color Iron = new(0.055f, 0.060f, 0.070f);
    private static readonly Color Grass = new(0.085f, 0.145f, 0.065f);
    private static readonly Color GrassDark = new(0.038f, 0.072f, 0.035f);
    private static readonly Color River = new(0.035f, 0.125f, 0.19f);
    private static readonly Color Road = new(0.265f, 0.185f, 0.105f);
    private static readonly Color Parchment = new(0.49f, 0.31f, 0.15f);
    private static readonly Color Blue = new(0.045f, 0.10f, 0.30f);
    private static readonly Color Red = new(0.31f, 0.035f, 0.025f);
    private static readonly Color Skin = new(0.52f, 0.30f, 0.19f);

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
            BackgroundColor = new Color(0.008f, 0.007f, 0.010f),
            AmbientLightSource = Environment.AmbientSource.Color,
            AmbientLightColor = new Color(0.28f, 0.30f, 0.39f),
            AmbientLightEnergy = 0.95f
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
        AddBox("Ceiling", new Vector3(0f, 16.8f, -3f), new Vector3(38f, 0.7f, 38f), new Color(0.035f,0.025f,0.026f));

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
    }

    private void BuildWarTable()
    {
        AddBox("WarTable", new Vector3(0f, -0.28f, -3.1f), new Vector3(30f, 1.0f, 27f), Wood);
        AddBox("NearTrim", new Vector3(0f, 0.25f, 10.2f), new Vector3(30.4f, .58f, .65f), WoodLight);
        AddBox("FarTrim", new Vector3(0f, 0.25f, -16.4f), new Vector3(30.4f, .58f, .65f), WoodLight);
        AddBox("LeftTrim", new Vector3(-14.75f, 0.25f, -3.1f), new Vector3(.65f, .58f, 26f), WoodLight);
        AddBox("RightTrim", new Vector3(14.75f, 0.25f, -3.1f), new Vector3(.65f, .58f, 26f), WoodLight);

        AddBox("BoardBase", new Vector3(0f, 0.42f, -4.8f), new Vector3(22.8f, .30f, 18.4f), GrassDark);
        AddBox("BattleSurface", new Vector3(0f, 0.60f, -4.8f), new Vector3(22.0f, .10f, 17.6f), Grass);
    }

    private void BuildBattlefield()
    {
        BuildRiver();
        BuildRoad();
        BuildBridge();

        BuildCastle(new Vector3(0f, 0.68f, 1.55f), false);
        BuildCastle(new Vector3(0f, 0.68f, -11.15f), true);

        BuildForest(new Vector3(-8.3f, 0.68f, -2.3f), 5, 1.45f);
        BuildForest(new Vector3(8.0f, 0.68f, -6.7f), 5, 1.40f);
        BuildForest(new Vector3(-7.8f, 0.68f, -10.2f), 3, 1.35f);

        Spawn("spearman", new Vector3(-3.4f, 0.72f, -1.0f), .68f);
        Spawn("archer", new Vector3(-1.2f, 0.72f, -2.6f), .68f);
        Spawn("swordsman", new Vector3(2.4f, 0.72f, -1.5f), .68f);
        Spawn("catapult", new Vector3(5.3f, 0.72f, -2.7f), .58f);

        Spawn("spearman", new Vector3(3.0f, 0.72f, -8.2f), .66f, new Vector3(0f,180f,0f));
        Spawn("archer", new Vector3(1.0f, 0.72f, -9.0f), .66f, new Vector3(0f,180f,0f));
        Spawn("swordsman", new Vector3(-2.7f, 0.72f, -8.0f), .66f, new Vector3(0f,180f,0f));
    }

    private void BuildCastle(Vector3 origin, bool enemy)
    {
        Vector3 rotation = enemy ? new Vector3(0f, 180f, 0f) : Vector3.Zero;
        float s = .62f;

        Spawn("castle_gatehouse", origin, s, rotation);
        Spawn("castle_wall", origin + new Vector3(-4.2f,0f,.15f), s, rotation);
        Spawn("castle_wall", origin + new Vector3(4.2f,0f,.15f), s, rotation);
        Spawn("castle_tower", origin + new Vector3(-6.0f,0f,.15f), s, rotation);
        Spawn("castle_tower", origin + new Vector3(6.0f,0f,.15f), s, rotation);
    }

    private void BuildForest(Vector3 origin, int count, float spacing)
    {
        for (int i = 0; i < count; i++)
        {
            float x = origin.X + ((i % 3) - 1) * spacing;
            float z = origin.Z + (i / 3) * spacing;
            float scale = .62f + (i % 2) * .08f;
            Spawn("oak_tree", new Vector3(x, origin.Y, z), scale, new Vector3(0f, i * 37f, 0f));
        }
    }

    private void BuildRiver()
    {
        AddRotatedBox("RiverA", new Vector3(-5.7f,.67f,-1.7f), new Vector3(2.2f,.06f,5.1f), River, new Vector3(0f,11f,0f));
        AddRotatedBox("RiverB", new Vector3(-5.1f,.67f,-5.7f), new Vector3(2.2f,.06f,4.3f), River, new Vector3(0f,-10f,0f));
        AddRotatedBox("RiverC", new Vector3(-5.6f,.67f,-9.7f), new Vector3(2.2f,.06f,4.2f), River, new Vector3(0f,8f,0f));
    }

    private void BuildRoad()
    {
        AddRotatedBox("RoadA", new Vector3(.2f,.68f,-2.3f), new Vector3(2.2f,.045f,4.4f), Road, new Vector3(0f,-5f,0f));
        AddRotatedBox("RoadB", new Vector3(-.2f,.68f,-6.1f), new Vector3(2.0f,.045f,4.0f), Road, new Vector3(0f,8f,0f));
        AddRotatedBox("RoadC", new Vector3(.1f,.68f,-9.3f), new Vector3(1.85f,.045f,2.8f), Road, new Vector3(0f,-7f,0f));
    }

    private void BuildBridge()
    {
        for (int i = 0; i < 8; i++)
        {
            AddRotatedBox($"BridgePlank_{i}", new Vector3(-6.22f + i*.33f, .82f, -5.05f), new Vector3(.28f,.14f,2.45f), i%2==0 ? WoodLight : Wood, new Vector3(0f,7f,0f));
        }
    }

    private void BuildPlayerArea()
    {
        AddBox("ReserveTray", new Vector3(-9.6f,.50f,7.1f), new Vector3(6.5f,.30f,3.15f), WoodDark);
        AddBox("ReserveInset", new Vector3(-9.6f,.68f,7.1f), new Vector3(6.0f,.08f,2.65f), new Color(.035f,.027f,.025f));

        Spawn("spearman", new Vector3(-11.3f,.70f,7.0f), .80f);
        Spawn("spearman", new Vector3(-9.6f,.70f,7.0f), .80f);
        Spawn("archer", new Vector3(-7.9f,.70f,7.0f), .80f);

        for (int i = 0; i < 5; i++)
        {
            float x = -3.7f + i*1.85f;
            AddRotatedBox($"Card_{i}", new Vector3(x,.68f,7.55f), new Vector3(1.45f,.10f,2.15f), i==2 ? new Color(.17f,.25f,.20f) : Parchment, new Vector3(-4f,0f,(i-2)*2.2f));
            AddBox($"CardInset_{i}", new Vector3(x,.75f,7.30f), new Vector3(.95f,.035f,1.25f), i==2 ? Blue : new Color(.25f,.09f,.045f));
        }

        AddBox("Deck", new Vector3(6.8f,.83f,7.25f), new Vector3(2.25f,.60f,3.1f), WoodDark);
        AddBox("DeckTop", new Vector3(6.8f,1.16f,7.25f), new Vector3(2.05f,.06f,2.9f), Parchment);

        for (int i = 0; i < 5; i++)
            AddRotatedBox($"Mana_{i}", new Vector3(9.5f+i*.55f,.86f,6.6f+(i%2)*.30f), new Vector3(.38f,.28f,.48f), new Color(.055f,.18f,.58f), new Vector3(15f,i*18f,15f));
    }

    private void BuildOpponent()
    {
        Vector3 basePos = new(0f, 0f, -17.3f);
        AddBox("OpponentTorso", basePos + new Vector3(0f,4.0f,0f), new Vector3(4.7f,5.0f,2.1f), new Color(.085f,.055f,.065f));
        AddBox("OpponentShoulders", basePos + new Vector3(0f,5.7f,.05f), new Vector3(5.7f,1.1f,2.4f), new Color(.075f,.045f,.055f));
        AddBox("OpponentHead", basePos + new Vector3(0f,7.4f,.20f), new Vector3(2.15f,2.35f,1.75f), Skin);
        AddBox("OpponentHair", basePos + new Vector3(0f,8.25f,.05f), new Vector3(2.35f,.85f,1.92f), new Color(.055f,.028f,.018f));
        AddRotatedBox("OpponentArmL", basePos + new Vector3(-3.2f,3.5f,1.0f), new Vector3(1.2f,4.2f,1.15f), Skin, new Vector3(24f,0f,-24f));
        AddRotatedBox("OpponentArmR", basePos + new Vector3(3.2f,3.5f,1.0f), new Vector3(1.2f,4.2f,1.15f), Skin, new Vector3(24f,0f,24f));
    }

    private void BuildLighting()
    {
        var coolFill = new DirectionalLight3D
        {
            Name = "CoolFill",
            RotationDegrees = new Vector3(-52f,-28f,0f),
            LightColor = new Color(.44f,.54f,.78f),
            LightEnergy = 1.05f,
            ShadowEnabled = true
        };
        AddChild(coolFill);

        AddWarmLight("PlayerFire", new Vector3(-10f,7.5f,8f), 7.5f, 23f);
        AddWarmLight("EnemyFire", new Vector3(10f,6.5f,-12f), 6.2f, 20f);
        AddWarmLight("BackLanternGlow", new Vector3(0f,8f,-18f), 4.2f, 18f);
    }

    private void AddWarmLight(string name, Vector3 position, float energy, float range)
    {
        var light = new OmniLight3D
        {
            Name = name,
            Position = position,
            LightColor = new Color(1f,.49f,.20f),
            LightEnergy = energy,
            OmniRange = range,
            ShadowEnabled = true
        };
        AddChild(light);
    }

    private void AddLantern(Vector3 position, string name)
    {
        AddBox(name+"Frame", position, new Vector3(.55f,1.1f,.55f), Iron);
        AddBox(name+"Glow", position, new Vector3(.24f,.48f,.24f), new Color(1f,.32f,.06f), true);
    }

    private void AddBanner(Vector3 position, Color color)
    {
        AddBox("BannerPole", position + new Vector3(0f,1.65f,0f), new Vector3(2.6f,.10f,.10f), Iron);
        AddBox("Banner", position, new Vector3(2.1f,2.9f,.12f), color);
    }

    private void BuildCamera()
    {
        var camera = new Camera3D
        {
            Name = "PlayerCamera",
            Position = new Vector3(0f, 8.1f, 20.7f),
            Fov = 58f,
            Current = true
        };
        AddChild(camera);
        camera.LookAt(new Vector3(0f, 1.9f, -4.7f), Vector3.Up);
    }

    private Node3D Spawn(string name, Vector3 position, float scale, Vector3? rotation = null)
    {
        if (!AssetLibrary.Exists(name))
            return null;

        return AssetLibrary.Spawn(name, this, position, Vector3.One * scale, rotation ?? Vector3.Zero);
    }

    private void AddBox(string name, Vector3 position, Vector3 size, Color color, bool emissive = false)
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
        var material = new StandardMaterial3D
        {
            AlbedoColor = color,
            Roughness = .92f
        };

        var mesh = new MeshInstance3D
        {
            Name = name,
            Position = position,
            RotationDegrees = rotationDegrees,
            Mesh = new BoxMesh { Size = size },
            MaterialOverride = material
        };
        AddChild(mesh);
    }
}
