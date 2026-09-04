using Godot;

public partial class GameBuilder
{
    // Shared colors also used by the other detail partial.
    private static readonly Color Stone = new(0.34f, 0.33f, 0.31f);
    private static readonly Color StoneDark = new(0.17f, 0.18f, 0.18f);
    private static readonly Color Leather = new(0.16f, 0.055f, 0.020f);

    private bool _designDetailBuilt;
    private int _designDetailFrames;

    public override void _PhysicsProcess(double delta)
    {
        if (_designDetailBuilt)
            return;

        _designDetailFrames++;
        if (_designDetailFrames < 3)
            return;

        _designDetailBuilt = true;
        BuildDesignDrivenPass();
    }

    private void BuildDesignDrivenPass()
    {
        BuildKingAndCastleGameplayDetails();
        BuildBattlefieldGameplayDetails();
        BuildReinforcementAndSpellDetails();
        BuildCheatAndKarmaDetails();
        BuildRunMapWallProp();
        BuildDesignHudDetails();
    }

    private void BuildKingAndCastleGameplayDetails()
    {
        // The design says the match ends when the king dies, so both kings physically exist
        // inside their castles instead of castle health being the only representation.
        Spawn("throne", new Vector3(0f, .70f, .18f), .28f, new Vector3(0f, 180f, 0f));
        Spawn("king", new Vector3(0f, .72f, .58f), .38f, new Vector3(0f, 180f, 0f));
        Spawn("royal_guard", new Vector3(-1.15f, .72f, .40f), .34f, new Vector3(0f, 170f, 0f));
        Spawn("royal_guard", new Vector3(1.15f, .72f, .40f), .34f, new Vector3(0f, 190f, 0f));

        Spawn("throne", new Vector3(0f, .70f, -10.72f), .29f);
        Spawn("king", new Vector3(0f, .72f, -10.38f), .37f);
        Spawn("royal_guard", new Vector3(-1.15f, .72f, -10.58f), .34f, new Vector3(0f, -8f, 0f));
        Spawn("royal_guard", new Vector3(1.15f, .72f, -10.58f), .34f, new Vector3(0f, 8f, 0f));

        // Defensive upgrade language: castle braziers, upgrade sockets and trap approaches.
        Spawn("castle_brazier", new Vector3(-1.85f, .70f, 1.20f), .36f);
        Spawn("castle_brazier", new Vector3(1.85f, .70f, 1.20f), .36f);
        Spawn("castle_brazier", new Vector3(-1.85f, .70f, -11.35f), .34f);
        Spawn("castle_brazier", new Vector3(1.85f, .70f, -11.35f), .34f);

        Spawn("trap_spikes", new Vector3(-3.55f, .70f, -.25f), .31f, new Vector3(0f, 16f, 0f));
        Spawn("trap_spikes", new Vector3(3.55f, .70f, -9.55f), .30f, new Vector3(0f, 196f, 0f));

        // Empty sockets telegraph that castle/terrain upgrades can physically change the board.
        Vector3[] playerSockets =
        {
            new(-4.55f,.735f,1.75f), new(4.55f,.735f,1.75f),
            new(-5.00f,.735f,.35f), new(5.00f,.735f,.35f)
        };
        Vector3[] enemySockets =
        {
            new(-4.55f,.735f,-12.0f), new(4.55f,.735f,-12.0f),
            new(-5.00f,.735f,-10.6f), new(5.00f,.735f,-10.6f)
        };

        for (int i = 0; i < playerSockets.Length; i++)
        {
            AddSphere($"PlayerUpgradeSocket_{i}", playerSockets[i], new Vector3(.25f,.035f,.25f), StoneDark);
            AddSphere($"PlayerSocketRim_{i}", playerSockets[i] + new Vector3(0f,.025f,0f), new Vector3(.16f,.025f,.16f), WoodLight);
            AddSphere($"EnemyUpgradeSocket_{i}", enemySockets[i], new Vector3(.25f,.035f,.25f), StoneDark);
            AddSphere($"EnemySocketRim_{i}", enemySockets[i] + new Vector3(0f,.025f,0f), new Vector3(.16f,.025f,.16f), Red);
        }
    }

