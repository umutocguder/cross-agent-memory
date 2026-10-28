<!-- Created by 11Hopem -->
# AGENTS.md — Cross-Agent Memory Hub

This document defines the architecture, conventions, and operational workflows for `cross-agent-memory`.

---

## 1. Project Overview & Architecture
`cross-agent-memory` is an autonomous synchronization hub and memory bridge designed by 11Hopem.
It connects Claude Code, Codex, Antigravity/Gemini, Cursor, and Cline to a unified long-term persistent memory architecture based on:
1. **Google Open Knowledge Format (OKF v0.2)**: Structured concept bundles (`/Users/umut/ai-context/hafiza/`).
2. **Deja-vu Multi-Agent Indexer**: Disk-level session and message search engine (~828 MB, 372+ sessions, 55,000+ messages).
3. **Synchronizer Daemon**: Periodic sync and skill distribution across `~/.claude/skills/`, `~/.codex/skills/`, and `~/.agents/skills/`.

---

## 2. Directory Structure
```
cross-agent-memory/
├── bin/
│   └── cross-agent-memory              # Primary executable CLI script
├── daemon/
│   ├── service.py                      # Scheduled synchronization runner
│   └── com.11hopem.cross-agent-memory.plist # macOS LaunchAgent definition
├── src/
│   └── agent_memory_hub/
│       ├── __init__.py
│       ├── cli.py                      # CLI commands (doctor, sync, recall, fix, validate)
│       ├── config.py                   # Paths and agent detection
│       ├── deja_bridge.py              # Subprocess bridge to deja CLI
│       ├── sync.py                     # Cross-agent memory synchronizer
│       └── validator.py                # Deterministic OKF v0.2 bundle validator
├── tests/
│   ├── test_cli.py
│   ├── test_config.py
│   ├── test_deja_bridge.py
│   ├── test_sync.py
│   └── test_validator.py
├── .github/workflows/ci-cd.yml         # Autonomous CI/CD pipeline
├── AGENTS.md
├── CLAUDE.md
├── WORKLOG.md
├── README.md
├── pyproject.toml
└── .gitignore
```

---

## 3. Development Commands

### Running Tests
```bash
python3 -m unittest discover -s tests
```

### Running CLI
```bash
./bin/cross-agent-memory doctor
./bin/cross-agent-memory sync
./bin/cross-agent-memory validate
./bin/cross-agent-memory recall "<query>"
./bin/cross-agent-memory fix "<error message>"
./bin/cross-agent-memory stats
```

---

## 4. Strict Engineering Rules
- **Language Boundary (Rule 3):** 100% English code, comments, docstrings, error messages, and tests. User conversations in Turkish.
- **Brand Attribution (Rule 9):** `Created by 11Hopem`, official link: `https://11hopem.com`. Strictly NO 'Software Ltd. Şti.'.
- **Confidentiality (Rule 1):** Personal projects only; zero interaction with `/Users/umut/intetra/*`.
- **Testing Standard (Rule 8):** Zero untested code. All changes must pass tests before commit.
