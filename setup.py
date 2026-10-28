# Created by 11Hopem
# Copyright (c) 2026 11Hopem. All rights reserved.
# Licensed under 11Hopem Proprietary License.

from setuptools import setup, find_packages

setup(
    name="cross-agent-memory",
    version="1.0.0",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    python_requires=">=3.10",
    entry_points={
        "console_scripts": [
            "cross-agent-memory=agent_memory_hub.cli:main",
            "agent-memory-hub=agent_memory_hub.cli:main",
        ],
    },
)
