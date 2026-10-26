#!/usr/bin/env python3
"""gen_figma_sheets.py - draw the Crystal Palace 1851 sheets as SVG from the project's own records.

    python3 -I gen_figma_sheets.py OUTDIR

READS (never writes) in /Users/bear/Documents/CoWork/bear-textbooks/books/architecture/crystal-palace-1851/:
  controls.json            the record's figures as tested (D01..D34), each with its status
  DEPARTURES-LEDGER.md     every inference / simplification / departure (rows parsed, markers placed on the drawings)
  model/build_slice.py     ONLY the plan constants (AVENUE_VOID_BAYS, STAIR_BAYS, NAVE_VOID_FIRST_BAY, ...), read with ast,
                           never executed; they are the plan as read off Plates I and II (ledger rows 14, 22, 24-27)
WRITES: OUTDIR/*.svg and OUTDIR/manifest.json. Nothing is drawn from the Blender model, so a drawing is not
circular evidence for the model.

Honesty rules the sheets follow:
  - dimension line style = status of the figure (solid printed, dashed checked, dotted text-only, orange derived/inferred)
  - every dimension carries its control ID; every ledger-relevant element carries an L<n> marker coloured by the
    strongest word in that row's Status (departure > inferred > simplified > matches record)
  - figures that are NOT in controls.json are tagged LEDGER (taken from the ledger text, row cited) or DERIVED (worked out
    here, listed on the sheet and in the index) and drawn orange
  - the footer of every sheet carries the sha of each input so a stale drawing can be spotted
"""
import ast
import datetime
import hashlib
import json
import math
import re
import sys
import textwrap
from pathlib import Path
from xml.sax.saxutils import escape

PROJ = Path("/Users/bear/Documents/CoWork/bear-textbooks/books/architecture/crystal-palace-1851")
F_CONTROLS, F_LEDGER, F_BUILD = PROJ / "controls.json", PROJ / "DEPARTURES-LEDGER.md", PROJ / "model" / "build_slice.py"
OUT = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("out")
OUT.mkdir(parents=True, exist_ok=True)

INK, PAPER, ORANGE, RED, AMBER = "#292929", "#FAF8F2", "#D2611F", "#B3261E", "#B7791F"
GREY, LIGHT, MID, FLOOR = "#9E9E99", "#E4E1D8", "#CFC9B8", "#DAD5C6"
FONT = "Inter, Helvetica, Arial, sans-serif"


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()[:8]


# ---------------------------------------------------------------- inputs
CTL_DOC = json.loads(F_CONTROLS.read_text(encoding="utf-8"))
CTL = {c["id"]: c for c in CTL_DOC["controls"]}


def V(cid):
    if cid not in CTL:
        sys.exit(f"controls.json has no control {cid}; the generator needs it")
    return CTL[cid]["stated"]


def ST(cid):
    return {"plate-printed": "printed", "plate-checked": "checked", "text": "text"}.get(CTL[cid]["status"], "open")


def clean(t):
    return re.sub(r"\s+", " ", t.replace("**", "").replace("`", "")).strip()


LEDGER = {}
for line in F_LEDGER.read_text(encoding="utf-8").splitlines():
    if re.match(r"\|\s*\d+\s*\|", line):
        c = [clean(x) for x in line.strip().strip("|").split("|")]
        sl = c[4].lower()
        # "scope" is tested first: rows 16 and 23 say "scope limit, not a departure" and must not count as departures
        cls = ("scope" if "scope" in sl else "departure" if "departure" in sl else "inferred" if "inferred" in sl
               else "simplified" if "simplified" in sl else "matches")
        LEDGER[int(c[0])] = dict(n=int(c[0]), part=c[1], record=c[2], model=c[3], status=c[4], disclose=c[5] if len(c) > 5 else "", cls=cls)
m = re.search(r"## Not modelled yet[^\n]*\n(.*?)\n## ", F_LEDGER.read_text(encoding="utf-8"), re.S)
NOT_MODELLED = clean(m.group(1)) if m else ""


def load_plan():
    tree, env = ast.parse(F_BUILD.read_text(encoding="utf-8")), {}
    for node in tree.body:
        if not isinstance(node, ast.Assign):
            continue
        t = node.targets[0]
        if isinstance(t, ast.Name):
            pairs = [(t.id, node.value)]
        elif isinstance(t, ast.Tuple) and isinstance(node.value, ast.Tuple):
            pairs = list(zip([e.id for e in t.elts], node.value.elts))
        else:
            continue
        for n, v in pairs:
            try:
                env[n] = eval(compile(ast.Expression(v), "<plan>", "eval"), {"__builtins__": {}, "set": set, "range": range}, dict(env))
            except Exception:
                pass
    need = ["GRID", "X_WEST", "Y_SOUTH", "ROWS", "AVENUE_VOID_BAYS", "STAIR_BAYS", "NAVE_VOID_FIRST_BAY", "PLAN_DATA_LAST_LINE"]
    miss = [n for n in need if n not in env]
    if miss:
        sys.exit(f"build_slice.py constants not found: {miss}")
    return env


PLAN = load_plan()
GRID, ROWS = PLAN["GRID"], PLAN["ROWS"]
AVE_BAYS, STAIR_BAYS, NAVE_FIRST = PLAN["AVENUE_VOID_BAYS"], PLAN["STAIR_BAYS"], PLAN["NAVE_VOID_FIRST_BAY"]
LAST_LINE = PLAN["PLAN_DATA_LAST_LINE"]
NBAYS = LAST_LINE                       # bays 0 .. LAST_LINE-1, lines 0 .. LAST_LINE

# ---------------------------------------------------------------- figures from controls.json
W1, W2, W3 = V("D02"), V("D03"), V("D04")
TOP = {1: V("D11a"), 2: V("D11b"), 3: V("D11c")}
GIRD, GIRL, PITCH, GALF = V("D10a"), V("D10b"), V("D06"), V("D12")
COLTOP, PIECE, PIECE3TOP, COLD = V("D14"), V("D15"), V("D18"), V("D13") / 12
NAVE, AVE = V("D08"), V("D07")
# figures that are NOT in controls.json: taken from the ledger text (row cited) - drawn orange when they matter
LEDGER_FIG = {
    "upper column 16 ft 7 1/2 in": (16 + 7.5 / 12, "L2"),
    "roof rise 1.6 ft (inferred)": (1.6, "L5"),
    "gallery slab 9 in": (0.75, "L11"),
    "railing height 3.06 ft (inferred)": (3.06, "L12"),
    "ground slab 6 in": (0.5, "L6"),
    "gallery strip 24 ft": (24.0, "L11"),
    "stair flight width 8 ft": (8.0, "L17"),
    "well hole 8 x 16 ft": ((8.0, 16.0), "L19"),
}
UPPER_COL, RISE, SLAB, RAIL, FLOOR_T, STRIP = (LEDGER_FIG[k][0] for k in (
    "upper column 16 ft 7 1/2 in", "roof rise 1.6 ft (inferred)", "gallery slab 9 in", "railing height 3.06 ft (inferred)",
    "ground slab 6 in", "gallery strip 24 ft"))
