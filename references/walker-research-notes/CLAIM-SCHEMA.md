# Claim schema

## Summary (read first)

A **claim** is one statement about 1851 with its evidence, in one JSON file. The game reads
claims to build evidence cards; agents and contributors write candidate claims in the same
format. If a statement has no source it is not a claim, it is a question: put it in
`research/QUESTIONS.md`.

## Format

```json
{
  "id": "C-exhibit-0001",
  "kind": "exhibit | position | day | experience | person | labour | sense | image | building",
  "subject": "short noun phrase, for example 'Koh-i-Noor diamond display'",
  "statement": "one sentence, in plain words, that the sources support",
  "tier": "documented | measured | inferred | simplified | invented | unknown",
  "sources": [
    {
      "tier": "primary | secondary | tertiary",
      "citation": "author, title, year, volume/page or column",
      "url": "link to a public scan or record, or null",
      "quote": "under 15 words, or null",
      "rights": "public-domain | cc0 | cc-by | restricted | unknown"
    }
  ],
  "date": "ISO date the statement is about, or null",
  "position": {"x_ft": null, "y_ft": null, "z_ft": null, "tier": "unknown"},
  "conflicts_with": [],
  "unknowns": "what the sources do NOT tell us",
  "contributor": "handle or agent name",
  "status": "candidate | reviewed | accepted | disputed | rejected",
  "reviewed_by": null
}
```

## Rules

- `tier` names the weakest link of the statement: an object that is documented but whose place
  is guessed has `tier: documented` on the exhibit claim and a separate `position` claim with
  `tier: inferred`.
- `measured` is reserved for the building (taken from the plates); it is not used for exhibits.
- At least one source with `tier: primary` is required for `documented`. A claim with only
  secondary or tertiary sources is `inferred` at best.
- `quote` is optional and short. Never paste long passages. Restricted-rights works are paraphrased and cited.
- A claim file is named `<id>.json` and never edited after acceptance; corrections are new
  claims with `conflicts_with` pointing at the old one.
- Positions use the building model's source units (feet) and origin (centre of the nave and
  transept crossing at floor level, +X east, +Y north, Z up).
