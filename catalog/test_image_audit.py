import unittest
from io import BytesIO
from zipfile import ZipFile

from audit_images import check_package
from catalog import ROOT
from hashlib import sha256


class PackageAuditTests(unittest.TestCase):
    def test_shared_file_and_assignment_are_checked_separately(self):
        path = "fallbacks/neutral.webp"
        data = (ROOT / "media" / path).read_bytes()
        digest = sha256(data).digest()
        entry = {"model_id": "example", "path": path}
        prefix = "assets/"
        with ZipFile(BytesIO(), "w") as archive:
            archive.writestr(prefix + "turntables/media/" + path, data)
            self.assertEqual("OK", check_package(archive, prefix, "example", entry, digest, {"example": [entry]}))
            self.assertEqual("assignment differs", check_package(archive, prefix, "example", entry, digest, {}))
            self.assertEqual("different bytes", check_package(archive, prefix, "example", entry, b"", {"example": [entry]}))
            wrong = dict(entry, path="fallbacks/Neutral.webp")
            result = check_package(archive, prefix, "example", wrong, digest, {"example": [wrong]})
            self.assertEqual("missing or duplicate path", result)
