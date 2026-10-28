# Created by 11Hopem
# Copyright (c) 2026 11Hopem. All rights reserved.
# Licensed under 11Hopem Proprietary License.

"""
Configuration and paths for cross-agent memory management.
"""

import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Dict, Any


@dataclass
class AgentPaths:
    """Paths to supported AI coding agents' configs and stores."""
    home: Path = field(default_factory=Path.home)

    @property
    def ai_context(self) -> Path:
        return self.home / "ai-context"

    @property
    def okf_bundle(self) -> Path:
        return self.ai_context / "hafiza"

    @property
    def deja_binary(self) -> Path:
        local_bin = self.home / ".local" / "bin" / "deja"
        if local_bin.exists():
            return local_bin
        return Path("/usr/local/bin/deja")

    @property
    def deja_db(self) -> Path:
        return self.home / ".cache" / "deja" / "index.db"

    @property
    def claude_dir(self) -> Path:
        return self.home / ".claude"

    @property
    def claude_skills(self) -> Path:
        return self.claude_dir / "skills"

    @property
    def codex_dir(self) -> Path:
        return self.home / ".codex"

    @property
    def codex_skills(self) -> Path:
        return self.codex_dir / "skills"

    @property
    def shared_skills(self) -> Path:
        return self.home / ".agents" / "skills"

    @property
    def gemini_config(self) -> Path:
        return self.home / ".gemini" / "config"

    @property
    def cursor_config(self) -> Path:
        return self.home / ".cursor"

    @property
    def cline_config(self) -> Path:
        return self.home / ".cline"


def detect_installed_agents(paths: AgentPaths = None) -> Dict[str, Dict[str, Any]]:
    """Detect which AI coding agents are installed on the local system."""
    p = paths or AgentPaths()
    agents = {}

    # Claude Code
    claude_installed = p.claude_dir.exists()
    claude_mcp = (p.home / ".claude.json").exists()
    agents["claude-code"] = {
        "installed": claude_installed,
        "config_dir": str(p.claude_dir),
        "skills_dir": str(p.claude_skills),
        "mcp_wired": claude_mcp,
    }

    # Codex
    codex_installed = p.codex_dir.exists()
    codex_cfg = (p.codex_dir / "config.toml").exists()
    agents["codex"] = {
        "installed": codex_installed,
        "config_dir": str(p.codex_dir),
        "skills_dir": str(p.codex_skills),
        "hooks_wired": (p.codex_dir / "hooks.json").exists(),
    }

    # Antigravity / Gemini
    antigravity_installed = p.gemini_config.exists()
    agents["antigravity"] = {
        "installed": antigravity_installed,
        "config_dir": str(p.gemini_config),
        "mcp_wired": (p.gemini_config / "mcp_config.json").exists(),
    }

    # Cursor
    cursor_installed = p.cursor_config.exists()
    agents["cursor"] = {
        "installed": cursor_installed,
        "config_dir": str(p.cursor_config),
        "mcp_wired": (p.cursor_config / "mcp.json").exists(),
    }

    # Cline
    cline_installed = p.cline_config.exists()
    agents["cline"] = {
        "installed": cline_installed,
        "config_dir": str(p.cline_config),
    }

    return agents
