# O-WORKSHOP (CP011): an off-site ironworks and glassworks, 1850 (Grok Bot)

A composite workshop in the style of Fox, Henderson & Co. (London Works, Smethwick) and Chance Brothers (Spon Lane). It holds:
- A machine shop with a line shaft and steam engine, two sash-bar machines, a gutter machine and stacked sash bars.
- A glass house with a furnace, a blowing stage over swing pits, cylinder racks and a flattening kiln.
- A railway siding with two wagons carrying a 24 ft girder and columns, under shear legs.

Branch `grok-workshop-1850`, local commits only. The build is self-contained (`scripts/build_workshop.py`); figures come from the Grok fitout `figures.py`.

```
blender -b -P scripts/build_workshop.py -- --out rounds/w01.blend          (run from scripts/)
blender -b rounds/w01.blend -P scripts/check_workshop.py -- --out checks/w01
scripts/render_round.sh w01 CP011_shop_start,...        (wagon exterior: add --exposure -0.7, see W15)
```
