# scan-fig56-cannibal-islanders — Muse version

**This is the Muse version** of this model (ships as `scan-fig56-cannibal-islanders-muse`).

## Source and historical context
- Figure 56, "Cannibal Islanders" — a coloured caricature of an exhibition refreshment-room
  scene, presented in the source book explicitly as an example of **racialized stereotyping
  of foreign visitors** at the Great Exhibition (catalogue scan IMG_6439).
- One view only.

## Treatment — read this first
The source is a racialized 1851 satire whose humour depends on caricatured features.
**The model deliberately does NOT reproduce the caricature.** It preserves only the
scene's composition and setting: the visitors are rendered as dignified, neutral,
stylised figures in plain period dress, with simple featureless heads — the same house
figure style used for the British visitors in the other Punch models in this batch.
What is preserved is the composition (a party at a laid table, attendants serving),
not the caricature.

## Subject modelled
- A round refreshment table with a cloth to the floor, laid with: a joint of meat on an
  oval platter (centrepiece), a ewer, a wine bottle, six place settings (plates, glasses,
  bread rolls).
- Six diners seated around the table on simple chairs, in varied plain dress and caps.
- Two attendants standing behind the table in dark jackets with white shirtfronts; one
  carries a tray with a domed cover (cloche), the other has a napkin over his arm.
- Setting hints: a plain rear wall panel and a serving sideboard with plates and an ewer
  at the left, as in the print's refreshment-room interior.

## Scale
- **Estimated**, set from the figures (adults ~1.68–1.76 m). Vignette footprint
  6.4 × 4.8 m; table Ø ~2.1 m including cloth.

## Assumptions and interpretation
- Seating arrangement follows the print's grouping (six diners, two standing attendants);
  the far side of the room and all backs are interpretation.
- The print's tableware is denser than modelled; the principal pieces are included.
- Dress colours are muted period tones; the source is hand-coloured but its palette is
  part of the caricature staging and was not copied literally.

## Technical
- Blender 4.5.3, metres, origin at base centre, scale applied.
- 13,832 triangles.
- Files: `.blend`, `.glb` (verified glTF), `preview.png` (Cycles, 48 samples + denoise,
  frontal view comparable to the print), re-runnable `build_scan_fig56.py` with its
  in-folder `vignette_common.py` helper.
- QC note: the seated-figure torso in the shared helper was twice adjusted after preview
  audits (first a neck gap, then heads swallowed by the torso cone) — final preview shows
  heads seated correctly on all six diners.
- QC fix round (parent audit): the six diners still read as straight pillars on chairs,
  so `seated_person` in the in-folder helper was rebuilt with a true seated construction —
  real sitting height (~72% of the seat-to-standing span), a lap/skirt mass resting on the
  seat and draping over the chair's front edge, a horizontal thigh/lap cap, a torso rising
  from the hips with a slight forward lean, shoulders, and arms resting forward over the
  lap. The two attendants were given arms in the standard standing form (one raised
  forward carrying the tray + cloche, now seated on his hand; shirtfronts shortened to
  chest panels). Table, settings, sideboard, chairs and room unchanged. Triangles
  10,604 → 13,832; regenerated preview verified figure by figure — all six diners now
  read as seated people.

## Manual-review items
- A parallel builder's separate package for this entry exists at
  `scan-fig56-cannibal-islanders-caricature/` — the parent should ship only one.
- The cloche tray is partly occluded from the preview angle; check in the .blend before
  close-up use.
- Sensitivity review recommended before any public use, given the source.
