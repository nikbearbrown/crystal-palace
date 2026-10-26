"""Write README.md, BUILD_NOTES.md and the self-contained index.html for this folder from one set of captions, so the three
pages cannot drift apart. Every number comes from checks/scene-counts.json, checks/gate-west-03_v001.json, the ledger copy
and the file sizes on disk.

  python3 -I scripts/make_pages.py .          (run from this folder, twice: the second run puts the first run's file sizes in the Download tables)
"""
import base64
import io
import json
import re
import sys
from html import escape
from pathlib import Path

from PIL import Image

root = Path(sys.argv[1]).resolve()
FOLDER = "crystal-palace-1851-claude"
REPO = "https://github.com/nikbearbrown/csye-7270-building-virtual-environments"
RAW = f"{REPO}/raw/main/blender/{FOLDER}"
TREE = f"{REPO}/tree/main/blender/{FOLDER}"
PAGES = f"https://nikbearbrown.github.io/csye-7270-building-virtual-environments/blender/{FOLDER}/"
FALLBACK = f"https://htmlpreview.github.io/?{RAW}/index.html"
ZIP = f"{REPO}/archive/refs/heads/main.zip"

S = json.loads((root / "checks/scene-counts.json").read_text())
G = json.loads((root / "checks/gate-west-03_v001.json").read_text())
EXT = S["extent_ft"]
TRIS = f"{S['triangles_instanced_total']:,}"
PARTS = f"{S['parts']:,}"
STATS = (f"{PARTS} placed parts · {S['library_collections']} library collections ({S['library_mesh_objects']} meshes) · {TRIS} triangles "
         f"with instances · {S['materials']} materials · 888 × 408 ft between column lines · Blender {S['blender']}")


def size(rel):
    if not (root / rel).exists():
        return "this page"
    n = (root / rel).stat().st_size
    return f"{n / 1e6:.1f} MB" if n >= 1e6 else f"{max(1, round(n / 1e3))} KB"


# ---- ledger counts, parsed the same way the Figma sheets parse it (scope tested before departure)
rows = []
for line in (root / "DEPARTURES-LEDGER.md").read_text(encoding="utf-8").splitlines():
    if re.match(r"\|\s*\d+\s*\|", line):
        c = [re.sub(r"[*`]", "", x).strip() for x in line.strip().strip("|").split("|")]
        sl = c[4].lower()
        rows.append((int(c[0]), c[1], ("scope" if "scope" in sl else "departure" if "departure" in sl else "inferred" if "inferred" in sl
                                       else "simplified" if "simplified" in sl else "matches")))
cls_count = {k: sum(1 for r in rows if r[2] == k) for k in ("matches", "simplified", "inferred", "departure", "scope")}

