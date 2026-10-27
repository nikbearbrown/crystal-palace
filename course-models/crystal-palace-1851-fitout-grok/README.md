# Crystal Palace, Hyde Park 1851: fit-out, daily life and closing (Grok Bot)

Storyboard sets **HP-FITOUT** (CP018-CP020, Jan-Apr 1851) and **HP51** (CP026-CP029, May-Oct 1851). Branch `grok-fitout-1851`, local commits only.

The sets reuse the Grok transept/exterior build (`scripts/build_transept.py`) with a new `--state` switch:
- `fitout`: no exhibits and no fountain. Paint goes on top-down over primer, with half-painted bays, ladders, cradles and painters. Crates come in on drays and trucks through open south doors. An unboarded floor patch has Muse floor tiles, loose boards, and Paxton's sweeping machine with the hand-engine.
- `hp51`: a shilling-day crowd re-dressed in working clothes. Turnstiles, pay boxes, police and a queue outside. Visitors on the gallery stair. Attendants work Muse's louvres by rope and water the elms.
- `closing`: the hp51 dressing plus the October closing ceremony. A dais with a canopy and chair of state, commissioners, 620 floor and 260 gallery spectators, autumn elms and a lower sun.

```
blender -b -P scripts/build_transept.py -- --state fitout|hp51|closing --out rounds/f01.blend|h01|c01
blender -b rounds/X.blend -P scripts/check_dims.py  -- --out checks/X      # D-checks
blender -b rounds/X.blend -P scripts/check_state.py -- --out checks/X      # camera grammar + state contents
scripts/render_round.sh X CAM_start,...                                    # 1280x720, 48 spp -> renders/X
```

Appended props (credit):
- Muse: `models/hp-floor-boards`, `hp-crate-and-display-case`, `hp-louvre-and-blind`, plus the exhibits in hp51/closing.
- Claude's folder and Codex's `blender-deliverables/` are not touched.

Departures are in DEPARTURES.md and history in PROGRESS.md.
