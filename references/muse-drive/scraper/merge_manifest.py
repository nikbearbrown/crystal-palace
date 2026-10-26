#!/usr/bin/env python3
"""Merge the Wikimedia crawl manifest with the extra-sources manifest.

Produces the final data/manifest.json and data/manifest.csv.

Steps:
  1. Load data/manifest.json (Wikimedia crawl).
  2. Load data/extra_manifest.json (Internet Archive books, V&A, article
     scrapes) + data/plates_extra.json (high-res Downes foldout plates).
  3. Rebuild the architectuul-crystal-palace records from the real 1312px
     downloads (the first scrape_page_images pass captured only blur
     placeholders, which were deleted).
  4. Dedupe by title, sort by (section rank, section, title).

Usage: python3 merge_manifest.py [--root DIR]
"""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

from PIL import Image

SECTION_RANK = {
    "main-article": 0,
    "commons": 1,
    "linked": 2,
    "downes-1852-working-drawings": 3,
    "va-paxton-sketches": 4,
    "architectuul-crystal-palace": 5,
    "routledge-1851-guide": 6,
    "tallis-history-v1": 7,
    "tallis-history-v4": 8,
    "new-york-crystal-palace": 9,
    "iln-1850": 10,
}

CSV_FIELDS = ["title", "local_path", "section", "source_pages", "original_url",
              "width", "height", "bytes", "mime", "license", "license_url",
              "description", "status"]


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--root", default=str(Path(__file__).resolve().parents[1]))
    root = Path(ap.parse_args().root)
    data = root / "data"

    records: dict[str, dict] = {}
    for name in ("manifest.json", "extra_manifest.json", "plates_extra.json"):
        path = data / name
        if path.exists():
            for rec in json.loads(path.read_text(encoding="utf-8")):
                records[rec["title"]] = rec
    print(f"loaded {len(records)} records from crawl + extras")

    # Rebuild architectuul records from the real downloads.
    slug = "architectuul-crystal-palace"
    records = {t: r for t, r in records.items()
               if not t.startswith(f"[{slug}]")}
    media_urls = json.loads(
        (data / "architectuul_media_urls.json").read_text(encoding="utf-8"))
    page_url = "https://architectuul.com/architecture/the-crystal-palace"
    n = 0
    for fname in sorted((root / "images" / slug).glob("*.jpg")):
        w, h = Image.open(fname).size
        title = f"[{slug}] {fname.name}"
        records[title] = {
            "title": title,
            "local_path": str(fname.relative_to(root)),
            "section": slug,
            "source_pages": [page_url],
            "original_url": media_urls.get(fname.name, ""),
            "description_url": page_url,
            "width": w, "height": h, "bytes": fname.stat().st_size,
            "mime": "image/jpeg",
            "license": "Images embedded in the Architectuul article "
                       "(license per page)",
            "license_url": "",
            "description": "Crystal Palace article image incl. 1851 floor "
                           "plan and 1862 Sydenham grounds map set.",
            "status": "downloaded",
        }
        n += 1
    print(f"rebuilt {n} architectuul records")

    merged = sorted(records.values(),
                    key=lambda r: (SECTION_RANK.get(r["section"], 99),
                                   r["section"], r["title"]))
    (data / "manifest.json").write_text(
        json.dumps(merged, indent=2, ensure_ascii=False), encoding="utf-8")
    with open(data / "manifest.csv", "w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=CSV_FIELDS)
        writer.writeheader()
        for r in merged:
            row = {**r, "source_pages": "; ".join(r.get("source_pages", []))}
            writer.writerow({k: row.get(k, "") for k in CSV_FIELDS})
    print(f"wrote {len(merged)} merged records")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
