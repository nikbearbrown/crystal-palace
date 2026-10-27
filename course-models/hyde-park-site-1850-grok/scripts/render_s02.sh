#!/bin/bash
# detached final render of every s02 camera (1920x1080, 96 samples); log in /workspace/logs/site_render_s02.log
cd "$(dirname "$0")/.."
/workspace/blender5/blender -b rounds/s02.blend -P scripts/render_shots.py -- --out renders/s02 --samples 96 --pct 100 \
  && python3 /workspace/tmp/sheet.py renders/s02 renders/s02/contact_sheet_s02.jpg && echo RENDER_S02_DONE
