# Created by 11Hopem
# Copyright (c) 2026 11Hopem. All rights reserved.
# Licensed under 11Hopem Proprietary License.

import unittest
from pathlib import Path
import tempfile

from agent_memory_hub.config import AgentPaths, detect_installed_agents


class TestConfig(unittest.TestCase):
    """Test configuration paths and agent detection logic."""

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.fake_home = Path(self.temp_dir.name)
        self.paths = AgentPaths(home=self.fake_home)

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_paths_derivation(self):
        """Verify derived agent paths originate from home correctly."""
        self.assertEqual(self.paths.ai_context, self.fake_home / "ai-context")
        self.assertEqual(self.paths.okf_bundle, self.fake_home / "ai-context" / "hafiza")
        self.assertEqual(self.paths.claude_skills, self.fake_home / ".claude" / "skills")
        self.assertEqual(self.paths.codex_skills, self.fake_home / ".codex" / "skills")

    def test_detect_installed_agents_empty(self):
        """Verify empty environment reports not found."""
        agents = detect_installed_agents(self.paths)
        self.assertIn("claude-code", agents)
        self.assertIn("codex", agents)
        self.assertIn("antigravity", agents)
        self.assertFalse(agents["claude-code"]["installed"])
        self.assertFalse(agents["codex"]["installed"])

    def test_detect_installed_agents_with_mocks(self):
        """Verify mock agent directories are detected as installed."""
        (self.fake_home / ".claude").mkdir(parents=True)
        (self.fake_home / ".claude.json").write_text("{}")
        (self.fake_home / ".codex").mkdir(parents=True)
        (self.fake_home / ".codex" / "hooks.json").write_text("{}")

        agents = detect_installed_agents(self.paths)
        self.assertTrue(agents["claude-code"]["installed"])
        self.assertTrue(agents["claude-code"]["mcp_wired"])
        self.assertTrue(agents["codex"]["installed"])
        self.assertTrue(agents["codex"]["hooks_wired"])


if __name__ == "__main__":
    unittest.main()
