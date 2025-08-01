# Data Analyzer - Technical Documentation

## Architecture Overview

The Data Analyzer follows a modular architecture with clear separation of concerns:

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Input Layer   │    │ Processing Layer│    │  Output Layer   │
│                 │    │                 │    │                 │
│ • File I/O      │───▶│ • Pattern Match │───▶│ • CSV Export    │
│ • Text Parsing  │    │ • Data Cleaning │    │ • File Writing  │
│ • Validation    │    │ • Deduplication │    │ • Formatting    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│ Configuration   │    │    Logging      │    │ Error Handling  │
│                 │    │                 │    │                 │
│ • Pattern Defs  │    │ • Progress Info │    │ • Exception Mgmt│
│ • Settings      │    │ • Debug Data    │    │ • User Feedback │
│ • Paths         │    │ • Error Reports │    │ • Graceful Fails│
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## Core Components

### 1. TaskParser Class
The main parser engine that handles:
- Text processing using regex patterns
- Data structure conversion
- Duplicate detection and removal
- Error handling and recovery

### 2. ParsedTask Dataclass
Represents a single parsed task with fields:
- `step`: Task step number or identifier
- `task`: Task code/identifier
- `title`: Descriptive title
- `proponent`: Responsible organization
- `status`: Current status (e.g., "Approved")
- `verb`: Action verb (for drill format)

### 3. TaskPatternConfig Class
Manages regex patterns for different data formats:
- Pattern storage and retrieval
- Pattern validation
- Format type management

### 4. Configuration Module
Handles application settings:
- File paths and directories
- Default values
- System constraints

## Data Flow

```
Input File (.txt)
      │
      ▼
File Reading & Validation
      │
      ▼
Pattern Matching (Regex)
      │
      ▼
Data Structure Creation (ParsedTask)
      │
      ▼
Duplicate Removal
      │
      ▼
CSV Generation
      │
      ▼
Output File (.csv)
```

## Pattern Matching Details

### Original Format Pattern
Matches military task entries like:
```
1. 07-CO-3036 Integrate Indirect Fire Support - Company 07 - Infantry (Collective) Approved
```

Regex breakdown:
- `(?:(?P<step>\d+)\.\s)?` - Optional step number with period
- `(?P<task>\S+)` - Task identifier (non-whitespace)
- `(?P<title>.+?)` - Task title (non-greedy)
- `(?P<proponent>\d{2,3}\s-\s.+?)` - Proponent organization
- `(?P<status>Approved)` - Status field

### Drill Format Pattern
Matches battle drill entries like:
```
D8005 Approved React Direct Fire Contact While Mounted
```

Regex breakdown:
- `^\s*(?:\d+\.\s+)?` - Optional leading number
- `(?P<step>[\w-]+)` - Drill identifier
- `(?P<status>\S+)` - Status
- `(?P<verb>\S+)` - Action verb
- `(?P<title>.*)` - Drill description

## Error Handling Strategy

### File Operations
- FileNotFoundError: Clear message with path
- IOError: Detailed error with context
- Encoding issues: Fallback strategies

### Pattern Matching
- Regex compilation errors: Skip invalid patterns
- No matches found: Informative user feedback
- Partial matches: Graceful handling

### Data Processing
- Invalid data structures: Skip and log
- Memory constraints: Chunk processing
- Type conversion errors: Default values

## Performance Considerations

### Memory Usage
- Streaming file reading for large files
- Generator patterns for data processing
- Efficient duplicate detection using sets

### Processing Speed
- Compiled regex patterns
- Optimized data structures
- Minimal string operations

### Scalability
- Support for files up to 100MB
- Configurable batch sizes
- Progress reporting for long operations

## Testing Strategy

### Unit Tests
- Individual function testing
- Edge case validation
- Error condition testing

### Integration Tests
- End-to-end workflow testing
- File I/O validation
- Pattern matching verification

### Performance Tests
- Large file processing
- Memory usage monitoring
- Speed benchmarking

## Configuration Management

### Pattern Configuration
Patterns stored in `config/settings.ini`:
```ini
[patterns]
original_patterns = [
    "pattern1",
    "pattern2"
]
```

### Runtime Settings
Configurable via `src/config.py`:
- File size limits
- Encoding preferences
- Output formats
- Logging levels

## Logging Framework

### Log Levels
- **DEBUG**: Detailed processing information
- **INFO**: General progress updates
- **WARNING**: Non-critical issues
- **ERROR**: Serious problems
- **CRITICAL**: System failures

### Log Format
```
2025-08-01 10:30:45 - task_parser - INFO - Successfully parsed 25 tasks
```

## Deployment Guidelines

### Prerequisites
- Python 3.8 or higher
- Standard library only (no external dependencies)
- Windows, macOS, or Linux

### Installation Steps
1. Extract/clone repository
2. Verify Python installation
3. Optional: Install development dependencies
4. Run initial tests

### Usage Patterns
- Command-line execution via `run_parser.bat`
- Python API integration
- Batch processing scripts

## Maintenance and Updates

### Adding New Patterns
1. Define regex in `TaskPatternConfig`
2. Add corresponding format type
3. Update documentation
4. Create test cases

### Performance Optimization
- Profile with `cProfile`
- Monitor memory usage
- Optimize regex patterns
- Consider multiprocessing for large datasets

### Bug Reporting
Include:
- Input file sample
- Expected output
- Actual output
- Error messages
- System information

## Security Considerations

### Input Validation
- File size limits
- Path traversal prevention
- Encoding validation
- Pattern complexity limits

### Output Security
- Safe file writing
- Path validation
- Permission handling
- Data sanitization

## Future Enhancements

### Planned Features
- Database integration
- Web interface
- Advanced analytics
- Multi-format support

### Architecture Evolution
- Plugin system for patterns
- Distributed processing
- Real-time processing
- API endpoints

This documentation provides a comprehensive technical overview of the Data Analyzer system architecture and implementation details.
