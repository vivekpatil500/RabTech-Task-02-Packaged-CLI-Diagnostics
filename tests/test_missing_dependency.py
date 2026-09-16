import unittest
from unittest.mock import patch

from diagnostics.checks import check_developer_tools


class TestMissingDependency(unittest.TestCase):
    def test_missing_developer_tool_is_reported(self):
        def fake_which(command):
            return None if command == "git" else "/usr/bin/" + command

        with patch("diagnostics.checks.shutil.which", side_effect=fake_which):
            result = check_developer_tools(["python", "git"])

        self.assertEqual(result["status"], "FAIL")
        self.assertIn("git", result["value"]["missing"])


if __name__ == "__main__":
    unittest.main()
