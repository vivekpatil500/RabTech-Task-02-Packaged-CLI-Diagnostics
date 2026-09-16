import json
import tempfile
import unittest
from pathlib import Path

from diagnostics.config import ConfigError, load_config


class TestMalformedConfig(unittest.TestCase):
    def test_malformed_json_raises_config_error(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "broken.json"
            path.write_text('{"min_python": ', encoding="utf-8")
            with self.assertRaises(ConfigError):
                load_config(str(path))


if __name__ == "__main__":
    unittest.main()
