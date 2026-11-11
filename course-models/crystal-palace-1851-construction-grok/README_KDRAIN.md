# K-DRAIN (CP014) — rain path cutaway

Labelled cutaway of rain running from the ridge-and-furrow roof into the Paxton gutter, down the hollow cast-iron column and out through the base pipe (after Downes 1852, plates XII–XIII). Detail set under the construction branch.

```
blender -b -P scripts/build_drain.py -- --out rounds/k01.blend
blender -b rounds/k01.blend -P scripts/check_set.py -- --out checks/k01 --route route/drain_route.json
scripts/render_round.sh k01 ALL
```

Shots: `CP014_drain_whole` (ortho portrait), `CP014_drain_roof` (ortho), `CP014_drain_gutter` (50 mm live), `CP014_drain_base` (50 mm live).

**2026-11-11:** live k01 carries the CP014_drain_whole "Downes plate" KEEP (KD07–KD13). After `build_drain.py`, apply `scripts/cand_cp014_plate_20261111.py` (or just run `scripts/render_cp014_plate_live.sh --rebuild`), otherwise the polish is lost. Hero render: `scripts/render_cp014_plate_live.sh` (studio, 24 spp, exposure −0.13).

**2026-11-11 (later):** live k01 also carries the CP014 cams KEEP (KD14–KD16: KEEP base piece, outlet and main gutter in all four CP014 shots, roof labels in frame, grey concrete section), md5 dc8469af…. Rebuild = committed `build_drain.py` output (k01 at f2c8530) → `cand_cp014_plate_20261111.py` → `cand_cp014_cams_20261111.py`, i.e. `scripts/render_cp014_cams_live.sh --rebuild` (renders max diff 0 vs live). Running today's `build_drain.py` from scratch (`--rebuild-scratch`) does NOT reproduce live: the script was edited at ae50e7d (rejected Muse gutter profile) and a fresh build moves the scale figure. Hero renders (all four shots, one camera per Blender session, studio 24 spp; exposures whole −0.13, roof 0.40, gutter 0.42, base 0.30): `scripts/render_cp014_cams_live.sh`. `render_cp014_plate_live.sh --rebuild` now forwards there. Candidate rebuild for comparison: `scripts/render_cp014_cams.sh` (builds from the pre-KEEP k01 at 4f7da40).
