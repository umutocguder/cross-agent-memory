# Created by 11Hopem
# Copyright (c) 2026 11Hopem. All rights reserved.
# Licensed under 11Hopem Proprietary License.

"""
Deterministic validator for Open Knowledge Format (OKF v0.2) bundles.
Spec: GoogleCloudPlatform/open-knowledge-format (v0.2)
"""

import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Dict, Any, Optional


@dataclass
class ValidationIssue:
    file_path: str
    level: str  # 'ERROR' or 'WARN'
    message: str


@dataclass
class ValidationResult:
    bundle_path: str
    concepts_count: int = 0
    index_count: int = 0
    log_count: int = 0
    issues: List[ValidationIssue] = field(default_factory=list)

    @property
    def is_conformant(self) -> bool:
        return not any(i.level == "ERROR" for i in self.issues)

    @property
    def error_count(self) -> int:
        return sum(1 for i in self.issues if i.level == "ERROR")

    @property
    def warn_count(self) -> int:
        return sum(1 for i in self.issues if i.level == "WARN")


def parse_simple_frontmatter(text: str) -> Optional[Dict[str, Any]]:
    """Parse basic YAML frontmatter between initial triple dashes without third-party deps."""
    if not text.startswith("---"):
        return None
    parts = text.split("---", 2)
    if len(parts) < 3:
        return None

    raw_yaml = parts[1].strip()
    data = {}
    current_key = None

    for line in raw_yaml.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue

        if ":" in line and not line.startswith("-"):
            key, val = line.split(":", 1)
            key = key.strip()
            val = val.strip()
            current_key = key
            if val.startswith("[") and val.endswith("]"):
                items = [x.strip() for x in val[1:-1].split(",") if x.strip()]
                data[key] = items
            elif val.startswith("{") and val.endswith("}"):
                data[key] = val
            elif val.startswith('"') and val.endswith('"'):
                data[key] = val[1:-1]
            elif val.startswith("'") and val.endswith("'"):
                data[key] = val[1:-1]
            elif val:
                data[key] = val
            else:
                data[key] = []
        elif line.startswith("-") and current_key:
            item = line[1:].strip()
            if isinstance(data.get(current_key), list):
                data[current_key].append(item)
            else:
                data[current_key] = [item]

    return data


def validate_bundle(bundle_dir: Path) -> ValidationResult:
    """Validate a directory tree as an OKF v0.2 bundle."""
    bundle_path = Path(bundle_dir).resolve()
    result = ValidationResult(bundle_path=str(bundle_path))

    if not bundle_path.exists() or not bundle_path.is_dir():
        result.issues.append(
            ValidationIssue(file_path=str(bundle_path), level="ERROR", message="Path is not a directory")
        )
        return result

    for root, _, files in os.walk(bundle_path):
        for file in files:
            if not file.endswith(".md"):
                continue

            full_path = Path(root) / file
            rel_path = str(full_path.relative_to(bundle_path))

            if file == "index.md":
                result.index_count += 1
                continue
            elif file == "log.md":
                result.log_count += 1
                continue

            # Non-reserved markdown is a concept
            result.concepts_count += 1
            try:
                content = full_path.read_text(encoding="utf-8")
            except Exception as e:
                result.issues.append(
                    ValidationIssue(file_path=rel_path, level="ERROR", message=f"Failed to read file: {e}")
                )
                continue

            fm = parse_simple_frontmatter(content)
            if fm is None:
                result.issues.append(
                    ValidationIssue(
                        file_path=rel_path,
                        level="ERROR",
                        message="Missing or unparseable YAML frontmatter block",
                    )
                )
                continue

            if "type" not in fm or not fm["type"]:
                result.issues.append(
                    ValidationIssue(
                        file_path=rel_path,
                        level="ERROR",
                        message="Concept frontmatter missing required 'type' field",
                    )
                )

            if "title" not in fm:
                result.issues.append(
                    ValidationIssue(
                        file_path=rel_path,
                        level="WARN",
                        message="Concept frontmatter missing recommended 'title' field",
                    )
                )

            if "description" not in fm:
                result.issues.append(
                    ValidationIssue(
                        file_path=rel_path,
                        level="WARN",
                        message="Concept frontmatter missing recommended 'description' field",
                    )
                )

    return result
