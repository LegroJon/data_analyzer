"""
Test suite for the task parser module.

Tests various parsing scenarios, error handling, and edge cases.
"""

import unittest
import tempfile
import os
from unittest.mock import patch, mock_open
import sys
from pathlib import Path

# Add src directory to path for imports
project_root = Path(__file__).parent.parent
src_path = project_root / "src"
if str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))

# Also add the project root to handle different import scenarios
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

try:
    from task_parser import TaskParser, ParsedTask, TaskPatternConfig, generate_output_filename
except ImportError as e:
    print(f"Import error: {e}")
    print(f"Current working directory: {os.getcwd()}")
    print(f"Python path: {sys.path}")
    print(f"Looking for module in: {src_path}")
    print(f"Project root: {project_root}")
    print(f"Files in src directory: {list(src_path.glob('*.py')) if src_path.exists() else 'src directory does not exist'}")
    raise


class TestParsedTask(unittest.TestCase):
    """Test cases for ParsedTask class."""
    
    def test_to_list_original_format(self):
        """Test conversion to list for original format."""
        task = ParsedTask(
            step="1",
            task="07-CO-3036",
            title="Test Task",
            proponent="07 - Infantry",
            status="Approved"
        )
        expected = ["1", "07-CO-3036", "Test Task", "07 - Infantry", "Approved"]
        self.assertEqual(task.to_list("original"), expected)
    
    def test_to_list_drill_format(self):
        """Test conversion to list for drill format."""
        task = ParsedTask(
            step="D8005",
            status="Approved",
            verb="React",
            title="Direct Fire Contact"
        )
        expected = ["D8005", "Approved", "React", "Direct Fire Contact"]
        self.assertEqual(task.to_list("drill"), expected)


class TestTaskPatternConfig(unittest.TestCase):
    """Test cases for TaskPatternConfig class."""
    
    def test_get_patterns_valid_type(self):
        """Test getting patterns for valid type."""
        patterns = TaskPatternConfig.get_patterns("original")
        self.assertIsInstance(patterns, list)
        self.assertTrue(len(patterns) > 0)
    
    def test_get_patterns_invalid_type(self):
        """Test getting patterns for invalid type."""
        patterns = TaskPatternConfig.get_patterns("invalid")
        self.assertEqual(patterns, [])
    
    def test_get_available_types(self):
        """Test getting available pattern types."""
        types = TaskPatternConfig.get_available_types()
        self.assertIn("original", types)
        self.assertIn("drill", types)


class TestTaskParser(unittest.TestCase):
    """Test cases for TaskParser class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.parser = TaskParser()
        self.sample_original_text = """
        1. 07-CO-3036 Integrate Indirect Fire Support - Company 07 - Infantry (Collective) Approved
        2. 71-CO-5100 Conduct Troop Leading Procedures 71 - Mission Command (Collective) Approved
        """
        self.sample_drill_text = """
        D8005 Approved React Direct Fire Contact While Mounted
        D9508 Approved Establish Security at the Halt
        """
    
    def test_parse_text_original_format(self):
        """Test parsing text with original format."""
        tasks = self.parser.parse_text(self.sample_original_text, "original")
        self.assertTrue(len(tasks) > 0)
        self.assertEqual(tasks[0].step, "1")
        self.assertEqual(tasks[0].task, "07-CO-3036")
    
    def test_parse_text_invalid_type(self):
        """Test parsing with invalid pattern type."""
        with self.assertRaises(ValueError):
            self.parser.parse_text("test", "invalid_type")
    
    def test_remove_duplicates(self):
        """Test duplicate removal functionality."""
        # Create duplicate tasks
        task1 = ParsedTask(step="1", task="TEST", title="Test Task")
        task2 = ParsedTask(step="1", task="TEST", title="Test Task")  # Duplicate
        task3 = ParsedTask(step="2", task="TEST2", title="Different Task")
        
        tasks = [task1, task2, task3]
        unique_tasks = self.parser.remove_duplicates(tasks)
        
        self.assertEqual(len(unique_tasks), 2)
    
    def test_parse_file_not_found(self):
        """Test parsing non-existent file."""
        with self.assertRaises(FileNotFoundError):
            self.parser.parse_file("nonexistent.txt", "original")
    
    @patch("builtins.open", new_callable=mock_open, read_data="test content")
    @patch("os.path.isfile", return_value=True)
    def test_parse_file_success(self, mock_isfile, mock_file):
        """Test successful file parsing."""
        with patch.object(self.parser, 'parse_text', return_value=[]) as mock_parse:
            tasks = self.parser.parse_file("test.txt", "original")
            mock_parse.assert_called_once_with("test content", "original")
    
    def test_save_to_csv(self):
        """Test saving tasks to CSV file."""
        tasks = [
            ParsedTask(step="1", task="TEST", title="Test Task", status="Approved"),
            ParsedTask(step="2", task="TEST2", title="Test Task 2", status="Approved")
        ]
        
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.csv') as tmp:
            tmp_path = tmp.name
        
        try:
            self.parser.save_to_csv(tasks, tmp_path, "original", include_headers=True)
            
            # Verify file was created and has content
            self.assertTrue(os.path.exists(tmp_path))
            
            with open(tmp_path, 'r', encoding='utf-8') as f:
                content = f.read()
                self.assertIn("Step", content)  # Header
                self.assertIn("TEST", content)  # Data
                
        finally:
            os.unlink(tmp_path)


class TestUtilityFunctions(unittest.TestCase):
    """Test cases for utility functions."""
    
    def test_generate_output_filename(self):
        """Test output filename generation."""
        input_path = "/path/to/input.txt"
        output_filename = generate_output_filename(input_path, "test")
        
        self.assertIn("input_test", output_filename)
        self.assertTrue(output_filename.endswith(".csv"))
        self.assertTrue(len(output_filename) > len("input_test.csv"))  # Should include timestamp


class TestIntegration(unittest.TestCase):
    """Integration tests for the complete parsing workflow."""
    
    def test_full_parsing_workflow(self):
        """Test complete parsing workflow from file to CSV."""
        parser = TaskParser()
        
        # Create temporary input file
        test_content = "1. 07-CO-3036 Test Task 07 - Infantry (Collective) Approved"
        
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as input_file:
            input_file.write(test_content)
            input_path = input_file.name
        
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.csv') as output_file:
            output_path = output_file.name
        
        try:
            # Parse file
            tasks = parser.parse_file(input_path, "original")
            self.assertTrue(len(tasks) > 0)
            
            # Save to CSV
            parser.save_to_csv(tasks, output_path, "original")
            
            # Verify output
            self.assertTrue(os.path.exists(output_path))
            
        finally:
            os.unlink(input_path)
            os.unlink(output_path)


if __name__ == '__main__':
    # Create test suite
    test_suite = unittest.TestLoader().loadTestsFromModule(sys.modules[__name__])
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    
    # Exit with error code if tests failed
    sys.exit(0 if result.wasSuccessful() else 1)
