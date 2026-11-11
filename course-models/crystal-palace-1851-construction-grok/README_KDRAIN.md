# K-DRAIN (CP014) — rain path cutaway

Labelled cutaway of rain running from the ridge-and-furrow roof into the Paxton gutter, down the hollow cast-iron column and out through the base pipe (after Downes 1852, plates XII–XIII). Detail set under the construction branch.

```
blender -b -P scripts/build_drain.py -- --out rounds/k01.blend
blender -b rounds/k01.blend -P scripts/check_set.py -- --out checks/k01 --route route/drain_route.json
scripts/render_round.sh k01 ALL
```

Shots: `CP014_drain_whole` (ortho portrait), `CP014_drain_roof` (ortho), `CP014_drain_gutter` (50 mm live), `CP014_drain_base` (50 mm live).

**2026-11-11:** live k01 carries the CP014_drain_whole "Downes plate" KEEP (KD07–KD13). After `build_drain.py`, apply `scripts/cand_cp014_plate_20261111.py` (or just run `scripts/render_cp014_plate_live.sh --rebuild`), otherwise the polish is lost. Hero render: `scripts/render_cp014_plate_live.sh` (studio, 24 spp, exposure −0.13).
