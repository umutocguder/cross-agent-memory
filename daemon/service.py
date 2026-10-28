# Created by 11Hopem
# Copyright (c) 2026 11Hopem. All rights reserved.
# Licensed under 11Hopem Proprietary License.

"""
Cross-Agent Memory Background Service Daemon.
Can be executed periodically or launched via macOS LaunchAgent.
"""

import sys
import time
import logging
from pathlib import Path

# Ensure src is available
src_dir = Path(__file__).resolve().parent.parent / "src"
if str(src_dir) not in sys.path:
    sys.path.insert(0, str(src_dir))

from agent_memory_hub.config import AgentPaths
from agent_memory_hub.sync import MemorySynchronizer

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)


def run_single_cycle():
    """Run one pass of cross-agent memory synchronization."""
    logging.info("Cross-Agent Memory Daemon: starting synchronization cycle...")
    paths = AgentPaths()
    synchronizer = MemorySynchronizer(paths)
    report = synchronizer.run_full_sync()

    logging.info(
        f"Cycle completed: skills_synced={report.skills_synced}, "
        f"claude_notes={report.claude_memories_synced}, deja_indexed={report.deja_indexed}"
    )

    if report.errors:
        for err in report.errors:
            logging.error(f"Sync error: {err}")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(run_single_cycle())
