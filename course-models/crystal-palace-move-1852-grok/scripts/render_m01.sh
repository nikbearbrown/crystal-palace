#!/bin/bash
# detached final render of every m01 camera (1920x1080, 96 samples); log in /workspace/logs/move_render_m01.log
cd "$(dirname "$0")/.."
/workspace/blender5/blender -b rounds/m01.blend -P scripts/render_shots.py -- --out renders/m01 --samples 96 --pct 100 \
  && python3 /workspace/tmp/sheet.py renders/m01 renders/m01/contact_sheet_m01.jpg && echo RENDER_M01_DONE
