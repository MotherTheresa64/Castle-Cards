using Godot;

public partial class ReferenceQualityDirector : Node
{
    public override void _Ready()
    {
        CallDeferred(nameof(ApplyReferencePass));
    }

    private void ApplyReferencePass()
    {
        if (GetParent() is not Node3D root)
            return;

        ReframeCamera(root);
        RebalanceEnvironment(root);
        RebalanceHeroScale(root);
        AddReferenceFillLights(root);
        HideDebugPresentation(root);
    }

    private static void ReframeCamera(Node3D root)
    {
        var rig = root.GetNodeOrNull<CinematicCameraController>("CinematicCameraRig");
        if (rig == null)
            return;

        var camera = rig.GetNodeOrNull<Camera3D>("PlayerCamera");
        if (camera == null)
            return;

        // The approved reference shows the physical table edge, reserve miniatures, cards and
        // resource tray. Pulling back and lowering the pitch restores that seated-table framing.
        camera.Fov = 49.0f;
        rig.Configure(camera, new Vector3(0f, 1.02f, -4.55f), 24.35f, 0f, 23.5f);
    }

    private static void RebalanceEnvironment(Node3D root)
    {
        var world = root.GetNodeOrNull<WorldEnvironment>("WorldEnvironment");
        var environment = world?.Environment;
        if (environment == null)
            return;

        // Keep the room cinematic-dark while lifting enough shadow detail to read stone, wood,
        // faces and the miniature silhouettes. The previous pass crushed too much into black.
        environment.AmbientLightColor = new Color(.27f, .285f, .33f);
        environment.AmbientLightEnergy = .46f;
        environment.Set("tonemap_exposure", 1.48f);
        environment.Set("tonemap_agx_contrast", 1.12f);
        environment.Set("ssao_intensity", 2.35f);
        environment.Set("ssao_power", 1.22f);
        environment.Set("ssil_intensity", .82f);
        environment.Set("glow_intensity", .095f);
        environment.Set("glow_bloom", .028f);
        environment.Set("fog_density", .00072f);
        environment.Set("fog_light_energy", .22f);
    }

    private static void RebalanceHeroScale(Node3D root)
    {
        // Spawned GLBs are direct children of GameBuilder. Identify the three large hero pieces
        // by authored spawn location so this pass stays independent of imported GLB root names.
        Node3D playerCastle = FindDirectNodeNear(root, new Vector3(0f, .795f, 1.18f), .20f);
        if (playerCastle != null)
        {
            playerCastle.Scale = Vector3.One * .555f;
            playerCastle.Position = new Vector3(0f, .795f, 1.05f);
        }

        Node3D enemyCastle = FindDirectNodeNear(root, new Vector3(0f, .795f, -11.08f), .22f);
        if (enemyCastle != null)
        {
            enemyCastle.Scale = Vector3.One * .305f;
            enemyCastle.Position = new Vector3(0f, .795f, -10.95f);
        }

        Node3D opponent = FindDirectNodeNear(root, new Vector3(0f, -2.22f, -14.55f), .35f);
        if (opponent != null)
        {
            opponent.Scale = Vector3.One * 1.44f;
            opponent.Position = new Vector3(0f, -2.28f, -14.72f);
        }
    }

    private static Node3D FindDirectNodeNear(Node3D root, Vector3 target, float tolerance)
    {
        Node3D best = null;
        float bestDistance = tolerance;
        foreach (Node child in root.GetChildren())
        {
            if (child is not Node3D node)
                continue;

            float distance = node.Position.DistanceTo(target);
            if (distance < bestDistance)
            {
                best = node;
                bestDistance = distance;
            }
        }
        return best;
    }

    private static void AddReferenceFillLights(Node3D root)
    {
        if (root.HasNode("ReferencePlayerEdgeFill"))
            return;

        AddOmni(root, "ReferencePlayerEdgeFill", new Vector3(0f, 3.35f, 6.35f),
            new Color(1f, .50f, .22f), .82f, 9.0f, false);
        AddOmni(root, "ReferenceBoardCoolFill", new Vector3(-7.6f, 5.3f, -2.3f),
            new Color(.34f, .43f, .58f), .52f, 12.5f, false);
        AddOmni(root, "ReferenceOpponentRim", new Vector3(4.5f, 6.1f, -13.8f),
            new Color(1f, .42f, .14f), 1.05f, 7.8f, true);
        AddOmni(root, "ReferenceOpponentCoolFace", new Vector3(-3.1f, 5.0f, -12.3f),
            new Color(.42f, .52f, .69f), .58f, 7.0f, false);
    }

    private static void AddOmni(Node3D root, string name, Vector3 position, Color color,
        float energy, float range, bool shadows)
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
        root.AddChild(light);
    }

    private static void HideDebugPresentation(Node3D root)
    {
        var hud = root.GetNodeOrNull<CanvasLayer>("HUD");
        if (hud == null)
            return;

        foreach (Node node in hud.FindChildren("*", "Label", true, false))
        {
            if (node is Label label &&
                (label.Text.Contains("RMB LOOK") || label.Text.Contains("WHEEL ZOOM")))
            {
                label.Visible = false;
            }
        }
    }
}
