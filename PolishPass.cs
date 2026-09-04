using Godot;
using System;

public partial class PolishPass : Node3D
{
    private int _frames;
    private bool _built;

    private static readonly Color Stone = new(0.34f, 0.33f, 0.31f);
    private static readonly Color StoneDark = new(0.17f, 0.18f, 0.18f);
    private static readonly Color StoneLight = new(0.47f, 0.44f, 0.39f);
    private static readonly Color Wood = new(0.20f, 0.085f, 0.030f);
    private static readonly Color WoodDark = new(0.075f, 0.028f, 0.014f);
    private static readonly Color WoodLight = new(0.34f, 0.155f, 0.055f);
    private static readonly Color Iron = new(0.055f, 0.060f, 0.070f);
    private static readonly Color Brass = new(0.36f, 0.19f, 0.055f);
    private static readonly Color GrassA = new(0.085f, 0.145f, 0.055f);
    private static readonly Color GrassB = new(0.13f, 0.205f, 0.075f);
    private static readonly Color Dirt = new(0.24f, 0.155f, 0.075f);
    private static readonly Color River = new(0.055f, 0.20f, 0.31f);
    private static readonly Color Red = new(0.40f, 0.045f, 0.030f);
    private static readonly Color Blue = new(0.050f, 0.12f, 0.37f);
    private static readonly Color Parchment = new(0.60f, 0.43f, 0.24f);

    public override void _Process(double delta)
    {
        if (_built)
            return;

        _frames++;
        if (_frames < 2)
            return;

        _built = true;
        BuildOpponentHero();
        BuildBattlefieldMicroDetail();
        BuildCastleMicroDetail();
        BuildTabletopMicroDetail();
        BuildBackWallFocalDetail();
        BuildFarPlayerArea();
        BuildPolishLights();
    }

    private void BuildOpponentHero()
    {
        Node game = GetParent();
        Node3D oldTorso = game?.GetNodeOrNull<Node3D>("OpponentTorso");

        if (AssetLibrary.Exists("opponent"))
        {
            Node3D hero = AssetLibrary.Spawn(
                "opponent",
                this,
                new Vector3(0f, -0.05f, -16.25f),
                Vector3.One * 1.30f,
                Vector3.Zero);

            if (hero != null)
            {
                hero.Name = "OpponentHeroVisible";
                if (oldTorso != null)
                    HideOldOpponent(game);
                return;
            }
        }

        // If the authored asset is unavailable for any reason, restore the blockout
        // instead of leaving the opponent completely absent.
        if (oldTorso != null)
            ShowOldOpponent(game);
    }

    private void HideOldOpponent(Node game)
    {
        string[] names =
        {
            "OpponentTorso", "OpponentChest", "OpponentHead", "OpponentHair", "OpponentNose",
            "UpperArmL", "UpperArmR", "ForearmL", "ForearmR", "HandL", "HandR"
        };

        foreach (string name in names)
        {
            Node3D node = game.GetNodeOrNull<Node3D>(name);
            if (node != null)
                node.Visible = false;
        }
    }

    private void ShowOldOpponent(Node game)
    {
        string[] names =
        {
            "OpponentTorso", "OpponentChest", "OpponentHead", "OpponentHair", "OpponentNose",
            "UpperArmL", "UpperArmR", "ForearmL", "ForearmR", "HandL", "HandR"
        };

        foreach (string name in names)
        {
            Node3D node = game.GetNodeOrNull<Node3D>(name);
            if (node != null)
                node.Visible = true;
        }
    }