FLT_W = LEDGER_FIG["stair flight width 8 ft"][0]
WELL_W, WELL_L = LEDGER_FIG["well hole 8 x 16 ft"][0]
COLGAPS = [7 + 1 / 12, 8 + 5 / 12, 7 + 1 / 12]            # Plate XVII Fig. 1 via ledger row 18
DERIVED = []                                                # things worked out here, listed on the sheets


def derive(what):
    DERIVED.append(what)
    return what


# consistency checks between the sources; a failure means a source changed and the drawing must not be trusted
assert abs(sum(COLGAPS) - V("D29")) < 0.01, "D29 no longer equals 7'1\" + 8'5\" + 7'1\""
AVE_IN = NAVE / 2 + STRIP                                   # inner edge of an avenue void
AVE_OUT = AVE_IN + AVE                                      # outer edge
assert abs(AVE_OUT + STRIP - W2 / 2) < 0.01, "gallery zone (24+48+24+72+24+48+24) no longer equals D03"
PIECE_W = PITCH - GIRL                                      # DERIVED: 24 ft - 23 ft 3 1/4 in
TOP_TIER = lambda y: 3 if abs(y) <= W3 / 2 else 2 if abs(y) <= W2 / 2 else 1  # noqa: E731
ROW_Y = [-W1 / 2 + PITCH * j for j in range(ROWS)]
assert len(ROW_Y) == 18 and abs(ROW_Y[-1] - W1 / 2) < 0.01

# ---------------------------------------------------------------- formatting
EIGHTHS = {0: "", 1: "⅛", 2: "¼", 3: "⅜", 4: "½", 5: "⅝", 6: "¾", 7: "⅞"}


def fmt(v, unit="ft"):
    if unit == "in":
        return f"{v:g} in"
    ft = int(math.floor(v + 1e-9))
    inch = (v - ft) * 12
    e = inch * 8
    if abs(e - round(e)) > 0.06:
        return f"{v:g} ft"
    e = int(round(e))
    if e == 96:
        ft, e = ft + 1, 0
    if e == 0:
        return f"{ft} ft"
    i, f = divmod(e, 8)
    return f"{ft}′ {i if i else ''}{EIGHTHS[f]}″"


def FL(cid, extra=""):
    return f"{fmt(V(cid), CTL[cid].get('unit', 'ft'))} · {cid}{extra}"


STY = {"printed": (None, INK), "checked": ("6 3", INK), "text": ("1.5 3", INK), "open": ("2 2", GREY),
       "derived": (None, ORANGE), "inferred": ("6 3", ORANGE)}
CLS_COL = {"departure": RED, "inferred": ORANGE, "simplified": AMBER, "matches": INK, "scope": GREY}
DRAWN = {}           # control id -> set of sheet names
MARKED = {}          # ledger row -> set of sheet names


class Svg:
    def __init__(self, w, h, name, title, sub):
        self.w, self.h, self.name, self.o, self.ids = w, h, name, [], set()
        self.o.append(f'<rect id="paper" width="{w}" height="{h}" fill="{PAPER}"/>')
        self.text(30, 44, title, 24, 600)
        self.text(30, 68, sub, 12, 400, ORANGE)

    def _id(self, i):
        if not i:
            return ""
        i = re.sub(r'[<>&"]', "", i)[:90]
        b, k = i, 1
        while i in self.ids:
            k += 1
            i = f"{b} ({k})"
        self.ids.add(i)
        return f' id="{i}"'

    def open(self, i=None, tr=None):
        self.o.append(f'<g{self._id(i)}' + (f' transform="translate({tr[0]} {tr[1]})"' if tr else "") + ">")

    def close(self):
        self.o.append("</g>")

    def _st(self, fill, stroke, sw, dash, op=None):
        a = f' fill="{fill or "none"}"'
        if stroke:
            a += f' stroke="{stroke}" stroke-width="{sw:g}"'
            if dash:
                a += f' stroke-dasharray="{dash}"'
        if op is not None:
            a += f' fill-opacity="{op}"'
        return a

    def rect(self, x, y, w, h, fill=None, stroke=None, sw=1, dash=None, i=None, op=None):
        self.o.append(f'<rect{self._id(i)} x="{x:.2f}" y="{y:.2f}" width="{max(w, .01):.2f}" height="{max(h, .01):.2f}"'
                      + self._st(fill, stroke, sw, dash, op) + "/>")

    def line(self, x1, y1, x2, y2, col=INK, sw=1, dash=None, i=None):
        self.o.append(f'<line{self._id(i)} x1="{x1:.2f}" y1="{y1:.2f}" x2="{x2:.2f}" y2="{y2:.2f}" stroke="{col}" '
                      f'stroke-width="{sw:g}"' + (f' stroke-dasharray="{dash}"' if dash else "") + ' fill="none"/>')

    def poly(self, pts, col=INK, sw=1, dash=None, i=None, fill=None, close=False):
        tag = "polygon" if close else "polyline"
        self.o.append(f'<{tag}{self._id(i)} points="' + " ".join(f"{x:.2f},{y:.2f}" for x, y in pts) + '"'
                      + self._st(fill, col, sw, dash) + "/>")

    def circle(self, cx, cy, r, fill=None, stroke=None, sw=1, i=None):
        self.o.append(f'<circle{self._id(i)} cx="{cx:.2f}" cy="{cy:.2f}" r="{r:.2f}"' + self._st(fill, stroke, sw, None) + "/>")

    def text(self, x, y, s, size=11, weight=400, fill=INK, anchor="start", i=None, vmid=False):
        yb = y + size * 0.35 if vmid else y
        a = {"start": "", "middle": ' text-anchor="middle"', "end": ' text-anchor="end"'}[anchor]
        self.o.append(f'<text{self._id(i)} x="{x:.2f}" y="{yb:.2f}" font-family="{FONT}" font-size="{size}" '
                      f'font-weight="{weight}" fill="{fill}"{a}>{escape(s)}</text>')

    def block(self, x, y, s, wpx, size=10, fill=INK, weight=400, i=None):
        n = max(20, int(wpx / (size * 0.53)))
        lines = textwrap.wrap(s, n)
        self.open(i or "note")
        for k, ln in enumerate(lines):
            self.text(x, y + size + k * size * 1.35, ln, size, weight, fill)
        self.close()
        return y + (len(lines) + 0.4) * size * 1.35

    def tick(self, x, y, col):
        self.line(x - 3, y + 3, x + 3, y - 3, col, 1.25)

    def hdim(self, x1, x2, y, label, st, cid=None, ext=None, size=11, above=True):
        d, col = STY[st]
        self.open(f"DIM {cid or ''} {st} {label}")
        self.line(x1, y, x2, y, col, 1, d)
        e = y - 8 if ext is None else ext
        self.line(x1, e, x1, y + 8, col, .75)
        self.line(x2, e, x2, y + 8, col, .75)
        self.tick(x1, y, col)
        self.tick(x2, y, col)
        self.text((x1 + x2) / 2, y - 6 if above else y + 15, label, size, 500, col, "middle")
        self.close()
        if cid:
            DRAWN.setdefault(cid, set()).add(self.name)

    def vdim(self, x, ya, yb, label, st, cid=None, ext=None, pos="right", size=11):
        d, col = STY[st]
        top, bot = min(ya, yb), max(ya, yb)
        self.open(f"DIM {cid or ''} {st} {label}")
        self.line(x, ya, x, yb, col, 1, d)
        if ext is not None:
            self.line(ext, top, x + (-6 if pos == "left" else 6), top, col, .75)
        self.tick(x, top, col)
        self.tick(x, bot, col)
        ym = (top + bot) / 2
        if pos == "left":
            self.text(x - 9, ym, label, size, 500, col, "end", vmid=True)
        elif pos == "above":
            self.text(x, top - 12, label, size, 500, col, "middle")
        else:
            self.text(x + 9, ym, label, size, 500, col, vmid=True)
        self.close()
        if cid:
            DRAWN.setdefault(cid, set()).add(self.name)

    def mention(self, cid):
        DRAWN.setdefault(cid, set()).add(self.name)

    def marker(self, x, y, n):
        r = LEDGER[n]
        col = CLS_COL[r["cls"]]
        self.open(f"LEDGER L{n} {r['cls']}")
        self.circle(x, y, 8, "#FFFFFF", col, 1.5)
        self.text(x, y, f"L{n}", 8, 600, col, "middle", vmid=True)
        self.close()
        MARKED.setdefault(n, set()).add(self.name)

    def legend(self, x, y):
        self.open("LEGEND")
        self.text(x, y, "LINE KEY: the status of each figure", 11, 600)
        for k, (st, txt) in enumerate([("printed", "plate-printed: the plate prints it"),
                                       ("checked", "plate-checked: read off a plate (±0.5-0.7%)"),
                                       ("text", "text only: printed page, no plate"),
                                       ("derived", "derived or inferred: see notes (orange)")]):
            yy = y + 20 + k * 17
            d, col = STY[st]
            self.line(x, yy, x + 44, yy, col, 1.5, d)
            self.text(x + 54, yy, txt, 10, 400, INK, vmid=True)
        x2 = x + 400
        self.text(x2, y, "LEDGER MARKER: strongest word in the row's Status", 11, 600)
        for k, (c, txt) in enumerate([("matches", "matches record"), ("simplified", "simplified (detail left out)"),
                                      ("inferred", "inferred (record silent or not read)"), ("departure", "departure (deliberately different)")]):
            yy = y + 20 + k * 17
            self.circle(x2 + 8, yy, 6, "#FFFFFF", CLS_COL[c], 1.5)
            self.text(x2 + 22, yy, txt, 10, 400, INK, vmid=True)
        self.close()

    def footer(self, extra=""):
        s = (f"Generated {datetime.date.today().isoformat()} by gen_figma_sheets.py from controls.json (sha {sha(F_CONTROLS)}), "
             f"DEPARTURES-LEDGER.md (sha {sha(F_LEDGER)}), build_slice.py plan constants (sha {sha(F_BUILD)}). "
             "TEST DRAWINGS: schematic, drawn from the record's figures as tested, not redraws of the plates, not independent evidence. " + extra)
        self.block(30, self.h - 54, s, self.w - 60, 9, GREY, i="footer")

    def save(self):
        p = OUT / f"{self.name}.svg"
        p.write_text(f'<svg xmlns="http://www.w3.org/2000/svg" width="{self.w}" height="{self.h}" viewBox="0 0 {self.w} {self.h}">\n'
                     + "\n".join(self.o) + "\n</svg>\n", encoding="utf-8")
        return p


