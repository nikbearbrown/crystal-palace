#!/bin/bash
# usage: scripts/build_round.sh dNN   -> rounds/dNN_empty.blend, rounds/dNN_dismantle.blend
# Stage 1 runs the transept's own build (same scripts, non-HP51 state); stage 2 adds the after-exhibition dressing.
set -e
R=$1; B=/workspace/blender5/blender; cd "$(dirname "$0")/.."
T=../crystal-palace-1851-transept-grok/scripts/build_transept.py
mkdir -p rounds/_base
for S in empty dismantle; do
  $B -b -P $T -- --state $S --out rounds/_base/base_$S.blend > /workspace/logs/${R}_base_$S.log 2>&1
  $B -b rounds/_base/base_$S.blend -P scripts/build_dismantle.py -- --state $S --out rounds/${R}_$S.blend 2>&1 | grep -E "DISMANTLE_INFO|SAVED|Error|Traceback|line [0-9]" 
done
# CP031 KEEP (2026-11-02): build_dismantle.py still lays down the r09 stand-in striker; swap it for the live dressed
# striker (DM24) with the maul-face nudge (DM25) so every full round ends with the CP031 striker in place.
TMP=$(mktemp -d)
$B -b rounds/${R}_dismantle.blend -P scripts/candidate_cp031_strike.py -- --contact-dy 0.10 --out "$TMP/${R}_dismantle.blend" 2>&1 | grep -E "CP031_INFO|CP031 saved|Error|Traceback"
mv "$TMP/${R}_dismantle.blend" rounds/${R}_dismantle.blend; rm -rf "$TMP"
$B -b rounds/${R}_dismantle.blend --python-expr "import bpy,sys; ok=('D_STAFF_STRIKER_CPL3' in bpy.data.objects) and ('D_STAFF_STRIKER' not in bpy.data.objects); print('CP031_STRIKER_IN_PLACE', ok); sys.exit(0 if ok else 3)" 2>&1 | grep CP031_STRIKER_IN_PLACE
echo BUILD_DONE
