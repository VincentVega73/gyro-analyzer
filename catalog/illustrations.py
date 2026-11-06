"""Validate offline illustration assignments and resolve source-backed captions."""
import re
from pathlib import Path, PurePosixPath
from urllib.parse import urlsplit

from PIL import Image


FALLBACKS = {"neutral", "classic", "open", "linear"}
GENERIC_CAPTION = "Условное изображение"


def check_file(root, relative):
    if not isinstance(relative, str) or not re.fullmatch(
        r"(models|fallbacks)/[a-z0-9-]+\.webp", relative
    ):
        raise ValueError(f"Unsafe illustration path: {relative!r}")
    path = (root / PurePosixPath(relative)).resolve()
    if not path.is_relative_to(root.resolve()):
        raise ValueError(f"Illustration outside media directory: {relative}")
    try:
        with Image.open(path) as image:
            if image.format != "WEBP" or image.size != (960, 720) or image.n_frames != 1:
                raise ValueError(f"Expected a single 960 x 720 WebP: {relative}")
            image.load()
    except OSError as exc:
        raise ValueError(f"Unreadable illustration: {relative}") from exc


def check_construction_study(entry):
    sources = entry.get("construction_sources")
    if not isinstance(sources, list) or "reference" in entry or "additional_references" in entry:
        raise ValueError("Independent study requires a separate construction evidence list")
    photos, manuals = set(), set()
    for source in sources:
        if not isinstance(source, dict) or not all(
            isinstance(source.get(k), str) and source[k].strip()
            for k in ("title", "organization", "page", "detail", "locator", "type")
        ):
            raise ValueError("Incomplete construction source")
        url = urlsplit(source["page"])
        if url.scheme not in ("http", "https") or not url.hostname:
            raise ValueError("Invalid construction source URL")
        location = (source["page"], source["locator"])
        if source["type"] == "photograph":
            photos.add(location)
        elif source["type"] == "manual":
            manuals.add(location)
        else:
            raise ValueError("Unknown construction source type")
    if len(photos) < 2 or not manuals:
        raise ValueError("Two distinct photo views and a factory manual are required")
    credit = entry.get("artwork_credit")
    if not isinstance(credit, dict) or not all(isinstance(credit.get(k), str)
            and credit[k].strip() for k in ("credit", "license", "license_url")):
        raise ValueError("Missing independent artwork credit")


def check_evidence(entry):
    review = entry.get("visual_review")
    if not isinstance(review, dict) or not all(
        isinstance(review.get(key), str) and review[key].strip() for key in ("full_size", "card_size")
    ):
        raise ValueError("Missing visual review at both sizes")
    mode = entry.get("creation", "reference_redraw")
    if mode == "independent_study":
        check_construction_study(entry)
        return
    if mode != "reference_redraw":
        raise ValueError("Unknown illustration creation mode")
    source = entry.get("reference")
    required = ("page", "author", "title", "depicted", "identification", "license", "license_url", "changes")
    if not isinstance(source, dict) or not all(
        isinstance(source.get(key), str) and source[key].strip() for key in required
    ):
        raise ValueError("Missing model reference or attribution")
    for key in ("page", "license_url"):
        url = urlsplit(source[key])
        if url.scheme not in ("https", "http") or not url.hostname:
            raise ValueError(f"Invalid source {key}")
    for extra in entry.get("additional_references", []):
        if not isinstance(extra, dict) or not all(
            isinstance(extra.get(key), str) and extra[key].strip() for key in required
        ) or extra["depicted"] != entry["caption"]:
            raise ValueError("Missing supporting reference details")
    if source["depicted"] != entry["caption"]:
        raise ValueError("Depicted model differs from caption")



def validate_illustrations(models, manifest, root):
    if not isinstance(manifest, dict) or manifest.get("version") != 2 or not isinstance(manifest.get("assignments"), list):
        raise ValueError("Invalid illustration manifest")
    names = {row["model_id"]: (row["model"] if row["manufacturer"].casefold() in row["model"].casefold()
                             else f"{row['manufacturer']} {row['model']}") for row in models}
    seen, paths = set(), {f"fallbacks/{name}.webp" for name in FALLBACKS}
    for entry in manifest["assignments"]:
        if not isinstance(entry, dict):
            raise ValueError("Invalid illustration assignment")
        mid = entry.get("model_id")
        if mid not in names or mid in seen:
            raise ValueError(f"Unknown or duplicate illustration ID: {mid}")
        seen.add(mid)
        kind, path = entry.get("kind"), entry.get("path")
        if kind == "generic":
            if entry.get("caption") != GENERIC_CAPTION or path not in {f"fallbacks/{x}.webp" for x in FALLBACKS}:
                raise ValueError(f"{mid}: invalid conditional illustration or caption")
        elif kind == "model":
            if path != f"models/{mid}.webp" or entry.get("caption") != names[mid]:
                raise ValueError(f"{mid}: wrong model path or depicted designation")
            check_evidence(entry)
        else:
            raise ValueError(f"{mid}: unknown illustration kind")
        paths.add(path)
    if seen != names.keys():
        raise ValueError(f"Missing illustration assignments: {sorted(names.keys() - seen)}")
    # Color variants use a labeled fallback until given a separate visual review.
    related = {(r["model_id"], item["designation"]) for r in models for item in r.get("related_designations", [])}
    for entry in manifest.get("related_designations", []):
        key = (entry.get("model_id"), entry.get("designation"))
        if key not in related or entry.get("kind") != "generic" or entry.get("caption") != GENERIC_CAPTION:
            raise ValueError(f"Invalid related illustration: {key}")
        if entry.get("path") not in {f"fallbacks/{x}.webp" for x in FALLBACKS}:
            raise ValueError(f"Invalid related fallback: {key}")
        related.remove(key)
    if related:
        raise ValueError(f"Missing related designations: {sorted(related)}")
    for path in sorted(paths):
        check_file(root, path)
    files = {p.relative_to(root).as_posix() for p in root.rglob("*.webp")}
    if files != paths:
        raise ValueError(f"Unassigned media files: {sorted(files - paths)}")
    return sorted(paths)
