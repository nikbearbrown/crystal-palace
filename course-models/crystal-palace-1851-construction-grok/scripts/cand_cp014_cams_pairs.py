"""2026-11-11 pairs for the CP014 cams CANDIDATE (DEPARTURES KD14-KD16; no verdict, NOT live).
before = live rounds/k01.blend (md5 2c1e3235), after = rounds/candidates/k01_cp014cams.blend, both from scripts/render_cp014_cams.sh
(one cam per Blender session, look v1 era 1850 / studio, 24 spp; after exposure re-matched to the before mean luma)
-> survey look/pairs_geo/CANDIDATE_CP014_cams_<cam>_{before,after,pair,detail_pair}.png + CANDIDATE_CP014_cams_contact_after.png"""
from PIL import Image, ImageDraw, ImageFont, ImageStat
import os, shutil
H = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); OUT = "/workspace/crystal-palace-survey/look/pairs_geo"
R = f"{H}/renders/candidates/cp014_cams_20261111"
try: FN = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 18)
except Exception: FN = ImageFont.load_default()
CAMS = {  # cam: (exp before, exp after, before note, after note, detail crop box)
    "roof": (0.40, 0.40, "old 12 in box gutter; labels off the top of the frame", "p.15 main gutter + shoe, red cut faces; 8 labels in frame (KD14-15)", (420, 380, 1060, 720)),
    "gutter": (0.40, 0.42, "old 12 in box gutter + lead plate", "p.15 main gutter: plank, false bottom, shoe (KD14)", (330, 400, 970, 720)),
    "base": (0.40, 0.30, "old 2.4 ft plate, socket ribs, black cut faces", "Pl. VIII base piece, 7 in outlet, grey concrete section (KD14, KD16)", (60, 330, 620, 720)),
    "whole": (-0.13, -0.13, "KEEP: base plate + concrete merge in red", "concrete cut in concrete grey (KD16 only)", (190, 960, 470, 1140)),
}
def pair(A, B, LB, LA, out):
    S = Image.new("RGB", (A.width + B.width + 10, max(A.height, B.height) + 56), (20, 20, 20)); S.paste(A, (0, 56)); S.paste(B, (A.width + 10, 56))
    d = ImageDraw.Draw(S)
    for i, t in enumerate(LB.split("\n")): d.text((8, 6 + 22 * i), t, fill=(255, 255, 255), font=FN)
    for i, t in enumerate(LA.split("\n")): d.text((A.width + 18, 6 + 22 * i), t, fill=(255, 255, 255), font=FN)
    S.save(out); print("PAIR", out); return out
for c, (eb, ea, nb, na, box) in CAMS.items():
    f = f"CP014_drain_{c}_start.png"; a, b = f"{R}/before/{f}", f"{R}/after/{f}"; P = f"{OUT}/CANDIDATE_CP014_cams_{c}"
    shutil.copy(a, P + "_before.png"); shutil.copy(b, P + "_after.png")
    A, B = Image.open(a).convert("RGB"), Image.open(b).convert("RGB")
    la, lb = ImageStat.Stat(A.convert("L")).mean[0], ImageStat.Stat(B.convert("L")).mean[0]
    pair(A, B, f"BEFORE live k01 {c} (exp {eb}, luma {la:.2f})\n{nb}", f"AFTER CANDIDATE (exp {ea}, luma {lb:.2f})\n{na}", P + "_pair.png")
    k = 2; w, h = box[2] - box[0], box[3] - box[1]
    pair(A.crop(box).resize((w * k, h * k)), B.crop(box).resize((w * k, h * k)), f"BEFORE {c} detail (same crop, x{k})", f"AFTER {c} detail (same crop, x{k})", P + "_detail_pair.png")
    print("LUMA", c, round(la, 2), round(lb, 2))
# contact sheet: after state of all four CP014 shots (whole portrait left, the three landscape shots stacked right)
W_ = Image.open(f"{R}/after/CP014_drain_whole_start.png").convert("RGB")
ims = [Image.open(f"{R}/after/CP014_drain_{c}_start.png").convert("RGB") for c in ("roof", "gutter", "base")]
th = (W_.height - 2 * 10) // 3; tw = int(1280 * th / 720); ims = [i.resize((tw, th)) for i in ims]
S = Image.new("RGB", (W_.width + 10 + tw, W_.height + 40), (20, 20, 20)); S.paste(W_, (0, 40))
for j, i in enumerate(ims): S.paste(i, (W_.width + 10, 40 + j * (th + 10)))
d = ImageDraw.Draw(S); d.text((8, 10), "CP014 cams CANDIDATE (after, not live): whole | roof / gutter / base. Same Downes VIII base piece, p.15 main gutter, cut faces in all four", fill=(255, 255, 255), font=FN)
S.save(f"{OUT}/CANDIDATE_CP014_cams_contact_after.png"); print("CONTACT", f"{OUT}/CANDIDATE_CP014_cams_contact_after.png")
