#!/usr/bin/env python3
"""Extra architectural sources for the Crystal Palace research pack.

Supplements the Wikimedia crawl (scrape_crystal_palace.py) with high-value
public-domain material that Commons does not carry at full resolution:

  downes-1852-working-drawings  Internet Archive: Downes' 1852 folio of
                                Fox, Henderson & Co. working drawings
                                (28 plates) — JP2 zip -> JPEG plates
  routledge-1851-guide          Internet Archive: Routledge's 1851 Guide to
                                the exhibition ("with a plan") — all pages
  tallis-history-v1 / v4        Internet Archive: Tallis's illustrated
                                history of the exhibition, vols 1 & 4
  new-york-crystal-palace       Internet Archive: NY Crystal Palace
                                (same lineage) — best effort
  va-paxton-sketches            V&A item O18167: Paxton's original
                                blotting-paper sketches via IIIF
  architectuul-crystal-palace   architectuul.com article: 11 images incl.
                                the 1851 floor plan and 1862 Sydenham map
  iln-1850                      Illustrated London News 1850 Great
                                Exhibition pages — best effort

Writes:
  images/<slug>/                 downloaded/converted images
  data/extra_manifest.json      manifest records (same schema as the main
                                crawler; merge with merge_manifest.py)
  data/extra_sources_summary.json  per-source attempt log for sources.md

Usage: python3 scrape_extra_sources.py [--root DIR] [--only slug]
"""

from __future__ import annotations

import argparse
import io
import json
import re
import sys
import time
import zipfile
from pathlib import Path
from urllib.parse import urljoin, urlparse

import requests
from PIL import Image

USER_AGENT = "MuseCrystalPalaceResearch/1.0 (CSYE 7270 course research)"
SESSION = requests.Session()
SESSION.headers.update({"User-Agent": USER_AGENT})

# Conversion policy: book scans become JPEGs; the Downes folio (the
# motherlode) keeps higher quality/resolution. Per-book items stop
# converting once their JPEG output passes OUT_CAP_MB.
BOOK_Q, BOOK_MAXW = 88, 3000
FOLIO_Q, FOLIO_MAXW = 92, 4500
OUT_CAP_MB = 500


def log(msg: str) -> None:
    print(f"[{time.strftime('%H:%M:%S')}] {msg}", flush=True)


def http_get(url: str, timeout: int = 90, retries: int = 2) -> requests.Response:
    last = None
    for i in range(retries + 1):
        try:
            r = SESSION.get(url, timeout=timeout)
            r.raise_for_status()
            return r
        except Exception as exc:  # noqa: BLE001
            last = exc
            time.sleep(2 * (i + 1))
    raise RuntimeError(f"GET failed: {url}: {last}")


def download(url: str, dest: Path, skip_if_exists: bool = True) -> int:
    if skip_if_exists and dest.exists() and dest.stat().st_size > 0:
        log(f"    cached {dest.name} ({dest.stat().st_size/1e6:.1f} MB)")
        return dest.stat().st_size
    dest.parent.mkdir(parents=True, exist_ok=True)
    tmp = dest.with_suffix(dest.suffix + ".part")
    log(f"    downloading {urlparse(url).path.rsplit('/', 1)[-1]} ...")
    with SESSION.get(url, stream=True, timeout=300) as r:
        r.raise_for_status()
        with open(tmp, "wb") as fh:
            for chunk in r.iter_content(chunk_size=1 << 20):
                fh.write(chunk)
    tmp.replace(dest)
    return dest.stat().st_size


# ---------------------------------------------------------------- IA books

def ia_metadata(identifier: str) -> dict:
    r = http_get(f"https://archive.org/metadata/{identifier}", timeout=120)
    return r.json()


