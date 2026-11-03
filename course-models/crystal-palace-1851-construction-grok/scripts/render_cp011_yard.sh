#!/bin/bash
# CP011 yard CANDIDATE 2026-11-03 (CN47): rebuild candidate blend from c07, render before/after, make pairs. Not live.
set -e; cd "$(dirname "$0")/.."; B=/workspace/blender5/blender; C=renders/candidates/cp011_yard_20261103
$B -b rounds/c07.blend -P scripts/cand_cp011_yard_20261103.py
$B -b rounds/c07.blend -P scripts/render_views.py -- --cams CP011_yard_start,CP011_yard_end --outdir $C/before --res 1280x720 --samples 48
$B -b rounds/candidates/c07_cp011yard.blend -P scripts/render_views.py -- --cams CP011_yard_start --outdir $C/after --res 1280x720 --samples 48 --no-people --exposure 0.95
$B -b rounds/candidates/c07_cp011yard.blend -P scripts/render_views.py -- --cams CP011_yard_end --outdir $C/after --res 1280x720 --samples 48 --no-people --exposure 1.06
python3 scripts/cand_cp011_yard_pairs.py
