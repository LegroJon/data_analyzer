"""
Task Parser Module

A robust module for parsing military task data from text files using configurable
regex patterns. Supports multiple output formats and includes comprehensive error handling.

Author: Jonathan Legro
Date: 2025-08-01
"""

import csv
import re
import os
import logging
from datetime import datetime
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass


@dataclass
class ParsedTask:
    """Data class representing a parsed task."""
    step: str = ""
    task: str = ""
    title: str = ""
    proponent: str = ""
    status: str = ""
    verb: str = ""
    
    def to_list(self, format_type: str = "original") -> List[str]:
        """Convert to list format based on parsing type."""
        if format_type == "original":
            return [self.step, self.task, self.title, self.proponent, self.status]
        elif format_type == "drill":
            return [self.step, self.status, self.verb, self.title]
        else:
            return [self.step, self.task, self.title, self.proponent, self.status]


class TaskPatternConfig:
    """Configuration class for regex patterns."""
    
    PATTERNS = {
        'original': [
            r'(?:(?P<step>\d+)\.\s)?(?P<task>\S+)\s(?P<title>.+?)\s(?P<proponent>\d{2,3}\s-\s.+?)\s(?P<status>Approved)',
            r'(?:(?P<step>\d+)-PLT-)?(?P<task>\S+)\s(?P<title>.+?)\sBattle Drill\s(?P<proponent>\d{2,3}\s-\s.+?)\s(?P<status>Approved)'
        ],
        'drill': [
            r'^\s*(?:\d+\.\s+)?(?P<step>[\w-]+)\s+(?P<status>\S+)\s+(?P<verb>\S+)\s+(?P<title>.*)'
        ]
    }
    
    @classmethod
    def get_patterns(cls, pattern_type: str) -> List[str]:
        """Get patterns for a specific type."""
        return cls.PATTERNS.get(pattern_type, [])
    
    @classmethod
    def get_available_types(cls) -> List[str]:
        """Get list of available pattern types."""
        return list(cls.PATTERNS.keys())


