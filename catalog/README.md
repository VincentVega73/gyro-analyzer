# Gyro Pro turntable library

Edition 1.2.0 identifies 154 turntables and one related factory designation. Every record has model evidence; technical fields are optional. Factory specifications describe a model, not an owner's measurements.

| Manufacturer | Models |
| --- | ---: |
| Audio-Technica | 11 |
| Dual | 31 |
| Michell | 8 |
| Pioneer | 34 |
| Rega | 22 |
| Sony | 5 |
| Technics | 11 |
| Thorens | 12 |
| Ария | 1 |
| Арктур | 1 |
| Вега | 4 |
| Импульс | 1 |
| Корвет | 2 |
| Орфей | 1 |
| Радиотехника | 2 |
| Феникс | 2 |
| Электроника | 5 |
| Эстония | 1 |
| **Total** | **154** |

## Build and verify

From the public repository root, with Python 3.10 or later:

```console
python -m pip install -r catalog/requirements.txt
python catalog/catalog.py check
python -m unittest discover -s catalog
python catalog/catalog.py build
```

After dependency installation these commands work offline. The check validates the data and compares the committed artifact byte for byte. The build sorts records by manufacturer, model and ID, sorts object keys and writes UTF-8 without BOM, with LF endings. The offline package contains the data, illustrations and credits.

## Offline illustrations

From the repository root, run `python catalog/catalog.py bundle ../gyro-turntables-assets.zip` after installing the dependencies above. Extract the ZIP into `app/src/main/assets/`. The archive root is `turntables/`; the catalog is `turntables/catalog.json` and the illustration manifest is `turntables/media/manifest.json`. Resolve a model ID in `assignments`, then open its `path` relative to the manifest directory. Render its `caption` verbatim. It either identifies the pictured model or says «Условное изображение». Use the separate `related_designations` entry when looking up a related name. It has its own caption decision and adds no model ID.

The manifest also carries per-image attribution, source and license links and the visual review notes. Keep it with the images. Four original generic plates are stored once and referenced by multiple rows. The catalog validator checks every assignment and decodes all WebP files during both check and build. Adding a model requires a media assignment in the same change.

[Coverage, source credits and review notes](media/REPORT.md) · [All 154 thumbnails](review/catalog-overview.png) · [Per-model research log](media/research.json)

## Editing the data

- Edit [one source array per manufacturer](manufacturers). [schema.json](schema.json) describes the assembled object and its individual records under `$defs.model`. [version.json](version.json) separates format compatibility from data edition.
- Assign a permanent `model_id` once; retain it when correcting names and never recycle retired IDs. A future private instance can reference a model or omit that reference. Serial numbers, repairs and user measurements do not belong here.
- The local source key `identity` identifies the model. Cite other sources by their local key. PDF pages are one-based file pages. Japanese source titles may be translated for the English repository. Omit unknown fields; an empty alias array means no alternative names have been verified.
- RPM values are exact strings: `100/3` means 33⅓; `33` means exactly 33. Preserve the published measurement method and conditions for each specification. A motor-generator measurement is not a measurement from a test record.
- Lookup ignores case, spacing and punctuation but keeps digits and revision suffixes. Conflicting aliases stop the build and identify the records requiring review.
- Submit corrections via an Issue with primary evidence, then a reviewed PR. Private entries made in the app are not submitted automatically.

## Searching by the designation on the turntable

Use an alias for a documented second name of the same model. For a separately labelled finish, use a related designation when the manufacturer explicitly identifies the color pairing. Give a technically distinct revision its own model ID. Ignore punctuation, spaces and case in all three cases. All normalized labels must be unique within each manufacturer.

Schema 2 adds an optional field. Schema 1 rejected additional model properties, so strict version 1 readers need an update. Existing individual records remain valid without the field. The legacy Python function `lookup` still returns full records for names and aliases. Use `lookup_matches` or the CLI for designation-aware results. The CLI requires a manufacturer and reads the built asset. An empty result is `[]`. Specifications accessed later by model ID describe the base record. Only the facts in the relation itself are attributed to the matched finish.