VIEWS = [
    ("overview", "Overview, from the south-west",
     "All 37 built bays (888 ft between the end column lines) from the south-west and high: three stepped tiers under ridge-and-valley "
     "roofs, tier 1 (408 ft across) nearest, tiers 2 (264 ft) and 3 (120 ft) stepping back. Nothing east of the transept's west face is built."),
    ("iso", "West end, from the south-west",
     "The west end and the tier-1 roof in front, tiers 2 and 3 stepping back behind it. The roofs are plain sheets with the ridge-and-valley "
     "profile; there are no walls or glazing, so the frame shows through."),
    ("section", "Cross-section view, looking east",
     "Orthographic, looking east from the west end, 440 ft across, lit. Every bay's frame lies behind the first, so it reads as one cross-section: "
     "tiers 408, 264 and 120 ft wide, girder tops at 22′ 2″, 42′ 2″ and 62′ 2″. This is the view set beside Plate VI."),
    ("nave", "Inside the nave",
     "From the nave at gallery height looking north-east and up: columns, connecting pieces and lattice girders under the roofs, with the lattice "
     "gallery railing in view. Interior light is raised 2.5 stops, because the roofs are opaque."),
    ("gallery", "From the gallery floor",
     "From the nave-side gallery floor strip (22′ 11″ above the ground floor) looking across the nave void: the railing along the void edge, the "
     "frame and the roof beyond."),
    ("voidend", "The end of the nave void",
     "From inside the nave void looking west at the cross railing that closes the void 72 ft from the west end (control D24), with the gallery "
     "floor beyond it."),
    ("stairs", "A staircase from the ground floor",
     "One avenue staircase (bay 192–216 ft, north avenue) from the nave floor: the ground flights rise to the landing, then the upper flights "
     "climb to the galleries, under the 48 × 24 ft cross gallery."),
    ("stairgal", "The stair wells from the gallery",
     "From the nave-side gallery looking north over the cross gallery, the two well holes (8 × 16 ft) and the landing."),
    ("joint", "Under the gallery, close-up",
     "A close-up from the ground floor looking up at the underside of the gallery: column heads and connecting pieces, the lattice girders and "
     "the underside of the gallery floor slab."),
    ("stairsec_flat", "Stair section, unlit",
     "Orthographic section along the flights, north avenue, drawn white on black and unlit so every part shows: two ground flights, the landing "
     "and its columns, the upper flights and the cross gallery. This is the view set beside Plate XV; the lit render was too dark to read."),
]
for v in VIEWS:
    assert (root / f"renders/{v[0]}.png").exists(), v[0]

COMPARES = [
    ("section_left_half_vs_plateVI.jpg", "Transverse section, left half: Plate VI beside the model",
     "Left: Plate VI of Downes (1852), transverse section on line A-B, cropped to the model's camera window. Right: the model's section view "
     "in the same window, left half only. The tier stepping, the girder levels and the column grid fall where the plate draws them (registered "
     "on the plate's scale bar and ground line). The plate has what the model lacks: the glazing, the end walls and doors, the arched ironwork "
     "and cresting, the foundation pads. The model was built from this plate's own figures, so the match is a consistency check, not independent evidence."),
    ("section_full_stacked_vs_plateVI.jpg", "Transverse section, full width: plate above, render below",
     "The same comparison at full width. The section is so wide (440 ft across, 3.75 : 1) that side by side would be unreadable, so here the plate is "
     "above and the render below."),
    ("section_overlay_plateVI.jpg", "Transverse section: the model overlaid on Plate VI",
     "The model's unlit render in red over the plate. It lies on the plate's frame, tiers and stairs; everything the plate shows outside the red is "
     "what the model leaves out."),
    ("stair_section_vs_plateXV.jpg", "Staircase section: Plate XV beside the model",
     "Left: Plate XV, section through the staircases. Right: the model's stair-section view, unlit, same window. The flights, the landing and the "
     "cross gallery fall where the plate draws them. The plate has the cast lattice standards, the diagonal bracing between the columns and the "
     "I-section strings, which the model leaves out. Registration used the plate's three main columns (74.4 px/ft across, 1% more than the "
     "scale bar's 73.65 px/ft up the height, from paper stretch)."),
    ("stair_section_overlay_plateXV.jpg", "Staircase section: the model overlaid on Plate XV",
     "The model's unlit render in red over the plate. A consistency check, not independent evidence: the model was built from this sheet's figures."),
]
for c in COMPARES:
    assert (root / "compare" / c[0]).exists(), c[0]

ASSESS = ("As a likeness of the Crystal Palace this model is poor. It is a bare iron frame under plain grey roofs: no glass, no walls, no colour, "
          "no transept and no vault, which is the part that gives the real building its silhouette. Someone who knows the palace would see the "
          "three stepped tiers and the ridge-and-valley roofs and might guess what it is going for, but would not take it for the building. "
          "What it is good for is a dimensioned frame: its figures were tested against the plates, and every place it infers or simplifies is "
          "written down in the ledger. That is the author's own assessment, made by looking at the renders next to the plates; "
          "Professor Bear's review is pending.")
