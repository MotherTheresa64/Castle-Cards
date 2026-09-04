using Godot;
using System;

public partial class GameBuilder
{
    private bool _detailPassBuilt;

    public override void _Process(double delta)
    {
        if (_detailPassBuilt)
            return;

        _detailPassBuilt = true;
        BuildHighDetailPass();
    }

    private void BuildHighDetailPass()
    {
        ReplaceBlockoutOpponent();
        BuildTavernDetailPass();
        BuildBattlefieldDetailPass();
        BuildTabletopDetailPass();
        BuildAtmosphereDetailPass();
        BuildHudDetailPass();
    }

    private void ReplaceBlockoutOpponent()
    {
        string[] oldOpponentParts =
        {
            "OpponentTorso", "OpponentChest", "OpponentHead", "OpponentHair", "OpponentNose",
            "UpperArmL", "UpperArmR", "ForearmL", "ForearmR", "HandL", "HandR"
        };

        foreach (string part in oldOpponentParts)
        {
            Node3D node = GetNodeOrNull<Node3D>(part);
            if (node != null)
                node.Visible = false;
        }

        Spawn("opponent", new Vector3(0f, -0.05f, -18.15f), 1.05f);
    }

    private void BuildTavernDetailPass()
    {
        Color timber = new(0.105f, 0.040f, 0.018f);
        Color timberEdge = new(0.235f, 0.105f, 0.038f);
        Color plaster = new(0.095f, 0.075f, 0.070f);
        Color brass = new(0.32f, 0.17f, 0.055f);
        Color clothDark = new(0.11f, 0.025f, 0.030f);

        // Ceiling rafters and braces. These are intentionally dense because the seated
        // camera should feel like it is inside a real room, not floating in darkness.
        for (int i = 0; i < 9; i++)
        {
            float x = -16f + i * 4f;
            AddBox($"CeilingRafter_{i}", new Vector3(x, 15.55f, -3f), new Vector3(.42f, .48f, 34f), timber);
            AddRotatedBox($"RafterBraceL_{i}", new Vector3(x - .85f, 12.7f, -17.9f), new Vector3(.26f, 5.2f, .28f), timberEdge, new Vector3(0f, 0f, -24f));
            AddRotatedBox($"RafterBraceR_{i}", new Vector3(x + .85f, 12.7f, -17.9f), new Vector3(.26f, 5.2f, .28f), timberEdge, new Vector3(0f, 0f, 24f));
        }

        // Break up the flat back wall with inset plaster bays.
        for (int i = 0; i < 8; i++)
        {
            float x = -14f + i * 4f;
            AddBox($"PlasterBay_{i}", new Vector3(x, 8.0f, -20.17f), new Vector3(3.25f, 5.7f, .10f), plaster);
            AddBox($"PlasterBayLower_{i}", new Vector3(x, 1.7f, -20.17f), new Vector3(3.25f, 4.8f, .10f), plaster * .78f);
        }

        // Decorative iron pegs and brass caps along the beams.
        for (int i = 0; i < 17; i++)
        {
            float x = -16f + i * 2f;
            AddSphere($"BeamStudTop_{i}", new Vector3(x, 11.6f, -20.10f), new Vector3(.10f, .10f, .10f), Iron);
            AddSphere($"BeamStudMid_{i}", new Vector3(x, 4.4f, -20.10f), new Vector3(.08f, .08f, .08f), brass);
        }

        // Furniture clusters.
        Spawn("bench", new Vector3(-13.8f, -2.9f, -9.0f), 1.15f, new Vector3(0f, 90f, 0f));
        Spawn("bench", new Vector3(13.8f, -2.9f, -8.0f), 1.10f, new Vector3(0f, -90f, 0f));
        Spawn("chair", new Vector3(-10.5f, -2.9f, -15.2f), 1.0f, new Vector3(0f, 28f, 0f));
        Spawn("chair", new Vector3(10.5f, -2.9f, -15.2f), 1.0f, new Vector3(0f, -28f, 0f));
        Spawn("small_table", new Vector3(-13.5f, -2.9f, -12.4f), 1.0f);
        Spawn("small_table", new Vector3(13.5f, -2.9f, -11.8f), .96f);

        // Tables are cluttered rather than empty.
        Spawn("bottle_cluster", new Vector3(-13.7f, -1.52f, -12.4f), 1.0f, new Vector3(0f, 26f, 0f));
        Spawn("mug", new Vector3(-12.7f, -1.52f, -12.2f), .88f, new Vector3(0f, -18f, 0f));
        Spawn("book_stack", new Vector3(13.35f, -1.52f, -11.8f), .90f, new Vector3(0f, 15f, 0f));
        Spawn("candle_cluster", new Vector3(14.15f, -1.52f, -11.5f), .88f);

        // Wall displays.
        Spawn("weapon_rack", new Vector3(-15.7f, 1.1f, -19.75f), 1.05f);
        Spawn("weapon_rack", new Vector3(15.7f, 1.1f, -19.75f), 1.05f);
        Spawn("shield_decor", new Vector3(-4.3f, 6.0f, -19.95f), 1.15f);
        Spawn("shield_decor", new Vector3(4.3f, 6.0f, -19.95f), 1.15f, new Vector3(0f, 0f, 12f));
        Spawn("shield_decor", new Vector3(-10.2f, 9.7f, -19.95f), .90f);
        Spawn("shield_decor", new Vector3(10.2f, 9.7f, -19.95f), .90f);

        // Ground clutter along both walls.
        for (int i = 0; i < 4; i++)
        {
            Spawn("crate", new Vector3(-16.7f, -2.9f, -2.0f - i * 2.1f), .82f + i * .04f, new Vector3(0f, i * 17f, 0f));
            Spawn("crate", new Vector3(16.6f, -2.9f, -1.2f - i * 2.25f), .76f + i * .05f, new Vector3(0f, -i * 19f, 0f));
        }

        Spawn("skull", new Vector3(-12.4f, .35f, -19.2f), .72f, new Vector3(0f, 18f, 0f));
        Spawn("book_stack", new Vector3(12.35f, .32f, -19.1f), .75f, new Vector3(0f, -11f, 0f));
        Spawn("bottle_cluster", new Vector3(-11.5f, 2.10f, -19.15f), .74f);
        Spawn("bottle_cluster", new Vector3(11.4f, 2.10f, -19.15f), .74f, new Vector3(0f, 34f, 0f));

        // Hanging chandelier and side braziers.
        Spawn("chandelier", new Vector3(0f, 10.7f, -5.0f), 1.20f);
        Spawn("brazier", new Vector3(-17.0f, -2.9f, -12.0f), 1.15f);
        Spawn("brazier", new Vector3(17.0f, -2.9f, -11.0f), 1.15f);

        // Chains and hanging hooks.
        for (int i = 0; i < 4; i++)
        {
            float x = -6.6f + i * 4.4f;
            for (int link = 0; link < 7; link++)
            {
                float y = 15.0f - link * .42f;
                AddRotatedBox($"Chain_{i}_{link}", new Vector3(x, y, -17.6f), new Vector3(.08f, .35f, .08f), Iron, new Vector3(0f, 0f, (link % 2 == 0 ? 18f : -18f)));
            }
        }

        // A woven-looking floor runner behind the table.
        AddBox("BackRug", new Vector3(0f, -2.94f, -14.0f), new Vector3(11.0f, .035f, 3.0f), clothDark);
        for (int i = 0; i < 10; i++)
            AddBox($"RugStripe_{i}", new Vector3(-4.8f + i * 1.07f, -2.91f, -14.0f), new Vector3(.10f, .035f, 2.75f), i % 2 == 0 ? Red : brass);
    }

