#!/usr/bin/env python3
"""Crystal Palace research scraper (CSYE 7270 course research).

Crawls Wikimedia for architectural material on the Crystal Palace (1851):

  1. Seed article  -- every image on en.wikipedia.org/wiki/The_Crystal_Palace
  2. First hop     -- every image on every namespace-0 article the seed links to
  3. Commons       -- every file in the Crystal Palace Commons categories
                      (subcategories walked 2 levels deep)

Everything goes through the MediaWiki API (no HTML scraping). Files are
downloaded once (deduped by Commons file title) and every source page that
referenced a file is recorded in the manifest.

Outputs (relative to the project root, the parent of this script's folder):
  data/manifest.json / data/manifest.csv   one record per image file
  data/pages.json                          every page visited + image counts
  data/seed-article.txt                    plain-text extract of the seed article
  images/main-article/                     files first seen on the seed article
  images/linked/<page-slug>/               files first seen on a linked page
  images/commons/                          files only found via Commons categories

Politeness: descriptive User-Agent, batched API queries (50 titles), a short
pause between file downloads, retries (honoring Retry-After) on transient
errors. The HTTP session also retries dropped connections at the adapter
level with backoff, because the egress proxy intermittently resets them.

Caps: files larger than 45 MB are logged as "skipped-too-large"; audio,
video and PDFs are logged as "skipped-media"; downloads stop once the running
total passes ~900 MB (remaining files logged as "skipped-budget").

Usage:  python3 scrape_crystal_palace.py [--root DIR] [--pause SECONDS]
"""

from __future__ import annotations

import argparse
import csv
import html
import json
import re
import signal
import sys
import time
import unicodedata
from pathlib import Path
from urllib.parse import unquote

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# --------------------------------------------------------------------------
# Config
# --------------------------------------------------------------------------

EN_API = "https://en.wikipedia.org/w/api.php"
COMMONS_API = "https://commons.wikimedia.org/w/api.php"
SEED_TITLE = "The_Crystal_Palace"
SEED_URL = "https://en.wikipedia.org/wiki/The_Crystal_Palace"
COMMONS_CATEGORY_CANDIDATES = ["Category:Crystal Palace (building)"]

USER_AGENT = "MuseCrystalPalaceResearch/1.0 (CSYE 7270 course research)"
MAX_FILE_BYTES = 45 * 1024 * 1024        # skip individual files over 45 MB
TOTAL_BUDGET_BYTES = 900 * 1024 * 1024   # stop downloading past ~900 MB
DOWNLOAD_PAUSE = 2.0                     # seconds between file downloads
SKIP_MIME_PREFIXES = ("audio/", "video/")
SKIP_EXTENSIONS = {".pdf", ".ogg", ".ogv", ".webm", ".mp3", ".wav", ".flac",
                   ".mid", ".midi", ".djvu"}
# TIFF masters are kept (they are often the best plan/drawing scans); the
# 45 MB per-file cap below is what governs them.

SESSION = requests.Session()
SESSION.headers.update({"User-Agent": USER_AGENT})
# The egress proxy in this environment intermittently hard-drops connections
# (ProxyError: Remote end closed connection without response, ~25-50% of
# requests). Absorb those at the adapter level with fast backoff so a single
# flaky connection costs seconds, not minutes. HTTP 429/5xx are still handled
# by the application-level logic below (which honors Retry-After).
_adapter_retry = Retry(
    total=2,                 # deliberately small: a dropped connection should
    backoff_factor=0.5,      # cost ~1s, not minutes; the app layer decides
    status_forcelist=[500, 502, 503, 504],
    allowed_methods=["GET"],
    raise_on_status=False,
)
SESSION.mount("https://", HTTPAdapter(max_retries=_adapter_retry))
SESSION.mount("http://", HTTPAdapter(max_retries=_adapter_retry))


# --------------------------------------------------------------------------
# Small helpers
# --------------------------------------------------------------------------

