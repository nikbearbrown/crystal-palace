# CP026 wrapper (copied from /workspace/tmp/cp026/rv31.py 2026-11-10): render_views.py with people_lib v3.1 (survey 0dfacfa), the lib that made live renders/h03/CP026 (fitout b7069ee)
import sys, importlib.util
spec = importlib.util.spec_from_file_location("people_lib", "/workspace/tmp/cp026/ppl31/people_lib.py")
m = importlib.util.module_from_spec(spec); sys.modules["people_lib"] = m; spec.loader.exec_module(m)
sys.modules["cpl_people"] = m
RV = "/workspace/crystal-palace-fitout/course-models/crystal-palace-1851-fitout-grok/scripts/render_views.py"
g = {"__name__": "__main__", "__file__": RV}
exec(compile(open(RV).read(), RV, "exec"), g)
