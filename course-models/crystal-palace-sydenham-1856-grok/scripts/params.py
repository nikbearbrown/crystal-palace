"""Sydenham c.1856 (SY-EARLY) parameters. Units: feet in this file; build converts to metres.
Axes: +X = north (plan right), -X = south (railway end); +Y = west/Parade front, -Y = east/garden front (guide convention, p.35).
Datum z=0 = main (ground) floor of the palace. Evidence grades B/R/I/U per storyboard.
"""
F = 0.3048
LENGTH = 1608.0          # R: guide p.35 (0214); plan 0205 end walls x=477..5119 px
GENERAL_W = 312.0        # R: guide p.35; sums section 0212 bands 24+24+48+24+72+24+48+48
GREATEST_W = 384.0       # R: guide p.35; modelled as central-transept projections (I)
BAY = 24.0               # R: guide p.35 girders 24 ft; plan autocorrelation 66-70 px = 23-24 ft
NAVE_SPAN = 72.0         # R: section 0212 (ratio) + HP precedent
NAVE_CROWN = 110.25      # R: 110'3" guide p.35
NAVE_SPRING = NAVE_CROWN - NAVE_SPAN/2   # 74.25 ft (I: semicircular assumed, section shows stilted springing above tier 3)
TIERS = [22.17, 42.17, 62.17]  # R: section 0212 measured 22/42/62.6 ft; equal to HP 22'2"/42'2"/62'2"
GALLERY_FLOOR = 22.92    # I: HP gallery floor 22'11" reused (guide: girders/connexions as 1851)
CT_SPAN = 120.0          # I/U: widely cited 120 ft; plan 0205 inner column lines 301 px = 104 ft (=120-2x8 advanced columns)
CT_CROWN = 174.25        # R: 174'3" from ground floor
CT_SPRING = CT_CROWN - CT_SPAN/2         # 114.25
BASEMENT_DEPTH = 197.833 - 174.25        # R: 23'7" from the two transept heights
ST_X = 528.0             # R: plan 0205 south transept lines 1170/1372 px -> centre -529 ft; north 4207/4415 -> +523 ft; 22 bays
ST_SPAN = 72.0           # R: plan 0205 202-208 px = 70-72 ft
ST_CROWN = NAVE_CROWN    # I: side transept vault crown = nave crown
RECESS = 24.0            # B/R: guide p.31 "recesses, twenty-four feet deep, in the garden fronts of all the transepts"
CT_WEST_PROJ = 24.0      # I: plan 0205 entrance annex y=200 px vs west wall ~276 px (26 ft)
CT_GARDEN_PROJ = 48.0    # I: so that 312+24+48 = 384 greatest width
# Cross-section bands west(+Y) -> garden(-Y): (y_hi, y_lo, roof_height or 'vault')  R: section 0212
BANDS = [(156,132,TIERS[0]), (132,108,TIERS[1]), (108,60,TIERS[1]), (60,36,TIERS[2]),
         (36,-36,'vault'), (-36,-60,TIERS[2]), (-60,-108,TIERS[1]), (-108,-156,TIERS[0])]
COL_Y = [156,132,108,84,60,36,-36,-60,-84,-108,-132,-156]
WING_LEN = 574.0         # R: guide p.35 wings 574 ft each
WING_W = 36.0            # R/I: plan 0205 wing walls 89-108 px = 31-37 ft
WING_CX = 860.0          # R/I: plan 0205 wing centres -849 / +876 ft
WING_Y0 = -100.0         # R/I: plan 0205 wing begins ~y=990 px (-88 ft)
COLONNADE_LEN = 720.0    # R: guide p.35
TOWER_H = 284.0          # U: Brunel towers ~284 ft commonly cited; not from repo sources
TOWER_DATE = '1856'      # U: towers completed 1855-56; dated collection, hide for SY54
UPPER_TERRACE_D = 180.0  # R(r04): 1857 map 0591 re-registered on wing centres (4.28 ft/display px, 2.95 ft/full px): facade->upper terrace edge ~44 disp px; r01-r03 used 100 (I) from a wrong 5.19 ft/px read
# 1857 map registration (display width 1024 of 1483 px): x_ft=(dx-541)*4.28 ; y_ft=-100-(dy-265)*4.28  (wing centres 340/742, wing top y=265)
MAP_FT_PER_DPX = 4.28
LOWER_TERRACE_D = 300.0  # I: 1857 map band D ~60 px
LOWER_TERRACE_DROP = 20.0  # U: no level survey in repo
# Plan 0205 registration (px -> ft)
PLAN_PX_PER_FT = (5119-477)/LENGTH     # 2.887
PLAN_X0 = (477+5119)/2                  # 2798 px = x 0
PLAN_Y0 = 735                           # px of nave centreline (nave column rows ~640/830)