def api_get(api: str, params: dict, retries: int = 4, timeout: int = 60) -> dict:
    """One MediaWiki API GET with polite retries.

    Backs off (honoring Retry-After) when the API rate-limits, and a short
    pause follows every successful call to keep the request rate modest.
    NOTE: Wikimedia's maxlag parameter is intentionally NOT sent - the
    egress proxy in this environment hard-drops any API request carrying
    it (ProxyError: Remote end closed connection without response).
    """
    params = {**params, "format": "json", "formatversion": "2"}
    last_err = None
    for attempt in range(retries + 1):
        try:
            r = SESSION.get(api, params=params, timeout=timeout)
            if r.status_code == 429:
                wait = int(r.headers.get("Retry-After", 0)) or 10 * (attempt + 1)
                print(f"  (rate limited; backing off {wait}s)", file=sys.stderr)
                time.sleep(wait)
                continue
            r.raise_for_status()
            time.sleep(0.25)
            return r.json()
        except Exception as exc:  # noqa: BLE001 - report and retry
            last_err = exc
            if attempt < retries:
                time.sleep(3.0 * (attempt + 1))
    raise RuntimeError(f"API call failed ({api}): {last_err}")


def strip_html(text: str | None) -> str:
    if not text:
        return ""
    text = re.sub(r"<[^>]+>", " ", text)
    return re.sub(r"\s+", " ", html.unescape(text)).strip()


def slugify(title: str) -> str:
    """Filesystem-safe slug for a Wikipedia article title."""
    s = unicodedata.normalize("NFKD", title).encode("ascii", "ignore").decode()
    s = re.sub(r"[^A-Za-z0-9._-]+", "-", s).strip("-._").lower()
    return s[:80] or "page"


def safe_filename(file_title: str) -> str:
    """Keep the Commons file title; replace characters illegal on disk."""
    name = file_title[len("File:"):] if file_title.startswith("File:") else file_title
    name = unquote(name).replace(" ", "_")
    name = re.sub(r'[\\/:*?"<>|\x00-\x1f]', "_", name)
    return name[:180] or "unnamed"


def batched(seq: list, n: int):
    for i in range(0, len(seq), n):
        yield seq[i:i + n]


# --------------------------------------------------------------------------
# API collectors
# --------------------------------------------------------------------------

def page_images(api: str, titles: list[str]) -> dict[str, list[str]]:
    """prop=images for many pages at once -> {page title: [File: titles]}.

    Keys are the canonical (space-form) titles the API returns, regardless
    of whether the input used underscores.
    """
    canon = {t: t.replace("_", " ") for t in titles}
    out: dict[str, list[str]] = {c: [] for c in canon.values()}
    for batch in batched(titles, 50):
        params = {"action": "query", "prop": "images", "imlimit": "max",
                  "titles": "|".join(batch)}
        while True:
            data = api_get(api, params)
            for page in data.get("query", {}).get("pages", []):
                title = page.get("title", "")
                if title in out:
                    out[title].extend(
                        im["title"] for im in page.get("images", [])
                        if im.get("ns") == 6)
            cont = data.get("continue")
            if not cont:
                break
            params.update(cont)
    return out


def seed_links() -> list[str]:
    """All namespace-0 article titles the seed article links to."""
    titles: list[str] = []
    params = {"action": "query", "prop": "links", "plnamespace": "0",
              "pllimit": "max", "titles": SEED_TITLE}
    while True:
        data = api_get(EN_API, params)
        for page in data.get("query", {}).get("pages", []):
            titles.extend(l["title"] for l in page.get("links", [])
                          if l.get("ns") == 0)
        cont = data.get("continue")
        if not cont:
            break
        params.update(cont)
    return sorted(set(titles))


def image_info(api: str, file_titles: list[str]) -> dict[str, dict]:
    """imageinfo (url/size/mime/extmetadata) for many files -> {title: info}."""
    out: dict[str, dict] = {}
    for batch in batched(sorted(set(file_titles)), 50):
        params = {"action": "query", "prop": "imageinfo",
                  "iiprop": "url|size|mime|extmetadata",
                  "titles": "|".join(batch)}
        while True:
            data = api_get(api, params)
            for page in data.get("query", {}).get("pages", []):
                infos = page.get("imageinfo") or []
                if infos:
                    out[page["title"]] = infos[0]
            cont = data.get("continue")
            if not cont:
                break
            params.update(cont)
    return out