    private void BuildBattlefieldDetailPass()
    {
        Color moss = new(0.070f, 0.13f, 0.050f);
        Color dirt = new(0.22f, 0.145f, 0.078f);
        Color darkDirt = new(0.13f, 0.085f, 0.050f);

        // Replace the simple plank bridge visually with an authored bridge.
        for (int i = 0; i < 8; i++)
        {
            Node3D oldBridge = GetNodeOrNull<Node3D>($"BridgePlank_{i}");
            if (oldBridge != null)
                oldBridge.Visible = false;
        }
        Spawn("bridge_detail", new Vector3(-5.05f, .70f, -5.05f), .60f, new Vector3(0f, 90f, 0f));

        // Keeps make each modular castle read like a complete fortification.
        Spawn("castle_keep", new Vector3(0f, .68f, -0.45f), .34f);
        Spawn("castle_keep", new Vector3(0f, .68f, -10.1f), .36f, new Vector3(0f, 180f, 0f));

        // Terrain patches eliminate the flat green rectangle look.
        Vector3[] patches =
        {
            new(-7.2f,.675f,-1.0f), new(-4.1f,.675f,-2.7f), new(4.1f,.675f,-1.1f), new(7.2f,.675f,-2.8f),
            new(-8.0f,.675f,-5.4f), new(-2.9f,.675f,-5.4f), new(3.4f,.675f,-5.3f), new(8.2f,.675f,-5.0f),
            new(-7.0f,.675f,-8.0f), new(-3.8f,.675f,-8.8f), new(4.2f,.675f,-8.4f), new(7.5f,.675f,-9.2f),
            new(-8.1f,.675f,-11.8f), new(-4.6f,.675f,-11.5f), new(4.8f,.675f,-11.6f), new(8.1f,.675f,-11.4f)
        };

        for (int i = 0; i < patches.Length; i++)
        {
            float w = 1.35f + (i % 3) * .35f;
            float d = 1.05f + (i % 4) * .25f;
            Color c = i % 3 == 0 ? dirt : (i % 3 == 1 ? moss : darkDirt);
            AddRotatedBox($"TerrainPatch_{i}", patches[i], new Vector3(w, .025f, d), c, new Vector3(0f, (i * 23) % 90, 0f));
        }

        // Mixed vegetation instead of identical tree blobs.
        Spawn("pine_tree", new Vector3(-9.2f,.70f,-4.0f), .53f, new Vector3(0f,22f,0f));
        Spawn("pine_tree", new Vector3(9.1f,.70f,-8.7f), .49f, new Vector3(0f,-18f,0f));
        Spawn("pine_tree", new Vector3(-8.9f,.70f,-9.1f), .44f, new Vector3(0f,47f,0f));

        Vector3[] bushPositions =
        {
            new(-6.9f,.70f,-.2f), new(-7.5f,.70f,-3.7f), new(-4.0f,.70f,-4.8f), new(5.8f,.70f,-3.8f),
            new(7.2f,.70f,-4.1f), new(7.8f,.70f,-8.0f), new(-6.6f,.70f,-8.8f), new(-4.7f,.70f,-10.2f),
            new(5.9f,.70f,-10.6f), new(8.3f,.70f,-11.2f)
        };
        for (int i = 0; i < bushPositions.Length; i++)
            Spawn("bush_cluster", bushPositions[i], .52f + (i % 3) * .05f, new Vector3(0f,i*31f,0f));

        Vector3[] rockPositions =
        {
            new(-3.8f,.70f,-.5f), new(4.6f,.70f,-4.0f), new(-8.7f,.70f,-6.8f), new(8.5f,.70f,-6.1f),
            new(-2.3f,.70f,-10.9f), new(3.0f,.70f,-11.1f)
        };
        for (int i = 0; i < rockPositions.Length; i++)
            Spawn("rock_cluster", rockPositions[i], .42f + i*.02f, new Vector3(0f,i*41f,0f));

        // Fortified field edges and points of interest.
        Spawn("fence_section", new Vector3(-7.3f,.70f,-6.7f), .48f, new Vector3(0f,18f,0f));
        Spawn("fence_section", new Vector3(6.7f,.70f,-7.8f), .45f, new Vector3(0f,-21f,0f));
        Spawn("fence_section", new Vector3(5.8f,.70f,-.2f), .40f, new Vector3(0f,35f,0f));
        Spawn("ruin_wall", new Vector3(-8.0f,.70f,-6.1f), .42f, new Vector3(0f,22f,0f));
        Spawn("watchtower", new Vector3(8.4f,.70f,-10.0f), .38f, new Vector3(0f,-20f,0f));
        Spawn("tent", new Vector3(6.4f,.70f,-9.7f), .42f, new Vector3(0f,14f,0f));
        Spawn("tent", new Vector3(-6.7f,.70f,-2.1f), .38f, new Vector3(0f,-26f,0f));
        Spawn("campfire", new Vector3(5.1f,.70f,-9.8f), .46f);

        // More unit variety and siege silhouettes.
        Spawn("knight", new Vector3(4.1f,.72f,-4.7f), .53f, new Vector3(0f,-10f,0f));
        Spawn("ogre", new Vector3(-4.5f,.72f,-6.5f), .48f, new Vector3(0f,12f,0f));
        Spawn("ballista", new Vector3(-5.7f,.72f,-8.9f), .48f, new Vector3(0f,180f,0f));

        // Tiny stones around the road and riverbanks give scale to the board.
        for (int i = 0; i < 22; i++)
        {
            float z = -1.0f - i * .50f;
            float x = (i % 2 == 0 ? 1.25f : -1.35f) + ((i % 5) - 2) * .12f;
            AddSphere($"RoadStone_{i}", new Vector3(x,.72f,z), new Vector3(.12f + (i%3)*.025f,.06f,.10f), i%2==0 ? Stone : StoneDark);
        }

        for (int i = 0; i < 18; i++)
        {
            float z = -1.3f - i * .50f;
            float x = -5.45f + (i % 2 == 0 ? -1.15f : 1.15f);
            AddSphere($"RiverBankStone_{i}", new Vector3(x,.72f,z), new Vector3(.14f,.07f,.12f), StoneDark);
        }
    }

