# Model candidates — Crystal Palace props (Muse)

Ranked by provenance × buildability. "Taken" means a builder has claimed it;
other builders: pick from the open rows, don't duplicate a taken row.
All reference paths are relative to the repo root. Hyde Park 1851 and
Sydenham 1854+ are different buildings — never blend their evidence
(see `references/muse-drive/review/REVIEW.md`, "Corrections that matter").

| # | Object | Best references (view) | Feasibility | Status |
|---|---|---|---|---|
| 1 | Hyde Park tier-1 iron column + girder stub | `references/downes-1852/source-scans/plates/plate-008.jpg` (Plate VIII, Details of columns: Fig. 3/4/5 full columns, Fig. 12 girder connection, Fig. 13 flange plan); `references/downes-1852/crystal-palace-1851/CONTROL-DIMENSIONS.md` (D06 24 ft bay, D10 3 ft girder, D11 22 ft 2 in girder top) | High — fully dimensioned on the plate: 19 ft 2 in floor to girder bottom, 3 ft girder, 8 in bore, 2 ft 0 in × 1 ft 6 in base foot | **Taken — Muse, building now** → `models/hyde-park-column-tier1/` |
| 2 | Osler Crystal Fountain (Hyde Park transept centrepiece) | `references/muse-drive/images/commons/Catalogue_of_the_great_exhibition_Wellcome_L0022578.jpg` (transept view, CC BY 4.0); `references/muse-drive/images/commons/The_Transept_(BM_1917,1208.2277).jpg` and `..._1).jpg` (transept with fountain, public domain); `references/muse-drive/images/commons/Great_Exhibition_fountain_1851.jpg` (public domain) | Medium — several views, but no dedicated dimensioned detail set; tier/basin structure would need inference | Open |
| 3 | Cast-iron garden urn / planter (Sydenham grounds) | To be identified in `references/muse-drive/images/tallis-history-v1/` and `tallis-history-v4/` (decorative objects) — no single Palace urn isolated yet | Medium — lathe-turned form, but needs a specific Palace reference first | Open |
| 4 | 1851 exhibition display case / vitrine | Dickinson plates in `references/muse-drive/images/commons/` (e.g. plate XXIV, cases of goods, CC0) | Medium — box + glass + frame is easy geometry; sizes would be guessed, not dimensioned | Open |
| 5 | Great elm tree (transept elms, Hyde Park) | Transept interior views in `references/muse-drive/images/commons/` and `main-article/` | Medium — procedural, instancing-friendly, but generic: cannot capture a specific elm from these views | Open |
| 6 | Greek Slave / Una and the Lion / Three Graces (statuary) | `references/muse-drive/images/commons/-Stereograph,_Crystal_Palace,_John_Bell's_Una_and_the_Lion-_MET_DP700246.jpg` and `...247.jpg` (CC0); `..._The_Three_Graces-_MET_DP323102.jpg` (CC0) | Low for procedural modelling — figurative sculpture needs sculpting, not primitives | Open — needs a sculptor |

Notes for other builders:
- Do NOT use `references/image-leads/contact-sheet.jpg` as primary evidence
  (provenance not established, mixed buildings/periods).
- Do NOT use `references/walker-research-notes/` as fact (explicitly
  unverified ideas).
- Beware the REVIEW.md traps: filename years are not depicted years
  (e.g. `Kristallpalast_Sydenham_1851_aussen.png` depicts Sydenham);
  the French 1849 plan, Kroll's Wintergarten, committee and Turner
  proposals are NOT the Palace.
