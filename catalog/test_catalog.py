import copy
import unittest

from catalog import OUTPUT, collect, lookup, lookup_matches, read, validate


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
            ({"model": "Other", "model_id": "another", "aliases": ["SL1200MK2"]}, "Designation collisions"),
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

    def test_packaged_designations(self):
        rows = read(OUTPUT)["models"]
        base, = lookup_matches(rows, "Technics", "SL-1200GR2")
        self.assertEqual(base["match_type"], "name")
        for query in ("SL-1210GR2", "sl1210gr2", "SL 1210 GR2"):
            variant, = lookup_matches(rows, "Technics", query)
            self.assertEqual(variant, {
                "model_id": base["model_id"], "base_model": "SL-1200GR2",
                "match_type": "related_designation", "matched_designation": "SL-1210GR2",
                "color": "black", "relation_type": "color_variant",
                "source": lookup(rows, "Technics", "SL-1200GR2")[0]["sources"][0],
            })
        self.assertEqual(lookup_matches(rows, "Technics", "SL1200MK99"), [])

    def test_invalid_related_designations(self):
        base, = lookup(self.data["models"], "Technics", "SL-1200GR2")
        for patch, reason in [
            ({"designation": "SL 1200 mk2"}, "Designation collisions"),
            ({"designation": "Test Alias"}, "Designation collisions"),
            ({"designation": "Other Variant"}, "Designation collisions"),
            ({"designation": "SL1200GR2"}, "Designation collisions"),
            ({"designation": "---"}, "empty normalized"),
            ({"designation": " "}, "does not match"),
            ({"source": "missing"}, "unknown source"),
            ({"type": "region"}, "color_variant"),
        ]:
            with self.subTest(patch=patch):
                mk2, = lookup(self.data["models"], "Technics", "SL1200MK2")
                other = dict(mk2, aliases=["Test-Alias"], related_designations=[
                    dict(base["related_designations"][0], designation="Other-Variant")])
                target = dict(base, related_designations=[dict(base["related_designations"][0], **patch)])
                with self.assertRaisesRegex(ValueError, reason):
                    validate(dict(self.data, models=[target, other]))
        foreign = dict(other, manufacturer="Other", aliases=["sl1210gr2"])
        validate(dict(self.data, models=[base, foreign]))
        hit, = lookup_matches([base, foreign], "Other", "SL-1210GR2")
        self.assertEqual(hit["match_type"], "alias")

    def test_owner_queries_in_packaged_catalog(self):
        rows = read(OUTPUT)["models"]
        for brand, index, expected in [
            ("Арктур", "006", "Арктур-006-стерео"),
            ("электроника", "эп017", "Электроника ЭП-017-стерео"),
            ("Вега", "106", "Вега-106-стерео"),
        ]:
            with self.subTest(brand=brand):
                hit, = lookup_matches(rows, brand, index)
                self.assertEqual((hit["base_model"], hit["match_type"]), (expected, "short_name"))
                self.assertEqual([hit], lookup_matches(rows, brand, brand + " " + index))
                full, = lookup_matches(rows, brand, expected)
                self.assertEqual((full["model_id"], full["match_type"]), (hit["model_id"], "name"))
        for brand, query in [("Вега", "G-602"), ("Арктур", "G-2021"),
                             ("Электроника", "эф017"), ("Феникс", "эп008"),
                             ("Вега", "ЭП122М"), ("Электроника", "ep017")]:
            self.assertEqual(lookup_matches(rows, brand, query), [])

    def test_ambiguous_short_name_lists_all_candidates(self):
        data = copy.deepcopy(self.data)
        row, = lookup(data["models"], "Арктур", "Арктур-006-стерео")
        other = dict(row, model_id="another", model="Арктур-006")
        data["models"].append(other)
        validate(data)
        result = lookup_matches(data["models"], "Арктур", "006")
        self.assertCountEqual([r["model_id"] for r in result], [row["model_id"], "another"])

    def test_release_scope(self):
        brands = {"Audio-Technica", "Dual", "Michell", "Pioneer", "Rega", "Sony", "Technics", "Thorens"}
        self.assertTrue(brands <= {r["manufacturer"] for r in self.data["models"]})
        self.assertGreaterEqual(len(self.data["models"]), 100)


if __name__ == "__main__":
    unittest.main()