def seed_extract() -> str:
    """Plain-text extract of the seed article; non-fatal on failure."""
    try:
        data = api_get(EN_API, {"action": "query", "prop": "extracts",
                                "explaintext": "1", "titles": SEED_TITLE},
                       timeout=180)
        pages = data.get("query", {}).get("pages", [])
        return pages[0].get("extract", "") if pages else ""
    except Exception as exc:  # noqa: BLE001 - extract is a side deliverable
        print(f"  (extract failed, continuing: {exc})", file=sys.stderr)
        return ""


def seed_commons_category() -> str | None:
    """The seed article's Commons category, via Wikidata claim P373."""
    try:
        data = api_get(EN_API, {"action": "query", "prop": "pageprops",
                                "ppprop": "wikibase_item", "titles": SEED_TITLE})
        pages = data.get("query", {}).get("pages", [])
        item = pages[0].get("pageprops", {}).get("wikibase_item") if pages else None
        if not item:
            return None
        wd = api_get("https://www.wikidata.org/w/api.php",
                     {"action": "wbgetclaims", "entity": item, "property": "P373"})
        claims = wd.get("claims", {}).get("P373", [])
        if claims:
            return "Category:" + claims[0]["mainsnak"]["datavalue"]["value"]
    except Exception as exc:  # noqa: BLE001
        print(f"  (commons-category lookup failed: {exc})", file=sys.stderr)
    return None


def commons_category_size(category: str) -> int:
    """Quick non-empty check: number of direct file+subcat members."""
    try:
        params = {"action": "query", "list": "categorymembers",
                  "cmtitle": category, "cmtype": "file|subcat", "cmlimit": "5"}
        data = api_get(COMMONS_API, params)
        return len(data.get("query", {}).get("categorymembers", []))
    except Exception:  # noqa: BLE001
        return 0


def commons_category_files(root_category: str, depth: int = 2) -> set[str]:
    """All File: titles in a Commons category tree, `depth` levels of subcats."""
    files: set[str] = set()
    seen_cats: set[str] = set()
    frontier = [root_category]
    for level in range(depth + 1):
        next_frontier: list[str] = []
        for cat in frontier:
            if cat in seen_cats:
                continue
            seen_cats.add(cat)
            cmtypes = ["file"] + (["subcat"] if level < depth else [])
            for cmtype in cmtypes:
                params = {"action": "query", "list": "categorymembers",
                          "cmtitle": cat, "cmtype": cmtype, "cmlimit": "max"}
                while True:
                    data = api_get(COMMONS_API, params)
                    for member in data.get("query", {}).get("categorymembers", []):
                        if cmtype == "file" and member.get("ns") == 6:
                            files.add(member["title"])
                        elif cmtype == "subcat" and member.get("ns") == 14:
                            next_frontier.append(member["title"])
                    cont = data.get("continue")
                    if not cont:
                        break
                    params.update(cont)
        frontier = next_frontier
    return files


# --------------------------------------------------------------------------
# Downloader
# --------------------------------------------------------------------------

