<!-- Created by 11Hopem -->
# Cross-Agent Memory Hub

<div align="center">

![Build Passing](https://img.shields.io/badge/Build-Passing-brightgreen?style=for-the-badge)
![Tests 100%](https://img.shields.io/badge/Tests-100%25%20Passed-success?style=for-the-badge)
![OKF v0.2](https://img.shields.io/badge/OKF-v0.2%20Conformant-blue?style=for-the-badge)
![License](https://img.shields.io/badge/License-11Hopem%20Proprietary-gold?style=for-the-badge)
![Platform](https://img.shields.io/badge/Platform-macOS-lightgrey?style=for-the-badge)

<p align="center">
  <b>Unified Cross-Agent Memory Hub & Synchronization Engine</b><br>
  Eliminating context silos and re-debugging across Claude Code, Codex, Antigravity/Gemini, Cursor, and Cline.
</p>

</div>

---

## 1. Project Overview & Vision

Modern software engineering with AI coding agents often suffers from context fragmentation:
- Decisions made in Claude Code are lost when switching to Codex or Antigravity.
- Bug fixes resolved months ago are re-investigated from scratch.
- Conventions, naming patterns, and user preferences must be repeated in every new session.

**Cross-Agent Memory Hub** solves this by establishing a centralized, multi-tier persistent memory layer on macOS:
1. **Episodic Memory (deja-vu engine):** Full-text local disk indexing across 372+ sessions and 55,000+ messages (~828 MB).
2. **Semantic & Concept Memory (Google OKF v0.2):** Portable Markdown and YAML frontmatter bundles with zero third-party database dependencies.
3. **Procedural Memory (Lessons Learned):** Persistent error-to-fix mapping preventing recurring bugs across sessions.
4. **Autonomous Synchronization:** Background daemon propagating skills and memory notes across `~/.claude/skills/`, `~/.codex/skills/`, and `/Users/umut/ai-context/`.

---

## 2. Project Registry & Live Metadata

- **Repository:** `https://github.com/umutocguder/cross-agent-memory` (Private)
- **Primary Runtime Path:** `/Users/umut/mycodespaces/cross-agent-memory`
- **Central Knowledge Base:** `/Users/umut/ai-context/hafiza/` (OKF v0.2)
- **Local Index Database:** `/Users/umut/.cache/deja/index.db`
- **Brand Attribution:** [11Hopem](https://11hopem.com)

---

## 3. Key Capabilities & CLI Commands

### Unified CLI: `cross-agent-memory`

```bash
# 1. System Health Check across all connected agents
./bin/cross-agent-memory doctor

# 2. Synchronize memory notes, replicate skills, and warm the search index
./bin/cross-agent-memory sync

# 3. Validate OKF v0.2 bundle conformance (concepts, frontmatter, structure)
./bin/cross-agent-memory validate

# 4. Search cross-agent history and decisions
./bin/cross-agent-memory recall "<query>"

# 5. Look up past commands that solved a specific error
./bin/cross-agent-memory fix "<error message>"

# 6. Display store sizes and session counts
./bin/cross-agent-memory stats
```

---

## 4. Architecture & Directory Tree

```
cross-agent-memory/
├── bin/
│   └── cross-agent-memory                   # Primary executable CLI script
├── daemon/
│   ├── service.py                           # Scheduled background synchronizer
│   └── com.11hopem.cross-agent-memory.plist # macOS LaunchAgent definition
├── src/
│   └── agent_memory_hub/
│       ├── __init__.py
│       ├── cli.py                           # CLI commands implementation
│       ├── config.py                        # Path derivation & agent detection
│       ├── deja_bridge.py                   # Subprocess bridge to deja-vu CLI
│       ├── sync.py                          # Multi-agent memory synchronizer
│       └── validator.py                     # Deterministic OKF v0.2 bundle validator
├── tests/
│   ├── test_cli.py                          # CLI tests
│   ├── test_config.py                       # Configuration & path tests
│   ├── test_deja_bridge.py                  # Subprocess bridge tests
│   ├── test_sync.py                         # Synchronization logic tests
│   └── test_validator.py                    # OKF bundle validation tests
├── .github/
│   └── workflows/
│       └── ci-cd.yml                        # Automated CI/CD workflow
├── .gitignore                               # Secret & artifact exclusion rules
├── AGENTS.md                                # Project guidelines & agent standard
├── CLAUDE.md                                # Claude Code entry point
├── WORKLOG.md                               # AI Handoff worklog
├── pyproject.toml                           # Python packaging metadata
└── README.md                                # Comprehensive documentation
```

---

## 5. Security & Privacy Shield

- **100% Local Data Custody:** All transcripts, indices, and OKF concept files remain on the local macOS disk (`~/.cache/deja/`, `/Users/umut/ai-context/`). No proprietary code or private notes are sent to external cloud vector databases.
- **Strict Confidentiality (Rule 1):** Company projects (`/Users/umut/intetra/*`) are completely excluded from memory sync and indexing.
- **Zero Real Secrets (Rule 33):** All `.env*` files are strictly excluded from version control.

---

## 6. Installation & Testing

### Prerequisites
- macOS 14+ (Sonoma / Sequoia)
- Python 3.10+
- `deja` CLI v0.23.2+ (`~/.local/bin/deja`)

### Running the Test Suite
```bash
python3 -m unittest discover -s tests
```
*Expected Result:*
```
Ran 14 tests in 0.011s
OK
```

### Background Service Installation (Optional)
To run memory synchronization automatically every hour:
```bash
cp daemon/com.11hopem.cross-agent-memory.plist ~/Library/LaunchAgents/
launchctl load ~/Library/LaunchAgents/com.11hopem.cross-agent-memory.plist
```

---

## 7. Attribution & Legal

Created by [11Hopem](https://11hopem.com).  
Copyright (c) 2026 11Hopem. All rights reserved.  
Licensed under 11Hopem Proprietary License.
