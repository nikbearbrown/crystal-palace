"""Write manifest.json + MANIFEST.md accounting for all 49 cataloged scans, and reference-vs-preview comparison images.
Run after run_scan_models.py and build_models.py. Reads ../Scans/catalog.json, objects.json, ledger.jsonl, mesh stats from the GLBs."""
import json
from pathlib import Path

from PIL import Image, ImageDraw

HERE = Path(__file__).resolve().parent
CAT = json.loads((HERE.parent / "Scans" / "catalog.json").read_text())["images"]
OBJ = {}
for _o in json.loads((HERE / "objects.json").read_text()):
    OBJ.setdefault(_o["source"], []).append(_o)
CHAIN = ["tripo_h31", "trellis2", "rodin_v25", "hunyuan_pro", "meshy_71"]

# figure -> (status, reason) for every catalog entry that is not modelled automatically
NOT_MODELLED = {
 1: ("excluded", "Engraved panorama of a fair on the frozen Thames: a crowded scene, not an object."),
 4: ("excluded", "Group portrait of people around a table: portrait, not an object."),
 6: ("excluded", "Portrait of a person."),
 21: ("excluded", "Interior view of the nave with many exhibits and visitors: a scene with no single principal object."),
 28: ("excluded", "Interior court scene of hangings and vessels: a scene."),
 29: ("excluded", "Visitors beside cotton machinery under the roof: machinery in a crowded scene."),
 30: ("excluded", "Envelope-machine demonstration at a stationery stand: machinery in a crowded scene."),
 36: ("excluded", "Interior view of Pugin's court with visitors: a scene."),
 37: ("excluded", "Fantastical crowded satire: not an object."),
 38: ("excluded", "Workers at woodworking machinery: a scene of people and machinery."),
 39: ("excluded", "Cartoon of figures in glass cases: caricature scene."),
 40: ("excluded", "Satirical street view: a scene."),
 41: ("excluded", "Crowded street scene: a scene."),
 42: ("excluded", "Interior scene of people in a cellar: a scene."),
 43: ("excluded", "Seated portrait of a person."),
 44: ("excluded", "Crowd of visitors; a lion statue on a plinth is visible at the top edge but is a small part of the image. A crop could be modelled if wanted."),
 45: ("excluded", "Cartoon of a crowd: caricature scene."),
 46: ("excluded", "Cartoon of social groups: caricature scene."),
 47: ("excluded", "Cartoon of people resting around a statue; the statue is a small part of the image. A crop could be modelled if wanted."),
 48: ("excluded", "Machinery stand with visitors: machinery and a display structure in a scene."),
 49: ("excluded", "Interior display of fabrics and cabinets with people: a scene."),
 50: ("excluded", "Cartoon of spectators before an enclosure: caricature scene."),
 51: ("excluded", "Cartoon contrasting peace and arms: caricature scene."),
 53: ("manual_review", "A satirical drawing of a statue on a pedestal: modellable as an object, but it is a racialised caricature of an enslaved woman. Not modelled without your decision."),
 56: ("excluded", "Coloured caricature scene: not an object."),
 57: ("excluded", "Coloured satirical frontispiece: a document and caricature scene."),
 58: ("excluded", "Ceremonial group scene inside the building: people and interior."),
 59: ("excluded", "Printed song broadside: a document."),
 60: ("excluded", "Punch cartoon of people with washing equipment: caricature scene."),
 61: ("excluded", "Cartoon of people at an opera reception: caricature scene."),
 65: ("excluded", "Interior scene at Sydenham (not the 1851 building) with colossi and visitors: a scene."),
 67: ("excluded", "Festival interior with orchestra and audience at Sydenham: a scene."),
 68: ("excluded", "Portrait of a person and her children."),
 69: ("excluded", "Night photograph of the building on fire: an event, not an object."),
 70: ("excluded", "Photograph of ruins and debris: not an object."),
 71: ("manual_review", "Souvenir blotting-book cover: a real object, but flat. It would model as a thin slab with a painted panel and gilt vine border. Say if you want it."),
 74: ("excluded", "Printed poster: a document."),
 75: ("excluded", "Printed advertisement: a document."),
}

state = {}
for line in (HERE / "ledger.jsonl").read_text().splitlines():
    if line.strip():
        r = json.loads(line)
        state.setdefault((r["model"], r["image_id"]), {}).update(r)

def attempts(slug):
    return [{"model": m, "status": state[(m, slug)].get("status"), "request_id": state[(m, slug)].get("request_id"),
             "error": state[(m, slug)].get("error")} for m in CHAIN if (m, slug) in state]

