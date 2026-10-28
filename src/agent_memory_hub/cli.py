# Created by 11Hopem
# Copyright (c) 2026 11Hopem. All rights reserved.
# Licensed under 11Hopem Proprietary License.

"""
Command-line interface for the Cross-Agent Memory Hub.
"""

import sys
import argparse
from pathlib import Path

from .config import AgentPaths, detect_installed_agents
from .validator import validate_bundle
from .deja_bridge import DejaBridge
from .sync import MemorySynchronizer


def cmd_doctor(paths: AgentPaths) -> int:
    """Check the health and integration status of memory stores across all coding agents."""
    print("=" * 60)
    print("Cross-Agent Memory Hub — System Doctor")
    print("Created by 11Hopem (https://11hopem.com)")
    print("=" * 60)

    agents = detect_installed_agents(paths)
    for agent_name, status in agents.items():
        state = "INSTALLED" if status["installed"] else "NOT FOUND"
        print(f"\n[{agent_name.upper()}] Status: {state}")
        for k, v in status.items():
            if k != "installed":
                print(f"  - {k}: {v}")

    bridge = DejaBridge(paths.deja_binary)
    print("\n[DEJA-VU CORE ENGINE]")
    print(f"  - Binary exists: {bridge.is_available} ({bridge.binary})")
    print(f"  - Index database: {paths.deja_db.exists()} ({paths.deja_db})")

    okf_exists = paths.okf_bundle.exists()
    print("\n[OPEN KNOWLEDGE FORMAT (OKF v0.2) BUNDLE]")
    print(f"  - Bundle directory: {okf_exists} ({paths.okf_bundle})")
    if okf_exists:
        res = validate_bundle(paths.okf_bundle)
        status_str = "CONFORMANT" if res.is_conformant else "NON-CONFORMANT"
        print(f"  - Validation: {status_str} ({res.concepts_count} concepts, {res.error_count} errors, {res.warn_count} warnings)")

    print("\n" + "=" * 60)
    return 0


def cmd_sync(paths: AgentPaths) -> int:
    """Run cross-agent memory synchronization."""
    print("Starting cross-agent memory synchronization...")
    synchronizer = MemorySynchronizer(paths)
    report = synchronizer.run_full_sync()

    print(f"  ✓ Skills synchronized: {report.skills_synced}")
    print(f"  ✓ Claude memory notes collected: {report.claude_memories_synced}")
    print(f"  ✓ Deja-vu index warmed: {report.deja_indexed}")

    if report.errors:
        print("\nErrors encountered:")
        for err in report.errors:
            print(f"  ✗ {err}")
        return 1

    print("\n✓ Synchronization completed successfully.")
    return 0


def cmd_validate(bundle_dir: str, paths: AgentPaths) -> int:
    """Validate an OKF v0.2 knowledge bundle."""
    target = Path(bundle_dir) if bundle_dir else paths.okf_bundle
    print(f"Validating OKF v0.2 bundle at: {target}")

    res = validate_bundle(target)
    print(f"Concepts: {res.concepts_count} | Index files: {res.index_count} | Log files: {res.log_count}")

    for issue in res.issues:
        prefix = "✗ ERROR" if issue.level == "ERROR" else "! WARN"
        print(f"  {prefix} {issue.file_path}: {issue.message}")

    if res.is_conformant:
        print(f"\n✓ Bundle is fully conformant with OKF v0.2 ({res.warn_count} warning(s)).")
        return 0
    else:
        print(f"\n✗ Bundle is non-conformant ({res.error_count} error(s)).")
        return 1


def cmd_recall(query: str, paths: AgentPaths) -> int:
    """Query cross-agent sessions and notes using deja recall."""
    bridge = DejaBridge(paths.deja_binary)
    res = bridge.recall(query)
    if res["success"]:
        print(res["stdout"])
        return 0
    else:
        print(f"Recall failed: {res['stderr']}", file=sys.stderr)
        return res["exit_code"]


def cmd_fix(error_msg: str, paths: AgentPaths) -> int:
    """Query past resolutions for a given error message."""
    bridge = DejaBridge(paths.deja_binary)
    res = bridge.fix(error_msg)
    if res["success"]:
        print(res["stdout"])
        return 0
    else:
        print(f"Fix lookup failed: {res['stderr']}", file=sys.stderr)
        return res["exit_code"]


def cmd_stats(paths: AgentPaths) -> int:
    """Display overall session and store statistics."""
    bridge = DejaBridge(paths.deja_binary)
    res = bridge.stats()
    if res["success"]:
        print(res["stdout"])
        return 0
    else:
        print(f"Stats failed: {res['stderr']}", file=sys.stderr)
        return res["exit_code"]


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(
        prog="cross-agent-memory",
        description="Unified Cross-Agent Memory Hub & Synchronization Engine (11Hopem)",
    )
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    subparsers.add_parser("doctor", help="Check health and integration across agents")
    subparsers.add_parser("sync", help="Synchronize skills, notes, and index")

    val_parser = subparsers.add_parser("validate", help="Validate an OKF v0.2 bundle")
    val_parser.add_argument("path", nargs="?", default="", help="Path to the OKF bundle (default: ai-context/hafiza)")

    recall_parser = subparsers.add_parser("recall", help="Recall sessions by query")
    recall_parser.add_argument("query", help="Query string or identifier")

    fix_parser = subparsers.add_parser("fix", help="Find past fixes for an error message")
    fix_parser.add_argument("error", help="Error message string")

    subparsers.add_parser("stats", help="Display indexed session statistics")

    args = parser.parse_args(argv)
    paths = AgentPaths()

    if args.command == "doctor":
        return cmd_doctor(paths)
    elif args.command == "sync":
        return cmd_sync(paths)
    elif args.command == "validate":
        return cmd_validate(args.path, paths)
    elif args.command == "recall":
        return cmd_recall(args.query, paths)
    elif args.command == "fix":
        return cmd_fix(args.error, paths)
    elif args.command == "stats":
        return cmd_stats(paths)
    else:
        parser.print_help()
        return 0


if __name__ == "__main__":
    sys.exit(main())
