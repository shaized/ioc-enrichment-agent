import copy
import json
from pathlib import Path
import unittest

from agent import analyze


class AgentTests(unittest.TestCase):
    def setUp(self):
        self.data = json.loads(Path(__file__).with_name("example.json").read_text())

    def test_example_retains_three_distinct_applicability_states(self):
        result = analyze(self.data)
        self.assertEqual(result["summary"]["affected_version_matches"], 1)
        self.assertEqual(
            [row["status"] for row in result["findings"]],
            ["affected_version_match", "version_unknown", "version_not_listed"],
        )

    def test_vendor_and_product_case_does_not_hide_a_candidate(self):
        self.data["inventory"]["assets"][0]["vendor"] = " example vendor "
        self.assertEqual(analyze(self.data)["summary"]["affected_version_matches"], 1)

    def test_empty_inventory_does_not_assert_safety(self):
        self.data["inventory"]["assets"] = []
        self.assertEqual(analyze(self.data)["summary"]["assessment"], "inconclusive")

    def test_missing_version_is_not_interpreted_as_patched(self):
        self.data["inventory"]["assets"][0]["version"] = None
        self.assertEqual(analyze(self.data)["findings"][0]["status"], "version_unknown")

    def test_empty_affected_versions_is_rejected(self):
        self.data["advisory"]["affected_versions"] = []
        with self.assertRaises(ValueError):
            analyze(self.data)

    def test_duplicate_asset_ids_are_rejected(self):
        self.data["inventory"]["assets"].append(
            copy.deepcopy(self.data["inventory"]["assets"][0])
        )
        with self.assertRaises(ValueError):
            analyze(self.data)


if __name__ == "__main__":
    unittest.main()
