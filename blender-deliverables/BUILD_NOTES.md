# Build notes — Crystal Palace conversion

Built October 23, 2026 for Nik Bear Brown. Builder: Codex.

## Source and dimensions

Imported `Crystal Palace_FBX.FBX` (SHA-256: b4e56895c16ea7a9924e5da45c4294a90f1588e2a8cc1405184cc087238532cb). The MAX, 3DS, DWG and ZIP source files were not modified. Original FBX: 11 meshes, 4,538,403 vertices and 6,832,098 polygons. Full-resolution local native retains all those polygons. Transform matrices were baked into mesh coordinates while retaining world positions and UVs.

Structure bounds: 124.00 × 36.82 × 34.67 scene meters. Complete scene including ground: 234.58 × 184.42 × 42.15. Imported scale is retained; these are audited model bounds, not verified real-building dimensions. Detailed per-object bounds are in audit.json.

Course copy: 2,032,048 vertices, 2,040,388 polygons, 2,143,430 triangles; 11 meshes, 16 materials, 10 packed texture images (audit.json also counts the transient Render Result). The STRUCTURE decimation ratio is 0.20; other meshes are unchanged. Packed images in this copy are capped at 2048 px. Full-resolution local native preserves source-resolution images.

## Material decisions

The importer produced no image textures and GLASS had no assigned material. Legacy shaders also imported with zero shader Weight and inappropriate metal values. Replaced them with Principled shaders and assigned the glazing material. Glass: transmission 1, roughness 0.075, IOR 1.45; water IOR 1.333. Assigned supplied concrete, stone, grass and one oak-board map using existing UVs. Metal glossiness is inverted into roughness; supplied bump maps provide subtle surface variation. Full mapping decisions are in audit.json. These are inferred assignments, not recovery of a hidden original material network. Original alternate maps remain untouched.

## Comparison round 1

Inspected imported source and reduced geometry renders at the same camera. Overall roof arches, facade bays, stairs, terrace balustrades and garden outline remain visually aligned at overview scale. Fine tracery may differ after reduction. Examined actual Cycles overview, front, entrance and reverse renders. Repaired glazing reveals the frame and interior; the original Workbench view is opaque. No claim of matching an unavailable original Corona render or historical photograph.

## Comparison round 2

Reopened and rendered the full-resolution native file at 64 samples, beside the reduced course copy at 32 samples. Overall silhouette and main ironwork align at the provided overview resolution. Texture resolution and sampling differ. Fine-detail equivalence is not established by the overview. Professor Bear's visual acceptance is pending.

## Verification and export

Both native files reopened in Blender 5.1.2. Verified all 10 used images are packed, full native polygon count matches the source, and glazing has an assigned material. GLB binary header/length checked, embedded images checked, and GLB reimported in Blender. See verification.json. The GLB has 10 images, 16 materials, and 11 meshes. Draco compression is required. It carries image textures and transmission, not flat colors only. Blender procedural bump and lighting do not survive exactly. No animation or collision testing was performed.

## Reproduce

With Blender 5.1.2 available and the FBX plus maps in a source directory:

```bash
CRYSTAL_SOURCE=/absolute/path/to/the-crystal-palace CRYSTAL_OUTPUT=/absolute/path/to/new-output blender -b --python scripts/build.py
```

The build script saves the full-resolution native file in the output directory's parent and the reduced package within the output directory. It produces source/current geometry images, four Cycles views and the GLB. Do not use an output folder containing an earlier deliverable you want to preserve. Gallery generation and final full-resolution verification were separate packaging steps.

## Limitations

The source geometry and scale are inherited, not a verified historical reconstruction. The source folder supplied no historical reference images or original renderer previews. Texture assignments are inferred from names and visual appearance; the original Corona/Scanline shaders were not recovered. The public copy reduces only STRUCTURE to 20% of its original triangle count, so fine ornament can differ; the full-resolution native file remains beside the source assets. Ten used images are packed; unused alternate maps are left in the source folder. The GLB contains textures and transmission materials, but procedural bump detail and Blender lighting do not transfer exactly; a Draco-capable importer is required. No collision, rig, or animation is provided. Native files were reopened in Blender 5.1.2; Blender 4.2 compatibility is unverified. Human review: Professor Bear — pending.
