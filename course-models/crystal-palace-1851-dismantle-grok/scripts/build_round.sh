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
echo BUILD_DONE
