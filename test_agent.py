import copy
import json
from pathlib import Path
import unittest

from agent import analyze


class AgentTests(unittest.TestCase):
    def setUp(self):
        self.data = json.loads(Path(__file__).with_name("example.json").read_text())

    def test_conflict_and_staleness_remain_visible(self):
        result = analyze(self.data)["findings"]
        self.assertEqual(result[0]["normalized_value"], "demo.example")
        self.assertEqual(result[0]["status"], "conflicting_reputation")
        self.assertEqual(result[1]["status"], "unknown")
        self.assertEqual(result[1]["stale_evidence_ids"], ["rep-3"])

    def test_no_sources_is_unknown(self):
        self.data["snapshots"] = []
        self.assertEqual(analyze(self.data)["findings"][0]["status"], "unknown")

    def test_future_reputation_is_rejected(self):
        self.data["snapshots"][0]["observed_at"] = "2027-01-01T00:00:00Z"
        with self.assertRaises(ValueError):
            analyze(self.data)

    def test_latest_provider_observation_supersedes_old_verdict(self):
        self.data["snapshots"] = [self.data["snapshots"][0]]
        newer = copy.deepcopy(self.data["snapshots"][0])
        newer.update(id="newer", verdict="benign", observed_at="2026-01-14T12:00:00.1Z")
        self.data["snapshots"].append(newer)
        row = analyze(self.data)["findings"][0]
        self.assertEqual(row["status"], "no_malicious_verdict_in_current_snapshots")
        self.assertEqual(row["active_evidence_ids"], ["newer"])

    def test_tied_provider_disagreement_is_retained(self):
        self.data["snapshots"][1]["provider"] = "Synthetic Provider A"
        self.assertEqual(
            analyze(self.data)["findings"][0]["status"], "conflicting_reputation"
        )

    def test_url_is_not_accepted_as_domain(self):
        self.data["indicators"][0]["value"] = "https://demo.example/path"
        with self.assertRaises(ValueError):
            analyze(self.data)

    def test_ipv6_normalization_matches(self):
        self.data["indicators"] = [{"id": "v6", "type": "ip", "value": "2001:0db8::1"}]
        self.data["snapshots"] = [
            {
                "id": "r-v6",
                "type": "ip",
                "value": "2001:db8::1",
                "provider": "Synthetic",
                "observed_at": "2026-01-14T00:00:00Z",
                "verdict": "malicious",
            }
        ]
        self.assertEqual(
            analyze(self.data)["findings"][0]["status"], "reported_malicious"
        )

    def test_malformed_hash_is_rejected(self):
        self.data["indicators"] = [
            {"id": "hash", "type": "sha256", "value": "not-a-hash"}
        ]
        with self.assertRaises(ValueError):
            analyze(self.data)


if __name__ == "__main__":
    unittest.main()
