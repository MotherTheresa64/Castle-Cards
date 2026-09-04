using Godot;

public partial class CinematicCameraController : Node3D
{
    private Camera3D _camera;
    private Vector3 _focus = new(0f, 1.15f, -4.75f);
    private Vector3 _homeFocus;
    private float _distance = 20.0f;
    private float _homeDistance;
    private float _yaw;
    private float _pitch = Mathf.DegToRad(27.0f);
    private float _homeYaw;
    private float _homePitch;
    private bool _orbiting;

    private const float OrbitSensitivity = 0.0042f;
    private const float PanSpeed = 5.2f;
    private const float ZoomStep = 1.25f;
    private const float MinDistance = 11.5f;
    private const float MaxDistance = 28.0f;
    private static readonly float MinPitch = Mathf.DegToRad(15.0f);
    private static readonly float MaxPitch = Mathf.DegToRad(53.0f);

    public void Configure(Camera3D camera, Vector3 focus, float distance, float yawDegrees = 0f, float pitchDegrees = 27f)
    {
        _camera = camera;
        _focus = focus;
        _distance = distance;
        _yaw = Mathf.DegToRad(yawDegrees);
        _pitch = Mathf.DegToRad(pitchDegrees);

        _homeFocus = _focus;
        _homeDistance = _distance;
        _homeYaw = _yaw;
        _homePitch = _pitch;
        ApplyCameraTransform();
    }

    public override void _Process(double delta)
    {
        if (_camera == null)
            return;

        float dt = (float)delta;
        Vector3 input = Vector3.Zero;

        if (Input.IsKeyPressed(Key.W)) input.Z -= 1f;
        if (Input.IsKeyPressed(Key.S)) input.Z += 1f;
        if (Input.IsKeyPressed(Key.A)) input.X -= 1f;
        if (Input.IsKeyPressed(Key.D)) input.X += 1f;

        if (input.LengthSquared() > 0f)
        {
            input = input.Normalized();
            float speed = PanSpeed * (_distance / 20f);
            Vector3 forward = new(-Mathf.Sin(_yaw), 0f, -Mathf.Cos(_yaw));
            Vector3 right = new(Mathf.Cos(_yaw), 0f, -Mathf.Sin(_yaw));
            _focus += (right * input.X + forward * input.Z) * speed * dt;
            ClampFocus();
            ApplyCameraTransform();
        }
    }

    public override void _UnhandledInput(InputEvent @event)
    {
        if (_camera == null)
            return;

        if (@event is InputEventMouseButton mouse)
        {
            if (mouse.ButtonIndex == MouseButton.Right)
            {
                _orbiting = mouse.Pressed;
                Input.MouseMode = _orbiting ? Input.MouseModeEnum.Captured : Input.MouseModeEnum.Visible;
                GetViewport().SetInputAsHandled();
                return;
            }

            if (mouse.Pressed && mouse.ButtonIndex == MouseButton.WheelUp)
            {
                _distance = Mathf.Max(MinDistance, _distance - ZoomStep);
                ApplyCameraTransform();
                GetViewport().SetInputAsHandled();
                return;
            }

            if (mouse.Pressed && mouse.ButtonIndex == MouseButton.WheelDown)
            {
                _distance = Mathf.Min(MaxDistance, _distance + ZoomStep);
                ApplyCameraTransform();
                GetViewport().SetInputAsHandled();
                return;
            }
        }

        if (@event is InputEventMouseMotion motion && _orbiting)
        {
            _yaw -= motion.Relative.X * OrbitSensitivity;
            _pitch = Mathf.Clamp(_pitch - motion.Relative.Y * OrbitSensitivity, MinPitch, MaxPitch);
            ApplyCameraTransform();
            GetViewport().SetInputAsHandled();
            return;
        }

        if (@event is InputEventKey key && key.Pressed && !key.Echo)
        {
            if (key.Keycode == Key.F)
            {
                ResetView();
                GetViewport().SetInputAsHandled();
            }
            else if (key.Keycode == Key.Escape && _orbiting)
            {
                _orbiting = false;
                Input.MouseMode = Input.MouseModeEnum.Visible;
                GetViewport().SetInputAsHandled();
            }
        }
    }

    private void ResetView()
    {
        _focus = _homeFocus;
        _distance = _homeDistance;
        _yaw = _homeYaw;
        _pitch = _homePitch;
        ApplyCameraTransform();
    }

    private void ClampFocus()
    {
        _focus.X = Mathf.Clamp(_focus.X, -5.5f, 5.5f);
        _focus.Z = Mathf.Clamp(_focus.Z, -8.8f, -0.2f);
        _focus.Y = Mathf.Clamp(_focus.Y, 0.85f, 2.2f);
    }

    private void ApplyCameraTransform()
    {
        if (_camera == null)
            return;

        float horizontal = Mathf.Cos(_pitch) * _distance;
        Vector3 offset = new(
            Mathf.Sin(_yaw) * horizontal,
            Mathf.Sin(_pitch) * _distance,
            Mathf.Cos(_yaw) * horizontal);

        _camera.GlobalPosition = _focus + offset;
        _camera.LookAt(_focus, Vector3.Up);
    }
}
