# Gyro Pro turntable library

Edition 1.1.0 identifies 134 turntables and one related factory designation. Every record has model evidence; technical fields are optional. Factory specifications describe a model, not an owner's measurements.

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
| **Total** | **134** |

## Build and verify

From the public repository root, with Python 3.10 or later:

```console
python -m pip install -r catalog/requirements.txt
python catalog/catalog.py check
python -m unittest discover -s catalog
python catalog/catalog.py build
```

After dependency installation these commands work offline. The check validates the data and compares the committed artifact byte for byte. The build sorts records by manufacturer, model and ID, sorts object keys and writes UTF-8 without BOM, with LF endings. To bundle the [built JSON](dist/catalog.json) in Android, copy it to `app/src/main/assets/turntables/catalog.json` during app assembly. Reading this asset requires no GitHub request.

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