The SL-1200GR2 record links its variant to the existing local source key:

```json
{
  "related_designations": [
    {
      "color": "black",
      "designation": "SL-1210GR2",
      "source": "identity",
      "type": "color_variant"
    }
  ]
}
```

```console
python catalog/catalog.py lookup Technics SL-1200GR2
```

```json
[
  {
    "model_id": "technics-0011",
    "base_model": "SL-1200GR2",
    "match_type": "name",
    "matched_designation": "SL-1200GR2"
  }
]
```

```console
python catalog/catalog.py lookup Technics SL-1210GR2
```

```json
[
  {
    "model_id": "technics-0011",
    "base_model": "SL-1200GR2",
    "match_type": "related_designation",
    "matched_designation": "SL-1210GR2",
    "relation_type": "color_variant",
    "source": {
      "key": "identity",
      "title": "Technics unveils the next generation high-end turntables in its iconic SL-1200 Series",
      "url": "https://www.technics.com/se/news/0024.html"
    },
    "color": "black"
  }
]
```

## Soviet domestic turntables

Edition 1.2.0 adds 20 models across ten marques. Each record cites a leaf of the manufacturer's manual for the complete Cyrillic designation. The production year has a separate local source: a dated factory sheet or the model history in the radio museum. It documents Soviet production and need not be the year of the first unit. Leaf numbers count from the beginning of the scan, including covers. A single leaf may contain two printed pages.

The existing `manufacturer` field is the marque used for selection. `factory.value` names the enterprise and `factory.source` identifies its evidence. `production_evidence` gives the country, year and source. Source documents identify the finished product; an EPU code identifies an installed mechanism. Search keys comprise the original designations, verified aliases and relationships. Schema 3 adds the optional factory, production, product conformity and speed transcription fields to the closed schema.

For Soviet cards the detailed lookup also accepts the index within the selected marque, optionally with the word «стерео» omitted. It returns every candidate with a matching short name. Letter suffixes, including С, and leading zeroes stay significant. Search preserves the distinction between Cyrillic and Latin characters. Examples from the bundled artifact:

| Command (from repository root) | Result | ID |
| --- | --- | --- |
| `python catalog/catalog.py lookup Арктур 006` | Арктур-006-стерео | arktur-0001 |
| `python catalog/catalog.py lookup электроника эп017` | Электроника ЭП-017-стерео | elektronika-0003 |
| `python catalog/catalog.py lookup Вега 106` | Вега-106-стерео | vega-0001 |

The three results have `match_type: short_name`. Factory speed limits and tests apply to the edition cited. A published 33.33 rpm is stored as `3333/100`; an explicit 33⅓ rpm is `100/3`. Vega-106 speeds describe the two-speed manual. Preserve the scope of the general `product_standard` separately from any standard explicitly named for determining a specification.

| Verified field | New cards / 20 |
| --- | ---: |
| Drive type | 10 |
| Speeds | 20 |
| Factory wow and flutter rating | 16 |
| Rating explicitly described as an absolute value | 7 |
| Standard explicitly referenced for determining the characteristics | 1 |

Two examples trace the rating from the document to the data:

