"""Shim: import people v2 from this folder or the survey people/ tree."""
from __future__ import annotations
import sys
from pathlib import Path

_HERE = Path(__file__).resolve().parent
if str(_HERE) not in sys.path:
    sys.path.insert(0, str(_HERE))
try:
    from people_lib import (  # noqa: F401
        PEOPLE_VERSION, catalogue, clear_mesh_cache, person_mesh,
        resolve_role, swap_scene_people, ERA_ROLES, POSES,
    )
except ImportError:
    _SURVEY = Path("/workspace/crystal-palace-survey/people")
    if str(_SURVEY) not in sys.path:
        sys.path.insert(0, str(_SURVEY))
    from people_lib import (  # noqa: F401
        PEOPLE_VERSION, catalogue, clear_mesh_cache, person_mesh,
        resolve_role, swap_scene_people, ERA_ROLES, POSES,
    )