def ledger_box(s, x, y, w, rows, title="Ledger rows marked on this sheet"):
    s.open("LEDGER NOTES")
    s.text(x, y, title, 12, 600)
    yy = y + 18
    for n in rows:
        r = LEDGER[n]
        s.circle(x + 8, yy + 5, 6, "#FFFFFF", CLS_COL[r["cls"]], 1.5)
        s.text(x + 8, yy + 5, f"L{n}", 6.5, 600, CLS_COL[r["cls"]], "middle", vmid=True)
        txt = f"{r['part']} - {r['status']}"
        yy = s.block(x + 24, yy - 1, txt[:260] + ("…" if len(txt) > 260 else ""), w - 24, 9.5) + 4
    s.close()
    return yy


def panel(s, x, y, w, h, title):
    s.open(f"PANEL {title}", (x, y))
    s.rect(0, 0, w, h, None, GREY, 1)
    s.text(12, 20, title, 13, 600)


# ================================================================ sheet 1: plan
def sheet_plan():
    s = Svg(1500, 1740, "1-plan", "Plan — whole building key plan, west half gallery-level plan",
            "Plan data as encoded in build_slice.py (read off Plates I and II, ledger rows 14, 22, 24-27) with the printed dimension chain")
    s.legend(30, 96)
    # ---- key plan, 0.72 px/ft
    panel(s, 30, 210, 1440, 440, "K  Key plan, whole building (0.70 px/ft). Shaded = the part of the plan that has been read (bays 0-36); the rest is outline only")
    k = 0.70
    kx, ky = (lambda X: 27 + X * k), (lambda Y: 250 - Y * k)
    L = V("D01")
    s.rect(kx(0), ky(W1 / 2), L * k, W1 * k, None, INK, 1.2, i="main block D01 x D02")
    for yy in (W3 / 2, -W3 / 2, W2 / 2, -W2 / 2):
        s.line(kx(0), ky(yy), kx(L), ky(yy), GREY, .75, "2 3", i=f"tier edge y={yy:g}")
    edge = LAST_LINE * GRID
    s.rect(kx(0), ky(W1 / 2), edge * k, W1 * k, FLOOR, None, op=0.55, i=f"plan read to line {LAST_LINE} ({edge} ft)")
    s.text(kx(edge / 2), ky(0) + 4, f"plan read from Plates I-II to line {LAST_LINE} ({edge} ft); ledger: west-03_v001 builds the west half to here",
           10, 500, INK, "middle")
    s.line(kx(edge), ky(W1 / 2), kx(edge), ky(-W1 / 2), INK, 1, "6 3", i="transept west face (line 37)")
    cx = kx(L / 2)
    s.line(cx - 8, ky(0), cx + 8, ky(0), INK, 1)
    s.line(cx, ky(0) - 8, cx, ky(0) + 8, INK, 1)
    s.text(cx + 10, ky(0) + 14, "crossing = origin; transept not modelled (D19, D20)", 9, 400, GREY)
    NS0 = 216                                              # controls.json model_conventions.origin: "north strip runs from 216 ft"
    s.rect(kx(NS0), ky(W1 / 2 + V("D05b")), V("D05a") * k, V("D05b") * k, None, ORANGE, 1, "6 3", i="north strip (not built)")
    s.text(kx(NS0) + 8, ky(W1 / 2 + V("D05b")) + 18, "north strip: not built (start at 216 ft per controls.json model_conventions)", 9, 400, ORANGE)
    s.hdim(kx(NS0), kx(NS0 + V("D05a")), ky(W1 / 2 + V("D05b")) - 14, FL("D05a"), ST("D05a"), "D05a", ext=ky(W1 / 2 + V("D05b")))
    s.vdim(kx(NS0 + V("D05a")) + 16, ky(W1 / 2), ky(W1 / 2 + V("D05b")), FL("D05b"), ST("D05b"), "D05b", ext=kx(NS0 + V("D05a")))
    s.hdim(kx(0), kx(L), ky(-W1 / 2) + 38, FL("D01"), ST("D01"), "D01", ext=ky(-W1 / 2) + 4, above=False)
    s.vdim(kx(L) + 20, ky(W1 / 2), ky(-W1 / 2), FL("D02"), ST("D02"), "D02", ext=kx(L) + 2)
    s.close()
    # ---- gallery-level plan, 1.4 px/ft
    panel(s, 30, 670, 1440, 880, f"P  Gallery-level plan, bays 0-{NBAYS - 1} (1.34 px/ft). White = void (railed), shaded = gallery floor")
    p = 1.34
    px, py = (lambda X: 40 + X * p), (lambda Y: 470 - Y * p)
    xe = NBAYS * GRID
    s.open("PLAN")
    s.rect(px(0), py(W1 / 2), xe * p, W1 * p, None, INK, 1, i="main block 408 ft")
    s.rect(px(0), py(W2 / 2), xe * p, W2 * p, FLOOR, None, i="gallery zone (D03, 264 ft)")
    bay_void = lambda b: ((b in AVE_BAYS or b in STAIR_BAYS), b >= NAVE_FIRST)  # noqa: E731

    def runs(pred):
        out, start = [], None
        for b in range(NBAYS + 1):
            ok = b < NBAYS and pred(b)
            if ok and start is None:
                start = b
            if not ok and start is not None:
                out.append((start, b))
                start = None
        return out

    for a, b in runs(lambda b: b in AVE_BAYS):
        for lo, hi, nm in ((AVE_IN, AVE_OUT, "N"), (-AVE_OUT, -AVE_IN, "S")):
            s.rect(px(a * GRID), py(hi), (b - a) * GRID * p, (hi - lo) * p, PAPER, INK, 1.4, i=f"avenue void {nm} bays {a}-{b - 1}")
    a = NAVE_FIRST
    s.rect(px(a * GRID), py(NAVE / 2), (NBAYS - a) * GRID * p, NAVE * p, PAPER, INK, 1.4, i=f"nave void bays {a}-{NBAYS - 1}")
    for b in sorted(STAIR_BAYS):
        if b < NBAYS:
            for lo, hi, nm in ((AVE_IN, AVE_OUT, "N"), (-AVE_OUT, -AVE_IN, "S")):
                s.rect(px(b * GRID), py(hi), GRID * p, (hi - lo) * p, MID, INK, .8, i=f"cross gallery {nm} bay {b}")
                xc, yc = (b + .5) * GRID, (hi + lo) / 2
                sgn = 1 if nm == "N" else -1
                for y0 in (sgn * AVE_IN, sgn * (AVE_OUT - WELL_L)):
                    ya = min(y0, y0 + sgn * WELL_L)
                    s.rect(px(xc - WELL_W / 2), py(ya + WELL_L), WELL_W * p, WELL_L * p, PAPER, INK, .6, "2 1.5", i="well hole")
    for j, Y in enumerate(ROW_Y):
        for i in range(LAST_LINE + 1):
            s.rect(px(i * GRID) - 1.2, py(Y) - 1.2, 2.4, 2.4, INK, i=None)
    s.close()
    s.text(px(NAVE_FIRST * GRID + 12 * GRID), py(0) + 4, "nave void: 72 ft (D08), from line 3, to the transept west face", 11, 500, GREY, "middle")
    s.text(px(1.2 * GRID), py((AVE_IN + AVE_OUT) / 2) + 4, "avenue void", 10, 400, GREY)
    s.text(px(0.1 * GRID), py(W1 / 2) - 6, "west end (line 0)", 10, 400, GREY)
    s.line(px(edge := xe), py(W1 / 2), px(edge), py(-W1 / 2), INK, 1, "6 3")
    s.text(px(edge) + 6, py(W1 / 2) + 10, "transept west face", 9, 400, GREY)
    # printed chain along the top (bays: 0 = west end bay, then void runs and stair bays)
    segs, b = [], 0
    while b < NBAYS:
        kind = "stair" if b in STAIR_BAYS else "void" if b in AVE_BAYS else "end"
        e = b
        while e < NBAYS and (("stair" if e in STAIR_BAYS else "void" if e in AVE_BAYS else "end") == kind) and (kind != "stair" or e == b):
            e += 1
        segs.append((kind, b, e))
        b = e
    cid_for = {(0, 1): "D23", (1, 8): "D25", (8, 9): "D26"}
    rowfor = {(9, 17): 22, (17, 18): 24, (18, 26): 22, (26, 27): 24, (27, 34): 26, (34, 35): 25, (35, 37): 27}
    ytop = py(W1 / 2) - 46
    for kind, a, e in segs:
        ft_len = (e - a) * GRID
        cid = cid_for.get((a, e))
        lab = f"{ft_len:g}" + (f" · {cid}" if cid else "")
        if (a, e) == (27, 34):
            lab = "168 (120+48)"
        s.hdim(px(a * GRID), px(e * GRID), ytop, lab, "printed", cid, ext=py(W1 / 2) - 2, size=9, above=True)
        if (a, e) in rowfor:
            s.marker((px(a * GRID) + px(e * GRID)) / 2, ytop - 24, rowfor[(a, e)])
    s.hdim(px(0), px(NAVE_FIRST * GRID), ytop - 56, FL("D24"), ST("D24"), "D24", ext=ytop - 40, size=10)
    s.marker(px(GRID * .5), ytop - 24, 14)
    s.marker(px(8.5 * GRID), py(W1 / 2) + 22, 21)
    s.marker(px(34.5 * GRID), py(W1 / 2) + 22, 25)
    # bottom scale ticks
    for i in range(0, LAST_LINE + 1):
        yb = py(-W1 / 2) + 6
        s.line(px(i * GRID), yb, px(i * GRID), yb + (7 if i % 4 == 0 else 3), GREY, .75)
        if i % 4 == 0:
            s.text(px(i * GRID), yb + 19, f"{i * GRID:g}", 8, 400, GREY, "middle")
    s.text(px(0), py(-W1 / 2) + 46, "ft from the west end (a tick every 24 ft grid line; numbers every 96 ft)", 9, 400, GREY)
    # right dims
    xr = px(xe) + 20
    s.vdim(xr, py(W3 / 2), py(-W3 / 2), FL("D04"), ST("D04"), "D04", ext=px(xe), pos="above")
    s.vdim(xr + 68, py(W2 / 2), py(-W2 / 2), FL("D03"), ST("D03"), "D03", ext=px(xe), pos="above")
    s.vdim(xr + 136, py(W1 / 2), py(-W1 / 2), FL("D02"), ST("D02"), "D02", ext=px(xe), pos="above")
    s.close()
    ledger_box_y = 1585
    s.block(30, 1560, "Columns are drawn 2.4 px square (true size is 0.5 px). The avenue void's inner edge is nave/2 + 24 ft strip = 60 ft and its outer edge 108 ft "
            "(D08, D07, ledger row 11; the 24 ft strips are LEDGER figures). Voids carry railings on every edge (rows 12, 13, 20; the stair-bay cross railings are inferred). "
            "Not modelled yet (ledger): " + NOT_MODELLED, 1400, 9.5, INK)
    s.footer()
    return s.save()


