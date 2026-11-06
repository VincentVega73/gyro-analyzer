"""Build and check the offline turntable catalog."""
import argparse
import json
import sys
import unicodedata
from collections import defaultdict
from pathlib import Path
from urllib.parse import urlsplit

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parent
OUTPUT = ROOT / "dist" / "catalog.json"


def unique_keys(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"Repeated JSON key: {key}")
        result[key] = value
    return result


def read(path):
    return json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=unique_keys)


def norm(name):
    return "".join(c for c in unicodedata.normalize("NFKC", name).casefold() if c.isalnum())


def lookup(records, manufacturer, name):
    return [r for r in records if norm(r["manufacturer"]) == norm(manufacturer)
            and norm(name) in {norm(x) for x in [r["model"], *r["aliases"]]}]


def validate(data):
    schema = read(ROOT / "schema.json")
    validator = Draft202012Validator(schema)
    for e in validator.iter_errors(data):
        raise ValueError(f"{e.json_path}: {e.message}")
    ids, canonical = set(), set()
    names = defaultdict(set)
    for row in data["models"]:
        mid = row["model_id"]
        brand = norm(row["manufacturer"])
        model = norm(row["model"])
        if not brand or not model or mid in ids or (brand, model) in canonical:
            raise ValueError(f"{mid}: empty name or duplicate ID/canonical name")
        ids.add(mid)
        canonical.add((brand, model))
        keys = set()
        for s in row["sources"]:
            url = urlsplit(s["url"])
            if not url.hostname or (url.path.lower().endswith(".pdf") and "page" not in s):
                raise ValueError(f"{mid}: invalid URL or missing PDF page")
            if s["key"] in keys:
                raise ValueError(f"{mid}: duplicate local source key")
            keys.add(s["key"])
        facts = row.get("specifications", []) + [row[k] for k in ("drive_type", "speeds_rpm") if k in row]
        if any(f["source"] not in keys for f in facts):
            raise ValueError(f"{mid}: unknown source key")
        local = set()
        for label in [row["model"], *row["aliases"]]:
            n = norm(label)
            if not n or n in local:
                raise ValueError(f"{mid}: empty or redundant alias {label}")
            names[brand, n].add(mid)
            local.add(n)
    collisions = {k: sorted(v) for k, v in names.items() if len(v) > 1}
    if collisions:
        raise ValueError(f"Alias collisions (review separately): {collisions}")


def collect():
    records = []
    for path in sorted((ROOT / "manufacturers").glob("*.json")):
        batch = read(path)
        if not isinstance(batch, list) or not batch or any(
            not isinstance(r, dict) or str(r.get("manufacturer")).casefold() != path.stem for r in batch
        ):
            raise ValueError(f"{path.name}: expected nonempty array for this manufacturer")
        records.extend(batch)
    data = {**read(ROOT / "version.json"), "models": records}
    validate(data)
    records.sort(key=lambda r: (norm(r["manufacturer"]), norm(r["model"]), r["model_id"]))
    return data


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=["check", "build"])
    args = parser.parse_args()
    try:
        data = collect()
        content = (json.dumps(data, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode("utf-8")
        if args.action == "build":
            OUTPUT.parent.mkdir(exist_ok=True)
            OUTPUT.write_bytes(content)
        elif not OUTPUT.exists() or OUTPUT.read_bytes() != content:
            raise ValueError("catalog/dist/catalog.json is missing or stale; run build")
        print(f"{args.action}: OK, {len(data['models'])} models")
    except (ValueError, OSError) as exc:
        sys.exit(str(exc))


if __name__ == "__main__":
    main()
