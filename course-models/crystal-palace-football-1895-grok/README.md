# G-FOOTBALL — Crystal Palace football ground 1895 / 1913

Appends the Sydenham palace shell read-only. Never edits `/workspace/crystal-palace-sydenham/`.

```
blender -b -P scripts/build_football.py -- --state 1913 --out rounds/fb01.blend
blender -b -P scripts/build_football.py -- --state 1895 --out rounds/fb01_1895.blend
blender -b rounds/fb01.blend -P scripts/check_set.py -- --out checks/fb01
scripts/render_round.sh fb01 ALL
```