- Арктур-006-стерео: scan leaf 3, printed page 5, gives an absolute upper bound of 0.10% at 33.33 rpm. The field `specifications[0]` stores `value = "≤ 0.10"`, unit `%`, the absolute-value qualifier and the speed condition. [Operating manual](https://rw6ase.narod.ru/index1/gram_zapis/ep_s_el/arktur006in.djvu)
- Орфей-101-стерео: scan leaf 3, printed page 4, section 3.2 gives an absolute upper bound of 0.15%. The footnote explicitly names ГОСТ 24470-80 for determination of the characteristics. The field stores `value = "≤ 0.15"` and `standard = "ГОСТ 24470-80"`. [Operating manual](https://rw6ase.narod.ru/index1/gram_zapis/ep_s_el/orfey101s_in.djvu)

Absolute-value qualifiers describe the published rating. The last row counts only explicit standards for determination. Missing measurement procedures remain unknown. The upper bounds retain their published meaning, including the indicated unilateral tolerance where present.

Электроника Б1-01 was deferred: material on the electrophone set needs separate primary identification of the standalone player. The early Вега-110-стерео and post-Soviet or alternate spellings were not added as extra models. This edition identifies the documented Вега-ЭП-110-стерео. There are no new aliases or export relationships in this batch.

## Exclusions and identity decisions

- Michell Gyro SE, GyroDec and the new Gyro are separate records. A Gyro SE MK II setup guide does not establish equivalence with every Gyro SE. Its revision-specific parameters were not copied into the family record.
- SL-1210GR2 is the black counterpart to the silver SL-1200GR2. Both names resolve to technics-0011. See the [Technics joint announcement](https://www.technics.com/se/news/0024.html). SL-1200LTD was retained because Technics identifies a pitch reset function as well as a different finish.
- Rega Record Store Day 2016 RP1 and Thorens TD 124 DD 140th Anniversary were not counted on the basis of artwork or a commemorative bundle. See the [Rega timeline](https://www.rega.co.uk/about/timeline) and [Thorens lineup](https://www.thorens.com/en/items/products/turntables.html). TD 1600 TP 160 and TD 1601 TP 160 were deferred until the base model and tonearm configurations can be documented separately.
- Sony PS-LX150H and PS-LX350H were deferred because the individual support pages could not be verified for this edition.

## Two complete records

The [Michell timeline](https://www.michellaudio.com/about) describes the introduction of the Gyro SE separately from the GyroDec. Technics documents the MK2 in its [series history](https://www.technics.com/global/home/sl1200/heritage.html); the [120 V operating instructions, page 8](https://help.na.panasonic.com/wp-content/uploads/2023/02/SL1200MK2_SFNU122M06_ENG.pdf#page=8) support the speeds and the three distinct wow and flutter ratings below.

```json
{
  "model_id": "michell-0001",
  "manufacturer": "Michell",
  "model": "Gyro SE",
  "aliases": [],
  "sources": [
    {
      "key": "identity",
      "url": "https://www.michellaudio.com/about",
      "title": "About Michell Audio — Michell Timeline"
    }
  ]
}
```

```json
{
  "model_id": "technics-0001",
  "manufacturer": "Technics",
  "model": "SL-1200MK2",
  "aliases": [],
  "sources": [
    {
      "key": "identity",
      "url": "https://www.technics.com/global/home/sl1200/heritage.html",
      "title": "SL-1200 — Heritage"
    },
    {
      "key": "manual",
      "url": "https://help.na.panasonic.com/wp-content/uploads/2023/02/SL1200MK2_SFNU122M06_ENG.pdf",
      "title": "SL-1200MK2 Operating Instructions (120 V, 60 Hz) — Specifications",
      "page": 8
    }
  ],
  "drive_type": {
    "value": "direct",
    "source": "manual"
  },
  "speeds_rpm": {
    "value": [
      "100/3",
      "45"
    ],
    "source": "manual"
  },
  "specifications": [
    {
      "name": "wow_and_flutter",
      "original": "0.01% WRMS*",
      "value": "0.01",
      "unit": "%",
      "source": "manual",
      "method": "WRMS",
      "condition": "Motor frequency-generator signal; platter included, record, cartridge and tonearm excluded."
    },
    {
      "name": "wow_and_flutter",
      "original": "0.025% WRMS (JIS C5521)",
      "value": "0.025",
      "unit": "%",
      "source": "manual",
      "method": "WRMS",
      "standard": "JIS C5521"
    },
    {
      "name": "wow_and_flutter",
      "original": "±0.035% peak (IEC 98A Weighted)",
      "value": "±0.035",
      "unit": "%",
      "source": "manual",
      "method": "peak",
      "standard": "IEC 98A",
      "weighting": "IEC 98A Weighted"
    }
  ]
}
```
