#!/usr/bin/env bash
# Construction round c07 (HP-BUILD, Hyde Park 1850-51; never Sydenham). Builds a round with build_construction.py
# (c07 = horse harness + darker coats, commit 69d29f8), then re-applies, in order:
#   1. the CP011 works-yard KEEP (2026-11-03, DEPARTURES CN47, cand_cp011_yard_20261103.py --live: camera-scoped, new
#      CP011C_* only_cams=CP011_yard; DETAIL_DRAINAGE, old KYARD stock and KWORKER_024-026 hide_cams=CP011_yard),
#      asserting CP011_YARD_IN_PLACE True;
#   2. the CP011 one-tier girder lattice v2 KEEP (2026-11-03, DEPARTURES CN49, cand_cp011_lattice_v2_20261103.py --live:
#      only CP011C_* only_cams=CP011_yard objects added/moved), asserting CP011_LATTICE_IN_PLACE True;
#   3. the CP011 near pile + timber bay KEEP (2026-11-03, DEPARTURES CN50, cand_cp011_pile_20261103.py --live: flanges,
#      as-cast iron, deal floor/landing/stacks; only CP011C_* objects, only_cams=CP011_yard), asserting CP011_PILE_IN_PLACE True.
# Idempotent: each --live step on a blend that already carries it only checks it.
#   bash scripts/build_c07.sh [OUT]   (default rounds/c07.blend)
# Caution: a fresh build is not guaranteed byte- or pixel-identical to the frozen live c07 (the exterior prelude it
# execs may have moved on); use scripts/render_cp011_yard_live.sh --rebuild to reproduce live c07 exactly.
set -euo pipefail
cd "$(dirname "$0")/.."
B=/workspace/blender5/blender; OUT=${1:-rounds/c07.blend}
"$B" -b --factory-startup -P scripts/build_construction.py -- --out "$OUT" 2>&1 | grep -E "^SAVED|Error|Traceback" | cut -c1-200
YD=$("$B" -b "$OUT" -P scripts/cand_cp011_yard_20261103.py -- --live 2>&1 | grep -E "CP011_YARD|Error|Traceback" || true)
echo "$YD"; grep -q "CP011_YARD_IN_PLACE True" <<<"$YD" || { echo "CP011_YARD_IN_PLACE check failed"; exit 3; }
LT=$("$B" -b "$OUT" -P scripts/cand_cp011_lattice_v2_20261103.py -- --live 2>&1 | grep -E "GIRDERS|CP011_LATTICE|Error|Traceback" || true)
echo "$LT"; grep -q "CP011_LATTICE_IN_PLACE True" <<<"$LT" || { echo "CP011_LATTICE_IN_PLACE check failed"; exit 3; }
PL=$("$B" -b "$OUT" -P scripts/cand_cp011_pile_20261103.py -- --live 2>&1 | grep -E "DEAL|CP011_PILE|Error|Traceback" || true)
echo "$PL"; grep -q "CP011_PILE_IN_PLACE True" <<<"$PL" || { echo "CP011_PILE_IN_PLACE check failed"; exit 3; }
echo BUILD_DONE