    private void BuildTabletopDetailPass()
    {
        Color felt = new(.028f,.050f,.043f);
        Color brass = new(.35f,.18f,.055f);
        Color ink = new(.11f,.035f,.025f);
        Color bone = new(.58f,.52f,.40f);

        // Decorative inset around the board.
        AddBox("BoardInnerFrameNear", new Vector3(0f,.70f,3.78f), new Vector3(22.1f,.08f,.18f), WoodLight);
        AddBox("BoardInnerFrameFar", new Vector3(0f,.70f,-13.78f), new Vector3(22.1f,.08f,.18f), WoodLight);
        AddBox("BoardInnerFrameL", new Vector3(-10.98f,.70f,-5.0f), new Vector3(.18f,.08f,17.7f), WoodLight);
        AddBox("BoardInnerFrameR", new Vector3(10.98f,.70f,-5.0f), new Vector3(.18f,.08f,17.7f), WoodLight);

        // Metal corner brackets and nail heads.
        Vector3[] corners = { new(-14.45f,.60f,9.7f), new(14.45f,.60f,9.7f), new(-14.45f,.60f,-15.95f), new(14.45f,.60f,-15.95f) };
        for (int i = 0; i < corners.Length; i++)
        {
            AddBox($"CornerBracket_{i}", corners[i], new Vector3(.75f,.12f,.75f), Iron);
            AddSphere($"CornerRivet_{i}", corners[i] + new Vector3(0f,.10f,0f), new Vector3(.11f,.06f,.11f), brass);
        }

        for (int i = 0; i < 14; i++)
        {
            float x = -12.5f + i * 1.92f;
            AddSphere($"NearTrimNail_{i}", new Vector3(x,.62f,10.18f), new Vector3(.09f,.055f,.09f), Iron);
        }

        // Reserve tray dividers and felt pads.
        for (int i = 0; i < 4; i++)
            AddBox($"ReserveDivider_{i}", new Vector3(-11.75f + i * 1.55f,.79f,7.05f), new Vector3(.08f,.22f,2.55f), WoodLight);
        AddBox("ReserveFelt", new Vector3(-9.5f,.735f,7.05f), new Vector3(5.75f,.025f,2.38f), felt);

        // Card borders, center pips and little faux text bars.
        for (int i = 0; i < 5; i++)
        {
            float x = -3.7f + i * 1.85f;
            float rot = (i - 2) * 2.6f;
            AddRotatedBox($"CardBorderTop_{i}", new Vector3(x,.80f,6.82f), new Vector3(1.20f,.025f,.055f), brass, new Vector3(-5f,0f,rot));
            AddRotatedBox($"CardBorderBottom_{i}", new Vector3(x,.80f,7.82f), new Vector3(1.20f,.025f,.055f), brass, new Vector3(-5f,0f,rot));
            AddRotatedBox($"CardTextA_{i}", new Vector3(x,.82f,7.52f), new Vector3(.70f,.022f,.05f), ink, new Vector3(-5f,0f,rot));
            AddRotatedBox($"CardTextB_{i}", new Vector3(x,.82f,7.70f), new Vector3(.52f,.022f,.04f), ink, new Vector3(-5f,0f,rot));
            AddSphere($"CardPip_{i}", new Vector3(x,.84f,7.08f), new Vector3(.12f,.035f,.12f), i==2 ? Blue : Red);
        }

        // Deck leather straps and clasp.
        AddBox("DeckStrapV", new Vector3(6.8f,1.205f,7.25f), new Vector3(.26f,.05f,2.95f), Leather);
        AddBox("DeckStrapH", new Vector3(6.8f,1.21f,7.25f), new Vector3(2.08f,.05f,.26f), Leather);
        AddBox("DeckClasp", new Vector3(6.8f,1.26f,7.25f), new Vector3(.36f,.10f,.36f), brass);

        // Player-side personal clutter.
        Spawn("dice_cluster", new Vector3(4.6f,.69f,8.65f), .80f, new Vector3(0f,25f,0f));
        Spawn("mug", new Vector3(12.6f,.70f,7.7f), 1.05f, new Vector3(0f,-20f,0f));
        Spawn("candle_cluster", new Vector3(-13.4f,.70f,8.2f), .82f);
        Spawn("book_stack", new Vector3(8.2f,.70f,9.0f), .82f, new Vector3(0f,-8f,0f));
        Spawn("skull", new Vector3(11.8f,.70f,9.2f), .65f, new Vector3(0f,22f,0f));

        // Coin / token piles.
        for (int i = 0; i < 12; i++)
        {
            float x = 8.8f + (i % 4) * .28f;
            float z = 8.35f + (i / 4) * .28f;
            AddBox($"Token_{i}", new Vector3(x,.76f + (i%2)*.035f,z), new Vector3(.22f,.055f,.22f), i%3==0 ? bone : brass);
        }

        // Small engraved-looking bars in the near trim.
        for (int i = 0; i < 9; i++)
        {
            float x = -8.0f + i * 2.0f;
            AddRotatedBox($"TrimRune_{i}", new Vector3(x,.58f,10.16f), new Vector3(.55f,.035f,.06f), brass, new Vector3(0f,(i%2==0?18f:-18f),0f));
        }
    }