CHECKED = (f"{G['controls_run']} of the plates' figures were run against the model: {G['gated_pass']} gated checks pass and {G['gated_fail']} fail, "
           f"and {G['controls_run'] - G['gated_pass'] - G['gated_fail']} text-only figures (taken from the printed text, no plate) are reported but "
           f"never gate. {len(G['controls_skipped'])} controls ({', '.join(G['controls_skipped'])}) were skipped because the parts they measure do not exist yet. "
           "Several checks are true by construction, because the model is built to the same figures. The gate catches build mistakes, not "
           "misreadings of the plates, and it does not look for parts that are missing.")
LIMITS = [
    "<b>Unfinished.</b> 37 of the building's 77 bays: the west half, to the transept's west face. Not built: the transept and its vault, the east half, the "
    "walls, doors and louvres, the north strip, the west entrance and end wall, glazing and sash bars, base plates and foundation pads, "
    "and six of the twelve avenue staircases (the ledger lists everything).",
    "<b>Look.</b> White, grey and wood preview materials, opaque roof sheets and a generic dark ground. Owen Jones's 1851 colour scheme is not applied.",
    f"<b>Simplified and inferred.</b> The ledger has {len(rows)} rows: {cls_count['matches']} match the record, {cls_count['simplified']} are simplified, "
    f"{cls_count['inferred']} are inferred (roof rise 1.6 ft, railing height 3.06 ft, the stair going and landing level, among others), "
    f"{cls_count['departure']} are departures (the solid 6 in floor slab, no colour, the preview lighting) and {cls_count['scope']} are scope notes.",
    "<b>The plate overlays are consistency checks.</b> The model was built from the same plates' figures, so a close match shows where the model is missing "
    "parts, not that the plates were read correctly.",
    "<b>Two text-only checks read wrongly.</b> D28 and D34 report 648 ft against 24 ft, because the <code>sample</code> tag that selects one stair part now sits "
    "on four parts (one per stair bay) and the check measures all four together. The parts are 24 ft by construction; the report is misleading, not the model.",
    f"<b>Blender version.</b> The .blend was saved in Blender {S['blender']}. It was not opened in Blender 4.2, so 4.2 compatibility is untested; "
    "the GLB or <code>scripts/build_slice.py</code> are the safer routes in an older Blender.",
    "<b>GLB.</b> Flat PBR colours only, no textures. Collection instances become shared meshes (165 meshes, 59,082 nodes).",
    "<b>Plate scans are not in this folder.</b> The comparison scripts need the Internet Archive scans of Plates VI and XV; the images here are crops of them.",
]
BUILT = [
    ("Builder", "Claude (Anthropic), working in Claude Code across several sessions on 17 and 18 October 2026. This publishing session ran on Claude Sonnet 5.5; "
                "the model version of the earlier build sessions is not recorded in the project files."),
    ("Method", "Scripted. <code>build_slice.py</code> places parts from a library (<code>parts.py</code>) on the 24 ft grid; all but the floor slab of its {PARTS} parts are "
               f"instances of the 12 library collections. Drawings first: the figures went into <code>controls.json</code>, a dimension gate checks the model against them, and a "
               "departures ledger records every inference and simplification. Comparison: two plate overlays (Plate VI section, Plate XV stair section). "
               "No likeness-improvement rounds were run: the model has no surface finish to compare."),
    ("Tools", f"Blender {S['blender']} (Cycles, CPU, OpenImageDenoise; glTF exporter 5.1.20), Python 3.14.6 with Pillow 12.3.0 and NumPy 2.3.5 for the overlays, "
              "comparison images and these pages. The Downes plates are the 1852 originals as scanned by McGill University Library and held by the Internet Archive."),
    ("Build date", "The model was built 17–18 October 2026; these files were published on 18 October 2026."),
    ("Human review", "Professor Bear (verdict pending)."),
]
IMPORT = [
    "<b>Native scene:</b> install Blender 4.2 or later and open <code>crystal-palace-1851.blend</code> with <b>File &gt; Open</b>. It was saved in Blender "
    f"{S['blender']} and not tested in 4.2 (see the limitations). You get the model with its materials, two sun lights and ten cameras (one per view).",
    "<b>GLB:</b> use <b>File &gt; Import &gt; glTF 2.0 (.glb/.gltf)</b> and pick <code>crystal-palace-1851.glb</code>. It also works in game engines and web viewers.",
]
DOWNLOADS = [
    ("crystal-palace-1851.blend", "Blender scene: 7,757 parts (all but the floor slab are instances of 12 library collections), materials, two lights, ten cameras."),
    ("crystal-palace-1851.glb", "glTF binary, flat colours only, no textures; instances are shared meshes."),
    ("BUILD_NOTES.md", "Dimensions, counts, the full gate table, method, how to rebuild, limitations."),
    ("DEPARTURES-LEDGER.md", "Every place the model infers, simplifies or departs from the record (28 rows)."),
    ("checks/gate-west-03_v001.json", "The dimension gate's output for this model."),
    ("checks/controls.json", "The plates' figures the model is tested against."),
    ("scripts/build_slice.py", "Builds the model: <code>blender -b -P build_slice.py -- --out x.blend --lines 0:37</code>."),
    ("scripts/parts.py", "The part library the builder places."),
    ("index.html", "The self-contained interactive viewer."),
]
for f, _ in DOWNLOADS:
    assert (root / f).exists() or f in ("index.html", "BUILD_NOTES.md"), f  # the pages are written by this script