def tri_count(path):
    try:
        import trimesh
        sc = trimesh.load(path, force="scene")
        return int(sum(len(g.faces) for g in sc.geometry.values()))
    except Exception:
        return None

def model_entry(base, o):
    slug = o["slug"]
    built = (HERE / "glb" / f"{slug}.glb").exists() and (HERE / "blend" / f"{slug}.blend").exists()
    done = [m for m in CHAIN if state.get((m, slug), {}).get("status") == "completed"]
    e = {**base, "status": "modeled" if built else ("generated_not_built" if done else "failed_all_models"),
         "slug": slug, "input_image": f"scan-models/inputs/{slug}.png", "crop_box": o["crop"],
         "generator": done[0] if done else None, "attempts": attempts(slug),
         "blend": f"scan-models/blend/{slug}.blend" if built else None,
         "glb": f"scan-models/glb/{slug}.glb" if built else None,
         "preview": f"scan-models/previews/{slug}.png" if built else None,
         "comparison": f"scan-models/comparisons/{slug}.jpg" if built else None,
         "triangles": tri_count(HERE / "glb" / f"{slug}.glb") if built else None,
         "observed_result": o["observed"], "scale": o["scale"], "assumptions": o["assumptions"] + ["Repaired areas in the scan are not historical evidence."]}
    if built:
        ref = Image.open(HERE / "inputs" / f"{slug}.png").convert("RGB"); ref.thumbnail((700, 700))
        pre = Image.open(HERE / "previews" / f"{slug}.png").convert("RGB"); pre.thumbnail((700, 700))
        W = ref.width + pre.width + 30; Hh = max(ref.height, pre.height) + 40
        sheet = Image.new("RGB", (W, Hh), (30, 30, 30)); d = ImageDraw.Draw(sheet)
        d.text((10, 10), f"{slug}: reference scan (left) | generated model, {done[0]} (right)", fill=(230, 230, 230))
        sheet.paste(ref, (10, 30)); sheet.paste(pre, (ref.width + 20, 30))
        (HERE / "comparisons").mkdir(exist_ok=True)
        sheet.save(HERE / "comparisons" / f"{slug}.jpg", quality=90)
    return e


EXTRA_NOTE = {
 24: " Not modelled: stone slabs, the equestrian statuette, the timber tower and the visitors.",
 31: " Not modelled: the fire screen, wall trays, iron crest, pendant lamp, wall plaques, the second cabinet and the visitors.",
}

entries = []
for c in CAT:
    fig = c["figure_number"]
    base = {"figure_number": fig, "title": c["title"], "source_image": f"Scans/images/{c['filename']}",
            "description": c["description"], "catalog_uncertainties": c.get("uncertainties", [])}
    objs = OBJ.get(c["filename"])
    if objs and len(objs) == 1:
        e = model_entry(base, objs[0])
    elif objs:
        subs = [model_entry({}, o) for o in objs]
        built = sum(1 for m in subs if m["status"] == "modeled")
        e = {**base, "status": "modeled" if built == len(subs) else ("partial" if built else "failed_all_models"),
             "note": f"One scan, {len(subs)} separate objects, each cropped and modelled on its own." + EXTRA_NOTE.get(fig, ""), "models": subs}
    else:
        status, reason = NOT_MODELLED[fig]
        e = {**base, "status": status, "reason": reason}
    entries.append(e)

assert len(entries) == 49
(HERE / "manifest.json").write_text(json.dumps({"count": len(entries), "entries": entries}, indent=1))
counts = {}
for e in entries:
    counts[e["status"]] = counts.get(e["status"], 0) + 1
lines = ["# Scan model manifest", "", f"{len(entries)} cataloged scans accounted for: " +
         ", ".join(f"{k} {v}" for k, v in sorted(counts.items())) + ".", "",
         "| Fig | Title | Status | Generator | Triangles | Note |", "|---|---|---|---|---|---|"]
for e in entries:
    note = e.get("reason") or "; ".join(f"{a['model']}: {a['status']}" for a in e.get("attempts", []))
    if "models" in e:
        lines.append(f"| {e['figure_number']} | {e['title']} | {e['status']} | | | {e['note']} |")
        for m in e["models"]:
            lines.append(f"| {e['figure_number']} | - {m['slug']} | {m['status']} | {m.get('generator') or ''} | "
                         f"{m.get('triangles') or ''} | {'; '.join(a['model'] + ': ' + a['status'] for a in m['attempts'])} |")
        continue
    lines.append(f"| {e['figure_number'] or '-'} | {e['title']} | {e['status']} | {e.get('generator') or ''} | "
                 f"{e.get('triangles') or ''} | {note} |")
(HERE / "MANIFEST.md").write_text("\n".join(lines) + "\n")
print(counts)
