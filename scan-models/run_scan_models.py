"""fal.ai image-to-3D for the object scans. Per image: Tripo H3.1 first; if it fails, Trellis 2; then by average
triangle count from the bake-off (Rodin 500,000, Hunyuan 499,605, Meshy 30,587). Stops at the first success.

Reads FAL_KEY from the environment (never printed or written). Every submitted request is logged to ledger.jsonl
before waiting. A failed (model, image) pair is never resubmitted; it moves to the next model in the chain.

    bakeoff/.venv/bin/python scan-models/run_scan_models.py --dry-run
    bakeoff/.venv/bin/python scan-models/run_scan_models.py
"""
import argparse
import json
import threading
import time
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from pathlib import Path

import fal_client

HERE = Path(__file__).resolve().parent
INPUTS, OUTPUTS = HERE / "inputs", HERE / "outputs"
LEDGER, UPLOADS = HERE / "ledger.jsonl", HERE / "uploads.json"
BUDGET = 50.00
MAX_PARALLEL = 2
POLL_SECONDS = 10
CLIENT_TIMEOUT = 45 * 60

CHAIN = [  # (model folder, endpoint, argument builder, estimated cost)
    ("tripo_h31", "tripo3d/h3.1/image-to-3d", lambda u: {"image_url": u}, 0.30),
    ("trellis2", "fal-ai/trellis-2", lambda u: {"image_url": u, "resolution": 1024}, 0.30),
    ("rodin_v25", "fal-ai/hyper3d/rodin/v2.5", lambda u: {"image_urls": [u], "geometry_file_format": "glb"}, 0.40),
    ("hunyuan_pro", "fal-ai/hunyuan-3d/v3.1/pro/image-to-3d", lambda u: {"input_image_url": u}, 0.375),
    ("meshy_71", "meshy/v7.1/image-to-3d", lambda u: {"image_url": u}, 1.20),
]
_lock = threading.RLock()


def now():
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def ledger_append(rec):
    with _lock, LEDGER.open("a") as f:
        f.write(json.dumps(rec) + "\n")


def ledger_state():
    state = {}
    if LEDGER.exists():
        for line in LEDGER.read_text().splitlines():
            if line.strip():
                r = json.loads(line)
                state.setdefault((r["model"], r["image_id"]), {}).update(r)
    return state


def committed_spend(state):
    """Every request that got an id counts, failed ones included: billing on a failure is unknown."""
    return sum(r.get("est_cost", 0) for r in state.values() if r.get("request_id"))


def upload(path):
    key = f"{path.name}:{path.stat().st_size}"
    with _lock:
        cache = json.loads(UPLOADS.read_text()) if UPLOADS.exists() else {}
        if key in cache:
            return cache[key]
    url = fal_client.upload_file(path)
    with _lock:
        cache = json.loads(UPLOADS.read_text()) if UPLOADS.exists() else {}
        cache[key] = url
        UPLOADS.write_text(json.dumps(cache, indent=1))
    return url


def glb_url(model, res):
    if model == "tripo_h31":
        mu = res.get("model_urls") or {}
        for k in ("glb", "pbr_model"):
            if mu.get(k) and mu[k].get("url"):
                return mu[k]["url"]
        return res["model_mesh"]["url"]
    if model == "rodin_v25":
        return res["model_mesh"]["url"]
    return res["model_glb"]["url"]


def download(url, dest):
    dest.parent.mkdir(parents=True, exist_ok=True)
    with urllib.request.urlopen(url, timeout=300) as r, dest.open("wb") as f:
        while chunk := r.read(1 << 20):
            f.write(chunk)
    return dest.stat().st_size


