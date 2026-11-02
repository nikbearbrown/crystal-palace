#!/usr/bin/env bash
# Move round m02 (CP032). Builds a round with build_move.py, then re-applies the CP032 departure hands KEEP
# (2026-11-02, DEPARTURES MV15) in place and asserts CP032_HANDS_IN_PLACE True, so every rebuilt round carries
# the dressed hands instead of the STAFF_* stand-ins.
#   bash scripts/build_m02.sh [OUT]   (default rounds/m02.blend)
# Caution: build_move.py has grown since m02 was frozen on 2026-10-27 (it now also builds the CP068 legacy region),
# so a fresh round is NOT byte- or pixel-identical to the live m02; use render_cp032_live.sh --rebuild to reproduce live.
set -euo pipefail
cd "$(dirname "$0")/.."
B=/workspace/blender5/blender; OUT=${1:-rounds/m02.blend}
"$B" -b --factory-startup -P scripts/build_move.py -- --out "$OUT" 2>&1 | grep -E "SAVED|Error|Traceback"
"$B" -b "$OUT" -P scripts/candidate_cp032_people.py -- --live 2>&1 | grep -E "CP032_HANDS_IN_PLACE|CP032 saved|Error|Traceback"
"$B" -b "$OUT" --python-expr "import bpy,sys; h=[o for o in bpy.data.objects if o.name.startswith('DEP_HAND_')]; s=[n for n in ('STAFF_00_workman','STAFF_01_workman','STAFF_02_workman','STAFF_03_clerk','STAFF_04_workman','STAFF_05_workman','STAFF_06_workman') if n in bpy.data.objects]; ok=len(h)==7 and not s; print('CP032_HANDS_IN_PLACE', ok); sys.exit(0 if ok else 3)" 2>&1 | grep CP032_HANDS_IN_PLACE
echo BUILD_DONE