# ================================================================ sheet 2: stair bay detail
def sheet_stair():
    s = Svg(1500, 1460, "2-stair-bay", "Stair bay — first avenue staircase, north avenue, bay 8 (192-216 ft)",
            "Record layout from the ledger (rows 17-21) and controls D26-D34; the south staircase is the mirror (row 21)")
    s.legend(30, 96)
    s.open("PANEL stair bay 8 px/ft", (30, 210))
    s.rect(0, 0, 1440, 1200, None, GREY, 1)
    s.text(12, 20, "S  Gallery-level plan, bays 7-9 (168-240 ft), y = +36 to +132 ft (8 px/ft); ground flights, landing and upper flights", 13, 600)
    sc = 8
    X0, X1, Y0, Y1 = 168, 240, 36, 132
    px, py = (lambda X: 150 + (X - X0) * sc), (lambda Y: 150 + (Y1 - Y) * sc)
    xs = [168, 192, 216, 240]
    ys = [36, 60, 84, 108, 132]
    # floor panels: bays 7 and 9 floor except avenue cells; bay 8 all floor (cross gallery over the avenue)
    for bx in (168, 216):
        s.rect(px(bx), py(AVE_IN), GRID * sc, (AVE_IN - Y0) * sc, FLOOR, None, i=f"gallery floor bay x={bx} (inner strip)")
        s.rect(px(bx), py(Y1), GRID * sc, (Y1 - AVE_OUT) * sc, FLOOR, None, i=f"gallery floor bay x={bx} (outer strip)")
        s.rect(px(bx), py(AVE_OUT), GRID * sc, AVE * sc, PAPER, None, i=f"avenue void bay x={bx}")
    s.rect(px(192), py(Y1), GRID * sc, (Y1 - Y0) * sc, FLOOR, None, i="gallery floor bay 8")
    s.rect(px(192), py(AVE_OUT), GRID * sc, AVE * sc, MID, INK, 1, i="cross gallery 48 x 24 ft (D33, D34)")
    # grid
    for X in xs:
        s.line(px(X), py(Y1) - 14, px(X), py(Y0) + 14, GREY, .5, "1 3", i=f"grid x={X}")
        s.text(px(X), py(Y1) - 20, f"line {X // GRID} · {X} ft", 9, 400, GREY, "middle")
    for Y in ys:
        s.line(px(X0) - 14, py(Y), px(X1) + 14, py(Y), GREY, .5, "1 3", i=f"grid y={Y}")
        s.text(px(X0) - 20, py(Y), f"y {Y}", 9, 400, GREY, "end", vmid=True)
    # railings: nave edge, avenue edges (bays 7 and 9), cross railings at lines 8 and 9 (inferred, row 20)
    s.line(px(X0), py(Y0), px(X1), py(Y0), INK, 2.5, i="railing: nave void edge y=36")
    for bx in (168, 216):
        for yy in (AVE_IN, AVE_OUT):
            s.line(px(bx), py(yy), px(bx + GRID), py(yy), INK, 2.5, i=f"railing: avenue edge y={yy:g}")
    for xx in (192, 216):
        s.line(px(xx), py(AVE_IN), px(xx), py(AVE_OUT), ORANGE, 2.5, "6 3", i=f"cross railing at line {xx // GRID} (inferred)")
    # wells
    xc = 204
    for y0 in (AVE_IN, AVE_OUT - WELL_L):
        s.rect(px(xc - WELL_W / 2), py(y0 + WELL_L), WELL_W * sc, WELL_L * sc, PAPER, INK, 1, "4 3", i="well hole 8 x 16 ft (L19)")
    # ground flights (outer strips) and upper flights (middle strip), tread lines at 1 ft
    run = V("D32")
    for nm, x0f in (("W", xc - 12), ("E", xc + 4)):
        s.rect(px(x0f), py(AVE_IN + run), FLT_W * sc, run * sc, LIGHT, INK, 1, i=f"ground flight {nm} (D32)")
        for t in range(1, int(run)):
            s.line(px(x0f), py(AVE_IN + t), px(x0f + FLT_W), py(AVE_IN + t), GREY, .6)
        s.poly([(px(x0f + 4), py(AVE_IN + 3)), (px(x0f + 4), py(AVE_IN + run - 3))], INK, 1.2, i=f"up arrow {nm}")
        s.poly([(px(x0f + 3), py(AVE_IN + run - 6)), (px(x0f + 4), py(AVE_IN + run - 3)), (px(x0f + 5), py(AVE_IN + run - 6))], INK, 1.2, close=True, fill=INK)
    for nm, y0f, dirn in (("IN", AVE_IN, -1), ("OUT", AVE_OUT - run, 1)):
        s.rect(px(xc - FLT_W / 2), py(y0f + run), FLT_W * sc, run * sc, None, INK, 1, "3 2", i=f"upper flight {nm}")
        for t in range(1, int(run)):
            s.line(px(xc - FLT_W / 2), py(y0f + t), px(xc + FLT_W / 2), py(y0f + t), GREY, .6, "1 2")
        ya, yb = (y0f + run - 3, y0f + 3) if dirn == -1 else (y0f + 3, y0f + run - 3)
        s.poly([(px(xc), py(ya)), (px(xc), py(yb))], INK, 1.2, i=f"direction arrow {nm}")
        tip = py(yb)
        d = 3 * (1 if tip > py(ya) else -1)
        s.poly([(px(xc - .8), tip - d), (px(xc), tip), (px(xc + .8), tip - d)], INK, 1.2, close=True, fill=INK)
    # landing 24 x 8 at the centre of the avenue
    lw, ll = V("D28"), V("D27")
    yc = (AVE_IN + AVE_OUT) / 2
    s.rect(px(xc - lw / 2), py(yc + ll / 2), lw * sc, ll * sc, MID, INK, 1.2, i="landing 24 x 8 ft (D28, D27)")
    s.text(px(xc), py(yc), "landing", 10, 500, INK, "middle", vmid=True)
    # landing columns: outermost 22'7" (D29): 7'1", 8'5", 7'1"
    cx0 = xc - V("D29") / 2
    xsc = [cx0]
    for g in COLGAPS:
        xsc.append(xsc[-1] + g)
    for x in xsc:
        for dy in (-ll / 2, ll / 2):
            s.circle(px(x), py(yc + dy), 5 / 12 / 2 * sc, INK, i="landing column 5 in")
    # landing railings (row 18): the two ends and the far side
    for x in (xc - lw / 2, xc + lw / 2):
        s.line(px(x), py(yc - ll / 2), px(x), py(yc + ll / 2), INK, 2, i="landing railing end")
    s.line(px(xc - 8), py(yc + ll / 2), px(xc + 8), py(yc + ll / 2), INK, 2, i="landing railing far side")
    # columns of the main grid (8 in)
    for X in xs:
        for Y in ys:
            s.rect(px(X) - COLD * sc / 2, py(Y) - COLD * sc / 2, COLD * sc, COLD * sc, INK, i=None)
    # markers
    s.marker(px(xc - 8), py(AVE_IN + 10), 17)
    s.marker(px(xc), py(yc) - 14, 18)
    s.marker(px(204) + 62, py(AVE_OUT) + 18, 19)
    s.marker(px(216), py(AVE_IN + 3), 20)
    s.marker(px(xc - 12) - 18, py(AVE_IN) - 10, 21)
    # dims
    s.hdim(px(192), px(216), py(Y1) - 42, FL("D26"), ST("D26"), "D26", ext=py(Y1) - 14)
    s.hdim(px(192), px(216), py(Y1) - 70, FL("D34"), ST("D34"), "D34", ext=py(Y1) - 50)
    xr = px(X1) + 40
    s.vdim(xr, py(AVE_IN), py(AVE_OUT), FL("D07"), ST("D07"), "D07", ext=px(X1) + 6, pos="above")
    s.vdim(xr + 130, py(AVE_IN), py(AVE_OUT), FL("D33"), ST("D33"), "D33", ext=px(216), pos="above")
    s.vdim(xr + 260, py(yc + ll / 2), py(yc - ll / 2), FL("D27"), ST("D27"), "D27", ext=px(216), pos="above")
    s.vdim(xr + 390, py(AVE_IN), py(AVE_IN + run), FL("D32", " (20 treads)"), ST("D32"), "D32", ext=px(216), pos="above")
    yb0 = py(Y0) + 44
    s.hdim(px(xsc[0]), px(xsc[-1]), yb0, FL("D29"), ST("D29"), "D29", ext=py(Y0) + 20, above=False)
    for a, b, g in zip(xsc, xsc[1:], COLGAPS):
        s.hdim(px(a), px(b), yb0 + 38, fmt(g), "printed", None, ext=yb0 + 20, above=False, size=10)
    s.hdim(px(192), px(216), yb0 + 82, FL("D28"), ST("D28"), "D28", ext=yb0 + 62, above=False)
    # notes
    yy = ledger_box(s, 760, 800, 660, [17, 18, 19, 20, 21])
    s.block(760, yy + 14, "Where each figure comes from. Controls: D26 (24 ft bay, Plate II), D07 (48 ft avenue), D27 (landing 8 ft, plate-checked), D28 (landing 24 ft, text only), "
            "D29 (22′ 7″, Plate XVII Fig. 1), D32 (20 treads of 1 ft, plate-checked), D33 and D34 (cross gallery 48 x 24 ft, text only). "
            "LEDGER figures, not in controls.json: flight width 8 ft with 8 ft between them (row 17), wells 8 x 16 ft over the middle 8 ft of the bay at the two ends of the "
            "avenue (row 19), flights start at the nave-side edge of the avenue and the landing is centred on it (row 21), the 24 ft strips either side of the avenue (row 11). "
            "Positions of the wells were read off Plate II to about 1 ft (row 19). Orange dashed lines are INFERRED cross railings (row 20). "
            "Not drawn: lattice standards, volutes, strings, I-sections, hand rails (row 17).", 660, 10, INK)
    s.close()
    s.footer()
    return s.save()


