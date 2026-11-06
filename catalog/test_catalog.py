import copy
import unittest

from catalog import collect, lookup, validate


class CatalogTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = collect()

    def test_lookup_and_revision(self):
        rows = self.data["models"]
        mk2, = lookup(rows, "Technics", "SL1200MK2")
        self.assertEqual([mk2], lookup(rows, "technics", "SL-1200MK2"))
        mk3, = lookup(rows, "Technics", "SL 1200 mk3")
        self.assertNotEqual(mk2["model_id"], mk3["model_id"])
        se, = lookup(rows, "Michell", "Gyro SE")
        dec, = lookup(rows, "Michell", "GyroDec")
        self.assertNotEqual(se["model_id"], dec["model_id"])

    def test_rename_preserves_id(self):
        data = copy.deepcopy(self.data)
        item, = lookup(data["models"], "Technics", "SL1200MK2")
        original = item["model_id"]
        item["model"] = "Corrected display name"
        validate(data)
        self.assertEqual(original, lookup(data["models"], "Technics", item["model"])[0]["model_id"])

    def test_invalid_records(self):
        first, = lookup(self.data["models"], "Technics", "SL1200MK2")
        for patch, reason in [
            ({"sources": []}, "non-empty"),
            ({"unknown": True}, "Additional properties"),
            ({"drive_type": {"value": "direct", "source": "missing"}}, "unknown source"),
            ({"speeds_rpm": {"value": ["0"], "source": "manual"}}, "does not match"),
            ({"model_id": first["model_id"], "model": "Other"}, "duplicate ID"),
            ({"model": "SL 1200 MK2", "model_id": "another"}, "canonical"),
            ({"model": "Other", "model_id": "another", "aliases": ["SL1200MK2"]}, "Alias collisions"),
        ]:
            with self.subTest(patch=patch):
                data = copy.deepcopy(self.data)
                row = dict(first, **patch)
                if "model_id" in patch:
                    data["models"].append(row)
                else:
                    data["models"][data["models"].index(first)] = row
                with self.assertRaisesRegex(ValueError, reason):
                    validate(data)

    def test_release_scope(self):
        brands = {"Audio-Technica", "Dual", "Michell", "Pioneer", "Rega", "Sony", "Technics", "Thorens"}
        self.assertTrue(brands <= {r["manufacturer"] for r in self.data["models"]})
        self.assertGreaterEqual(len(self.data["models"]), 100)


if __name__ == "__main__":
    unittest.main()
