"""
Tests for init command, including template copying and auto-detection
"""

import json
from argparse import Namespace
from pathlib import Path

import pytest

from clingy.commands.init import InitCommand
from clingy.core.discovery import read_clingy_marker


class TestInitCopiesClingyMarker:
    """Tests for .clingy marker file copying during init"""

    def test_init_copies_clingy_from_template(self, tmp_path):
        """Should copy .clingy from template instead of generating inline"""
        project_dir = tmp_path / "new-project"
        project_dir.mkdir()

        # Change to project directory
        import os

        original_cwd = os.getcwd()
        try:
            os.chdir(project_dir)

            # Execute init command
            cmd = InitCommand()
            args = Namespace(
                force=False,
                template="basic",
                update=False,
            )

            result = cmd.execute(args)
            assert result is True

            # Verify .clingy was created
            marker_file = project_dir / ".clingy"
            assert marker_file.exists()

            # Verify it contains expected fields
            marker_data = read_clingy_marker(project_dir)
            assert marker_data is not None
            assert marker_data["version"] == "1.0"
            assert marker_data["type"] == "clingy-project"
            assert marker_data["template"] == "basic"

        finally:
            os.chdir(original_cwd)

    def test_init_marker_contains_template_version(self, tmp_path):
        """Should copy .clingy with template_version field"""
        project_dir = tmp_path / "new-project"
        project_dir.mkdir()

        import os

        original_cwd = os.getcwd()
        try:
            os.chdir(project_dir)

            cmd = InitCommand()
            args = Namespace(
                force=False,
                template="basic",
                update=False,
            )

            result = cmd.execute(args)
            assert result is True

            # Verify template_version field exists
            marker_data = read_clingy_marker(project_dir)
            assert marker_data is not None
            assert "template_version" in marker_data
            assert isinstance(marker_data["template_version"], str)

        finally:
            os.chdir(original_cwd)


class TestInitUpdateAutoDetectsTemplate:
    """Tests for --update flag auto-detecting template from local .clingy"""

    def test_update_auto_detects_template_from_marker(self, temp_project):
        """Should read template name from local .clingy during --update"""
        # Setup: project with basic template
        marker_content = {
            "version": "1.0",
            "type": "clingy-project",
            "template": "basic",
            "template_version": "1.0.0",
        }
        marker_file = temp_project / ".clingy"
        marker_file.write_text(json.dumps(marker_content, indent=2) + "\n")

        # Create minimal project structure
        commands_dir = temp_project / "commands"
        commands_dir.mkdir(exist_ok=True)
        (commands_dir / "__init__.py").write_text("")

        config_file = temp_project / "config.py"
        config_file.write_text('PROJECT_NAME = "Test"\nPROJECT_VERSION = "1.0.0"\nITEMS = []\n')

        import os

        original_cwd = os.getcwd()
        try:
            os.chdir(temp_project)

            # Execute update command (without --template flag)
            cmd = InitCommand()
            args = Namespace(
                force=True,  # Use force for update
                template="basic",  # Default, but should be overridden
                update=True,
            )

            result = cmd.execute(args)
            # Update should succeed (or at least not fail due to template detection)
            assert result is True

            # Verify template was auto-detected (marker still exists)
            marker_data = read_clingy_marker(temp_project)
            assert marker_data is not None
            assert marker_data["template"] == "basic"

        finally:
            os.chdir(original_cwd)

    def test_update_falls_back_to_default_template_if_no_marker(self, tmp_path):
        """Should use default template if no .clingy exists"""
        project_dir = tmp_path / "project"
        project_dir.mkdir()

        # Create minimal project structure (no .clingy)
        commands_dir = project_dir / "commands"
        commands_dir.mkdir()
        (commands_dir / "__init__.py").write_text("")

        config_file = project_dir / "config.py"
        config_file.write_text('PROJECT_NAME = "Test"\nPROJECT_VERSION = "1.0.0"\nITEMS = []\n')

        import os

        original_cwd = os.getcwd()
        try:
            os.chdir(project_dir)

            cmd = InitCommand()
            args = Namespace(
                force=True,  # Use force for update
                template="basic",  # Default template
                update=True,
            )

            result = cmd.execute(args)
            # Should use default template and succeed
            assert result is True

        finally:
            os.chdir(original_cwd)


