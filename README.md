# Castle Cards

Castle Cards is a first-person medieval tabletop roguelike built with Godot 4.7.2 .NET, C#, and Blender.

The player sits at a physical war table with cards, visible miniature reserves, castles, sculpted terrain, resources, and an opponent across the board. Cards issue commands to tabletop units while cheating mechanics let the player bend the physical rules at the risk of suspicion and consequences.

## Local update workflow

The repository contains the source code and procedural Blender build pipeline. Generated GLB files are intentionally local build outputs.

1. Pull/commit source changes through GitHub.
2. Run `Update-Project.bat` in the local clone.
3. The update script acquires the pinned CC0 source packs, runs every Blender generator, applies the final cinematic embedded-PBR material pass, and verifies the expected GLB outputs.
4. The script runs `dotnet build`.
5. Open Godot (or return to it) and allow the generated GLBs to import/reload.

The asset pipeline is versioned, so changing a generator automatically forces a fresh local regeneration on the next update.

## Scene controls

- **Right mouse drag** — orbit/look around the tabletop scene.
- **Mouse wheel** — zoom.
- **WASD** — pan the camera focus across the board.
- **F** — reset to the authored seated composition.
- **Left click** — select a gameplay placement cell. The board stays visually gridless until a cell is hovered/selected.

## Visual target

The intended look is a premium stylized tabletop diorama: sculpted terrain, collectible miniatures, layered castles, a readable opponent hero, warm practical tavern lighting, cool ambient fill, deep contact shadows, restrained bloom, and material breakup that reads as wood, stone, cloth, metal, earth, parchment, skin, foliage, and water rather than flat primitive colors.
