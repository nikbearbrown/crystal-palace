# CP020 wrapper (2026-11-11): render_views.py with people_lib v3.3 (survey d19449b), the lib that made live renders/f03/CP020_floor_start.png
# (fitout 0c6f2e4, survey people/batch_people_v33_statues.py). Lib copy made by scripts/render_cp020_nave.sh in /workspace/tmp/cp020/ppl33.
import sys, importlib.util
spec = importlib.util.spec_from_file_location("people_lib", "/workspace/tmp/cp020/ppl33/people_lib.py")
m = importlib.util.module_from_spec(spec); sys.modules["people_lib"] = m; spec.loader.exec_module(m)
sys.modules["cpl_people"] = m
RV = "/workspace/crystal-palace-fitout/course-models/crystal-palace-1851-fitout-grok/scripts/render_views.py"
g = {"__name__": "__main__", "__file__": RV}
exec(compile(open(RV).read(), RV, "exec"), g)
