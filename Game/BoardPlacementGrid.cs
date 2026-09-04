using Godot;

public partial class BoardPlacementGrid : Node3D
{
    [Signal]
    public delegate void CellSelectedEventHandler(Vector2I cell);

    public const int Columns = 13;
    public const int Rows = 8;
    public const float CellSize = 1.35f;
    public const float GridY = 0.805f;
    public const float MinX = -8.775f;
    public const float MinZ = -9.95f;

    private static readonly Color HoverColor = new(0.72f, 0.52f, 0.20f, .72f);
    private static readonly Color SelectedColor = new(0.95f, 0.72f, 0.28f, .92f);

    private Camera3D _camera;
    private Node3D _hoverOutline;
    private Node3D _selectedOutline;
    private bool _placementEnabled = true;

    public override void _Ready()
    {
        // The battlefield is intentionally gridless at rest. Gameplay cells are still present
        // mathematically; only the cell under the cursor (and the selected cell) is visualized.
        _hoverOutline = CreateCellOutline("HoverCell", HoverColor, .026f);
        _selectedOutline = CreateCellOutline("SelectedCell", SelectedColor, .042f);
        _hoverOutline.Visible = false;
        _selectedOutline.Visible = false;
        _camera = GetViewport().GetCamera3D();
    }

    public override void _Process(double delta)
    {
        if (!_placementEnabled)
        {
            if (_hoverOutline != null)
                _hoverOutline.Visible = false;
            return;
        }

        _camera ??= GetViewport().GetCamera3D();
        if (_camera == null)
            return;

        if (TryGetCellAtScreen(GetViewport().GetMousePosition(), out Vector2I cell))
        {
            MoveOutline(_hoverOutline, cell);
            _hoverOutline.Visible = true;
        }
        else
        {
            _hoverOutline.Visible = false;
        }
    }

    public override void _UnhandledInput(InputEvent @event)
    {
        if (!_placementEnabled || _camera == null)
            return;

        if (@event is InputEventMouseButton mouse &&
            mouse.ButtonIndex == MouseButton.Left &&
            mouse.Pressed &&
            TryGetCellAtScreen(mouse.Position, out Vector2I cell))
        {
            MoveOutline(_selectedOutline, cell);
            _selectedOutline.Visible = true;
            EmitSignal(SignalName.CellSelected, cell);
        }
    }

    public void SetPlacementEnabled(bool enabled)
    {
        _placementEnabled = enabled;
        if (!enabled && _hoverOutline != null)
            _hoverOutline.Visible = false;
    }

    public Vector3 GetCellCenter(Vector2I cell)
    {
        int col = Mathf.Clamp(cell.X, 0, Columns - 1);
        int row = Mathf.Clamp(cell.Y, 0, Rows - 1);
        return new Vector3(
            MinX + (col + .5f) * CellSize,
            GridY,
            MinZ + (row + .5f) * CellSize);
    }

    public bool IsPlayerDeploymentCell(Vector2I cell) => IsInside(cell) && cell.Y >= Rows - 2;
    public bool IsEnemyDeploymentCell(Vector2I cell) => IsInside(cell) && cell.Y <= 1;

    public bool IsInside(Vector2I cell)
    {
        return cell.X >= 0 && cell.X < Columns && cell.Y >= 0 && cell.Y < Rows;
    }

    public bool TryWorldToCell(Vector3 worldPosition, out Vector2I cell)
    {
        int col = (int)Mathf.Floor((worldPosition.X - MinX) / CellSize);
        int row = (int)Mathf.Floor((worldPosition.Z - MinZ) / CellSize);
        cell = new Vector2I(col, row);
        return IsInside(cell);
    }

    private bool TryGetCellAtScreen(Vector2 screenPosition, out Vector2I cell)
    {
        cell = new Vector2I(-1, -1);
        Vector3 origin = _camera.ProjectRayOrigin(screenPosition);
        Vector3 direction = _camera.ProjectRayNormal(screenPosition);

        if (Mathf.Abs(direction.Y) < .0001f)
            return false;

        float distance = (GridY - origin.Y) / direction.Y;
        if (distance <= 0f)
            return false;

        Vector3 hit = origin + direction * distance;
        return TryWorldToCell(hit, out cell);
    }

    private Node3D CreateCellOutline(string name, Color color, float thickness)
    {
        var root = new Node3D { Name = name };
        AddChild(root);

        float half = CellSize * .5f;
        float y = GridY + .030f;
        AddLine($"{name}_Top", new Vector3(0f, y, -half), new Vector3(CellSize, .020f, thickness), color, root);
        AddLine($"{name}_Bottom", new Vector3(0f, y, half), new Vector3(CellSize, .020f, thickness), color, root);
        AddLine($"{name}_Left", new Vector3(-half, y, 0f), new Vector3(thickness, .020f, CellSize), color, root);
        AddLine($"{name}_Right", new Vector3(half, y, 0f), new Vector3(thickness, .020f, CellSize), color, root);
        return root;
    }

    private void MoveOutline(Node3D outline, Vector2I cell)
    {
        Vector3 center = GetCellCenter(cell);
        outline.Position = new Vector3(center.X, 0f, center.Z);
    }

    private void AddLine(string name, Vector3 position, Vector3 size, Color color, Node parent)
    {
        var material = new StandardMaterial3D
        {
            AlbedoColor = color,
            Roughness = .55f,
            Transparency = BaseMaterial3D.TransparencyEnum.Alpha,
            EmissionEnabled = true,
            Emission = new Color(color.R, color.G, color.B)
        };

        var mesh = new MeshInstance3D
        {
            Name = name,
            Position = position,
            Mesh = new BoxMesh { Size = size },
            MaterialOverride = material
        };
        parent.AddChild(mesh);
    }
}