    private void BuildBattlefieldMicroDetail()
    {
        // Low hills and uneven ground so the board no longer reads as one flat slab.
        Vector3[] hills =
        {
            new(-8.5f, .54f, -4.4f), new(7.9f, .54f, -3.3f),
            new(-7.7f, .54f, -8.7f), new(7.3f, .54f, -10.2f),
            new(4.5f, .54f, -6.6f), new(-3.8f, .54f, -7.1f)
        };

        for (int i = 0; i < hills.Length; i++)
        {
            AddSphere(
                $"GroundMound_{i}",
                hills[i],
                new Vector3(1.3f + (i % 2) * .35f, .22f + (i % 3) * .05f, 1.0f + (i % 2) * .30f),
                i % 2 == 0 ? GrassA : GrassB);
        }

        // Fine grass tufts. The crossed blades read well from the seated camera.
        for (int i = 0; i < 44; i++)
        {
            float x = -9.5f + ((i * 37) % 190) / 10f;
            float z = -12.1f + ((i * 53) % 145) / 10f;

            // Keep the central road and castles comparatively clear.
            if (Mathf.Abs(x) < 1.25f)
                x += x >= 0 ? 1.8f : -1.8f;

            Color c = i % 3 == 0 ? GrassB : GrassA;
            float h = .22f + (i % 4) * .045f;
            AddRotatedBox($"GrassBladeA_{i}", new Vector3(x, .79f + h * .5f, z), new Vector3(.035f, h, .035f), c, new Vector3(0f, 0f, -12f));
            AddRotatedBox($"GrassBladeB_{i}", new Vector3(x + .06f, .79f + h * .45f, z + .02f), new Vector3(.030f, h * .90f, .030f), c, new Vector3(0f, 0f, 14f));
        }

        // Pebbles and rubble distributed around the field.
        for (int i = 0; i < 36; i++)
        {
            float x = -9.2f + ((i * 71) % 184) / 10f;
            float z = -11.8f + ((i * 43) % 142) / 10f;
            Vector3 s = new(.08f + (i % 4) * .025f, .035f + (i % 3) * .015f, .07f + (i % 5) * .018f);
            AddSphere($"FieldPebble_{i}", new Vector3(x, .73f, z), s, i % 4 == 0 ? StoneLight : StoneDark);
        }

        // River highlights give the water a layered surface instead of a single blue strip.
        for (int i = 0; i < 16; i++)
        {
            float z = -1.5f - i * .55f;
            float x = -5.35f + Mathf.Sin(i * .82f) * .42f;
            AddRotatedBox($"WaterGlint_{i}", new Vector3(x, .725f, z), new Vector3(.72f, .012f, .055f), River.Lightened(.30f), new Vector3(0f, (i % 2 == 0 ? 15f : -18f), 0f));
        }

        // Road ruts and scattered dirt patches.
        for (int i = 0; i < 18; i++)
        {
            float z = -1.0f - i * .62f;
            float x = (i % 2 == 0 ? -.42f : .46f) + Mathf.Sin(i) * .10f;
            AddRotatedBox($"RoadRut_{i}", new Vector3(x, .714f, z), new Vector3(.18f, .012f, .72f), Dirt.Darkened(.20f), new Vector3(0f, (i % 3 - 1) * 8f, 0f));
        }

        // More authored clusters concentrated where they are visible from camera.
        Vector3[] detailRocks =
        {
            new(-9.1f,.70f,-1.5f), new(-6.8f,.70f,-4.2f), new(-8.4f,.70f,-7.1f),
            new(8.7f,.70f,-2.0f), new(6.4f,.70f,-5.5f), new(8.6f,.70f,-9.4f),
            new(-4.2f,.70f,-11.4f), new(4.3f,.70f,-11.2f)
        };
        for (int i = 0; i < detailRocks.Length; i++)
            Spawn("rock_cluster", detailRocks[i], .30f + (i % 3) * .045f, new Vector3(0f, i * 29f, 0f));

        Vector3[] detailBushes =
        {
            new(-8.8f,.70f,-3.2f), new(-6.2f,.70f,-6.0f), new(-7.4f,.70f,-10.7f),
            new(8.2f,.70f,-3.8f), new(6.8f,.70f,-7.2f), new(8.0f,.70f,-11.1f)
        };
        for (int i = 0; i < detailBushes.Length; i++)
            Spawn("bush_cluster", detailBushes[i], .38f + (i % 2) * .05f, new Vector3(0f, i * 47f, 0f));
    }

    private void BuildCastleMicroDetail()
    {
        // Warm gate / tower points make both fortifications feel inhabited.
        Vector3[] torchPositions =
        {
            new(-.72f,1.95f,1.05f), new(.72f,1.95f,1.05f),
            new(-4.65f,2.35f,1.05f), new(4.65f,2.35f,1.05f),
            new(-.72f,2.0f,-11.45f), new(.72f,2.0f,-11.45f),
            new(-4.85f,2.45f,-11.45f), new(4.85f,2.45f,-11.45f)
        };

        for (int i = 0; i < torchPositions.Length; i++)
        {
            AddSphere($"CastleTorch_{i}", torchPositions[i], new Vector3(.065f,.10f,.065f), new Color(1f,.27f,.035f), true);
        }

        AddWarmLight("NearCastleGlow", new Vector3(0f,2.3f,1.8f), 1.2f, 5.0f);
        AddWarmLight("FarCastleGlow", new Vector3(0f,2.4f,-11.1f), 1.0f, 4.5f);

        // Small flags on flank towers.
        AddFlag("NearFlagL", new Vector3(-4.75f,3.85f,1.10f), Blue);
        AddFlag("NearFlagR", new Vector3(4.75f,3.85f,1.10f), Blue);
        AddFlag("FarFlagL", new Vector3(-4.75f,4.0f,-11.52f), Red);
        AddFlag("FarFlagR", new Vector3(4.75f,4.0f,-11.52f), Red);
    }

