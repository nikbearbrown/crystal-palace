"""Cut the model inputs from the cataloged scans. Originals in Scans/images are only read."""
import json
from pathlib import Path
from PIL import Image

HERE = Path(__file__).resolve().parent
SCANS = HERE.parent / "Scans" / "images"
(HERE / "inputs").mkdir(exist_ok=True)
for o in json.loads((HERE / "objects.json").read_text()):
    im = Image.open(SCANS / o["source"]).convert("RGB")
    if o["crop"]:
        im = im.crop(tuple(o["crop"]))
    im.save(HERE / "inputs" / f"{o['slug']}.png")
    print(o["slug"], im.size)
