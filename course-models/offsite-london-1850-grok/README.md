# O-INDUSTRY + O-ROOM — London 1850

```
blender -b -P scripts/build_london.py -- --out rounds/ln01.blend
blender -b rounds/ln01.blend -P scripts/check_set.py -- --out checks/ln01
scripts/render_round.sh ln01 ALL
```
