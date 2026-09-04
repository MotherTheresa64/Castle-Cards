using System.Collections.Generic;

public enum UpgradeCategory
{
    Defense,
    Troops,
    Spells,
    Terrain
}

public enum UpgradeRarity
{
    Common,
    Rare,
    Epic,
    Legendary
}

public enum NpcTrait
{
    Suspicious,
    Aggressive,
    Tactical,
    Naive,
    Trickster,
    Wizard,
    Commander,
    Golem
}

public enum AreaTheme
{
    MedievalTavern,
    CaveMines,
    Forest,
    Prison,
    DesertOasis,
    PolarRegion,
    Asia,
    EvilCastle,
    Seaport,
    FloatingIsland,
    Steampunk,
    RoyalCastle,
    DragonLair,
    Pantheon
}

public enum CheatAction
{
    ExtraSoldier,
    FreeSpell,
    FreeMana,
    MoveCastle,
    ExtraCreature,
    Other
}

public static class GameDesignCatalog
{
    public const int OpponentsPerArea = 5;
    public const int PantheonGodCount = 12;
    public const int UpgradeCategoryChoices = 4;
    public const int UpgradeOptionChoices = 3;

    public static readonly IReadOnlyDictionary<UpgradeRarity, float> BaseUpgradeRarityWeights =
        new Dictionary<UpgradeRarity, float>
        {
            [UpgradeRarity.Common] = 0.60f,
            [UpgradeRarity.Rare] = 0.27f,
            [UpgradeRarity.Epic] = 0.11f,
            [UpgradeRarity.Legendary] = 0.02f
        };

    public static readonly AreaTheme[] StandardAreas =
    {
        AreaTheme.MedievalTavern,
        AreaTheme.CaveMines,
        AreaTheme.Forest,
        AreaTheme.Prison,
        AreaTheme.DesertOasis,
        AreaTheme.PolarRegion,
        AreaTheme.Asia,
        AreaTheme.EvilCastle,
        AreaTheme.Seaport,
        AreaTheme.FloatingIsland,
        AreaTheme.Steampunk,
        AreaTheme.RoyalCastle,
        AreaTheme.DragonLair
    };
}