    private void BuildAtmosphereDetailPass()
    {
        // More local pools of light; keep energy modest so the battlefield stays readable.
        AddWarmLight("ChandelierGlow", new Vector3(0f,11.0f,-5f), 2.1f, 13f);
        AddWarmLight("LeftBrazierGlow", new Vector3(-17f,-.8f,-12f), 1.8f, 8f);
        AddWarmLight("RightBrazierGlow", new Vector3(17f,-.8f,-11f), 1.8f, 8f);
        AddWarmLight("TableCandleGlow", new Vector3(-13.4f,2.2f,8.2f), 1.2f, 6f);
        AddWarmLight("BattleCampfireGlow", new Vector3(5.1f,2.0f,-9.8f), .8f, 5f);
        AddCoolLight("BackWallCoolLift", new Vector3(0f,10f,-17f), 1.1f, 14f);
    }

    private void BuildHudDetailPass()
    {
        var layer = new CanvasLayer { Name = "GameHUD" };
        AddChild(layer);

        AddHudPanel(layer, new Vector2(22,20), new Vector2(250,64), new Color(.025f,.020f,.026f,.86f));
        AddHudPanel(layer, new Vector2(1008,20), new Vector2(250,64), new Color(.025f,.020f,.026f,.86f));
        AddHudPanel(layer, new Vector2(490,18), new Vector2(300,50), new Color(.025f,.020f,.026f,.78f));
        AddHudPanel(layer, new Vector2(1000,625), new Vector2(258,66), new Color(.025f,.020f,.026f,.82f));

        AddHudLabel(layer,"CASTLE  20 / 20",new Vector2(38,31),22,new Color(.70f,.82f,1f));
        AddHudLabel(layer,"ENEMY  20 / 20",new Vector2(1025,31),22,new Color(1f,.68f,.60f));
        AddHudLabel(layer,"ROUND 1   •   YOUR TURN",new Vector2(518,29),19,new Color(.90f,.82f,.61f));
        AddHudLabel(layer,"MANA  5 / 5",new Vector2(1020,638),18,new Color(.48f,.68f,1f));
        AddHudLabel(layer,"SUSPICION  0%",new Vector2(1020,662),16,new Color(.85f,.72f,.50f));

        AddHudLabel(layer,"RESERVES",new Vector2(30,610),14,new Color(.72f,.70f,.66f));
        AddHudLabel(layer,"COMMAND HAND",new Vector2(486,610),14,new Color(.72f,.70f,.66f));
    }

    private void AddHudPanel(CanvasLayer layer, Vector2 position, Vector2 size, Color color)
    {
        var rect = new ColorRect
        {
            Position = position,
            Size = size,
            Color = color,
            MouseFilter = Control.MouseFilterEnum.Ignore
        };
        layer.AddChild(rect);
    }

    private void AddHudLabel(CanvasLayer layer, string text, Vector2 position, int fontSize, Color color)
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
