"""
Tests for the init command
"""
import pytest
from pathlib import Path
from argparse import Namespace
from manager_core.commands.init import InitCommand


class TestInitCommand:
    """Tests for InitCommand"""
    
    def test_creates_project_structure(self, tmp_path):
        """Should create commands/ and config.py"""
        init_cmd = InitCommand()
        
        # Change to temp directory
        import os
        original_cwd = os.getcwd()
        os.chdir(tmp_path)
        
        try:
            # Execute init
            args = Namespace(force=False, template="basic")
            result = init_cmd.execute(args)
            
            # Verify success
            assert result is True
            
            # Verify structure
            assert (tmp_path / "commands").exists()
            assert (tmp_path / "commands" / "__init__.py").exists()
            assert (tmp_path / "config.py").exists()
            
        finally:
            os.chdir(original_cwd)
    
    def test_creates_template_basic(self, tmp_path):
        """Should create basic template with example commands"""
        init_cmd = InitCommand()
        
        import os
        original_cwd = os.getcwd()
        os.chdir(tmp_path)
        
        try:
            args = Namespace(force=False, template="basic")
            result = init_cmd.execute(args)
            
            assert result is True
            
            # Verify template files exist
            commands_dir = tmp_path / "commands"
            assert (commands_dir / "greet.py").exists()
            assert (commands_dir / "info.py").exists()
            assert (commands_dir / "calculator.py").exists()
            
        finally:
            os.chdir(original_cwd)
    
    def test_fails_if_project_already_exists(self, temp_project):
        """Should fail if commands/ already exists (without --force)"""
        init_cmd = InitCommand()
        
        import os
        original_cwd = os.getcwd()
        os.chdir(temp_project)
        
        try:
            args = Namespace(force=False, template="basic")
            result = init_cmd.execute(args)
            
            # Should fail because project already exists
            assert result is False
            
        finally:
            os.chdir(original_cwd)
    
    def test_force_flag_overwrites_existing(self, temp_project):
        """Should overwrite existing project with --force"""
        init_cmd = InitCommand()
        
        # Add a custom file to commands/
        custom_file = temp_project / "commands" / "custom.py"
        custom_file.write_text("# Custom command")
        
        import os
        original_cwd = os.getcwd()
        os.chdir(temp_project)
        
        try:
            args = Namespace(force=True, template="basic")
            result = init_cmd.execute(args)
            
            assert result is True
            
            # Custom file should be gone (commands/ was recreated)
            assert not custom_file.exists()
            
            # Template files should exist
            assert (temp_project / "commands" / "greet.py").exists()
            
        finally:
            os.chdir(original_cwd)
    
    def test_invalid_template_fails(self, tmp_path):
        """Should fail gracefully for invalid template name"""
        init_cmd = InitCommand()
        
        import os
        original_cwd = os.getcwd()
        os.chdir(tmp_path)
        
        try:
            args = Namespace(force=False, template="nonexistent-template")
            result = init_cmd.execute(args)
            
            # Should fail
            assert result is False
            
            # Should not create partial structure
            assert not (tmp_path / "commands").exists()
            
        finally:
            os.chdir(original_cwd)
    
    def test_command_has_correct_name(self):
        """Command should have name 'init'"""
        init_cmd = InitCommand()
        assert init_cmd.name == "init"
    
    def test_command_has_help_text(self):
        """Command should have help text"""
        init_cmd = InitCommand()
        assert init_cmd.help is not None
        assert len(init_cmd.help) > 0
