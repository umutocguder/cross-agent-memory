# Created by 11Hopem
# Copyright (c) 2026 11Hopem. All rights reserved.
# Licensed under 11Hopem Proprietary License.

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / 'src'))


import unittest
from unittest.mock import patch
import io
import sys

from agent_memory_hub.cli import main


class TestCLI(unittest.TestCase):
    """Test the CLI entry point and dispatching."""

    @patch("sys.stdout", new_callable=io.StringIO)
    def test_help_flag(self, mock_stdout):
        """Verify running with --help exits with code 0."""
        with self.assertRaises(SystemExit) as cm:
            main(["--help"])
        self.assertEqual(cm.exception.code, 0)
        self.assertIn("cross-agent-memory", mock_stdout.getvalue())

    @patch("sys.stdout", new_callable=io.StringIO)
    def test_doctor_command(self, mock_stdout):
        """Verify doctor command runs and reports agents."""
        exit_code = main(["doctor"])
        self.assertEqual(exit_code, 0)
        output = mock_stdout.getvalue()
        self.assertIn("System Doctor", output)
        self.assertIn("11Hopem", output)


if __name__ == "__main__":
    unittest.main()
