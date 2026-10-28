# Created by 11Hopem
# Copyright (c) 2026 11Hopem. All rights reserved.
# Licensed under 11Hopem Proprietary License.

"""
Cross-agent memory synchronizer.
Syncs memory files, skills, and triggers index updates across Claude Code, Codex, and Antigravity.
"""

import shutil
from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Dict, Any

from .config import AgentPaths
from .deja_bridge import DejaBridge


@dataclass
class SyncReport:
    skills_synced: int = 0
    claude_memories_synced: int = 0
    deja_indexed: bool = False
    errors: List[str] = field(default_factory=list)

    @property
    def is_successful(self) -> bool:
        return len(self.errors) == 0


class MemorySynchronizer:
    """Orchestrates multi-agent memory propagation and index warming."""

    def __init__(self, paths: AgentPaths = None, bridge: DejaBridge = None):
        self.paths = paths or AgentPaths()
        self.bridge = bridge or DejaBridge(self.paths.deja_binary)

    def sync_skills(self) -> int:
        """Sync core memory skills from shared repository to Claude and Codex skill stores."""
        synced_count = 0
        memory_skills = [
            "okf",
            "okf-backfill",
            "okf-validate",
            "okf-visualize",
            "mem0",
            "mem0-cli",
            "mem0-integrate",
            "mem0-remember",
            "mem0-search",
            "mem0-status",
            "agent-memory",
            "hindsight-architect",
            "hindsight-local",
            "claude-mem-timeline",
            "claude-mem-digests",
            "deja-search",
            "deja-history",
        ]

        target_dirs = [self.paths.claude_skills, self.paths.codex_skills]

        for target_dir in target_dirs:
            target_dir.mkdir(parents=True, exist_ok=True)
            for skill_name in memory_skills:
                source = self.paths.shared_skills / skill_name
                if source.exists() and source.is_dir():
                    dest = target_dir / skill_name
                    if not dest.exists():
                        shutil.copytree(source, dest, dirs_exist_ok=True)
                        synced_count += 1
                    else:
                        # Check and update if source is newer
                        src_skill = source / "SKILL.md"
                        dst_skill = dest / "SKILL.md"
                        if src_skill.exists() and dst_skill.exists():
                            if src_skill.stat().st_mtime > dst_skill.stat().st_mtime:
                                shutil.copytree(source, dest, dirs_exist_ok=True)
                                synced_count += 1

        return synced_count

    def sync_claude_memories(self) -> int:
        """Collect memory notes authored in Claude Code projects into the shared knowledge base."""
        target_dir = self.paths.ai_context / "bilgi-bankasi"
        target_dir.mkdir(parents=True, exist_ok=True)
        synced_count = 0

        projects_dir = self.paths.claude_dir / "projects"
        if not projects_dir.exists():
            return 0

        for project_folder in projects_dir.iterdir():
            if not project_folder.is_dir():
                continue
            memory_dir = project_folder / "memory"
            if not memory_dir.exists() or not memory_dir.is_dir():
                continue

            for md_file in memory_dir.glob("*.md"):
                if md_file.name == "MEMORY.md":
                    continue
                dest_file = target_dir / md_file.name
                if not dest_file.exists() or md_file.stat().st_mtime > dest_file.stat().st_mtime:
                    shutil.copy2(md_file, dest_file)
                    synced_count += 1

        return synced_count

    def refresh_deja_index(self) -> bool:
        """Trigger deja warmup to index new sessions across Claude, Codex, Antigravity, and Cursor."""
        res = self.bridge.warmup()
        return res["success"]

    def run_full_sync(self) -> SyncReport:
        """Run all memory synchronization steps and compile the report."""
        report = SyncReport()

        try:
            report.skills_synced = self.sync_skills()
        except Exception as e:
            report.errors.append(f"Skills sync error: {e}")

        try:
            report.claude_memories_synced = self.sync_claude_memories()
        except Exception as e:
            report.errors.append(f"Claude memory sync error: {e}")

        try:
            report.deja_indexed = self.refresh_deja_index()
        except Exception as e:
            report.errors.append(f"Deja index refresh error: {e}")

        return report
