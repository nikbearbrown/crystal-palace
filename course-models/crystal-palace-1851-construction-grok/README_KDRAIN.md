# K-DRAIN (CP014) — rain path cutaway

Labelled cutaway of rain running from the ridge-and-furrow roof into the Paxton gutter, down the hollow cast-iron column and out through the base pipe (after Downes 1852, plates XII–XIII). Detail set under the construction branch.

```
blender -b -P scripts/build_drain.py -- --out rounds/k01.blend
blender -b rounds/k01.blend -P scripts/check_set.py -- --out checks/k01 --route route/drain_route.json
scripts/render_round.sh k01 ALL
```

Shots: `CP014_drain_whole` (ortho portrait), `CP014_drain_roof` (ortho), `CP014_drain_gutter` (50 mm live), `CP014_drain_base` (50 mm live).
