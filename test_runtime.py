"""Safety and command-line contract tests shared by the example projects."""

import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from runtime import instant, load, markdown, number

ROOT = Path(__file__).resolve().parent


class RuntimeTests(unittest.TestCase):
    def test_example_cli_emits_valid_json(self):
        result = subprocess.run(
            [
                sys.executable,
                str(ROOT / "agent.py"),
                str(ROOT / "example.json"),
                "--format",
                "json",
            ],
            capture_output=True,
            text=True,
            check=True,
        )
        self.assertEqual(json.loads(result.stdout)["schema_version"], "1.0")
        self.assertEqual(result.stderr, "")

    def test_rejects_non_object_input_with_exit_two(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "input.json"
            path.write_text("[]")
            result = subprocess.run(
                [sys.executable, str(ROOT / "agent.py"), str(path)],
                capture_output=True,
                text=True,
            )
        self.assertEqual(result.returncode, 2)
        self.assertEqual(result.stdout, "")
        self.assertNotIn("Traceback", result.stderr)

    def test_duplicate_json_keys_are_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "input.json"
            path.write_text('{"scope": "one", "scope": "two"}')
            with self.assertRaises(ValueError):
                load(path)

    def test_input_size_is_bounded(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "input.json"
            path.write_bytes(b" " * (2 * 1024 * 1024 + 1))
            with self.assertRaises(ValueError):
                load(path)

    def test_naive_time_is_rejected(self):
        with self.assertRaises(ValueError):
            instant("2026-01-01T12:00:00", "time")

    def test_offsets_represent_the_same_instant(self):
        self.assertEqual(
            instant("2026-01-01T12:00:00+02:00", "time"),
            instant("2026-01-01T10:00:00Z", "time"),
        )

    def test_non_finite_and_boolean_numbers_are_rejected(self):
        for value in (float("nan"), float("inf"), True, -1):
            with self.subTest(value=value), self.assertRaises(ValueError):
                number(value, "value")

    def test_untrusted_text_cannot_create_html_or_links(self):
        value = "<img src=x> [click](https://example.org)\n# forged heading"
        output = markdown(
            {
                "agent": "Example",
                "summary": {"note": value},
                "findings": [],
                "limitations": [],
                "next_steps": [],
            }
        )
        self.assertNotIn("<img", output)
        self.assertNotIn("[click]", output)
        self.assertNotIn("\n# forged", output)


if __name__ == "__main__":
    unittest.main()