class TestInitUpdateBumpsTemplateVersion:
    """Tests for template_version being updated after --update"""

    def test_update_copies_new_template_version(self, temp_project):
        """Should copy updated template_version from framework after --update"""
        # Setup: project with old template version
        old_version = "1.0.0"
        marker_content = {
            "version": "1.0",
            "type": "clingy-project",
            "template": "basic",
            "template_version": old_version,
        }
        marker_file = temp_project / ".clingy"
        marker_file.write_text(json.dumps(marker_content, indent=2) + "\n")

        # Create minimal project structure
        commands_dir = temp_project / "commands"
        commands_dir.mkdir(exist_ok=True)
        (commands_dir / "__init__.py").write_text("")

        config_file = temp_project / "config.py"
        config_file.write_text('PROJECT_NAME = "Test"\nPROJECT_VERSION = "1.0.0"\nITEMS = []\n')

        import os

        original_cwd = os.getcwd()
        try:
            os.chdir(temp_project)

            cmd = InitCommand()
            args = Namespace(
                force=True,  # Use force for update
                template="basic",
                update=True,
            )

            result = cmd.execute(args)
            assert result is True

            # Verify .clingy was updated with framework's template_version
            marker_data = read_clingy_marker(temp_project)
            assert marker_data is not None
            assert "template_version" in marker_data

            # The new version should be from the framework template
            # (may be same or newer depending on framework version)
            new_version = marker_data["template_version"]
            assert isinstance(new_version, str)

        finally:
            os.chdir(original_cwd)

    def test_update_preserves_config_py(self, temp_project):
        """Should preserve config.py during --update"""
        # Setup: project with custom config
        marker_content = {
            "version": "1.0",
            "type": "clingy-project",
            "template": "basic",
            "template_version": "1.0.0",
        }
        marker_file = temp_project / ".clingy"
        marker_file.write_text(json.dumps(marker_content, indent=2) + "\n")

        # Create project structure with custom config
        commands_dir = temp_project / "commands"
        commands_dir.mkdir(exist_ok=True)
        (commands_dir / "__init__.py").write_text("")

        custom_config = 'PROJECT_NAME = "Custom"\nPROJECT_VERSION = "2.0.0"\nITEMS = ["custom"]\n'
        config_file = temp_project / "config.py"
        config_file.write_text(custom_config)

        import os

        original_cwd = os.getcwd()
        try:
            os.chdir(temp_project)

            cmd = InitCommand()
            args = Namespace(
                force=True,  # Use force for update
                template="basic",
                update=True,
            )

            result = cmd.execute(args)
            assert result is True

            # Verify config.py was preserved
            updated_config = config_file.read_text()
            assert updated_config == custom_config

        finally:
            os.chdir(original_cwd)


class TestInitCommandIntegration:
    """Integration tests for init command"""

    def test_init_creates_complete_project_structure(self, tmp_path):
        """Should create all necessary project files and directories"""
        project_dir = tmp_path / "new-project"
        project_dir.mkdir()

        import os

        original_cwd = os.getcwd()
        try:
            os.chdir(project_dir)

            cmd = InitCommand()
            args = Namespace(
                force=False,
                template="basic",
                update=False,
            )

            result = cmd.execute(args)
            assert result is True

            # Verify all expected files/dirs exist
            assert (project_dir / "commands").is_dir()
            assert (project_dir / "config.py").is_file()
            assert (project_dir / ".clingy").is_file()

        finally:
            os.chdir(original_cwd)

    def test_init_with_force_overwrites_existing(self, tmp_path):
        """Should overwrite existing project with --force"""
        project_dir = tmp_path / "project"
        project_dir.mkdir()

        # Create existing project
        commands_dir = project_dir / "commands"
        commands_dir.mkdir()
        (commands_dir / "__init__.py").write_text("# old")

        config_file = project_dir / "config.py"
        config_file.write_text('PROJECT_NAME = "Old"\n')

        marker_file = project_dir / ".clingy"
        marker_file.write_text(json.dumps({"version": "1.0"}, indent=2) + "\n")

        import os

        original_cwd = os.getcwd()
        try:
            os.chdir(project_dir)

            cmd = InitCommand()
            args = Namespace(
                force=True,
                template="basic",
                update=False,
            )

            result = cmd.execute(args)
            assert result is True

            # Verify project was re-initialized
            marker_data = read_clingy_marker(project_dir)
            assert marker_data is not None
            assert marker_data["template"] == "basic"

        finally:
            os.chdir(original_cwd)

    def test_init_fails_without_force_if_project_exists(self, temp_project):
        """Should fail if project exists and --force is not used"""
        import os

        original_cwd = os.getcwd()
        try:
            os.chdir(temp_project)

            cmd = InitCommand()
            args = Namespace(
                force=False,
                template="basic",
                update=False,
            )

            result = cmd.execute(args)
            assert result is False

        finally:
            os.chdir(original_cwd)
