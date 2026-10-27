#!/bin/bash
# usage: scripts/render_round.sh <round> <cams,comma,list|ALL>   (1280x720, 48 spp, detached-friendly)
cd "$(dirname "$0")/.." && /workspace/blender5/blender -b rounds/$1.blend -P scripts/render_views.py -- --cams "$2" --outdir renders/$1 --res 1280x720 --samples 48
