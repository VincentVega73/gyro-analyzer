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


def designations(row):
    yield "name", row["model"], None
    for alias in row["aliases"]:
        yield "alias", alias, None
    for relation in row.get("related_designations", []):
        yield "related_designation", relation["designation"], relation


def matches(records, manufacturer, name, *, short_names=False):
    brand, query = norm(manufacturer), norm(name)
    for row in records:
        if norm(row["manufacturer"]) != brand:
            continue
        for kind, label, relation in designations(row):
            if norm(label) == query:
                yield row, kind, label, relation
                break
        else:
            if short_names and row.get("production_evidence", {}).get("country") == "USSR":
                # Remove only the known brand and the whole stereo descriptor.
                # Letter suffixes and revision digits remain part of the index.
                index = norm(row["model"]).removeprefix(brand).removesuffix(brand)
                short = index.removesuffix("стерео")
                if query and query in {index, short, brand + short}:
                    yield row, "short_name", row["model"], None


def lookup(records, manufacturer, name):
    """Legacy API returns full model records for names and aliases."""
    return [row for row, _, _, relation in matches(records, manufacturer, name)
            if relation is None]


def lookup_matches(records, manufacturer, name):
    """Return identity and evidence. Technical fields belong to the base record."""
    results = []
    for row, kind, label, relation in matches(records, manufacturer, name, short_names=True):
        result = {"model_id": row["model_id"], "base_model": row["model"],
                  "match_type": kind, "matched_designation": label}
        if relation is not None:
            result["relation_type"] = relation["type"]
            result["source"] = next(s for s in row["sources"] if s["key"] == relation["source"])
            if "color" in relation:
                result["color"] = relation["color"]
        results.append(result)
    return results


def validate(data):
    schema = read(ROOT / "schema.json")
    validator = Draft202012Validator(schema)
    for e in validator.iter_errors(data):
        raise ValueError(f"{e.json_path}: {e.message}")
    ids, canonical = set(), set()
    names = defaultdict(list)
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
        facts = row.get("specifications", []) + [row[k] for k in ("drive_type", "speeds_rpm", "factory", "production_evidence", "product_standard") if k in row]
        if any(f["source"] not in keys for f in facts):
            raise ValueError(f"{mid}: unknown source key")
        for kind, label, relation in designations(row):
            n = norm(label)
            if not n:
                raise ValueError(f"{mid}: empty normalized {kind} {label!r}")
            if relation is not None and relation["source"] not in keys:
                raise ValueError(f"{mid}: {label!r}: unknown source {relation['source']!r}")
            names[brand, n].append(f"{mid} {kind} {label!r}")
    collisions = {k: v for k, v in names.items() if len(v) > 1}
    if collisions:
        raise ValueError(f"Designation collisions: {collisions}")


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
    commands = parser.add_subparsers(dest="action", required=True)
    commands.add_parser("check")
    commands.add_parser("build")
    search = commands.add_parser("lookup")
    search.add_argument("manufacturer")
    search.add_argument("query")
    args = parser.parse_args()
    try:
        if args.action == "lookup":
            data = read(OUTPUT)
            validate(data)
            print(json.dumps(lookup_matches(data["models"], args.manufacturer, args.query), ensure_ascii=False, indent=2))
            return
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
