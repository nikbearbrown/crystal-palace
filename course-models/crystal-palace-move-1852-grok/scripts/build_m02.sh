#!/usr/bin/env bash
# Move round m02 (CP032). Builds a round with build_move.py, then re-applies the CP032 departure hands KEEP
# (2026-11-02, DEPARTURES MV15) in place and asserts CP032_HANDS_IN_PLACE True, so every rebuilt round carries
# the dressed hands instead of the STAFF_* stand-ins. Since 2026-11-02 it also re-applies the CP032 arrival hands KEEP
# (DEPARTURES MV16, candidate_cp032_arrival.py --live) and asserts CP032_ARR_HANDS_IN_PLACE True, and the CP032 arrival
# near-foreground KEEP (DEPARTURES MV17, candidate_cp032_foreground.py --live: grok_states hides CPL_HorizonGround for
# CP032_arrival* cams, ARR_CLAY -> GT_SydenhamClayYard) and asserts CP032_FG_IN_PLACE True, then the CP032 arrival
# yard dressing KEEP (DEPARTURES MV18, candidate_cp032_yard.py --live: ARR_YD_* ruts/puddles/stones/boards/barrow/tools,
# yard clay rebuilt, grey-brown spoil, weathered arrival bar bundles; needs MV17 first) and asserts CP032_YARD_IN_PLACE True, then the CP032
# parkland oaks KEEP (DEPARTURES MV19, candidate_cp032_trees.py --live: parametric oaks replace the lollipop meshes,
# Sydenham meadow, ARR-only weathered bearers/crates, ARR_HD_HAT felt hats + hair; needs MV17 + MV18 first) and asserts
# CP032_TREES_IN_PLACE True.
#   bash scripts/build_m02.sh [OUT]   (default rounds/m02.blend)
# Caution: build_move.py has grown since m02 was frozen on 2026-10-27 (it now also builds the CP068 legacy region),
# so a fresh round is NOT byte- or pixel-identical to the live m02; use render_cp032_live.sh --rebuild to reproduce live.
set -euo pipefail
cd "$(dirname "$0")/.."
B=/workspace/blender5/blender; OUT=${1:-rounds/m02.blend}
"$B" -b --factory-startup -P scripts/build_move.py -- --out "$OUT" 2>&1 | grep -E "SAVED|Error|Traceback"
"$B" -b "$OUT" -P scripts/candidate_cp032_people.py -- --live 2>&1 | grep -E "CP032_HANDS_IN_PLACE|CP032 saved|Error|Traceback"
"$B" -b "$OUT" --python-expr "import bpy,sys; h=[o for o in bpy.data.objects if o.name.startswith('DEP_HAND_')]; s=[n for n in ('STAFF_00_workman','STAFF_01_workman','STAFF_02_workman','STAFF_03_clerk','STAFF_04_workman','STAFF_05_workman','STAFF_06_workman') if n in bpy.data.objects]; ok=len(h)==7 and not s; print('CP032_HANDS_IN_PLACE', ok); sys.exit(0 if ok else 3)" 2>&1 | grep CP032_HANDS_IN_PLACE
"$B" -b "$OUT" -P scripts/candidate_cp032_arrival.py -- --live 2>&1 | grep -E "CP032_ARR_HANDS_IN_PLACE|CP032_ARR saved|Error|Traceback"
"$B" -b "$OUT" --python-expr "import bpy,sys; h=[o for o in bpy.data.objects if o.name.startswith('ARR_HAND_')]; s=[n for n in ('STAFF_07_workman','STAFF_08_workman','STAFF_09_workman','STAFF_10_workman','STAFF_11_clerk') if n in bpy.data.objects]; ok=len(h)==5 and not s; print('CP032_ARR_HANDS_IN_PLACE', ok); sys.exit(0 if ok else 3)" 2>&1 | grep CP032_ARR_HANDS_IN_PLACE
FG=$("$B" -b "$OUT" -P scripts/candidate_cp032_foreground.py -- --live 2>&1 | grep -E "CP032_FG_IN_PLACE|CP032_FG saved|Error|Traceback" || true)
echo "$FG"; grep -q "CP032_FG_IN_PLACE True" <<<"$FG" || { echo "CP032_FG_IN_PLACE check failed"; exit 3; }
YD=$("$B" -b "$OUT" -P scripts/candidate_cp032_yard.py -- --live 2>&1 | grep -E "CP032_YARD_IN_PLACE|CP032_YARD saved|Error|Traceback" || true)
echo "$YD"; grep -q "CP032_YARD_IN_PLACE True" <<<"$YD" || { echo "CP032_YARD_IN_PLACE check failed"; exit 3; }
TR=$("$B" -b "$OUT" -P scripts/candidate_cp032_trees.py -- --live 2>&1 | grep -E "CP032_TREES_IN_PLACE|CP032_TREES saved|Error|Traceback" || true)
echo "$TR"; grep -q "CP032_TREES_IN_PLACE True" <<<"$TR" || { echo "CP032_TREES_IN_PLACE check failed"; exit 3; }
echo BUILD_DONE