    private void BuildBattlefieldGameplayDetails()
    {
        // Reinforcement structures make the limited reinforcement system visible on-board.
        Spawn("reinforcement_outpost", new Vector3(-8.15f, .70f, -.65f), .35f, new Vector3(0f, 18f, 0f));
        Spawn("reinforcement_outpost", new Vector3(8.10f, .70f, -10.45f), .34f, new Vector3(0f, 198f, 0f));

        // Siege escalation / defense progression.
        Spawn("trebuchet", new Vector3(-6.15f, .72f, -3.45f), .39f, new Vector3(0f, 12f, 0f));
        Spawn("trebuchet", new Vector3(6.35f, .72f, -8.10f), .37f, new Vector3(0f, 190f, 0f));

        // Unit paths that reflect the document's strategies: brute force, magic support and assassination.
        Spawn("wizard", new Vector3(-2.45f, .72f, -4.45f), .50f, new Vector3(0f, -8f, 0f));
        Spawn("assassin", new Vector3(3.25f, .72f, -6.65f), .46f, new Vector3(0f, 168f, 0f));
        Spawn("royal_guard", new Vector3(.65f, .72f, -6.25f), .43f, new Vector3(0f, 182f, 0f));

        // Active spell aftermath. These are physical board effects, matching spells that alter terrain.
        Spawn("fireball_scorch", new Vector3(3.75f, .70f, -5.35f), .47f, new Vector3(0f, 21f, 0f));
        Spawn("healing_rune", new Vector3(-3.35f, .705f, -4.05f), .48f, new Vector3(0f, -12f, 0f));

        // Scorched trees around the fireball zone give the terrain consequence more weight.
        for (int i = 0; i < 6; i++)
        {
            float x = 3.05f + (i % 3) * .48f;
            float z = -4.55f - (i / 3) * .70f;
            AddRotatedBox($"BurntBranch_{i}", new Vector3(x,.82f,z), new Vector3(.10f,.85f,.10f), StoneDark,
                new Vector3((i%2==0?15f:-12f), 0f, (i-2)*9f));
        }

        // Additional battlefield rubble clustered around siege lanes.
        for (int i = 0; i < 18; i++)
        {
            float x = -7.1f + (i % 6) * 2.75f;
            float z = -2.1f - (i / 6) * 3.35f;
            AddSphere($"GameplayRubble_{i}", new Vector3(x,.72f,z),
                new Vector3(.10f + (i%3)*.035f,.055f,.09f + (i%2)*.025f),
                i%4==0 ? Stone : StoneDark);
        }
    }

    private void BuildReinforcementAndSpellDetails()
    {
        // The visible reserve system should feel like an inventory of physical miniatures.
        Spawn("reinforcement_cart", new Vector3(-5.95f, .70f, 8.65f), .72f, new Vector3(0f, 90f, 0f));
        Spawn("reinforcement_cart", new Vector3(7.15f, .70f, -14.75f), .47f, new Vector3(0f, -90f, 0f));

        // Spellcasting tools occupy their own physical portion of the player's table.
        Spawn("spellbook_open", new Vector3(7.85f, .72f, 8.95f), .78f, new Vector3(0f, -8f, 0f));
        Spawn("mana_crystals", new Vector3(10.10f, .72f, 8.45f), .84f, new Vector3(0f, 19f, 0f));

        // A few spare miniatures near the cart make reinforcement count legible without UI alone.
        Spawn("swordsman", new Vector3(-6.55f, .72f, 7.65f), .55f);
        Spawn("archer", new Vector3(-5.75f, .72f, 7.70f), .55f);
        Spawn("wizard", new Vector3(-4.90f, .72f, 7.62f), .50f);

        // Upgrade category totem: defense / troops / spells / terrain.
        Spawn("upgrade_totem", new Vector3(-12.55f, .72f, 8.85f), .72f, new Vector3(0f, 15f, 0f));
    }

    private void BuildCheatAndKarmaDetails()
    {
        // Cheating is a core mechanic, so it has physical table language instead of only a meter.
        Spawn("suspicion_dial", new Vector3(11.35f, .72f, 9.18f), .78f, new Vector3(0f, -7f, 0f));
        Spawn("karma_medallion", new Vector3(9.95f, .72f, 9.45f), .74f, new Vector3(0f, 12f, 0f));
        Spawn("cheat_stash", new Vector3(5.15f, .47f, 9.50f), .63f, new Vector3(0f, 0f, 0f));

        // The opponent can cheat too: a less-visible stash on their side of the table.
        Spawn("cheat_stash", new Vector3(-6.9f, .44f, -15.25f), .42f, new Vector3(0f, 180f, 0f));
    }

