# scan-fig68-victoria-and-children — Muse version

**Muse version** (ships as `scan-fig68-victoria-and-children-muse`).

## Subject
John Callcott Horsley, *A Portrait Group of Queen Victoria and Her Children* (c. 1865; catalog fig. 68, scan IMG_6430). Modelled as a posed interior group vignette exactly as composed in the image: a standing man at screen-left holding a document against his waist, a table at centre carrying a globe on a stand and two spread (blank) documents, the Queen seated at centre-right in a high-back chair gesturing with her extended arm toward the globe/documents, an elder boy standing at screen-right, and five children grouped around the table and in the foreground. Dark wall, chimney-breast column at screen-left and deep-red drape at screen-right evoke the painting's interior.

## Scale
Group spans ~4.6 m; figures 0.82–1.76 m. **Scale estimated** from the figures themselves (adult man set to 1.76 m); no dimension exists in the source.

## Assumptions / interpretation
- Figures are stylised simplified forms in period dress silhouettes — tapered coat/skirt masses, plain heads, hair caps, no facial features and **no likenesses**; the Queen is identified only by pose, dress, lace collar and a small gilt coronet.
- The catalog describes "a map or document and a globe" — both are included; all paper is blank (no lettering invented).
- The painting is a single viewpoint: backs of figures, the room's extent and all detail beyond the drawn group are plain interpretation.
- The standing man's identity is not asserted (the catalog titles the work "Queen Victoria and her children" only).

## Technical
- Triangles: **30,548**. Blender 4.5.3, metres, origin at base centre, scale applied.
- Files: `scan-fig68-victoria-and-children.blend`, `.glb`, `preview.png` (Cycles, 48 samples + denoise, frontal view comparable to the painting), re-runnable `build_scan_fig68_victoria_and_children.py`.

## QC
Preview checked against the reference: composition, handedness (man screen-left, Queen screen-right, globe centre-left on the table) and the Queen's pointing gesture verified after two camera fixes (a stray default cube removed; camera re-aimed with a tracked quaternion after an initial roll error). Colours converted sRGB→linear. Known simplifications: the document in the man's hands is a plain sheet with the hands suggested at its edges; the elder girl stands partly behind the table as in the painting's crowding.

## Manual-review items
- Figure likeness is deliberately nil — do not present any figure as a portrait.
- If the vignette is used at close range, the hands/document junction and the boy's hand-held book read crudely.
