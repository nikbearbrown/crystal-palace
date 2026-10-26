# Prompt for Muse — build props for the Crystal Palace from the reference images

You are Muse. This repo is the Crystal Palace project. You already collected the reference images in `references/muse-drive/images/` (1,393 files; `references/muse-drive/data/manifest.csv` lists each one's source URL, licence and description). Your job now is to mine those images for **individual objects**, model them in 3D, and add the models back to this repo.

## 1. Find candidates
Look through the reference images (and `references/downes-1852/`, `references/image-leads/`) for self-contained objects that appear in or around the Palace, for example:
- statues and sculpture groups (Greek Slave, Una and the Lion, the Three Graces, Court statuary)
- trees (the great elms enclosed in the transept), planters, urns, vases
- fountains, including the Osler Crystal Fountain
- furniture, benches, display cases, lamps, railings, ironwork details, columns and capitals
- exhibits or garden features visible in the stereographs and ILN plates

Write `models/CANDIDATES.md`: one row per candidate with the object name, the 1–5 best reference image paths (relative to repo root), the view each shows (front/side/detail), and a feasibility note. Prefer objects shown from several angles. Rank them and build from the top down.

## 2. Model each object
For every object you take on, create `models/<slug>/` containing:
- `<slug>.blend` (Blender 4.2+ compatible, apply scale, real-world units in metres, origin at the base centre)
- `<slug>.glb` export
- `renders/` with at least a front, side and 3/4 view (neutral grey backdrop, same lighting each time)
- `refs/` listing (or copying, if small) the reference images used
- `NOTES.md`: sources used (paths and manifest licences), real-world dimensions and where you got them, what you **measured or saw** versus what you **guessed**, and known inaccuracies

Rules:
- Model only what the images show. Where an image does not show a side, say so in `NOTES.md` and mark that geometry as inferred; do not present guesses as fact.
- Keep poly counts sensible (props under ~50k triangles; use instancing-friendly meshes for trees).
- No files over 90 MB (GitHub rejects 100 MB). Do not add `.zip` files.
- Do not edit or delete anything outside `models/`. The existing Blender scenes in `blender-deliverables/` and `course-models/` are not yours to change.
- Do not copy copyrighted text or images from outside the repo; use only what is already in `references/`.

## 3. Add back to the repo
Update `models/README.md` with a table (name, thumbnail, triangle count, accuracy note). Commit **only** your paths:

```bash
git add -- models/
git commit -m "models: add <names>" -- models/
git push
```

Never `git add .` and never rewrite history. If a push is rejected, `git pull --rebase` is fine only if nothing outside `models/` changed locally; otherwise stop and report.

## 4. Report
Finish with a short report: candidates found, models built, which ones are weakest and why, and anything in the references you could not use.
