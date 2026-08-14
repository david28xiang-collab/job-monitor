"""Shared project paths.

Keeping paths here makes commands work regardless of the current directory.
"""

from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
CONFIG_FILE = PROJECT_ROOT / "config" / "companies.yaml"
DATA_DIR = PROJECT_ROOT / "data" / "current"
BASELINE_DIR = PROJECT_ROOT / "data" / "baseline"
