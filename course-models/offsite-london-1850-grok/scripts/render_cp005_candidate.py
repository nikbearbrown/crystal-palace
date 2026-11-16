#!/usr/bin/env python3
"""CANDIDATE renders for CP005 (ln03_cp005) with the SAME pipeline as the live CP005 hero
(survey look/batch_mat_keeplight.py): enhance_offsite_materials + render_views --keep-lighting,
era 1850 (live CP005 recipe; pass --era 1840s for the CP002 side-effect cams, = live CP002 recipe), 1280x720, 28 spp,
authored exposure (-0.10 in both ln02 and ln03_cp005).

usage: render_cp005_candidate.py <blend> <cams,comma> <outdir> [--samples N] [--era 1850|1840s]
Writes <outdir>/<cam>.png. Never writes into renders/ln02 (live)."""
import subprocess, sys, textwrap
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
LOOK = "/workspace/crystal-palace-survey/look"
blend, cams, outdir = sys.argv[1], sys.argv[2], Path(sys.argv[3]).resolve()
samples = sys.argv[sys.argv.index("--samples") + 1] if "--samples" in sys.argv else "28"
era = sys.argv[sys.argv.index("--era") + 1] if "--era" in sys.argv else "1850"   # CP005 live recipe (batch_mat_keeplight.py) = era 1850; CP002 cams = 1840s
assert "renders/ln02" not in str(outdir), "refusing to write into live renders/ln02"
outdir.mkdir(parents=True, exist_ok=True)
drv = Path(f"/tmp/cp005_cand_drv_{abs(hash((blend, cams, str(outdir), era)))}.py")
drv.write_text(textwrap.dedent(f'''
    import runpy, sys
    sys.path.insert(0, "{LOOK}")
    import enhance_offsite_materials as E
    E.enhance()
    sys.argv = ["render_views.py", "--", "--cams", "{cams}", "--res", "1280x720", "--samples", "{samples}",
                "--era", "{era}", "--tod", "exterior_midday", "--threads", "8",
                "--keep-lighting", "--outdir", "{outdir}"]
    runpy.run_path("{ROOT / 'scripts' / 'render_views.py'}", run_name="__main__")
'''))
rc = subprocess.run(["/workspace/blender5/blender", "-b", str(Path(blend).resolve()), "-P", str(drv)], cwd=str(ROOT)).returncode
sys.exit(rc)
