# Scan models

3D models of the object scans in `../Scans`, generated image-to-3D on fal.ai. Nothing in `Scans/` was changed.

**Chain per image:** Tripo H3.1 first; if it fails, Trellis 2; then Rodin, Hunyuan, Meshy (ordered by average triangles in the earlier bake-off). Tripo succeeded on all 9, so no fallback ran. Estimated spend $2.70 of the $50 cap (the ledger counts every submitted request; fal's own billing was not checked).

**Which scans:** 11 of the 49 scans are modelled: 9 are single objects (or structures), and fig 24 and fig 31 are scenes from which 2 and 5 objects were cropped, giving 16 models in all. 36 are excluded (portraits, cartoons, crowded scenes, documents) and 2 are held for review (fig 53, fig 71). All 49 are in `manifest.json` / `MANIFEST.md` with a reason.

| File | What |
|---|---|
| `manifest.json`, `MANIFEST.md` | every catalog entry: status, source, files, description, assumptions, scale, observed result |
| `inputs/` | images sent to the generator (two are crops of the scan) |
| `comparisons/` | reference next to the generated model |
| `previews/` | model render at an angle comparable to the reference |
| `blend/`, `glb/` | editable Blender file and exported GLB per model (not committed; ~65 MB and ~45 MB each) |
| `ledger.jsonl` | every request submitted |
| `objects.json` | per-model crop, scale, assumptions, preview angle |

Scripts, in order: `make_inputs.py`, `run_scan_models.py` (needs `FAL_KEY` in the environment), `build_models.py` (Blender headless), `make_manifest.py`.

**Read before using:** each model is one generated mesh of about 1.4 million triangles with a baked texture, not retopologised. Unseen sides are invented. Scale is estimated except where the manifest says otherwise. Fig 72 and fig 73 are rough proxies. In the fig 24 and fig 31 crops, Tripo fused backgrounds into the mesh (a wall slab behind the urn stand and the balloon-back chair, a box around the balustrade, a standing man beside the piano, a curtain beside the canopy chair), so those need manual clean-up; the obelisk is clean.
