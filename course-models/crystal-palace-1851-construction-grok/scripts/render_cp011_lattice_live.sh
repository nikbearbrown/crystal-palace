#!/usr/bin/env bash
# CP011 lattice v2 one-tier LIVE (KEEP 2026-11-03, DEPARTURES CN49). Same as render_cp011_yard_live.sh, which renders the
# live CP011 (yard CN47 + lattice CN49 + pile CN50 + yard2 CN51) at exposure 0.83 start / 0.88 end -> renders/c07/CP011_yard_{start,end}.png.
#   scripts/render_cp011_lattice_live.sh [--rebuild] [samples=48] [outdir=renders/c07]
exec "$(dirname "$0")/render_cp011_yard_live.sh" "$@"
