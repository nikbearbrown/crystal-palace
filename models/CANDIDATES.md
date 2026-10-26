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

| 7 | HP glazing + sash panel (SCENE-BUILD-PLAN Wave 1.1) | `references/downes-1852/source-scans/plates/` plates XII–XIV, XVIII; `references/downes-1852/crystal-palace-1851/CONTROL-DIMENSIONS.md` | High — dimensioned plates | **Built** — shipped on main by the parallel Muse stream (156 tris); this builder's duplicate staging was not pushed |
| 8 | HP open-boarded floor section (SCENE-BUILD-PLAN Wave 1.2) | `references/muse-round2/images/S25-catalogue-1851-introduction-p62.jpg` + `p63.jpg` (branch muse-round2; Paxton's own account: boards 1½ in thick, ½ in gaps; joists 7 × 2½ in; sleepers 13 × 3¼ in at 8 ft) | High — primary text evidence | **Built** — `models/hp-floor-boards/` on main (288 tris; boards/gaps/joists/sleepers all Paxton's printed figures, board width + joist spacing inferred and labelled) |

| 9 | HP gallery stair + rail section (SCENE-BUILD-PLAN Wave 1.3) | `references/downes-1852/source-scans/plates/` plates II, XV–XVII | Medium-high — plates + course-model dimensions as starting point only | **Built** — `models/hp-gallery-stair/` on main (6,596 tris; landing at exactly half gallery height, rail height printed on Plate XVII Fig. 7, lattice pitch counted on Plate XV; well-hole edges unmodelled, evidence-gated) |
| 10 | HP louvre + canvas blind unit (SCENE-BUILD-PLAN Wave 1.4) | `references/downes-1852/source-scans/plates/` plate XXVII | Medium-high — mechanism plate | **Taken — Muse (round-2 builder), building now** → `models/hp-louvre-and-blind/` |

| 11 | HP roof furrow bay — full 24 ft bay: both slopes, ridge piece, Paxton gutters (companion to row 7's single row) | `references/downes-1852/source-scans/plates/plate-012.jpg` (Plate XII Figs. 1/3/10; bar chain sums to exactly 288 in); plates XIII, XIV, XVIII consulted | High — printed chain + sections | **Built** — `models/hp-roof-furrow-bay/` on main (2,388 tris) |

| 12 | Great elm tree (SCENE-BUILD-PLAN Wave 1.5) | Transept interior views in `references/muse-drive/images/commons/` and `main-article/` | Medium — procedural; ships labelled generic, never as a named tree | **Built** — `models/hp-great-elm/` on main (45,712 tris instanced; height 22.0 m measured from the Talbot 1851 transept photograph against the 102 ft 2 in vault crown; generic, stylised foliage — a distance/background tree, not a hero asset) |
| 13 | Packing crate + exhibition display case (SCENE-BUILD-PLAN Wave 1.6) | Dickinson plates in `references/muse-drive/images/commons/` (e.g. plate XXIV, CC0) | Medium — sizes guessed, not dimensioned; NOTES must say so | **Built** — `models/hp-crate-and-display-case/` on main (2,278 tris; case form read from Dickinson plate XXIV, all sizes guessed and labelled; crate is generic period construction — no crate image exists in the collection) |

| 14 | Sydenham High Level subway vault bay (SCENE-BUILD-PLAN Wave 3.9) | Round-2 S87 material (branch muse-round2): OS 25-inch plan 1895; ILN 1865 station engraving; conservation photos 2016/2023/2025 of the vaults themselves | High for the vault geometry (surviving fabric, photographed during restoration); station-to-entry layout still unplotted — bay only, no route claims | **Taken — Muse (round-2 builder), building now** → `models/sy-subway-vault-bay/` |
| 15 | Sydenham Egyptian Court column pair (SCENE-BUILD-PLAN Wave 3.10) | Court plan 0226 + dated court views in `references/muse-drive/images/`; 1856 guide plan 0205 for position only | Medium-high — views + plan; polychromy partly unverified | **Taken — Muse (round-2 builder), building now** → `models/sy-egyptian-column-pair/` |

Notes for other builders:
- Do NOT use `references/image-leads/contact-sheet.jpg` as primary evidence
  (provenance not established, mixed buildings/periods).
- Do NOT use `references/walker-research-notes/` as fact (explicitly
  unverified ideas).
- Beware the REVIEW.md traps: filename years are not depicted years
  (e.g. `Kristallpalast_Sydenham_1851_aussen.png` depicts Sydenham);
  the French 1849 plan, Kroll's Wintergarten, committee and Turner
  proposals are NOT the Palace.