    private void BuildRunMapWallProp()
    {
        // Physical route map based on the branching area structure in the design document.
        Color mapWood = new(.105f,.045f,.020f);
        Color mapParchment = new(.33f,.245f,.14f);
        Color route = new(.41f,.21f,.07f);

        AddBox("RunMapFrame", new Vector3(-12.2f, 8.25f, -19.72f), new Vector3(6.2f, 5.0f, .22f), mapWood);
        AddBox("RunMapSurface", new Vector3(-12.2f, 8.25f, -19.56f), new Vector3(5.65f, 4.45f, .08f), mapParchment);

        Vector3[] nodes =
        {
            new(-14.25f,7.10f,-19.45f),
            new(-13.25f,8.05f,-19.45f), new(-13.25f,6.20f,-19.45f),
            new(-12.10f,8.70f,-19.45f), new(-12.10f,7.30f,-19.45f), new(-12.10f,5.70f,-19.45f),
            new(-10.85f,8.15f,-19.45f), new(-10.10f,7.05f,-19.45f)
        };

        for (int i = 0; i < nodes.Length; i++)
        {
            Color c = i == 0 ? Blue : (i == nodes.Length-1 ? Red : route);
            AddSphere($"RunMapNode_{i}", nodes[i], new Vector3(.16f,.16f,.07f), c);
        }

        // Stylized connecting route bars.
        AddRotatedBox("RunRouteA", new Vector3(-13.72f,7.58f,-19.46f), new Vector3(.08f,1.42f,.04f), route, new Vector3(0f,0f,-45f));
        AddRotatedBox("RunRouteB", new Vector3(-13.72f,6.63f,-19.46f), new Vector3(.08f,1.42f,.04f), route, new Vector3(0f,0f,45f));
        AddRotatedBox("RunRouteC", new Vector3(-12.68f,8.38f,-19.46f), new Vector3(.08f,1.20f,.04f), route, new Vector3(0f,0f,-55f));
        AddRotatedBox("RunRouteD", new Vector3(-12.68f,7.66f,-19.46f), new Vector3(.08f,1.18f,.04f), route, new Vector3(0f,0f,42f));
        AddRotatedBox("RunRouteE", new Vector3(-12.68f,6.52f,-19.46f), new Vector3(.08f,1.32f,.04f), route, new Vector3(0f,0f,-40f));
        AddRotatedBox("RunRouteF", new Vector3(-11.48f,8.40f,-19.46f), new Vector3(.08f,1.35f,.04f), route, new Vector3(0f,0f,62f));
        AddRotatedBox("RunRouteG", new Vector3(-10.48f,7.58f,-19.46f), new Vector3(.08f,1.32f,.04f), route, new Vector3(0f,0f,34f));
    }

    private void BuildDesignHudDetails()
    {
        var layer = new CanvasLayer { Name = "DesignHUD" };
        AddChild(layer);

        AddDesignLabel(layer, "TACTICAL COMMANDER", new Vector2(1040, 82), 13, new Color(.85f,.69f,.55f));
        AddDesignLabel(layer, "KARMA  HONORABLE", new Vector2(1030, 600), 13, new Color(.66f,.91f,.66f));
        AddDesignLabel(layer, "REINFORCEMENTS  3", new Vector2(42, 636), 13, new Color(.75f,.78f,.84f));
        AddDesignLabel(layer, "CHEAT RISK  LOW", new Vector2(1030, 620), 12, new Color(.94f,.66f,.39f));
    }

    private void AddDesignLabel(CanvasLayer layer, string text, Vector2 position, int fontSize, Color color)
    {
        var label = new Label
        {
            Text = text,
            Position = position,
            Modulate = color,
            MouseFilter = Control.MouseFilterEnum.Ignore
        };
        label.AddThemeFontSizeOverride("font_size", fontSize);
        layer.AddChild(label);
    }
}
