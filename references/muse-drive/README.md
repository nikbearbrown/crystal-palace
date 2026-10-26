# Crystal Palace (1851) — Architectural Research Scrape

A research haul of architectural material on the Crystal Palace — images,
drawings, blueprints, plans — staged for the CSYE 7270 course repo
(`blender/crystal-palace-1851-claude/research/`).

## Headline numbers

| | |
|---|---|
| Total files catalogued | **8,860** (`data/manifest.json` / `data/manifest.csv`) |
| Files downloaded | **1,398** (**2.11 GB**) |
| Skipped (budget cap) | 7,380 — the long tail of first-hop pages, cut by the ~900 MB Wikimedia download budget |
| Skipped (audio/video/PDF) | 56 |
| Skipped (over 45 MB each) | 26 |
| Errors | **0** |
| Pages visited | **398** (seed article + 396 linked articles + Commons categories) |
| Downloaded files with plan/section/elevation/drawing keywords | **529** |

## Where it came from

### Wikimedia pass (MediaWiki API only — no HTML scraping)
- **Seed:** [The Crystal Palace](https://en.wikipedia.org/wiki/The_Crystal_Palace) — all 32 images via `prop=images` + `imageinfo`.
- **First hop:** all 396 namespace-0 articles linked from the seed; every image on each, deduped by Commons file title across pages (all source pages recorded per file).
- **Commons:** `Category:Crystal Palace (building)` (verified non-empty via API before walking; the plausible-looking `Category:Crystal Palace (London)` does not exist), subcategories walked 2 levels deep — 825 files.
- Downloads ordered by architectural value (seed → Commons → linked; keyword-prioritized within each), capped at ~900 MB total for the Wikimedia pass.

### Extra architectural sources (all public domain)
| Source | Folder | What it contributed |
|---|---|---|
| Downes (1852) working drawings — Fox, Henderson & Co. plates (IA `McGillLibrary-rbsc_building-erected-hyde-park_folioNA6750L6D71852-21979`) | `images/downes-1852-working-drawings/` | 209 images (187 pages + **22 foldout plates re-rendered at high res, up to 9000px wide** — the motherlode: ground-floor plan, gallery plans, sections, elevations) |
| Routledge's 1851 Guide "with a plan" (IA `guidetogreatexhi00grea`) | `images/routledge-1851-guide/` | 272 page images |
| Tallis's illustrated history, vols 1 & 4 (IA) | `images/tallis-history-v1/`, `images/tallis-history-v4/` | 232 + 172 plate/page images |
| New York Crystal Palace (IA `newyorkcrystalp00carsa`) — same lineage | `images/new-york-crystal-palace/` | 114 page images |
| V&A O18167 — Paxton's original blotting-paper sketches + acceptance telegram | `images/va-paxton-sketches/` | 3 images |
| architectuul.com/architecture/the-crystal-palace | `images/architectuul-crystal-palace/` | 11 images incl. 1851 floor plan and 1862 Sydenham grounds map |
| Illustrated London News 1850 (low resolution, logged as-is) | `images/iln-1850/` | 9 scans |

See `data/sources.md` for URLs and per-source notes.

## Folder guide

```
.
├── README.md                      this file
├── scraper/
│   ├── scrape_crystal_palace.py   the Wikimedia scraper (re-runnable)
│   ├── scrape_extra_sources.py    the extra-sources scraper (re-runnable)
│   └── merge_manifest.py          merges both manifests into data/manifest.*
├── data/
│   ├── manifest.json / manifest.csv   one record per file: local path, title,
│   │                                  source page(s), original URL, dimensions,
│   │                                  bytes, license, description, status
│   ├── manifest_raw.json          crawl collection checkpoint (for --resume)
│   ├── pages.json                 every page visited + image counts
│   ├── seed-article.txt           plain-text extract of the seed article
│   ├── crystal-palace-facts.md    key architectural facts (dimensions, Paxton,
│   │                              dates, materials, transept, Sydenham move, 1936 fire)
│   ├── sources.md                 extra-source URLs + what each contributed
│   └── extra_manifest.json, plates_extra.json, architectuul_media_urls.json,
│       extra_sources_summary.json  extra-pass working files
├── images/
│   ├── main-article/              32 files from the seed article (56 MB)
│   ├── linked/                    (empty — first-hop files were cut by the budget cap;
│   │                              they are catalogued in the manifest as skipped-budget)
│   ├── commons/                   340 files from Commons categories (827 MB)
│   ├── downes-1852-working-drawings/  209 images (335 MB)
│   ├── routledge-1851-guide/      272 images (306 MB)
│   ├── tallis-history-v1/         232 images (198 MB)
│   ├── tallis-history-v4/         172 images (146 MB)
│   ├── new-york-crystal-palace/   114 images (120 MB)
│   ├── va-paxton-sketches/        3 images (1.4 MB)
│   ├── architectuul-crystal-palace/  11 images (3.4 MB)
│   └── iln-1850/                  9 images (6.1 MB)
└── extra-work/                    Internet Archive JP2 zips (retained so full-res
                                   is recoverable; not part of the repo payload)
```

## Crawl policy

- Seed article + one hop + Commons categories (2 levels). No HTML scraping; MediaWiki API throughout.
- Polite: descriptive User-Agent (`MuseCrystalPalaceResearch/1.0 (CSYE 7270 course research)`), batched API queries (50 titles), 4s between downloads, retries honoring Retry-After, graceful stop on sustained 429 throttling.
- Caps: individual files over 45 MB skipped (logged); audio/video/PDFs logged, not downloaded; ~900 MB total download budget for the Wikimedia pass (extra sources are separate).
- Dedupe by Commons file title; every source page recorded.

## Licenses

Licenses vary per file — see the `license` / `license_url` columns in `data/manifest.csv`. The overwhelming majority of the 1851-era material is **public domain** (1,244 of 1,398 downloaded files: PD, PD-published-1850s/1852, CC0). A minority are Creative Commons (CC BY-SA 2.0/3.0, mostly modern photos). Assume nothing — check the manifest entry for any file you reuse.

## Architectural richness

This is a genuinely architecturally rich haul, not just a photo dump:
- **Working drawings:** the 22 high-res Downes foldout plates (ground-floor plan, gallery plans, transverse/longitudinal sections, elevations, column/girder details) are the single most valuable item — Fox, Henderson & Co.'s actual construction drawings.
- **Design origins:** Paxton's blotting-paper sketch (V&A) — the famous 9-day concept.
- **Plans/maps:** 1851 floor plan + 1862 Sydenham grounds map (Architectuul), Routledge's 1851 guide plan.
- **529 downloaded files** carry plan/section/elevation/drawing keywords in title or description.
- The rest: 1851-era engravings, interior views (nave, transept, courts), Sydenham-era photos, and the medal/commemorative material. The 7,380 skipped-budget files are the noisy first-hop tail (unrelated article illustrations), catalogued but not downloaded.

## Re-running

```bash
# Wikimedia pass (resumable; safe to re-run)
python3 scraper/scrape_crystal_palace.py [--resume] [--pause SECONDS]

# Extra sources (resumable)
python3 scraper/scrape_extra_sources.py [--resume]

# Rebuild the merged manifest after either
python3 scraper/merge_manifest.py
```

`--resume` reloads `data/manifest_raw.json` (skipping the ~20 min collection phase) and skips already-downloaded files; error/throttled records are retried. Checkpoints are written every 500 records.

## Known limitations (honest)

- The egress network throttles sustained `upload.wikimedia.org` downloads (HTTP 429); the scraper backs off and stops gracefully, but a full re-download of the 7,380 skipped-budget files is not feasible from this environment.
- `images/linked/` is empty by design (budget cap) — the files are catalogued in the manifest with their source URLs if someone with better bandwidth wants them.
- ILN 1850 scans are low resolution (noted in manifest).
- The Downes bound volume also contains unrelated bound works (blank pages, a mathematics section); only the wide foldout scans (width >6000px in the JP2 headers) were treated as plates.
