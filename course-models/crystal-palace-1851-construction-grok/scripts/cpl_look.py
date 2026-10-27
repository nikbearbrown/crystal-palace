"""Import crystal-palace-look v1 from the shared survey copy.

Usage in a render script:

    from cpl_look import apply_look, era_for_scene, tod_for_scene
    apply_look(era=era_for_scene("CP017"), time_of_day=tod_for_scene("CP017", cam_name))
"""
import sys
from pathlib import Path
_CPL = Path("/workspace/crystal-palace-survey/look")
if str(_CPL) not in sys.path:
    sys.path.insert(0, str(_CPL))
from crystal_palace_look import (  # noqa: E402
    LOOK_VERSION, apply_look, era_for_scene, tod_for_scene,
    clamp_materials, EXPOSURE, ERA_SUN_RGB, SUN,
)
