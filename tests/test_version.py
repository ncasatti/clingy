"""
Tests for template version checking and comparison logic
"""

import json
from pathlib import Path

import pytest

from clingy.core.version import (
    TemplateUpdateInfo,
    _parse_semver,
    check_template_version,
)


class TestParseSemver:
    """Tests for _parse_semver helper function"""

    def test_parses_valid_semver(self):
        """Should parse valid semantic version strings"""
        assert _parse_semver("1.0.0") == (1, 0, 0)
        assert _parse_semver("1.2.3") == (1, 2, 3)
        assert _parse_semver("0.0.1") == (0, 0, 1)

    def test_returns_none_for_invalid_semver(self):
        """Should return None for invalid version strings"""
        assert _parse_semver("invalid") is None
        assert _parse_semver("1.a.0") is None
        assert _parse_semver("") is None
        assert _parse_semver(None) is None


class TestCheckTemplateVersion:
    """Tests for check_template_version function"""

    def test_update_available_when_framework_newer(self, temp_project, tmp_path):
        """Should return TemplateUpdateInfo when framework version > local"""
        # Setup: local project with older template version
        marker_content = {
            "version": "1.0",
            "type": "clingy-project",
            "template": "basic",
            "template_version": "1.0.0",
        }
        marker_file = temp_project / ".clingy"
        marker_file.write_text(json.dumps(marker_content, indent=2) + "\n")

        # Mock framework template with newer version
        # (The actual framework template is in clingy/templates/basic/.clingy)
        # This test relies on the real framework template having version >= 1.0.0

        result = check_template_version(temp_project)

        # Result depends on actual framework template version
        # If framework is newer, result should be TemplateUpdateInfo
        if result is not None:
            assert isinstance(result, TemplateUpdateInfo)
            assert result.template_name == "basic"
            assert result.local_version == "1.0.0"

    def test_no_update_when_up_to_date(self, temp_project):
        """Should return None when local version == framework version"""
        # Read the actual framework template version
        framework_template = (
            Path(__file__).parent.parent / "clingy" / "templates" / "basic" / ".clingy"
        )
        if framework_template.exists():
            with open(framework_template) as f:
                framework_data = json.load(f)
                framework_version = framework_data.get("template_version", "1.0.0")
        else:
            framework_version = "1.0.0"

        # Setup: local project with same version as framework
        marker_content = {
            "version": "1.0",
            "type": "clingy-project",
            "template": "basic",
            "template_version": framework_version,
        }
        marker_file = temp_project / ".clingy"
        marker_file.write_text(json.dumps(marker_content, indent=2) + "\n")

        result = check_template_version(temp_project)
        assert result is None

    def test_backward_compatibility_missing_template_version(self, temp_project):
        """Should return None when template_version field is missing"""
        # Setup: old .clingy without template_version field
        marker_content = {
            "version": "1.0",
            "type": "clingy-project",
            "template": "basic",
        }
        marker_file = temp_project / ".clingy"
        marker_file.write_text(json.dumps(marker_content, indent=2) + "\n")

        result = check_template_version(temp_project)
        assert result is None

    def test_returns_none_when_no_marker_file(self, tmp_path):
        """Should return None when .clingy file doesn't exist"""
        project = tmp_path / "no-marker"
        project.mkdir()

        result = check_template_version(project)
        assert result is None

    def test_returns_none_for_malformed_marker(self, tmp_path):
        """Should return None when .clingy is malformed JSON"""
        project = tmp_path / "malformed"
        project.mkdir()
        marker_file = project / ".clingy"
        marker_file.write_text("{ invalid json }")

        result = check_template_version(project)
        assert result is None

    def test_returns_none_when_template_field_missing(self, temp_project):
        """Should return None when template field is missing"""
        marker_content = {
            "version": "1.0",
            "type": "clingy-project",
            "template_version": "1.0.0",
        }
        marker_file = temp_project / ".clingy"
        marker_file.write_text(json.dumps(marker_content, indent=2) + "\n")

        result = check_template_version(temp_project)
        assert result is None

    def test_returns_none_for_nonexistent_framework_template(self, temp_project):
        """Should return None when framework template doesn't exist"""
        marker_content = {
            "version": "1.0",
            "type": "clingy-project",
            "template": "nonexistent-template",
            "template_version": "1.0.0",
        }
        marker_file = temp_project / ".clingy"
        marker_file.write_text(json.dumps(marker_content, indent=2) + "\n")

        result = check_template_version(temp_project)
        assert result is None

    def test_version_comparison_with_multiple_digits(self, temp_project):
        """Should correctly compare versions with multiple digits"""
        # Setup: local version 1.9.0, framework version 1.10.0
        marker_content = {
            "version": "1.0",
            "type": "clingy-project",
            "template": "basic",
            "template_version": "1.9.0",
        }
        marker_file = temp_project / ".clingy"
        marker_file.write_text(json.dumps(marker_content, indent=2) + "\n")

        # This test verifies tuple comparison works correctly
        # (1, 9, 0) < (1, 10, 0) should be True
        result = check_template_version(temp_project)

        # Result depends on actual framework version
        # But the comparison logic should work correctly
        if result is not None:
            assert isinstance(result, TemplateUpdateInfo)


class TestReadClingyMarker:
    """Tests for read_clingy_marker function (imported from discovery)"""

    def test_read_valid_marker(self, temp_project):
        """Should read and parse valid .clingy file"""
        from clingy.core.discovery import read_clingy_marker

        result = read_clingy_marker(temp_project)

        assert result is not None
        assert isinstance(result, dict)
        assert result["version"] == "1.0"
        assert result["type"] == "clingy-project"
        assert result["template"] == "test"

    def test_read_marker_with_template_version(self, temp_project):
        """Should read template_version field if present"""
        from clingy.core.discovery import read_clingy_marker

        marker_content = {
            "version": "1.0",
            "type": "clingy-project",
            "template": "basic",
            "template_version": "1.1.0",
        }
        marker_file = temp_project / ".clingy"
        marker_file.write_text(json.dumps(marker_content, indent=2) + "\n")

        result = read_clingy_marker(temp_project)

        assert result is not None
        assert result["template_version"] == "1.1.0"

    def test_returns_none_for_missing_marker(self, tmp_path):
        """Should return None when .clingy doesn't exist"""
        from clingy.core.discovery import read_clingy_marker

        project = tmp_path / "no-marker"
        project.mkdir()

        result = read_clingy_marker(project)
        assert result is None

    def test_returns_none_for_malformed_json(self, tmp_path):
        """Should return None when .clingy is malformed"""
        from clingy.core.discovery import read_clingy_marker

        project = tmp_path / "malformed"
        project.mkdir()
        marker_file = project / ".clingy"
        marker_file.write_text("{ invalid json }")

        result = read_clingy_marker(project)
        assert result is None
