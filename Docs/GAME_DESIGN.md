# Castle Cards — Game Design Source of Truth

## Core Premise

Players sit around a physical table playing cards, deploying miniatures, casting magic, and defending a castle. Matches can be played against NPCs, other players, or cooperatively. The main objective is to protect your king while defeating the opponent's king.

The game is a roguelike. Across a run, the player upgrades four major pillars:

1. Defense / castle
2. Troops / creatures
3. Spells
4. Terrain

The table, battlefield, castle, reserves, cards, mana, suspicion and upgrades should all have physical visual language wherever possible.

## Match Loop

1. Pick a spot for your castle.
2. Place troops.
3. Start the match.
4. Cast spells to support your troops or damage enemy troops.
5. Deploy a limited number of reinforcements from your castle during ongoing skirmishes.
6. Attack the enemy castle and kill the enemy king.
7. Win the match.
8. Choose one of four upgrade categories.
9. Receive three random upgrade options from that category.
10. Choose one upgrade.
11. Continue to the next challenger.

Possible king-kill strategies include assassination, brute-force castle destruction, overwhelming pressure, magic, sneaking troops through alternate routes, or other emergent strategies.

## Cheating / Karma / Suspicion

During a match, the player can cheat. Opponents can cheat too.

Examples:

- Play extra soldiers.
- Cast a spell with insufficient mana.
- Move the castle.
- Deploy a large creature that should not be available.

Cheating raises opponent suspicion. Larger cheats raise suspicion more quickly. Frequent small cheats also make the opponent increasingly suspicious.

Playing honorably builds karma. High karma makes it easier to attempt a large run-saving cheat later.

If suspicion reaches a threshold, the opponent may call out a cheat. If the player actually cheated, penalties can include losing an upgrade, downgrading something, or ending the match/run. If the opponent falsely accuses the player, the opponent is penalized.

The design goal is that cheating can save a run but always carries visible risk and tension.

## Upgrades

Each post-match upgrade begins with four category choices:

- Defense
- Troops
- Spells
- Terrain

After choosing a category, the player receives three random upgrades.

### Rarity Targets

| Rarity | Intent | Approx. chance |
| --- | --- | ---: |
| Common | Incremental improvement | ~60% |
| Rare | Significant improvement | ~27% |
| Epic | New mechanic / build direction | ~11% |
| Legendary | Run-defining mechanic | ~2% |

Upgrade quality improves as the player advances through an area, then resets when entering the next area.

### Common

Small stacking improvements such as more reinforcements, more damage, more health, larger spell radius, improved terrain coverage, better traps, etc.

### Rare

Significant improvements to existing systems such as watchtowers, larger moats, forest traps, better terrain funnels, larger units, upgraded spells, etc.

### Epic

New mechanics such as defenders pouring tar, new troop types, advanced spell behavior or spell combinations.

### Legendary

Run-defining effects that are extremely powerful but usually include drawbacks.

Examples:

- Dead units in the castle may return to life, including enemy units.
- A powerful wizard may sacrifice friendly troops to cast spells.
- A meta-scale resurrection spell could affect the entire area outside the immediate match.
- A dragon could guard the castle but may accidentally burn friendly troops.
- Berserk troops may occasionally go rogue or revolt.

## Defense Design

Defense upgrades improve the castle, defenders, reinforcements and defensive terrain.

Possible common progression includes:

- Wall health I–III
- Tree coverage I–IV
- Terrain difficulty I–III
- Guards I–IV
- Trap I–III
- King I–III
- Reinforcements I–IV
- Castle I–IV

Possible rare progression includes:

- Watchtower I–III
- Moat I–III
- Forest / tree upgrades I–III
- Terrain upgrades I–III

Higher tiers can create new behavior such as mage towers, lava moats, ambushes, lookout posts, enemies getting lost, mountainous terrain or valley funnels.

## Troops

Troop upgrades strengthen offensive pressure and battlefield control. They can improve stats, increase unit count, improve weapons, unlock better creature tiers or add new unit types.

Troop-heavy builds should be strong in skirmishes and castle pressure but can leave the player's own king vulnerable.

## Spells

Spells support both offense and defense. Examples include healing troops, fireball damage and other battlefield effects.

Spells can become stronger, affect larger areas and eventually combine with each other.

Spells can affect terrain. Fireball can ignite forested terrain. Other combinations can produce persistent battlefield changes.

## Areas and Run Structure

Each area contains five opponents. The fifth opponent is a miniboss with a stronger army, upgraded castle and stronger spells.

After defeating an area's boss, the player moves to the next connected area on a branching run map.

Area themes:

- Medieval tavern — humans; starting character/theme
- Cave / mines — dwarves
- Forest — fae / elves
- Prison — gruff humans / monsters
- Desert town or oasis — Persian-inspired
- Polar region — arctic-inspired
- Asia — samurai / ninja-inspired
- Evil castle — monsters
- Seaport — fishermen / maritime
- Floating island — mages
- Steampunk — artificers / machines
- Castle — royalty
- Dragon lair — dragons / dragon-born

Different areas should influence the style and behavior of upgrades. Forest creature upgrades should feel wilder. Tavern upgrades should reflect medieval human warfare. Other areas should follow their own visual and mechanical logic.

### Example Branching Map

```text
                 AREA 4
                 /    \
       AREA 2 — AREA 3 — AREA 5
      /          |          \
START            |           AREA 8
      \          |          /
       AREA 6 — AREA 7
```

## NPC Characteristics

NPCs can have one or more gameplay personalities:

- Suspicious — harder to cheat against, more likely to call cheating.
- Aggressive — pushes troops with little strategy.
- Tactical — plays strategically and may take longer to decide.
- Naive — easy to cheat against; being caught heavily damages karma.
- Trickster — cheats well and detects cheating well.
- Wizard — prefers spells.
- Commander — prefers troops.
- Golem — highly defensive.

NPC behavior should have visible tells through clothing, tabletop setup, reserve composition, props and animation where possible.

## Pantheon Endgame

After every area boss has been defeated, the player can enter the Pantheon.

The Pantheon contains twelve extremely difficult matches against gods in a row.

Each god has a game-altering mechanic similar to a Legendary upgrade, but without the player's drawback.

After defeating the final god, the player chooses between:

- Ascend — end the save and completely restart progression.
- Gain notoriety — continue the save while making all future matches harder.

## Visual Direction

The starting Medieval Tavern area should feel like a dense, lived-in, low-poly medieval room built around an enormous physical war table.

The visual target is polished stylized low-poly rather than realistic rendering. Detail should come from deliberate modeling, material variation, lighting, asymmetry, prop density and physical representations of game systems.

Important visible gameplay elements include:

- Player and enemy castles
- Kings and royal guards
- Physical unit reserves
- Reinforcement staging areas
- Siege weapons
- Spellcasting props and active spell effects
- Terrain consequences from magic
- Castle upgrade sockets / defensive additions
- Traps
- Physical mana objects
- Suspicion and karma objects
- Concealed cheat resources
- Opponent personality / trait cues
- Branching run-map imagery in the tavern
- Four upgrade category language: Defense, Troops, Spells, Terrain

The art pipeline should prefer authored Blender assets for hero objects and use Godot procedural geometry mainly for subtle filler, micro-detail and runtime effects.
