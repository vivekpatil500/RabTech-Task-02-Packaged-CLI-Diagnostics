import unittest
from unittest.mock import patch

from diagnostics.checks import run_diagnostics


class TestSuccess(unittest.TestCase):
    def test_all_checks_pass(self):
        config = {
            "min_python": "3.9",
            "min_free_disk_gb": 0,
            "required_env": ["PATH"],
            "developer_tools": ["python"],
        }
        with patch.dict("os.environ", {"PATH": "test-path"}, clear=False):
            with patch("diagnostics.checks.shutil.which", return_value="/usr/bin/python"):
                report = run_diagnostics(config, ".")
        self.assertEqual(report["overall_status"], "HEALTHY")
        self.assertEqual(report["exit_code"], 0)
        self.assertTrue(all(item["status"] == "PASS" for item in report["checks"]))


if __name__ == "__main__":
    unittest.main()