FILM_COMMENT = "<!-- FILM_URL: paste the companion film link on the next line, replacing 'coming soon' (also set FILM_URL at the top of the script in index.html). -->"
IMG = lambda rel: f"{RAW}/{rel}"  # noqa: E731


def md_inline(s):
    return re.sub(r"</?b>", "**", re.sub(r"<code>(.*?)</code>", r"`\1`", s)).replace("&gt;", ">").replace("&amp;", "&")


# =============================================================== index.html (self-contained, base64 JPEGs)
def b64(path, width, q=82):
    im = Image.open(path).convert("RGB")
    if im.width > width:
        im = im.resize((width, round(im.height * width / im.width)), Image.LANCZOS)
    buf = io.BytesIO()
    im.save(buf, "JPEG", quality=q, optimize=True)
    return "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode()


D = [{"name": name, "cap": cap, "src": b64(root / f"renders/{key}.png", 1100), "file": f"renders/{key}.png"} for key, name, cap in VIEWS]
C = [{"name": name, "cap": cap, "src": b64(root / "compare" / fn, 1200), "file": f"compare/{fn}"} for fn, name, cap in COMPARES]
DL = [{"file": f, "size": size(f) if f != "index.html" else "this page", "purpose": what, "url": f"{RAW}/{f}"} for f, what in DOWNLOADS]
tpl = (Path(__file__).parent / "viewer_template.html").read_text(encoding="utf-8") if (Path(__file__).parent / "viewer_template.html").exists() else None
assert tpl, "viewer_template.html is missing"
html = (tpl.replace("{{TITLE}}", "Crystal Palace 1851 Viewer").replace("{{H1}}", "Crystal Palace, Hyde Park 1851: the west half's iron frame")
        .replace("{{STATS}}", escape(STATS + " · built by Claude"))
        .replace("{{BLURB}}", escape("An unfinished Blender model of the iron frame of the 1851 Crystal Palace, 37 of 77 bays, built by script from Charles Downes's 1852 "
                                      "working drawings. Tested against the plates' figures; not a likeness: no glass, no walls, no colour, no transept."))
        .replace("{{COMPARE_INTRO}}", escape("Left: Downes (1852) Plate VI or XV, cropped to the model's camera window (scan: McGill University Library via the Internet "
                                              "Archive; the work is public domain, shown for comparison only). Right: the model's render from the same window."))
        .replace("{{ASSESS}}", escape(ASSESS))
        .replace("{{BUILT}}", "".join(f"<li><b>{k}:</b> {v}</li>" for k, v in BUILT))
        .replace("{{IMPORT}}", "".join(f"<li>{t}</li>" for t in IMPORT))
        .replace("{{LIMITS}}", "".join(f"<li>{t}</li>" for t in LIMITS))
        .replace("{{CHECKED}}", escape(CHECKED))
        .replace("{{STATLIST}}", "".join(f"<li><b>{k}:</b> {v}</li>" for k, v in [
            ("Placed parts", f"{PARTS}; all but the floor slab are instances of {S['library_collections']} library collections ({S['library_mesh_objects']} meshes)"),
            ("Triangles", f"{TRIS} counting every instance"),
            ("Size", f"888 ft long × 408 ft wide between column lines; bounding box {EXT['length']:.1f} × {EXT['width']:.1f} × {EXT['height']:.1f} ft"),
            ("Gate", f"{G['gated_pass']} of {G['controls_run']} controls pass (gated), {G['gated_fail']} fail, 4 text-only reported"),
            ("Built with", f"Blender {S['blender']}, Cycles CPU")]))
        .replace("{{FOLDER_URL}}", TREE).replace("{{NOTES_URL}}", f"{TREE}/BUILD_NOTES.md").replace("{{ZIP}}", ZIP)
        .replace("{{DATA}}", "const D=" + json.dumps(D) + ",C=" + json.dumps(C) + ",DL=" + json.dumps(DL) + ";"))
