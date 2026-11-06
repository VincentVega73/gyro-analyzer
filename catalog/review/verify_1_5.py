"""Verify edition 1.5 against Git baseline and the original research archive."""
import argparse
import csv
import io
import json
import subprocess
from pathlib import Path
from zipfile import ZipFile

REPORTS = Path(__file__).resolve().parent
BASE = "bb7dfb9377c9e74af89c89223afff1cb0072bc32"


def rows(path):
    with path.open(encoding="utf-8-sig", newline="") as stream:
        return list(csv.DictReader(stream))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("research_zip", type=Path)
    args = parser.parse_args()
    previous = json.loads(subprocess.check_output(
        ["git", "show", BASE + ":catalog/dist/catalog.json"], cwd=REPORTS
    ))
    current = json.loads((REPORTS.parent / "dist/catalog.json").read_bytes())
    old = {r["model_id"]: r for r in previous["models"]}
    new = {r["model_id"]: r for r in current["models"]}
    assert previous["catalog_version"] == "1.4.0" and len(old) == 1581
    assert current["catalog_version"] == "1.5.0" and len(new) == len(current["models"])
    assert all((r["manufacturer"], r["model"]) == (new[i]["manufacturer"], new[i]["model"])
               for i, r in old.items())

    audit = rows(REPORTS / "source-review-1.4.csv")
    added = [r for r in audit if r["decision"] == "added_1.4"]
    assert len(added) == len({r["model_id"] for r in added}) == 1214
    for r in added:
        assert r["primary_evidence"] and r["primary_evidence"] in {
            s["url"] for s in old[r["model_id"]]["sources"]
        }
    sample = rows(REPORTS / "added-1.4-sample.csv")
    assert len({r["manufacturer"] for r in sample}) >= 20
    assert all(r["source"] and r["page_or_figure"] and r["printed_designation"] for r in sample)

    decisions = rows(REPORTS / "document-review-1.5.csv")
    expected = [(r["brand"], r["candidate"]) for r in audit if r["decision"] == "document_unverified"]
    assert len(decisions) == len(expected) == 162
    assert [(r["manufacturer"], r["candidate"]) for r in decisions] == expected
    assert all(r["source"] and r["reason"] and (not r["model_id"] or r["model_id"] in new) for r in decisions)
    priority = rows(REPORTS / "priority-1.5.csv")
    with ZipFile(args.research_zip) as z:
        original = list(csv.DictReader(io.StringIO(z.read("priority_models.csv").decode("utf-8-sig"))))
    assert [(r["brand"], r["query"]) for r in priority] == [(r["brand"], r["model"]) for r in original]
    assert len(priority) == 50 and all(r["model_id"] in new for r in priority)
    added_ids = {r["model_id"] for r in decisions if r["decision"] == "самостоятельная модель"}
    added_ids.update(r["model_id"] for r in priority if r["model_id"] not in old)
    assert added_ids == new.keys() - old.keys()
    images = rows(REPORTS / "images-audit.csv")
    assert len(images) == len(new) and {r["model_id"] for r in images} == new.keys()
    assert all(r["source_check"] == r["bundle_check"] == r["apk_check"] == "OK" for r in images)
    print(f"OK: {len(added)} evidence links, {len(sample)} sample sheets, {len(decisions)} decisions, "
          f"{len(priority)} priority rows, {len(images)} image assignments; {len(added_ids)} new IDs")


if __name__ == "__main__":
    main()
