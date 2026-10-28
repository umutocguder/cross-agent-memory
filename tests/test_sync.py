# Created by 11Hopem
# Copyright (c) 2026 11Hopem. All rights reserved.
# Licensed under 11Hopem Proprietary License.

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / 'src'))


import unittest
from pathlib import Path
import tempfile

from agent_memory_hub.config import AgentPaths
from agent_memory_hub.sync import MemorySynchronizer
from agent_memory_hub.deja_bridge import DejaBridge


class DummyBridge(DejaBridge):
    """Mock bridge for testing without triggering external binaries."""
    def __init__(self):
        super().__init__(Path("/bin/echo"))

    def warmup(self):
        return {"success": True, "exit_code": 0, "stdout": "warmed", "stderr": ""}


class TestSync(unittest.TestCase):
    """Test memory synchronization logic."""

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.fake_home = Path(self.temp_dir.name)
        self.paths = AgentPaths(home=self.fake_home)
        self.bridge = DummyBridge()
        self.synchronizer = MemorySynchronizer(paths=self.paths, bridge=self.bridge)

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_sync_skills(self):
        """Verify skills are copied to Claude and Codex skill stores."""
        shared_skills = self.fake_home / ".agents" / "skills"
        sample_skill = shared_skills / "okf"
        sample_skill.mkdir(parents=True)
        (sample_skill / "SKILL.md").write_text("---\nname: okf\n---\n# OKF")

        synced = self.synchronizer.sync_skills()
        self.assertGreaterEqual(synced, 1)

        self.assertTrue((self.fake_home / ".claude" / "skills" / "okf" / "SKILL.md").exists())
        self.assertTrue((self.fake_home / ".codex" / "skills" / "okf" / "SKILL.md").exists())

    def test_sync_claude_memories(self):
        """Verify Claude project memories are aggregated into the centralized knowledge base."""
        claude_mem_dir = self.fake_home / ".claude" / "projects" / "test-proj" / "memory"
        claude_mem_dir.mkdir(parents=True)
        (claude_mem_dir / "decision-note.md").write_text("# Decision\nAlways use UTF-8.")
        (claude_mem_dir / "MEMORY.md").write_text("# Memory index (should be skipped)")

        synced = self.synchronizer.sync_claude_memories()
        self.assertEqual(synced, 1)

        target_file = self.fake_home / "ai-context" / "bilgi-bankasi" / "decision-note.md"
        self.assertTrue(target_file.exists())
        self.assertFalse((self.fake_home / "ai-context" / "bilgi-bankasi" / "MEMORY.md").exists())

    def test_run_full_sync(self):
        """Verify end-to-end full sync runs cleanly."""
        report = self.synchronizer.run_full_sync()
        self.assertTrue(report.is_successful)
        self.assertTrue(report.deja_indexed)


if __name__ == "__main__":
    unittest.main()