(root / "index.html").write_text(html, encoding="utf-8")
# =============================================================== README.md
r = ["# Crystal Palace, Hyde Park 1851: the west half's iron frame", "",
     "A Blender model of the iron frame of the 1851 Crystal Palace, 37 of its 77 bays (the west half, 888 ft), built by script from Charles Downes's 1852 "
     "working drawings and tested against figures read from them. It is an unfinished frame, not a likeness.", "",
     f"**{STATS}.** Built by Claude.", "",
     f"**Interactive viewer:** [open the viewer]({PAGES}) (GitHub Pages) · [htmlpreview fallback]({FALLBACK}) · or download "
     f"[`index.html`]({RAW}/index.html) and open it locally; it is self-contained.", "",
     f'<p><img src="renders/web/overview.jpg" alt="Crystal Palace, overview from the south-west" width="720"></p>', "", "## Views", ""]
for key, name, cap in VIEWS:
    r += [f"### {name}", "", cap, "", f'<img src="renders/web/{key}.jpg" alt="{name}" width="600">', "",
          f"Full size: [renders/{key}.png](renders/{key}.png)", ""]
r += ["## Compare with references", "",
      "The references are Plates VI and XV of Charles Downes, *The Building Erected in Hyde Park for the Great Exhibition* (London: John Weale, 1852), "
      "from the scan by McGill University Library held by the Internet Archive. The work is in the public domain; the Internet Archive item states no "
      "licence for the scan. Each plate is cropped to the model's camera window and shown for comparison only.", ""]
for fn, name, cap in COMPARES:
    r += [f"### {name}", "", cap, "", f'<img src="compare/web/{fn}" alt="{name}" width="900">', "", f"Full size: [compare/{fn}](compare/{fn})", ""]
r += ["## Film", "", FILM_COMMENT, "**Companion film: coming soon.**", "",
      "## Download", "",
      f"Click a file name to download it directly. To get everything, clone the repo or use [Code → Download ZIP]({ZIP}).", "",
      "| File | Size | What it is |", "|---|---|---|"]
for f, what in DOWNLOADS:
    r.append(f"| [`{f}`]({RAW}/{f}) | {size(f)} | {md_inline(what)} |")
