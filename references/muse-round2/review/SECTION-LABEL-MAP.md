# Section-label map: branch manifest vs my manifest (stage 20)

Branch section labels are kept verbatim in MERGED-MANIFEST-V1.csv; this map records equivalences only where they are exact, and lists everything else as unmapped rather than forcing a mapping. No section value was remapped in v1 itself.

My manifest section labels (21): B-plans, S03, S04, S05, S13, S19, S25, S34, S37, S41, S44, S45, S51, S52, S53, S55, S57, S67, S70, S83, S87

Branch manifest section labels (37): B1-guide1856, B2-iln1854, B2-phillips1854, B5-heights, PLAN 1856 guide plate, PLAN court plan 1854, PLAN heights evidence, PLAN railway arrival, S03, S04, S05, S13, S15, S19, S25, S34, S37, S41, S44, S45, S45-47, S46, S47, S51, S52, S53, S55, S56-S66 route plan, S57, S62 grounds, S66 north transept / fire context, S66 post-fire plan, S67, S70, S83, S87, S89

## Identical labels (20): mapped 1:1

- `S03` = my `S03`
- `S04` = my `S04`
- `S05` = my `S05`
- `S13` = my `S13`
- `S19` = my `S19`
- `S25` = my `S25`
- `S34` = my `S34`
- `S37` = my `S37`
- `S41` = my `S41`
- `S44` = my `S44`
- `S45` = my `S45`
- `S51` = my `S51`
- `S52` = my `S52`
- `S53` = my `S53`
- `S55` = my `S55`
- `S57` = my `S57`
- `S67` = my `S67`
- `S70` = my `S70`
- `S83` = my `S83`
- `S87` = my `S87`

## Unmapped branch labels (17): no single my label

- `B1-guide1856`: Guide-set grouping (70 files: the 1856 guide run, mostly text pages), not a scene label. Its files belong to scenes by content, not by this label.
- `B2-iln1854`: Source-set grouping (ILN 1854 material), not a scene label.
- `B2-phillips1854`: Source-set grouping (Phillips 1854 guide material), not a scene label.
- `B5-heights`: Evidence grouping (dimensions/heights pages), not a scene label.
- `PLAN 1856 guide plate`: Plate grouping within the 1856 guide; not equivalent to my B-plans (5 rows of standalone plans).
- `PLAN court plan 1854`: Plate grouping; not equivalent to my B-plans.
- `PLAN heights evidence`: Evidence grouping (dimensions pages); not equivalent to my B-plans.
- `PLAN railway arrival`: Route/arrival grouping; the kept file for its content is my S44-section routes map row, but the label itself has no single my equivalent.
- `S15`: Scene label with no my-manifest counterpart: my S15 material (Fox, Henderson pamphlet pages) lives in build/gap-closers/, not in my manifest, because it was staged during the build, not round 2.
- `S45-47`: Multi-scene tag spanning my S45 (and the S46/S47 passage). No single my label; the kept S45 row carries my S45 only.
- `S46`: Scene label with no my-manifest counterpart (my removal passage is filed under S45 only).
- `S47`: Scene label with no my-manifest counterpart as a section: the S47 interior alias maps to my S57 row (see ALIAS-TABLE.csv, cross-section case).
- `S56-S66 route plan`: Route-plan grouping for the Sydenham route scenes; my route material is filed under B-plans / S57, not under a route-plan label.
- `S62 grounds`: Grounds-map grouping; no my-manifest counterpart (my grounds material is under B-plans).
- `S66 north transept / fire context`: Fire-context grouping; no my-manifest counterpart.
- `S66 post-fire plan`: Post-fire-plan grouping; my post-1866 plan (1878 guide plan) was staged in build/gap-closers/, not in my manifest.
- `S89`: Scene label with no my-manifest counterpart: round 2 found no usable S89 file, so my manifest has no S89 section; the branch S89 row is a modern (2024) fallback photo, never a 1960s photo.

## My labels with no branch counterpart

- `B-plans`: my standalone-plan grouping (1856 ground plan, 1856 Plan of Palace and Park, OS Surrey crop, and related plans). The branch files these under PLAN/B1/B2 labels instead; see above.