class Downloader:
    def __init__(self, root: Path):
        self.root = root
        self.total_bytes = 0
        self.budget_exhausted = False

    def fetch(self, url: str, dest: Path) -> tuple[int, str | None]:
        """Download url -> dest. Returns (bytes_written, error_or_None).

        upload.wikimedia.org rate-limits aggressively: 429/5xx responses are
        retried a few times honoring Retry-After, then the file is marked as
        an error and the run moves on (a later --resume pass retries errors).
        Retries are deliberately shallow - retry storms against a throttled
        host make the throttling worse for everyone on the shared egress.
        """
        if self.budget_exhausted or self.total_bytes >= TOTAL_BUDGET_BYTES:
            self.budget_exhausted = True
            return 0, "skipped-budget"
        # imageinfo URLs carry ?utm_source=... tracking params; strip them.
        # The bare URL is the canonical, CDN-cacheable file address - the
        # query string makes the URL uncacheable and draws harder throttling.
        url = url.split("?", 1)[0]
        tmp = dest.with_suffix(dest.suffix + ".part")
        waits = (10, 30, 60)
        last_err: str | None = None
        # Fresh session per download: the egress proxy denies repeat
        # requests on a reused keep-alive CONNECT tunnel (HTTP 403 after
        # the first response). A new session forces a new tunnel and
        # downloads reliably.
        sess = requests.Session()
        sess.headers.update({"User-Agent": USER_AGENT})
        sess.mount("https://", HTTPAdapter(max_retries=_adapter_retry))

        class _FileTimeout(Exception):
            pass

        def _alarm_handler(signum, frame):
            raise _FileTimeout("per-file time budget (300s) exceeded")

        for attempt in range(len(waits) + 1):
            # Hard per-file time budget: the egress proxy occasionally
            # blackholes a connection in a way socket timeouts don't catch.
            # SIGALRM bounds the damage to ~5 min per attempt.
            old_handler = signal.signal(signal.SIGALRM, _alarm_handler)
            signal.alarm(300)
            try:
                with sess.get(url, stream=True, timeout=120) as r:
                    if r.status_code == 429 or r.status_code >= 500:
                        retry_after = r.headers.get("Retry-After")
                        wait = int(retry_after) if retry_after else waits[
                            min(attempt, len(waits) - 1)]
                        last_err = f"HTTP {r.status_code}"
                        print(f"    (download {r.status_code}; waiting {wait}s)",
                              file=sys.stderr, flush=True)
                        time.sleep(min(wait, 120))
                        continue
                    r.raise_for_status()
                    written = 0
                    with open(tmp, "wb") as fh:
                        for chunk in r.iter_content(chunk_size=1 << 16):
                            fh.write(chunk)
                            written += len(chunk)
                tmp.replace(dest)
                self.total_bytes += written
                time.sleep(DOWNLOAD_PAUSE)
                return written, None
            except Exception as exc:  # noqa: BLE001
                last_err = f"{type(exc).__name__}: {exc}"
                if attempt < len(waits):
                    time.sleep(5 * (attempt + 1))
            finally:
                signal.alarm(0)
                signal.signal(signal.SIGALRM, old_handler)
        tmp.unlink(missing_ok=True)
        return 0, f"error: {last_err}"


# --------------------------------------------------------------------------
# Main crawl
# --------------------------------------------------------------------------

def classify(info: dict, file_title: str) -> str | None:
    """Return a skip status for a file, or None if it should be downloaded."""
    mime = (info.get("mime") or "").lower()
    ext = Path(file_title).suffix.lower()
    size = info.get("size") or 0
    if mime.startswith(SKIP_MIME_PREFIXES) or ext in SKIP_EXTENSIONS:
        return "skipped-media"
    if size > MAX_FILE_BYTES:
        return "skipped-too-large"
    if not mime.startswith("image/"):
        return "skipped-media"
    return None


