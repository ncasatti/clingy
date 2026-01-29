"""
Tests for context detection and project discovery
"""

from pathlib import Path

import pytest

from clingy.core.discovery import (
    find_clingy_root,
    get_project_context,
    load_project_config,
)


class TestFindManagerRoot:
    """Tests for find_clingy_root function"""

    def test_finds_project_in_current_directory(self, temp_project):
        """Should find project in current directory"""
        result = find_clingy_root(start_path=temp_project)
        assert result == temp_project

    def test_finds_project_walking_up_directories(self, temp_project):
        """Should walk up directories to find project root"""
        # Create nested subdirectories
        deep_dir = temp_project / "src" / "deep" / "nested"
        deep_dir.mkdir(parents=True)

        result = find_clingy_root(start_path=deep_dir)
        assert result == temp_project

    def test_returns_none_if_no_project_found(self, tmp_path):
        """Should return None if no project found"""
        # Create a directory with no project markers
        no_project = tmp_path / "no-project"
        no_project.mkdir()

        result = find_clingy_root(start_path=no_project)
        # Result should be None or a parent project (if one exists above)
        # The key is: it should not find a project in no_project itself
        if result is not None:
            assert result != no_project

    def test_stops_at_filesystem_root(self, tmp_path):
        """Should not search infinitely, stop at filesystem root"""
        # Create a deep nested directory with no project
        deep_dir = tmp_path / "a" / "b" / "c" / "d" / "e"
        deep_dir.mkdir(parents=True)

        result = find_clingy_root(start_path=deep_dir)
        # Should either find nothing or find a project above tmp_path
        # But should not crash
        assert result is None or isinstance(result, Path)

    def test_requires_both_commands_and_config(self, tmp_path):
        """Should require both commands/ and config.py to be valid"""
        # Project with only commands/
        project_no_config = tmp_path / "no-config"
        project_no_config.mkdir()
        (project_no_config / "commands").mkdir()

        result = find_clingy_root(start_path=project_no_config)
        # Should not find project_no_config as a valid project
        if result is not None:
            assert result != project_no_config

        # Project with only config.py
        project_no_commands = tmp_path / "no-commands"
        project_no_commands.mkdir()
        (project_no_commands / "config.py").write_text("PROJECT_NAME = 'Test'")

        result = find_clingy_root(start_path=project_no_commands)
        # Should not find project_no_commands as a valid project
        if result is not None:
            assert result != project_no_commands


class TestValidProjectDetection:
    """Tests for valid project detection logic"""

    def test_valid_project_root_found(self, temp_project_with_command):
        """Should find valid project root"""
        result = find_clingy_root(start_path=temp_project_with_command)
        assert result == temp_project_with_command

    def test_missing_commands_directory(self, tmp_path):
        """Should not find project if commands/ is missing"""
        project = tmp_path / "project"
        project.mkdir()
        (project / "config.py").write_text("PROJECT_NAME = 'Test'")

        result = find_clingy_root(start_path=project)
        # Should not identify this as a valid project
        if result is not None:
            assert result != project

    def test_missing_config_file(self, tmp_path):
        """Should not find project if config.py is missing"""
        project = tmp_path / "project"
        project.mkdir()
        commands = project / "commands"
        commands.mkdir()
        (commands / "test.py").write_text("# test")

        result = find_clingy_root(start_path=project)
        # Should not identify this as a valid project
        if result is not None:
            assert result != project

    def test_empty_commands_directory(self, tmp_path):
        """Should find project even if commands/ is empty"""
        import json

        project = tmp_path / "project"
        project.mkdir()
        (project / "commands").mkdir()
        (project / "commands" / "__init__.py").write_text("")
        (project / "config.py").write_text("PROJECT_NAME = 'Test'")
        (project / ".clingy").write_text(
            json.dumps({"version": "1.0", "type": "clingy-project"}, indent=2) + "\n"
        )

        result = find_clingy_root(start_path=project)
        assert result == project


class TestLoadProjectConfig:
    """Tests for load_project_config function"""

    def test_loads_config_successfully(self, temp_project):
        """Should load config.py and return dictionary"""
        config = load_project_config(temp_project)

        assert config is not None
        assert isinstance(config, dict)
        assert "PROJECT_NAME" in config
        assert config["PROJECT_NAME"] == "Test Project"
        assert "ITEMS" in config
        assert len(config["ITEMS"]) == 3

    def test_raises_error_for_missing_config(self, tmp_path):
        """Should raise ImportError if config.py doesn't exist"""
        project = tmp_path / "project"
        project.mkdir()

        with pytest.raises(ImportError):
            load_project_config(project)

    def test_raises_error_for_invalid_python(self, tmp_path):
        """Should raise error if config.py has syntax errors"""
        project = tmp_path / "project"
        project.mkdir()
        (project / "config.py").write_text("INVALID PYTHON CODE !!!")

        # Should raise some kind of error (ImportError or SyntaxError)
        with pytest.raises((ImportError, SyntaxError)):
            load_project_config(project)


class TestGetProjectContext:
    """Tests for get_project_context function"""

    def test_returns_context_for_valid_project(self, temp_project, monkeypatch):
        """Should return context dict with root and config for valid project"""
        # Mock find_clingy_root to return our temp project
        monkeypatch.setattr("clingy.core.discovery.find_clingy_root", lambda: temp_project)

        context = get_project_context()

        assert context is not None
        assert isinstance(context, dict)
        assert "root" in context
        assert "config" in context
        assert context["root"] == temp_project
        assert isinstance(context["config"], dict)

    def test_returns_none_for_no_project(self, monkeypatch):
        """Should return None if no project found"""
        # Mock find_clingy_root to return None
        monkeypatch.setattr("clingy.core.discovery.find_clingy_root", lambda: None)

        context = get_project_context()
        assert context is None
