"""Audit exact paths and bytes in the catalog, Android assets ZIP and debug APK."""
import argparse
import csv
import hashlib
import io
import json
from collections import Counter, defaultdict
from contextlib import ExitStack
from functools import lru_cache
from pathlib import Path
from zipfile import ZipFile

from PIL import Image

from catalog import ROOT, OUTPUT, read
from illustrations import check_evidence, check_file, FALLBACKS, GENERIC_CAPTION


def table(path, columns, rows):
    with path.open("w", encoding="utf-8-sig", newline="") as stream:
        writer = csv.DictWriter(stream, columns)
        writer.writeheader()
        writer.writerows(rows)


@lru_cache(maxsize=64)
def packed_file(archive, name, expected_hash):
    if archive.namelist().count(name) != 1:
        return "missing or duplicate path"
    blob = archive.read(name)
    if expected_hash is not None and hashlib.sha256(blob).digest() != expected_hash:
        return "different bytes"
    with Image.open(io.BytesIO(blob)) as image:
        image.load()
        if image.format != "WEBP" or image.size != (960, 720):
            return "invalid WebP"
    return "OK"


def check_package(archive, prefix, model_id, assignment, expected_hash, manifest_index):
    if archive is None:
        return "not checked"
    if manifest_index.get(model_id) != [assignment]:
        return "assignment differs"
    return packed_file(archive, prefix + "turntables/media/" + assignment["path"], expected_hash)


@lru_cache(maxsize=64)
def source_file(media, path):
    check_file(media, path)
    return hashlib.sha256((media / path).read_bytes()).digest()


def index(manifest):
    result = defaultdict(list)
    for entry in manifest["assignments"]:
        result[entry["model_id"]].append(entry)
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("bundle", type=Path)
    parser.add_argument("--apk", type=Path)
    args = parser.parse_args()
    out = ROOT / "review"
    media = ROOT / "media"
    models = read(OUTPUT)["models"]
    ids = {row["model_id"] for row in models}
    manifest = read(media / "manifest.json")
    assignments = index(manifest)
    study = {r["model_id"]: r.get("reason", "") for r in read(media / "research.json")["records"]}
    real_paths = {p.relative_to(media).as_posix() for p in media.rglob("*") if p.is_file()}
    priority = {}
    with (out / "priority-1.5.csv").open(encoding="utf-8-sig") as stream:
        for row in csv.DictReader(stream):
            if row["model_id"] and row["match"] != "related_designation":
                priority[row["model_id"]] = row["thumbnail_review"]
    rows, problems = [], []
    with ExitStack() as stack:
        archives = [(stack.enter_context(ZipFile(args.bundle)), "")]
        archives.append((stack.enter_context(ZipFile(args.apk)) if args.apk else None, "assets/"))
        packages = []
        used = {a["path"] for a in manifest["assignments"] + manifest["related_designations"]}
        for package, prefix in archives:
            packaged = {}
            if package is not None:
                base = prefix + "turntables/"
                if package.read(base + "catalog.json") != OUTPUT.read_bytes():
                    raise ValueError(f"{package.filename}: catalog differs")
                packed_manifest = json.loads(package.read(base + "media/manifest.json"))
                if packed_manifest != manifest:
                    problems.append(f"{package.filename}: manifest differs")
                packaged = index(packed_manifest)
                files = {n.removeprefix(base + "media/") for n in package.namelist()
                         if n.startswith(base + "media/") and n.lower().endswith(".webp")}
                if files != used:
                    problems.append(f"{package.filename}: extra/missing files {sorted(files ^ used)}")
            packages.append((package, prefix, packaged))
        for model in models:
            mid = model["model_id"]
            row = dict(model_id=mid, manufacturer=model["manufacturer"], model=model["model"],
                       kind="", path="", caption="", source_check="", bundle_check="", apk_check="",
                       visual_review=priority.get(mid, "не просматривался в этой итерации"), reason="")
            entries = assignments.get(mid, [])
            if not entries:
                row.update(status="назначения нет", source_check="missing assignment", reason="Нет назначения для ID")
            elif len(entries) != 1:
                row.update(status="изображение или привязка ошибочны", source_check="duplicate", reason="Несколько назначений")
            else:
                a = entries[0]
                row.update({k: a.get(k, "") for k in ("kind", "path", "caption")})
                try:
                    if a["path"] not in real_paths:
                        raise FileNotFoundError(a["path"])
                    digest = source_file(media, a["path"])
                    name = model["model"]
                    if model["manufacturer"].casefold() not in name.casefold():
                        name = model["manufacturer"] + " " + name
                    if a["kind"] == "model":
                        if a["caption"] != name or a["path"] != f"models/{mid}.webp":
                            raise ValueError("wrong depicted designation or path")
                        check_evidence(a)
                        status = "модельный эскиз доступен"
                    elif (a["kind"] == "generic" and a["caption"] == GENERIC_CAPTION
                          and a["path"] in {f"fallbacks/{f}.webp" for f in FALLBACKS}):
                        status = "условный эскиз доступен"
                        row["reason"] = study.get(mid) or "Индивидуальный рисунок ожидает проверки."
                    else:
                        raise ValueError("wrong kind, caption or fallback")
                    row.update(status=status, source_check="OK")
                except FileNotFoundError as exc:
                    row.update(status="файл отсутствует", source_check="missing exact path", reason=str(exc))
                except (ValueError, OSError, KeyError) as exc:
                    row.update(status="изображение или привязка ошибочны", reason=str(exc))
                    if not row["source_check"]:
                        row["source_check"] = "error"
                for column, (pkg, prefix, ix) in zip(("bundle_check", "apk_check"), packages):
                    try:
                        expected = digest if row["source_check"] == "OK" else None
                        row[column] = check_package(pkg, prefix, mid, a, expected, ix)
                    except (OSError, ValueError, KeyError) as exc:
                        row[column] = str(exc)
                    if row[column] not in ("OK", "not checked") and row["source_check"] == "OK":
                        row.update(status="изображение или привязка ошибочны", reason=column + ": " + row[column])
            rows.append(row)
    problems.extend("unknown ID " + mid for mid in sorted(set(assignments) - ids))
    problems.extend("unassigned file " + p for p in sorted({p for p in real_paths if p.lower().endswith(".webp")} - used))
    table(out / "images-audit.csv", list(rows[0]), rows)
    errors = [dict(model_id=r["model_id"], issue=r["reason"], next_action="Проверить источник и исправить назначение")
              for r in rows if r["status"] not in ("модельный эскиз доступен", "условный эскиз доступен")]
    errors.extend(dict(model_id="", issue=p, next_action="Сверить манифест и комплект") for p in problems)
    table(out / "images-errors.csv", ["model_id", "issue", "next_action"], errors)
    counts = Counter((r["manufacturer"], r["status"]) for r in rows)
    summary = [dict(manufacturer=b, status=s, count=n) for (b, s), n in sorted(counts.items())]
    table(out / "images-by-brand.csv", ["manufacturer", "status", "count"], summary)
    print(f"{len(rows)} models; {len(used)} unique files; {len(errors)} errors")
    if errors:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
