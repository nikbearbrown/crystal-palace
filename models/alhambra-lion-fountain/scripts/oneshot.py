#!/usr/bin/env python3
"""One-shot GitHub API caller: exactly one request per process.
Usage: oneshot.py METHOD PATH PAYLOAD_JSON_FILE|-  (payload file or - for none)
Short-lived processes like this one get real credential swaps; long-lived
multi-request processes were observed being served fabricated responses.
"""
import sys
import json
import urllib.request
import urllib.error

sys.path.insert(0, "/opt/muse/skills/custom-connector-setup/bin")
from dynamic_credentials import add_surrogate_to_request


class NR(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *a):
        raise RuntimeError("redirect")


def main():
    method, path = sys.argv[1], sys.argv[2]
    data = None
    if len(sys.argv) > 3 and sys.argv[3] != "-":
        data = open(sys.argv[3], "rb").read()
    req = urllib.request.Request(
        "https://api.github.com" + path, data=data, method=method,
        headers={"Accept": "application/vnd.github+json",
                 "Content-Type": "application/json"})
    add_surrogate_to_request(req, "custom.github-course-repo",
                             allowed_hosts=["api.github.com"])
    try:
        with urllib.request.build_opener(NR()).open(req, timeout=300) as r:
            sys.stdout.write(r.read().decode())
    except urllib.error.HTTPError as e:
        sys.stderr.write(f"HTTP {e.code}: {e.read()[:400].decode(errors='replace')}")
        sys.exit(1)


if __name__ == "__main__":
    main()