def ia_jp2_pages(root: Path, identifier: str, slug: str, folio: bool = False,
                 out_cap_mb: float = OUT_CAP_MB) -> tuple[int, list[dict], dict]:
    """Download an IA item's JP2 zip and convert every page to JPEG.

    Returns (converted_count, manifest_records, summary).
    """
    summary: dict = {"slug": slug, "item": identifier,
                     "item_url": f"https://archive.org/details/{identifier}"}
    meta = ia_metadata(identifier)
    meta_info = meta.get("metadata", {}) or {}
    summary["ia_title"] = meta_info.get("title")
    summary["ia_creator"] = meta_info.get("creator")
    files = meta.get("files", []) or []
    zips = [f for f in files if f.get("name", "").endswith("_jp2.zip")]
    if not zips:
        summary["status"] = "no jp2 zip found"
        return 0, [], summary
    zname = sorted(zips, key=lambda f: f.get("size", 0), reverse=True)[0]["name"]
    work = root / "extra-work" / identifier
    zpath = work / zname
    download(f"https://archive.org/download/{identifier}/{zname}", zpath)
    q, maxw = (FOLIO_Q, FOLIO_MAXW) if folio else (BOOK_Q, BOOK_MAXW)
    outdir = root / "images" / slug
    outdir.mkdir(parents=True, exist_ok=True)
    records, converted = [], 0
    out_bytes = 0
    with zipfile.ZipFile(zpath) as zf:
        names = sorted(n for n in zf.namelist() if n.lower().endswith(".jp2"))
        summary["jp2_pages"] = len(names)
        for idx, name in enumerate(names):
            if out_bytes > out_cap_mb * 1e6:
                summary["capped"] = f"stopped after {converted} pages " \
                                    f"(>{out_cap_mb} MB JPEG output)"
                break
            outname = f"{slug}_p{idx:04d}.jpg"
            dest = outdir / outname
            if not dest.exists():
                try:
                    with zf.open(name) as fh:
                        im = Image.open(io.BytesIO(fh.read()))
                        im.load()
                    im = im.convert("RGB")
                    if im.width > maxw:
                        im = im.resize((maxw, int(im.height * maxw / im.width)),
                                       Image.LANCZOS)
                    im.save(dest, "JPEG", quality=q, optimize=True)
                except Exception as exc:  # noqa: BLE001
                    summary.setdefault("page_errors", []).append(f"{name}: {exc}")
                    continue
            w, h = Image.open(dest).size
            nbytes = dest.stat().st_size
            out_bytes += nbytes
            converted += 1
            records.append({
                "title": f"[{slug}] {outname}",
                "local_path": str(dest.relative_to(root)),
                "section": slug,
                "source_pages": [summary["item_url"]],
                "original_url": f"https://archive.org/download/{identifier}/{zname}",
                "description_url": summary["item_url"],
                "width": w, "height": h, "bytes": nbytes, "mime": "image/jpeg",
                "license": "Public domain (published 1850s)",
                "license_url": "",
                "description": f"Page scan from {summary['ia_title']} "
                               f"({summary['ia_creator']}); converted from "
                               f"Internet Archive JP2 master.",
                "status": "downloaded",
            })
    summary["status"] = "ok"
    summary["converted_pages"] = converted
    summary["output_mb"] = round(out_bytes / 1e6, 1)
    log(f"    {slug}: {converted} pages -> {summary['output_mb']} MB JPEG")
    return converted, records, summary


# ---------------------------------------------------------------- V&A IIIF

def va_paxton(root: Path) -> tuple[int, list[dict], dict]:
    slug = "va-paxton-sketches"
    item_url = ("https://collections.vam.ac.uk/item/O18167/"
                "the-great-exhibition-building-architectural-sketch-"
                "paxton-joseph-sir/")
    summary: dict = {"slug": slug, "item_url": item_url}
    manifest_url = None
    for probe in ["https://iiif.vam.ac.uk/collections/O18167/manifest.json"]:
        try:
            http_get(probe, timeout=60)
            manifest_url = probe
            break
        except Exception:  # noqa: BLE001
            continue
    if manifest_url is None:
        try:
            page = http_get(item_url, timeout=60).text
            m = re.search(r'https?://[^\s"\']*manifest\.json[^\s"\']*', page)
            if m:
                manifest_url = m.group(0)
        except Exception as exc:  # noqa: BLE001
            summary["status"] = f"item page unreachable: {exc}"
            return 0, [], summary
    if manifest_url is None:
        summary["status"] = "no IIIF manifest found"
        return 0, [], summary
    man = http_get(manifest_url, timeout=60).json()
    outdir = root / "images" / slug
    outdir.mkdir(parents=True, exist_ok=True)
    records, n = [], 0
    seqs = man.get("sequences", man.get("items", []))
    canvases = []
    for seq in (seqs if isinstance(seqs, list) else [seqs]):
        canvases.extend(seq.get("canvases", seq.get("items", [])))
    for ci, canvas in enumerate(canvases):
        images = canvas.get("images", canvas.get("items", []))
        for img in images:
            svc = img.get("resource", {}).get("service", {}) or {}
            base = svc.get("@id") or img.get("resource", {}).get("@id")
            if not base:
                continue
            img_url = base.rstrip("/") + "/full/!2000,2000/0/default.jpg"
            dest = outdir / f"{slug}_{ci:02d}.jpg"
            try:
                download(img_url, dest)
            except Exception as exc:  # noqa: BLE001
                summary.setdefault("errors", []).append(f"{img_url}: {exc}")
                continue
            w, h = Image.open(dest).size
            n += 1
            records.append({
                "title": f"[{slug}] {dest.name}",
                "local_path": str(dest.relative_to(root)),
                "section": slug,
                "source_pages": [item_url],
                "original_url": img_url,
                "description_url": item_url,
                "width": w, "height": h, "bytes": dest.stat().st_size,
                "mime": "image/jpeg",
                "license": "Underlying work public domain (Paxton, 1850); "
                           "image via V&A IIIF",
                "license_url": "", "description": "Paxton's original "
                "blotting-paper sketches of the Great Exhibition building.",
                "status": "downloaded",
            })
    summary["status"] = "ok" if n else "manifest parsed but no images"
    summary["images"] = n
    log(f"    {slug}: {n} images via IIIF")
    return n, records, summary


