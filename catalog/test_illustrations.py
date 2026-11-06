import copy
import tempfile
import unittest
from pathlib import Path

from catalog import ROOT, read
from illustrations import check_file, validate_illustrations


class IllustrationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.media = ROOT / "media"
        cls.manifest = read(cls.media / "manifest.json")
        cls.models = read(ROOT / "dist" / "catalog.json")["models"]

    def test_manifest_covers_the_artifact_once(self):
        validate_illustrations(self.models, self.manifest, self.media)
        for change in ("missing", "duplicate", "unknown", "new_model"):
            with self.subTest(change=change):
                doc = copy.deepcopy(self.manifest)
                models = list(self.models)
                rows = doc["assignments"]
                if change == "missing":
                    rows.pop()
                elif change == "duplicate":
                    rows.append(rows[0])
                elif change == "unknown":
                    rows[0]["model_id"] = "unknown-model"
                else:
                    models.append({"model_id": "new", "manufacturer": "Example", "model": "New"})
                with self.assertRaises(ValueError):
                    validate_illustrations(models, doc, self.media)

    def test_false_labels_and_unsafe_paths(self):
        for kind, patch in [
            ("generic", {"caption": ""}), ("generic", {"path": "../escape.webp"}),
            ("model", {"reference": {}}), ("model", {"visual_review": {}}),
        ]:
            with self.subTest(patch=patch):
                doc = copy.deepcopy(self.manifest)
                next(r for r in doc["assignments"] if r["kind"] == kind).update(patch)
                with self.assertRaises(ValueError):
                    validate_illustrations(self.models, doc, self.media)

    def test_invalid_files(self):
        from PIL import Image
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "models").mkdir()
            path = root / "models/sample.webp"
            for state in ("missing", "corrupt", "wrong size", "wrong format"):
                with self.subTest(state=state):
                    if state == "corrupt":
                        path.write_bytes(b"invalid")
                    elif state == "wrong size":
                        Image.new("RGB", (50, 50)).save(path)
                    elif state == "wrong format":
                        Image.new("RGB", (960, 720)).save(path, "PNG")
                    with self.assertRaises(ValueError):
                        check_file(root, "models/sample.webp")
