# Data Analyzer

A professional-grade Python project for extracting, processing, and analyzing military task data from text documents. This tool uses configurable regex patterns to parse structured data and export results to CSV format.

## Features

- **Flexible Pattern Matching**: Support for multiple regex patterns to handle different data formats
- **Robust Error Handling**: Comprehensive error handling and logging
- **Data Deduplication**: Automatic removal of duplicate entries
- **Multiple Output Formats**: Configurable CSV output with headers
- **Extensible Architecture**: Modular design for easy pattern additions
- **Comprehensive Testing**: Full test suite with unit and integration tests

## Project Structure

```
data_analyzer/
├── src/                    # Source code
│   ├── __init__.py        # Package initialization
│   ├── task_parser.py     # Main parser module
│   └── config.py          # Configuration settings
├── data/                  # Data directories
│   ├── input/             # Input text files
│   └── output/            # Generated CSV files
├── tests/                 # Test suite
│   └── test_task_parser.py
├── docs/                  # Documentation
├── config/                # Configuration files
├── requirements.txt       # Python dependencies
├── setup.py              # Package setup
├── README.md             # This file
└── LICENSE               # License information
```

## Installation (Optional)

The project works without any external dependencies using only Python's standard library.

For development or enhanced features:
1. Clone or download the repository
2. Install development dependencies (optional):
   ```bash
   pip install -r requirements.txt
   ```
3. For development installation (optional):
   ```bash
   pip install -e .
   ```

## Usage

### Command Line Interface

```bash
python src/task_parser.py
```

The script will prompt you for:
- Path to input text file
- Pattern type (original/drill)

### Python API

```python
from src.task_parser import TaskParser

# Initialize parser
parser = TaskParser()

# Parse a file
tasks = parser.parse_file("input.txt", "original")

# Save results
parser.save_to_csv(tasks, "output.csv", "original")
```

### Pattern Types

1. **Original**: Parses military task data with step, task ID, title, proponent, and status
2. **Drill**: Parses battle drill data with step, status, verb, and title

## Supported Input Formats

### Original Format
```
1. 07-CO-3036 Integrate Indirect Fire Support - Company 07 - Infantry (Collective) Approved
2. 71-CO-5100 Conduct Troop Leading Procedures 71 - Mission Command (Collective) Approved
```

### Drill Format
```
D8005 Approved React Direct Fire Contact While Mounted
D9508 Approved Establish Security at the Halt
```

## Output Format

CSV files with appropriate headers based on pattern type:

**Original Format:**
- Step, Task, Title, Proponent, Status

**Drill Format:**
- Step, Status, Verb, Title

## Testing

Run the test suite:

```bash
python -m pytest tests/
```

Or run specific tests:

```bash
python tests/test_task_parser.py
```

## Configuration

The `src/config.py` file contains default settings that can be modified:

- File paths and directories
- Default encodings and formats
- Logging configuration
- Pattern validation settings

## Error Handling

The parser includes comprehensive error handling for:
- File not found errors
- Invalid pattern types
- Regex compilation errors
- I/O exceptions
- Invalid file formats

## Logging

Built-in logging provides detailed information about:
- Parsing progress
- Duplicate removal
- Error conditions
- File operations

## Contributing

1. Ensure all tests pass
2. Follow PEP 8 style guidelines
3. Add tests for new features
4. Update documentation as needed

## Performance

The parser is optimized for:
- Large text files (up to 100MB)
- Multiple pattern matching
- Memory-efficient duplicate removal
- Fast CSV generation

## Future Enhancements

- Support for additional input formats (JSON, XML)
- Database integration
- Web interface
- Advanced analytics and reporting
- Batch processing capabilities

## License

Proprietary License - See LICENSE file for details.

## Author

Jonathan Legro - 2025

## Version History

- **1.0.0** (2025-08-01): Initial release with core parsing functionality






