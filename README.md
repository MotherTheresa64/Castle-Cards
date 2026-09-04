# Castle Cards

Castle Cards is a first-person medieval tabletop roguelike built with Godot 4.7.2 .NET, C#, and Blender.

The player sits at a physical war table with cards, visible miniature reserves, castles, terrain, and an opponent across the board. Cards issue commands to real tabletop units, while cheating mechanics allow the player to bend the physical rules at the risk of suspicion and consequences.

## Development workflow

This repository is the source of truth for the project.

1. Changes are committed here.
2. Run `Update-Project.bat` in the local clone.
3. The script pulls the latest commit and builds the C# project.
4. Godot detects the changed files and reloads/imports them locally.

Generated `.glb` models and editable Blender source files can both live in the repository so visual updates arrive with a normal pull.