# ---------------------------------------------------------------- page scrapes

IMG_RE = re.compile(r'<img[^>]+src=["\']([^"\']+)["\'][^>]*>', re.I)
ALT_RE = re.compile(r'alt=["\']([^"\']*)["\']', re.I)


def scrape_page_images(root: Path, slug: str, page_url: str, desc: str,
                       allow_hosts: tuple[str, ...] = ()) -> tuple[int, list[dict], dict]:
    summary: dict = {"slug": slug, "item_url": page_url}
    try:
        html_text = http_get(page_url, timeout=60).text
    except Exception as exc:  # noqa: BLE001
        summary["status"] = f"page unreachable: {exc}"
        return 0, [], summary
    outdir = root / "images" / slug
    outdir.mkdir(parents=True, exist_ok=True)
    records, n = [], 0
    seen: set[str] = set()
    for tag in IMG_RE.finditer(html_text):
        src = tag.group(1)
        if src in seen or src.startswith("data:"):
            continue
        seen.add(src)
        url = urljoin(page_url, src)
        host = urlparse(url).netloc
        if allow_hosts and not any(host.endswith(h) for h in allow_hosts):
            continue
        if not re.search(r"\.(jpe?g|png|webp|gif)(\?|$)", url, re.I):
            continue
        alt = (ALT_RE.search(tag.group(0)) or [None, ""])[1]
        dest = outdir / f"{slug}_{n:02d}{Path(urlparse(url).path).suffix or '.jpg'}"
        try:
            download(url, dest)
            w, h = Image.open(dest).size
            if dest.stat().st_size < 20_000 or w < 100 or h < 100:
                # Tracking pixel / blur placeholder, not a real image.
                summary.setdefault("skipped_placeholders", []).append(url)
                dest.unlink(missing_ok=True)
                continue
        except Exception as exc:  # noqa: BLE001
            summary.setdefault("errors", []).append(f"{url}: {exc}")
            continue
        n += 1
        time.sleep(0.3)
        records.append({
            "title": f"[{slug}] {dest.name}",
            "local_path": str(dest.relative_to(root)),
            "section": slug,
            "source_pages": [page_url],
            "original_url": url,
            "description_url": page_url,
            "width": w, "height": h, "bytes": dest.stat().st_size,
            "mime": "image/jpeg",
            "license": desc,
            "license_url": "",
            "description": (alt or "image from " + slug)[:300],
            "status": "downloaded",
        })
    summary["status"] = "ok"
    summary["images"] = n
    log(f"    {slug}: {n} images")
    return n, records, summary


# ---------------------------------------------------------------- registry

IA_BOOKS = [
    ("downes-1852-working-drawings",
     "McGillLibrary-rbsc_building-erected-hyde-park_folioNA6750L6D71852-21979",
     True),
    ("routledge-1851-guide", "guidetogreatexhi00grea", False),
    ("tallis-history-v1", "tallisshistoryde01tall", False),
    ("tallis-history-v4", "tallisshistoryde04tall", False),
    ("new-york-crystal-palace", "newyorkcrystalp00carsa", False),
]


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--root", default=str(Path(__file__).resolve().parents[1]))
    ap.add_argument("--only", default=None, help="run only this source slug")
    args = ap.parse_args()
    root = Path(args.root)
    (root / "data").mkdir(parents=True, exist_ok=True)

    all_records: list[dict] = []
    summaries: list[dict] = []

    def run(slug: str, fn, *a, **k):
        if args.only and slug != args.only:
            return
        log(f"== {slug}")
        try:
            n, records, summary = fn(*a, **k)
            all_records.extend(records)
            summaries.append(summary)
            log(f"   -> {n} images")
        except Exception as exc:  # noqa: BLE001
            summaries.append({"slug": slug, "status": f"failed: {exc}"})
            log(f"   !! failed: {exc}")

    for slug, ident, folio in IA_BOOKS:
        run(slug, ia_jp2_pages, root, ident, slug, folio)
    run("va-paxton-sketches", va_paxton, root)
    run("architectuul-crystal-palace", scrape_page_images, root,
        "architectuul-crystal-palace",
        "https://architectuul.com/architecture/the-crystal-palace",
        "Images embedded in the Architectuul article (license per page)")
    run("iln-1850", scrape_page_images, root, "iln-1850",
        "https://iln.org.uk/iln_years/year/1850greatex.html",
        "Illustrated London News scans (1850, public domain)")

    (root / "data" / "extra_manifest.json").write_text(
        json.dumps(all_records, indent=2, ensure_ascii=False), encoding="utf-8")
    (root / "data" / "extra_sources_summary.json").write_text(
        json.dumps(summaries, indent=2, ensure_ascii=False), encoding="utf-8")
    total = sum(r["bytes"] for r in all_records)
    log(f"DONE: {len(all_records)} images, {total/1e6:.1f} MB total")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
