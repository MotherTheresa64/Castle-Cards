using Godot;

public partial class FlickerLight : OmniLight3D
{
    public float BaseEnergy { get; set; } = 1.0f;
    public float Variation { get; set; } = 0.10f;
    public float FlickerSpeed { get; set; } = 5.0f;

    private float _time;
    private float _phase;

    public override void _Ready()
    {
        _phase = (float)GD.RandRange(0.0, 1000.0);
        LightEnergy = BaseEnergy;
    }

    public override void _Process(double delta)
    {
        _time += (float)delta;
        float primary = Mathf.Sin((_time + _phase) * FlickerSpeed);
        float secondary = Mathf.Sin((_time * 1.73f + _phase * .37f) * (FlickerSpeed * .61f));
        float flutter = primary * .62f + secondary * .38f;
        LightEnergy = BaseEnergy * (1f + flutter * Variation);
    }
}
