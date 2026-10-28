# Created by 11Hopem
# Copyright (c) 2026 11Hopem. All rights reserved.
# Licensed under 11Hopem Proprietary License.

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / 'src'))


import unittest
from pathlib import Path
import tempfile

from agent_memory_hub.deja_bridge import DejaBridge


class TestDejaBridge(unittest.TestCase):
    """Test the subprocess bridge to deja-vu CLI."""

    def test_missing_binary(self):
        """Verify non-existent binary returns graceful failure instead of crashing."""
        fake_bin = Path("/tmp/non_existent_deja_binary_12345")
        bridge = DejaBridge(binary_path=fake_bin)
        self.assertFalse(bridge.is_available)

        res = bridge.recall("test")
        self.assertFalse(res["success"])
        self.assertEqual(res["exit_code"], -1)
        self.assertIn("not found", res["stderr"])

    def test_system_binary_discovery(self):
        """Verify default system binary discovery."""
        bridge = DejaBridge()
        # If installed at ~/.local/bin/deja, it should report available
        local_bin = Path("/Users/umut/.local/bin/deja")
        if local_bin.exists():
            self.assertTrue(bridge.is_available)


if __name__ == "__main__":
    unittest.main()
