# Sources

Every source crawled for this research pack, what it contributed, and where it
came from. All pre-1929 published material below is public domain; see the
per-file `license` column in `data/manifest.csv` for the exact license of each
image (Commons extmetadata where available).

## Wikimedia (via MediaWiki API)
- **Seed:** https://en.wikipedia.org/wiki/The_Crystal_Palace — every image on
  the article → `images/main-article/`. Plain-text extract in `data/seed-article.txt`.
- **First hop:** all 396 namespace-0 articles the seed links to; every image on
  each → `images/linked/<article-slug>/`. Deduped by file title across pages;
  the manifest records every source page for each file. Audio/video/PDF skipped
  (logged as `skipped-media`); files over 45 MB skipped (logged as
  `skipped-too-large`); downloads stop at ~900 MB total (rest logged as
  `skipped-budget`).
- **Commons:** `Category:Crystal Palace (building)` (verified non-empty via the
  API before walking), subcategories 2 levels deep — includes "Crystal Palace
  in Hyde Park", "Crystal Palace in Sydenham", "Crystal Palace in art",
  "Crystal Palace Museum" — → `images/commons/`.

## Extra architectural sources

### downes-1852-working-drawings → `images/downes-1852-working-drawings/`
- https://archive.org/details/McGillLibrary-rbsc_building-erected-hyde-park_folioNA6750L6D71852-21979
- Charles Downes' 1852 folio of Fox, Henderson & Co.'s working drawings for the
  Hyde Park building — sections, elevations, plans, details. The bound volume's
  JP2 zip (187 scans) was converted page-by-page to JPEG (q88, ≤3000 px);
  the 22 foldout plates were additionally converted at high resolution
  (q92, ≤9000 px, `*_plate-NN.jpg`) — includes Plate I "Plan of Ground Floor"
  and Plate II "Plan of Galleries".
- License: public domain (published 1852).

### va-paxton-sketches → `images/va-paxton-sketches/`
- https://collections.vam.ac.uk/item/O18167/the-great-exhibition-building-architectural-sketch-paxton-joseph-sir/
- Joseph Paxton's original blotting-paper concept sketches (side elevation and
  cross-section) plus the acceptance telegram, fetched via the V&A IIIF API.
- License: underlying work public domain (Paxton, 1850); images via V&A IIIF.

### architectuul-crystal-palace → `images/architectuul-crystal-palace/`
- https://architectuul.com/architecture/the-crystal-palace
- 11 images (1312 px) from the Architectuul article, including the 1851 floor
  plan and the 1862 Sydenham grounds map set. (The page lazy-loads its
  gallery; the first pass captured only blur placeholders, which were
  discarded and re-fetched at full gallery resolution.)
- License: as published on the article page; see manifest.

### routledge-1851-guide → `images/routledge-1851-guide/`
- https://archive.org/details/guidetogreatexhi00grea
- Routledge's 1851 *Guide to the Great Exhibition* "with a plan" — full page
  scans converted from the IA JP2 zip (JPEG q88, ≤3000 px).
- License: public domain (published 1851).

### tallis-history-v1 / tallis-history-v4 → `images/tallis-history-v1/`, `images/tallis-history-v4/`
- https://archive.org/details/tallisshistoryde01tall
- https://archive.org/details/tallisshistoryde04tall
- Tallis's illustrated *History and description of the Crystal Palace*,
  vols 1 and 4 — plates and text pages from the IA JP2 zips.
- License: public domain (published 1850s).

### new-york-crystal-palace → `images/new-york-crystal-palace/`
- https://archive.org/details/newyorkcrystalp00carsa
- *New York Crystal Palace: illustrated description of the building* — the
  American Crystal Palace of 1853, same architectural lineage (Paxton's
  influence; built for the Exhibition of the Industry of All Nations).
- License: public domain (published 1850s).

### iln-1850 → `images/iln-1850/`
- https://iln.org.uk/iln_years/year/1850greatex.html
- Scans from the Illustrated London News Great Exhibition coverage (1850).
  Note: source images are low resolution; recorded as-is in the manifest.
- License: public domain (published 1850).

## How to re-run
- Wikimedia crawl: `python3 scraper/scrape_crystal_palace.py`
  (polite: descriptive UA, 50-title batches, Wikimedia `maxlag`, 2 s between
  downloads, 429/5xx backoff; skips files >45 MB; ~900 MB download budget).
- Extra sources: `python3 scraper/scrape_extra_sources.py`
  (`--only <slug>` to re-run one source).
- Merge manifests: `python3 scraper/merge_manifest.py`.