class TaskParser:
    """Main parser class for task data extraction."""
    
    def __init__(self, log_level: int = logging.INFO):
        """Initialize the parser with logging configuration."""
        self.logger = self._setup_logging(log_level)
        self.patterns = TaskPatternConfig()
    
    def _setup_logging(self, level: int) -> logging.Logger:
        """Set up logging configuration."""
        logger = logging.getLogger(__name__)
        logger.setLevel(level)
        
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)
        
        return logger
    
    def parse_text(self, text: str, pattern_type: str) -> List[ParsedTask]:
        """
        Parse text using specified pattern type.
        
        Args:
            text: The text content to parse
            pattern_type: Type of patterns to use ('original' or 'drill')
            
        Returns:
            List of ParsedTask objects
            
        Raises:
            ValueError: If pattern_type is not supported
        """
        if pattern_type not in self.patterns.get_available_types():
            raise ValueError(f"Unsupported pattern type: {pattern_type}")
        
        patterns = self.patterns.get_patterns(pattern_type)
        parsed_tasks = []
        
        self.logger.info(f"Parsing text with {len(patterns)} patterns of type '{pattern_type}'")
        
        for pattern in patterns:
            try:
                matches = re.finditer(pattern, text, re.MULTILINE)
                for match in matches:
                    task = ParsedTask()
                    groups = match.groupdict()
                    
                    # Populate task fields based on available groups
                    for field in ['step', 'task', 'title', 'proponent', 'status', 'verb']:
                        if field in groups and groups[field]:
                            setattr(task, field, groups[field].strip())
                    
                    parsed_tasks.append(task)
                    
            except re.error as e:
                self.logger.error(f"Regex error with pattern '{pattern}': {e}")
                continue
        
        self.logger.info(f"Successfully parsed {len(parsed_tasks)} tasks")
        return parsed_tasks
    
    def remove_duplicates(self, tasks: List[ParsedTask], format_type: str = "original") -> List[ParsedTask]:
        """
        Remove duplicate tasks based on their list representation.
        
        Args:
            tasks: List of ParsedTask objects
            format_type: Format type for comparison
            
        Returns:
            List of unique ParsedTask objects
        """
        unique_tasks = []
        seen = set()
        
        for task in tasks:
            task_tuple = tuple(task.to_list(format_type))
            if task_tuple not in seen:
                seen.add(task_tuple)
                unique_tasks.append(task)
        
        removed_count = len(tasks) - len(unique_tasks)
        if removed_count > 0:
            self.logger.info(f"Removed {removed_count} duplicate tasks")
        
        return unique_tasks
    
    def parse_file(self, file_path: str, pattern_type: str) -> List[ParsedTask]:
        """
        Parse a text file and return extracted tasks.
        
        Args:
            file_path: Path to the input text file
            pattern_type: Type of patterns to use
            
        Returns:
            List of ParsedTask objects
            
        Raises:
            FileNotFoundError: If file doesn't exist
            IOError: If file cannot be read
        """
        if not os.path.isfile(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                text = f.read()
            
            self.logger.info(f"Successfully read file: {file_path}")
            tasks = self.parse_text(text, pattern_type)
            return self.remove_duplicates(tasks, pattern_type)
            
        except IOError as e:
            self.logger.error(f"Error reading file {file_path}: {e}")
            raise
    
    def save_to_csv(self, tasks: List[ParsedTask], output_path: str, 
                   format_type: str = "original", include_headers: bool = True) -> None:
        """
        Save parsed tasks to CSV file.
        
        Args:
            tasks: List of ParsedTask objects to save
            output_path: Path for output CSV file
            format_type: Format type for output
            include_headers: Whether to include column headers
            
        Raises:
            IOError: If file cannot be written
        """
        try:
            with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                
                # Add headers if requested
                if include_headers:
                    if format_type == "original":
                        headers = ["Step", "Task", "Title", "Proponent", "Status"]
                    elif format_type == "drill":
                        headers = ["Step", "Status", "Verb", "Title"]
                    else:
                        headers = ["Step", "Task", "Title", "Proponent", "Status"]
                    writer.writerow(headers)
                
                # Write task data
                for task in tasks:
                    writer.writerow(task.to_list(format_type))
            
            self.logger.info(f"Successfully saved {len(tasks)} tasks to {output_path}")
            
        except IOError as e:
            self.logger.error(f"Error writing to file {output_path}: {e}")
            raise


def generate_output_filename(input_path: str, suffix: str = "parsed") -> str:
    """
    Generate an output filename based on input path.
    
    Args:
        input_path: Path to input file
        suffix: Suffix to add to filename
        
    Returns:
        Generated output filename
    """
    base_name = os.path.splitext(os.path.basename(input_path))[0]
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"{base_name}_{suffix}_{timestamp}.csv"


# Example usage and backwards compatibility
def main():
    """Main function for command-line usage."""
    parser = TaskParser()
    
    try:
        # Get input file
        input_file = input("Enter the path to your text file (.txt): ").strip()
        
        # Get pattern type
        available_types = TaskPatternConfig.get_available_types()
        print(f"Available pattern types: {', '.join(available_types)}")
        pattern_choice = input("Enter pattern type (original/drill): ").strip().lower()
        
        if pattern_choice not in available_types:
            print(f"Error: Invalid pattern type. Choose from: {', '.join(available_types)}")
            return
        
        # Parse tasks
        tasks = parser.parse_file(input_file, pattern_choice)
        
        if not tasks:
            print("No tasks found with the specified patterns.")
            return
        
        # Generate output filename
        output_file = generate_output_filename(input_file)
        output_path = os.path.join(os.path.dirname(input_file), output_file)
        
        # Save results
        parser.save_to_csv(tasks, output_path, pattern_choice)
        print(f"Successfully processed {len(tasks)} tasks and saved to '{output_file}'")
        
    except (FileNotFoundError, IOError, ValueError) as e:
        print(f"Error: {e}")
    except KeyboardInterrupt:
        print("\nOperation cancelled by user.")
    except Exception as e:
        print(f"Unexpected error: {e}")


if __name__ == "__main__":
    main()
