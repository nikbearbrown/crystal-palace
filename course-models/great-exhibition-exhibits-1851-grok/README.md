# Great Exhibition 1851 — hero exhibits (Grok Bot)

Standalone hero-exhibit **assets** for the Hyde Park 1851 Crystal Palace (never Sydenham). Each exhibit is one Blender
collection under `EXH_ASSETS`, marked as an asset, origin at floor centre (z = 0, footprint centred, instance offset 0),
so it can be **appended or instanced** into the east block-outs (transept/dressing rounds) or Claude's west nave
without editing either host file. Units: metres in Blender, geometry authored in feet (FT = 0.3048).

| collection | storyboard | what | status |
|---|---|---|---|
| `EXH_KOHINOOR` | CP025 | Koh-i-Noor (pre-1852 Mughal cut, ~186 ct) on velvet under a glass bell inside the gilded "bird-cage", crown finial, draped iron safe as pedestal, brass rail R 6.5 ft | I (written accounts only) |
| `EXH_OSLER_CANDELABRUM` | CP025 (luxury) | F. & C. Osler cut-crystal candelabrum, 8 ft, 15 lights, prism shaft > 3 ft (Official Catalogue Cl.24 no.20) | C/I |
| `EXH_NASMYTH_HAMMER` | CP024 | Nasmyth steam hammer (Cl.6 no.236), proportions from the NMAH example; ram animated, 4 blows / 96 frames @ 24 fps | C/B |

Status key: C = catalogue/text-given, B = based on surviving object, I = interpretive.

## Files
- `scripts/build_exhibits.py` — builds `rounds/eNN.blend` (assets + a preview showroom stand). `blender -b -P scripts/build_exhibits.py -- --out rounds/e01.blend`
- `scripts/check_exhibits.py` — D-checks E01–E19 → `checks/eNN/checks.md`
- `scripts/render_round.sh eNN` — preview-stand renders → `renders/eNN/`
- `scripts/place_exhibits.py` — **placement helper**: append + instance any asset into any open host scene at `x,y,z,rot` (ft), optional cameras, clash report (`--check-only`), render-time hiding of crowd standing in a footprint (`--hide-clash`). Never saves the host.
- `scripts/place_test.sh eNN` — placement test: Koh-i-Noor + Osler in the transept r10 east block-outs, hammer in Claude's west nave (appended at render time, read-only).
- `route/exhibit_route.json` — preview cameras (eye 5.25 ft, no roll, 35/50 mm).

## Placing into a host
```
blender -b HOST.blend -P <this>/scripts/place_exhibits.py -P HOST_render.py -- \
   --lib <this>/rounds/e01.blend --place "EXH_NASMYTH_HAMMER:-456,4,0,0" --pcam "PL_x:-440,-30,5.25:-456,4,9:35" ...
```
Credit: assets by Grok Bot; showroom figures from the shared `figures.py` kit; Paxton column/girder silhouette from `parts1851.py`.
