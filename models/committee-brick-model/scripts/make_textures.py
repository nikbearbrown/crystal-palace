#!/usr/bin/env python3
"""Generate the procedural textures for committee-brick-model.

Run with the system Python (needs PIL):
    python3 scripts/make_textures.py

Everything is drawn, nothing is copied from a photograph.  The model
is a 1:500 miniature, so the textures are deliberately *fine*:
brick courses are drawn at their true model scale (~3 px per course)
and read as masonry grain, not as individual bricks.

Outputs (in ../textures/):
    brick.png       tileable running-bond brick, one tile = 24 mm of model wall
    arcade.png      one ground-floor arch bay (stone pier + dark opening)
    clerestory.png  the rotunda drum's window band, 28 windows per wrap
    dome.png        sheet-iron dome skin, 24 rib bays per wrap
    archwindow.png  glazing for the great arch panels (5 vertical lights)
    wood.png        base-board wood grain
"""
import os
import random
from PIL import Image, ImageDraw

random.seed(1850)
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "textures")
os.makedirs(OUT, exist_ok=True)


def save(img, name):
    path = os.path.join(OUT, name)
    img.save(path)
    print("wrote", path, img.size)


# ---------------------------------------------------------------- brick
def brick():
    S = 512
    img = Image.new("RGB", (S, S), (146, 136, 120))  # mortar
    d = ImageDraw.Draw(img)
    course = 3          # px per course (2 brick + 1 mortar) ~ true 1:500 scale
    brick_h = 2
    brick_l = 26        # px per brick length, staggered running bond
    base = (126, 64, 46)          # deep red-brown brick mid tone
    for y in range(0, S, course):
        row = y // course
        off = (brick_l // 2) if row % 2 else 0
        tone = random.uniform(-7, 7)
        for x in range(-brick_l, S + brick_l, brick_l):
            j = random.uniform(-13, 13)
            col = tuple(max(0, min(255, int(c + tone + j))) for c in base)
            if random.random() < 0.06:      # occasional dark burnt header
                col = (80, 48, 38)
            d.rectangle([x + off + 1, y, x + off + brick_l - 1, y + brick_h - 1],
                        fill=col)
    save(img, "brick.png")


# ---------------------------------------------------------------- arcade
def arcade():
    # One bay: 256x256. Cream stone piers at the edges, dark round-arch
    # opening between. Tiled horizontally by UV (u = length / bay width).
    S = 256
    img = Image.new("RGB", (S, S), (188, 174, 146))  # stone
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, S, 10], fill=(170, 156, 128))          # top band
    d.rectangle([0, S - 12, S, S], fill=(164, 150, 122))      # plinth
    # opening: rectangle + semicircle top, centred, pier ~22% each side
    x0, x1 = 58, S - 58
    spring = 96
    d.rectangle([x0, spring, x1, S - 12], fill=(72, 68, 72))
    d.pieslice([x0, spring - (x1 - x0) // 2, x1, spring + (x1 - x0) // 2],
               180, 360, fill=(72, 68, 72))
    # arch ring
    d.arc([x0 - 7, spring - (x1 - x0) // 2 - 7, x1 + 7, spring + (x1 - x0) // 2 + 7],
          180, 360, fill=(202, 190, 164), width=6)
    # faint inner sheen so the opening is not a flat void
    d.rectangle([x0 + 16, spring + 30, x0 + 30, S - 30], fill=(94, 90, 94))
    save(img, "arcade.png")


# ---------------------------------------------------------------- clerestory
def clerestory():
    W, H = 1400, 128
    img = Image.new("RGB", (W, H), (188, 174, 148))  # stone drum band
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, W, 12], fill=(204, 192, 166))
    d.rectangle([0, H - 12, W, H], fill=(176, 162, 134))
    n = 28
    for i in range(n):
        cx = (i + 0.5) * W / n
        w = W / n * 0.42
        d.rectangle([cx - w / 2, 30, cx + w / 2, H - 28], fill=(40, 40, 46))
        d.rectangle([cx - 1, 30, cx + 1, H - 28], fill=(70, 68, 72))
    save(img, "clerestory.png")


# ---------------------------------------------------------------- dome
def dome():
    # 24 rib bays per wrap. Pale sheet iron, darker rib at each bay edge,
    # faint horizontal seams.
    W, H = 1440, 384
    img = Image.new("RGB", (W, H), (146, 148, 140))
    d = ImageDraw.Draw(img)
    bays = 24
    bw = W / bays
    for i in range(bays):
        x = i * bw
        for k in range(int(bw)):
            t = k / bw
            shade = int(10 * abs(t - 0.5) * 2)      # gentle cylindrical shading
            d.line([x + k, 0, x + k, H],
                   fill=(146 - shade, 148 - shade, 140 - shade))
        d.rectangle([x - 2, 0, x + 2, H], fill=(104, 106, 100))   # rib
        d.rectangle([x + 2, 0, x + 3, H], fill=(186, 188, 180))  # rib highlight
    for y in range(0, H, 48):
        d.line([0, y, W, y], fill=(138, 140, 134))
    save(img, "dome.png")


# ---------------------------------------------------------------- arch window
def archwindow():
    W, H = 256, 384
    img = Image.new("RGB", (W, H), (66, 72, 84))
    d = ImageDraw.Draw(img)
    # five tall lights separated by stone mullions (as the engravings show)
    for i in range(1, 5):
        x = i * W / 5
        d.rectangle([x - 3, 0, x + 3, H], fill=(196, 184, 160))
    d.rectangle([0, H * 0.42, W, H * 0.42 + 5], fill=(196, 184, 160))  # transom
    for i in range(5):  # subtle per-light tone difference
        x0 = i * W / 5
        tone = random.randint(-8, 8)
        d.rectangle([x0 + 4, 6, x0 + W / 5 - 4, H - 6],
                    fill=(66 + tone, 72 + tone, 84 + tone))
    save(img, "archwindow.png")


# ---------------------------------------------------------------- wood
def wood():
    S = 512
    img = Image.new("RGB", (S, S), (96, 66, 44))
    d = ImageDraw.Draw(img)
    for i in range(260):
        y = random.uniform(0, S)
        tone = random.randint(-16, 16)
        length = random.uniform(60, S)
        x = random.uniform(0, S - 60)
        d.line([x, y, x + length, y + random.uniform(-2, 2)],
               fill=(96 + tone, int(66 + tone * 0.7), int(44 + tone * 0.5)), width=1)
    for x in range(0, S, 128):     # board joints
        d.line([x, 0, x, S], fill=(70, 46, 30), width=2)
    save(img, "wood.png")


if __name__ == "__main__":
    brick()
    arcade()
    clerestory()
    dome()
    archwindow()
    wood()
