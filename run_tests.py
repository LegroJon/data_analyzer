#!/usr/bin/env python3
"""
Test runner script for the data analyzer project.
Handles proper import paths and provides detailed test results.
"""

import sys
import os
from pathlib import Path

# Add project root and src to Python path
project_root = Path(__file__).parent
src_path = project_root / "src"
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(src_path))

# Change to project directory to ensure relative imports work
os.chdir(project_root)

# Import and run tests
if __name__ == "__main__":
    import unittest
    
    print("=" * 60)
    print("Data Analyzer - Test Suite")
    print("=" * 60)
    print(f"Project root: {project_root}")
    print(f"Python version: {sys.version}")
    print(f"Current directory: {os.getcwd()}")
    print("-" * 60)
    
    # Discover and run tests
    loader = unittest.TestLoader()
    start_dir = project_root / "tests"
    suite = loader.discover(str(start_dir), pattern="test_*.py")
    
    # Run tests with detailed output
    runner = unittest.TextTestRunner(
        verbosity=2,
        stream=sys.stdout,
        descriptions=True,
        failfast=False
    )
    
    result = runner.run(suite)
    
    print("-" * 60)
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Success: {result.wasSuccessful()}")
    print("=" * 60)
    
    # Exit with appropriate code
    sys.exit(0 if result.wasSuccessful() else 1)
