# Third-party art used by the local build pipeline

Castle Cards keeps generated GLB output out of Git and acquires the following source packs into the ignored `.asset-cache/` directory when `Update-Project.bat` runs.

## KayKit — Medieval Hexagon Pack

- Source: `KayKit-Game-Assets/KayKit-Medieval-Hexagon-Pack-1.0`
- Pinned commit: `84fa4e91af6a88989be7c99e0891cede11f2ca38`
- License: CC0 1.0 Universal
- Current Castle Cards use: authored castle buildings, tower modules, wall segments, bridge, trees and rocks.

## KayKit — Character Pack: Adventurers

- Source: `KayKit-Game-Assets/KayKit-Character-Pack-Adventures-1.0`
- Pinned commit: `672074b73ba276876a19e8816ecdc5241817ab47`
- License: CC0 1.0 Universal
- Current Castle Cards use: authored rigged character source for the medieval-tavern opponent visual pass.

These packs are intentionally pinned. Upstream changes cannot silently alter generated Castle Cards art. The acquisition script verifies the required files before Blender generation begins.
