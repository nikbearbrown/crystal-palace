#!/usr/bin/env python3
"""Build the two comparison images for osler-crystal-fountain:
compare-wellcome.jpg — Wellcome engraving fountain crop (left) + front render
compare-met.jpg      — MET Sydenham photograph crop (left) + 3/4 render
Run AFTER renders exist. Reference crops are pre-cut in work/ (see NOTES)."""
import os
from PIL import Image

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REFS = os.path.join(BASE, "refs")
WORK = os.path.join(BASE, "work")
OUT = os.path.join(BASE, "renders")


def side_by_side(left_path, right_path, out_path, height=1500):
    L = Image.open(left_path).convert("RGB")
    R = Image.open(right_path).convert("RGB")
    L = L.resize((round(L.width * height / L.height), height))
    R = R.resize((round(R.width * height / R.height), height))
    canvas = Image.new("RGB", (L.width + R.width + 12, height), (128, 128, 128))
    canvas.paste(L, (0, 0))
    canvas.paste(R, (L.width + 12, 0))
    canvas.save(out_path, quality=88)
    print("wrote", out_path, canvas.size)


# Wellcome: crop the fountain from the full plate first if needed
wcrop = os.path.join(WORK, "crop_wellcome_fountain.png")
if not os.path.exists(wcrop):
    im = Image.open(os.path.join(
        REFS, "Catalogue_of_the_great_exhibition_Wellcome_L0022578.jpg"))
    im.crop((270, 150, 620, 1030)).save(wcrop)
side_by_side(wcrop, os.path.join(OUT, "front.png"),
             os.path.join(OUT, "compare-wellcome.jpg"))

mcrop = os.path.join(WORK, "crop_met_fountain.png")
if not os.path.exists(mcrop):
    im = Image.open(os.path.join(
        REFS, "View_of_Transept,_Looking_South_MET_DP238264.jpg"))
    im.crop((1350, 1450, 1900, 2100)).save(mcrop)
side_by_side(mcrop, os.path.join(OUT, "three-quarter.png"),
             os.path.join(OUT, "compare-met.jpg"))
print("COMPARE DONE")