    private void BuildTabletopMicroDetail()
    {
        // Quill, ink pot, wax seals and loose coins near the player's hand.
        AddSphere("InkPot", new Vector3(4.0f,.86f,8.8f), new Vector3(.20f,.18f,.20f), Iron);
        AddRotatedBox("QuillShaft", new Vector3(3.35f,.90f,8.65f), new Vector3(.055f,.055f,1.65f), StoneLight, new Vector3(3f,31f,6f));
        AddRotatedBox("QuillFeatherA", new Vector3(2.95f,.96f,8.30f), new Vector3(.32f,.035f,.78f), new Color(.46f,.42f,.34f), new Vector3(3f,31f,18f));

        for (int i = 0; i < 6; i++)
        {
            float x = 5.0f + (i % 3) * .35f;
            float z = 8.45f + (i / 3) * .33f;
            AddSphere($"LooseCoin_{i}", new Vector3(x,.80f + (i%2)*.025f,z), new Vector3(.14f,.035f,.14f), Brass);
        }

        for (int i = 0; i < 3; i++)
        {
            float x = -1.1f + i * 1.10f;
            AddSphere($"WaxSeal_{i}", new Vector3(x,.84f,8.83f), new Vector3(.18f,.035f,.18f), i == 1 ? Blue : Red);
        }

        // Raised card corners / tiny metal studs make the five command cards feel physical.
        for (int card = 0; card < 5; card++)
        {
            float x = -3.7f + card * 1.85f;
            for (int corner = 0; corner < 4; corner++)
            {
                float sx = corner % 2 == 0 ? -.54f : .54f;
                float sz = corner < 2 ? -.82f : .82f;
                AddSphere($"CardStud_{card}_{corner}", new Vector3(x + sx,.845f,7.55f + sz), new Vector3(.045f,.025f,.045f), Brass);
            }
        }

        // More mana shards rather than a single neat row.
        for (int i = 0; i < 9; i++)
        {
            float x = 9.0f + (i % 5) * .47f;
            float z = 7.20f + (i / 5) * .52f + (i % 2) * .12f;
            AddRotatedBox($"ManaShardExtra_{i}", new Vector3(x,.90f,z), new Vector3(.16f,.34f,.16f), Blue.Lightened(.20f), new Vector3(18f,i*23f,12f));
        }

        // A row of brass nails along the reserve tray and deck corners.
        for (int i = 0; i < 8; i++)
        {
            AddSphere($"ReserveNail_{i}", new Vector3(-12.0f + i*.72f,.84f,8.32f), new Vector3(.055f,.025f,.055f), Brass);
        }
    }

    private void BuildBackWallFocalDetail()
    {
        // Central heraldic wall composition directly in the player's sightline.
        AddBox("CentralPlaque", new Vector3(0f,8.2f,-20.06f), new Vector3(4.3f,5.1f,.16f), WoodDark);
        AddBox("CentralPlaqueInset", new Vector3(0f,8.2f,-19.94f), new Vector3(3.65f,4.45f,.08f), new Color(.095f,.055f,.045f));
        AddSphere("CentralShield", new Vector3(0f,8.45f,-19.76f), new Vector3(1.20f,1.35f,.16f), Red);
        AddBox("ShieldStripeV", new Vector3(0f,8.45f,-19.58f), new Vector3(.23f,2.18f,.10f), StoneLight);
        AddBox("ShieldStripeH", new Vector3(0f,8.45f,-19.56f), new Vector3(1.95f,.23f,.10f), StoneLight);

        // Crossed weapon silhouettes beside the shield.
        AddRotatedBox("WallSwordL", new Vector3(-1.45f,8.35f,-19.62f), new Vector3(.12f,3.4f,.10f), Iron, new Vector3(0f,0f,-34f));
        AddRotatedBox("WallSwordR", new Vector3(1.45f,8.35f,-19.62f), new Vector3(.12f,3.4f,.10f), Iron, new Vector3(0f,0f,34f));
        AddRotatedBox("WallGuardL", new Vector3(-.93f,7.70f,-19.54f), new Vector3(.70f,.10f,.10f), Brass, new Vector3(0f,0f,-34f));
        AddRotatedBox("WallGuardR", new Vector3(.93f,7.70f,-19.54f), new Vector3(.70f,.10f,.10f), Brass, new Vector3(0f,0f,34f));

        // Additional sconces visible in the central wall bays.
        for (int i = 0; i < 4; i++)
        {
            float x = -8.5f + i * 5.7f;
            AddBox($"WallSconceBracket_{i}", new Vector3(x,6.0f,-19.72f), new Vector3(.12f,.55f,.24f), Iron);
            AddSphere($"WallSconceFlame_{i}", new Vector3(x,6.45f,-19.60f), new Vector3(.09f,.16f,.09f), new Color(1f,.28f,.04f), true);
        }

        AddWarmLight("CentralWallWarmth", new Vector3(0f,8.2f,-16.7f), 1.25f, 10f);
    }

