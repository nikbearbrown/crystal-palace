# Crystal Palace dinosaurs, 1854 — scripted Blender model (grok)

This folder holds scripted Blender 5.1 models of the Benjamin Waterhouse Hawkins sculptures in Crystal Palace Park, Sydenham, as first shown in 1854. These are the Victorian reconstructions, which are wrong by modern standards: Iguanodon with a nose horn, a quadruped Megalosaurus, ichthyosaurs basking like seals, and Megatherium with a tapir trunk. It is built for shots CP043 (lake islands) and CP034 (Hawkins' studio and the Dinner in the Iguanodon).

## Build / check / render
```
B=/workspace/blender5/blender
$B -b -P scripts/build.py -- rounds/dinosaurs-1854-r01.blend
$B -b rounds/dinosaurs-1854-r01.blend -P checks/dimension_check.py -- checks/r01.txt
RES=1920x1080 $B -b rounds/dinosaurs-1854-r01.blend -P scripts/render.py -- renders/r01 r01 100 48 CAM_...
python3 scripts/state_sheet.py out.jpg "title" 3 "label=path" ...
```

## Collections (dated)
- `DN-1854_crystal_palace_park_geological_illustration`
  - `DN54_lake_islands__1854`: terrain, lake, fence, planting
  - `DN54_secondary_island_sculptures__1854`: 2 Iguanodons, Megalosaurus, Hylaeosaurus, 3 Ichthyosaurs, 3 Plesiosaurs
  - `DN54_tertiary_island_mammals__1854`: Megatherium with its tree, and 4 Irish elk (2 stags and 2 does, one reclining)
  - `DN54_geological_strata__1854`
  - `DN53_hawkins_studio__1853` (set at x = 2000): the Sydenham workshop with clay Iguanodon, scaffold and workmen
  - `DN53_iguanodon_dinner__31Dec1853` (set at x = 3000): open mould, deck, marquee and 21 diners
- `CAMERAS`: all cameras use a 36 mm sensor, 1.6 m eye height and no roll
  - `CAM_CP043_lake_islands_35mm`
  - `CAM_CP043b_iguanodons_detail_50mm`
  - `CAM_CP043c_tertiary_megatherium_elk_50mm`
  - `CAM_CP034_hawkins_studio_28mm`
  - `CAM_CP034b_iguanodon_dinner_28mm`

## Scripts
- `scripts/hawkins.py`: one function per species. Each animal is metaball-sculpted (`scripts/mb.py`, method after the HP executor's `figures.py`, read-only, credited), with cones for spines, horns, teeth and tines. All face +X with the origin on the ground.
- `scripts/build.py`: builds the scene, sets, cameras, world and Cycles.

## References
- PD prints, downsized and committed in `refs/`:
  - ILN 1853, Hawkins' Sydenham studio: https://commons.wikimedia.org/wiki/File:Sydenham_studio.jpg
  - ILN 7 Jan 1854, Dinner in the Iguanodon woodcut: https://commons.wikimedia.org/wiki/File:Crystal_palace_iguanodon.jpg
- CC photos of the surviving statues, used as visual reference only and not committed:
  - https://commons.wikimedia.org/wiki/File:Iguanodon_Crystal_Palace.jpg (CC BY-SA 2.0)
  - https://commons.wikimedia.org/wiki/File:2005-03-30_-_London_-_Crystal_Palace_-_Victorian_Dinosaurs_1_4887762470.jpg (CC BY 2.0)
  - Commons "Crystal Palace Hylaeosaurus", "Crystal Palace Ichthyosaurus", "Crystal Palace Megaloceros giganteus" and "Crystal Palace Dinosaurs overview"
- Sizes and counts:
  - cpdinosaurs.org statue pages (Iguanodon, Megalosaurus, Ichthyosaur, Plesiosaur, Megaloceros)
  - Historic England listing
  - Wikipedia, "Crystal Palace Dinosaurs" (citing McCarthy & Gilbert 1994)

Every guess is graded in DEPARTURES.md. Progress is logged in PROGRESS.md.
