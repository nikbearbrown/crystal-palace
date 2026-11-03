#!/bin/bash
# CP011 yard CANDIDATE 2026-11-03 (CN47): rebuild candidate blend from the PRE-KEEP c07, render before/after, make pairs.
# KEEP 2026-11-03: live rounds/c07.blend now carries the yard (render_cp011_yard_live.sh), so this historical script
# reads the pre-yard c07 pinned at construction commit f73d09c instead of rounds/c07.blend.
set -e; cd "$(dirname "$0")/.."; B=/workspace/blender5/blender; C=renders/candidates/cp011_yard_20261103
TMP=$(mktemp -d); git show f73d09c:course-models/crystal-palace-1851-construction-grok/rounds/c07.blend > $TMP/c07_preyard.blend
$B -b $TMP/c07_preyard.blend -P scripts/cand_cp011_yard_20261103.py -- --out rounds/candidates/c07_cp011yard.blend
$B -b $TMP/c07_preyard.blend -P scripts/render_views.py -- --cams CP011_yard_start,CP011_yard_end --outdir $C/before --res 1280x720 --samples 48
$B -b rounds/candidates/c07_cp011yard.blend -P scripts/render_views.py -- --cams CP011_yard_start --outdir $C/after --res 1280x720 --samples 48 --no-people --exposure 0.95
$B -b rounds/candidates/c07_cp011yard.blend -P scripts/render_views.py -- --cams CP011_yard_end --outdir $C/after --res 1280x720 --samples 48 --no-people --exposure 1.06
rm -rf $TMP
python3 scripts/cand_cp011_yard_pairs.py