    private void BuildFarPlayerArea()
    {
        // Opponent command hand and reserves so the far side mirrors the player's physical setup.
        for (int i = 0; i < 5; i++)
        {
            float x = -3.4f + i * 1.7f;
            AddRotatedBox($"EnemyCard_{i}", new Vector3(x,.72f,-14.45f), new Vector3(1.28f,.08f,1.85f), Parchment.Darkened(.12f), new Vector3(4f,180f,(i-2)*2f));
            AddBox($"EnemyCardInset_{i}", new Vector3(x,.77f,-14.25f), new Vector3(.84f,.025f,1.05f), Red);
        }

        AddBox("EnemyReserveTray", new Vector3(8.9f,.50f,-14.65f), new Vector3(5.1f,.26f,2.2f), WoodDark);
        AddBox("EnemyReserveFelt", new Vector3(8.9f,.66f,-14.65f), new Vector3(4.75f,.04f,1.85f), new Color(.055f,.025f,.028f));
        Spawn("spearman", new Vector3(7.6f,.68f,-14.6f), .58f, new Vector3(0f,180f,0f));
        Spawn("archer", new Vector3(8.9f,.68f,-14.6f), .58f, new Vector3(0f,180f,0f));
        Spawn("swordsman", new Vector3(10.2f,.68f,-14.6f), .58f, new Vector3(0f,180f,0f));
    }

    private void BuildPolishLights()
    {
        AddCoolLight("BattlefieldPolishFill", new Vector3(0f,5.0f,-4.0f), 1.1f, 15f);
        AddWarmLight("ForegroundDeskGlow", new Vector3(7.0f,3.0f,7.0f), .85f, 7.5f);
    }

    private Node3D Spawn(string name, Vector3 position, float scale, Vector3? rotation = null)
    {
        if (!AssetLibrary.Exists(name))
            return null;

        return AssetLibrary.Spawn(name, this, position, Vector3.One * scale, rotation ?? Vector3.Zero);
    }

    private void AddFlag(string name, Vector3 position, Color color)
    {
        AddBox(name + "Pole", position + new Vector3(0f,.55f,0f), new Vector3(.05f,1.35f,.05f), Iron);
        AddBox(name + "Cloth", position + new Vector3(.26f,.68f,0f), new Vector3(.52f,.62f,.05f), color);
    }

    private void AddWarmLight(string name, Vector3 position, float energy, float range)
    {
        var light = new OmniLight3D
        {
            Name = name,
            Position = position,
            LightColor = new Color(1f,.48f,.20f),
            LightEnergy = energy,
            OmniRange = range,
            ShadowEnabled = false
        };
        AddChild(light);
    }

    private void AddCoolLight(string name, Vector3 position, float energy, float range)
    {
        var light = new OmniLight3D
        {
            Name = name,
            Position = position,
            LightColor = new Color(.40f,.54f,.82f),
            LightEnergy = energy,
            OmniRange = range,
            ShadowEnabled = false
        };
        AddChild(light);
    }

    private void AddBox(string name, Vector3 position, Vector3 size, Color color, bool emissive = false)
    {
        var mesh = new MeshInstance3D
        {
            Name = name,
            Position = position,
            Mesh = new BoxMesh { Size = size },
            MaterialOverride = MakeMaterial(color, emissive)
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

    private void AddSphere(string name, Vector3 position, Vector3 scale, Color color, bool emissive = false)
    {
        var mesh = new MeshInstance3D
        {
            Name = name,
            Position = position,
            Scale = scale,
            Mesh = new SphereMesh { Radius = 1f, Height = 2f },
            MaterialOverride = MakeMaterial(color, emissive)
        };
        AddChild(mesh);
    }

    private StandardMaterial3D MakeMaterial(Color color, bool emissive = false)
    {
        var material = new StandardMaterial3D
        {
            AlbedoColor = color,
            Roughness = emissive ? .32f : .94f
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
