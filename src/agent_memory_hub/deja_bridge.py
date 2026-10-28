# Created by 11Hopem
# Copyright (c) 2026 11Hopem. All rights reserved.
# Licensed under 11Hopem Proprietary License.

"""
Subprocess bridge to the deja-vu CLI memory engine.
"""

import os
import subprocess
import shutil
from typing import Dict, Any, Optional
from pathlib import Path


class DejaBridge:
    """Wrapper around the deja CLI binary for cross-agent memory retrieval."""

    def __init__(self, binary_path: Optional[Path] = None):
        if binary_path is not None:
            self.binary = str(binary_path)
        else:
            resolved = shutil.which("deja")
            self.binary = resolved or "/Users/umut/.local/bin/deja"

    @property
    def is_available(self) -> bool:
        p = Path(self.binary)
        return p.exists() and os.access(p, os.X_OK)

    def _run_cmd(self, *args) -> Dict[str, Any]:
        """Execute a deja subcommand and return stdout, stderr, and exit_code."""
        if not self.is_available:
            return {
                "success": False,
                "exit_code": -1,
                "stdout": "",
                "stderr": "deja binary not found or not executable",
            }
        try:
            cmd = [self.binary] + list(args)
            proc = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=15,
                check=False,
            )
            return {
                "success": proc.returncode == 0,
                "exit_code": proc.returncode,
                "stdout": proc.stdout.strip(),
                "stderr": proc.stderr.strip(),
            }
        except subprocess.TimeoutExpired:
            return {
                "success": False,
                "exit_code": 124,
                "stdout": "",
                "stderr": "deja command timed out after 15s",
            }
        except Exception as e:
            return {
                "success": False,
                "exit_code": -1,
                "stdout": "",
                "stderr": str(e),
            }

    def warmup(self) -> Dict[str, Any]:
        """Re-index all agent sessions from disk into the cache database."""
        return self._run_cmd("warmup")

    def recall(self, query: str, limit: int = 5) -> Dict[str, Any]:
        """Recall relevant sessions and notes for a query."""
        return self._run_cmd("recall", query, f"--limit={limit}")

    def fix(self, error_message: str) -> Dict[str, Any]:
        """Find past commands that resolved the given error message."""
        return self._run_cmd("fix", error_message)

    def blame(self, file_path: str) -> Dict[str, Any]:
        """Find prior agent sessions that modified the file."""
        return self._run_cmd("blame", file_path)

    def how(self, action: str) -> Dict[str, Any]:
        """Find the real commands previously executed for this action."""
        return self._run_cmd("how", action)

    def stats(self) -> Dict[str, Any]:
        """Retrieve total indexed sessions, messages, and store sizes."""
        return self._run_cmd("sources")
