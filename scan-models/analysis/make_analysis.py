"""Build ANALYSIS.md and RIFF.md for the 16 scan models from findings.json (one reader's critique, 2026-11-03).
Facts (triangles, size, hashes) come from facts/*.json, objects.json and ledger.jsonl; the judgments are in findings.json."""
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
F = json.loads((HERE / "findings.json").read_text())
OBJ = {o["slug"]: o for o in json.loads((ROOT / "objects.json").read_text())}
LED = {}
for line in (ROOT / "ledger.jsonl").read_text().splitlines():
    if line.strip():
        r = json.loads(line)
        LED.setdefault((r["model"], r["image_id"]), {}).update(r)


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()[:12]


TIERS = [
    ("Reproduces its reference", ["fig-52_greek-slave", "unnumbered_watherston-brogden-vase", "fig-54_elkington-jewel-cabinet",
                                  "fig-03_tea-service", "fig-24a_obelisk"]),
    ("Good object, contaminated by the scene around it (usable after cleanup)",
     ["fig-31a_inlaid-piano-and-stool", "fig-31b_tufted-canopy-chair", "fig-31c_gilt-urn-stand", "fig-31d_balloon-back-chair",
      "fig-27_indian-elephant-howdah"]),
    ("Starting mesh only", ["fig-24b_boulder-pile", "fig-31e_cast-iron-balustrade", "fig-33_model-working-class-home",
                            "fig-63_tower-conversion-design", "fig-73_centenary-model"]),
    ("Does not reproduce its reference", ["fig-72_brompton-boilers"]),
]

out = ["# Analysis: how well the 16 scan models match their reference images", "",
       "Made 2026-11-03 with the `blender-analysis` skill. One reader's critique from the comparison sheets in "
       "`analysis/sheets/`, which put each reference crop beside the model rendered from a comparable angle, plus a view "
       "the reference never shows. It judges likeness to the picture only. It says nothing about how a model behaves in "
       "a game engine, which was not tested.", "",
       "## Summary", "",
       F["summary"], "", "| Group | Models |", "|---|---|"]
for name, slugs in TIERS:
    out.append(f"| {name} | {', '.join(s.split('_', 1)[1] if '_' in s else s for s in slugs)} |")
out += ["", "## Reading the verdicts", "",
        "`matches`, `partly`, `does not`, or `cannot judge` (the reference does not show it). Every gap names its cause: "
        "**model** (the generator departed from the reference), **reference** (the picture cannot show it) or "
        "**comparison** (the comparison is unfair). A view the reference never shows is only described, never compared. "
        "Triangle counts are facts about the file; every model is about 1.4 million triangles and none is watertight, so the "
        "count says nothing about quality.", ""]
riff = ["# RIFF.md: reference against model, one row per pair", "",
        "| Pair | Reference (source, crop, sha256) | Model (file, sha256, camera) | Observation (visible) | Cause | Narration | Next experiment |",
        "|---|---|---|---|---|---|---|"]
for name, slugs in TIERS:
    out += [f"## {name}", ""]
    for s in slugs:
        o, f = OBJ[s], F["models"][s]
        facts = json.loads((HERE / "facts" / f"{s}.json").read_text())
        led = LED.get(("tripo_h31", s), {})
        out += [f"### {s}", "",
                f"- **Reference:** `Scans/images/{o['source']}`, crop `{o['crop'] or 'whole image'}`, input `inputs/{s}.png` (sha256 {sha(ROOT / 'inputs' / (s + '.png'))}…).",
                f"- **Made by:** Tripo H3.1 through fal.ai, request `{led.get('request_id', 'unknown')}` (ledger). One image, no second view.",
                f"- **Model:** `glb/{s}.glb` (sha256 {facts['sha256'][:12]}…), {facts['triangles']:,} triangles, "
                f"{facts['dimensions'][0]} x {facts['dimensions'][1]} x {facts['dimensions'][2]} m as built, not watertight. "
                f"Claimed scale: {o['scale']['dim']} = {o['scale']['metres']} m, {o['scale']['basis']}.",
                f"- **Sheet:** `analysis/sheets/{s}.jpg`.", "",
                "| Criterion | Verdict | What is visible | Cause |", "|---|---|---|---|"]
        for crit, verdict, what, cause in f["rows"]:
            out.append(f"| {crit} | {verdict} | {what} | {cause} |")
        out += ["", f"**Good for as it stands:** {f['good_for']}", "", "**Next experiments:** " + " ".join(f"({i + 1}) {e}" for i, e in enumerate(f["next"])), ""]
        worst = [r for r in f["rows"] if r[1] in ("does not", "partly")]
        pick = worst[0] if worst else f["rows"][0]
        riff.append(f"| {s} | `{o['source']}` crop {o['crop']}, {sha(ROOT / 'inputs' / (s + '.png'))} | `glb/{s}.glb` {facts['sha256'][:12]}, "
                    f"azimuth {o['azimuth']} | {pick[0]}: {pick[2]} | {pick[3]} | {f['riff']} | {f['next'][0]} |")
out += ["## What the failures have in common", "", F["pattern"], "", "## Limits", "",
        "Judgments are the analyst's, read from rendered stills. Colour is not judged where the reference is a monochrome print or a "
        "hand-coloured plate. Hidden sides are called invention and are not scored. No likeness metric was computed: silhouette "
        "overlap and image similarity are unreliable across perspective, and the height-to-width ratios in `facts/` are a rough "
        "check only (a model with fused background or a different crop has a different ratio for reasons that are not the likeness).", ""]
(HERE / "ANALYSIS.md").write_text("\n".join(out))
(HERE / "RIFF.md").write_text("\n".join(riff) + "\n")
print(len(out), len(riff))