# ================================================================ sheet 3: transverse section
def sheet_section():
    s = Svg(1500, 1190, "3-section", "Transverse section — across the 408 ft width at a typical bay",
            "Tier stepping, gallery strips, voids, roofs and railings; heights from D11a-c and D12; roofs and railings are inferred (rows 5 and 12)")
    s.legend(30, 96)
    panel(s, 30, 210, 1440, 620, "T  Transverse section (2.5 px/ft), drawn at a bay between column lines")
    S, X0, G = 2.5, 640, 400
    z = lambda v: G - v * S  # noqa: E731
    yx = lambda Y: X0 + Y * S  # noqa: E731
    s.line(yx(-W1 / 2) - 30, G, 1290, G, INK, 1.5, i="floor_ground z=0")
    s.rect(yx(-W1 / 2), G, W1 * S, FLOOR_T * S, LIGHT, INK, .6, i="ground slab 6 in (L6: record is boards on joists)")
    s.marker(yx(-W1 / 2) - 14, G + 14, 6)
    for t, W in ((1, W1), (2, W2), (3, W3)):
        s.rect(yx(-W / 2), z(TOP[t]), W * S, GIRD * S, LIGHT, INK, 1, i=f"girder band tier {t}" + (" (depth assumed)" if t > 1 else ""))
    for j, Y in enumerate(ROW_Y):
        t = TOP_TIER(Y)
        s.rect(yx(Y) - COLD * S / 2, z(TOP[t]), COLD * S, TOP[t] * S, INK, i=f"column row {j} y={Y:g} top tier {t}")
    # gallery floor strips and railings
    for lo, hi in ((-W2 / 2, -AVE_OUT), (-AVE_IN, -NAVE / 2), (NAVE / 2, AVE_IN), (AVE_OUT, W2 / 2)):
        s.rect(yx(lo), z(GALF), (hi - lo) * S, SLAB * S, MID, INK, .8, i=f"gallery floor strip y {lo:g}..{hi:g} (L11)")
    for Y in (-AVE_OUT, -AVE_IN, -NAVE / 2, NAVE / 2, AVE_IN, AVE_OUT):
        s.line(yx(Y), z(GALF), yx(Y), z(GALF + RAIL), ORANGE, 1.2, i=f"railing y={Y:g} (3.06 ft inferred, L12)")
    s.marker(yx(AVE_OUT) + 12, z(GALF + RAIL) - 4, 12)
    s.marker(yx(-W2 / 2) + 8, z(GALF) - 14, 11)
    # roofs: valley at girder top, rise 1.6 ft, 8 ft units (D09), inferred rise
    unit = V("D09")
    for t, (a, b) in ((3, (-W3 / 2, W3 / 2)), (2, (W3 / 2, W2 / 2)), (2, (-W2 / 2, -W3 / 2)), (1, (W2 / 2, W1 / 2)), (1, (-W1 / 2, -W2 / 2))):
        pts, Y, k = [], a, 0
        while Y <= b + .01:
            pts.append((yx(Y), z(TOP[t] + (RISE if k % 2 else 0))))
            Y, k = Y + unit / 2, k + 1
        s.poly(pts, ORANGE, 1, i=f"roof tier {t} y {a:g}..{b:g} (rise inferred, L5)")
    s.marker(yx(W3 / 2) + 14, z(TOP[3] + RISE) - 6, 5)
    s.marker(yx(W2 / 2) + 14, z(TOP[2] + RISE) - 6, 7)
    # dims
    s.hdim(yx(-W3 / 2), yx(-W3 / 2 + unit), z(TOP[3] + RISE) - 24, FL("D09"), ST("D09"), "D09", ext=z(TOP[3] + RISE) - 4, size=9)
    s.hdim(yx(-NAVE / 2), yx(NAVE / 2), 150, FL("D08"), ST("D08"), "D08", ext=z(TOP[3] + RISE) - 6)
    yb = G + 44
    s.hdim(yx(-W1 / 2), yx(W1 / 2), yb, FL("D02"), ST("D02"), "D02", ext=G + 6)
    s.hdim(yx(-W2 / 2), yx(W2 / 2), yb + 36, FL("D03"), ST("D03"), "D03", ext=G + 6)
    s.hdim(yx(-W3 / 2), yx(W3 / 2), yb + 72, FL("D04"), ST("D04"), "D04", ext=G + 6)
    ch = yb + 120
    pos = [-W2 / 2, -AVE_OUT, -AVE_IN, -NAVE / 2, NAVE / 2, AVE_IN, AVE_OUT, W2 / 2]
    names = [("24", "checked", None), (FL("D07"), ST("D07"), "D07"), ("24", "checked", None), (FL("D08"), ST("D08"), "D08"),
             ("24", "checked", None), (FL("D07"), ST("D07"), "D07"), ("24", "checked", None)]
    for a, b, (lab, st, cid) in zip(pos, pos[1:], names):
        s.hdim(yx(a), yx(b), ch, lab, st, cid, ext=G + 6, size=10)
    s.text(yx(-W2 / 2), ch + 28, "gallery strips: 24 + 48 + 24 + 72 + 24 + 48 + 24 = 264 ft (ledger row 11; strip positions read off Plate II by eye)", 10, 400, INK)
    xr = 1180
    s.vdim(xr, G, z(TOP[1]), f"{fmt(TOP[1])} · D11a", ST("D11a"), "D11a", ext=yx(W1 / 2) + 2, pos="above")
    s.vdim(xr + 50, G, z(TOP[2]), f"{fmt(TOP[2])} · D11b", ST("D11b"), "D11b", ext=yx(W2 / 2) + 2, pos="above")
    s.vdim(xr + 100, G, z(TOP[3]), f"{fmt(TOP[3])} · D11c", ST("D11c"), "D11c", ext=yx(W3 / 2) + 2, pos="above")
    s.vdim(yx(-W1 / 2) - 40, G, z(GALF), f"{fmt(GALF)} · D12", ST("D12"), "D12", ext=yx(-W1 / 2) + 2, pos="above")
    s.close()
    ledger_box(s, 30, 880, 700, [5, 6, 7, 11, 12])
    s.block(760, 880, "Notes. Column rows follow from the 24 ft grid and the centred tier widths (18 rows; tier 3 reaches rows within ±60 ft, tier 2 within ±132 ft); they are "
            "not read off Plate VI. Girder depth on tiers 2 and 3 is ASSUMED equal to tier 1 (D10a is the only printed depth). The roof is a zigzag with valley at the girder "
            "top, 8 ft units (D09) and a 1.6 ft rise INFERRED from '2½ to 1' (row 5). Railings are 3.06 ft (row 12, inferred). Not drawn: connecting pieces, the 72 ft nave "
            "trusses (D19), the transept vault (D20), walls, louvres. Not modelled yet (ledger): " + NOT_MODELLED, 700, 9.5, INK)
    s.footer()
    return s.save()