def finish(model, image_id, endpoint, request_id, started):
    """True on success (GLB downloaded), False on a failed job, None if still running on fal."""
    try:
        res = fal_client.result(endpoint, request_id)
        out = OUTPUTS / model / f"{image_id}.glb"
        (OUTPUTS / model).mkdir(parents=True, exist_ok=True)
        (OUTPUTS / model / f"{image_id}.result.json").write_text(json.dumps(res, indent=1))
        size = download(glb_url(model, res), out)
    except Exception as e:
        ledger_append({"model": model, "image_id": image_id, "request_id": request_id, "ts": now(),
                       "status": "failed", "error": str(e)[:400]})
        print(f"[{model}/{image_id}] FAILED: {str(e)[:200]}", flush=True)
        return False
    ledger_append({"model": model, "image_id": image_id, "request_id": request_id, "ts": now(),
                   "status": "completed", "elapsed_s": round(time.time() - started, 1), "file_size": size,
                   "output_path": str(out.relative_to(HERE))})
    print(f"[{model}/{image_id}] done {size/1e6:.1f} MB", flush=True)
    return True


def wait(model, image_id, endpoint, request_id, started):
    while True:
        try:
            st = fal_client.status(endpoint, request_id)
        except Exception as e:
            print(f"[{model}/{image_id}] status error (retrying): {str(e)[:100]}", flush=True)
            time.sleep(POLL_SECONDS)
            continue
        if isinstance(st, fal_client.Completed):
            return finish(model, image_id, endpoint, request_id, started)
        if time.time() - started > CLIENT_TIMEOUT:
            ledger_append({"model": model, "image_id": image_id, "request_id": request_id, "ts": now(),
                           "status": "client_timeout"})
            print(f"[{model}/{image_id}] client timeout; job still running on fal", flush=True)
            return None
        time.sleep(POLL_SECONDS)


def run_image(image_id, dry_run):
    for model, endpoint, make_args, est in CHAIN:
        state = ledger_state().get((model, image_id), {})
        if state.get("status") == "completed" and (HERE / state.get("output_path", "x")).exists():
            print(f"[{model}/{image_id}] already completed", flush=True)
            return
        if state.get("request_id"):
            if state["status"] == "failed":
                print(f"[{model}/{image_id}] failed earlier; next model", flush=True)
                continue
            if dry_run:
                continue
            ok = wait(model, image_id, state.get("endpoint", endpoint), state["request_id"], time.time())
            if ok:
                return
            if ok is None:
                return  # still running; rerun later
            continue
        with _lock:  # budget check, upload, submit and ledger write are one atomic step
            spent = committed_spend(ledger_state())
            if spent + est > BUDGET + 1e-9:
                print(f"[{model}/{image_id}] REFUSED: ${spent:.3f} + ${est:.3f} would exceed ${BUDGET:.2f}", flush=True)
                return
            if dry_run:
                print(f"[{model}/{image_id}] would submit to {endpoint} (est ${est:.3f}, running ${spent+est:.3f})")
                return
            handle = fal_client.submit(endpoint, arguments=make_args(upload(INPUTS / f"{image_id}.png")))
            started = time.time()
            with LEDGER.open("a") as f:
                f.write(json.dumps({"model": model, "image_id": image_id, "endpoint": endpoint,
                                    "request_id": handle.request_id, "ts": now(), "est_cost": est,
                                    "status": "submitted"}) + "\n")
        print(f"[{model}/{image_id}] submitted {handle.request_id}", flush=True)
        ok = wait(model, image_id, endpoint, handle.request_id, started)
        if ok or ok is None:
            return
    print(f"[{image_id}] ALL MODELS FAILED", flush=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--only", help="comma-separated image ids")
    args = ap.parse_args()
    ids = [o["slug"] for o in json.loads((HERE / "objects.json").read_text())]
    if args.only:
        ids = [i for i in ids if i in args.only.split(",")]
    for i in ids:
        if not (INPUTS / f"{i}.png").exists():
            raise SystemExit(f"missing input {i}")
    print(f"{len(ids)} images, first-choice estimate ${sum(CHAIN[0][3] for _ in ids):.2f}, cap ${BUDGET:.2f}")
    with ThreadPoolExecutor(MAX_PARALLEL) as ex:
        list(ex.map(lambda i: run_image(i, args.dry_run), ids))
    print(f"committed estimate: ${committed_spend(ledger_state()):.3f}")


if __name__ == "__main__":
    main()
