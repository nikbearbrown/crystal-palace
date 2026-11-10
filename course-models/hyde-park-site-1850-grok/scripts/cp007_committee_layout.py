"""CP007 Building Committee design (June 1850) -- layout in plan feet, shared by the candidate model build and the
drawn ground-plan sheet. u = feet east from the west end wall, v = feet north from the south front wall.
Sources (read 2026-11-10):
  * 'The Crystal Palace' (1851, Bogue; Gutenberg 44192), 'Description of the Building Committee's Design' + the
    'Ground plan of the Building Committee's design' and 'Exterior view' engravings (pp. 22/24):
      length about 2,200 ft, greatest width nearly 450 ft; rotunda 200 ft diameter; cupola more than 160 ft high;
      wrought-iron ribs + corrugated iron on a brick drum about 60 ft high; glazed central opening;
      avenues 48 ft wide on 24 ft columns; main E-W avenue on semicircular ribs, 52 ft high; other avenues 36 ft,
      railway-shed roofs in slate with skylights at the apex; 15 ft corridor round the building; brick enclosing walls
      'relieved externally by panels in two colours'; arched recesses at the principal (south, opposite Prince's Gate),
      end and north entrances; pent roof ~15 ft along the principal front and ends; 24 exit doors with porches;
      courts left open for the trees (west octagon court; north-east refreshment court; small court '8').
  * Tallis 1852 (e-rara): main building 60 ft, dome 'more than 150', 200 ft diameter, 15 million bricks.
Plan positions are measured off the p.22 ground plan (2644 px scan; 2,515 px = 2,200 ft, 0.875 ft/px): grade B outline,
C detail.  Heights: text values (A for 36/52/60/160 ft); pavilion/gable proportions read off the p.24 view (C)."""
L = 2200.0                      # length (text: 'about 2,200 ft')
AXIS_V = 144.0                  # main avenue / rotunda axis (plan: 139-146)
MAIN_V = (120.0, 168.0)         # 48 ft main avenue
ROT_U, ROT_V, ROT_R = 1000.0, AXIS_V, 100.0
DRUM_H, DOME_TOP = 60.0, 163.0  # drum 'about 60'; cupola 'more than 160'
EAVE, RIDGE = 30.0, 36.0        # avenues 36 ft 'from the floor' (ridge); eaves inferred
MAIN_SPRING, MAIN_CROWN = 28.0, 52.0
WALL_H = 32.0                   # enclosing wall + parapet (inferred, just above the 30 ft eaves)
AV = 48.0
# north wall line, stepped as the plan (u0, u1, v_north)
NORTH = [(0.0, 90.0, 322.0), (90.0, 282.0, 335.0), (282.0, 445.0, 375.0), (445.0, 2008.0, 418.0), (2008.0, 2200.0, 351.0)]
# open courts (u0, u1, v0, v1, kind)
COURTS = [(445.0, 637.0, 205.0, 418.0, "octagon"),        # 4: west court round the elm clump (refreshments)
          (1461.0, 1563.0, 172.0, 260.0, "small"),         # 8: small court with a fountain
          (1738.0, 2008.0, 300.0, 418.0, "refresh")]       # A: north-east refreshment court with trees
# arched entrance pavilions: (u, v_face, facing, width, eave, gable_top, arch_r, arch_spring, depth)
PAVILIONS = [(ROT_U, 0.0, "S", 120.0, 56.0, 80.0, 44.0, 24.0, 24.0),     # principal entrance (10), opposite Prince's Gate
             (0.0, AXIS_V, "W", 96.0, 44.0, 64.0, 34.0, 18.0, 20.0),     # west end (11)
             (L, AXIS_V, "E", 96.0, 44.0, 64.0, 34.0, 18.0, 20.0),       # east end (11)
             (ROT_U + 27.0, 418.0, "N", 96.0, 44.0, 64.0, 34.0, 18.0, 16.0)]  # north entrance (11)
PORCHES_S = [150.0, 380.0, 640.0, 1330.0, 1600.0, 1880.0, 2080.0]          # exit-door porches on the south front (C)
OFFICES = [(890.0, 935.0), (1065.0, 1110.0)]                                 # executive offices flanking the principal entrance
TREES = [  # (u, v, crown radius ft, height ft) -- elms in courts and outside the north wall, from the plan hatching
    (505, 300, 34, 80), (545, 330, 36, 86), (585, 290, 30, 74), (530, 265, 26, 70), (560, 365, 28, 72), (600, 340, 24, 66),
    (1790, 360, 30, 74), (1850, 345, 34, 80), (1910, 360, 30, 76), (1965, 350, 26, 70),
    (1065, 440, 40, 84), (1080, 395, 30, 76), (1050, 340, 26, 70), (1110, 470, 34, 80),
    (1640, 445, 30, 70), (1700, 455, 34, 78), (1765, 450, 28, 70)]
ROAD_DRIVE_V = -55.0            # the drive in the park (12), south of the building
ROAD_KENS_V = -150.0            # Kensington Road (13)
ROTTEN_ROW_V = 470.0            # Rotten Row (14) north

def north_v(u):
    for a, b, v in NORTH:
        if a <= u < b: return v
    return NORTH[-1][2]

def rot_halfchord(u0, u1):
    """smallest half-chord of the rotunda circle over [u0,u1] (strip roof pushed into the drum, hidden), None if clear."""
    d = max(abs(u0 - ROT_U), abs(u1 - ROT_U))
    if min(abs(u0 - ROT_U), abs(u1 - ROT_U)) > ROT_R and not (u0 < ROT_U < u1): return None
    d = min(d, ROT_R - 0.5)
    return (ROT_R ** 2 - d ** 2) ** 0.5

def cut(iv, a, b):
    out = []
    for (x0, x1) in iv:
        if b <= x0 or a >= x1: out.append((x0, x1)); continue
        if a > x0: out.append((x0, a))
        if b < x1: out.append((b, x1))
    return [s for s in out if s[1] - s[0] > 2.0]

def strips():
    """N-S avenue strips (u0, u1, v0, v1) south and north of the main avenue, minus courts and rotunda."""
    res = []; u = 20.0
    while u < L - 20.0 - 1e-6:
        u0, u1 = u, min(u + AV, L - 20.0); uc = 0.5 * (u0 + u1)
        iv = [(20.0, MAIN_V[0]), (MAIN_V[1], north_v(uc) - 20.0)]
        hc = rot_halfchord(u0, u1)
        if hc is not None: iv = cut(iv, ROT_V - hc, ROT_V + hc)
        if 930.0 < uc < 1070.0: iv = cut(iv, 0.0, ROT_V)          # principal entrance vestibule + offices
        for (a, b, c, d, k) in COURTS:
            if u1 > a and u0 < b: iv = cut(iv, c, d)
        for (v0, v1) in iv: res.append((u0, u1, v0, v1))
        u += AV
    return res