# ================================================================ sheet 4: bay elevation
def sheet_bay():
    s = Svg(1500, 1560, "4-bay-elevation", "Bay elevation — one 24 ft bay: three tiers, and tier 1 in detail",
            "Heights from D11a-c, D14, D15, D18; one derived width (the connecting piece) is orange and is not in the ledger")
    s.legend(30, 96)
    # panel A: three tiers at 8 px/ft
    panel(s, 30, 210, 640, 1020, "A  Three tiers, one bay (8 px/ft)")
    sc, XA, G = 8, 210, 940
    z = lambda v: G - v * sc  # noqa: E731
    xa, xb = XA, XA + PITCH * sc
    s.line(xa - 60, G, xb + 60, G, INK, 1.5, i="floor_ground z=0")
    pw = PIECE_W * sc
    for t in (1, 2, 3):
        gt = TOP[t]
        s.rect(xa + pw / 2, z(gt), PITCH * sc - pw, GIRD * sc, LIGHT, INK, 1, i=f"girder tier {t}" + (" (depth assumed)" if t > 1 else ""))
    s.rect(xa, z(GALF), PITCH * sc, SLAB * sc, MID, INK, .8, i="gallery floor panel (L11)")
    for x in (xa, xb):
        s.rect(x - COLD * sc / 2, z(PIECE3TOP), COLD * sc, PIECE3TOP * sc, INK, i="column shafts")
        for t in (1, 2, 3):
            foot = COLTOP + (t - 1) * 20
            s.rect(x - pw / 2, z(foot + PIECE), pw, PIECE * sc, LIGHT, ORANGE, 1, i=f"connecting piece tier {t} (width derived)")
    s.vdim(xb + 30, G, z(TOP[3]), f"{fmt(TOP[3])} · D11c", ST("D11c"), "D11c", ext=xb + 12, pos="above")
    s.vdim(xb + 80, G, z(TOP[2]), f"{fmt(TOP[2])} · D11b", ST("D11b"), "D11b", ext=xb + 12, pos="above")
    s.vdim(xb + 130, G, z(TOP[1]), f"{fmt(TOP[1])} · D11a", ST("D11a"), "D11a", ext=xb + 12, pos="right")
    s.vdim(xa - 60, G, z(COLTOP), f"{fmt(COLTOP)} · D14", ST("D14"), "D14", ext=xa - 8, pos="left")
    s.vdim(xa - 60, z(COLTOP), z(COLTOP + PIECE), f"{fmt(PIECE)} · D15", ST("D15"), "D15", ext=xa - 8, pos="left")
    s.vdim(xa - 60, z(COLTOP + PIECE), z(COLTOP + PIECE + UPPER_COL), f"{fmt(UPPER_COL)} · L2", "derived", None, ext=xa - 8, pos="left")
    s.vdim(xa - 150, G, z(PIECE3TOP), f"{fmt(PIECE3TOP)} · D18", ST("D18"), "D18", ext=xa - 8, pos="above")
    s.hdim(xa, xb, G + 44, FL("D06"), ST("D06"), "D06", ext=G + 6, above=False)
    s.marker(xa - 20, z(COLTOP / 2), 1)
    s.marker(xa + 28, z(COLTOP + PIECE / 2), 3)
    s.marker(xa + 70, z(TOP[1] - GIRD / 2), 4)
    s.marker(xb - 40, z(GALF) - 12, 11)
    s.close()
    # panel B: tier 1 detail at 24 px/ft
    panel(s, 690, 210, 780, 1020, "B  Tier 1 in detail (18 px/ft)")
    sc, XA, G = 18, 150, 880
    z = lambda v: G - v * sc  # noqa: E731
    xa, xb = XA, XA + PITCH * sc
    pw = PIECE_W * sc
    s.line(xa - 90, G, xb + 150, G, INK, 1.5, i="floor_ground z=0")
    s.rect(xa, z(GALF), PITCH * sc, SLAB * sc, MID, INK, 1, i="gallery floor panel 9 in, 24 x 24 ft cell (L11)")
    s.rect(xa + pw / 2, z(TOP[1]), PITCH * sc - pw, GIRD * sc, LIGHT, INK, 1, i="girder (D10a, D10b)")
    for x in (xa, xb):
        s.rect(x - COLD * sc / 2, z(COLTOP), COLD * sc, COLTOP * sc, INK, i="column shaft 8 in (D13, D14)")
        s.rect(x - pw / 2, z(COLTOP + PIECE), pw, PIECE * sc, LIGHT, ORANGE, 1.4, i="connecting piece (width DERIVED)")
    s.rect(xa, z(GALF + RAIL), PITCH * sc, RAIL * sc, None, ORANGE, 1, "6 3", i="railing 3.06 ft (inferred, L12)")
    s.text((xa + xb) / 2, z(GALF + RAIL / 2), f"balustrade {RAIL} ft - INFERRED (ledger row 12)", 10, 400, ORANGE, "middle")
    s.text((xa + xb) / 2, z(GALF - .3), "gallery floor panel, 9 in (row 11)", 10, 400, INK, "middle")
    s.text((xa + xb) / 2 - 40, z(TOP[1] - GIRD / 2), f"girder {fmt(GIRD)} deep × {fmt(GIRL)} face to face", 10, 400, INK, "middle", vmid=True)
    s.text(xa + 18, z(10), f"column shaft {fmt(V('D13'), 'in')} across (D13)", 10, 400, INK)
    s.poly([(xa + 30, z(15.4)), (xa + pw / 2, z(COLTOP))], ORANGE, 1)
    s.text(xa + 34, z(15.4), f"connecting piece {fmt(PIECE)} (D15); width {PIECE_W * 12:.2f} in is DERIVED = D06 − D10b", 10, 400, ORANGE, vmid=True)
    derive(f"connecting-piece width {PIECE_W:.4f} ft = D06 - D10b (not a figure in the record or the ledger)")
    s.hdim(xa, xb, G + 40, FL("D06"), ST("D06"), "D06", ext=G + 6, above=False)
    s.hdim(xa + pw / 2, xb - pw / 2, G + 82, FL("D10b"), ST("D10b"), "D10b", ext=G + 6, above=False)
    s.vdim(xa - 50, G, z(COLTOP), f"{fmt(COLTOP)} · D14", ST("D14"), "D14", ext=xa - 8, pos="left")
    s.vdim(xa - 50, z(COLTOP), z(COLTOP + PIECE), f"{fmt(PIECE)} · D15", ST("D15"), "D15", ext=xa - 8, pos="left")
    s.vdim(xb + 50, G, z(TOP[1]), f"{fmt(TOP[1])} · D11a", ST("D11a"), "D11a", ext=xb + 12, pos="above")
    s.vdim(xb + 130, G, z(GALF), f"{fmt(GALF)} · D12", ST("D12"), "D12", ext=xb + 12, pos="above")
    s.mention("D13")
    s.vdim((xa + xb) / 2 + 110, z(TOP[1] - GIRD), z(TOP[1]), f"{fmt(GIRD)} · D10a", ST("D10a"), "D10a", ext=(xa + xb) / 2 + 90)
    s.marker(xa + 40, z(18.0), 1)
    s.marker(xa - 30, z(COLTOP + PIECE / 2), 3)
    s.marker(xa + 140, z(TOP[1] - GIRD) + 16, 4)
    s.marker(xb - 40, z(GALF) + 10, 11)
    s.marker(xb - 40, z(GALF + RAIL) - 12, 12)
    s.close()
    ledger_box(s, 30, 1250, 1400, [1, 2, 3, 4, 11, 12])
    s.footer("Derived on this sheet: " + "; ".join(DERIVED))
    return s.save()


