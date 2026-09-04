# Castle Cards — Art Direction / Quality Bar

This document is the visual source of truth for Castle Cards.

## Target Quality

The target is polished, authored, stylized low-poly 3D — not blockout art, not raw primitives, and not "more objects" as a substitute for quality.

The desired result should feel like a premium tabletop diorama inside a dark medieval environment:

- Deliberately modeled silhouettes with strong shape language.
- Rounded/beveled edges where appropriate so assets catch light cleanly.
- Layered geometry and secondary forms instead of single primitive masses.
- Cohesive low-poly materials with value/color variation, roughness differences, and believable separation between wood, stone, metal, cloth, skin, foliage, earth, parchment, and magic.
- Strong ambient occlusion/contact shadowing so small forms read clearly.
- Warm practical light sources combined with cooler ambient fill.
- Dark atmosphere without crushing detail into black.
- Dense environmental storytelling: shelves, bottles, chains, banners, crates, tools, weapons, books, candles, barrels, and architectural breakup.
- Battlefield terrain that reads as sculpted miniature terrain rather than a flat green rectangle.
- Castles that feel handcrafted and asymmetrical, with layered walls, towers, battlements, gates, stairs, torches, flags, buttresses, rubble, trim, and readable interior focal points.
- Units that read as finished tabletop miniatures: distinct silhouettes, proper weapons/shields, coherent armor/clothing forms, and clean bases.
- Opponents that feel like stylized characters, not mannequins: believable anatomy, face planes, hair/beard/clothing layers, hands, seated posture, and purposeful lighting.

## What Does Not Count As "More Detail"

The following do not satisfy the quality target by themselves:

- Adding dozens of tiny primitives.
- Repeating the same asset many times.
- Adding HUD panels to imply complexity.
- Increasing object count while keeping hero assets rough.
- Using raw cubes/cylinders/spheres as final visible geometry.
- Flat single-color materials with no authored variation.

Quality per asset matters more than object count.

## Production Priority

When improving visuals, prioritize in this order:

1. Opponent hero character.
2. Player castle / enemy castle modular hero kit.
3. Core troop miniature set.
4. Battlefield terrain and terrain materials.
5. Main tabletop / cards / reserves / mana / cheat props.
6. Tavern architecture and environmental props.
7. Lighting / atmosphere / post-process polish.
8. Secondary clutter and micro-detail.

## Hero Asset Standard

A hero asset is anything large or repeatedly visible from the seated gameplay camera. Hero assets must:

- Have intentional silhouette design.
- Use multiple material regions.
- Include secondary and tertiary details visible at gameplay distance.
- Avoid obvious primitive stacking.
- Use bevels/edge treatment appropriate to the style.
- Be tested in Godot under final-ish lighting before mass production.

## Materials

The project should move toward a small cohesive stylized material library instead of ad-hoc flat colors.

Minimum material families:

- Weathered timber / dark timber / polished tabletop wood.
- Cut stone / rough stone / dark masonry / scorched stone.
- Iron / steel / bronze.
- Leather / parchment / cloth colors.
- Skin / hair.
- Grass / dirt / mud / rock / moss.
- Water / lava / magical emissive materials.

Material variation should come from authored color/value breakup, roughness differences, AO, and texture/vertex-color treatment rather than photorealistic detail.

## Terrain Standard

The battlefield must eventually be a sculpted miniature landscape with:

- Small elevation changes.
- Embedded rivers and roads.
- Irregular grass/dirt/rock patches.
- Valleys, hills, chokepoints, forests, and upgrade-driven terrain changes.
- Props that feel integrated into the terrain instead of placed on top of a flat board.

Terrain is gameplay. It must visually communicate upgrade state, routes, hazards, spell effects, and tactical opportunities.

## Castle Standard

Castles must physically evolve with defense upgrades. Visual progression should support:

- Wood -> stone -> darker/high-tier masonry.
- Larger wall mass and stronger gates.
- Watchtowers / mage towers.
- Moats / lava moats.
- Traps and defensive structures.
- Additional courtyards / checkpoints / guard positions.
- Reinforcement outposts and secret-tunnel language.
- King / throne-room readability.

The castle should look meaningfully different as the run progresses.

## Unit Standard

Each troop type needs a unique silhouette and readable battlefield role.

Examples:

- Spearman: long weapon, round/large shield, defensive posture.
- Archer: bow/quiver silhouette.
- Swordsman: sword/shield, closer stance.
- Knight: larger armored silhouette / mount if used.
- Wizard: robe/staff/glow cues.
- Assassin: narrow silhouette, dark cloth, daggers/hood.
- Ogre / monster units: exaggerated mass and distinct proportions.

Miniatures should look like collectible tabletop pieces rather than tiny blockout characters.

## Opponent Standard

The opponent is a major visual anchor and must receive hero-character treatment.

Required qualities:

- Proper stylized head and facial planes.
- Hair/beard mass with clean silhouette.
- Layered clothing such as cloak, tunic, straps, jewelry, gloves, etc.
- Natural seated posture.
- Forearms/hands interacting with the table.
- Personality variants that can visually support NPC traits.
- Lighting designed specifically to keep the face readable.

## Lighting Standard

The lighting target is cinematic-dark, not simply dim.

Use:

- Warm lantern/candle/brazier key lights.
- Cooler ambient/fill lighting.
- Strong contact shadows.
- AO to ground objects.
- Controlled highlights on stone, wood, metal, faces, and cards.
- Dark corners for atmosphere while maintaining battlefield readability.

## Rule For Future Visual Changes

Before adding a new visual feature, ask:

1. Does this improve the quality of a hero asset?
2. Does it communicate gameplay, progression, personality, or atmosphere?
3. Is it visible from the actual gameplay camera?
4. Does it match the established material and shape language?

If the answer is no, it is lower priority than improving an existing hero asset.