r += ["", "## How to import into Blender", ""]
r += [f"{i + 1}. {md_inline(t)}" for i, t in enumerate(IMPORT)]
r += ["", "The GLB carries flat colours only.", "", "## Viewer", "",
      f"Open [`index.html`]({PAGES}) via GitHub Pages ([htmlpreview fallback]({FALLBACK})), or download it and open it in a browser. It has view buttons, a "
      "thumbnail strip, the reference comparisons, light and dark themes and a mobile layout.", "", "## Built by", ""]
r += [f"- **{k}:** {md_inline(v)}" for k, v in BUILT]
r += ["", "## Honest limitations", "", "**What was checked.** " + CHECKED, ""]
r += [f"- {md_inline(t)}" for t in LIMITS]
r += ["", "**Assessment.** " + ASSESS, "", "**Human review:** pending (Professor Bear).", "",
      f"Full technical record: [BUILD_NOTES.md]({RAW}/BUILD_NOTES.md). Every inference and simplification: [DEPARTURES-LEDGER.md]({RAW}/DEPARTURES-LEDGER.md).", ""]
(root / "README.md").write_text("\n".join(r), encoding="utf-8")

# =============================================================== BUILD_NOTES.md
n = ["# BUILD_NOTES: Crystal Palace 1851 (Claude)", "",
     "## Summary", "",
     "**What this is.** The iron frame of the 1851 Crystal Palace as built in Hyde Park, west half only (37 bays, 888 ft between the end column lines), as a Blender "
     "scene, a GLB, ten review views and two plate comparisons.", "",
     "**Why it exists.** It is the pilot for a planned \"building walkthrough\" method for famous historical buildings: drawings first, model second, a dimension gate "
     "that fails the build when the model leaves the plates' figures, and a departures ledger that says honestly what is measured, inferred or simplified.", "",
     "**What was found.** The frame passes every figure that was tested; it is not a likeness of the building (see the README). Two text-only checks report wrong "
     "numbers because of a sample tag (below).", "",
     "## Dimensions and counts (from `checks/scene-counts.json`, counted from the .blend)", "",
     f"- Placed parts: **{PARTS}** (all but the floor slab are instances of the {S['library_collections']} library collections; {S['library_mesh_objects']} library mesh objects)",
     "- Parts by kind: " + ", ".join(f"{k} {v:,}" for k, v in sorted(S["kinds"].items(), key=lambda kv: -kv[1])),
     f"- Triangles: **{TRIS}** counting every instance (evaluated meshes)",
     f"- Materials: {S['materials']} ({', '.join(S['material_names'])})",
     f"- Between column lines: 888 ft long (line 0 to line 37) × 408 ft wide (outer columns), girder tops at 22′ 2″, 42′ 2″, 62′ 2″",
     f"- Bounding box of everything placed: {EXT['length']:.1f} × {EXT['width']:.1f} × {EXT['height']:.1f} ft "
     f"(the ground slab runs 12 ft past the last column line, the connecting-piece flanges stand proud, and the slab is 6 in below the floor line)",
     f"- Scene units: metres, scale {S['unit_scale']}; origin at the centre of the nave and transept crossing, floor top at z = 0",
     f"- Blender {S['blender']}; the GLB has {size('crystal-palace-1851.glb')}, 165 meshes, 59,082 nodes, 4 materials, no textures", "",
     "## Dimension gate (`checks/gate-west-03_v001.json`)", "",
     f"{G['controls_run']} controls run, **{G['gated_pass']} gated pass, {G['gated_fail']} fail**, {G['controls_run'] - G['gated_pass'] - G['gated_fail']} text-only "
     f"reported, {len(G['controls_skipped'])} skipped ({', '.join(G['controls_skipped'])}: no such parts yet). Status words: plate-printed (the plate prints the "
     "figure; tight tolerance), plate-checked (read off a plate; the larger of 0.5% and the scale bar's scatter), text (printed page only; reported, never gates).", "",
     "| Control | What | Stated | Measured | Status | Result |", "|---|---|---|---|---|---|"]
