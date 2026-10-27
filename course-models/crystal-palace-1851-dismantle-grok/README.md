# Crystal Palace, Hyde Park 1851: HP-EMPTY and HP-DISMANTLE (Grok)

These are the after-exhibition states for storyboard shots **CP030** (HP-EMPTY: the hall emptied after the closing on 11 October 1851) and **CP031** (HP-DISMANTLE: partial dismantling in Hyde Park, 1852). They are Hyde Park 1851–52 only; nothing here is Sydenham.

They are built from the **same scripts** as the HP51 model, not from a copy:
1. `../crystal-palace-1851-transept-grok/scripts/build_transept.py -- --state empty|dismantle` builds the transept with no HP51 dressing (`dressing.py` only adds statuary, banners, textiles, machinery, planters and crowd when `--state hp51`).
2. `scripts/build_dismantle.py` adds the after-exhibition layer (collection `DISMANTLE_GROK`) and the CP030/CP031 cameras from `route/camera_route.json`.
   - **Both states:** Muse's plinths and benches are cleared and the fountain is drained.
   - **EMPTY:**
     - Half the vitrines are kept under dust sheets.
     - Muse's crates (closed sheathing) stand where the other cases stood.
     - The exhibitors' packing cases are at the machinery footprints, with the locomotive half boxed.
     - Straw litter, porters, two-man carrying poles, sack trucks and a policeman.
   - **DISMANTLE:**
     - Everything is out and the fountain is removed.
     - One tier-1 24 ft girder is lowered by sheer legs, with fall, blocks, sling, snatch block, crab winch, guys and tag lines.
     - The neighbouring girder is propped on two timber shores with head tree, wedges and rakers *before* its joint is released.
     - A scaffold tower and deck stand at the column head, with the joint keys being knocked out and a maul.
     - A glazier on the gutter lowers a pane box.
     - Component stacks: columns 5-4-3 on bearers, girders, sash bars and gutters, glass crates.
     - A horse trolley.
3. `scripts/render_dismantle.py` opens the exterior `x05.blend` and appends this round and Claude's west frame **read-only** through the exterior's `combine()`. It then swaps in Muse's furrow bay and applies `scripts/zones.py` at render time:
   - zone R: roof units stripped
   - zone G: glass off, with Muse's furrow bay minus its pane faces
   - the south transept vault glass is off
   - the home girder is hidden

   Nothing is saved; Claude's file is never written.

Run (from this folder): `scripts/build_round.sh d01 && scripts/render_round.sh d01 1280x720 48`, then the checks:
`blender -b ../crystal-palace-1851-exterior-grok/rounds/x05.blend -P scripts/check_dismantle.py -- --dismantle rounds/d01_dismantle.blend --state dismantle --claude ../crystal-palace-1851-claude/crystal-palace-1851.blend --out checks/d01_dismantle` (same for `empty`).

The frame is Claude's: feet, with the origin at the crossing and X east. Camera grammar: 1.6 m eye height above the standing surface (the CP031 joint detail stands on a 13.5 ft scaffold deck), 28/35/50 mm on 36 mm, no roll.

Credits:
- Muse: hp-crate-and-display-case, hp-roof-furrow-bay, display-plinth and park-bench, appended read-only from models/ on origin/main.
- Claude: the west frame, appended read-only at render time.

Judgment calls are in DEPARTURES.md.