# ================================================================ sheet 5: index
def sheet_index(sheet_names):
    s = Svg(1500, 1900, "5-control-index", "Index — every control and every ledger row, and where it is drawn",
            "Built last, from what the other sheets actually drew; a control with no sheet is not drawn anywhere")
    y = 100
    s.text(30, y, "CONTROLS (controls.json)", 14, 600)
    y += 14
    for xx, h in ((30, "ID"), (90, "What"), (790, "Stated"), (900, "Status"), (1010, "Drawn on")):
        s.text(xx, y + 12, h, 10, 600, GREY)
    y += 20
    allc = list(CTL_DOC["controls"])
    for c in allc:
        cid = c["id"]
        st = ST(cid)
        d, col = STY[st]
        s.line(30, y + 16, 1470, y + 16, LIGHT, .5)
        s.text(30, y + 12, cid, 10, 600)
        s.text(90, y + 12, clean(c["what"])[:112], 10)
        s.text(790, y + 12, fmt(c["stated"], c.get("unit", "ft")), 10)
        s.line(900, y + 8, 928, y + 8, col, 1.5, d)
        s.text(936, y + 12, c["status"], 10)
        drawn = sorted(DRAWN.get(cid, []))
        s.text(1010, y + 12, ", ".join(drawn) if drawn else "NOT DRAWN (no sheet)", 10, 500 if drawn else 600, INK if drawn else RED)
        y += 18
    y += 30
    s.text(30, y, "NOT A CONTROL (controls.json not_included)", 12, 600)
    y += 6
    for n in CTL_DOC.get("not_included", []):
        y = s.block(30, y + 6, f"{n['id']}: {n['why']}", 1400, 9.5) + 2
    y += 18
    s.text(30, y, "LEDGER ROWS (DEPARTURES-LEDGER.md)", 14, 600)
    y += 14
    for xx, h in ((30, "Row"), (80, "Part"), (470, "Strongest word"), (590, "Disclose in film?"), (800, "Marked on")):
        s.text(xx, y + 12, h, 10, 600, GREY)
    y += 20
    for n in sorted(LEDGER):
        r = LEDGER[n]
        s.line(30, y + 16, 1470, y + 16, LIGHT, .5)
        s.circle(46, y + 8, 7, "#FFFFFF", CLS_COL[r["cls"]], 1.5)
        s.text(46, y + 8, f"L{n}", 7, 600, CLS_COL[r["cls"]], "middle", vmid=True)
        s.text(80, y + 12, r["part"][:60], 10)
        s.text(470, y + 12, r["cls"], 10, 500, CLS_COL[r["cls"]])
        s.text(590, y + 12, r["disclose"][:44], 10)
        mk = sorted(MARKED.get(n, []))
        s.text(800, y + 12, ", ".join(mk) if mk else "not marked on any sheet", 10, 400 if mk else 500, INK if mk else GREY)
        y += 18
    s.h = y + 80
    s.o[0] = f'<rect id="paper" width="{s.w}" height="{s.h}" fill="{PAPER}"/>'
    s.footer()
    return s.save()


if __name__ == "__main__":
    made = [sheet_plan(), sheet_stair(), sheet_section(), sheet_bay()]
    made.append(sheet_index([p.stem for p in made]))
    manifest = {"generated": datetime.date.today().isoformat(),
                "inputs": {"controls.json": sha(F_CONTROLS), "DEPARTURES-LEDGER.md": sha(F_LEDGER), "build_slice.py": sha(F_BUILD)},
                "plan": {"bays": NBAYS, "stair_bays": sorted(STAIR_BAYS), "nave_first_bay": NAVE_FIRST},
                "sheets": [p.name for p in made],
                "controls_not_drawn": sorted(c["id"] for c in CTL_DOC["controls"] if c["id"] not in DRAWN),
                "ledger_rows_not_marked": sorted(n for n in LEDGER if n not in MARKED),
                "derived_here": DERIVED}
    (OUT / "manifest.json").write_text(json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps(manifest, indent=2, ensure_ascii=False))
