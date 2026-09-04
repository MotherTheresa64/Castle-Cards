using Godot;

public partial class GameBuilder : Node3D
{
    public override void _Ready()
    {
        BuildEnvironment();
        BuildTable();
        BuildBattlefield();
        BuildLighting();
        BuildCamera();
    }

    private void BuildEnvironment()
    {
        var environment = new Environment
        {
            BackgroundMode = Environment.BGMode.Color,
            BackgroundColor = new Color(0.008f, 0.010f, 0.014f),
            AmbientLightSource = Environment.AmbientSource.Color,
            AmbientLightColor = new Color(0.12f, 0.15f, 0.20f),
            AmbientLightEnergy = 0.45f
        };

        AddChild(new WorldEnvironment
        {
            Name = "WorldEnvironment",
            Environment = environment
        });
    }

    private void BuildTable()
    {
        AddBox(
            "WarTable",
            new Vector3(0f, 0f, -2f),
            new Vector3(24f, 0.8f, 22f),
            new Color(0.12f, 0.055f, 0.022f));

        AddBox(
            "BattleBoard",
            new Vector3(0f, 0.52f, -4f),
            new Vector3(19f, 0.22f, 15f),
            new Color(0.12f, 0.16f, 0.09f));
    }

    private void BuildBattlefield()
    {
        // Near-side castle placeholder.
        AddBox(
            "PlayerKeep",
            new Vector3(0f, 1.55f, 1.5f),
            new Vector3(3.2f, 2.0f, 2.2f),
            new Color(0.28f, 0.28f, 0.27f));

        // Far-side castle placeholder.
        AddBox(
            "EnemyKeep",
            new Vector3(0f, 1.55f, -9.5f),
            new Vector3(3.2f, 2.0f, 2.2f),
            new Color(0.25f, 0.24f, 0.23f));

        // Physical card/reserve placeholders in the foreground.
        for (int i = 0; i < 5; i++)
        {
            AddBox(
                $"Card_{i}",
                new Vector3(-4f + (i * 2f), 1.05f, 7.1f),
                new Vector3(1.35f, 0.10f, 2.0f),
                new Color(0.18f, 0.09f + (i * 0.015f), 0.055f));
        }
    }

    private void BuildLighting()
    {
        var coolFill = new DirectionalLight3D
        {
            Name = "CoolFill",
            RotationDegrees = new Vector3(-48f, -25f, 0f),
            LightColor = new Color(0.40f, 0.52f, 0.78f),
            LightEnergy = 0.8f,
            ShadowEnabled = true
        };

        AddChild(coolFill);

        var warmKey = new OmniLight3D
        {
            Name = "WarmKey",
            Position = new Vector3(-8f, 8f, 8f),
            LightColor = new Color(1.0f, 0.43f, 0.18f),
            LightEnergy = 5.0f,
            OmniRange = 24f,
            ShadowEnabled = true
        };

        AddChild(warmKey);

        var warmFill = new OmniLight3D
        {
            Name = "WarmFill",
            Position = new Vector3(8f, 5f, -7f),
            LightColor = new Color(1.0f, 0.68f, 0.35f),
            LightEnergy = 2.2f,
            OmniRange = 20f
        };

        AddChild(warmFill);
    }

    private void BuildCamera()
    {
        var camera = new Camera3D
        {
            Name = "PlayerCamera",
            Position = new Vector3(0f, 8.2f, 17.0f),
            Fov = 60f,
            Current = true
        };

        AddChild(camera);
        camera.LookAt(new Vector3(0f, 0.9f, -3.8f), Vector3.Up);
    }

    private void AddBox(string name, Vector3 position, Vector3 size, Color color)
    {
        var material = new StandardMaterial3D
        {
            AlbedoColor = color,
            Roughness = 0.95f
        };

        var mesh = new MeshInstance3D
        {
            Name = name,
            Position = position,
            Mesh = new BoxMesh { Size = size },
            MaterialOverride = material
        };

        AddChild(mesh);
    }
}