def main() -> int:
    global DOWNLOAD_PAUSE
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--root", default=str(Path(__file__).resolve().parents[1]),
                    help="project root (default: parent of scraper/)")
    ap.add_argument("--pause", type=float, default=DOWNLOAD_PAUSE,
                    help="seconds between downloads")
    ap.add_argument("--resume", action="store_true",
                    help="resume: reload collection from data/manifest_raw.json "
                    "and skip records already in data/manifest_partial.json")
    args = ap.parse_args()

    DOWNLOAD_PAUSE = args.pause

    root = Path(args.root)
    data_dir = root / "data"
    img_root = root / "images"
    for d in (data_dir, img_root / "main-article", img_root / "linked",
              img_root / "commons"):
        d.mkdir(parents=True, exist_ok=True)

    dl = Downloader(root)
    if args.resume:
        # Pre-seed the download budget from what's already on disk, so a
        # resumed run (possibly with a reordered queue) can't overshoot the
        # total budget before it encounters the earlier downloads. Only the
        # three Wikimedia-pass folders count toward the budget, not the
        # extra-source folders (downes-*, routledge-*, etc.).
        disk_bytes = sum(
            f.stat().st_size
            for sub in ("main-article", "linked", "commons")
            for f in (img_root / sub).rglob("*") if f.is_file())
        dl.total_bytes = disk_bytes
        print(f"      --resume: {disk_bytes/1e6:.0f} MB already on disk "
              f"(budget {TOTAL_BUDGET_BYTES/1e6:.0f} MB)")
    manifest: dict[str, dict] = {}   # File: title -> record
    pages: list[dict] = []           # visited pages

    def register(file_title: str, source_page: str, section: str,
                 subdir: Path) -> None:
        rec = manifest.get(file_title)
        if rec is None:
            rec = {"title": file_title, "section": section,
                   "source_pages": [], "_subdir": subdir}
            manifest[file_title] = rec
        if source_page not in rec["source_pages"]:
            rec["source_pages"].append(source_page)

    raw_path = data_dir / "manifest_raw.json"
    partial_path = data_dir / "manifest_partial.json"
    resume_raw = None
    if args.resume and raw_path.exists():
        print("      --resume: loading collection from manifest_raw.json")
        resume_raw = json.loads(raw_path.read_text(encoding="utf-8"))
        manifest = {t: {"title": t, "section": r["section"],
                        "source_pages": r["source_pages"],
                        "_subdir": Path(r["subdir"])} for t, r in resume_raw.items()}
        if (data_dir / "pages.json").exists():
            pages = json.loads((data_dir / "pages.json").read_text(encoding="utf-8"))
    if resume_raw is None:
        # -- 1. Seed article ----------------------------------------------------
        print(f"[1/4] Seed article: {SEED_TITLE}")
        seed_map = page_images(EN_API, [SEED_TITLE])
        seed_files = seed_map.get(SEED_TITLE.replace("_", " "), [])
        for f in seed_files:
            register(f, SEED_URL, "main-article", img_root / "main-article")
        pages.append({"title": SEED_TITLE, "url": SEED_URL, "section": "seed",
                      "images_found": len(seed_files), "images_new": len(seed_files)})
        print(f"      {len(seed_files)} images")

        extract = seed_extract()
        if extract:
            (data_dir / "seed-article.txt").write_text(extract, encoding="utf-8")
            print(f"      extract saved ({len(extract)} chars)")

        # -- 2. First hop --------------------------------------------------------
        print("[2/4] First hop: linked articles")
        links = seed_links()
        print(f"      {len(links)} namespace-0 links")
        new_total = 0
        for batch in batched(links, 50):
            mapping = page_images(EN_API, batch)
            for title in batch:
                files = mapping.get(title, [])
                before = len(manifest)
                subdir = img_root / "linked" / slugify(title)
                for f in files:
                    register(f, f"https://en.wikipedia.org/wiki/{title.replace(' ', '_')}",
                             "linked", subdir)
                new = len(manifest) - before
                new_total += new
                pages.append({"title": title,
                              "url": f"https://en.wikipedia.org/wiki/{title.replace(' ', '_')}",
                              "section": "linked", "images_found": len(files),
                              "images_new": new})
        print(f"      +{new_total} new files from linked pages")

        # -- 3. Commons categories ------------------------------------------------
        print("[3/4] Commons categories")
        candidates: list[str] = []
        derived = seed_commons_category()
        if derived:
            candidates.append(derived)
        candidates.extend(c for c in COMMONS_CATEGORY_CANDIDATES if c not in candidates)
        roots: list[str] = []
        for cat in candidates:
            count = commons_category_size(cat)
            print(f"      candidate {cat}: {count} direct members")
            if count > 0:
                roots.append(cat)
        if not roots:
            print("      FATAL: every Commons root category came back empty - "
                  "the Commons pass produced nothing!", file=sys.stderr)
            pages.append({"title": "Commons pass", "url": "", "section": "commons",
                          "images_found": 0, "images_new": 0, "failed": True})
        commons_files: set[str] = set()
        for cat in roots:
            commons_files |= commons_category_files(cat)
        before = len(manifest)
        for f in sorted(commons_files):
            register(f, " & ".join(
                f"https://commons.wikimedia.org/wiki/{c.replace(' ', '_')}" for c in roots),
                "commons", img_root / "commons")
        pages.append({"title": " & ".join(roots) if roots else "Commons pass",
                      "url": ("https://commons.wikimedia.org/wiki/"
                              + roots[0].replace(" ", "_")) if roots else "",
                      "section": "commons", "images_found": len(commons_files),
                      "images_new": len(manifest) - before})
        print(f"      {len(commons_files)} category files from {len(roots)} roots, "
              f"+{len(manifest) - before} new")

        # persist collection + page list so --resume can skip steps 1-3
        raw = {t: {"section": r["section"], "source_pages": r["source_pages"],
               "subdir": str(r["_subdir"])} for t, r in manifest.items()}
        raw_path.write_text(json.dumps(raw, ensure_ascii=False), encoding="utf-8")
        (data_dir / "pages.json").write_text(
            json.dumps(pages, indent=2, ensure_ascii=False), encoding="utf-8")

    # -- 4. Metadata + downloads ----------------------------------------------
    print(f"[4/4] Fetching metadata + downloading {len(manifest)} unique files")
    # Metadata comes from Commons (nearly all Wikipedia files live there);
    # anything missing is retried against the English Wikipedia API, which
    # hosts a small number of local-only files.
    def safe_image_info(api, file_titles):
        out = {}
        for batch in batched(sorted(set(file_titles)), 50):
            try:
                out.update(image_info(api, batch))
            except Exception as exc:  # noqa: BLE001 - one bad batch must not kill the run
                print(f"  (metadata batch failed, marking as errors: {exc})",
                      file=sys.stderr)
        return out

    infos = safe_image_info(COMMONS_API, list(manifest.keys()))
    missing = [t for t in manifest if t not in infos]
    if missing:
        print(f"      {len(missing)} files not on Commons; trying en.wikipedia")
        infos.update(safe_image_info(EN_API, missing))

    # Process the most architecturally valuable sections first so the
    # download budget is spent on the seed article and Commons material
    # before the noisy first-hop tail. Within commons/linked, prioritize
    # files whose titles/descriptions look architectural (plans, sections,
    # elevations, drawings) so throttling or budget exhaustion cuts the
    # least valuable material first.
    ARCH_KEYWORDS = ("plan", "section", "elevation", "blueprint", "drawing",
                     "architect", "paxton", "transept", "nave", "facade",
                     "cross-section", "ground floor", "gallery")

    def _arch_score(title: str, info: dict) -> int:
        t = title.lower()
        meta = info.get("extmetadata") or {}
        desc = strip_html((meta.get("ImageDescription") or {}).get("value"))[:500].lower()
        score = 0
        for kw in ARCH_KEYWORDS:
            if kw in t:
                score += 2
            if kw in desc:
                score += 1
        return score

    SECTION_RANK = {"main-article": 0, "commons": 1, "linked": 2}
    ordered = sorted(
        manifest.items(),
        key=lambda kv: (SECTION_RANK.get(kv[1]["section"], 9),
                        kv[1]["section"],
                        -_arch_score(kv[0], infos.get(kv[0], {})),
                        kv[0]))

    records: list[dict] = []
    downloaded = skipped = errors = 0
    done_titles: set[str] = set()
    if args.resume and partial_path.exists():
        retried = 0
        for r in json.loads(partial_path.read_text(encoding="utf-8")):
            # Error and throttled records are re-queued so a resume pass
            # retries them; downloaded / other skipped records are final.
            if r["status"].startswith("error") or r["status"] == "skipped-throttled":
                retried += 1
                continue
            done_titles.add(r["title"])
            records.append(r)
        print(f"      --resume: {len(done_titles)} records already processed, "
              f"{retried} error records re-queued")
    ordered = [kv for kv in ordered if kv[0] not in done_titles]
    consecutive_throttled = 0
    throttled_break = False
    for i, (file_title, rec) in enumerate(ordered, 1):
      if throttled_break:
          break
      try:
        info = infos.get(file_title, {})
        meta = info.get("extmetadata") or {}
        record = {
            "title": file_title,
            "local_path": "",
            "section": rec["section"],
            "source_pages": rec["source_pages"],
            "original_url": info.get("url", ""),
            "description_url": info.get("descriptionurl", ""),
            "width": info.get("width"),
            "height": info.get("height"),
            "bytes": 0,
            "mime": info.get("mime", ""),
            "license": strip_html((meta.get("LicenseShortName") or {}).get("value")),
            "license_url": (meta.get("LicenseUrl") or {}).get("value", ""),
            "description": strip_html((meta.get("ImageDescription") or {}).get("value"))[:500],
            "status": "",
        }
        skip = classify(info, file_title) if info else "error: no imageinfo"
        if skip:
            record["status"] = skip
            skipped += 1
        else:
            dest_dir: Path = rec["_subdir"]
            dest_dir.mkdir(parents=True, exist_ok=True)
            dest = dest_dir / safe_filename(file_title)
            if dest.exists() and dest.stat().st_size > 0:
                # Resume: a previous run already fetched this file.
                # (dl.total_bytes was pre-seeded from disk, so don't add again.)
                record["status"] = "downloaded"
                record["bytes"] = dest.stat().st_size
                record["local_path"] = str(dest.relative_to(root))
                downloaded += 1
                records.append(record)
                if i % 100 == 0:
                    print(f"      {i}/{len(manifest)} processed, "
                          f"{downloaded} downloaded, {dl.total_bytes/1e6:.0f} MB so far")
                continue
            written, err = dl.fetch(info["url"], dest)
            if err == "skipped-budget":
                record["status"] = "skipped-budget"
                skipped += 1
            elif err:
                record["status"] = err
                errors += 1
                # Circuit breaker: sustained 429 throttling means the egress
                # IP is rate-limited. Stop gracefully rather than burning
                # through the queue marking everything as throttled errors.
                if "429" in err:
                    consecutive_throttled += 1
                    if consecutive_throttled >= 6:
                        print("      circuit breaker: 6 consecutive 429s - "
                              "stopping gracefully", flush=True)
                        throttled_break = True
                else:
                    consecutive_throttled = 0
            else:
                record["status"] = "downloaded"
                record["bytes"] = written
                record["local_path"] = str(dest.relative_to(root))
                downloaded += 1
                consecutive_throttled = 0
        records.append(record)
        if i % 100 == 0:
            print(f"      {i}/{len(manifest)} processed, "
                  f"{downloaded} downloaded, {dl.total_bytes/1e6:.0f} MB so far")

      except Exception as exc:  # noqa: BLE001 - one bad record must not kill the run
          record = {"title": file_title, "local_path": "", "section": rec["section"],
                    "source_pages": rec["source_pages"], "original_url": "",
                    "description_url": "", "width": None, "height": None,
                    "bytes": 0, "mime": "", "license": "", "license_url": "",
                    "description": "", "status": f"error: {exc}"}
          errors += 1
          records.append(record)
      if i % 500 == 0:
          partial_path.write_text(json.dumps(records, ensure_ascii=False),
                                  encoding="utf-8")

    if throttled_break:
        # Mark everything we didn't get to as skipped-throttled so the
        # manifest is complete and a later --resume pass retries them.
        for file_title, rec in ordered[i:]:
            info = infos.get(file_title, {})
            meta = info.get("extmetadata") or {}
            records.append({
                "title": file_title, "local_path": "",
                "section": rec["section"], "source_pages": rec["source_pages"],
                "original_url": info.get("url", ""),
                "description_url": info.get("descriptionurl", ""),
                "width": info.get("width"), "height": info.get("height"),
                "bytes": 0, "mime": info.get("mime", ""),
                "license": strip_html((meta.get("LicenseShortName") or {}).get("value")),
                "license_url": (meta.get("LicenseUrl") or {}).get("value", ""),
                "description": strip_html((meta.get("ImageDescription") or {}).get("value"))[:500],
                "status": "skipped-throttled",
            })
        print(f"      {len(ordered) - i} remaining files marked skipped-throttled")

    # -- Write outputs ---------------------------------------------------------
    records.sort(key=lambda r: (SECTION_RANK.get(r["section"], 9),
                               r["section"], r["title"]))
    (data_dir / "manifest.json").write_text(
        json.dumps(records, indent=2, ensure_ascii=False), encoding="utf-8")
    with open(data_dir / "manifest.csv", "w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=[
            "title", "local_path", "section", "source_pages", "original_url",
            "width", "height", "bytes", "mime", "license", "license_url",
            "description", "status"])
        writer.writeheader()
        for r in records:
            row = {**r, "source_pages": "; ".join(r["source_pages"])}
            writer.writerow({k: row.get(k, "") for k in writer.fieldnames})
    (data_dir / "pages.json").write_text(
        json.dumps(pages, indent=2, ensure_ascii=False), encoding="utf-8")

    downloaded = sum(1 for r in records if r["status"] == "downloaded")
    skipped = sum(1 for r in records if r["status"].startswith("skipped"))
    errors = sum(1 for r in records if r["status"].startswith("error"))
    total_mb = sum(r["bytes"] for r in records) / 1e6
    partial_path.unlink(missing_ok=True)  # run complete; drop the checkpoint
    print("\nDone.")
    print(f"  unique files in manifest : {len(records)}")
    print(f"  downloaded               : {downloaded} ({total_mb:.1f} MB)")
    print(f"  skipped                  : {skipped}")
    print(f"  errors                   : {errors}")
    print(f"  pages visited            : {len(pages)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
