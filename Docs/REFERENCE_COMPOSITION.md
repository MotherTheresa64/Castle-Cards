# Castle Cards — Gameplay Camera / Reference Composition

This is the visual composition lock for the first playable medieval-tavern arena.

## Non-negotiable frame

- The player is seated at a physical war table in a dark, warm medieval tavern.
- The battlefield is a long miniature diorama that runs away from the player toward the opponent.
- The player castle anchors the lower foreground and must **not** dominate the middle of the screen.
- The enemy castle sits at the far end of the board, smaller through perspective.
- A fully modeled brunette, bearded opponent is visible from the torso up behind the enemy castle and is one of the primary focal points.
- Troops are collectible tabletop miniatures distributed in irregular skirmish groups, not chess-piece rows.
- Terrain is sculpted and patchy with roads, water, rocks, trees, cover and readable tactical lanes.
- Tavern architecture frames the scene with shelves, timber, chains, lanterns, barrels and weapons, but never hides the opponent or battlefield.
- Warm lantern/fire light is the key; cool ambient fill preserves readable detail in the shadows.
- HUD is secondary to the diorama and must remain small and translucent.

## Quality hierarchy

When a visual change conflicts with this composition, protect these in order:

1. Opponent face / silhouette readability.
2. Full-board readability from player castle to enemy castle.
3. Player castle as a low foreground anchor rather than a screen-blocking centerpiece.
4. Unit silhouettes and active skirmish readability.
5. Terrain routes / hazards / upgrade state.
6. Tabletop props and cheat-system props.
7. Tavern clutter.
8. HUD decoration.

## Progression rule

Upgrades should physically alter the miniature board. Walls, towers, moat/lava, traps, reinforcement structures, troop equipment, terrain density and spell aftermath should appear on the diorama itself rather than only as UI statistics.

This composition is the baseline for future areas. Forest, mines, prison, desert, polar, Asian-inspired, evil castle, seaport, floating-island, steampunk, royal castle and dragon-lair arenas can change architecture, opponents, troops, terrain and lighting while preserving the same readable seated-tabletop relationship.
