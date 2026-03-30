"""
Template version checking and comparison logic.

Compares local project template version against the installed framework's
template version to detect when updates are available.
"""

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

from clingy.core.discovery import read_clingy_marker


@dataclass
class TemplateUpdateInfo:
    """Information about an available template update."""

    template_name: str
    local_version: str
    framework_version: str


def _parse_semver(version_str: str) -> Optional[tuple]:
    """
    Parse a semantic version string into a comparable tuple.

    Args:
        version_str: Version string (e.g., "1.1.0")

    Returns:
        Tuple of integers (e.g., (1, 1, 0)), or None if parsing fails
    """
    try:
        parts = version_str.split(".")
        return tuple(int(x) for x in parts)
    except (ValueError, AttributeError):
        return None


def check_template_version(
    project_root: Path,
) -> Optional[TemplateUpdateInfo]:
    """
    Check if a template update is available.

    Compares the local project's template version against the installed
    framework's template version. Returns update info if framework version
    is newer, None otherwise.

    Args:
        project_root: Path to project root directory

    Returns:
        TemplateUpdateInfo if update is available, None otherwise
    """
    # Read local .clingy marker
    marker_data = read_clingy_marker(project_root)
    if marker_data is None:
        return None

    # Extract template name and local version
    template_name = marker_data.get("template")
    local_version = marker_data.get("template_version")

    if template_name is None or local_version is None:
        return None

    # Resolve framework template path
    framework_template_path = Path(__file__).parent.parent / "templates" / template_name / ".clingy"

    if not framework_template_path.is_file():
        return None

    # Read framework template's .clingy
    try:
        with open(framework_template_path, "r") as f:
            framework_marker = json.load(f)
    except (json.JSONDecodeError, IOError):
        return None

    framework_version = framework_marker.get("template_version")
    if framework_version is None:
        return None

    # Compare versions using tuple-based semver
    local_tuple = _parse_semver(local_version)
    framework_tuple = _parse_semver(framework_version)

    if local_tuple is None or framework_tuple is None:
        return None

    if framework_tuple > local_tuple:
        return TemplateUpdateInfo(
            template_name=template_name,
            local_version=local_version,
            framework_version=framework_version,
        )

    return None
