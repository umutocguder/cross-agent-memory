# Created by 11Hopem
# Copyright (c) 2026 11Hopem. All rights reserved.
# Licensed under 11Hopem Proprietary License.

import unittest
from pathlib import Path
import tempfile

from agent_memory_hub.validator import validate_bundle, parse_simple_frontmatter


class TestValidator(unittest.TestCase):
    """Test OKF v0.2 bundle validation logic."""

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.bundle_path = Path(self.temp_dir.name)

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_parse_simple_frontmatter(self):
        """Verify frontmatter parsing without external YAML dependencies."""
        raw = """---
type: Concept
title: "Test Concept"
description: "A valid test concept"
tags: [alpha, beta, gamma]
---
# Content Body
"""
        fm = parse_simple_frontmatter(raw)
        self.assertIsNotNone(fm)
        self.assertEqual(fm["type"], "Concept")
        self.assertEqual(fm["title"], "Test Concept")
        self.assertEqual(fm["description"], "A valid test concept")
        self.assertEqual(fm["tags"], ["alpha", "beta", "gamma"])

    def test_validate_empty_directory(self):
        """Verify directory with no concepts passes as conformant with 0 concepts."""
        result = validate_bundle(self.bundle_path)
        self.assertTrue(result.is_conformant)
        self.assertEqual(result.concepts_count, 0)

    def test_validate_valid_okf_bundle(self):
        """Verify compliant OKF concepts report conformant with 0 errors."""
        (self.bundle_path / "index.md").write_text("# Bundle Index")
        (self.bundle_path / "log.md").write_text("# Bundle Log")

        concept = """---
type: Guideline
title: "Coding Standard"
description: "English only code standard"
tags: [standard, code]
---
# Guidelines
Rule 1: Always write tests.
"""
        (self.bundle_path / "coding-standard.md").write_text(concept)

        result = validate_bundle(self.bundle_path)
        self.assertTrue(result.is_conformant)
        self.assertEqual(result.concepts_count, 1)
        self.assertEqual(result.index_count, 1)
        self.assertEqual(result.log_count, 1)
        self.assertEqual(result.error_count, 0)

    def test_validate_invalid_okf_concept(self):
        """Verify concept without frontmatter reports non-conformant."""
        (self.bundle_path / "broken.md").write_text("# Just regular markdown without frontmatter")

        result = validate_bundle(self.bundle_path)
        self.assertFalse(result.is_conformant)
        self.assertEqual(result.error_count, 1)


if __name__ == "__main__":
    unittest.main()