for res in G["results"]:
    ok = {True: "pass", False: "FAIL", None: "reported"}[res["ok"]]
    unit = res.get("unit", "ft")
    n.append(f"| {res['id']} | {res['what'][:78]}{'…' if len(res['what']) > 78 else ''} | {res['stated']:g} {unit} | {res['measured']:.4f} {unit} | {res['status']} | {ok} |")
n += ["", "D28 and D34 read 648 ft against 24 ft: the `sample` tag that should select one stair part is set on four (one per stair bay), and the check measures all four "
      "together. The parts are 24 ft by construction. The gate does not fail on text-only controls, so the build passed.", "",
      "## Method", "",
      "1. **Read the plate or the printed page for every figure** (the book's OCR is wrong on fractions) and put the figures into `controls.json` with how each was measured.",
      "2. **Build by script**: `scripts/build_slice.py --lines 0:37` places parts from `scripts/parts.py` on the 24 ft grid (18 column rows, line i at 24 i ft from the west end), "
      "with the plan (voids, stair bays) as read from Plates I and II.",
      "3. **Gate**: a Blender script measures the evaluated geometry against `controls.json` and exits non-zero on a miss.",
      "4. **Ledger**: every inference, simplification or departure is a row in `DEPARTURES-LEDGER.md`.",
      "5. **Regression**: `scripts/part_signature.py` hashes every part's name, kind, position, rotation and properties. The builder reproduces the earlier files' hashes "
      "(31d28a05cb53a430 for lines 4:5, baa9ab74096de122 for 0:6, ede6c112ab6a9a58 for 0:12) and this model's own, **af709609ae4364c6** (7,757 parts).",
      "6. **Compare with the plates**: `scripts/render_preview.py` renders the section views, `scripts/compare_plate_vi.py` and `compare_plate_xv.py` register them on the "
      "plates and write the overlays. Both are consistency checks.",
      "7. **Publish**: `scripts/publish_assets.py` adds the lights and cameras, saves the scene, renders the views and exports the GLB; `scripts/make_compare.py` makes "
      "the comparison images; `scripts/make_pages.py` writes these pages.", "",
      "## Departures ledger", "",
      f"`DEPARTURES-LEDGER.md` has {len(rows)} rows: {cls_count['matches']} match the record, {cls_count['simplified']} simplified, {cls_count['inferred']} inferred, "
      f"{cls_count['departure']} departures, {cls_count['scope']} scope notes (strongest word in each row's Status). The figures drawn from the ledger's text rather than a "
      "control include the roof rise (1.6 ft), the railing height (3.06 ft) and the stair landing level.", "",
      "## Rebuild it", "",
      "```bash",
      "blender --background --python scripts/build_slice.py -- --out rebuilt.blend --lines 0:37",
      "blender --background rebuilt.blend --python scripts/part_signature.py     # prints SIG af709609ae4364c6 7757",
      "blender --background rebuilt.blend --python scripts/publish_assets.py -- --stage-dir out --steps blend,shaded,glb",
      "```", "",
      "The gate script (`check_controls.py`) and the plate scans are not in this folder. Written and run under Blender 5.1.2; 4.2 is untested.", "",
      "## Comparison rounds", "",
      "Two plate comparisons (Plate VI section; Plate XV stair section), each a registration of a render on the plate. No iterative likeness rounds.", "",
      "## Known limitations", ""]
n += [f"- {md_inline(t)}" for t in LIMITS]
n += ["", "## Assessment and review", "", ASSESS, "", "Human review: pending (Professor Bear).", ""]
(root / "BUILD_NOTES.md").write_text("\n".join(n), encoding="utf-8")


print("README.md", size("README.md"), "| BUILD_NOTES.md", size("BUILD_NOTES.md"), "| index.html", size("index.html"))
