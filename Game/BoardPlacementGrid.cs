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

    private static readonly Color GridColor = new(0.20f, 0.17f, 0.12f);
    private static readonly Color MajorGridColor = new(0.33f, 0.26f, 0.15f);
    private static readonly Color PlayerZoneColor = new(0.10f, 0.22f, 0.42f);
    private static readonly Color EnemyZoneColor = new(0.42f, 0.10f, 0.075f);
    private static readonly Color HoverColor = new(0.82f, 0.61f, 0.22f);
    private static readonly Color SelectedColor = new(0.95f, 0.78f, 0.36f);

    private Camera3D _camera;
    private Node3D _hoverOutline;
    private Node3D _selectedOutline;
    private Vector2I _hoverCell = new(-1, -1);
    private bool _placementEnabled = true;

    public override void _Ready()
    {
        BuildGrid();
        _hoverOutline = CreateCellOutline("HoverCell", HoverColor, .038f);
        _selectedOutline = CreateCellOutline("SelectedCell", SelectedColor, .050f);
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
            _hoverCell = cell;
            MoveOutline(_hoverOutline, cell);
            _hoverOutline.Visible = true;
        }
        else
        {
            _hoverCell = new Vector2I(-1, -1);
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

    public bool IsPlayerDeploymentCell(Vector2I cell)
    {
        return IsInside(cell) && cell.Y >= Rows - 2;
    }

    public bool IsEnemyDeploymentCell(Vector2I cell)
    {
        return IsInside(cell) && cell.Y <= 1;
    }

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

    private void BuildGrid()
    {
        float width = Columns * CellSize;
        float depth = Rows * CellSize;
        float centerX = MinX + width * .5f;
        float centerZ = MinZ + depth * .5f;

        for (int col = 0; col <= Columns; col++)
        {
            float x = MinX + col * CellSize;
            bool major = col == 0 || col == Columns || col == Columns / 2;
            AddLine(
                $"GridV_{col}",
                new Vector3(x, GridY, centerZ),
                new Vector3(major ? .042f : .024f, .018f, depth),
                major ? MajorGridColor : GridColor);
        }

        for (int row = 0; row <= Rows; row++)
        {
            float z = MinZ + row * CellSize;
            bool major = row == 0 || row == Rows || row == Rows / 2;
            AddLine(
                $"GridH_{row}",
                new Vector3(centerX, GridY, z),
                new Vector3(width, .018f, major ? .042f : .024f),
                major ? MajorGridColor : GridColor);
        }

        float enemyBoundaryZ = MinZ + 2 * CellSize;
        float playerBoundaryZ = MinZ + (Rows - 2) * CellSize;
        AddLine("EnemyDeployBoundary", new Vector3(centerX, GridY + .008f, enemyBoundaryZ), new Vector3(width, .026f, .070f), EnemyZoneColor);
        AddLine("PlayerDeployBoundary", new Vector3(centerX, GridY + .008f, playerBoundaryZ), new Vector3(width, .026f, .070f), PlayerZoneColor);

        for (int col = 0; col < Columns; col++)
        {
            for (int row = 0; row < Rows; row++)
            {
                if ((col + row) % 2 != 0)
                    continue;

                Vector3 center = GetCellCenter(new Vector2I(col, row));
                Color mark = row >= Rows - 2 ? PlayerZoneColor : (row <= 1 ? EnemyZoneColor : GridColor);
                AddLine(
                    $"GridPip_{col}_{row}",
                    new Vector3(center.X, GridY + .006f, center.Z),
                    new Vector3(.080f, .022f, .080f),
                    mark);
            }
        }
    }

    private Node3D CreateCellOutline(string name, Color color, float thickness)
    {
        var root = new Node3D { Name = name };
        AddChild(root);

        float half = CellSize * .5f;
        AddLine($"{name}_Top", new Vector3(0f, GridY + .035f, -half), new Vector3(CellSize, .030f, thickness), color, root);
        AddLine($"{name}_Bottom", new Vector3(0f, GridY + .035f, half), new Vector3(CellSize, .030f, thickness), color, root);
        AddLine($"{name}_Left", new Vector3(-half, GridY + .035f, 0f), new Vector3(thickness, .030f, CellSize), color, root);
        AddLine($"{name}_Right", new Vector3(half, GridY + .035f, 0f), new Vector3(thickness, .030f, CellSize), color, root);
        return root;
    }

    private void MoveOutline(Node3D outline, Vector2I cell)
    {
        Vector3 center = GetCellCenter(cell);
        outline.Position = new Vector3(center.X, 0f, center.Z);
    }

    private void AddLine(string name, Vector3 position, Vector3 size, Color color, Node parent = null)
    {
        var mesh = new MeshInstance3D
        {
            Name = name,
            Position = position,
            Mesh = new BoxMesh { Size = size },
            MaterialOverride = new StandardMaterial3D
            {
                AlbedoColor = color,
                Roughness = .96f
            }
        };

        (parent ?? this).AddChild(mesh);
    }
}
