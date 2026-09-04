using Godot;

public partial class HeroOverridePass : Node3D
{
    private int _frames;
    private bool _done;

    public override void _Process(double delta)
    {
        if (_done)
            return;

        _frames++;
        if (_frames < 2)
            return;

        _done = true;
        ReplaceProceduralTable();
    }

    private void ReplaceProceduralTable()
    {
        Node game = GetParent();
        if (game == null || !AssetLibrary.Exists("hero_table"))
            return;

        string[] names =
        {
            "WarTableBody", "WarTableTop", "NearRail", "FarRail", "LeftRail", "RightRail",
            "BoardWell", "BoardFrameNear", "BoardFrameFar", "BoardFrameLeft", "BoardFrameRight"
        };

        foreach (string name in names)
        {
            Node3D node = game.GetNodeOrNull<Node3D>(name);
            if (node != null)
                node.Visible = false;
        }

        for (int i = 0; i < 4; i++)
        {
            Node3D plate = game.GetNodeOrNull<Node3D>($"CornerPlate_{i}");
            Node3D rivet = game.GetNodeOrNull<Node3D>($"CornerRivet_{i}");
            if (plate != null) plate.Visible = false;
            if (rivet != null) rivet.Visible = false;
        }

        for (int i = 0; i < 15; i++)
        {
            Node3D rivet = game.GetNodeOrNull<Node3D>($"NearRivet_{i}");
            if (rivet != null) rivet.Visible = false;
        }

        AssetLibrary.Spawn(
            "hero_table",
            game,
            new Vector3(0f, -0.32f, -3.10f),
            Vector3.One,
            Vector3.Zero);
    }
}
